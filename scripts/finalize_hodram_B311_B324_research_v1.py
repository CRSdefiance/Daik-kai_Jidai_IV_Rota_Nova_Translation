"""Seal400 individual reviews with exact stored proofs and two bounded, directly viewed runs."""
from pathlib import Path
from scripts import finalize_hodram_B301_B310_research_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

ROOT = Path('work/Hodram_B311_B324_clean_20261107')
INPUT = ROOT/'storage_inputs_v1'
VIEW = ROOT/'offline_visual_approval_v4.json'
REBUILT = ROOT/'reconstruction_v1/reconstruction.json'
STORED = ROOT/'stored_v1/stored_native_verification.json'
LOOKUP = ROOT/'stored_catalogue_all_v1/all387_stored_effective_body_bindings.json'
LOADERS = ROOT/'loaders_v1/verification.json'
NATIVE = INPUT/'native_pages.json'
PLAN = INPUT/'compiled_plans.json'
MANUSCRIPT = INPUT/'storage_manuscript.json'
LIVE = ROOT/'bounded_combined_v1/focused_actual_pixels.json'
MENU = ROOT/'bounded_combined_v1/menu_actual_pixels.json'
NAMES = ROOT/'name_plane_inputs_v1/names.json'
NAME_PLANES = ROOT/'name_planes_v1/native_name_planes.json'
FIXTURE = ROOT/'bounded_combined_v1/fixture_set.json'
EXIT = ROOT/'bounded_QA_return_proof_v1.json'
OUT = ROOT/'research_final_v1'
FINAL = Path('translations/hodram_B311_B324_final_review_v1.json')
FINAL_NAMES = Path('translations/hodram_B311_B324_scoped_names_final_v1.json')
READY = OUT/'research_completion.json'

source = checked_text(previous.source, {
    "exit_proof['qualified_frames']==34162": "exit_proof['qualified_frames']==57202",
    'all97_display_pages_qualified': 'all191_display_pages_qualified',
    'all225_ordinary_and_style_bodies_checked': 'all387_ordinary_and_style_bodies_checked',
    '(228,35,193,190)': '(389,75,314,495)',
    '(325,20,630)': '(325,28,622)',
    "len(rebuilt['changed_blocks'])==10 and rebuilt['unchanged_control_only_blocks']==[] and rebuilt['reviewed_blocks']==list(range(301,311))":
        "len(rebuilt['changed_blocks'])==14 and rebuilt['unchanged_control_only_blocks']==[] and rebuilt['reviewed_blocks']==list(range(311,325))",
    "rebuilt['command_count']==264 and rebuilt['relative_sites']==38":
        "rebuilt['command_count']==494 and rebuilt['relative_sites']==99",
    "visual['final_speech_pages_visually_approved'] and visual['all21_new_native_pages_directly_viewed'] and visual['all_name_andmenu_sheets_directly_viewed']":
        "visual['final_all389_pages_directly_viewed_or_exact_reused'] and visual['all39_trial_pages_directly_viewed'] and visual['final_two_new_pages_directly_viewed'] and visual['eleven_scoped_name_retentions_ten_native_strings_viewed'] and visual['thirteen_captions_six_native_menus_viewed']",
    "nameplanes['scoped_actors']==len(names['records'])==8 and nameplanes['distinct_strings']==8":
        "nameplanes['scoped_actors']==len(names['records'])==11 and nameplanes['distinct_strings']==10",
    '(34162,96,97)': '(57202,189,191)',
    "live['complete_body_planes']>=97 and live['complete_header_planes']>=89":
        "live['complete_body_planes']==398 and live['complete_header_planes']==370",
    "len(live['review_sheets'])==17 and len(live['observed_source_selectors'])==14":
        "len(live['review_sheets'])==32 and len(live['observed_source_selectors'])==17",
    '{(302,1226,(0,)),(302,2272,(0,)),(304,576,(0,)),(309,738,(0,))}':
        '{(311,1086,(0,)),(311,1306,(0,)),(313,782,(0,)),(316,674,(0,)),(316,934,(0,)),(317,764,(0,))}',
    "compact['actual_dialogue_pages']==97": "compact['actual_dialogue_pages']==191",
    'assert len(sheets)==10': 'assert len(sheets)==17',
    'len(bodies)==225 and len(captions)==9': 'len(bodies)==387 and len(captions)==13',
    'len(seen)==96': 'len(seen)==189',
    "assert len({r['id'] for r in doc['records'] if r.get('source_selector')==254})==8 and len({r['id'] for r in doc['records'] if r.get('source_selector')==254}&seen)==8":
        "assert len({r['id'] for r in doc['records'] if r.get('source_selector')==254})==14 and len({r['id'] for r in doc['records'] if r.get('source_selector')==254}&seen)==14",
    "{'DK4_MES_B307_R0034','DK4_MES_B307_R0042','DK4_MES_B307_R0055','DK4_MES_B309_R0174','DK4_MES_B309_R0294','DK4_MES_B310_R0016'}":
        "{'DK4_MES_B314_R0030','DK4_MES_B314_R0043','DK4_MES_B313_R0228','DK4_MES_B317_R0127','DK4_MES_B318_R0109','DK4_MES_B318_R0114','DK4_MES_B322_R0071','DK4_MES_B322_R0076','DK4_MES_B324_R0013','DK4_MES_B324_R0109','DK4_MES_B324_R0148'}",
    "for r in fixture['selected_records'])==23": "for r in fixture['selected_records'])==38",
    'total_frames=34162,initialized_fixture_runs=2': 'total_frames=57202,initialized_fixture_runs=2',
    'source_speech_variants_observed=96': 'source_speech_variants_observed=189',
    'native_body_pages_observed=97': 'native_body_pages_observed=191',
    'offline_only_speech_variants=129': 'offline_only_speech_variants=198',
    'all8_FE_FI_23_voice_objects_Mihwa_pagination_andcorrected_departure_rows_observed':
        'all14_FE_FI_38_voice_objects_Rafael0_two_page_passages_andreturns_observed',
    'body_pages=228': 'body_pages=389',
    'observed_pages=97': 'observed_pages=191',
    'actual_sheets_directly_viewed=10': 'actual_sheets_directly_viewed=17',
    'visual_layout_revisions=18,visual_candidate_retentions=1': 'visual_layout_revisions=27,visual_candidate_retentions=12',
    "{'revision':127,'retention':107}": "{'revision':175,'retention':225}",
    'Hodram B301–B310 exchanges': 'Hodram B311–B324 exchanges',
    'records=234,revisions=127,retentions=107': 'records=400,revisions=175,retentions=225',
    'typed_labels=9,scoped_names=8,actual_source_variants=96,actual_pages=97':
        'typed_labels=13,scoped_names=11,actual_source_variants=189,actual_pages=191',
    'actual_distinct_menu_behaviors=4,offline_only_source_variants=129':
        'actual_distinct_menu_behaviors=6,offline_only_source_variants=198',
    "    evidence={str(p):digest(p) for p in (*paths,Path(__file__))}":
        "    resolution=ROOT/'source_occurrence_resolution_v2.json'\n    resolved=load(resolution)\n    assert resolved['duplicate_command_source_key_regression_pass'] and resolved['original_fixtures_ROMs_terminals_captures_andpixel_receipts_unchanged']\n    for p,h in resolved['evidence'].items():assert digest(p)==h\n    assert exit_proof['evidence'][str(resolution)]==digest(resolution)\n    assert exit_proof['all14_production_blocks_inside_conservative_bound']\n    evidence={str(p):digest(p) for p in (*paths,resolution,ROOT/'scoped_names_visual_approval_v1.json',Path(__file__))}",
    'Sealed234 five-gate reviews,228 stored pages and97 observed pages; bounded QA terminal resolution required. Registered integration remains.':
        'Sealed400 five-gate reviews,389 stored pages and191 observed pages; both bounded returns pass. Registered integration remains.',
})
env = {**previous.env, **globals(), '__file__':__file__}
exec(compile(source,__file__+'::same-individual-gates-storage-pixel-visual-and-source-provenance-guards-new-scope','exec'),env)

if __name__ == '__main__':
    from scripts.audit_story_glyph_consistency import load, save
    from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
    model = ROOT/'bounded_combined_v1/model_qualification_reuse.json'
    assert not model.exists()
    prior = Path('work/Hodram_B231_B250_clean_20261107/actual_menus_band_v1/model_qualification.json')
    qualified = load(prior)
    assert digest(prior) == '1af1a246e88a9ba61a5e0dccc11987d5daaf2878cf0c7baf7d0d26edf33517c8'
    assert qualified['all6_pixel_andcursor_mutations_rejected'] and qualified['no_ROM_orcapture_mutation']
    for p,h in qualified['evidence'].items():
        assert digest(p) == h
    assert load(MENU)['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
    assert load(EXIT)['following_native_dialogue_observed']
    save(model,dict(all6_pixel_andcursor_mutations_rejected=True,exact_checker_andnegative_cases_reused=True,
        prior=str(prior),prior_sha256=digest(prior),cases=qualified['cases'],no_ROM_orcapture_mutation=True,
        all_current_geometry_andcaption_pixels_freshly_checked=True,no_new_negative_case_execution=True,new_credit=0))
    env['main']()
