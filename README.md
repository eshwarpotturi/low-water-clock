# Low Water Clock: exception console

A working console for the 2026 Rhine low-water season. It shows a person only the shipments the system cannot safely handle alone, with the facts needed to decide.

**Demo:** https://eshwarpotturi.github.io/low-water-clock/

**The message:** most shipments need no screen. A few need a person, and the console shows why.

## How it works

1. A carrier notice arrives (five are replayed: Maersk 14 Jul, Hapag-Lloyd 20 Jul, Tradlinx 6 Aug, Maersk 12 Aug, Maersk 8 Oct).
2. The AI read each notice once and turned it into rules, each with a version and a source link.
3. Plain code checks every shipment against the rules on file for that date.
4. Shipments where the barge is still guaranteed, or not needed soon, are handled and counted. No screen.
5. The rest appear as a queue with the reason, the surcharge, the rule version and the carrier's words. A person approves, overrides or escalates.
6. Every decision goes in a log with the rule version used.

Click the river to move to any day, or press "Replay the season". "Rule changes" shows three versions of Maersk's price table and two entries that look like errors.

## What is real, what is made up

| Part | Status |
|---|---|
| Kaub daily water levels, 20 Jun to 24 Oct 2026 | Real (Pegelonline, 15-minute readings) |
| Maersk, Hapag-Lloyd, Contargo, CMA CGM terms | Real, read from carrier notices and trade press, linked in the page |
| The 420 shipments | Made up (seeded, so the page is the same every time) |
| Rail slots per week (4) | An assumption |
| Rule owner | A role, not a named person |

Not connected to any company system. Approving a decision only writes the log on the page. Not a forecast. Carrier pages change, so check the current notice before acting.

## Rebuild

```
python3 scripts/fetch_2026.py data/kaub_2026_daily.csv   # re-fetch river data
```

`index.html` is a single file with the river data embedded. It needs no network connection.

## Known limits

- Hapag-Lloyd's site blocks automatic download. Its figures were read by hand and the 50 to 41 cm band is confirmed by Tradlinx.
- CMA CGM and Contargo terms come from a Tradlinx article (6 Aug 2026). "On file since" dates are the dates of our sources, not the dates carriers first set the terms.
- Maersk's October table comes from Container News (8 Oct 2026), not Maersk's own page.
- We did not test whether the river warned shippers before carriers did. The public record does not allow it.
