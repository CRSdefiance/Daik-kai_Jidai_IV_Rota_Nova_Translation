"""Keep every individual five-gate guard for the exact349-source mixed scope."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

_prior=Path('scripts/finalize_maria305_research_v1.py').read_text(encoding='utf-8')
_start=_prior.index("    assert (actual['frames'], actual['initialized_runs']")
_end=_prior.index("    assert not any(actual[k]",_start)
source=checked_text(_prior,{
    'Maria_B176_B195_clean_20261110':'Maria_B275_B285_clean_20261110',
    'maria_B176_B195_':'maria_B275_B285_',
    'plan_v8/automatic_plans.json':'plan_v6/automatic_plans.json',
    'compiled_styles_v2/compiled_style_objects.json':'compiled_styles_v4/compiled_style_objects.json',
    "len(doc['records']) == 305 and Counter(r['decision'] for r in doc['records']) == {'revision':205, 'retention':100}":
        "len(doc['records']) == 349 and Counter(r['decision'] for r in doc['records']) == {'revision':184, 'retention':165}",
    "len(d['catalogue']['records']) == 294":"len(d['catalogue']['records']) == 341",
    "len(stored['records']) == 272 and len(stored['style_records']) == 22 and stored['typed_labels_checked'] == 11":
        "len(stored['records']) == 179 and len(stored['style_records']) == 162 and stored['typed_labels_checked'] == 8",
    '(302, 302, 1176)':'(347, 347, 1364)',
    '(148, 154, 170)':'(104, 243, 330)',
    '== (22, 24, 3)':'== (162, 216, 27)',
    "sum(len(r['rejected']) for r in d['styles']['compiler_negatives']) == 27":"sum(len(r['rejected']) for r in d['styles']['compiler_negatives']) == 243",
    "len(d['menus']['menus']) == 5":"len(d['menus']['menus']) == 3",
    _prior[_start:_end]:"""    assert (actual['frames'],actual['initialized_runs'],actual['distinct_source_body_objects'],actual['distinct_body_pages']) == (77043,3,191,193)
    assert actual['observed_pages_including_repeats'] == 193 and actual['offline_only_source_body_objects'] == 150
    assert actual['all_actual_body_menu_andtransition_sheets_directly_viewed']
    assert actual['all_selected_current_pages_match_current_compiled_native_planes']
    assert actual['both_two_page_turns_andfollowing_calls_observed']
    assert actual['former_actor_governor_priest_headers_andFI_macros_observed']
    assert actual['wolf_andscorpion_roles215_218_andall_three_menu_returns_observed']
    assert actual['all_seven_FE_panels_andfollowing_A_returns_observed']
    assert actual['complete_QA_host_nonspeech_setup_cleanup_andreturn_to_sailing_observed']
""",
    "rebuilt['source_editorial_objects'] == 305":"rebuilt['source_editorial_objects'] == 349",
    'all305_individual_five_gates_pass=True':'all349_individual_five_gates_pass=True',
    'native_body_pages=302, source_editorial_body_objects=294, actual_source_body_objects=127':'native_body_pages=347, source_editorial_body_objects=341, actual_source_body_objects=191',
    'actual_body_pages=132, observed_pages_including_repeats=135, offline_only_source_body_objects=167':'actual_body_pages=193, observed_pages_including_repeats=193, offline_only_source_body_objects=150',
    'actual_caption_strings=7, offline_only_caption_strings=4':'actual_caption_strings=8, offline_only_caption_strings=0',
    "len(names['records']) == 27":"len(names['records']) == 19",
    'all27_individual_five_gates_pass_in_scoped_context=True':'all19_individual_five_gates_pass_in_scoped_context=True',
    'source294_release_plans.json':'source341_release_plans.json',
    'source_editorial_objects=305,':'source_editorial_objects=349,',
    'source_body_objects=294, physical_native_bodies=294':'source_body_objects=341, physical_native_bodies=341',
    'records=305, revisions=205, retentions=100, complete_exchanges=19':'records=349, revisions=184, retentions=165, complete_exchanges=11',
    'physical_body_candidates=294, native_body_pages=302, typed_labels=11, scoped_names=27, name_strings=31':'physical_body_candidates=341, native_body_pages=347, typed_labels=8, scoped_names=19, name_strings=21',
    'source_styles=22, source_style_objects=3, source_FE_records=16, physical_FE_panels=16':'source_styles=162, source_style_objects=27, source_FE_records=7, physical_FE_panels=7',
    'source_bound_layout_changes=26, additional_phrase_wrap_fixes=17, scoped_FE_guard_reserves=2':'source_bound_layout_changes=10, additional_phrase_wrap_fixes=0, scoped_FE_guard_reserves=0',
    'observed_FE_blank_rows_repaired=1, pages_reclaimed=0, actual_source_body_objects=127':'observed_FE_blank_rows_repaired=0, pages_reclaimed=3, actual_source_body_objects=191',
    'actual_pages=132, observed_pages_including_repeats=135, actual_caption_strings=7':'actual_pages=193, observed_pages_including_repeats=193, actual_caption_strings=8',
    'offline_only_source_body_objects=167, offline_only_caption_strings=4, actual_frames=63843, actual_runs=3, actual_menus=3':'offline_only_source_body_objects=150, offline_only_caption_strings=0, actual_frames=77043, actual_runs=3, actual_menus=3',
    "Path(__file__)]}))":"Path('scripts/finalize_maria305_research_v1.py'), Path(__file__)]}))",
    'Sealed305 five-gate reviews and27 scoped names:205 revisions/100 retentions. Registration/once-only credit remain.':'Sealed349 five-gate reviews and19 scoped names:184 revisions/165 retentions. Registration/once-only credit remain.',
})

if __name__=='__main__':exec(compile(source,__file__+'::complete-individual-source-current-native-stored-andactual-five-gate-contract','exec'),globals())
