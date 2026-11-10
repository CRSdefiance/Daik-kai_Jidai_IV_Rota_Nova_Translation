"""Reload343 blocks; refresh38 changed parent modes and reuse648 exact cases."""
from scripts.check_rafael_B51_B60_loaders import source as previous,parent_adapter
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'Rafael_B51_B60_rebuilt_20261104/reconstruction.json':'Rafael_B61_B80_rebuilt_20261104/reconstruction.json',
    'Rafael_B36_B41_loaders_20261104/verification.json':'Rafael_B51_B60_loaders_20261104/verification.json',
    'changed == set(range(51,61))':'changed == set(range(61,81))-{68}',
    'pending-Rafael-B51-B60-research':'pending-Rafael-B61-B80-research',
    'len(fresh) == 20 and len(reused) == 666':'len(fresh) == 38 and len(reused) == 648',
    'fresh_whole_archive_loads_andcache_hits=343, fresh_parent_cases=20,':'fresh_whole_archive_loads_andcache_hits=343, fresh_parent_cases=38,',
    'exact_reused_parent_cases=666':'exact_reused_parent_cases=648',
    '343 whole native loads/cache hits;20 fresh and666 exact reused parent cases pass.':'343 whole native loads/cache hits;38 fresh and648 exact reused parent cases pass.',
})
exec(compile(source,__file__+'::same-native-source-word-guards-19-changed-blocks','exec'),globals())
