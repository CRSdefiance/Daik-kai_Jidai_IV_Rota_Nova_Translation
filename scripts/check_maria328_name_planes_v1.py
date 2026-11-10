"""Reuse13 exact approved name planes andcheck15 new strings withthe unchanged native oracle."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/check_maria303_name_planes_v1.py').read_text(encoding='utf-8'), {
    "ROOT=Path('work/Maria_B58_B70_clean_20261109')":"ROOT=Path('work/Maria_B73_B95_clean_20261109')",
    'work/Maria_B51_B57_clean_20261109':'work/Maria_B58_B70_clean_20261109',
    'scoped20_names_editorial_review_v3.json':'scoped24_names_editorial_review_v1.json',
    "binding_rows=deepcopy(bound['records']);binding_rows.append(deepcopy(terms['spoken_Mihwa']))":"binding_rows=deepcopy(bound['records'])",
    'len(binding_rows)==20':'len(binding_rows)==24',
    "bound_source if row['actor_ID']!=201 else term_source":"bound_source",
    "approval['all31_name_strings_directly_viewed']":"approval['all24_names_andfour_captions_directly_viewed']",
    '(24,16,8)':'(28,13,15)',
    'fresh_native_name_strings=8,reused_native_name_strings=16':'fresh_native_name_strings=15,reused_native_name_strings=13',
    '(20,24,8,16)':'(24,28,15,13)',
    'Qualified20 actors/40 exact getter bindings;24 strings:16 compatible native planes reused,eight fresh.':
        'Qualified24 actors/48 exact getter bindings;28 strings:13 exact approved planes reused,15 fresh.',
})
if __name__ == '__main__':
    exec(compile(source,__file__+'::same-native-style11-pixels-codes-bounds-and13-exact-plane-reuses','exec'),globals())
