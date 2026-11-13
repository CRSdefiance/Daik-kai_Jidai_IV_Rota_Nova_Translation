"""Record the individually viewed Maria selection/opening and all18 native offline pages."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_view_v7691')
MANUSCRIPT=Path('translations/maria_B207_editorial_manuscript_v1.json')
PLAN=Path('work/analysis/maria_B207_layout_v7689/Maria18_automatic_full_width_plans_all_base_QA_preserved.json')
NATIVE=Path('work/analysis/maria_B207_pages_v7690/Maria18_complete_native_pages72_fresh_compiled_alignments.json')
CONTEXT=Path('work/analysis/maria_B207_native_v7681/own_current_Maria_captain3_strict2b6_context_binding.json')
REASONS={
8:'The complete familiar question and Daydreaming? fit one35-cell row. English does not need the Japanese staging break.',
11:'The retained surprise and return question fit one28-cell row without a new date, location or repeated name.',
36:'Three31/27/35-cell rows preserve personal recollection, reported historical prosperity and peak papal power, rather than copying four source rows.',
39:'Three34/32/15-cell rows preserve past agreement, lords, competition, donation kinds and quantities. The short trailing phrase carries the source continuation naturally.',
46:'The retained cooperative historical completion fits two31/26-cell rows; the Church phrase and decline remain complete.',
50:'Three28/25/33-cell rows preserve hard work and rueful great-grandfather envy. The complete-word My/great-grandfather continuation is readable within one original page; the compound itself stays intact. This is not an isolated glyph, authored break or change of viewport.',
63:'Three35/33/30-cell rows retain the courteous tentative introduction and explicit if-found condition. The complete-word we/found continuation keeps the paragraph on one original page; no word or conditional meaning is lost.',
}
if __name__=='__main__':
    assert not ROOT.exists();doc,plan,native,context=map(read,[MANUSCRIPT,PLAN,NATIVE,CONTEXT])
    assert native['layout_plan_sha256']==sha(PLAN.read_bytes()) and native['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    assert native['fresh_native_page_renders']==13 and native['exact_reused_native_page_renders']==5
    for sheet in native['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    opening=context['review_sheet'];assert sha(Path(opening['path']).read_bytes())==opening['sha256']
    rows=[];infos=0
    for r,p,n in zip(doc['records'],plan['records'],native['records'],strict=True):
        assert r['id']==p['id']==n['id'] and p['encoded_hex']==n['compiled_hex'] and len(n['pages'])==1
        issues=p['base_QA']['issues'];assert not any(i['severity'] in ['warning','error'] for i in issues)
        info=[i for i in issues if i['severity']=='info'];index=r['source_record_index'];assert bool(info)==(index in REASONS)
        infos+=len(info)
        rows.append(dict(id=r['id'],file_path=doc['file_path'],source_record_index=index,English=r['english'],compiled_hex=p['encoded_hex'],lines=p['lines'],line_lengths=p['line_lengths'],base_QA_issues=issues,row_count_reason=REASONS.get(index),qa_waivers=[],complete_native_page_reference=dict(path=str(NATIVE),id=r['id'],plane=n['pages'][0]['native_plane'],plane_sha256=n['pages'][0]['native_plane_sha256']),visually_reviewed_complete_paragraph=True,all_logical_words_andpunctuation_preserved=True,formatting_gate_still_false_stored_actual_policy_andrelease_pending=True))
    assert infos==7
    ROOT.mkdir(parents=True);save(ROOT/'Maria18_native_paragraphs_andown_selection_viewed_stored_actual_pending.json',dict(records=rows,all_three_native_page_sheets_individually_viewed=True,all18_paragraphs_reviewed_in_complete_exchange_order=True,review_sheets=native['review_sheets'],own_current_captain3_selection_andopening_sheet_individually_viewed=opening,existing_system_only_unlock_fixture=True,earned_unlock_verified=False,actual_NewGame_selection_opening_not_optional_B207_gameplay=True,all_base_QA_issues_preserved=True,informational_row_count_changes=7,base_QA_warning_orerror_count=0,no_qa_waivers=True,no_global_font_viewport_weak_ending_literal_I_F_orpairphase_change=True,retained_R4_three_CP932_ellipses_exact_font_reuse_not_actual_palette_claim=True,source22_Im_aboard_softwrap_is_complete_words_withnative_glyph_proof=True,source15_four_rows_are_needed_for_full_natural_teasing_paragraph_not_anarrowed_viewport=True,full_width_216px_36cell_firstrow_35cell_guarded_continuations_preserved=True,two_contextual_name_retentions_not_full_catalogue_UI_orfull207_approval=True,stored_bytes_policy_relocation_representative_actual_andregistered_release_pending=True,all18_formatting_gates_remain_false=True,no_ROM_registry_orledger_mutation=True,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [MANUSCRIPT,PLAN,NATIVE,CONTEXT,Path(__file__)]},full_goal_complete=False))
    print('Viewed Maria selection/opening andall3 native sheets/all18 paragraphs;7 row-count infos,no base warnings/errors orwaivers. Stored/actual/release pending.')
