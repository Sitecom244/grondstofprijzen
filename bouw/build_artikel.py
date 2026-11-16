"""Vult het kennisbankartikel met de laatste cijfers.
Gebruik: python3 -I build_artikel.py <data.json> <widget_url> <img_ongebruikt> <out.html> [nl|be|fr|de]"""
import json, sys, os
data_p, widget, _img, out = sys.argv[1:5]
lang = sys.argv[5] if len(sys.argv) > 5 else 'nl'
d = json.load(open(data_p, encoding='utf-8'))
m = d['markets']['DE']; ds = m['dates']; S = m['series']
MAAND = {
    'nl': ['januari','februari','maart','april','mei','juni','juli','augustus','september','oktober','november','december'],
    'fr': ['janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre'],
    'de': ['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember']}
L = 'nl' if lang in ('nl', 'be') else lang

def last(s):
    for i in range(len(s) - 1, -1, -1):
        if s[i] is not None: return i
def num(n):
    t = f"{n:,.0f}"
    return t.replace(',', ' ') if L == 'fr' else t.replace(',', '.')
def datum(iso):
    y, mo, da = map(int, iso.split('-'))
    if L == 'de': return f"{da}. {MAAND[L][mo-1]} {y}"
    if L == 'fr': return f"{'1er' if da == 1 else da} {MAAND[L][mo-1]} {y}"
    return f"{da} {MAAND[L][mo-1]} {y}"
def rng(vals):
    lo, hi = round(min(vals)), round(max(vals))
    pc = ' %' if L in ('fr', 'de') else '%'
    if lo == hi: return f"{lo}{pc}"
    sep = {'nl': ' tot ', 'fr': ' à ', 'de': ' bis '}[L]
    return f"{lo}{sep}{hi}{pc}"

i = last(S['LDPE'])
jan = ds.index('2026-01-05')
peak = {p: max(v for v in S[p] if v is not None) for p in ('LDPE', 'LLDPE', 'HDPE')}
fill = {
    '%%DATUM%%': datum(ds[i]), '%%LDPE%%': num(S['LDPE'][i]), '%%LLDPE%%': num(S['LLDPE'][i]), '%%HDPE%%': num(S['HDPE'][i]),
    '%%VS_PIEK%%': rng([abs(S[p][i] / peak[p] - 1) * 100 for p in peak]), '%%VS_JAN%%': rng([(S[p][i] / S[p][jan] - 1) * 100 for p in peak]),
    '%%WIDGET%%': widget,
}
base = os.path.dirname(os.path.abspath(__file__))
tpl = {'nl': 'artikel_template.html', 'be': 'artikel_template_be.html', 'fr': 'artikel_template_fr.html', 'de': 'artikel_template_de.html'}[lang]
html = open(os.path.join(base, tpl), encoding='utf-8').read()
for k, v in fill.items(): html = html.replace(k, v)
assert '%%' not in html, 'onvervangen placeholder'
open(out, 'w', encoding='utf-8').write(html)
print('ok', lang, out, {k: v for k, v in fill.items() if k != '%%WIDGET%%'})
