"""Seal321 source reviews only after the exact stored and representative display gates."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/finalize_maria305_research_v1.py').read_text(encoding='utf-8'), {
    'Maria_B176_B195_clean_20261110': 'Maria_B196_B215_clean_20261110',
    'maria_B176_B195_': 'maria_B196_B215_',
    'plan_v8/automatic_plans.json': 'plan_v5/automatic_plans.json',
    "len(doc['records']) == 305 and Counter(r['decision'] for r in doc['records']) == {'revision':205, 'retention':100}":
        "len(doc['records']) == 321 and Counter(r['decision'] for r in doc['records']) == {'revision':171, 'retention':150}",
    "len(d['catalogue']['records']) == 294": "len(d['catalogue']['records']) == 317",
    "len(stored['records']) == 272 and len(stored['style_records']) == 22 and stored['typed_labels_checked'] == 11":
        "len(stored['records']) == 296 and len(stored['style_records']) == 21 and stored['typed_labels_checked'] == 4",
    "stored['complete_stored_pages'] == native['pages'] == 302": "stored['complete_stored_pages'] == native['pages'] == 325",
    "== (22, 24, 3)": "== (21, 24, 3)",
    "len(d['menus']['menus']) == 5": "len(d['menus']['menus']) == 2",
    '(63843, 3, 127, 132)': '(73443, 3, 156, 162)',
    "actual['observed_pages_including_repeats'] == 135 and actual['offline_only_source_body_objects'] == 167":
        "actual['observed_pages_including_repeats'] == 178 and actual['offline_only_source_body_objects'] == 161",
    "actual['all135_actual_pages_seven_captions_andthree_host_transitions_directly_viewed']":
        "actual['all178_actual_pages_four_captions_andthree_host_transitions_directly_viewed']",
    "actual['all_five_two_page_turns_andfollowing_calls_observed']":
        "actual['all_six_two_page_turns_andfollowing_calls_observed']",
    "actual['repaired_B177_FE_panel_complete_andnormal_A_return_observed'] and actual['both_fullwidth_I_replacements_original_FA_andGuan_Yu_translation_observed']":
        "actual['Frozen_Rose_FE_complete_andnormal_A_return_observed'] and actual['repaired_strength_of_mind_page_andreclaimed_Jam_page_observed']",
    "actual['parrot_complete_echo_exchange_andEmilio_first_person_replies_observed'] and actual['both_letter_page_turns_signatures_andSailor_headers_observed']":
        "actual['Boy_andSailor_headers_andcorrected_Julio_departure_instruction_observed'] and actual['Ian_andJam_letters_signatures_andscoped_name_headers_observed']",
    "rebuilt['source_editorial_objects'] == 305": "rebuilt['source_editorial_objects'] == 321",
    'all305_individual_five_gates_pass=True': 'all321_individual_five_gates_pass=True',
    'native_body_pages=302, source_editorial_body_objects=294, actual_source_body_objects=127':
        'native_body_pages=325, source_editorial_body_objects=317, actual_source_body_objects=156',
    'actual_body_pages=132, observed_pages_including_repeats=135, offline_only_source_body_objects=167':
        'actual_body_pages=162, observed_pages_including_repeats=178, offline_only_source_body_objects=161',
    'actual_caption_strings=7, offline_only_caption_strings=4': 'actual_caption_strings=4, offline_only_caption_strings=0',
    "parent_manuscript=str(paths['source']), parent_manuscript_sha256=digest(paths['source']), new_credit=0, full_goal_complete=False)":
        "parent_manuscript=str(paths['source']), parent_manuscript_sha256=digest(paths['source']), native_macro_tokens_still_require_formatter_marking=False, no_new_formatted_pages_orbatch_gameplay_orintegration_claim=False, new_credit=0, full_goal_complete=False)",
    "len(names['records']) == 27": "len(names['records']) == 24",
    'all27_individual_five_gates_pass_in_scoped_context=True, all_name_formatting_gates_pending=False':
        'all24_individual_five_gates_pass_in_scoped_context=True, all_name_formatting_gates_pending=False, formatting_gates_pending=False',
    'source294_release_plans.json': 'source317_release_plans.json',
    'source_editorial_objects=305,': 'source_editorial_objects=321,',
    'source_body_objects=294, physical_native_bodies=294': 'source_body_objects=317, physical_native_bodies=317',
    'records=305, revisions=205, retentions=100, complete_exchanges=19':
        'records=321, revisions=171, retentions=150, complete_exchanges=18',
    'physical_body_candidates=294, native_body_pages=302, typed_labels=11, scoped_names=27, name_strings=31':
        'physical_body_candidates=317, native_body_pages=325, typed_labels=4, scoped_names=24, name_strings=28',
    'source_styles=22, source_style_objects=3, source_FE_records=16, physical_FE_panels=16':
        'source_styles=21, source_style_objects=3, source_FE_records=2, physical_FE_panels=2',
    'source_bound_layout_changes=26, additional_phrase_wrap_fixes=17, scoped_FE_guard_reserves=2':
        'source_bound_layout_changes=19, additional_directly_viewed_page_repairs=1, scoped_FE_guard_reserves=0',
    'observed_FE_blank_rows_repaired=1, pages_reclaimed=0, actual_source_body_objects=127':
        'observed_FE_blank_rows_repaired=0, pages_reclaimed=1, actual_source_body_objects=156',
    'actual_pages=132, observed_pages_including_repeats=135, actual_caption_strings=7':
        'actual_pages=162, observed_pages_including_repeats=178, actual_caption_strings=4',
    'offline_only_source_body_objects=167, offline_only_caption_strings=4, actual_frames=63843, actual_runs=3, actual_menus=3':
        'offline_only_source_body_objects=161, offline_only_caption_strings=0, actual_frames=73443, actual_runs=3, actual_menus=2',
    'FINAL, NAMES, source_plan, Path(__file__)]':
        "FINAL, NAMES, source_plan, Path('scripts/finalize_maria305_research_v1.py'), Path(__file__)]",
    'Sealed305 five-gate reviews and27 scoped names:205 revisions/100 retentions. Registration/once-only credit remain.':
        'Sealed321 five-gate reviews and24 scoped names:171 revisions/150 retentions. Registration/once-only credit remain.',
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::same-source-current-stored-actual-andindividual-five-gate-contract-current-scope', 'exec'), globals())
