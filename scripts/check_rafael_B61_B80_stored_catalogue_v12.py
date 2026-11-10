"""Bind every current final body to the unchanged original pre-macro lookup."""
from scripts.check_rafael_B61_B80_stored_catalogue import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'Rafael_B61_B80_stored_catalogue_20261104':'Rafael_B61_B80_stored_catalogue_v12_20261104',
    'Rafael_B61_B80_stored_native_v2_20261104':'Rafael_B61_B80_stored_native_v12_20261104',
})
exec(compile(source,__file__+'::same-catalogue-lookup-revised-reassurance-body','exec'),globals())
