"""Record all twelve sheets individually inspected; native display is not actual scene coverage."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_story_native_view_v7739')
NATIVE=Path('work/analysis/maria_story_pages_v7738/67_compiled268_alignments68_complete_native_pages.json')
PLAN=Path('work/analysis/maria_story_refined_v7735/67_refined_decisions_native_logical_bindings_automatic_plans_QA.json')
MANUSCRIPT=Path('translations/maria_B34_B108_B35_editorial_manuscript_v2.json')
if __name__=='__main__':
    assert not ROOT.exists();native,plan,doc=map(read,[NATIVE,PLAN,MANUSCRIPT])
    assert native['manuscript_sha256']==plan['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    assert len(native['review_sheets'])==12 and native['fresh_complete_native_page_renders']==68
    for sheet in native['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    rows=[]
    for n,p,r in zip(native['records'],plan['records'],doc['records'],strict=True):
        assert n['id']==p['id']==r['id'] and n['compiled_hex']==p['encoded_hex']
        assert len(n['pages'])==p['expected_native_pages'] and not any(i['severity'] in ['warning','error'] for i in p['base_QA']['issues'])
        for page in n['pages']:
            assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256'] and sha(Path(page['preview']).read_bytes())==page['preview_sha256']
        rows.append(dict(id=r['id'],file_path=r['file_path'],English=r['english'],lines=p['lines'],line_lengths=p['line_lengths'],
            native_pages=len(n['pages']),all_native_pages_individually_viewed=True,base_QA_issues=p['base_QA']['issues'],row_count_reason=p.get('row_count_reason'),
            native_proof=str(NATIVE),compiled_hex=p['encoded_hex'],qa_waivers=[],
            actual_button_pagination_andfull_scene_header_palette_transition_approval_pending=True))
    assert len(rows)==67 and sum('row_count_reason' in r and r['row_count_reason'] is not None for r in rows)==23
    ROOT.mkdir(parents=True);save(ROOT/'67_complete_paragraphs68_native_pages12_sheets_viewed.json',dict(
        records=rows,review_sheets=native['review_sheets'],all12_sheets_individually_viewed=True,all67_complete_paragraphs_reviewed_in_source_exchange_order=True,
        all68_native_pages_preserve_complete_leading_internal_trailing_glyphs_without_clipping_oroverlap=True,
        R111_second_page_resumes_at_exact_original_return_with_one_compiler_owned_guard=True,
        R111_long_report_retained_whole_without_clipping_omission_orinvented_prose=True,
        informational_row_count_changes=23,no_QA_warning_orerror_orwaiver=True,all_native_four_row_geometry_andguards_unchanged=True,
        full_width_216px_firstrows_andguarded_continuations_preserved=True,
        CP932_preview_shade_not_actual_scene_palette_approval=True,offline_native_checks_not_actual_gameplay=True,
        stored_policy_wholecontrols_actual_andregistered_integration_pending=True,all67_formatting_gates_false=True,
        no_ROM_registry_ledger_orcredit_change=True,new_emulator_runs=0,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [NATIVE,PLAN,MANUSCRIPT,Path(__file__)]},full_goal_complete=False))
    print('12sheets/67whole paragraphs/68complete native pages individually viewed;23 row-count infos,no warnings/waivers.Actual,stored,controls andrelease pending.')
