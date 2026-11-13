"""Reuse the additional identical Shopkeeper plane;getters anddistinct text caches have different counts."""
from scripts import check_rafael_B81_B84_scoped_name_planes_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    'Rafael_B81_B84_progressive_name_planes_20261105':'Rafael_B81_B84_progressive_name_planes_v2_20261105',
    '(fresh,reused)==(7,9)':'(fresh,reused)==(6,10)',
})
exec(compile(source,__file__+'::same-native-guards-six-fresh-ten-exact-text-cache-reuses','exec'),globals())
