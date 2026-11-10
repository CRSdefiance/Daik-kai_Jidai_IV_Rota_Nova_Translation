"""Bind both full dialogue reviews to directly viewed stored and focused gameplay evidence."""
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text


BASE = Path('scripts/finalize_rafael_B161_B165_research_v1.py')
SOURCE = Path('work/analysis/Rafael_B168_B169_current1860_20261105')
B169_LABELS = Path('translations/rafael_B169_scoped_names_review_v1.json')
MASK_PROBE = SOURCE / 'actual_mask_diagnostics_v1.txt'
source = checked_text(BASE.read_text(encoding='utf-8'), {
    'Rafael_B161_B165_research_final_v1_20261105': 'Rafael_B168_B169_research_final_v1_20261105',
    "A/'Rafael_B161_B165_reconstruction_v1_20261105/reconstruction.json'": "SOURCE/'reconstruction_v1/reconstruction.json'",
    "A/'Rafael_B161_B165_stored_v1_20261105/stored_native_verification.json'": "SOURCE/'stored_native_v1/stored_native_verification.json'",
    "A/'Rafael_B161_B165_stored_catalogue_v1_20261105/all67_stored_effective_body_bindings.json'": "SOURCE/'stored_catalogue_v1/all115_stored_effective_body_bindings.json'",
    "A/'Rafael_B161_B165_loaders_v1_20261105/verification.json'": "SOURCE/'loaders_v1/verification.json'",
    "A/'Rafael_B161_B165_storage_inputs_v1_20261105/visual_review.json'": "SOURCE/'offline_display_v2/visual_review.json'",
    "A/'Rafael_B161_B165_actual_fixtures_v1_20261105/mediterranean_story_and_audiences_fixture.json'": "SOURCE/'actual_fixtures_v1/angelo_trade_and_ian_recruitment_fixture.json'",
    "A/'Rafael_B161_B165_actual_run_v1_20261105/terminal.json'": "SOURCE/'actual_run_v1/terminal.json'",
    "A/'Rafael_B161_B165_actual_pixels_v1_20261105/focused_actual_pixels.json'": "SOURCE/'actual_pixels_v2/focused_actual_pixels.json'",
    "A/'Rafael_B161_B165_actual_compact_v1_20261105/receipt.json'": "SOURCE/'actual_compact_v1/receipt.json'",
    "Path('translations/rafael_B161_B165_scoped_names_review_v1.json')": "SOURCE/'focused_name_decisions_v1.json'",
    'rafael_B161_B165_': 'rafael_B168_B169_',
    "    doc_path,plan_path,native_path,menu_path,styles_path=map(Path,": 
        "    names = {**load(B169_LABELS), 'records': names['records']}\n"
        "    assert len(names['records'])==10\n"
        "    doc_path,plan_path,native_path,menu_path,styles_path=map(Path,",
    '==67': '==115',
    '==68': '==117',
    '==(36,32,100)': '==(55,62,125)',
    "len(stored['relative_cases'])==20 and rebuilt['relative_sites']==20": "len(stored['relative_cases'])==25 and rebuilt['relative_sites']==25",
    '==(343,10,676)': '==(343,4,682)',
    "visual['scoped_name_count']==8": "visual['scoped_names']==10",
    '==18401': '==19361',
    "sheets['actual_dialogue_pages']==56": "sheets['actual_dialogue_pages']==60",
    "    review_sheets=visual['sheets']+sheets['bottom_screen_sheets']+sheets['full_scene_sheets']":
        "    offline_sheets=visual['selected_body_previews']+visual['name_sheets']+[visual['reused_Angelo_name_preview']]\n"
        "    review_sheets=offline_sheets+sheets['bottom_screen_sheets']+sheets['full_scene_sheets']",
    "len(visual['sheets'])==9": "len(offline_sheets)==16 and len(sheets['bottom_screen_sheets'])==5 and len(sheets['full_scene_sheets'])==1",
    '=={0,4,5,8,120,125,132,163}': '=={0,5,6,15,21,92,96,152,164,165}',
    'len(observed)==55 and len(samples)==56 and len(set(b0)-observed)==12': 'len(observed)==58 and len(samples)==60 and len(set(b0)-observed)==57',
    "    assert b'Castor Co., I see.' in bytes.fromhex(b0['DK4_MES_B162_R0006']['expanded_hex'])\n"
    "    assert ('DK4_MES_B165_R0016',2) in samples":
        "    assert b'Rafael Castor.' in bytes.fromhex(b0['DK4_MES_B168_R0050']['expanded_hex'])\n"
        "    assert b'My name is Ian Dukov.' in bytes.fromhex(b0['DK4_MES_B169_R0291']['expanded_hex'])\n"
        "    assert {(f'DK4_MES_B168_R{i:04d}',2) for i in (182,214)}<=samples.keys()\n"
        "    assert pixels['exact_CP932_punctuation_ink_and_shadow_masks']\n"
        "    assert all(r['selector']!=254 for r in fixture['selected_records'])",
    "=={'revision':51,'retention':16}": "=={'revision':90,'retention':25}",
    'doc_path,plan_path,native_path,menu_path,styles_path,Path(__file__)]':
        'doc_path,plan_path,native_path,menu_path,styles_path,B169_LABELS,MASK_PROBE,BASE,Path(__file__)]',
    'body_pages=68,scoped_public_names=8,observed_pages=56': 'body_pages=117,scoped_public_names=10,observed_pages=60',
    'total_frames=18401,initialized_fixture_runs=1,source_speech_variants_observed=55':
        'total_frames=19361,initialized_fixture_runs=1,source_speech_variants_observed=58',
    'native_body_pages_observed=56,actual_choice_labels=0,offline_only_speech_variants=12':
        'native_body_pages_observed=60,actual_choice_labels=0,offline_only_speech_variants=57',
    'native_body_pages=68,actual_source_speech_variants=55,actual_body_pages=56,offline_only_source_speech_variants=12':
        'native_body_pages=117,actual_source_speech_variants=58,actual_body_pages=60,offline_only_source_speech_variants=57',
    'records=67,revisions=51,retentions=16': 'records=115,revisions=90,retentions=25',
    'body_pages=68,typed_labels=0,scoped_public_names=8,actual_source_variants=55,actual_pages=56,offline_only_source_variants=12':
        'body_pages=117,typed_labels=0,scoped_public_names=10,actual_source_variants=58,actual_pages=60,offline_only_source_variants=57',
    'Sealed all 67 five-gate reviews, 55 observed speeches, 56 observed pages and eight public headers.':
        'Sealed 115 five-gate reviews, 58 observed speeches, 60 observed pages and ten public nameplates.',
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::same-five-gates-for-115-ordinary-speeches', 'exec'), globals())
