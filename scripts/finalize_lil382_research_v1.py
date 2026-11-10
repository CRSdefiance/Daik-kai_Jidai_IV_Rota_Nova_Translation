"""Seal 382 individual reviews after source, complete display, storage and actual checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

prior = Path('scripts/finalize_maria305_research_v1.py').read_text(encoding='utf-8')
start = prior.index("    assert (actual['frames'], actual['initialized_runs']")
end = prior.index("    assert not any(actual[k]", start)
source = checked_text(prior, {
    'Maria_B176_B195_clean_20261110': 'Lil382_residual_A_clean_20261110',
    'maria_B176_B195_': 'lil_residual_A_382_',
    'plan_v8/automatic_plans.json': 'plan_v7/automatic_plans.json',
    'reconstruction_v1/reconstruction.json': 'reconstruction_v2/reconstruction.json',
    "len(doc['records']) == 305 and Counter(r['decision'] for r in doc['records']) == {'revision':205, 'retention':100}":
        "len(doc['records']) == 382 and Counter(r['decision'] for r in doc['records']) == {'revision':257, 'retention':125}",
    "len(d['catalogue']['records']) == 294": "len(d['catalogue']['records']) == 378",
    "len(stored['records']) == 272 and len(stored['style_records']) == 22 and stored['typed_labels_checked'] == 11":
        "len(stored['records']) == 364 and len(stored['style_records']) == 14 and stored['typed_labels_checked'] == 4",
    '(302, 302, 1176)': '(386, 386, 1512)',
    '(148, 154, 170)': '(180, 206, 555)',
    "(d['loaders']['fresh_whole_archive_loads_andcache_hits'], d['loaders']['fresh_parent_cases']) == (303, 606)":
        "(d['loaders']['whole_archive_loads_andcache_hits'], d['loaders']['parent_cases']) == (336, 672)",
    '== (22, 24, 3)': '== (14, 16, 2)',
    "sum(len(r['rejected']) for r in d['styles']['compiler_negatives']) == 27":
        "sum(len(r['rejected']) for r in d['styles']['compiler_negatives']) == 18",
    "len(d['menus']['menus']) == 5": "len(d['menus']['menus']) == 2",
    prior[start:end]: """    assert (actual['frames'],actual['initialized_runs'],actual['distinct_source_body_objects'],actual['distinct_body_pages']) == (82563,3,211,217)
    assert actual['observed_pages_including_repeats'] == 217 and actual['offline_only_source_body_objects'] == 167
    assert actual['all_actual_body_menu_andtransition_sheets_directly_viewed']
    assert actual['all_selected_current_pages_match_current_compiled_native_planes']
    assert actual['all_selected_two_page_turns_FE_andmenu_A_returns_observed']
    assert actual['complete_QA_host_nonspeech_setup_cleanup_andfollowing_tutorial_observed']
    delta=load(ROOT/'final_layout_delta_v1.json')
    assert (delta['final_layout_changes'],delta['initial_pages'],delta['final_pages'],delta['pages_reclaimed'])==(30,391,386,5)
    assert delta['no_prose_shortening_or_font_width_runtime_control_change']
    context=load(ROOT/'credited_context_rebuild_qualification_v1.json')
    assert context['actual_clean_current_andtarget_inverses_pass'] and context['positive_B115_target_byte_exact'] and len(context['rejected_cases'])==5
""",
    "rebuilt['source_editorial_objects'] == 305": "rebuilt['source_editorial_objects'] == 382",
    'all305_individual_five_gates_pass=True': 'all382_individual_five_gates_pass=True',
    'native_body_pages=302, source_editorial_body_objects=294, actual_source_body_objects=127':
        'native_body_pages=386, source_editorial_body_objects=378, actual_source_body_objects=211',
    'actual_body_pages=132, observed_pages_including_repeats=135, offline_only_source_body_objects=167':
        'actual_body_pages=217, observed_pages_including_repeats=217, offline_only_source_body_objects=167',
    'actual_caption_strings=7, offline_only_caption_strings=4': 'actual_caption_strings=4, offline_only_caption_strings=0',
    "len(names['records']) == 27": "len(names['records']) == 34",
    'all27_individual_five_gates_pass_in_scoped_context=True': 'all34_individual_five_gates_pass_in_scoped_context=True',
    'source294_release_plans.json': 'source378_release_plans.json',
    'source_editorial_objects=305,': 'source_editorial_objects=382,',
    'source_body_objects=294, physical_native_bodies=294': 'source_body_objects=378, physical_native_bodies=378',
    'records=305, revisions=205, retentions=100, complete_exchanges=19':
        'records=382, revisions=257, retentions=125, complete_exchanges=30',
    'physical_body_candidates=294, native_body_pages=302, typed_labels=11, scoped_names=27, name_strings=31':
        'physical_body_candidates=378, native_body_pages=386, typed_labels=4, scoped_names=34, name_strings=42',
    'source_styles=22, source_style_objects=3, source_FE_records=16, physical_FE_panels=16':
        'source_styles=14, source_style_objects=2, source_FE_records=3, physical_FE_panels=3',
    'source_bound_layout_changes=26, additional_phrase_wrap_fixes=17, scoped_FE_guard_reserves=2':
        'source_bound_layout_changes=30, additional_phrase_wrap_fixes=16, scoped_FE_guard_reserves=0',
    'observed_FE_blank_rows_repaired=1, pages_reclaimed=0, actual_source_body_objects=127':
        'observed_FE_blank_rows_repaired=0, pages_reclaimed=5, actual_source_body_objects=211',
    'actual_pages=132, observed_pages_including_repeats=135, actual_caption_strings=7':
        'actual_pages=217, observed_pages_including_repeats=217, actual_caption_strings=4',
    'offline_only_source_body_objects=167, offline_only_caption_strings=4, actual_frames=63843, actual_runs=3, actual_menus=3':
        'offline_only_source_body_objects=167, offline_only_caption_strings=0, actual_frames=82563, actual_runs=3, actual_menus=2',
    "Path(__file__)]}))":
        "ROOT/'final_layout_delta_v1.json',ROOT/'credited_context_rebuild_qualification_v1.json',Path('scripts/finalize_maria305_research_v1.py'),Path(__file__)]}))",
    'Sealed305 five-gate reviews and27 scoped names:205 revisions/100 retentions. Registration/once-only credit remain.':
        'Sealed382 five-gate reviews and34 scoped names:257 revisions/125 retentions. Registration/once-only credit remain.',
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-per-record-source-current-native-storage-andactual-gates', 'exec'), globals())
