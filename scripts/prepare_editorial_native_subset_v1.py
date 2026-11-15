"""Select exact parent records and plans for focused new-layout rendering."""
import argparse
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for key in ['manuscript','plan','out']:p.add_argument('--'+key,type=Path,required=True)
    p.add_argument('--ids',nargs='+',required=True);args=p.parse_args()
    assert not args.out.exists() and len(args.ids)==len(set(args.ids))
    doc,plan=map(load,[args.manuscript,args.plan]);assert plan['manuscript_sha256']==sha(args.manuscript.read_bytes()) and not plan['failures']
    chosen=set(args.ids);records=[r for r in doc['records'] if r['id'] in chosen]
    assert {r['id'] for r in records}==chosen and all(r['kind'] in ['progressive','system-FE'] for r in records)
    rows=[r for r in plan['records'] if r['id'] in chosen];assert {r['id'] for r in rows}==chosen
    subset=deepcopy(doc);subset.update(records=records,blocks=sorted({r['block'] for r in records}),
        physical_speech_objects=len(records),ordinary_speech_objects=len(records),typed_choice_objects=0,typed_choice_commands=0,
        subset_of=str(args.manuscript),subset_of_sha256=sha(args.manuscript.read_bytes()),complete_batch_display_still_pending=True)
    args.out.mkdir(parents=True);out=args.out/'manuscript.json';save(out,subset)
    save(args.out/'plans.json',dict(plan,records=rows,manuscript=str(out),manuscript_sha256=sha(out.read_bytes()),
        subset_of=str(args.plan),subset_of_sha256=sha(args.plan.read_bytes())))
    print('Prepared',len(records),'exact parent records for fresh focused native layout checks.')
