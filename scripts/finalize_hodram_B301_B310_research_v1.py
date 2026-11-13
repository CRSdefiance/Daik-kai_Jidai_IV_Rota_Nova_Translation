"""Seal all individual gates only with the resolved QA exit and exact current proofs."""
from pathlib import Path
from scripts import finalize_hodram_B281_B300_research_v1 as previous
from scripts.approve_hodram_B301_B310_display_v6 import ROOT,OUT as INPUT,VIEW
from scripts.source_locked_derivation_v5118 import checked_text

REBUILT=ROOT/'reconstruction_v1/reconstruction.json'
STORED=ROOT/'stored_v1/stored_native_verification.json'
LOOKUP=ROOT/'stored_catalogue_all_v1/all225_stored_effective_body_bindings.json'
LOADERS=ROOT/'loaders_v1/verification.json'
NATIVE=INPUT/'native_pages.json';PLAN=INPUT/'compiled_plans.json';MANUSCRIPT=INPUT/'storage_manuscript.json'
LIVE=ROOT/'actual_pixels_terminal_v4/focused_actual_pixels.json';MENU=ROOT/'actual_menus_terminal_v4/menu_actual_pixels.json'
NAMES=ROOT/'name_plane_inputs_v1/names.json';NAME_PLANES=ROOT/'name_planes_v1/native_name_planes.json'
FIXTURE=ROOT/'focused_fixtures_terminal_v4/hodram_desert_temple_wolf_and_offer_fixture.json'
EXIT=ROOT/'fixture_exit_resolution_v4.json'
OUT=ROOT/'research_final_v1';FINAL=Path('translations/hodram_B301_B310_final_review_v1.json')
FINAL_NAMES=Path('translations/hodram_B301_B310_scoped_names_final_v1.json');READY=OUT/'research_completion.json'

source=checked_text(previous.source,{
    "VIEW,FIXTURE,\n        ROOT/'actual_menus_v1/model_qualification_reuse.json'":
        "VIEW,FIXTURE,EXIT,\n        ROOT/'actual_menus_terminal_v4/model_qualification_reuse.json'",
    'visual,fixture,model=map(load,paths)':'visual,fixture,exit_proof,model=map(load,paths)',
    "    assert rebuilt['manuscript_sha256']":
        "    assert exit_proof['all_copied_commands_andbindings_exact'] and exit_proof['all97_display_pages_qualified']\n    assert exit_proof['following_native_dialogue_observed'] and exit_proof['no_production_scene_controls_changed']\n    assert exit_proof['prior_failed_runs_preserved'] and exit_proof['bounded_QA_terminal_resolution_not_full_event_activation']\n    assert rebuilt['manuscript_sha256']",
    'all373_ordinary_and_style_bodies_checked':'all225_ordinary_and_style_bodies_checked',
    '(374,108,266,1415)':'(228,35,193,190)',
    '(325,40,610)':'(325,20,630)',
    "len(rebuilt['changed_blocks'])==20 and rebuilt['unchanged_control_only_blocks']==[] and rebuilt['reviewed_blocks']==list(range(281,301))":
        "len(rebuilt['changed_blocks'])==10 and rebuilt['unchanged_control_only_blocks']==[] and rebuilt['reviewed_blocks']==list(range(301,311))",
    "rebuilt['command_count']==934 and rebuilt['relative_sites']==283":"rebuilt['command_count']==264 and rebuilt['relative_sites']==38",
    'all29_new_native_pages_directly_viewed':'all21_new_native_pages_directly_viewed',
    "nameplanes['scoped_actors']==len(names['records'])==18 and nameplanes['distinct_strings']==17":
        "nameplanes['scoped_actors']==len(names['records'])==8 and nameplanes['distinct_strings']==8",
    '(38561,134,135)':'(29201,96,97)',
    "live['complete_body_planes']>=135 and live['complete_header_planes']>=122":
        "live['complete_body_planes']>=97 and live['complete_header_planes']>=89",
    "len(live['review_sheets'])==23 and len(live['observed_source_selectors'])==15":
        "len(live['review_sheets'])==17 and len(live['observed_source_selectors'])==14",
    '{(290,876,(0,)),(290,1876,(0,)),(291,1114,(0,)),(294,820,(0,)),(300,560,(0,))}':
        '{(302,1226,(0,)),(302,2272,(0,)),(304,576,(0,)),(309,738,(0,))}',
    "ROOT/'actual_body_sheets_v1/receipt.json'":"ROOT/'actual_body_sheets_terminal_v4/receipt.json'",
    "compact['actual_dialogue_pages']==135":"compact['actual_dialogue_pages']==97",
    'assert len(sheets)==13':'assert len(sheets)==10',
    'len(bodies)==373 and len(captions)==11':'len(bodies)==225 and len(captions)==9',
    'len(seen)==134':'len(seen)==96',
    "assert len({r['id'] for r in doc['records'] if r.get('source_selector')==254})==16 and len({r['id'] for r in doc['records'] if r.get('source_selector')==254}&seen)==12":
        "assert len({r['id'] for r in doc['records'] if r.get('source_selector')==254})==8 and len({r['id'] for r in doc['records'] if r.get('source_selector')==254}&seen)==8",
    "{'DK4_MES_B282_R0019','DK4_MES_B287_R0125','DK4_MES_B290_R0148','DK4_MES_B283_R0100','DK4_MES_B287_R0065','DK4_MES_B290_R0092','DK4_MES_B290_R0179','DK4_MES_B296_R0033','DK4_MES_B299_R0278'}":
        "{'DK4_MES_B307_R0034','DK4_MES_B307_R0042','DK4_MES_B307_R0055','DK4_MES_B309_R0174','DK4_MES_B309_R0294','DK4_MES_B310_R0016'}",
    "for r in fixture['selected_records'])==7":"for r in fixture['selected_records'])==23",
    'total_frames=38561':'total_frames=29201',
    'source_speech_variants_observed=134':'source_speech_variants_observed=96',
    'native_body_pages_observed=135':'native_body_pages_observed=97',
    'offline_only_speech_variants=239':'offline_only_speech_variants=129',
    'twelve_of16_FE_panels_FI_FA_seven_voice_objects_royal_pagination_andcorrected_injury_rows_observed':
        'all8_FE_FI_23_voice_objects_Mihwa_pagination_andcorrected_departure_rows_observed',
    'body_pages=374':'body_pages=228',
    'observed_pages=135':'observed_pages=97',
    'actual_sheets_directly_viewed=13':'actual_sheets_directly_viewed=10',
    'visual_layout_revisions=28,visual_candidate_retentions=2':'visual_layout_revisions=18,visual_candidate_retentions=1',
    "{'revision':181,'retention':203}":"{'revision':127,'retention':107}",
    'Hodram B281–B300 exchanges':'Hodram B301–B310 exchanges',
    'records=384,revisions=181,retentions=203':'records=234,revisions=127,retentions=107',
    'typed_labels=11,scoped_names=18,actual_source_variants=134,actual_pages=135':
        'typed_labels=9,scoped_names=8,actual_source_variants=96,actual_pages=97',
    'actual_distinct_menu_behaviors=5,offline_only_source_variants=239':
        'actual_distinct_menu_behaviors=4,offline_only_source_variants=129',
    'Sealed 384 five-gate reviews, 374 stored pages and 135 observed pages.':
        'Sealed234 five-gate reviews,228 stored pages and97 observed pages; bounded QA terminal resolution required.',
})
env={**previous.env,**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-complete-individual-gates-with-qualified-QA-exit','exec'),env)

if __name__=='__main__':
    from scripts.audit_story_glyph_consistency import load,save
    from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
    model=ROOT/'actual_menus_terminal_v4/model_qualification_reuse.json';assert not model.exists()
    prior=Path('work/Hodram_B231_B250_clean_20261107/actual_menus_band_v1/model_qualification.json')
    qualified=load(prior)
    assert digest(prior)=='1af1a246e88a9ba61a5e0dccc11987d5daaf2878cf0c7baf7d0d26edf33517c8'
    assert qualified['all6_pixel_andcursor_mutations_rejected'] and qualified['no_ROM_orcapture_mutation']
    for p,h in qualified['evidence'].items():assert digest(p)==h
    assert load(MENU)['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
    assert load(EXIT)['following_native_dialogue_observed']
    save(model,dict(all6_pixel_andcursor_mutations_rejected=True,exact_checker_andnegative_cases_reused=True,
        prior=str(prior),prior_sha256=digest(prior),cases=qualified['cases'],no_ROM_orcapture_mutation=True,
        all_current_geometry_andcaption_pixels_freshly_checked=True,no_new_negative_case_execution=True,new_credit=0))
    env['main']()
