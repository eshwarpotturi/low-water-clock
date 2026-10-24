"""Parse BfG DGJ Kaub water-level yearbook text (pdftotext -layout) into daily values.

Usage: python3 -I parse_bafg.py kaub.txt out.csv
Each log line prints a timestamp and progress (done/total).
"""
import csv
import re
import sys
from datetime import date, datetime

MONTHS = ["Nov", "Dez", "Jan", "Feb", "Mrz", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]


def log(msg, done=None, total=None):
    prog = f" [{done}/{total}]" if done is not None else ""
    print(f"{datetime.now().isoformat(timespec='seconds')}{prog} {msg}", flush=True)


def main(src, dst):
    lines = open(src, encoding="utf-8").read().split("\n")
    # locate water-level blocks: a line "DGJ - Wasserstände ... <year>"
    starts = [i for i, l in enumerate(lines) if "DGJ - Wasserstände" in l]
    log(f"found {len(starts)} water-level blocks")
    out = []
    for bi, s in enumerate(starts):
        year = int(lines[s].split()[-1])
        end = starts[bi + 1] if bi + 1 < len(starts) else len(lines)
        block = lines[s:end]
        # the daily grid is the part before the first 'Hauptwerte' heading
        cut = next((k for k, l in enumerate(block) if "Hauptwerte" in l), len(block))
        block = block[:cut]
        # header line with month names: locate right edge of each month label
        hdr = next(l for l in block if re.search(r"\bNov\b.*\bDez\b.*\bJan\b", l))
        edges = []
        pos = 0
        for m in MONTHS:
            j = hdr.index(m, pos)
            edges.append(j + len(m))
            pos = j + len(m)
        last_day = 0
        for l in block:
            if not re.search(r"\d", l):
                continue
            m = re.match(r"\s*(\d{1,2})\.\s", l)
            if m:
                day = int(m.group(1))
                body_start = m.end()
            elif re.match(r"\s*\d+(\s+\d+)+\s*$", l):  # displaced row (no label)
                day = last_day + 1
                body_start = 0
            else:
                continue
            last_day = day
            for tok in re.finditer(r"\d+", l[body_start:]):
                right = body_start + tok.end()
                col = min(range(len(edges)), key=lambda c: abs(edges[c] - right))
                if col < 2 or col > 13:  # keep calendar-year columns only (Jan..Dez)
                    continue
                month = col - 1  # Jan -> 1
                try:
                    d = date(year, month, day)
                except ValueError:
                    continue
                out.append((d.isoformat(), int(tok.group())))
        log(f"parsed block {year}", bi + 1, len(starts))
    out = sorted(set(out))
    with open(dst, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "kaub_cm"])
        w.writerows(out)
    log(f"wrote {len(out)} rows to {dst}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
