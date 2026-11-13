"""Remove a nonexistent historical heading key before any package was created."""
from scripts.source_locked_derivation_v5118 import derive

if __name__=='__main__':
    print(derive('scripts/prepare_lil_B194_package_v5538.py','scripts/prepare_lil_B194_package_v5538c.py',{
        ",'V5437':'V5478'":'',
    }))
