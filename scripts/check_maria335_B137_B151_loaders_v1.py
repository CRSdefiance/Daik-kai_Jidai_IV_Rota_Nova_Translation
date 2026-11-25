"""Check the complete SC3 loader/cache and606 parent handoffs on this15-block rebuild."""
from scripts.check_maria337_loaders_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'work/Maria_B125_B136_clean_20261109':'work/Maria_B137_B151_clean_20261109',
    "ROOT/'reconstruction_v1/reconstruction.json'":"ROOT/'reconstruction_v2/reconstruction.json'",
    'list(range(125,137))':'list(range(137,152))',
    'Maria337-stored-research':'Maria335-B137-B151-stored-research',
})
if __name__=='__main__':exec(compile(source,__file__+'::same303-native-load-cache-and606-parent-handoff-guards','exec'),globals())
