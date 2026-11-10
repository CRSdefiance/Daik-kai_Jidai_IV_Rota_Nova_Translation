"""Reuse11 exact approved name planes and check19 new strings on the same renderer."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/check_maria303_name_planes_v1.py').read_text(encoding='utf-8'),{
    "ROOT=Path('work/Maria_B58_B70_clean_20261109')":"ROOT=Path('work/Maria_B137_B151_clean_20261109')",
    "PRIOR=Path('work/Maria_B51_B57_clean_20261109/name_planes_v1/native_name_planes.json')":"PRIOR=Path('work/Maria_B125_B136_clean_20261109/name_planes_v1/native_name_planes.json')",
    "PRIOR_APPROVAL=Path('work/Maria_B51_B57_clean_20261109/offline_display_approval_v1.json')":"PRIOR_APPROVAL=Path('work/Maria_B125_B136_clean_20261109/offline_display_approval_v1.json')",
    "ROOT/'scoped20_names_editorial_review_v3.json'":"Path('translations/maria_B137_B151_scoped_names_v1.json')",
    "binding_rows=deepcopy(bound['records']);binding_rows.append(deepcopy(terms['spoken_Mihwa']))":"binding_rows=deepcopy(bound['records'])",
    'len(binding_rows)==20':'len(binding_rows)==26',
    "bound_source if row['actor_ID']!=201 else term_source":"bound_source",
    "approval['all31_name_strings_directly_viewed'] and approval['names_sha256']==digest(PRIOR)":"approval['all_names_andtwo_captions_directly_viewed'] and approval['evidence'][str(PRIOR)]==digest(PRIOR)",
    '(24,16,8)':'(30,11,19)',
    'fresh_native_name_strings=8,reused_native_name_strings=16':'fresh_native_name_strings=19,reused_native_name_strings=11',
    '(20,24,8,16)':'(26,30,19,11)',
    'same-style11-complete-native-checks-with16-exact-plane-reuses':'same-style11-complete-native-checks-with11-exact-plane-reuses',
    'Qualified20 actors/40 exact getter bindings;24 strings:16 compatible native planes reused,eight fresh.':'Qualified26 actors/52 exact getter bindings;30 strings:11 compatible native planes reused,19 fresh.',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-native-name-codes-pixels-bounds-andcompatible-plane-reuse','exec'),globals())
