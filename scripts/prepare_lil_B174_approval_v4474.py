"""Prepare approval after viewing five full sheets and the corrected fourth sheet."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B174_approval_tools_v4474')
if __name__=='__main__':
    assert not ROOT.exists()
    old=Path('scripts/approve_lil_B173_native_v4425.py').read_text(encoding='utf-8')
    review=next(line for line in old.splitlines() if "'review': 'Viewed complete native sheet:" in line)
    replacement="                       'review': 'All five complete initial sheets were viewed this turn. Final sheets1/2/3/5 are byte-identical to those viewed sheets; corrected final sheet4 was freshly viewed. Every leading/internal/trailing glyph is present, zero row origins and four-row bounds hold. Read the complete gratitude/gift, travel banter, actual-grandfather aspiration, acceptance, flattery, jealousy, employer explanation, conditional date and closing-aside exchange. Crown/tomb titles remain intact; R128 uses the natural complete conditional proposal and R124 no longer strands the auxiliary contraction. All ten working retentions remain coherent. No extra rank, romance status or earned progress. Offline native rendering only.'})"
    tool=derive('scripts/approve_lil_B173_native_v4425.py','scripts/approve_lil_B174_native_v4474.py',{
        review:replacement,'all11':'all33','viewing both complete native sheets':'viewing all five complete native sheets',
        'lil_B173_layout_v1':'lil_B174_layout_v2','lil_B173_profile':'lil_B174_profile',
        'lil_B173_native_approval_v4425':'lil_B174_native_approval_v4474',
        'lil_B173_editorial_manuscript_v2':'lil_B174_editorial_manuscript_v4',
        'lil_B173_editorial_manuscript_v3':'lil_B174_editorial_manuscript_v5',
        'lil_B173_fonts_v4424':'lil_B174_fonts_v4473',
        "len(font['cases']) == 11":"len(font['cases']) == 33",
        "font['current_original_macro_alignment_calls'] == 88":"font['current_original_macro_alignment_calls'] == 264",
        "len(font['negative_controls']) == 13":"len(font['negative_controls']) == 17",
        'blocks[173]':'blocks[174]','block=173':'block=174','len(sheets) == 2':'len(sheets) == 5',
        "{'revise':8, 'retain-wording':3}":"{'revise':23, 'retain-wording':10}",
        "sum(bool(row.get('qa_waivers')) for row in doc['records']) == 5":
            "sum(bool(row.get('qa_waivers')) for row in doc['records']) == 17",
        "names = read(names_path)['native_four_consumer_cases']['rows']":"names = read(names_path)['native_eight_consumer_cases']['rows']",
        'assert len(names) == 4':'assert len(names) == 8','in [2]':'in [2,14,26]',"actor_ID']==202":"actor_ID']==201",
        'current_original_macro_alignment_calls=88,new_current_original_macro_alignment_calls=88,reused_original_macro_alignment_calls=0':
            'current_original_macro_alignment_calls=264,new_current_original_macro_alignment_calls=8,reused_original_macro_alignment_calls=256',
        'progressive_planes=11':'progressive_planes=33','source_macro_absence_and_two_selectors_preserved':'source_macro_absence_and_four_selectors_preserved',
        'source_two_presentations_two_resources_one_predicate_four_relative_sites_two_A000s_and_single_end_preserved':
            'source_two_presentations_one_resource_conditional_Emilio_four_relative_sites_two_A000s_C200_single_end_preserved',
        'revised=8,retained=3':'revised=23,retained=10','current_macro_alignment_cases=88':'current_macro_alignment_cases=264',
        'source_consumer_negatives=13':'source_consumer_negatives=17','narrow_row_count_notes=5':'narrow_row_count_notes=17',
        'actual_selected_B173_IDs':'actual_selected_B174_IDs',
        'B173:11 five-gate reviews approved,8 revisions/3 retentions;11 native planes/88 original alignment cases;13 source-consumer,3 macro-absence and14 formatter rejection controls.':
            'B174:33 five-gate reviews approved,23 revisions/10 retentions;33 native planes/8 fresh plus256 exact-reused alignment cases;17 source-consumer,3 macro-absence and14 formatter rejection controls.',
    })
    # These receipts describe independent exact reuse, not a repeated full native run.
    before=read('work/analysis/lil_B174_fonts_v4470/current_macro_QA_and_progressive_font_proof.json')
    after=read('work/analysis/lil_B174_fonts_v4473/current_macro_QA_and_progressive_font_proof.json')
    assert (after['new_current_original_macro_alignment_calls'],after['reused_original_macro_alignment_calls'])==(8,256)
    assert len(after['exact_reused_IDs'])==32
    for n in [0,1,2,4]:
        assert before['review_sheets'][n]['sha256']==after['review_sheets'][n]['sha256']
    assert before['review_sheets'][3]['sha256']!=after['review_sheets'][3]['sha256']
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,all5_initial_sheets_viewed=True,
        final_sheet4_freshly_viewed=True,final_sheets1_2_3_5_exact_to_viewed_initials=True,
        all33_prose_and10_retentions_reconciled=True,source_macro_count=0,
        original_name_paths=dict(Lil_Emilio_Julian_owned=6,Mihwa_readonly=2),
        no_shared_metric_or_guard_change=True,no_new_credit=True,full_goal_complete=False))
    print('Prepared B174 five-gate approval, retaining exact reuse and original failure provenance.')
