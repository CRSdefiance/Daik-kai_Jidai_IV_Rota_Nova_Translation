"""Seal the 278 complete Lil reviews after storage and representative gameplay."""

from scripts.finalize_lil361_research_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'Seal305 mixed source reviews': 'Seal 278 mixed source reviews',
    'Lil361_B283_B298_clean_20261110': 'Lil278_B299_B311_clean_20261110',
    'lil_B283_B298_': 'lil_B299_B311_',
    'plan_v6/automatic_plans.json': 'plan_visual_final_v1/automatic_plans.json',
    'formatting_v1/role_bindings.json': 'formatting_v1/role_bindings_v2.json',
    "len(doc['records']) == 361 and Counter(r['decision'] for r in doc['records']) == {'revision':178, 'retention':183}":
        "len(doc['records']) == 278 and Counter(r['decision'] for r in doc['records']) == {'revision':170, 'retention':108}",
    "len(d['catalogue']['records']) == 352": "len(d['catalogue']['records']) == 272",
    "len(stored['records']) == 175 and len(stored['style_records']) == 177 and stored['typed_labels_checked'] == 9":
        "len(stored['records']) == 133 and len(stored['style_records']) == 139 and stored['typed_labels_checked'] == 6",
    '(353, 353, 1408)': '(280, 280, 1088)',
    '(91, 262, 875)': '(67, 213, 670)',
    '(177, 192, 24)': '(139, 144, 18)',
    "sum(len(r['rejected']) for r in d['styles']['compiler_negatives']) == 216":
        "sum(len(r['rejected']) for r in d['styles']['compiler_negatives']) == 162",
    "len(d['menus']['menus']) == 4": "len(d['menus']['menus']) == 3",
    '(86324,4,199,200)': '(25121,1,52,55)',
    "actual['observed_pages_including_repeats'] == 242 and actual['offline_only_source_body_objects'] == 153":
        "actual['observed_pages_including_repeats'] == 55 and actual['offline_only_source_body_objects'] == 220",
    'repaired_R50_FE_no_blank_row_andnormal_A_return_observed': 'revised_Basra_Market_Info_page_turn_observed',
    'three_choice_Other_andtwo_choice_Run_andWait_cursors_andfollowing_A_returns_observed':
        'all_three_two_choice_menus_and_following_A_returns_observed',
    "    assert (len(delta['changed_record_IDs']),delta['old_pages'],delta['final_pages'],delta['reclaimed_pages']) == (9,353,353,0)":
        "    assert delta['counts']=={'plan_v1':25,'plan_v2':23} and delta['native_page_count']==280",
    "delta['all_logical_prose_unchanged'] and delta['FE_physical228px_width_font_runtime_andcontrols_unchanged']":
        "delta['all_logical_prose_unchanged'] and delta['plan_sha256']==digest(paths['plan'])",
    "rebuilt['source_editorial_objects'] == 361": "rebuilt['source_editorial_objects'] == 278",
    'all361_individual_five_gates_pass': 'all278_individual_five_gates_pass',
    'native_body_pages=353, source_editorial_body_objects=352, actual_source_body_objects=199':
        'native_body_pages=280, source_editorial_body_objects=272, actual_source_body_objects=52',
    'actual_body_pages=200, observed_pages_including_repeats=242, offline_only_source_body_objects=153':
        'actual_body_pages=55, observed_pages_including_repeats=55, offline_only_source_body_objects=220',
    'actual_caption_strings=9': 'actual_caption_strings=6',
    "len(names['records']) == 15": "len(names['records']) == 10",
    'all15_individual_five_gates_pass_in_scoped_context': 'all10_individual_five_gates_pass_in_scoped_context',
    'source352_release_plans.json': 'source272_release_plans.json',
    'source_editorial_objects=361,': 'source_editorial_objects=278,',
    'source_body_objects=352, physical_native_bodies=352': 'source_body_objects=272, physical_native_bodies=272',
    'records=361, revisions=178, retentions=183, complete_exchanges=16':
        'records=278, revisions=170, retentions=108, complete_exchanges=13',
    'physical_body_candidates=352, native_body_pages=353, typed_labels=9, scoped_names=15, name_strings=19':
        'physical_body_candidates=272, native_body_pages=280, typed_labels=6, scoped_names=10, name_strings=11',
    'source_styles=177, source_style_objects=24, source_FE_records=15, physical_FE_panels=15':
        'source_styles=139, source_style_objects=18, source_FE_records=8, physical_FE_panels=8',
    'source_bound_layout_changes=9, additional_phrase_wrap_fixes=7, scoped_FE_guard_reserves=1':
        'source_bound_layout_changes=25, scoped_FE_guard_reserves=0',
    'observed_FE_blank_rows_repaired=1, pages_reclaimed=0, actual_source_body_objects=199':
        'observed_FE_blank_rows_repaired=0, pages_reclaimed=0, actual_source_body_objects=52',
    'actual_pages=200, observed_pages_including_repeats=242': 'actual_pages=55, observed_pages_including_repeats=55',
    'offline_only_source_body_objects=153, offline_only_caption_strings=0, actual_frames=86324, actual_runs=4, actual_menus=4':
        'offline_only_source_body_objects=220, offline_only_caption_strings=0, actual_frames=25121, actual_runs=1, actual_menus=3',
    'Sealed361 five-gate reviews and15 scoped names:178 revisions/183 retentions. Registration/once-only credit remain.':
        'Sealed 278 five-gate reviews and 10 scoped names. Registration and coverage credit remain.',
})


if __name__ == '__main__':
    exec(compile(source, __file__, 'exec'), globals())
