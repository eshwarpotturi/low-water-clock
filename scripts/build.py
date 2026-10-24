"""Inject gauge data into template.html and write index.html. Usage: python3 -I scripts/build.py"""
import csv, json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
rows = list(csv.DictReader(open(root / "data/kaub_2026_daily.csv")))
gauge = [[r["date"], float(r["mean_cm"]), int(r["min_cm"])] for r in rows]
last = rows[-1]
data = {"gauge": gauge, "latest": {"value": int(last["last_cm"]), "when": "24 Oct, 17:45"}}
html = (root / "template.html").read_text().replace("/*DATA*/", json.dumps(data))
(root / "index.html").write_text(html)
print("wrote index.html", len(gauge), "days, latest", data["latest"])
