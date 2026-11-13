"""Rerun the complete archive/parent proofs against the corrected exact target."""
from scripts.check_maria310_loaders_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{"ROOT/'loaders_v1'":"ROOT/'loaders_v2'","ROOT/'reconstruction_v1/reconstruction.json'":"ROOT/'reconstruction_v2/reconstruction.json'"})
if __name__=='__main__':exec(compile(source,__file__+'::same303-loads606-handoffs-corrected-target','exec'),globals())
