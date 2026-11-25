"""Reload all343 blocks andrefresh20 changed parent modes;reuse666 exact cases."""
from scripts.check_rafael_B36_B41_loaders import source as previous,parent_adapter
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'Rafael_B36_B41_rebuilt_20261104/reconstruction.json':'Rafael_B51_B60_rebuilt_20261104/reconstruction.json',
    'Rafael_early_tutorial_B42_B43_loaders_20261104/verification.json':'Rafael_B36_B41_loaders_20261104/verification.json',
    'changed == set(range(36,42))':'changed == set(range(51,61))',
    'pending-Rafael-B36-B41-research':'pending-Rafael-B51-B60-research',
    'len(fresh) == 12 and len(reused) == 674':'len(fresh) == 20 and len(reused) == 666',
    'fresh_whole_archive_loads_andcache_hits=343, fresh_parent_cases=12,':'fresh_whole_archive_loads_andcache_hits=343, fresh_parent_cases=20,',
    'exact_reused_parent_cases=674':'exact_reused_parent_cases=666',
    '343 whole native loads/cache hits;12 fresh and674 exact reused parent cases pass.':'343 whole native loads/cache hits;20 fresh and666 exact reused parent cases pass.',
    'latest_tutorial_parent_proof':'latest_Rafael_parent_proof',
    'latest_tutorial_parent_sha256':'latest_Rafael_parent_sha256',
})
exec(compile(source,__file__+'::same-native-source-word-checks-new-ten-block-archive-andchanged-parent-modes','exec'),globals())
