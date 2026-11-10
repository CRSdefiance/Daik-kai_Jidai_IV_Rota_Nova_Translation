"""Refresh archive loads;reuse684 exact modes andexecute two changed B81 modes."""
from scripts import check_rafael330_loaders_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text
parent_adapter=previous.parent_adapter
source=checked_text(previous.source,{
    'Rafael330_stored_consumer_inputs_20261105/native_consumer_reconstruction.json':
        'Rafael330_stored_consumer_inputs_v2_20261105/native_consumer_reconstruction.json',
    'Rafael_B61_B80_loaders_v12_20261104/verification.json':'Rafael330_loaders_20261105/verification.json',
    'changed == {81,82,83,84}':'changed == {81}',
    'len(fresh) == 8 and len(reused) == 678':'len(fresh) == 2 and len(reused) == 684',
    'fresh_parent_cases=8':'fresh_parent_cases=2',
    'exact_reused_parent_cases=678':'exact_reused_parent_cases=684',
    '343 whole native loads/cache hits;eight fresh and678 exact reused parent cases pass.':
        '343 whole native loads/cache hits;two fresh and684 exact reused parent cases pass.',
})
exec(compile(source,__file__+'::same-archive-loader-andtwo-changed-parent-modes','exec'),globals())
