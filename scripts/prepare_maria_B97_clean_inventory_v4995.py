"""Return to the uncredited32-record Maria scene with a fresh clean-only inventory."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/maria_B97_inventory_tools_v4995');assert not root.exists()
    tool=derive('scripts/inventory_lil_B183_clean_v4922.py','scripts/inventory_maria_B97_clean_v4995.py',{
        'lil_B183_clean_inventory_v4922':'maria_B97_clean_inventory_v4995','all_clean_B183':'all_clean_B97',
        '/data/SC2.DK4':'/data/SC3.DK4','blocks[183]':'blocks[97]','block=183':'block=97','clean_SC2_sha256':'clean_SC3_sha256',
    })
    root.mkdir(parents=True);save(root/'prepared_tools.json',dict(tool=tool,source_only_no_predecessor_English_read=True,new_review_credit=0,full_goal_complete=False))
