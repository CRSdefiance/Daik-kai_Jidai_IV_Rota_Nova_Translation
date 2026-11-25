"""Keep the complete per-record five-gate contract for the measured Maria359 scope."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

_prior=Path('scripts/finalize_maria305_research_v1.py').read_text(encoding='utf-8')
_actual_start=_prior.index("    assert (actual['frames'], actual['initialized_runs']")
_actual_end=_prior.index("    assert not any(actual[k]",_actual_start)
source=checked_text(_prior,{
    'Maria_B176_B195_clean_20261110':'Maria_B253_B274_clean_20261110',
    'maria_B176_B195_':'maria_B253_B274_',
    'formatting_v1/formatting_input.json':'formatting_v1/formatting_input_v2.json',
    'contextual_review_v1.json':'contextual_review_v2.json',
    'plan_v8/automatic_plans.json':'plan_v7/automatic_plans.json',
    'final_native_v1.json':'final_native_v2.json',
    "len(doc['records']) == 305 and Counter(r['decision'] for r in doc['records']) == {'revision':205, 'retention':100}":
        "len(doc['records']) == 359 and Counter(r['decision'] for r in doc['records']) == {'revision':219, 'retention':140}",
    "len(d['catalogue']['records']) == 294":"len(d['catalogue']['records']) == 349",
    "len(stored['records']) == 272 and len(stored['style_records']) == 22 and stored['typed_labels_checked'] == 11":
        "len(stored['records']) == 218 and len(stored['style_records']) == 131 and stored['typed_labels_checked'] == 10",
    '(302, 302, 1176)':'(350, 350, 1396)',
    '(148, 154, 170)':'(104, 246, 1015)',
    '== (22, 24, 3)':'== (131, 144, 18)',
    "sum(len(r['rejected']) for r in d['styles']['compiler_negatives']) == 27":"sum(len(r['rejected']) for r in d['styles']['compiler_negatives']) == 162",
    _prior[_actual_start:_actual_end]:"""    assert (actual['frames'],actual['initialized_runs'],actual['distinct_source_body_objects'],actual['distinct_body_pages']) == (70803,3,164,165)
    assert actual['observed_pages_including_repeats'] == 165 and actual['offline_only_source_body_objects'] == 185
    assert actual['all_actual_body_menu_andtransition_sheets_directly_viewed']
    assert actual['all_selected_current_pages_match_current_compiled_native_planes']
    assert actual['London_two_page_turn_andfollowing_call_observed'] and actual['cure_complete_on_one_page_observed']
    assert actual['actor18_B271R223_header_andall_five_menu_returns_observed']
    assert actual['complete_QA_host_nonspeech_setup_cleanup_andreturn_to_sailing_observed']
""",
    "rebuilt['source_editorial_objects'] == 305":"rebuilt['source_editorial_objects'] == 359",
    'all305_individual_five_gates_pass=True':'all359_individual_five_gates_pass=True',
    'native_body_pages=302, source_editorial_body_objects=294, actual_source_body_objects=127':'native_body_pages=350, source_editorial_body_objects=349, actual_source_body_objects=164',
    'actual_body_pages=132, observed_pages_including_repeats=135, offline_only_source_body_objects=167':'actual_body_pages=165, observed_pages_including_repeats=165, offline_only_source_body_objects=185',
    'actual_caption_strings=7, offline_only_caption_strings=4':'actual_caption_strings=10, offline_only_caption_strings=0',
    "len(names['records']) == 27":"len(names['records']) == 18",
    'all27_individual_five_gates_pass_in_scoped_context=True':'all18_individual_five_gates_pass_in_scoped_context=True',
    'source294_release_plans.json':'source349_release_plans.json',
    'source_editorial_objects=305,':'source_editorial_objects=359,',
    'source_body_objects=294, physical_native_bodies=294':'source_body_objects=349, physical_native_bodies=349',
    'records=305, revisions=205, retentions=100, complete_exchanges=19':'records=359, revisions=219, retentions=140, complete_exchanges=22',
    'physical_body_candidates=294, native_body_pages=302, typed_labels=11, scoped_names=27, name_strings=31':'physical_body_candidates=349, native_body_pages=350, typed_labels=10, scoped_names=18, name_strings=21',
    'source_styles=22, source_style_objects=3, source_FE_records=16, physical_FE_panels=16':'source_styles=131, source_style_objects=18, source_FE_records=17, physical_FE_panels=17',
    'source_bound_layout_changes=26, additional_phrase_wrap_fixes=17, scoped_FE_guard_reserves=2':'source_bound_layout_changes=35, additional_phrase_wrap_fixes=35, scoped_FE_guard_reserves=0',
    'observed_FE_blank_rows_repaired=1, pages_reclaimed=0, actual_source_body_objects=127':'observed_FE_blank_rows_repaired=0, pages_reclaimed=1, actual_source_body_objects=164',
    'actual_pages=132, observed_pages_including_repeats=135, actual_caption_strings=7':'actual_pages=165, observed_pages_including_repeats=165, actual_caption_strings=10',
    'offline_only_source_body_objects=167, offline_only_caption_strings=4, actual_frames=63843, actual_runs=3, actual_menus=3':'offline_only_source_body_objects=185, offline_only_caption_strings=0, actual_frames=70803, actual_runs=3, actual_menus=5',
    "Path(__file__)]}))":"Path('scripts/finalize_maria305_research_v1.py'), Path(__file__)]}))",
    'Sealed305 five-gate reviews and27 scoped names:205 revisions/100 retentions. Registration/once-only credit remain.':'Sealed359 five-gate reviews and18 scoped names:219 revisions/140 retentions. Registration/once-only credit remain.',
})

if __name__=='__main__':exec(compile(source,__file__+'::same-per-record-source-current-native-stored-actual-five-gate-contract','exec'),globals())
