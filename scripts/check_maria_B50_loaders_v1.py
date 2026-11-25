"""Keep the complete original SC3 loader and handoff proof for the FE-paginated archive."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/check_maria301_loaders_v1.py').read_text(encoding='utf-8'),{
    'work/Maria_B0_B32_clean_20261109':'work/Maria_B50_FE_resolution_20261109_v3',
    "ROOT/'stored_reconstruction_v1/reconstruction.json'":"ROOT/'reconstruction_v1/reconstruction.json'",
    "len(rebuilt['changed_blocks']) == 32":"rebuilt['changed_blocks'] == [50]",
    'Maria301-stored-research':'Maria-B50-source-owned-FE-continuation-research',
})
exec(compile(source,__file__+'::same-full-SC3-native-load-cache-andparent-guards-one-owned-block','exec'),globals())
