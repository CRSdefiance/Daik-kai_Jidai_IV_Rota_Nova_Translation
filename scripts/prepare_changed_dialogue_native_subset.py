"""Prepare only changed compiled records for fresh native checks on an immutable full plan."""
import argparse
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['manuscript','plan','previous-native','out']:parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    doc,plan,previous=map(load,[args.manuscript,args.plan,args.previous_native])
    assert plan['manuscript_sha256']==sha(args.manuscript.read_bytes()) and not plan['failures']
    originals={r['id']:r for r in previous['records']}
    changed={r['id'] for r in plan['records'] if r['id'] not in originals or r['encoded_hex']!=originals[r['id']]['compiled_hex']}
    assert changed and {r['id'] for r in doc['records']}=={r['id'] for r in plan['records']}
    args.out.mkdir(parents=True)
    subset=deepcopy(doc);subset.update(records=[r for r in doc['records'] if r['id'] in changed],
        subset_of=str(args.manuscript),subset_of_sha256=sha(args.manuscript.read_bytes()))
    manuscript=args.out/'manuscript.json';save(manuscript,subset)
    subplan=deepcopy(plan);subplan.update(records=[r for r in plan['records'] if r['id'] in changed],
        manuscript=str(manuscript),manuscript_sha256=sha(manuscript.read_bytes()),
        subset_of=str(args.plan),subset_of_sha256=sha(args.plan.read_bytes()))
    save(args.out/'plans.json',subplan)
    save(args.out/'membership.json',dict(changed_IDs=sorted(changed),
        unchanged_count=len(doc['records'])-len(changed),previous_native=str(args.previous_native),
        previous_native_sha256=sha(args.previous_native.read_bytes()),new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print(dict(changed_records=len(changed),unchanged_records=len(doc['records'])-len(changed),changed_IDs=sorted(changed)))
