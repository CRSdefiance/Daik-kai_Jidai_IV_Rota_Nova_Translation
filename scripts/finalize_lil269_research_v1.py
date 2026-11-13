"""Seal all269 individual gates after complete stored and representative actual checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

prior = Path('scripts/finalize_maria305_research_v1.py').read_text(encoding='utf-8')
start = prior.index("    assert (actual['frames'], actual['initialized_runs']")
end = prior.index("    assert not any(actual[k]", start)
source = checked_text(prior, {
    'Maria_B176_B195_clean_20261110': 'Lil269_B243_B282_clean_20261110',
    'maria_B176_B195_': 'lil_B243_B282_',
    'contextual_review_v1.json': 'contextual_review_v3.json',
    'scoped_names_v1.json': 'scoped_names_v3.json',
    'formatting_v1/': 'formatting_v2/',
    'plan_v8/automatic_plans.json': 'plan_v13/automatic_plans.json',
    "len(doc['records']) == 305 and Counter(r['decision'] for r in doc['records']) == {'revision':205, 'retention':100}":
        "len(doc['records']) == 269 and Counter(r['decision'] for r in doc['records']) == {'revision':104, 'retention':165}",
    "len(d['catalogue']['records']) == 294": "len(d['catalogue']['records']) == 262",
    "len(stored['records']) == 272 and len(stored['style_records']) == 22 and stored['typed_labels_checked'] == 11":
        "len(stored['records']) == 246 and len(stored['style_records']) == 16 and stored['typed_labels_checked'] == 7",
    '(302, 302, 1176)': '(264, 264, 1048)',
    '(148, 154, 170)': '(117, 147, 990)',
    "(d['loaders']['fresh_whole_archive_loads_andcache_hits'], d['loaders']['fresh_parent_cases']) == (303, 606)":
        "(d['loaders']['whole_archive_loads_andcache_hits'], d['loaders']['parent_cases']) == (336, 672)",
    '== (22, 24, 3)': '== (16, 16, 2)',
    "sum(len(r['rejected']) for r in d['styles']['compiler_negatives']) == 27":
        "sum(len(r['rejected']) for r in d['styles']['compiler_negatives']) == 18",
    "len(d['menus']['menus']) == 5": "len(d['menus']['menus']) == 3",
    prior[start:end]: """    assert (actual['frames'],actual['initialized_runs'],actual['distinct_source_body_objects'],actual['distinct_body_pages']) == (64563,3,139,141)
    assert actual['observed_pages_including_repeats'] == 141 and actual['offline_only_source_body_objects'] == 123
    assert actual['all_actual_body_menu_andtransition_sheets_directly_viewed']
    assert actual['all_selected_current_pages_match_current_compiled_native_planes']
    assert actual['all_selected_two_page_turns_FE_andmenu_A_returns_observed']
    assert actual['repaired_riddle_complete_with_normal_A_return_observed']
    assert actual['three_choice_Right_andtwo_choice_No_cursor_andfollowing_A_return_observed']
    assert actual['complete_QA_host_nonspeech_setup_cleanup_andfollowing_tutorial_observed']
    delta=load(ROOT/'final_layout_delta_v1.json')
    assert (len(delta['changed_record_IDs']),delta['old_pages'],delta['final_pages'],delta['reclaimed_pages']) == (16,265,264,1)
    assert delta['no_prose_shortened_for_fit'] and delta['physical_width_font_andruntime_unchanged']
""",
    "rebuilt['source_editorial_objects'] == 305": "rebuilt['source_editorial_objects'] == 269",
    'all305_individual_five_gates_pass=True': 'all269_individual_five_gates_pass=True',
    'native_body_pages=302, source_editorial_body_objects=294, actual_source_body_objects=127':
        'native_body_pages=264, source_editorial_body_objects=262, actual_source_body_objects=139',
    'actual_body_pages=132, observed_pages_including_repeats=135, offline_only_source_body_objects=167':
        'actual_body_pages=141, observed_pages_including_repeats=141, offline_only_source_body_objects=123',
    'actual_caption_strings=7, offline_only_caption_strings=4': 'actual_caption_strings=7, offline_only_caption_strings=0',
    "len(names['records']) == 27": "len(names['records']) == 25",
    'all27_individual_five_gates_pass_in_scoped_context=True': 'all25_individual_five_gates_pass_in_scoped_context=True',
    'source294_release_plans.json': 'source262_release_plans.json',
    'source_editorial_objects=305,': 'source_editorial_objects=269,',
    'source_body_objects=294, physical_native_bodies=294': 'source_body_objects=262, physical_native_bodies=262',
    'records=305, revisions=205, retentions=100, complete_exchanges=19':
        'records=269, revisions=104, retentions=165, complete_exchanges=40',
    'physical_body_candidates=294, native_body_pages=302, typed_labels=11, scoped_names=27, name_strings=31':
        'physical_body_candidates=262, native_body_pages=264, typed_labels=7, scoped_names=25, name_strings=24',
    'source_styles=22, source_style_objects=3, source_FE_records=16, physical_FE_panels=16':
        'source_styles=16, source_style_objects=2, source_FE_records=36, physical_FE_panels=36',
    'source_bound_layout_changes=26, additional_phrase_wrap_fixes=17, scoped_FE_guard_reserves=2':
        'source_bound_layout_changes=16, additional_phrase_wrap_fixes=10, scoped_FE_guard_reserves=2',
    'observed_FE_blank_rows_repaired=1, pages_reclaimed=0, actual_source_body_objects=127':
        'observed_FE_blank_rows_repaired=1, pages_reclaimed=1, actual_source_body_objects=139',
    'actual_pages=132, observed_pages_including_repeats=135, actual_caption_strings=7':
        'actual_pages=141, observed_pages_including_repeats=141, actual_caption_strings=7',
    'offline_only_source_body_objects=167, offline_only_caption_strings=4, actual_frames=63843, actual_runs=3, actual_menus=3':
        'offline_only_source_body_objects=123, offline_only_caption_strings=0, actual_frames=64563, actual_runs=3, actual_menus=3',
    'Sealed305 five-gate reviews and27 scoped names:205 revisions/100 retentions. Registration/once-only credit remain.':
        'Sealed269 five-gate reviews and25 scoped names:104 revisions/165 retentions. Registration/once-only credit remain.',
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-individual-source-current-complete-storage-andactual-gates', 'exec'), globals())
