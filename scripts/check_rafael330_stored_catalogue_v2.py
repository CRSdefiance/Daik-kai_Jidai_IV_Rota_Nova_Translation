"""Refresh original catalogue selection for all327 current stored bodies."""
from scripts import check_rafael330_stored_catalogue_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous.source,{
    'Rafael330_stored_catalogue_20261105':'Rafael330_stored_catalogue_v2_20261105',
    'Rafael330_stored_native_20261105':'Rafael330_stored_native_v2_20261105',
})
exec(compile(source,__file__+'::same-complete-catalogue-lookup-current-Emilio-paragraph','exec'),globals())
