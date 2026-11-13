"""Use a captured pre-final town snapshot for the fifth model control;keep final RGB check."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/verify_shachihoko_expanded_boot_v6099.py','scripts/verify_shachihoko_expanded_boot_v6099b.py',{'else [11900,13400,14900,16400,17401]':'else [11900,13400,14900,16400,17300]'}))
