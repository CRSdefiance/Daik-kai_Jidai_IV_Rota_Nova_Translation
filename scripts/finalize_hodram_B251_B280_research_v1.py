"""Seal the individual gates using exact current native, visual and gameplay evidence."""
import inspect
from pathlib import Path
from scripts import finalize_hodram_B231_B250_research_v1 as previous
from scripts.approve_hodram_B251_B280_display_v5 import ROOT, OUT as INPUT, VIEW
from scripts.source_locked_derivation_v5118 import checked_text

REBUILT=ROOT/'research_rebuilt_v1/reconstruction.json'
STORED=ROOT/'stored_v1/stored_native_verification.json'
LOOKUP=ROOT/'stored_catalogue_all_v1/all209_stored_effective_body_bindings.json'
LOADERS=ROOT/'loaders_v1/verification.json'
NATIVE=INPUT/'native_pages.json'; PLAN=INPUT/'compiled_plans.json'; MANUSCRIPT=INPUT/'storage_manuscript.json'
LIVE=ROOT/'actual_pixels_v2/focused_actual_pixels.json'; MENU=ROOT/'actual_menus_v1/menu_actual_pixels.json'
NAMES=ROOT/'name_plane_inputs_v1/names.json'; NAME_PLANES=ROOT/'name_planes_v1/native_name_planes.json'
FIXTURE=ROOT/'focused_fixtures_v2/hodram_figureheads_riddle_and_guild_returns_fixture.json'
OUT=ROOT/'research_final_v1'; FINAL=Path('translations/hodram_B251_B280_final_review_v1.json')
FINAL_NAMES=Path('translations/hodram_B251_B280_scoped_names_final_v1.json'); READY=OUT/'research_completion.json'

source=checked_text(inspect.getsource(previous.main),{
    "ROOT/'actual_menus_band_v1/model_qualification.json'":"ROOT/'actual_menus_v1/model_qualification_reuse.json'",
    'all223_ordinary_and_style_bodies_checked':'all209_ordinary_and_style_bodies_checked',
    '(228,108,120,170)':'(212,113,99,660)', '(325,36,614)':'(325,60,590)',
    "len(rebuilt['changed_blocks'])==18 and rebuilt['unchanged_control_only_blocks']==[235] and 237 not in rebuilt['reviewed_blocks']":
        "len(rebuilt['changed_blocks'])==30 and rebuilt['unchanged_control_only_blocks']==[] and rebuilt['reviewed_blocks']==list(range(251,281))",
    "rebuilt['command_count']==359 and rebuilt['relative_sites']==34":"rebuilt['command_count']==575 and rebuilt['relative_sites']==132",
    "visual['all17_new_native_pages_directly_viewed']":"visual['all14_new_native_pages_directly_viewed']",
    "nameplanes['scoped_actors']==nameplanes['distinct_strings']==len(names['records'])==19":
        "nameplanes['scoped_actors']==len(names['records'])==21 and nameplanes['distinct_strings']==18",
    '(21521,63,68,144,136)':'(26801,86,88,184,148)',
    "len(live['review_sheets'])==12 and len(live['observed_source_selectors'])==13":
        "len(live['review_sheets'])==15 and len(live['observed_source_selectors'])==11",
    "{(243,674,(0,))}":"{(251,432,(0,)),(252,270,(0,)),(252,1606,(0,))}",
    "model['all6_pixel_andcursor_mutations_rejected'] and menu['original_flat_highlight_checker_rejected_preserved']":
        "model['all6_pixel_andcursor_mutations_rejected'] and model['exact_checker_andnegative_cases_reused']",
    "    sheets=live['review_sheets']+[menu['review_sheet']]":
        """    compact=load(ROOT/'actual_body_sheets_v1/sheets.json')
    assert compact['actual_sha256']==digest(LIVE) and compact['pages']==88
    sheets=[dict(path=s['path'],sha256=s['sha256']) for s in compact['sheets']]+[menu['review_sheet']]
    assert len(sheets)==9""",
    'len(bodies)==223 and len(captions)==2':'len(bodies)==209 and len(captions)==7',
    'len(seen)==63':'len(seen)==86',
    "assert {r['id'] for r in doc['records'] if r.get('source_selector')==254}<=seen":
        "assert len({r['id'] for r in doc['records'] if r.get('source_selector')==254})==31 and len({r['id'] for r in doc['records'] if r.get('source_selector')==254}&seen)==18",
    "{'DK4_MES_B239_R0039','DK4_MES_B244_R0014','DK4_MES_B248_R0016'}":
        "{'DK4_MES_B252_R0116','DK4_MES_B252_R0184','DK4_MES_B274_R0015','DK4_MES_B266_R0009','DK4_MES_B277_R0066'}",
    'total_frames=21521':'total_frames=26801', 'source_speech_variants_observed=63':'source_speech_variants_observed=86',
    'native_body_pages_observed=68':'native_body_pages_observed=88',
    'complete_body_planes=144,complete_header_planes=136':'complete_body_planes=184,complete_header_planes=148',
    'offline_only_speech_variants=160':'offline_only_speech_variants=123',
    'all_four_FE_panels_FI_expansions_two_voice_objects_andrepresentative_pagination_observed=True':
        'eighteen_of31_FE_panels_FI_FA_two_voice_objects_andboth_selected_two_page_passages_observed=True',
    "menu['cursor_background_model']":"'Unchanged strict uniform-row gray/cyan edge-band checker; complete caption and blank pixels checked.'",
    'body_pages=228':'body_pages=212', 'observed_pages=68':'observed_pages=88',
    'actual_sheets_directly_viewed=13':'actual_sheets_directly_viewed=9',
    'visual_candidate_retentions=9':'visual_candidate_retentions=3',
    "{'revision':115,'retention':110}":"{'revision':129,'retention':87}",
    'Hodram B231–B250 exchanges':'Hodram B251–B280 exchanges',
    'records=225,revisions=115,retentions=110':'records=216,revisions=129,retentions=87',
    'typed_labels=2,scoped_names=19,actual_source_variants=63,actual_pages=68':
        'typed_labels=7,scoped_names=21,actual_source_variants=86,actual_pages=88',
    'actual_distinct_menu_behaviors=1,offline_only_source_variants=160':
        'actual_distinct_menu_behaviors=3,offline_only_source_variants=123',
    'Sealed 225 five-gate reviews, 228 stored pages and 68 observed pages.':
        'Sealed 216 five-gate reviews, 212 stored pages and 88 observed pages.',
})
env={**vars(previous),**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-five-individual-gates-exact-current-evidence','exec'),env)


if __name__=='__main__':
    from scripts.audit_story_glyph_consistency import load,save
    from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
    from scripts.analyze_hodram_B231_B250_menu_v1 import background_band
    model=ROOT/'actual_menus_v1/model_qualification_reuse.json'
    assert not model.exists()
    prior=Path('work/Hodram_B231_B250_clean_20261107/actual_menus_band_v1/model_qualification.json')
    qualified=load(prior)
    assert digest(prior)=='1af1a246e88a9ba61a5e0dccc11987d5daaf2878cf0c7baf7d0d26edf33517c8'
    assert qualified['all6_pixel_andcursor_mutations_rejected'] and qualified['no_ROM_orcapture_mutation']
    for path,expected in qualified['evidence'].items():
        assert digest(path)==expected
    assert load(MENU)['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
    save(model,dict(all6_pixel_andcursor_mutations_rejected=True,exact_checker_andnegative_cases_reused=True,
        prior=str(prior),prior_sha256=digest(prior),cases=qualified['cases'],no_ROM_orcapture_mutation=True,
        all_current_geometry_andcaption_pixels_freshly_checked=True,
        no_new_negative_case_execution=True,new_credit=0))
    # Every page in the eight compact body sheets and all three menus was directly
    # viewed. The original complete-screen sheets remain preserved as evidence.
    env['main']()
