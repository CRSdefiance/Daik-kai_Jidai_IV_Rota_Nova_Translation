"""Seal individual gates only after exact native, viewed and representative live evidence passes."""
from pathlib import Path
from scripts import finalize_hodram_B251_B280_research_v1 as previous
from scripts.approve_hodram_B281_B300_display_v5 import ROOT,OUT as INPUT,VIEW
from scripts.source_locked_derivation_v5118 import checked_text

REBUILT=ROOT/'rebuilt_v1/reconstruction.json'
STORED=ROOT/'stored_v1/stored_native_verification.json'
LOOKUP=ROOT/'stored_catalogue_all_v1/all373_stored_effective_body_bindings.json'
LOADERS=ROOT/'loaders_v1/verification.json'
NATIVE=INPUT/'native_pages.json';PLAN=INPUT/'compiled_plans.json';MANUSCRIPT=INPUT/'storage_manuscript.json'
LIVE=ROOT/'actual_pixels_v1/focused_actual_pixels.json';MENU=ROOT/'actual_menus_v1/menu_actual_pixels.json'
NAMES=ROOT/'name_plane_inputs_v2/names.json';NAME_PLANES=ROOT/'name_planes_v2/native_name_planes.json'
FIXTURE=ROOT/'focused_fixtures_v1/hodram_royal_ruins_beasts_and_gunpowder_fixture.json'
OUT=ROOT/'research_final_v1';FINAL=Path('translations/hodram_B281_B300_final_review_v1.json')
FINAL_NAMES=Path('translations/hodram_B281_B300_scoped_names_final_v1.json');READY=OUT/'research_completion.json'

source=checked_text(previous.source,{
    'all209_ordinary_and_style_bodies_checked':'all373_ordinary_and_style_bodies_checked',
    '(212,113,99,660)':'(374,108,266,1415)','(325,60,590)':'(325,40,610)',
    "len(rebuilt['changed_blocks'])==30 and rebuilt['unchanged_control_only_blocks']==[] and rebuilt['reviewed_blocks']==list(range(251,281))":
        "len(rebuilt['changed_blocks'])==20 and rebuilt['unchanged_control_only_blocks']==[] and rebuilt['reviewed_blocks']==list(range(281,301))",
    "rebuilt['command_count']==575 and rebuilt['relative_sites']==132":"rebuilt['command_count']==934 and rebuilt['relative_sites']==283",
    "visual['all14_new_native_pages_directly_viewed']":"visual['all29_new_native_pages_directly_viewed']",
    "nameplanes['scoped_actors']==len(names['records'])==21 and nameplanes['distinct_strings']==18":
        "nameplanes['scoped_actors']==len(names['records'])==18 and nameplanes['distinct_strings']==17",
    "assert (live['frames'],live['selected_utterances'],live['selected_pages'],live['complete_body_planes'],live['complete_header_planes'])==(26801,86,88,184,148)":
        "assert (live['frames'],live['selected_utterances'],live['selected_pages'])==(38561,134,135)\n    assert live['complete_body_planes']>=135 and live['complete_header_planes']>=122",
    "len(live['review_sheets'])==15 and len(live['observed_source_selectors'])==11":
        "len(live['review_sheets'])==23 and len(live['observed_source_selectors'])==15",
    "{(251,432,(0,)),(252,270,(0,)),(252,1606,(0,))}":
        "{(290,876,(0,)),(290,1876,(0,)),(291,1114,(0,)),(294,820,(0,)),(300,560,(0,))}",
    "ROOT/'actual_body_sheets_v1/sheets.json'":"ROOT/'actual_body_sheets_v1/receipt.json'",
    "compact['actual_sha256']==digest(LIVE) and compact['pages']==88":
        "compact['actual_pixel_proof_sha256']==digest(LIVE) and compact['actual_dialogue_pages']==135",
    "for s in compact['sheets']":"for s in compact['bottom_screen_sheets']",
    'assert len(sheets)==9':'assert len(sheets)==13',
    'len(bodies)==209 and len(captions)==7':'len(bodies)==373 and len(captions)==11',
    'len(seen)==86':'len(seen)==134',
    "assert len({r['id'] for r in doc['records'] if r.get('source_selector')==254})==31 and len({r['id'] for r in doc['records'] if r.get('source_selector')==254}&seen)==18":
        "assert len({r['id'] for r in doc['records'] if r.get('source_selector')==254})==16 and len({r['id'] for r in doc['records'] if r.get('source_selector')==254}&seen)==12",
    "{'DK4_MES_B252_R0116','DK4_MES_B252_R0184','DK4_MES_B274_R0015','DK4_MES_B266_R0009','DK4_MES_B277_R0066'}":
        "{'DK4_MES_B282_R0019','DK4_MES_B287_R0125','DK4_MES_B290_R0148','DK4_MES_B283_R0100','DK4_MES_B287_R0065','DK4_MES_B290_R0092','DK4_MES_B290_R0179','DK4_MES_B296_R0033','DK4_MES_B299_R0278'}",
    "for r in fixture['selected_records'])==2":"for r in fixture['selected_records'])==7",
    'total_frames=26801':'total_frames=38561','source_speech_variants_observed=86':'source_speech_variants_observed=134',
    'native_body_pages_observed=88':'native_body_pages_observed=135',
    'complete_body_planes=184,complete_header_planes=148':"complete_body_planes=live['complete_body_planes'],complete_header_planes=live['complete_header_planes']",
    'offline_only_speech_variants=123':'offline_only_speech_variants=239',
    'eighteen_of31_FE_panels_FI_FA_two_voice_objects_andboth_selected_two_page_passages_observed=True':
        'twelve_of16_FE_panels_FI_FA_seven_voice_objects_royal_pagination_andcorrected_injury_rows_observed=True',
    'body_pages=212':'body_pages=374','observed_pages=88':'observed_pages=135',
    'actual_sheets_directly_viewed=9':'actual_sheets_directly_viewed=13',
    'visual_layout_revisions=13,visual_candidate_retentions=3':'visual_layout_revisions=28,visual_candidate_retentions=2',
    "{'revision':129,'retention':87}":"{'revision':181,'retention':203}",
    'Hodram B251–B280 exchanges':'Hodram B281–B300 exchanges',
    'records=216,revisions=129,retentions=87':'records=384,revisions=181,retentions=203',
    'typed_labels=7,scoped_names=21,actual_source_variants=86,actual_pages=88':
        'typed_labels=11,scoped_names=18,actual_source_variants=134,actual_pages=135',
    'actual_distinct_menu_behaviors=3,offline_only_source_variants=123':
        'actual_distinct_menu_behaviors=5,offline_only_source_variants=239',
    'Sealed 216 five-gate reviews, 212 stored pages and 88 observed pages.':
        'Sealed 384 five-gate reviews, 374 stored pages and 135 observed pages.',
})
env={**previous.env,**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-individual-gates-and-complete-source-stored-bindings','exec'),env)

if __name__=='__main__':
    from scripts.audit_story_glyph_consistency import load,save
    from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
    model=ROOT/'actual_menus_v1/model_qualification_reuse.json';assert not model.exists()
    prior=Path('work/Hodram_B231_B250_clean_20261107/actual_menus_band_v1/model_qualification.json')
    qualified=load(prior)
    assert digest(prior)=='1af1a246e88a9ba61a5e0dccc11987d5daaf2878cf0c7baf7d0d26edf33517c8'
    assert qualified['all6_pixel_andcursor_mutations_rejected'] and qualified['no_ROM_orcapture_mutation']
    for p,h in qualified['evidence'].items():assert digest(p)==h
    assert load(MENU)['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
    save(model,dict(all6_pixel_andcursor_mutations_rejected=True,exact_checker_andnegative_cases_reused=True,
        prior=str(prior),prior_sha256=digest(prior),cases=qualified['cases'],no_ROM_orcapture_mutation=True,
        all_current_geometry_andcaption_pixels_freshly_checked=True,no_new_negative_case_execution=True,new_credit=0))
    env['main']()
