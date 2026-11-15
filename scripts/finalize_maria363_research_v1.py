"""Seal363 individual reviews using the unchanged five-gate contract and exact scope."""
from scripts.finalize_maria321_research_v3 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'Maria_B196_B215_clean_20261110':'Maria_B216_B252_clean_20261110',
    'maria_B196_B215_':'maria_B216_B252_',
    'formatting_v1/formatting_input.json':'formatting_v1/formatting_input_v2.json',
    'contextual_review_v1.json':'contextual_review_v2.json',
    'plan_v5/automatic_plans.json':'plan_v8/automatic_plans.json',
    'formatting_v1/role_bindings.json':'formatting_v1/role_bindings_v2.json',
    "len(doc['records']) == 321 and Counter(r['decision'] for r in doc['records']) == {'revision':171, 'retention':150}":
        "len(doc['records']) == 363 and Counter(r['decision'] for r in doc['records']) == {'revision':202, 'retention':161}",
    "len(d['catalogue']['records']) == 317":"len(d['catalogue']['records']) == 351",
    "len(stored['records']) == 296 and len(stored['style_records']) == 21 and stored['typed_labels_checked'] == 4":
        "len(stored['records']) == 266 and len(stored['style_records']) == 85 and stored['typed_labels_checked'] == 12",
    '(325, 325, 1268)':'(353, 353, 1404)',
    '(156, 169, 120)':'(131, 222, 940)',
    '== (21, 24, 3)':'== (85, 96, 12)',
    "sum(len(r['rejected']) for r in d['styles']['compiler_negatives']) == 27":"sum(len(r['rejected']) for r in d['styles']['compiler_negatives']) == 108",
    "len(d['menus']['menus']) == 2":"len(d['menus']['menus']) == 5",
    '(73443, 3, 156, 162)':'(97683, 3, 252, 254)',
    "actual['observed_pages_including_repeats'] == 178 and actual['offline_only_source_body_objects'] == 161":
        "actual['observed_pages_including_repeats'] == 273 and actual['offline_only_source_body_objects'] == 99",
    'all178_actual_pages_four_captions_andthree_host_transitions_directly_viewed':'all273_actual_pages_twelve_captions_andthree_host_transitions_directly_viewed',
    'all_six_two_page_turns_andfollowing_calls_observed':'both_two_page_turns_andfollowing_calls_observed',
    'Frozen_Rose_FE_complete_andnormal_A_return_observed':'repaired_three_FE_panels_complete_andnormal_A_returns_observed',
    'repaired_strength_of_mind_page_andreclaimed_Jam_page_observed':'consecutive_menu_return_andboth_A_inputs_observed',
    'Boy_andSailor_headers_andcorrected_Julio_departure_instruction_observed':'restored_Jacob_reply_andWilliam_second_page_observed',
    'Ian_andJam_letters_signatures_andscoped_name_headers_observed':'runtime_selector216_only_offline_bound_andrendered',
    "rebuilt['source_editorial_objects'] == 321":"rebuilt['source_editorial_objects'] == 363",
    'all321_individual_five_gates_pass=True':'all363_individual_five_gates_pass=True',
    'native_body_pages=325, source_editorial_body_objects=317, actual_source_body_objects=156':'native_body_pages=353, source_editorial_body_objects=351, actual_source_body_objects=252',
    'actual_body_pages=162, observed_pages_including_repeats=178, offline_only_source_body_objects=161':'actual_body_pages=254, observed_pages_including_repeats=273, offline_only_source_body_objects=99',
    'actual_caption_strings=4, offline_only_caption_strings=0':'actual_caption_strings=12, offline_only_caption_strings=0',
    "len(names['records']) == 24":"len(names['records']) == 29",
    'all24_individual_five_gates_pass_in_scoped_context=True':'all29_individual_five_gates_pass_in_scoped_context=True',
    'source317_release_plans.json':'source351_release_plans.json',
    'source_editorial_objects=321,':'source_editorial_objects=363,',
    'source_body_objects=317, physical_native_bodies=317':'source_body_objects=351, physical_native_bodies=351',
    'records=321, revisions=171, retentions=150, complete_exchanges=18':'records=363, revisions=202, retentions=161, complete_exchanges=37',
    'physical_body_candidates=317, native_body_pages=325, typed_labels=4, scoped_names=24, name_strings=28':'physical_body_candidates=351, native_body_pages=353, typed_labels=12, scoped_names=29, name_strings=31',
    'source_styles=21, source_style_objects=3, source_FE_records=2, physical_FE_panels=2':'source_styles=85, source_style_objects=12, source_FE_records=38, physical_FE_panels=38',
    'source_bound_layout_changes=19, additional_directly_viewed_page_repairs=1, scoped_FE_guard_reserves=0':'source_bound_layout_changes=15, additional_directly_viewed_page_repairs=1, scoped_FE_guard_reserves=3',
    'observed_FE_blank_rows_repaired=0, pages_reclaimed=1, actual_source_body_objects=156':'observed_FE_blank_rows_repaired=1, pages_reclaimed=0, actual_source_body_objects=252',
    'actual_pages=162, observed_pages_including_repeats=178, actual_caption_strings=4':'actual_pages=254, observed_pages_including_repeats=273, actual_caption_strings=12',
    'offline_only_source_body_objects=161, offline_only_caption_strings=0, actual_frames=73443, actual_runs=3, actual_menus=2':'offline_only_source_body_objects=99, offline_only_caption_strings=0, actual_frames=97683, actual_runs=3, actual_menus=5',
    "Path('scripts/finalize_maria321_research_v2.py'), Path(__file__)]":"Path('scripts/finalize_maria321_research_v2.py'), Path('scripts/finalize_maria321_research_v3.py'), Path(__file__)]",
    'Sealed321 five-gate reviews and24 scoped names:171 revisions/150 retentions. Registration/once-only credit remain.':'Sealed363 five-gate reviews and29 scoped names:202 revisions/161 retentions. Registration/once-only credit remain.',
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::same-five-individual-gates-exact-current-native-stored-andactual-evidence', 'exec'), globals())
