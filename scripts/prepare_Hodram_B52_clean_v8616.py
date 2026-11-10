"""Inventory the next clean source candidate while registered B51 builds; no current English exposure."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_clean_tools_v8616');assert not root.exists()
    result=derive('scripts/inventory_Hodram_B51_clean_v8548.py','scripts/inventory_Hodram_B52_clean_v8616.py',{
        'Hodram_B51_clean_v8548':'Hodram_B52_clean_v8616',
        'editorial_handoff_verification_v8533':'editorial_handoff_verification_v8615',
        "ledger['records_editorially_completed']==7221":"ledger['records_editorially_completed']==7224",
        "verified['profile']=='all-routes-unified-v8475' and verified['Hodram_B49_completed_once']":"verified['profile']=='all-routes-unified-v8543'",
        'len(keys)==7221':'len(keys)==7224',
        'for number in [51]':'for number in [52]',"if g['block']==51:":"if g['block']==52:",
        'complete_clean_SC1_B51_EV1_andcoverage_before_current_English':'complete_clean_SC1_B52_EV1_andcoverage_before_current_English',
        'clean Hodram B51':'clean Hodram B52'})
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,clean_source_only_existing_English_not_opened=True,full_source_command_event_andprior_coverage_inventory_guards_preserved=True,no_ROM_capture_registry_orcredit_change=True,new_credit=0,full_goal_complete=False))
