"""Recheck changed layouts; reuse exact compiled bytes on the same runtime/font."""
import argparse
from copy import deepcopy
from pathlib import Path
import subprocess
import sys

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ('manuscript','plan','previous','out'):
        parser.add_argument('--'+arg,type=Path,required=True)
    args=parser.parse_args()
    assert not args.out.exists()
    doc,plan,previous=map(load,[args.manuscript,args.plan,args.previous])
    assert plan['manuscript_sha256']==previous['manuscript_sha256']==sha(args.manuscript.read_bytes())
    old_plan_path=Path(previous['plan'])
    assert sha(old_plan_path.read_bytes())==previous['plan_sha256']
    old_plan={row['id']:row for row in load(old_plan_path)['records']}
    old_rows={row['id']:row for row in previous['records']}
    assert set(old_rows)==set(old_plan)=={row['id'] for row in plan['records']}
    assert not plan['failures'] and not any(i['severity'] in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    changed=[r for r in plan['records'] if r['encoded_hex']!=old_plan[r['id']]['encoded_hex']]
    unchanged=[r for r in plan['records'] if r not in changed]
    assert changed
    args.out.mkdir(parents=True)
    subset=deepcopy(doc);ids={r['id'] for r in changed}
    subset['records']=[r for r in doc['records'] if r['id'] in ids]
    subset['blocks']=sorted({r['block'] for r in subset['records']})
    subset.update(total_editorial_objects=len(changed),
        revised=sum(r['decision']=='revision' for r in subset['records']),
        retained=sum(r['decision']=='retention' for r in subset['records']),
        source_macro_counts={key:sum(r['source_macros'][key] for r in subset['records']) for key in ('FI','FA','FO')},
        source_FE_panels=sum(r['source_selector']==254 for r in subset['records']),
        subset_of=str(args.manuscript),subset_of_sha256=sha(args.manuscript.read_bytes()),new_credit=0)
    subset_path=args.out/'changed_manuscript.json';save(subset_path,subset)
    subplan={**plan,'manuscript':str(subset_path),'manuscript_sha256':sha(subset_path.read_bytes()),'records':changed}
    subplan_path=args.out/'changed_plans.json';save(subplan_path,subplan)
    runtime=previous['runtime']
    subprocess.run([sys.executable,'scripts/check_editorial_compiled_pages.py',
        '--manuscript',str(subset_path),'--plan',str(subplan_path),
        '--release',runtime['release_proof'],'--startup',runtime['startup_proof'],
        '--out',str(args.out/'fresh')],check=True)
    fresh_path=args.out/'fresh/compiled_native_pages.json';fresh=load(fresh_path)
    assert fresh['runtime']==previous['runtime'] and fresh['font_sha256']==previous['font_sha256']
    revised={r['id']:r for r in fresh['records']}
    reused=[]
    for row in unchanged:
        old=old_rows[row['id']]
        assert old['compiled_hex']==row['encoded_hex'] and old['logical_English']==row['logical_English']
        rendered=old['complete_native_English_display']
        pages=rendered['pages'] if row['kind']=='progressive' else [rendered]
        for page in pages:
            for filename,key in [('native_plane','native_plane_sha256'),('preview','preview_sha256')]:
                assert sha(Path(page[filename]).read_bytes())==page[key]
        reused.append(row['id'])
    combined=[revised.get(row['id'],old_rows[row['id']]) for row in doc['records']]
    save(args.out/'compiled_native_pages.json',dict(
        manuscript=str(args.manuscript),manuscript_sha256=sha(args.manuscript.read_bytes()),
        plan=str(args.plan),plan_sha256=sha(args.plan.read_bytes()),
        runtime=fresh['runtime'],font_sha256=fresh['font_sha256'],records=combined,
        pages=sum(r['expected_native_pages'] for r in plan['records']),
        fresh_compiled_alignments=fresh['fresh_compiled_alignments'],
        reused_compiled_alignments=4*len(reused),reused_record_ids=reused,
        all_records_native_checked_once_or_exact_compiled_dependency_reuse=True,
        previous_native=str(args.previous),previous_native_sha256=sha(args.previous.read_bytes()),
        previous_direct_view_sheets=previous['review_sheets'],
        review_sheets=fresh['review_sheets'],fresh_native=str(fresh_path),fresh_native_sha256=sha(fresh_path.read_bytes()),
        changed_layout_ids=sorted(ids),only_fresh_pages_need_new_direct_view=True,
        direct_visual_review_pending=True,formatting_gates_still_false=True,
        actual_gameplay=False,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [args.manuscript,args.plan,args.previous,Path(__file__)]}))
    print(dict(fresh_records=len(changed),fresh_pages=fresh['pages'],reused_records=len(reused),pages=sum(r['expected_native_pages'] for r in plan['records'])),flush=True)

if __name__=='__main__':
    main()
