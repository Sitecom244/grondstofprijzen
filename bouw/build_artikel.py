"""Vult het kennisbankartikel met de laatste cijfers.
Gebruik: python3 -I build_artikel.py <data.json> <widget_url> <header_img_url> <out.html>"""
import json, sys
data_p, widget, img, out = sys.argv[1:5]
d = json.load(open(data_p, encoding='utf-8'))
m = d['markets']['DE']; ds = m['dates']; S = m['series']
MAAND = ['januari','februari','maart','april','mei','juni','juli','augustus','september','oktober','november','december']

def last(s):
    for i in range(len(s) - 1, -1, -1):
        if s[i] is not None: return i
def nl(n): return f"{n:,.0f}".replace(',', '.')
def datum(iso):
    y, mo, da = map(int, iso.split('-')); return f"{da} {MAAND[mo-1]} {y}"
def rng(vals):
    lo, hi = round(min(vals)), round(max(vals))
    return f"{lo}%" if lo == hi else f"{lo} tot {hi}%"

i = last(S['LDPE'])
jan = ds.index('2026-01-05')
peak = {p: max(v for v in S[p] if v is not None) for p in ('LDPE', 'LLDPE', 'HDPE')}
vs_peak = [abs(S[p][i] / peak[p] - 1) * 100 for p in peak]
vs_jan = [(S[p][i] / S[p][jan] - 1) * 100 for p in peak]
fill = {
    '%%DATUM%%': datum(ds[i]), '%%LDPE%%': nl(S['LDPE'][i]), '%%LLDPE%%': nl(S['LLDPE'][i]), '%%HDPE%%': nl(S['HDPE'][i]),
    '%%VS_PIEK%%': rng(vs_peak), '%%VS_JAN%%': rng(vs_jan), '%%WIDGET%%': widget,
}
html = open(__file__.replace('build_artikel.py', 'artikel_template.html'), encoding='utf-8').read()
for k, v in fill.items(): html = html.replace(k, v)
assert '%%' not in html, 'onvervangen placeholder'
open(out, 'w', encoding='utf-8').write(html)
print('ok', out, {k: v for k, v in fill.items() if k not in ('%%WIDGET%%', '%%HEADERIMG%%')})
