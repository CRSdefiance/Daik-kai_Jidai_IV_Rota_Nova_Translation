"""Extract the next complete clean Hodram exchange while the registered B50 build runs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B51_clean_tools_v8548');assert not root.exists()
    result=derive('scripts/inventory_Hodram_B50_clean_v8482.py','scripts/inventory_Hodram_B51_clean_v8548.py',{
        'Hodram_B50_clean_v8482':'Hodram_B51_clean_v8548',
        'editorial_handoff_verification_v8481':'editorial_handoff_verification_v8533',
        'for number in [50]':'for number in [51]',
        "if g['block']==50:":"if g['block']==51:",
        'complete_clean_SC1_B50_EV1_andcoverage_before_current_English.json':'complete_clean_SC1_B51_EV1_andcoverage_before_current_English.json',
        'clean Hodram B50':'clean Hodram B51',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,all_native_high_integer_constants_andmultiplicity_preserved=True,clean_only_no_current_English_orROM_revision=True,B50_atomic_release_andown_startup_still_separate_pending=True,no_editorial_orcompletion_credit=True,new_credit=0,full_goal_complete=False))
