"""Remove one over-constrained scoped preference while preserving its prose bindings and history."""
import argparse
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ['preferences','out']:p.add_argument('--'+key,type=Path,required=True)
    p.add_argument('--id',required=True);p.add_argument('--remove',choices=['one_page','required_pairs','page_clause'],required=True);p.add_argument('--reason',required=True)
    args=p.parse_args();assert not args.out.exists();prefs=deepcopy(load(args.preferences));row=prefs['records'][args.id]
    old=row.pop(args.remove);row['reason']+=' '+args.reason
    prefs.setdefault('constraint_revisions',[]).append(dict(id=args.id,removed_key=args.remove,removed_value=old,reason=args.reason))
    prefs.setdefault('evidence',{}).update({str(p):digest(p) for p in [args.preferences,Path(__file__)]});save(args.out,prefs)
    print('Removed only',args.remove,'for',args.id,'with exact existing source/current/prose bindings retained.')

if __name__=='__main__':main()
