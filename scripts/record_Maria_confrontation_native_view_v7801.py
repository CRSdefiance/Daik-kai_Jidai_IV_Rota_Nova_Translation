"""Record16 native pages viewed,including the corrected short-sentence wrap."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_confrontation_native_view_v7801')
PLAN=Path('work/analysis/maria_confrontation_wrap_v7799/16_plans_one_sentence_coherence_refinement_no_prose_change.json')
FONT=Path('work/analysis/maria_confrontation_final_pages_v7800/16_final_compiled_pages4_fresh60_exact_reused_alignments.json')
PRIOR=Path('work/analysis/maria_confrontation_pages_v7798/16_compiled64_alignments_complete_native_pages.json')
if __name__=='__main__':
    assert not ROOT.exists();plan,font,prior=map(read,[PLAN,FONT,PRIOR]);assert font['plan_sha256']==sha(PLAN.read_bytes())
    sheets=prior['review_sheets'];previews=font['review_previews'];assert len(sheets)==3 and len(previews)==1
    for p in [*sheets,*previews]:assert sha(Path(p['path']).read_bytes())==p['sha256']
    rows=[]
    for p,n in zip(plan['records'],font['records'],strict=True):
        assert p['id']==n['id'] and p['encoded_hex']==n['compiled_hex'] and len(n['pages'])==p['expected_native_pages']==1
        assert not any(i['severity'] in ['warning','error'] for i in p['base_QA']['issues'])
        row_reason=p.get('row_count_reason')
        if any(i['code']=='line-break-count' for i in p['base_QA']['issues']):assert row_reason
        rows.append(dict(id=p['id'],file_path=p['file_path'],block=p['block'],source_record_index=p['source_record_index'],
            compiled_hex=p['encoded_hex'],lines=p['lines'],line_lengths=p['line_lengths'],
            base_QA_issues=p['base_QA']['issues'],row_count_reason=row_reason,qa_waivers=[],
            complete_native_page=n['pages'][0],all_visible_first_internal_final_glyphs_andword_boundaries_reviewed=True))
    assert len(rows)==16 and sum(i['code']=='line-break-count' for r in rows for i in r['base_QA_issues'])==9
    ROOT.mkdir(parents=True);save(ROOT/'16_native_pages_three_sheets_one_final_preview_viewed.json',dict(
        plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),native_proof=str(FONT),native_proof_sha256=sha(FONT.read_bytes()),
        records=rows,all_three_original_sheets_andone_final_changed_preview_individually_viewed=True,
        fifteen_exact_unchanged_pages_andone_final_sentence_coherence_page=True,nine_individual_row_count_infos_no_warnings_orwaivers=True,
        one_source_scoped_sentence_wrap_preference_not_manual_break_or_global_QA_change=True,
        old_failed_FI_FO_order_plan_andearlier_split_sentence_proof_preserved=True,
        all16_formatting_gates_false_stored_controls_actual_reference_policy_release_pending=True,
        not_actual_scene_nameplate_portrait_palette_button_ortransition_coverage=True,
        evidence={str(p):sha(p.read_bytes()) for p in [PLAN,FONT,PRIOR,Path(__file__)]},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('16native pages viewed;three sheets plusone corrected preview;9row-count infos/no warnings.All16formatting gates remainfalse untilstored/control/actual/release checks.')
