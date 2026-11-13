"""Bind concise visual findings to exact source/current/prose dependencies; never edit the prose."""
import argparse
from copy import deepcopy
import hashlib
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for arg in ['manuscript','preferences','findings','out']:p.add_argument('--'+arg,type=Path,required=True)
    args=p.parse_args();assert not args.out.exists()
    doc,prefs,findings=map(load,[args.manuscript,args.preferences,args.findings]);prefs=deepcopy(prefs)
    rows={r['id']:r for r in doc['records']}
    for ident,value in findings['records'].items():
        assert ident in rows and ident not in prefs['records'] and value.get('reason')
        assert set(value)<={'reason','one_page','page_clause','required_pairs','QA_line_ending_retention'}
        row=rows[ident]
        if 'page_clause' in value:assert row['english'].count(value['page_clause'])==1
        prefs['records'][ident]=dict(value,bindings={k:hashlib.sha256(row[k].encode()).hexdigest() for k in ['source_hex','current_hex','english']})
    prefs.setdefault('evidence',{}).update({str(p):digest(p) for p in [args.manuscript,args.preferences,args.findings,Path(__file__)]})
    save(args.out,prefs);print('Bound',len(findings['records']),'individual visual findings; no prose or native geometry change.')

if __name__=='__main__':main()
