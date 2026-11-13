"""Reuse16 exact approved native name planes; check13 remaining scoped strings."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/check_maria303_name_planes_v1.py').read_text(encoding='utf-8'),{
    "ROOT=Path('work/Maria_B58_B70_clean_20261109')":"ROOT=Path('work/Maria_B96_B124_clean_20261109')",
    'work/Maria_B51_B57_clean_20261109':'work/Maria_B73_B95_clean_20261109',
    "ROOT/'scoped20_names_editorial_review_v3.json'":"Path('translations/maria_B96_B124_scoped_names_v2.json')",
    'scoped_terms_reference_v1.json':'scoped_item_stat_reference_v1.json',
    "binding_rows=deepcopy(bound['records']);binding_rows.append(deepcopy(terms['spoken_Mihwa']))":"binding_rows=deepcopy(bound['records'])",
    'len(binding_rows)==20':'len(binding_rows)==26',
    "bound_source if row['actor_ID']!=201 else term_source":"bound_source",
    "approval['all31_name_strings_directly_viewed']":"approval['all_names_and15_captions_directly_viewed']",
    '(24,16,8)':'(29,16,13)',
    'fresh_native_name_strings=8,reused_native_name_strings=16':'fresh_native_name_strings=13,reused_native_name_strings=16',
    '(20,24,8,16)':'(26,29,13,16)',
    'Qualified20 actors/40 exact getter bindings;24 strings:16 compatible native planes reused,eight fresh.':
        'Qualified26 actors/52 exact getter bindings;29 strings:16 compatible native planes reused,13 fresh.',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-native-style11-source-codes-pixels-bounds-andexact-name-plane-reuse330','exec'),globals())
