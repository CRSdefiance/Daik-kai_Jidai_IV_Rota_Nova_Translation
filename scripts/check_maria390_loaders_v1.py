"""Check the full SC3 loader/cache and606 native parent handoffs on24 changed blocks."""
from scripts.check_maria337_loaders_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'work/Maria_B125_B136_clean_20261109':'work/Maria_B152_B175_clean_20261109',
    'list(range(125,137))':'list(range(152,176))',
    'Maria337-stored-research':'Maria390-stored-research',
})
if __name__=='__main__':exec(compile(source,__file__+'::same303-whole-archive-load-cache-and606-handoff-guards','exec'),globals())
