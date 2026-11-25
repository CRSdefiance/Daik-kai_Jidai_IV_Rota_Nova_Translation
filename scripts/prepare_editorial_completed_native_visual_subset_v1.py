"""Prepare scoped visual evidence from durable complete receipts after an interrupted run."""
import argparse
from collections import defaultdict
from pathlib import Path
import runpy
import sys
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--run-dir',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--blocks',type=int,nargs='+',required=True);ap.add_argument('--expected-records',type=int,required=True)
    ap.add_argument('--use-existing-sheets',action='store_true');args=ap.parse_args();assert not args.out.exists()
    runpath=args.run_dir/'native_run_inputs.json';run=load(runpath)
    assert digest(run['manuscript'])==run['manuscript_sha256'] and digest(run['plan'])==run['plan_sha256']
    doc=load(run['manuscript']);plans={r['id']:r for r in load(run['plan'])['records']}
    rows=[];bindings=[];missing=[];grouped=defaultdict(list)
    for original in doc['records']:
        if original['block'] not in args.blocks:continue
        path=args.run_dir/('complete_'+original['id']+'.json')
        if not path.exists():missing.append(original['id']);continue
        proof=load(path);row=proof['record']
        assert proof['four_native_alignment_cases_pass'] and proof['all_original_native_glyph_pixels_consumption_canaries_bounds_androw_assertions_pass']
        assert digest(proof['native_run_inputs'])==proof['native_run_inputs_sha256']==digest(runpath)
        assert row['id']==original['id'] and row['logical_English']==original['english'] and row['compiled_hex']==plans[row['id']]['encoded_hex']
        assert all(row[k]==original[k] for k in ['source_reference','current_reference']) and len(row['native_alignment']['cases'])==4
        display=row['complete_native_English_display'];pages=display['pages'] if row['kind']=='progressive' else [display]
        for page in pages:
            assert digest(page['preview'])==page['preview_sha256'] and digest(page['native_plane'])==page['native_plane_sha256']
            grouped[row['block']].append(page)
        rows.append(row);bindings.append(dict(id=row['id'],receipt=str(path),receipt_sha256=digest(path),compiled_hex=row['compiled_hex']))
    assert len(rows)==args.expected_records and len({r['id'] for r in rows})==len(rows)
    args.out.mkdir(parents=True);sheets=[]
    if args.use_existing_sheets:
        assert not missing,'Existing full-block sheet positions cannot be inferred for an incomplete block.'
        for block,pages in sorted(grouped.items()):
            for start in range(0,len(pages),12):
                path=args.run_dir/f'B{block}_part{start//12+1}.png'
                assert path.exists();sheets.append(dict(block=block,path=str(path),sha256=digest(path),pages=len(pages[start:start+12])))
    else:
        selected=args.out/'scoped_receipt_selection.json'
        save(selected,dict(native_selection_complete=True,remaining_records=0,complete_body_candidates=len(rows),reused_native_records=bindings,
            subset_only_not_complete_batch=True,full_source_run_completion_not_inferred=True,missing_block_records_not_approved=missing,new_credit=0))
        before=sys.argv[:]
        try:
            sys.argv=[__file__,'--selection',str(selected),'--out',str(args.out/'sheets')]
            runpy.run_module('scripts.render_editorial_selected_native_sheets_v1',run_name='__main__')
        finally:sys.argv=before
        rendered=load(args.out/'sheets/selected_native_pages.json');assert rendered['records']==rows
        sheets=rendered['review_sheets']
    save(args.out/'scoped_native_pages.json',dict(records=rows,pages=sum(map(len,grouped.values())),runtime=run['runtime'],font_sha256=run['font_sha256'],
        review_sheets=sheets,all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass=True,complete_consumption_andpagination_exact=True,
        all_native_assertions_are_exact_per_record_complete_receipts_not_a_completed_parent_run=True,
        selected_alignment_cases=4*len(rows),source_run=str(runpath),source_run_sha256=digest(runpath),
        full_source_run_completion_not_inferred=True,subset_only_not_complete_batch=True,missing_block_records_not_approved=missing,
        direct_visual_review_pending=True,actual_gameplay=False,new_credit=0,evidence={str(p):digest(p) for p in [runpath,__file__]}))
    print(dict(scoped_records=len(rows),pages=sum(map(len,grouped.values())),sheets=len(sheets),direct_review_pending=True,full_batch_approval=False))


if __name__=='__main__':main()
