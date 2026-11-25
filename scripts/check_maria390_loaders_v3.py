"""Run the complete native archive/cache checks on the amended wine archive."""
from scripts.check_maria390_loaders_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{"ROOT/'reconstruction_v2/reconstruction.json'":"ROOT/'reconstruction_v3/reconstruction.json'",
    "OUT = ROOT/'loaders_v2'":"OUT = ROOT/'loaders_v3'"})
if __name__=='__main__':exec(compile(source,__file__+'::same303-loads-and606-handoffs-wine-amended-archive','exec'),globals())
