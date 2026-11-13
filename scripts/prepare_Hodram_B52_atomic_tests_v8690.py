"""Derive complete atomic and genuinely wrong-memory B52 lifecycle tests."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_atomic_tools_v8690');assert not root.exists()
    receipts=[]
    receipts.append(derive('scripts/validate_Hodram_B51_atomic_v8604.py','scripts/validate_Hodram_B52_atomic_v8690.py',{
        'B51':'B52','hodram_B51_editorial_v1':'hodram_B52_editorial_v1',
        'Hodram_B51_release_paths_v8595':'Hodram_B52_release_paths_v8688',
        'Hodram_B51_atomic_positive_v8604':'Hodram_B52_atomic_positive_v8690',
    }))
    receipts.append(derive('scripts/validate_Hodram_B51_wrong_memory_v8605.py','scripts/validate_Hodram_B52_wrong_memory_v8691.py',{
        'B51':'B52','hodram_B51_editorial_v1':'hodram_B52_editorial_v1',
        'Hodram_B51_release_paths_v8595':'Hodram_B52_release_paths_v8688',
        'Hodram_B51_wrong_memory_v8605':'Hodram_B52_wrong_memory_v8691',
    }))
    root.mkdir(parents=True);save(root/'derivations.json',receipts)
