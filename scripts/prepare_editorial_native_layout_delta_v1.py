"""Select only byte-changed layouts; unchanged native proof reuse stays conditional."""
import argparse
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['manuscript','before-plan','after-plan','out']:parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    doc,before,after=map(load,[args.manuscript,args.before_plan,args.after_plan])
    digest=sha(args.manuscript.read_bytes())
    assert before['manuscript_sha256']==after['manuscript_sha256']==digest
    assert not before['failures'] and not after['failures']
    assert not any(i['severity'] in ['warning','error'] for r in after['records'] for i in r['base_QA']['issues'])
    a,b=[{r['id']:r for r in p['records']} for p in [before,after]]
    assert a.keys()==b.keys()
    assert all(a[k]['logical_English']==b[k]['logical_English'] for k in a)
    changed={k for k in a if a[k]['encoded_hex']!=b[k]['encoded_hex']}
    assert changed
    args.out.mkdir()
    subset=deepcopy(doc);subset['records']=[r for r in doc['records'] if r['id'] in changed]
    subset.update(blocks=sorted({r['block'] for r in subset['records']}),physical_speech_objects=len(changed),
        ordinary_speech_objects=sum(r['kind']=='progressive' for r in subset['records']),
        FE_speech_objects=sum(r['kind']=='system-FE' for r in subset['records']),typed_choice_objects=0,
        subset_of=str(args.manuscript),subset_of_sha256=digest)
    path=args.out/'changed_manuscript.json';save(path,subset)
    plan=deepcopy(after);plan.update(manuscript=str(path),manuscript_sha256=sha(path.read_bytes()),
        records=[r for r in after['records'] if r['id'] in changed],subset_of=str(args.after_plan),
        subset_of_sha256=sha(args.after_plan.read_bytes()))
    save(args.out/'changed_plans.json',plan)
    save(args.out/'delta.json',dict(changed_record_IDs=sorted(changed),unchanged_record_IDs=sorted(a.keys()-changed),
        fresh_pages=sum(b[k]['expected_native_pages'] for k in changed),
        previous_changed_pages=sum(a[k]['expected_native_pages'] for k in changed),
        candidate_exact_reused_pages=sum(b[k]['expected_native_pages'] for k in a.keys()-changed),
        complete_base_native_receipt_required_before_claiming_reuse=True,
        all_prose_andunselected_compiled_bytes_unchanged=True,
        evidence={str(p):sha(p.read_bytes()) for p in [args.manuscript,args.before_plan,args.after_plan,Path(__file__)]},new_credit=0))
    print('Layout delta:',len(changed),'records /',sum(b[k]['expected_native_pages'] for k in changed),'fresh pages. Unchanged reuse awaits complete base proof.',flush=True)
