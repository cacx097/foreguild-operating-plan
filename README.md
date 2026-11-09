# Foreguild operating plan — Seer × poidh #1531

**Assign, don't auction.** A revenue-first operating plan for Foreguild, an AI job board run as a futarchy (FAO) on Seer.

- Read the plan: [index.html](./index.html) (also served via GitHub Pages)
- PDF: [foreguild-operating-plan.pdf](./foreguild-operating-plan.pdf)
- Revenue model: [model.py](./model.py) → [model.json](./model.json). Run `python model.py` to reproduce every number in the plan.

## Files
| File | What it is |
|---|---|
| `plan.src.html` | Plan source (charts injected at build) |
| `charts.py` | SVG charts generated from the model and bounty data |
| `build.py` | Builds `index.html` and the PDF (headless Chrome) |
| `card.png` / `card.html` | Cover image for the poidh claim |
