"""Continue clean-first editorial coverage while the registered cumulative build runs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B53_clean_tools_v8711');assert not root.exists()
    receipt=derive('scripts/inventory_Hodram_B52_clean_v8616.py','scripts/inventory_Hodram_B53_clean_v8711.py',{
        'Hodram B52':'Hodram B53','Hodram_B52_clean_v8616':'Hodram_B53_clean_v8711',
        'verification_v8615':'verification_v8710','7224':'7229','all-routes-unified-v8543':'all-routes-unified-v8609',
        'for number in [52]':'for number in [53]','complete_clean_SC1_B52_EV1':'complete_clean_SC1_B53_EV1',
        "g['block']==52":"g['block']==53",
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=receipt,
         source_only_complete_exchange_andoriginal_EV1_context_no_current_English=True,
         current_registered_B52_build_remains_separate_no_replay_orcredit=True))
