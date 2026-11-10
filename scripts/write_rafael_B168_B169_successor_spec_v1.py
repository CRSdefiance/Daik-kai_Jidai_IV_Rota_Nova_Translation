"""Describe the 115 reviewed speeches over the verified 685-entry predecessor."""
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text


BASE = Path('scripts/write_rafael_B161_B165_successor_spec_v2.py')
source = checked_text(BASE.read_text(encoding='utf-8'), {
    'Rafael_B161_B165_research_final_v1_20261105': 'Rafael_B168_B169_research_final_v1_20261105',
    'Rafael1607_extended_release_verified_v1_20261105': 'Rafael1860_extended_release_verified_v1_20261105',
    'Rafael_B161_B165_reconstruction_v1_20261105/reconstruction.json':
        'Rafael_B168_B169_current1860_20261105/reconstruction_v1/reconstruction.json',
    'rafael_B161_B165_registered_successor_spec_v2.json': 'rafael_B168_B169_registered_successor_spec_v1.json',
    "release['complete_stack_entries'] == 683": "release['complete_stack_entries'] == 685",
    '(67, 51, 16)': '(115, 90, 25)',
    'Rafael_B161_B165_stored_v1_20261105/stored_native_verification.json':
        'Rafael_B168_B169_current1860_20261105/stored_native_v1/stored_native_verification.json',
    'Rafael_B161_B165_stored_catalogue_v1_20261105/all67_stored_effective_body_bindings.json':
        'Rafael_B168_B169_current1860_20261105/stored_catalogue_v1/all115_stored_effective_body_bindings.json',
    'Rafael_B161_B165_loaders_v1_20261105/verification.json': 'Rafael_B168_B169_current1860_20261105/loaders_v1/verification.json',
    'translations/rafael_B161_B165_scoped_names_final_v1.json': 'translations/rafael_B168_B169_scoped_names_final_v1.json',
    "'scripts/rebuild_rafael_B161_B165_reviewed_v1.py',":
        "'scripts/seal_rafael_B168_B169_offline_v2.py','scripts/seal_rafael_B168_B169_offline_v1.py','dk4tool/patch/rafael_story_b161_b165_release_v2.py',",
    'all-routes-rafael1674-prepared-20261105': 'all-routes-rafael1975-prepared-20261105',
    'rafael-b161-b165': 'rafael-b168-b169',
    'rafael_story_b161_b165_release_v2': 'rafael_story_b168_b169_release_v1',
    'rafael_B161_B165_editorial_release_v2.json': 'rafael_B168_B169_editorial_release_v1.json',
    '_Rafael1674_release_v2.json': '_Rafael1975_release_v1.json',
    'record_count=67, speech_count=67, typed_choice_count=0, menu_count=0, scoped_name_count=8, native_pages=68,':
        'record_count=115, speech_count=115, typed_choice_count=0, menu_count=0, scoped_name_count=10, native_pages=117,',
    'relative_cases=100, FE_count=1, actual_frames=18401, actual_runs=1, actual_speeches=55, actual_body_pages=56, offline_speeches=12':
        'relative_cases=125, FE_count=0, actual_frames=19361, actual_runs=1, actual_speeches=58, actual_body_pages=60, offline_speeches=57',
    'with 51 revisions and 16 justified retentions': 'with 90 revisions and 25 justified retentions',
    'Wrote the exact five-block successor specification.': 'Wrote the exact B168–B169 successor specification.',
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::same-qualified-source-bound-append', 'exec'), globals())
