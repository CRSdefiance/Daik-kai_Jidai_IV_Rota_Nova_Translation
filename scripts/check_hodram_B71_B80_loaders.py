"""Reload the new archive; reuse only unchanged cases from the completed B61-B70 proof."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('scripts/check_pending_scene_loaders.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    'work/analysis/Hodram_B61_B70_stored_20261101/reconstruction.json':
        'work/analysis/Hodram_B71_B80_rebuilt_20261101/reconstruction.json',
    "rebuilt, prior = load(rebuild_path), load(prior_path)":
        """rebuilt, prior = load(rebuild_path), load(prior_path)
    current_modes = load('work/analysis/Hodram_B61_B70_loaders_20261101/verification.json')
    assert current_modes['prior_sha256'] == sha(prior_path.read_bytes())
    prior = {**prior, 'parent_mode_proof': current_modes['modes'],
             'parent_mode_sha256': current_modes['modes_sha256']}""",
    'changed == set(range(61, 71))':'changed == set(range(71, 81))',
})
exec(compile(source,__file__+'::same-native-loader-and-parent-checks','exec'),globals())
