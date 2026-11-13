"""Check current SC3 archive loads/handoffs with the original complete native loader."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/check_maria301_loaders_v1.py').read_text(encoding='utf-8'),{
    'work/Maria_B0_B32_clean_20261109':'work/Maria_B37_B50_clean_20261109',
    "OUT = ROOT/'loaders_v1'":"OUT = ROOT/'loaders270_v1'",
    "ROOT/'stored_reconstruction_v1/reconstruction.json'":"ROOT/'stored270_reconstruction_v1/reconstruction.json'",
    "len(rebuilt['changed_blocks']) == 32":"len(rebuilt['changed_blocks']) == 13",
    'Maria301-stored-research':'Maria270-stored-research-with-registered-market-fix',
})
exec(compile(source,__file__+'::same-full-native-SC3-load-cache-parent-guards-current13-block-transaction','exec'),globals())
