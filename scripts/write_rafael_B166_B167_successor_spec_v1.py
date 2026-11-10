"""Describe the 186-speech append over the verified 684-entry Rafael predecessor."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

BASE=Path('scripts/write_rafael_B161_B165_successor_spec_v2.py')
source=checked_text(BASE.read_text(encoding='utf-8'),{
    'Rafael_B161_B165_research_final_v1_20261105':'Rafael_B166_B167_research_final_v1_20261105',
    'Rafael1607_extended_release_verified_v1_20261105':'Rafael1674_extended_release_verified_v1_20261105',
    'Rafael_B161_B165_reconstruction_v1_20261105/reconstruction.json':'Rafael_B166_B167_current1674_20261105/reconstruction_v1/reconstruction.json',
    'rafael_B161_B165_registered_successor_spec_v2.json':'rafael_B166_B167_registered_successor_spec_v1.json',
    "release['complete_stack_entries'] == 683":"release['complete_stack_entries'] == 684",
    '(67, 51, 16)':'(186, 146, 40)',
    'Rafael_B161_B165_stored_v1_20261105/stored_native_verification.json':'Rafael_B166_B167_current1674_20261105/stored_native_v1/stored_native_verification.json',
    'Rafael_B161_B165_stored_catalogue_v1_20261105/all67_stored_effective_body_bindings.json':
        'Rafael_B166_B167_current1674_20261105/stored_catalogue_v1/all186_stored_effective_body_bindings.json',
    'Rafael_B161_B165_loaders_v1_20261105/verification.json':'Rafael_B166_B167_current1674_20261105/loaders_v1/verification.json',
    "scoped_names='translations/rafael_B161_B165_scoped_names_final_v1.json',":
        """scoped_names='translations/rafael_B166_B167_scoped_names_final_v1.json',
        actor8_alias=str(A/'Rafael_B166_B167_current1674_20261105/source_actor8_fixture_v2/actor8_alias_resolution.json'),""",
    "'scripts/rebuild_rafael_B161_B165_reviewed_v1.py',":
        "'scripts/rebuild_rafael_B166_B167_reviewed_v1.py','dk4tool/patch/rafael_story_b161_b165_release_v2.py',",
    'all-routes-rafael1674-prepared-20261105':'all-routes-rafael1860-prepared-20261105',
    'rafael-b161-b165':'rafael-b166-b167',
    'rafael_story_b161_b165_release_v2':'rafael_story_b166_b167_release_v1',
    'rafael_B161_B165_editorial_release_v2.json':'rafael_B166_B167_editorial_release_v1.json',
    '_Rafael1674_release_v2.json':'_Rafael1860_release_v1.json',
    'record_count=67, speech_count=67, typed_choice_count=0, menu_count=0, scoped_name_count=8, native_pages=68,':
        'record_count=186, speech_count=186, typed_choice_count=0, menu_count=0, scoped_name_count=24, native_pages=187,',
    'relative_cases=100, FE_count=1, actual_frames=18401, actual_runs=1, actual_speeches=55, actual_body_pages=56, offline_speeches=12':
        'relative_cases=740, FE_count=29, actual_frames=29441, actual_runs=1, actual_speeches=101, actual_body_pages=102, offline_speeches=85',
    'with 51 revisions and 16 justified retentions':'with 146 revisions and 40 justified retentions',
    'Wrote the exact five-block successor specification.':'Wrote the exact two-block 186-speech successor specification.',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::exact-source-bound-successor-inputs','exec'),globals())
