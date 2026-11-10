"""Reload the new archive and reuse exact tutorial-parent handoff cases."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.check_rafael_early_tutorial_loaders import source as previous,parent_adapter

source=checked_text(previous,{
    'work/analysis/Rafael_early_tutorial_B42_B43_storage_20261104/reconstruction_v2/reconstruction.json':
        'work/analysis/Rafael_B36_B41_rebuilt_20261104/reconstruction.json',
    "    modes_path = Path(prior['parent_mode_proof'])":
        "    latest_path=Path('work/analysis/Rafael_early_tutorial_B42_B43_loaders_20261104/verification.json')\n    latest=load(latest_path)\n    modes_path=Path(latest['modes'])",
    "sha(modes_path.read_bytes()) == prior['parent_mode_sha256']":
        "sha(modes_path.read_bytes()) == latest['modes_sha256']",
    'changed == {42,43}':'changed == set(range(36,42))',
    "'pending-Rafael-tutorial-research'":"'pending-Rafael-B36-B41-research'",
    'len(fresh) == 4 and len(reused) == 682':'len(fresh) == 12 and len(reused) == 674',
    'fresh_whole_archive_loads_andcache_hits=343, fresh_parent_cases=4,':
        'fresh_whole_archive_loads_andcache_hits=343, fresh_parent_cases=12,',
    'exact_reused_parent_cases=682, original_EV0_action_count=344,':
        'exact_reused_parent_cases=674, original_EV0_action_count=344,',
    "        prior=str(prior_path), prior_sha256=sha(prior_path.read_bytes()),":
        "        prior=str(prior_path), prior_sha256=sha(prior_path.read_bytes()),\n        latest_tutorial_parent_proof=str(latest_path),latest_tutorial_parent_sha256=sha(latest_path.read_bytes()),\n        exact_reused_parent_modes=str(modes_path),exact_reused_parent_modes_sha256=sha(modes_path.read_bytes()),",
    '343 whole native loads/cache hits;4 fresh and682 exact reused parent cases pass.':
        '343 whole native loads/cache hits;12 fresh and674 exact reused parent cases pass.',
})
exec(compile(source,__file__+'::same-native-SC0-loaders-with-exact-latest-parent-mode-reuse','exec'),globals())
