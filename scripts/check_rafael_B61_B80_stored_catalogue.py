"""Check all539 stored bodies using unchanged native pre-macro catalogue lookup."""
from scripts.check_rafael_B51_B60_stored_catalogue import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'Rafael_B51_B60_stored_catalogue_20261104':'Rafael_B61_B80_stored_catalogue_20261104',
    'Rafael_B51_B60_stored_native_20261104':'Rafael_B61_B80_stored_native_v2_20261104',
    'Rafael_B51_B60_current_runtime_20261104/current_effective.json':'Rafael_B61_B80_latest_runtime_20261104/all539_current_effective_qualified_v1.json',
    'len(rows)==245':'len(rows)==539',
    'all245_stored_effective_body_bindings.json':'all539_stored_effective_body_bindings.json',
    '245 stored bodies survive original catalogue lookup byte forbyte;no old wording,glyphs orwraps are restored.':
        '539 stored bodies survive original catalogue lookup byte forbyte;no old wording,glyphs orwraps are restored.',
})
exec(compile(source,__file__+'::same-guarded-pre-macro-lookup-all539','exec'),globals())
