"""Keep complete SC3 loader/cache and parent-handoff checks for the12-block rebuild."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/check_maria301_loaders_v1.py').read_text(encoding='utf-8'),{
    'work/Maria_B0_B32_clean_20261109':'work/Maria_B125_B136_clean_20261109',
    "ROOT/'stored_reconstruction_v1/reconstruction.json'":"ROOT/'reconstruction_v1/reconstruction.json'",
    "len(rebuilt['changed_blocks']) == 32":"rebuilt['changed_blocks'] == list(range(125,137))",
    'Maria301-stored-research':'Maria337-stored-research',
})
if __name__=='__main__':exec(compile(source,__file__+'::same303-native-load-cache-and606-parent-handoff-guards','exec'),globals())
