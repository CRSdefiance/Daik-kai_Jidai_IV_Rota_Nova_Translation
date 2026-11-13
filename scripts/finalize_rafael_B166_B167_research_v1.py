"""Seal the reviewed 186-record batch after focused runtime and source header checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

BASE=Path('scripts/finalize_rafael_B161_B165_research_v1.py')
SOURCE=Path('work/analysis/Rafael_B166_B167_current1674_20261105')
ALIAS=SOURCE/'source_actor8_fixture_v2/actor8_alias_resolution.json'
source=checked_text(BASE.read_text(encoding='utf-8'),{
    'Rafael_B161_B165_research_final_v1_20261105':'Rafael_B166_B167_research_final_v1_20261105',
    "A/'Rafael_B161_B165_reconstruction_v1_20261105/reconstruction.json'":"SOURCE/'reconstruction_v1/reconstruction.json'",
    "A/'Rafael_B161_B165_stored_v1_20261105/stored_native_verification.json'":"SOURCE/'stored_native_v1/stored_native_verification.json'",
    "A/'Rafael_B161_B165_stored_catalogue_v1_20261105/all67_stored_effective_body_bindings.json'":
        "SOURCE/'stored_catalogue_v1/all186_stored_effective_body_bindings.json'",
    "A/'Rafael_B161_B165_loaders_v1_20261105/verification.json'":"SOURCE/'loaders_v1/verification.json'",
    "A/'Rafael_B161_B165_storage_inputs_v1_20261105/visual_review.json'":"SOURCE/'offline_display_package_v1/visual_review.json'",
    "A/'Rafael_B161_B165_actual_fixtures_v1_20261105/mediterranean_story_and_audiences_fixture.json'":
        "SOURCE/'actual_fixtures_v1/audience_letter_and_recruitment_fixture.json'",
    "A/'Rafael_B161_B165_actual_run_v1_20261105/terminal.json'":"SOURCE/'actual_run_v1/terminal.json'",
    "A/'Rafael_B161_B165_actual_pixels_v1_20261105/focused_actual_pixels.json'":"SOURCE/'actual_pixels_v2/focused_actual_pixels.json'",
    "A/'Rafael_B161_B165_actual_compact_v1_20261105/receipt.json'":"SOURCE/'actual_compact_v2/receipt.json'",
    'rafael_B161_B165_':'rafael_B166_B167_',
    '==67':'==186',
    '==68':'==187',
    '==(36,32,100)':'==(83,104,740)',
    "len(stored['relative_cases'])==20 and rebuilt['relative_sites']==20":
        "len(stored['relative_cases'])==148 and rebuilt['relative_sites']==148",
    '==(343,10,676)':'==(343,4,682)',
    "visual['scoped_name_count']==8":"visual['scoped_name_count']==24",
    '==18401':'==29441',
    "sheets['actual_dialogue_pages']==56":"sheets['actual_dialogue_pages']==102",
    "len(visual['sheets'])==9":"len(visual['sheets'])==24",
    '=={0,4,5,8,120,125,132,163}':' and len(actors)==24',
    'len(observed)==55 and len(samples)==56 and len(set(b0)-observed)==12':
        'len(observed)==101 and len(samples)==102 and len(set(b0)-observed)==85',
    """    assert b'Castor Co., I see.' in bytes.fromhex(b0['DK4_MES_B162_R0006']['expanded_hex'])
    assert ('DK4_MES_B165_R0016',2) in samples""":
        """    alias=load(ALIAS)
    assert alias['retain_Arcadius_as_source_progressive_header_Eirene_as_scene_voice_and_FE_heading']
    assert all(digest(p)==h for p,h in alias['evidence'].items())
    assert ('DK4_MES_B166_R0085',2) in samples
    assert {r['id'] for r in alias['actors']}=={f'DK4_MES_B166_R{i:04d}' for i in (584,658,770,779)}
    assert b'Al Ferid Shin.' in bytes.fromhex(b0['DK4_MES_B167_R0217']['expanded_hex'])
    assert b'Muint obrigada' in bytes.fromhex(b0['DK4_MES_B166_R0791']['expanded_hex'])
    assert pixels['exact_black_and_CP932_shadow_masks_for_four_source_ellipses']
    assert sum(r['selector']==254 for r in fixture['selected_records'])==29""",
    """        r.update(planned_English_markup=plans[k]['formatted_markup'],""":
        """        if r.get('FE_source_layout_native_requalification_pending'):
            r['FE_source_layout_native_requalification_pending']=False
        if r.get('contextual_nameplate_vs_default_actor8_pending'):
            assert k in {a['id'] for a in alias['actors']}
            r['contextual_nameplate_vs_default_actor8_pending']=False
            r['source_bound_progressive_display_name']='Arcadius Eudoxios'
            r['actor8_source_and_English_alias_proof']=str(ALIAS)
        r.update(planned_English_markup=plans[k]['formatted_markup'],""",
    "=={'revision':51,'retention':16}":"=={'revision':146,'retention':40}",
    "        r['review']['formatting']=True":
        """        r['review']['formatting']=True
        r['contextual_alias_check_pending']=False
        if r['actor_ID']==8:
            r['actor8_source_and_English_alias_proof']=str(ALIAS)""",
    'doc_path,plan_path,native_path,menu_path,styles_path,Path(__file__)]':
        'doc_path,plan_path,native_path,menu_path,styles_path,ALIAS,BASE,Path(__file__)]',
    'body_pages=68,scoped_public_names=8,observed_pages=56':'body_pages=187,scoped_public_names=24,observed_pages=102',
    'total_frames=18401,initialized_fixture_runs=1,source_speech_variants_observed=55':
        'total_frames=29441,initialized_fixture_runs=1,source_speech_variants_observed=101,clean_alias_fixture_frames=6201',
    'native_body_pages_observed=56,actual_choice_labels=0,offline_only_speech_variants=12':
        'native_body_pages_observed=102,actual_choice_labels=0,offline_only_speech_variants=85',
    'observed_public_name_actor_IDs=sorted(actors),menus=[]':
        'observed_public_name_actor_IDs=sorted(actors),menus=[],source_actor8_alias_proof=str(ALIAS),all_29_modal_pages_observed=True',
    'native_body_pages=68,actual_source_speech_variants=55,actual_body_pages=56,offline_only_source_speech_variants=12':
        'native_body_pages=187,actual_source_speech_variants=101,actual_body_pages=102,offline_only_source_speech_variants=85',
    'records=67,revisions=51,retentions=16':'records=186,revisions=146,retentions=40',
    'body_pages=68,typed_labels=0,scoped_public_names=8,actual_source_variants=55,actual_pages=56,offline_only_source_variants=12':
        'body_pages=187,typed_labels=0,scoped_public_names=24,actual_source_variants=101,actual_pages=102,offline_only_source_variants=85',
    'Sealed all 67 five-gate reviews, 55 observed speeches, 56 observed pages and eight public headers.':
        'Sealed all 186 five-gate reviews, 101 observed speeches, 102 observed pages and 24 public headers.',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-gates-with-exact-staged-and-alias-coverage','exec'),globals())
