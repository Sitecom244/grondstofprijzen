import openpyxl, json, glob, datetime
data={'DE':{}, 'CN':{}}
for f in sorted(glob.glob('gp/g*.xlsx')):
    wb=openpyxl.load_workbook(f,data_only=True)
    for ws in wb:
        t=ws.title.lower()
        key='DE' if 'germany' in t else 'CN' if 'china' in t else None
        if not key: continue
        hdr=None
        for r in ws.iter_rows(values_only=True):
            if r and r[0]=='Date': hdr=list(r); continue
            if hdr and r and r[0] and '/' in str(r[0]):
                d=datetime.datetime.strptime(str(r[0]),'%d/%m/%Y').date().isoformat()
                row={}
                for i,h in enumerate(hdr):
                    if h and h not in ('Date','+/- %') and i<len(r) and r[i] not in (None,'','N/A'):
                        try: row[h]=float(r[i])
                        except: pass
                data[key].setdefault(d,{}).update(row)  # later files overwrite
out={}
for k,v in data.items():
    dates=sorted(v)
    out[k]={'dates':dates,'series':{}}
    for p in ['LDPE','LLDPE','HDPE','PPROP','PET','PVC','PS','ABS']:
        out[k]['series'][p]=[v[d].get(p) for d in dates]
    print(k,len(dates),dates[0],dates[-1], {p:sum(x is None for x in s) for p,s in out[k]['series'].items()})
json.dump(out,open('gp/polymer_data.json','w'))
