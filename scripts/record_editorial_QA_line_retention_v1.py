"""Record one exact reviewed grammatical soft boundary; retain all original diagnostics."""
import argparse
from copy import deepcopy
import hashlib
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for arg in ['plan','preferences','out']:p.add_argument('--'+arg,type=Path,required=True)
    p.add_argument('--id',required=True);p.add_argument('--line-index',type=int,required=True);p.add_argument('--reason',required=True)
    args=p.parse_args();assert not args.out.exists()
    plan,prefs=map(load,[args.plan,args.preferences]);prefs=deepcopy(prefs)
    row=next(r for r in plan['records'] if r['id']==args.id);pref=prefs['records'][args.id];assert 'QA_line_ending_retention' not in pref
    issues=[i for i in row['base_QA']['issues'] if i['severity'] in ['warning','error']]
    assert len(issues)==1 and issues[0]['severity']=='warning' and issues[0]['code']=='weak-line-ending'
    assert f'line {args.line_index+1} ends' in issues[0]['message']
    for key in ['source_hex','current_hex','english']:
        value=row['logical_English'] if key=='english' else row['planning_record'][key]
        assert hashlib.sha256(value.encode()).hexdigest()==pref['bindings'][key]
    pref['QA_line_ending_retention']=dict(line_index=args.line_index,exact_line=row['lines'][args.line_index],reason=args.reason)
    prefs.setdefault('evidence',{}).update({str(p):digest(p) for p in [args.plan,args.preferences,Path(__file__)]})
    save(args.out,prefs);print('Saved exact grammatical line retention for',args.id,'without changing prose, width or other guards.')

if __name__=='__main__':main()
