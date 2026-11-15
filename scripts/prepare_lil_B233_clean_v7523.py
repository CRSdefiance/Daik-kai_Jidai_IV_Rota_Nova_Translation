"""Preserve the empty B232 finding and inventory the following clean block."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B233_clean_tools_v7523')
if __name__=='__main__':
    assert not ROOT.exists();empty=Path('work/analysis/lil_B232_clean_inventory_v7522/all_clean_B232_speeches_before_predecessor_comparison.json');e=read(empty)
    assert e['physical_speech_objects']==0 and e['clean_stored_bytes']==12 and len(e['commands'])==1 and e['read_no_predecessor_English']
    row=derive('scripts/inventory_lil_B232_clean_v7522.py','scripts/inventory_lil_B233_clean_v7523.py',{'B232':'B233','v7522':'v7523','blocks[232]':'blocks[233]','block=232':'block=233'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_next_clean_inventory.json',dict(tool=row,preceding_B232_inventory=str(empty),preceding_B232_inventory_sha256=sha(empty.read_bytes()),B232_zero_speeches_no_dialogue_credit=True,read_no_predecessor_English=True,new_credit=0,full_goal_complete=False))
