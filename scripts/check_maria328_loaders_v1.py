"""Keep whole-SC3 native load/cache/parent guards for the21-block research transaction."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/check_maria301_loaders_v1.py').read_text(encoding='utf-8'),{
    'work/Maria_B0_B32_clean_20261109':'work/Maria_B73_B95_clean_20261109',
    "ROOT/'stored_reconstruction_v1/reconstruction.json'":"ROOT/'reconstruction_v1/reconstruction.json'",
    "len(rebuilt['changed_blocks']) == 32":"rebuilt['changed_blocks'] == [73,74,75,76,77,78,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95]",
    'Maria301-stored-research':'Maria328-stored-research',
})
if __name__=='__main__':exec(compile(source,__file__+'::same303-loads606-parent-handoffs-fresh-complete-SC3','exec'),globals())
