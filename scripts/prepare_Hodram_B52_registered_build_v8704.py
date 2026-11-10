"""Prepare sole-builder and regression wrappers for the registered cumulative profile."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_registered_tools_v8704');assert not root.exists()
    receipts=[]
    receipts.append(derive('scripts/build_Hodram_B51_v8609.py','scripts/build_Hodram_B52_v8704.py',{
        'Hodram_B51':'Hodram_B52','v8609':'v8704','v8608':'v8703',
    }))
    receipts.append(derive('scripts/run_Hodram_B51_regressions_v8609.py','scripts/run_Hodram_B52_regressions_v8704.py',{
        'Hodram_B51':'Hodram_B52','v8609':'v8704',
    }))
    root.mkdir(parents=True);save(root/'derivations.json',receipts)
