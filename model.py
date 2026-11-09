"""Foreguild 12-month model, driven by buyers. All inputs are assumptions stated in the plan (section 4).

GMV = active buyers x monthly spend per buyer. Revenue counts the free first brief and the 12% retainer fee.
Cash adds one-off costs, the assurance reserve and locked market liquidity, so the funding need is explicit.
"""
import json

FEE, RETAINER_FEE = 0.15, 0.12
ASSURE_RATE, ATTACH, CLAIMS = 0.06, 0.60, 0.02      # premium, share of GMV assured, claims as share of GMV
VAR_COST = 0.055                                    # verifier 1.0 + audit/jury 1.5 + forecasters 1.0 + intake 0.5 + rework 1.5
FIXED = 10_000                                      # infra 3k + market liquidity loss 2k + growth 5k per month
ONE_OFF = {1: 14_000}                               # escrow audit 8k + legal entity 6k
FIRST_BRIEF = 250                                   # first brief per new buyer is fee-free
SPEND_NEW, SPEND = 800, 1_600                       # monthly spend: first month, then later months
RETENTION = 0.80                                    # share of active buyers still buying next month
RETAINER_SHARE = lambda m: 0.0 if m < 4 else 0.30   # share of GMV on prepaid 12% Guild Contracts
RESERVE_MULT = 3                                    # assurance reserve = 3 x expected monthly claims
LIQ_LOCKED = 3_000                                  # seed liquidity locked in open markets from month 2
NEW0 = [6, 10, 14]                                  # new outside buyers in months 1-3
SCEN = {"conservative": 0.05, "base": 0.15, "upside": 0.25}   # monthly growth of new buyers from month 4


def run(g):
    rows, active, reserve, cum = [], 0.0, 0.0, 0.0
    new = NEW0[:]
    for m in range(4, 13):
        new.append(new[-1] * (1 + g))
    for m in range(1, 13):
        n = new[m - 1]
        gmv = active * SPEND + n * SPEND_NEW
        r = RETAINER_SHARE(m)
        fee = gmv * ((1 - r) * FEE + r * RETAINER_FEE) - n * FIRST_BRIEF * FEE
        gnr = fee + gmv * (ASSURE_RATE * ATTACH - CLAIMS)
        op = gnr - gmv * VAR_COST - FIXED
        need = RESERVE_MULT * gmv * CLAIMS
        cash = op - ONE_OFF.get(m, 0) - (need - reserve) - (LIQ_LOCKED if m == 2 else 0)
        reserve, cum = need, cum + cash
        rows.append({"m": m, "buyers": round(active + n), "gmv": round(gmv), "gnr": round(gnr), "op": round(op),
                     "cash": round(cash), "cum": round(cum)})
        active = (active + n) * RETENTION
    return rows


if __name__ == "__main__":
    out = {k: run(g) for k, g in SCEN.items()}
    for k, rows in out.items():
        be = next((r["m"] for r in rows if r["op"] >= 0), None)
        print(k, "| m3 GMV", rows[2]["gmv"], "buyers", rows[2]["buyers"], "| m12 GMV", rows[-1]["gmv"], "GNR", rows[-1]["gnr"],
              "buyers", rows[-1]["buyers"], "| yr GNR", sum(r["gnr"] for r in rows), "yr op", sum(r["op"] for r in rows),
              "| op break-even", be, "| funding need", -min(r["cum"] for r in rows), "end cum", rows[-1]["cum"])
    for r in out["base"]:
        print(r)
    json.dump(out, open(__file__.replace("model.py", "model.json"), "w"), indent=1)
