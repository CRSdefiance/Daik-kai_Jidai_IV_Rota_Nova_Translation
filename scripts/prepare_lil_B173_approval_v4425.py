"""Prepare native approval after both complete B173 sheets were viewed."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B173_approval_tools_v4425')
if __name__=='__main__':
    assert not ROOT.exists()
    old=Path('scripts/approve_lil_B172_native_v4378.py').read_text(encoding='utf-8')
    review=next(line for line in old.splitlines() if "'review': 'Viewed complete native sheet:" in line)
    replacement="                       'review': 'Viewed complete native sheet: every leading/internal/trailing glyph is present,zero row origins and four-row bounds hold. Lil tentative inquiry,search excitement,surprise,named tomb echo and competitive inference follow naturally from Reika guarded recognition,secondhand beauty,recent repeated question,uncertain name/smooth-talker recollection and reported destination. Silla Gold Crown and Tomb of King Muryeong remain intact. All three working retentions read coherently in the complete exchange. Ordinary complete-word wraps preserve all words. No extra relationship,location fact or completed progress. Offline native rendering only.'})"
    tool=derive('scripts/approve_lil_B172_native_v4378.py','scripts/approve_lil_B173_native_v4425.py',{
        review:replacement,'all27':'all11','all four complete native sheets':'both complete native sheets',
        'lil_B172_layout_v1':'lil_B173_layout_v1','lil_B172_profile':'lil_B173_profile',
        'lil_B172_native_approval_v4378':'lil_B173_native_approval_v4425','lil_B172_editorial':'lil_B173_editorial','lil_B172_fonts_v4377':'lil_B173_fonts_v4424',
        "len(font['cases']) == 27":"len(font['cases']) == 11","font['current_original_macro_alignment_calls'] == 216":"font['current_original_macro_alignment_calls'] == 88",
        "len(font['negative_controls']) == 15":"len(font['negative_controls']) == 13",'blocks[172]':'blocks[173]',
        'len(sheets) == 4':'len(sheets) == 2','block=172':'block=173',
        "{'revise':19, 'retain-wording':8}":"{'revise':8, 'retain-wording':3}",
        "sum(bool(row.get('qa_waivers')) for row in doc['records']) == 13":"sum(bool(row.get('qa_waivers')) for row in doc['records']) == 5",
        "names = read(names_path)['native_six_consumer_cases']['rows']":"names = read(names_path)['native_four_consumer_cases']['rows']",
        'assert len(names) == 6':'assert len(names) == 4','in [2,26]':'in [2]','actor_ID\']==201':'actor_ID\']==202',
        'current_original_macro_alignment_calls=216,new_current_original_macro_alignment_calls=216':'current_original_macro_alignment_calls=88,new_current_original_macro_alignment_calls=88',
        'progressive_planes=27':'progressive_planes=11','source_macro_absence_and_three_selectors_preserved':'source_macro_absence_and_two_selectors_preserved',
        'source_five_presentations_three_resources_C200_then_A000_and_single_end_preserved':'source_two_presentations_two_resources_one_predicate_four_relative_sites_two_A000s_and_single_end_preserved',
        'source_later_A000_retained_without_packed_semantics_or_earned_event_claim':'source_two_A000s_and_predicate_retained_without_packed_semantics_or_earned_event_claim',
        'revised=19,retained=8':'revised=8,retained=3','current_macro_alignment_cases=216':'current_macro_alignment_cases=88',
        'source_consumer_negatives=15':'source_consumer_negatives=13','narrow_row_count_notes=13':'narrow_row_count_notes=5',
        'actual_selected_B172_IDs':'actual_selected_B173_IDs',
        'B172:27 five-gate reviews approved,19 revisions/8 retentions;27 native planes/216 original alignment cases;15 source-consumer,3 macro-absence and14 formatter rejection controls.':'B173:11 five-gate reviews approved,8 revisions/3 retentions;11 native planes/88 original alignment cases;13 source-consumer,3 macro-absence and14 formatter rejection controls.',
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,both_complete_native_sheets_viewed=True,source_objects=11,revised=8,retained=3,
        original_name_paths=dict(Lil_owned=2,Reika_readonly=2),no_shared_metric_or_guard_change=True,no_new_credit=True,full_goal_complete=False))
    print('Prepared B173 native approval from both viewed complete sheets;actual scene and registered integration remain pending.')
