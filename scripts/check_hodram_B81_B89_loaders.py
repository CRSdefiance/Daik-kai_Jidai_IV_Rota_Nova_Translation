"""Fresh archive loads with exact unchanged B71-B80 parent-case reuse."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('scripts/check_pending_scene_loaders.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    'work/analysis/Hodram_B61_B70_stored_20261101/reconstruction.json':
        'work/analysis/Hodram_B81_B89_rebuild_20261101/reconstruction.json',
    '    rebuilt, prior = load(rebuild_path), load(prior_path)':
    """    rebuilt, prior = load(rebuild_path), load(prior_path)
    current_modes_path=Path('work/analysis/Hodram_B71_B80_loaders_20261101/verification.json')
    current_modes=load(current_modes_path)
    assert current_modes['prior_sha256']==sha(prior_path.read_bytes())
    prior={**prior,'parent_mode_proof':current_modes['modes'],'parent_mode_sha256':current_modes['modes_sha256']}""",
    'changed == set(range(61, 71))':'changed == set(range(81, 90))',
    'len(fresh) == 20 and len(reused) == 630':'len(fresh) == 18 and len(reused) == 632',
    'fresh_parent_cases=20':'fresh_parent_cases=18',
    'exact_reused_parent_cases=630':'exact_reused_parent_cases=632',
    '325 whole native loads/cache hits;20 fresh and630 exact reused parent cases pass.':
        '325 whole native loads/cache hits;18 fresh and632 exact reused parent cases pass.',
})
exec(compile(source,__file__+'::new-nine-blocks-exact-parent-reuse','exec'),globals())
