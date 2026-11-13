"""Retain complete303 SC3 loads and606 parent handoffs for the seven-block revision."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/check_maria301_loaders_v1.py').read_text(encoding='utf-8'),{
    'work/Maria_B0_B32_clean_20261109':'work/Maria_B51_B57_clean_20261109',
    "ROOT/'stored_reconstruction_v1/reconstruction.json'":"ROOT/'reconstruction_v1/reconstruction.json'",
    "len(rebuilt['changed_blocks']) == 32":"rebuilt['changed_blocks'] == list(range(51,58))",
    'Maria301-stored-research':'Maria310-stored-research',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-source-owned-SC3-full-load-cache-parent-guards310','exec'),globals())
