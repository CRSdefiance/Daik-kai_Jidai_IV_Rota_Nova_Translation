"""Check every327 stored command through the original pre-macro catalogue lookup."""
from scripts import check_rafael_B61_B80_stored_catalogue_v12 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    'Rafael_B61_B80_stored_catalogue_v12_20261104':'Rafael330_stored_catalogue_20261105',
    'Rafael_B61_B80_stored_native_v12_20261104':'Rafael330_stored_native_20261105',
    'work/analysis/Rafael_B61_B80_latest_runtime_20261104/all539_current_effective_qualified_v1.json':
        'work/analysis/Rafael_B81_B84_current_20261105/current_effective.json',
    'len(rows)==539':'len(rows)==327',
    'all539_stored_effective_body_bindings.json':'all327_stored_effective_body_bindings.json',
    '539 stored bodies survive original catalogue lookup byte forbyte;no old wording,glyphs orwraps are restored.':
        '327 stored native speech commands survive original catalogue lookup byte forbyte;FE children are not extra source credits.',
})
exec(compile(source,__file__+'::same-native-premacro-full-buffer-SP-andinput-canaries-all327-commands','exec'),globals())
