"""Inline SVG charts for the plan. Colors come from CSS variables so both themes work."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def scenarios():
    data = json.load(open(os.path.join(HERE, "model.json")))
    W, H, L, R, T, B = 640, 300, 56, 150, 16, 36
    ymin, ymax = -15_000, 30_000
    x = lambda m: L + (m - 1) * (W - L - R) / 11
    y = lambda v: T + (H - T - B) * (ymax - v) / (ymax - ymin)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Monthly operating result by scenario">']
    for v in range(ymin, ymax + 1, 15_000):
        out.append(f'<line x1="{L}" x2="{W - R}" y1="{y(v):.1f}" y2="{y(v):.1f}" class="{"ref" if v == 0 else "grid"}"/>'
                   f'<text x="{L - 8}" y="{y(v) + 4:.1f}" class="tick" text-anchor="end">{"−" if v < 0 else ""}${abs(v) // 1000}k</text>')
    out.append(f'<text x="{L + 6}" y="{y(0) - 7:.1f}" class="lab ref-t">break-even</text>')
    for m in range(1, 13):
        out.append(f'<text x="{x(m):.1f}" y="{H - B + 18}" class="tick" text-anchor="middle">M{m}</text>')
    for k, cls in (("conservative", "s3"), ("base", "s1"), ("upside", "s2")):
        pts = " ".join(f"{x(r['m']):.1f},{y(r['op']):.1f}" for r in data[k])
        last = data[k][-1]
        out.append(f'<polyline points="{pts}" class="line {cls}"/>'
                   f'<circle cx="{x(12):.1f}" cy="{y(last["op"]):.1f}" r="3.5" class="dot {cls}"/>'
                   f'<text x="{x(12) + 8:.1f}" y="{y(last["op"]) + 4:.1f}" class="lab {cls}-t">{k} +${last["op"] / 1000:.1f}k</text>')
    out.append("</svg>")
    return "".join(out)


def bounty():
    rows = [("Human-only bounties", 36, 25.4, "s3"), ("Agent-allowed bounties", 115.5, 5.0, "s1")]
    W, H = 640, 150
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Superteam 2026 bounties: entries and payout per entry">',
           '<text x="0" y="14" class="lab">Median entries per bounty</text>',
           f'<text x="{W / 2 + 16}" y="14" class="lab">Median payout per entry (USD)</text>']
    for i, (name, subs, usd, cls) in enumerate(rows):
        yy = 34 + i * 54
        w1 = subs / 120 * (W / 2 - 80)
        w2 = usd / 26 * (W / 2 - 80)
        out.append(f'<text x="0" y="{yy + 12}" class="tick">{name}</text>'
                   f'<rect x="0" y="{yy + 18}" width="{w1:.1f}" height="18" rx="3" class="bar {cls}"/>'
                   f'<text x="{w1 + 6:.1f}" y="{yy + 32}" class="val">{subs:g}</text>'
                   f'<rect x="{W / 2 + 16}" y="{yy + 18}" width="{w2:.1f}" height="18" rx="3" class="bar {cls}"/>'
                   f'<text x="{W / 2 + 22 + w2:.1f}" y="{yy + 32}" class="val">${usd:g}</text>')
    out.append("</svg>")
    return "".join(out)


if __name__ == "__main__":
    print(len(scenarios()), len(bounty()))
