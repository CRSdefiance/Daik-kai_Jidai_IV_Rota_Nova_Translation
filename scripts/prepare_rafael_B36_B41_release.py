"""Register the complete six-exchange successor through the unchanged six-stage workflow."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/prepare_rafael_early_tutorial_release.py').read_text(encoding='utf-8'),{
    'Rafael_early_tutorial_B42_B43_release_20261104':'Rafael_B36_B41_release_20261104',
    "PROFILE='all-routes-rafael-early-tutorial-static-text-20261104'":"PROFILE='all-routes-rafael-b36-b41-static-text-20261104'",
    "OLD='all-routes-hodram-b191-b210-static-text-20261104'":"OLD='all-routes-rafael-early-tutorial-static-text-20261104'",
    'rafael_B42_B43':'rafael_B36_B41',
    'rafael_early_tutorial_release_v1':'rafael_B36_B41_release_v1',
    'Rafael_early_tutorial_B42_B43_checked_20261104':'Rafael_B36_B41_checked_20261104',
    'Rafael_early_tutorial_B42_B43_storage_20261104/reconstruction_v2/reconstruction.json':'Rafael_B36_B41_rebuilt_20261104/reconstruction.json',
    'Rafael_early_tutorial_B42_B43_formatting_20261104/speech_display_approved_v2':'Rafael_B36_B41_formatting_20261104/speech_display_approved_v3',
    'fcc6e85f43b101ad459de1ff035be49640c04925c4a728bc9febfd37b5b69f96':'7ab22d90bc44f1c737608bec8df44044a62df6ebe3eda14f9d704f7122533752',
    'out/all_routes_combined_hodram_b191_b210_static_text_20261104_candidate.manifest.json':'out/all_routes_combined_rafael_early_tutorial_static_text_20261104_candidate.manifest.json',
    'all40_native_pages.json':'all175_native_pages.json',
    "len(doc['records'])==40":"len(doc['records'])==175",
    '88e9984f767a0fa14bde5e9ce07392d1fbcf44fb41a6815e4ca466740fb82a15':'c555f555a0e6a15b35e10a27b87ac98ed17601ba814cfeb9ba3d98dcc87344a8',
    "    assert len(FE)==1 and FE[0]['complete_native_English_display']['planned_native_row_comparison']['complete_glyph_row_membership_exact']":'    assert not FE',
    'FE_records=1':'FE_records=0',
    'work/analysis/Rafael_early_tutorial_B42_B43_storage_20261104/stored_native_v1/stored_native_verification.json':'work/analysis/Rafael_B36_B41_stored_native_20261104/stored_native_verification.json',
    'work/analysis/Rafael_early_tutorial_B42_B43_loaders_20261104/verification.json':'work/analysis/Rafael_B36_B41_loaders_20261104/verification.json',
    "actual=CHECKED/'actual_visual_approval.json'":"actual=CHECKED/'actual_review.json'",
    "name_visual=CHECKED/'scoped_name_visual_approval.json'":"name_visual=Path('work/analysis/Rafael_B36_B41_progressive_names_20261104/actual_header_verification_v2.json')",
    "focused_pixels=Path('work/analysis/Rafael_early_tutorial_B42_B43_actual_pixels_20261104/focused_actual_pixels.json'),FE_layout=FE_path)":
        "focused_pixels=Path('work/analysis/Rafael_B36_B41_focused_actual_pixels_20261104/focused_actual_pixels.json'),FE_layout=FE_path,\n        stored_lookup=Path('work/analysis/Rafael_B36_B41_stored_catalogue_20261104/all175_stored_effective_body_bindings.json'))",
    "CHECKED/'current_rebuilder_exact_replay.json',CHECKED/'formatting_checkpoint.json'":"CHECKED/'formatting_checkpoint.json'",
    'dk4tool/script/rafael_early_tutorial_rebuild_v1.py':'dk4tool/script/rafael_story_rebuild_with_fu_v1.py',
    'scripts/finalize_rafael_early_tutorial_review.py':'scripts/finalize_rafael_B36_B41_review.py',
    'scripts/check_rafael_early_tutorial_stored.py':'scripts/check_rafael_B36_B41_stored_blocks.py',
    'scripts/analyze_rafael_early_tutorial_actual.py':'scripts/analyze_rafael_B36_B41_focused_actual.py',
    'scripts/check_rafael_early_tutorial_loaders.py':'scripts/check_rafael_B36_B41_loaders.py',
    'translations/ascii_glyph_right_bounds_rafael_B42_B43_v1.json':'translations/ascii_glyph_right_bounds_rafael_B36_B41_v1.json',
    "format='dk4-rafael-early-tutorial-release-v1'":"format='dk4-rafael-B36-B41-release-v1'",
    'record_count=40,blocks=[42,43],native_pages=42,relative_cases=0,FE_count=1':'record_count=175,blocks=list(range(36,42)),native_pages=177,relative_cases=400,FE_count=0',
    "len(proof['changed_records'])==40":"len(proof['changed_records'])==175",
    "id='rafael-early-tutorial'":"id='rafael-B36-B41'",
    'Experimental cumulative Rafael early-tutorial successor:40 reviews,19 revisions/21 retentions,42 pages/two page fixes.':'Experimental cumulative Rafael B36-B41 successor:175 reviews,76 revisions/99 retentions,177 pages/four wrap fixes/two ASCII-I fixes.',
    'Registered 40-review Rafael tutorial profile;':'Registered 175-review Rafael B36-B41 profile;',
})
exec(compile(source,__file__+'::same-six-final-stages-complete-registered-Rafael-story-successor','exec'),globals())
