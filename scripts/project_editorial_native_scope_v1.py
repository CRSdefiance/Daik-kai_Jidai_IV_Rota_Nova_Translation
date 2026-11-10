"""Project immutable whole-block native checks while preserving parent records/plans exactly."""
import argparse
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for key in ['manuscript','plan','out']:ap.add_argument('--'+key,type=Path,required=True)
    ap.add_argument('--blocks',type=int,nargs='+',required=True)
    args=ap.parse_args();assert not args.out.exists()
    doc,plan=map(load,[args.manuscript,args.plan]);assert plan['manuscript_sha256']==digest(args.manuscript)
    assert not plan['failures'] and len(doc['records'])==len(plan['records'])
    assert len(args.blocks)==len(set(args.blocks)) and set(args.blocks)<=set(doc['blocks'])
    assert all(r['kind'] in ['progressive','system-FE'] for r in doc['records'])
    subset=deepcopy(doc);subset['records']=[r for r in subset['records'] if r['block'] in args.blocks]
    ids={r['id'] for r in subset['records']};assert len(ids)==len(subset['records']) and ids
    subset.update(blocks=sorted(args.blocks),physical_speech_objects=len(ids),ordinary_speech_objects=len(ids),
        source_objects=len(ids),source_FE_panels=sum(r['kind']=='system-FE' for r in subset['records']),
        total_editorial_objects=len(ids),typed_choice_objects=0,typed_choice_commands=0,
        subset_of=str(args.manuscript),subset_of_sha256=digest(args.manuscript),
        all_projected_rows_unchanged=True,no_new_editorial_orformatting_approval=True,new_credit=0)
    args.out.mkdir(parents=True);manuscript=args.out/'manuscript.json';save(manuscript,subset)
    subplan=deepcopy(plan);subplan['records']=[r for r in subplan['records'] if r['id'] in ids]
    assert len(subplan['records'])==len(ids)
    subplan.update(manuscript=str(manuscript),manuscript_sha256=digest(manuscript),
        complete_parent_plan=str(args.plan),complete_parent_plan_sha256=digest(args.plan),
        all_selected_plan_objects_unchanged=True,new_credit=0)
    save(args.out/'automatic_plans.json',subplan)
    save(args.out/'projection_qualification.json',dict(blocks=sorted(args.blocks),source_objects=len(ids),
        original_manuscript=str(args.manuscript),original_manuscript_sha256=digest(args.manuscript),
        original_plan=str(args.plan),original_plan_sha256=digest(args.plan),
        original_rows_andplans_exact=True,whole_exchanges_only=True,
        original_inputs_unchanged=True,new_credit=0,producer_sha256=digest(Path(__file__))))
    print('Projected whole native blocks',sorted(args.blocks),'records',len(ids),'without prose orplan changes.')
if __name__=='__main__':main()
