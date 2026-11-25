"""Reload343 blocks; only the revised B69 needs fresh parent modes."""
from scripts.check_rafael_B61_B80_loaders import source as previous,parent_adapter
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'Rafael_B61_B80_rebuilt_20261104/reconstruction.json':'Rafael_B61_B80_rebuilt_v12_20261104/reconstruction.json',
    'Rafael_B51_B60_loaders_20261104/verification.json':'Rafael_B61_B80_loaders_20261104/verification.json',
    'changed == set(range(61,81))-{68}':'changed == {69}',
    'len(fresh) == 38 and len(reused) == 648':'len(fresh) == 2 and len(reused) == 684',
    'fresh_parent_cases=38':'fresh_parent_cases=2',
    'exact_reused_parent_cases=648':'exact_reused_parent_cases=684',
    '343 whole native loads/cache hits;38 fresh and648 exact reused parent cases pass.':'343 whole native loads/cache hits;2 fresh and684 exact reused parent cases pass.',
})
exec(compile(source,__file__+'::same-archive-loaders-one-revised-block','exec'),globals())
