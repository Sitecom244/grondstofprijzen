"""Bouwt de grondstofprijzen-widget uit data.json + update.json.
Gebruik: python3 -I build.py <data.json> <update.json> <out.html>"""
import json, sys
data, update, out = sys.argv[1:4]
tpl = open(__file__.replace('build.py', 'widget_template.html'), encoding='utf-8').read()
html = tpl.replace('__DATA__', open(data, encoding='utf-8').read()).replace('__UPDATE__', open(update, encoding='utf-8').read())
open(out, 'w', encoding='utf-8').write(html)
print('ok', out, len(html))
