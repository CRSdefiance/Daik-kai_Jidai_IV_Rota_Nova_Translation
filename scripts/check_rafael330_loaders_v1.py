"""Reload343 native blocks;refresh eight changed parent cases and reuse678 exact cases."""
from scripts.check_rafael_B61_B80_loaders_v12 import source as previous,parent_adapter
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'Rafael_B61_B80_rebuilt_v12_20261104/reconstruction.json':'Rafael330_stored_consumer_inputs_20261105/native_consumer_reconstruction.json',
    'Rafael_B61_B80_loaders_20261104/verification.json':'Rafael_B61_B80_loaders_v12_20261104/verification.json',
    'changed == {69}':'changed == {81,82,83,84}',
    'pending-Rafael-B61-B80-research':'pending-Rafael330-research',
    'len(fresh) == 2 and len(reused) == 684':'len(fresh) == 8 and len(reused) == 678',
    'fresh_parent_cases=2':'fresh_parent_cases=8',
    'exact_reused_parent_cases=684':'exact_reused_parent_cases=678',
    '343 whole native loads/cache hits;2 fresh and684 exact reused parent cases pass.':
        '343 whole native loads/cache hits;eight fresh and678 exact reused parent cases pass.',
})
exec(compile(source,__file__+'::same-native-load-andparent-guards-four-changed-blocks-with-FE-children','exec'),globals())
