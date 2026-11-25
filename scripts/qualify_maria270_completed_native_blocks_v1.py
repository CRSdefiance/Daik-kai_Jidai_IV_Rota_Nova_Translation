"""Qualify already completed native blocks from the later-failed run without replay."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

ROOT=Path('work/Maria_B37_B50_clean_20261109')
OUT=ROOT/'complete_B37_B49_projection_v1'

def main():
    receipt=OUT/'initial_native_qualified.json';plan_output=OUT/'initial_selected_plans.json'
    assert not receipt.exists() and not plan_output.exists()
    records_path=OUT/'initial_completed_block_records.json';completed=load(records_path)
    projection_path=OUT/'projection_qualification.json';q=load(projection_path)
    old_plan_path=Path(completed['initial_plan']);old_form_path=Path(completed['initial_manuscript'])
    assert digest(old_plan_path)==completed['initial_plan_sha256'] and digest(old_form_path)==completed['initial_manuscript_sha256']
    ctx=RegisteredRuntime(completed['runtime']['release_proof'],completed['runtime']['startup_proof'],captain=3)
    assert ctx.receipt()==completed['runtime']
    for item in completed['original_block_receipts']:
        assert digest(item['path'])==item['sha256']
    old=load(old_plan_path);ids={r['id'] for r in completed['records']}
    chosen=deepcopy(old);chosen.update(records=[r for r in old['records'] if r['id'] in ids],failures=[],
        complete_parent_plan=str(old_plan_path),complete_parent_plan_sha256=digest(old_plan_path),
        metadata_projection_only_all_selected_plan_objects_unchanged=True)
    assert len(chosen['records'])==len(ids)==266
    for row in completed['records']:
        rendered=row['complete_native_English_display']
        assert len(row['native_alignment']['cases'])==4
        if row['kind']=='progressive':
            assert rendered['all_visible_first_internal_final_characters_in_order'] and rendered['no_blank_or_overlap_page']
            assert rendered['complete_consumed_bytes']==len(bytes.fromhex(row['expanded_native_hex']))
            assert all(p['native_independent_plane_equal'] and p['all_bitmap_header_input_canaries_exact'] for p in rendered['pages'])
        else:
            assert rendered['all_first_internal_final_ASCII_CP932_codes_andindependent_logical_plane_exact']
            assert rendered['input_bitmap_header_view_context_canaries_andcomplete_return_exact']
            assert rendered['all_executed_instructions_exact_current_sections_andpayload']
            assert rendered['planned_native_row_comparison']['complete_glyph_row_membership_exact']
    save(plan_output,chosen)
    save(receipt,dict(manuscript=str(old_form_path),manuscript_sha256=digest(old_form_path),
        plan=str(plan_output),plan_sha256=digest(plan_output),runtime=ctx.receipt(),
        font_sha256=sha(ctx.image.read_file('/GRP/KANJI.FNT')),records=completed['records'],
        pages=276,fresh_compiled_alignments=0,previously_completed_native_alignments_qualified=1064,
        all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass=True,
        complete_consumption_andpagination_exact=True,review_sheets=q['directly_viewed_initial_body_sheets'],
        direct_visual_review_pending=False,formatting_gates_still_false=True,actual_gameplay=False,new_credit=0,
        qualified_completed_blocks_only_not_full_failed_run=True,
        original_B50_failure_preserved=True,no_native_calls_orpage_rasters_replayed=True,
        evidence={str(p):digest(p) for p in [records_path,projection_path,old_form_path,old_plan_path,Path(__file__)]}))
    print('Qualified266 already completed native bodies/276 directly viewed pages/1064 prior alignment cases;no replay ornew credit.')

if __name__=='__main__':main()
