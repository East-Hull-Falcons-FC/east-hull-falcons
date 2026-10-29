# East Hull Falcons FC Safeguarding Hub

The club's safeguarding contacts, reporting guide, policies, codes of conduct and rules, published as a web page for parents, players and coaches.

Live page: https://east-hull-falcons-fc.github.io/east-hull-falcons/

- `index.html` is the page.
- `u10s/` is the U10s team page for parents: fixtures and results (`u10s/fixtures.json`), training calendar, matchday information, playbook and sponsorship. It holds no player names or personal details.
- `scripts/build_fixtures.py` builds `u10s/fixtures.json` from the tracker sheet's Fixtures & Goals tab (fixture rows only). A Claude scheduled task runs it every Monday evening and pushes any change.
- `pdf/u10s-playbook-2026-2030.pdf` is the playbook with the players' birth-month page removed.
- `pdf/` holds the documents as PDFs.
- `docs/` holds the same documents as page images, shown on the page.
- `img/` holds the crest, logos and photos.
