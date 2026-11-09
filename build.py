"""Build index.html (charts inlined) and foreguild-operating-plan.pdf from plan.src.html."""
import os
import subprocess

import charts

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

src = open(os.path.join(HERE, "plan.src.html"), encoding="utf-8").read()
html = src.replace("<!--CHART:bounty-->", charts.bounty()).replace("<!--CHART:scen-->", charts.scenarios())
assert "<!--CHART" not in html
out = os.path.join(HERE, "index.html")
open(out, "w", encoding="utf-8").write(html)
pdf = os.path.join(HERE, "foreguild-operating-plan.pdf")
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={pdf}", "file:///" + out.replace("\\", "/")], check=True, timeout=120)
print(out, os.path.getsize(out), pdf, os.path.getsize(pdf))
