"""Fetch per-day raw Kaub readings (15-min) from Pegelonline for 2026 and write daily min/mean/last.

Usage: python3 -I fetch_2026.py out.csv
Log lines carry a timestamp and done/total progress.
"""
import csv
import re
import subprocess
import sys
from datetime import date, datetime, timedelta

START = date(2026, 6, 1)
END = date(2026, 10, 24)
URL = "https://pegelonline.wsv.de/webservices/files/Wasserstand+Rohdaten/RHEIN/KAUB/{d}/down.txt"


def log(msg, done, total):
    print(f"{datetime.now().isoformat(timespec='seconds')} [{done}/{total}] {msg}", flush=True)


def fetch(day):
    url = URL.format(d=day.strftime("%d.%m.%Y"))
    r = subprocess.run(["curl", "-s", "-m", "25", "-w", "\n%{http_code}", url], capture_output=True, text=True)
    body, _, code = r.stdout.rpartition("\n")
    return code, body


def main(dst):
    days = [START + timedelta(n) for n in range((END - START).days + 1)]
    rows = []
    for i, d in enumerate(days, 1):
        code, body = fetch(d)
        if code != "200":
            log(f"{d} http {code} (skipped)", i, len(days))
            continue
        vals = [int(v) for v in re.findall(r"\d\d:\d\d#(-?\d+)", body)]
        if not vals:
            log(f"{d} no readings", i, len(days))
            continue
        rows.append((d.isoformat(), min(vals), round(sum(vals) / len(vals), 1), vals[-1], len(vals)))
        log(f"{d} n={len(vals)} min={min(vals)}", i, len(days))
    with open(dst, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "min_cm", "mean_cm", "last_cm", "n_readings"])
        w.writerows(rows)
    print(f"{datetime.now().isoformat(timespec='seconds')} wrote {len(rows)} days to {dst}")


if __name__ == "__main__":
    main(sys.argv[1])
