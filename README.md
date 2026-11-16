# Grondstofprijzen kunststof

Grafiek en calculator voor het kennisbankartikel "Grondstofprijzen kunststof" op verpakkingenxl.nl.

- Grafiek: https://sitecom244.github.io/grondstofprijzen/
- Calculator: https://sitecom244.github.io/grondstofprijzen/?view=calculator

## Wekelijks bijwerken
1. Nieuwste "grondstofprijzen [datum].xlsx" (Polymer Prices Germany + China) samenvoegen in `data.json` (`bouw/gp_merge.py`)
2. Concept-marktupdate in `update.json`, pas na goedkeuring
3. `python3 bouw/build.py data.json update.json index.html`
4. Committen en pushen naar `main`

Nooit EUWID-cijfers gebruiken.
