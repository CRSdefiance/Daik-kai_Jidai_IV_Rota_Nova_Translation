"""Bind each Lil254 editorial decision to stored and representative display proof."""

from scripts.finalize_lil278_research_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'Seal 278 mixed': 'Seal 254 mixed',
    'Lil278_B299_B311_clean_20261110': 'Lil254_B312_B319_clean_20261110',
    'lil_B299_B311_': 'lil_B312_B319_',
    'contextual_review_v1.json': 'contextual_review_v2.json',
    'scoped_names_v1.json': 'scoped_names_v2.json',
    'formatting_v1/formatting_input.json': 'formatting_v2/formatting_input.json',
    'formatting_v1/native_macro_measurements.json': 'formatting_v2/native_macro_measurements.json',
    'plan_visual_final_v1/automatic_plans.json': 'plan_v6/automatic_plans.json',
    "{'revision':170, 'retention':108}": "{'revision':151, 'retention':103}",
    '== 278': '== 254',
    '== 272': '== 246',
    "len(stored['records']) == 133 and len(stored['style_records']) == 139 and stored['typed_labels_checked'] == 6":
        "len(stored['records']) == 88 and len(stored['style_records']) == 158 and stored['typed_labels_checked'] == 8",
    '(280, 280, 1088)': '(251, 251, 984)',
    '(67, 213, 670)': '(41, 210, 330)',
    '(139, 144, 18)': '(158, 216, 27)',
    '== 162': '== 243',
    '(25121,1,52,55)': '(25841,1,53,58)',
    "actual['observed_pages_including_repeats'] == 55 and actual['offline_only_source_body_objects'] == 220":
        "actual['observed_pages_including_repeats'] == 58 and actual['offline_only_source_body_objects'] == 193",
    "actual['revised_Basra_Market_Info_page_turn_observed']":
        "actual['repaired_B316_alert_and_B319_company_substitution_observed'] and actual['both_B317_source_selector_00_headers_observed']",
    'all_three_two_choice_menus_and_following_A_returns_observed': 'all_three_menus_and_following_A_returns_observed',
    "delta['counts']=={'plan_v1':25,'plan_v2':23} and delta['native_page_count']==280":
        "delta['changed_records'] == len(delta['changes']) == 17 and delta['FE_blank_row_repaired'] == 'DK4_MES_B316_R0205'",
    "delta['all_logical_prose_unchanged'] and delta['plan_sha256']==digest(paths['plan'])":
        "delta['selected_plan_sha256']==digest(paths['plan']) and [r['id'] for r in delta['changes'] if r['prose_changed']] == ['DK4_MES_B319_R0008']",
    'all278_individual_five_gates_pass': 'all254_individual_five_gates_pass',
    'source272_release_plans.json': 'source246_release_plans.json',
    'source_editorial_objects=278': 'source_editorial_objects=254',
    'source_body_objects=272, physical_native_bodies=272': 'source_body_objects=246, physical_native_bodies=246',
    'records=278, revisions=170, retentions=108, complete_exchanges=13':
        'records=254, revisions=151, retentions=103, complete_exchanges=8',
    'physical_body_candidates=272, native_body_pages=280, typed_labels=6, scoped_names=10, name_strings=11':
        'physical_body_candidates=246, native_body_pages=251, typed_labels=8, scoped_names=10, name_strings=13',
    'native_body_pages=280, source_editorial_body_objects=272': 'native_body_pages=251, source_editorial_body_objects=246',
    'source_styles=139, source_style_objects=18, source_FE_records=8, physical_FE_panels=8':
        'source_styles=158, source_style_objects=27, source_FE_records=7, physical_FE_panels=7',
    'source_bound_layout_changes=25, scoped_FE_guard_reserves=0': 'source_bound_layout_changes=17, scoped_FE_guard_reserves=1',
    'observed_FE_blank_rows_repaired=0': 'observed_FE_blank_rows_repaired=1',
    'actual_source_body_objects=52': 'actual_source_body_objects=53',
    'actual_body_pages=55': 'actual_body_pages=58',
    'actual_pages=55': 'actual_pages=58',
    'observed_pages_including_repeats=55': 'observed_pages_including_repeats=58',
    'offline_only_source_body_objects=220': 'offline_only_source_body_objects=193',
    'actual_caption_strings=6': 'actual_caption_strings=8',
    'actual_frames=25121': 'actual_frames=25841',
    'Sealed 278 five-gate': 'Sealed 254 five-gate',
})


if __name__ == '__main__':
    exec(compile(source, __file__, 'exec'), globals())
