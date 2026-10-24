# Low Water Clock

A replay of the 2026 Rhine low-water season, built from real data.

**Demo:** https://eshwarpotturi.github.io/low-water-clock/

**The message:** at 24 cm on the Kaub gauge, no carrier guarantees a barge. Rail slots decide who moves.

## What is real, what is made up

| Part | Status |
|---|---|
| Kaub daily water levels, 20 Jun to 24 Oct 2026 | Real (Pegelonline, 15-minute readings) |
| Kaub daily values 2021 to 2025 | Real (BfG yearbook) |
| Maersk, Hapag-Lloyd, Contargo, CMA CGM terms | Real, read from carrier notices and trade press, linked in the page |
| The ten shipments | Made up |
| Rail slots per week (default 4) | An assumption you can change on the page |

Not connected to any company system. Not a forecast. Carrier pages change, so check the current notice before acting.

## How it works

- Rules were extracted from the notices by an AI model (Claude), each with its source. The page shows three versions of Maersk's price table (14 Jul, 12 Aug, 8 Oct) side by side.
- The decisions on the page come from plain code, not a live AI call. The page needs no network connection.

## Rebuild

```
python3 scripts/fetch_2026.py data/kaub_2026_daily.csv   # re-fetch river data
python3 scripts/build.py                                  # template.html -> index.html
```

## Known limits

- Hapag-Lloyd's site blocks automatic download. Its figures were read by hand and the 50 to 41 cm band is confirmed by Tradlinx.
- CMA CGM and Contargo terms come from a Tradlinx article (6 Aug 2026).
- Maersk's October table comes from Container News (8 Oct 2026), not Maersk's own page.
- We did not test whether the river warned shippers before carriers did. The public record does not allow it.
