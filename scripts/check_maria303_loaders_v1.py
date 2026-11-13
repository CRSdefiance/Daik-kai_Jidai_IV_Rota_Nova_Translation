"""Reuse unchanged native whole-SC3 load/cache/parent guards on the exact ten-block reconstruction."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/check_maria301_loaders_v1.py').read_text(encoding='utf-8'),{
    'work/Maria_B0_B32_clean_20261109':'work/Maria_B58_B70_clean_20261109',
    "ROOT/'stored_reconstruction_v1/reconstruction.json'":"ROOT/'reconstruction_v2/reconstruction.json'",
    "len(rebuilt['changed_blocks']) == 32":"rebuilt['changed_blocks'] == [58,59,60,61,62,64,65,66,68,70]",
    'Maria301-stored-research':'Maria303-stored-research',
})
if __name__=='__main__':exec(compile(source,__file__+'::same303-loads606-handoffs-complete-current-SC3','exec'),globals())
