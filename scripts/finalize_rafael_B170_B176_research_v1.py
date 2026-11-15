"""Bind all five gates for B170–B176 to the exact stored and observed evidence."""
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text


BASE = Path('scripts/finalize_rafael_B161_B165_research_v1.py')
SOURCE = Path('work/analysis/Rafael_B170_B176_current1975_20261105')
source = checked_text(BASE.read_text(encoding='utf-8'), {
    'Rafael_B161_B165_research_final_v1_20261105': 'Rafael_B170_B176_research_final_v1_20261105',
    "A/'Rafael_B161_B165_reconstruction_v1_20261105/reconstruction.json'": "SOURCE/'reconstruction_v1/reconstruction.json'",
    "A/'Rafael_B161_B165_stored_v1_20261105/stored_native_verification.json'": "SOURCE/'stored_native_v1/stored_native_verification.json'",
    "A/'Rafael_B161_B165_stored_catalogue_v1_20261105/all67_stored_effective_body_bindings.json'": "SOURCE/'stored_catalogue_v1/all190_stored_effective_body_bindings.json'",
    "A/'Rafael_B161_B165_loaders_v1_20261105/verification.json'": "SOURCE/'loaders_v1/verification.json'",
    "A/'Rafael_B161_B165_storage_inputs_v1_20261105/visual_review.json'": "SOURCE/'offline_display_package_v1/visual_review.json'",
    "A/'Rafael_B161_B165_actual_fixtures_v1_20261105/mediterranean_story_and_audiences_fixture.json'": "SOURCE/'actual_fixtures_v1/carlo_cristina_samwell_and_jam_fixture.json'",
    "A/'Rafael_B161_B165_actual_run_v1_20261105/terminal.json'": "SOURCE/'actual_run_v1/terminal.json'",
    "A/'Rafael_B161_B165_actual_pixels_v1_20261105/focused_actual_pixels.json'": "SOURCE/'actual_pixels_v1/focused_actual_pixels.json'",
    "A/'Rafael_B161_B165_actual_compact_v1_20261105/receipt.json'": "SOURCE/'actual_compact_v1/receipt.json'",
    'rafael_B161_B165_': 'rafael_B170_B176_',
    '==67': '==190',
    '==68': '==190',
    '==(36,32,100)': '==(84,106,100)',
    '==(343,10,676)': '==(343,14,672)',
    "visual['scoped_name_count']==8": "visual['scoped_name_count']==13",
    '==18401': '==22241',
    "sheets['actual_dialogue_pages']==56": "sheets['actual_dialogue_pages']==72",
    "len(visual['sheets'])==9": "len(visual['sheets'])==30 and len(sheets['bottom_screen_sheets'])==6 and len(sheets['full_scene_sheets'])==1",
    '=={0,4,5,8,120,125,132,163}': '=={0,5,6,7,8,11,19,20,22,105,116,142,151}',
    'len(observed)==55 and len(samples)==56 and len(set(b0)-observed)==12': 'len(observed)==72 and len(samples)==72 and len(set(b0)-observed)==118',
    "    assert b'Castor Co., I see.' in bytes.fromhex(b0['DK4_MES_B162_R0006']['expanded_hex'])\n"
    "    assert ('DK4_MES_B165_R0016',2) in samples":
        "    assert all(b'Rafael' in bytes.fromhex(b0[f'DK4_MES_B176_R{i:04d}']['expanded_hex']) for i in (98,106))\n"
        "    assert b'J-A-M' in bytes.fromhex(b0['DK4_MES_B176_R0044']['expanded_hex'])\n"
        "    assert b'Jam Jack Ludwyan!' in bytes.fromhex(b0['DK4_MES_B176_R0148']['expanded_hex'])\n"
        "    assert {r['id'] for r in fixture['selected_records'] if r['selector']==254}=={r['id'] for r in doc['records'] if r['source_selector']==254}\n"
        "    assert sum(r.get('source_staged_FE',False) for r in doc['records'])==3\n"
        "    assert 'DK4_MES_B174_R0006' in observed and 'DK4_MES_B175_R0006' not in observed",
    "        r.update(planned_English_markup=plans[k]['formatted_markup'],":
        "        if r.get('source_staged_FE'):\n"
        "            assert (k,1) in samples\n"
        "            r['FE_source_layout_native_requalification_pending']=False\n"
        "        r.update(planned_English_markup=plans[k]['formatted_markup'],",
    "=={'revision':51,'retention':16}": "=={'revision':152,'retention':38}",
    'doc_path,plan_path,native_path,menu_path,styles_path,Path(__file__)]':
        'doc_path,plan_path,native_path,menu_path,styles_path,BASE,Path(__file__)]',
    'body_pages=68,scoped_public_names=8,observed_pages=56': 'body_pages=190,scoped_public_names=13,observed_pages=72',
    'total_frames=18401,initialized_fixture_runs=1,source_speech_variants_observed=55':
        'total_frames=22241,initialized_fixture_runs=1,source_speech_variants_observed=72',
    'native_body_pages_observed=56,actual_choice_labels=0,offline_only_speech_variants=12':
        'native_body_pages_observed=72,actual_choice_labels=0,offline_only_speech_variants=118',
    'observed_public_name_actor_IDs=sorted(actors),menus=[]':
        'observed_public_name_actor_IDs=sorted(actors),all_six_FE_pages_observed=True,three_source_staged_heading_panels_observed=True,menus=[]',
    'native_body_pages=68,actual_source_speech_variants=55,actual_body_pages=56,offline_only_source_speech_variants=12':
        'native_body_pages=190,actual_source_speech_variants=72,actual_body_pages=72,offline_only_source_speech_variants=118',
    'records=67,revisions=51,retentions=16': 'records=190,revisions=152,retentions=38',
    'body_pages=68,typed_labels=0,scoped_public_names=8,actual_source_variants=55,actual_pages=56,offline_only_source_variants=12':
        'body_pages=190,typed_labels=0,scoped_public_names=13,actual_source_variants=72,actual_pages=72,offline_only_source_variants=118',
    'Sealed all 67 five-gate reviews, 55 observed speeches, 56 observed pages and eight public headers.':
        'Sealed 190 five-gate reviews, 72 observed pages, all six modal panels and 13 public nameplates.',
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::same-five-gate-checks-with-three-exact-staged-panels', 'exec'), globals())
