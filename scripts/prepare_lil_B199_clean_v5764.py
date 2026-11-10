"""Start the next complete Japanese exchange without inheriting B198 assumptions."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B199_clean_tools_v5764')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/inventory_lil_B198_clean_v5700.py','scripts/inventory_lil_B199_clean_v5764.py',{
        'B198':'B199','inventory_v5700':'inventory_v5764','blocks[198]':'blocks[199]','block=198':'block=199'})
    ROOT.mkdir(parents=True);save(ROOT/'generic_clean_inventory_prepared.json',dict(tool=tool,
        no_actor_count_menu_macro_effect_end_item_or_branch_assumptions_inherited=True,
        clean_source_only_prior_English_unread=True,new_review_credit=0,full_goal_complete=False))
