"""Keep the four-section probe failure and bind its exact five-section coverage successor."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/verify_shachihoko_expanded_boot_v6099b.py','scripts/verify_shachihoko_expanded_boot_v6099c.py',{
        'from scripts.probe_persistent_name_arm7_boot_overlap import execute as boot':'from scripts.expanded_pool_boot_probe_v6100 import execute as boot',
        'evidence=[RECEIPT,Path(__file__)]':"evidence=[RECEIPT,Path(__file__),Path('scripts/expanded_pool_boot_probe_v6100.py'),Path('scripts/probe_persistent_name_arm7_boot_overlap.py')]",
    }))
