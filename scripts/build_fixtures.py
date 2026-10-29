"""Build u10s/fixtures.json for the public U10s page.

Usage: python3 -I scripts/build_fixtures.py <fixtures_values.json> <out_file> <updated YYYY-MM-DD>

<fixtures_values.json> is the Google Sheets get_values response (JSON, as
returned) for 'Fixtures & Goals'!A1:AB10 of the "Training & Matches Attendance
Tracker" (spreadsheet 1Oz9nBVMovMd9pcTF90PCKfYxGpgIakRjuBIHg-mQg6M).

Only fixture details and scores are written. Rows 11 onwards of that tab hold
player names and goals; this script never reads them, so no child's name can
reach the public page.
"""
import json
import re
import sys


def cell(rows, r, c):
    try:
        return (rows[r][c] or "").strip()
    except IndexError:
        return ""


def iso(d):
    m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{2,4})$", d.strip())
    if not m:
        return ""
    dd, mm, yy = m.groups()
    yy = int(yy)
    if yy < 100:
        yy += 2000
    return f"{yy:04d}-{int(mm):02d}-{int(dd):02d}"


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def main(src, out, updated):
    with open(src) as f:
        rows = json.load(f).get("values", [])[:10]  # fixture rows only
    if not rows or cell(rows, 0, 0) != "Opponent" or cell(rows, 5, 0) != "Type":
        sys.exit("Unexpected layout: row 1 should start 'Opponent' and row 6 'Type'. Nothing written.")
    fixtures = []
    width = max(len(r) for r in rows)
    for c in range(1, width):
        opp, d = cell(rows, 0, c), iso(cell(rows, 1, c))
        if not opp or not d:
            continue
        sc = [num(cell(rows, r, c)) for r in (6, 7, 8, 9)]
        fixtures.append({
            "date": d, "opponent": opp,
            "ha": cell(rows, 2, c), "venue": cell(rows, 3, c), "ko": cell(rows, 4, c),
            "type": cell(rows, 5, c) or "League",
            "g1": [sc[0], sc[1]] if sc[0] is not None and sc[1] is not None else None,
            "g2": [sc[2], sc[3]] if sc[2] is not None and sc[3] is not None else None,
        })
    fixtures.sort(key=lambda f: (f["date"], f["type"] in ("Cancelled", "Postponed")))
    with open(out, "w") as f:
        json.dump({"updated": updated, "fixtures": fixtures}, f, indent=1)
        f.write("\n")
    print(f"fixtures={len(fixtures)}")
    for fx in fixtures:
        res = " ".join(f"{int(g[0])}-{int(g[1])}" for g in (fx["g1"], fx["g2"]) if g)
        print(f'  {fx["date"]} {fx["opponent"]} ({fx["ha"]}) {fx["type"]} ko {fx["ko"]} {res}')


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
