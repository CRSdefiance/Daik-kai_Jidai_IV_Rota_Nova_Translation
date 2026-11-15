"""Describe the seven-block append over the verified 686-entry parent."""
from scripts.write_rafael_B168_B169_successor_spec_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'Rafael_B168_B169_research_final_v1_20261105': 'Rafael_B170_B176_research_final_v1_20261105',
    'Rafael1860_extended_release_verified_v1_20261105': 'Rafael1975_extended_release_verified_v1_20261105',
    'Rafael_B168_B169_current1860_20261105': 'Rafael_B170_B176_current1975_20261105',
    'rafael_B168_B169_registered_successor_spec_v1.json': 'rafael_B170_B176_registered_successor_spec_v1.json',
    "release['complete_stack_entries'] == 685": "release['complete_stack_entries'] == 686",
    '(115, 90, 25)': '(190, 152, 38)',
    'all115_stored_effective_body_bindings.json': 'all190_stored_effective_body_bindings.json',
    'translations/rafael_B168_B169_scoped_names_final_v1.json': 'translations/rafael_B170_B176_scoped_names_final_v1.json',
    "'scripts/seal_rafael_B168_B169_offline_v2.py','scripts/seal_rafael_B168_B169_offline_v1.py'":
        "'scripts/seal_rafael_B170_B176_offline_v1.py','scripts/check_rafael_B171_patron_panels_v1.py','scripts/refine_rafael_B171_final_rows_v2.py','dk4tool/patch/rafael_story_b168_b169_release_v1.py'",
    'all-routes-rafael1975-prepared-20261105': 'all-routes-rafael2165-prepared-20261105',
    'rafael-b168-b169': 'rafael-b170-b176',
    'dk4tool.patch.rafael_story_b168_b169_release_v1': 'dk4tool.patch.rafael_story_b170_b176_release_v1',
    'rafael_B168_B169_editorial_release_v1.json': 'rafael_B170_B176_editorial_release_v1.json',
    '_Rafael1975_release_v1.json': '_Rafael2165_release_v1.json',
    'record_count=115, speech_count=115, typed_choice_count=0, menu_count=0, scoped_name_count=10, native_pages=117,':
        'record_count=190, speech_count=190, typed_choice_count=0, menu_count=0, scoped_name_count=13, native_pages=190,',
    'relative_cases=125, FE_count=0, actual_frames=19361, actual_runs=1, actual_speeches=58, actual_body_pages=60, offline_speeches=57':
        'relative_cases=100, FE_count=6, actual_frames=22241, actual_runs=1, actual_speeches=72, actual_body_pages=72, offline_speeches=118',
    'with 90 revisions and 25 justified retentions': 'with 152 revisions and 38 justified retentions',
    'Wrote the exact B168–B169 successor specification.': 'Wrote the exact B170–B176 successor specification.',
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::exact-seven-block-source-bound-append', 'exec'), globals())
