"""Keep every per-record research gate for the315-source mixed Maria scope."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

prior = Path('scripts/finalize_maria305_research_v1.py').read_text(encoding='utf-8')
start = prior.index("    assert (actual['frames'], actual['initialized_runs']")
end = prior.index("    assert not any(actual[k]", start)
source = checked_text(prior, {
    'Maria_B176_B195_clean_20261110': 'Maria_B286_B302_clean_20261110',
    'maria_B176_B195_': 'maria_B286_B302_',
    'plan_v8/automatic_plans.json': 'plan_v5/automatic_plans.json',
    'compiled_styles_v2/compiled_style_objects.json': 'compiled_styles_v3/compiled_style_objects.json',
    "len(doc['records']) == 305 and Counter(r['decision'] for r in doc['records']) == {'revision':205, 'retention':100}":
        "len(doc['records']) == 315 and Counter(r['decision'] for r in doc['records']) == {'revision':162, 'retention':153}",
    "len(d['catalogue']['records']) == 294": "len(d['catalogue']['records']) == 309",
    "len(stored['records']) == 272 and len(stored['style_records']) == 22 and stored['typed_labels_checked'] == 11":
        "len(stored['records']) == 196 and len(stored['style_records']) == 113 and stored['typed_labels_checked'] == 6",
    '(302, 302, 1176)': '(309, 309, 1236)',
    '(148, 154, 170)': '(97, 212, 320)',
    '== (22, 24, 3)': '== (113, 136, 17)',
    "sum(len(r['rejected']) for r in d['styles']['compiler_negatives']) == 27":
        "sum(len(r['rejected']) for r in d['styles']['compiler_negatives']) == 153",
    "len(d['menus']['menus']) == 5": "len(d['menus']['menus']) == 3",
    prior[start:end]: """    assert (actual['frames'],actual['initialized_runs'],actual['distinct_source_body_objects'],actual['distinct_body_pages']) == (91844,4,213,213)
    assert actual['observed_pages_including_repeats'] == 213 and actual['offline_only_source_body_objects'] == 96
    assert actual['all_actual_body_menu_andtransition_sheets_directly_viewed']
    assert actual['all_selected_current_pages_match_current_compiled_native_planes']
    assert actual['original_Rafael0_Lil2_headers_corrected_I_original_FA_andboth_FI_macros_observed']
    assert actual['all17_effective_voice4_objects_andall_three_menu_returns_observed']
    assert actual['all13_FE_panels_andfollowing_A_returns_observed']
    assert actual['conqueror_warning_complete_on_one_page_andfollowing_call_observed']
    assert actual['all_changed_text_single_page_no_new_multipage_behavior']
    assert actual['complete_QA_host_nonspeech_setup_cleanup_andreturn_to_sailing_observed']
    layout_delta=load(ROOT/'final_layout_delta_v1.json')
    assert (layout_delta['final_layout_changes'],layout_delta['phrase_wrap_improvements'],layout_delta['pages_reclaimed']) == (7,6,1)
    assert layout_delta['no_prose_shortening_or_font_width_runtime_control_change']
""",
    "rebuilt['source_editorial_objects'] == 305": "rebuilt['source_editorial_objects'] == 315",
    'all305_individual_five_gates_pass=True': 'all315_individual_five_gates_pass=True',
    'native_body_pages=302, source_editorial_body_objects=294, actual_source_body_objects=127':
        'native_body_pages=309, source_editorial_body_objects=309, actual_source_body_objects=213',
    'actual_body_pages=132, observed_pages_including_repeats=135, offline_only_source_body_objects=167':
        'actual_body_pages=213, observed_pages_including_repeats=213, offline_only_source_body_objects=96',
    'actual_caption_strings=7, offline_only_caption_strings=4':
        'actual_caption_strings=6, offline_only_caption_strings=0',
    "len(names['records']) == 27": "len(names['records']) == 14",
    'all27_individual_five_gates_pass_in_scoped_context=True': 'all14_individual_five_gates_pass_in_scoped_context=True',
    'source294_release_plans.json': 'source309_release_plans.json',
    'source_editorial_objects=305,': 'source_editorial_objects=315,',
    'source_body_objects=294, physical_native_bodies=294': 'source_body_objects=309, physical_native_bodies=309',
    'records=305, revisions=205, retentions=100, complete_exchanges=19':
        'records=315, revisions=162, retentions=153, complete_exchanges=17',
    'physical_body_candidates=294, native_body_pages=302, typed_labels=11, scoped_names=27, name_strings=31':
        'physical_body_candidates=309, native_body_pages=309, typed_labels=6, scoped_names=14, name_strings=18',
    'source_styles=22, source_style_objects=3, source_FE_records=16, physical_FE_panels=16':
        'source_styles=113, source_style_objects=17, source_FE_records=13, physical_FE_panels=13',
    'source_bound_layout_changes=26, additional_phrase_wrap_fixes=17, scoped_FE_guard_reserves=2':
        'source_bound_layout_changes=7, additional_phrase_wrap_fixes=6, scoped_FE_guard_reserves=0',
    'observed_FE_blank_rows_repaired=1, pages_reclaimed=0, actual_source_body_objects=127':
        'observed_FE_blank_rows_repaired=0, pages_reclaimed=1, actual_source_body_objects=213',
    'actual_pages=132, observed_pages_including_repeats=135, actual_caption_strings=7':
        'actual_pages=213, observed_pages_including_repeats=213, actual_caption_strings=6',
    'offline_only_source_body_objects=167, offline_only_caption_strings=4, actual_frames=63843, actual_runs=3, actual_menus=3':
        'offline_only_source_body_objects=96, offline_only_caption_strings=0, actual_frames=91844, actual_runs=4, actual_menus=3',
    "Path(__file__)]}))":
        "ROOT/'final_layout_delta_v1.json',Path('scripts/finalize_maria305_research_v1.py'),Path(__file__)]}))",
    'Sealed305 five-gate reviews and27 scoped names:205 revisions/100 retentions. Registration/once-only credit remain.':
        'Sealed315 five-gate reviews and14 scoped names:162 revisions/153 retentions. Registration/once-only credit remain.',
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::same-complete-per-record-source-current-native-stored-andactual-contract', 'exec'), globals())
