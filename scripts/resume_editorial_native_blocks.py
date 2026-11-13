"""Reuse completed block receipts after a narrow validator extension; check only remaining blocks."""
import argparse
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime import RegisteredRuntime

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ('manuscript','plan','partial','release','startup','role-bindings','out'):parser.add_argument('--'+arg,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    doc,plan=map(load,[args.manuscript,args.plan]);assert plan['manuscript_sha256']==sha(args.manuscript.read_bytes()) and not plan['failures']
    ctx=RegisteredRuntime(args.release,args.startup);assert doc['current_ROM_sha256']==ctx.receipt()['candidate_sha256']
    speeches=[r for r in doc['records'] if r['kind'] in ['progressive','system-FE']]
    planned={r['id']:r for r in plan['records']};reused={};block_receipts=[]
    for block in doc['blocks']:
        path=args.partial/f'B{block}_checked.json'
        if not path.exists():continue
        receipt=load(path);expected=[r for r in speeches if r['block']==block]
        assert {r['id'] for r in receipt['records']}=={r['id'] for r in expected}
        # The completed portion used the original static-selector predicate.
        # No dynamic record is imported under the newly extended predicate.
        assert not any(207<=r['source_selector']<224 for r in expected)
        for row in receipt['records']:
            original=next(r for r in expected if r['id']==row['id']);p=planned[row['id']]
            assert row['compiled_hex']==p['encoded_hex'] and row['logical_English']==original['english']
            assert row['source_reference']==original['source_reference'] and row['current_reference']==original['current_reference']
            assert len(row['native_alignment']['cases'])==4
            assert all(c['output_hex']==row['expanded_native_hex'] and c['original_macro_ABI_input_output_canaries_and_all_unowned4MiB_exact'] for c in row['native_alignment']['cases'])
            display=row['complete_native_English_display'];pages=display['pages'] if row['kind']=='progressive' else [display]
            assert len(pages)==p['expected_native_pages']
            for page in pages:
                for key,digest in [('native_plane','native_plane_sha256'),('preview','preview_sha256')]:assert sha(Path(page[key]).read_bytes())==page[digest]
            reused[row['id']]=row
        block_receipts.append(dict(block=block,path=str(path),sha256=sha(path.read_bytes()),records=len(expected)))
    fresh_rows=[r for r in speeches if r['id'] not in reused];assert reused and fresh_rows
    args.out.mkdir(parents=True)
    subset=deepcopy(doc);subset.update(records=fresh_rows,blocks=sorted({r['block'] for r in fresh_rows}),physical_speech_objects=len(fresh_rows),typed_choice_objects=0,
        total_editorial_objects=len(fresh_rows),source_FE_panels=sum(r['source_selector']==254 for r in fresh_rows),
        source_macro_counts={k:sum(r['source_macros'][k] for r in fresh_rows) for k in ['FI','FA','FO']},
        revised=sum(r['decision']=='revision' for r in fresh_rows),retained=sum(r['decision']=='retention' for r in fresh_rows))
    subset_path=args.out/'remaining_manuscript.json';save(subset_path,subset)
    subset_plan={**plan,'manuscript':str(subset_path),'manuscript_sha256':sha(subset_path.read_bytes()),'records':[planned[r['id']] for r in fresh_rows]}
    planpath=args.out/'remaining_plans.json';save(planpath,subset_plan)
    subprocess.run([sys.executable,'scripts/check_editorial_compiled_pages_v3.py','--manuscript',str(subset_path),'--plan',str(planpath),
        '--release',str(args.release),'--startup',str(args.startup),'--role-bindings',str(args.role_bindings),'--out',str(args.out/'fresh')],check=True)
    freshpath=args.out/'fresh/compiled_native_pages.json';fresh=load(freshpath)
    assert fresh['runtime']==ctx.receipt();all_rows={**reused,**{r['id']:r for r in fresh['records']}}
    final=[all_rows[r['id']] for r in speeches];assert len(final)==len(speeches)
    save(args.out/'compiled_native_pages.json',dict(manuscript=str(args.manuscript),manuscript_sha256=sha(args.manuscript.read_bytes()),
        plan=str(args.plan),plan_sha256=sha(args.plan.read_bytes()),runtime=ctx.receipt(),font_sha256=fresh['font_sha256'],records=final,
        pages=sum(r['expected_native_pages'] for r in plan['records']),fresh_compiled_alignments=fresh['fresh_compiled_alignments'],
        reused_compiled_alignments=4*len(reused),reused_record_ids=list(reused),reused_complete_block_receipts=block_receipts,
        source_owned_target_page_adapter=fresh['source_owned_target_page_adapter'],FE_factory_calibration=fresh['FE_factory_calibration'],
        source_owned_progressive_macro_adapter=fresh['source_owned_progressive_macro_adapter'],dynamic_role_bindings=fresh['dynamic_role_bindings'],
        review_sheets=fresh['review_sheets'],partial_static_run_producer='scripts/check_editorial_compiled_pages_v2.py',
        partial_run_ended_only_at_dynamic_identity_equals_prefix_assertion=True,
        exact_same_manuscript_plan_own_runtime_static_prefixes_andplanes_reused=True,
        all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass=True,complete_consumption_andpagination_exact=True,
        direct_visual_review_pending=True,formatting_gates_still_false=True,typed_choice_labels_separately_pending=True,
        actual_gameplay=False,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [args.manuscript,args.plan,args.role_bindings,freshpath,
            Path('scripts/check_editorial_compiled_pages_v2.py'),Path('scripts/check_editorial_compiled_pages_v3.py'),Path(__file__)]}))
    print(dict(reused_records=len(reused),fresh_records=len(fresh_rows),pages=sum(r['expected_native_pages'] for r in plan['records']),
        reused_alignments=4*len(reused),fresh_alignments=fresh['fresh_compiled_alignments'],new_credit=0))

if __name__=='__main__':main()
