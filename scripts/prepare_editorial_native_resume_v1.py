"""Resume only unproved final layouts from exact, durable per-record native receipts."""
import argparse
from pathlib import Path
import runpy
import sys
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for arg in ['manuscript','plan','macro-proof','out']:ap.add_argument('--'+arg,type=Path,required=True)
    ap.add_argument('--receipts',type=Path,nargs='+',required=True);args=ap.parse_args();assert not args.out.exists()
    doc,plan=map(load,[args.manuscript,args.plan]);assert plan['manuscript_sha256']==digest(args.manuscript) and not plan['failures']
    font_sha=sha(NdsImage.open(doc['current_ROM']).read_file('/GRP/KANJI.FNT'))
    manuscript={r['id']:r for r in doc['records']};chosen=[];pending=[];runs={}
    for target in plan['records']:
        ident=target['id'];original=manuscript[ident];match=None
        for directory in args.receipts:
            path=directory/('complete_'+ident+'.json')
            if not path.exists():continue
            proof=load(path);row=proof['record']
            if row['compiled_hex']!=target['encoded_hex']:continue
            assert all(row[k]==original[k] for k in ['source_reference','current_reference']) and row['logical_English']==original['english']
            assert row['kind']==original['kind'] and proof['four_native_alignment_cases_pass']
            assert proof['all_original_native_glyph_pixels_consumption_canaries_bounds_androw_assertions_pass'] and not proof['actual_gameplay']
            run_path=Path(proof['native_run_inputs']);assert digest(run_path)==proof['native_run_inputs_sha256']
            if str(run_path) not in runs:runs[str(run_path)]=load(run_path)
            run=runs[str(run_path)]
            assert run['runtime']==doc['runtime'] and run['font_sha256']==font_sha and run['all_v1_native_assertions_preserved']
            assert run['macro_proof_sha256']==digest(args.macro_proof)
            assert run['producer_sha256']==digest('scripts/check_editorial_compiled_pages_explicit_captain_v2.py')
            assert len(row['native_alignment']['cases'])==4
            display=row['complete_native_English_display'];pages=display['pages'] if row['kind']=='progressive' else [display]
            assert len(pages)==target['expected_native_pages']
            for page in pages:
                assert digest(page['preview'])==page['preview_sha256'] and digest(page['native_plane'])==page['native_plane_sha256']
            match=dict(id=ident,receipt=str(path),receipt_sha256=digest(path),compiled_hex=target['encoded_hex'],pages=len(pages),
                exact_runtime_font_macro_source_current_paragraph_andfour_alignment_native_pixels_reused=True,direct_visual_review_separate=True)
            break
        if match:chosen.append(match)
        else:pending.append(ident)
    assert len(chosen)+len(pending)==len(plan['records']) and pending
    sys.argv=['prepare_editorial_native_subset_v2','--manuscript',str(args.manuscript),'--plan',str(args.plan),'--out',str(args.out),'--ids',*pending]
    runpy.run_module('scripts.prepare_editorial_native_subset_v2',run_name='__main__')
    save(args.out/'resume_selection.json',dict(final_manuscript=str(args.manuscript),final_manuscript_sha256=digest(args.manuscript),
        final_plan=str(args.plan),final_plan_sha256=digest(args.plan),reused_native_records=chosen,reused_records=len(chosen),remaining_IDs=pending,
        remaining_records=len(pending),complete_body_candidates=len(plan['records']),exact_compatible_completed_receipts_not_replayed=True,
        all_fifth_gates_andremaining_native_visual_checks_pending=True,actual_gameplay=False,new_credit=0,
        evidence={str(p):digest(p) for p in [args.manuscript,args.plan,args.macro_proof,Path(__file__)]}))
    print(dict(reused_records=len(chosen),fresh_remaining_records=len(pending),new_credit=0))

if __name__=='__main__':main()
