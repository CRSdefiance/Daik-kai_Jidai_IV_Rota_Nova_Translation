"""Recheck the actual amended archive through the qualified full loader/handoff guards."""
from scripts.check_maria390_loaders_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{"ROOT/'reconstruction_v1/reconstruction.json'":"ROOT/'reconstruction_v2/reconstruction.json'",
    "OUT = ROOT/'loaders_v1'":"OUT = ROOT/'loaders_v2'"})
if __name__=='__main__':exec(compile(source,__file__+'::same303-loads-and606-handoffs-amended-archive','exec'),globals())
