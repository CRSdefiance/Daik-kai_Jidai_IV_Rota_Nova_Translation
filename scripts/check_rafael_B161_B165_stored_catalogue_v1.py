"""Reuse the exact full-buffer native catalogue check on the 67 new speeches."""
from scripts.check_rafael_B177_B180_stored_catalogue_v1 import source as previous,TEMPLATE
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'Rafael_B177_B180_stored_catalogue_v1_20261105':'Rafael_B161_B165_stored_catalogue_v1_20261105',
    'Rafael_B177_B180_stored_v1_20261105':'Rafael_B161_B165_stored_v1_20261105',
    'Rafael_B177_B180_current1424_20261105':'Rafael_B161_B165_current1607_20261105',
    'len(rows)==175':'len(rows)==67',
    'all175_stored_effective_body_bindings.json':'all67_stored_effective_body_bindings.json',
    '175 stored tutorial bodies pass':'67 stored story bodies pass',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-catalogue-check-for-67-stored-bodies','exec'),globals())
