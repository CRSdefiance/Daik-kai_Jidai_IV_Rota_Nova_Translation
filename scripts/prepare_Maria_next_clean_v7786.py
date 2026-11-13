"""Freeze source-only inventory ofthe explicitly dependent next Maria event."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/maria_next_clean_tools_v7786');assert not root.exists()
    p=derive('scripts/inventory_Maria_story_clean_v7724.py','scripts/inventory_Maria_next_clean_v7786.py',{
        'maria_story_clean_v7724':'maria_next_clean_v7786',
        'editorial_handoff_verification_v7723':'editorial_handoff_verification_v7785b',
        '==6855':'==6922','for number in [34,35]:':'for number in [36]:',
        'complete_clean_SC3_B34_B35_EV3_andcoverage_before_current_English.json':'complete_clean_SC3_B36_EV3_andcoverage_before_current_English.json',
        "if g['block']==34:":"if g['block']==36:",
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=p,
        original_complete_native_inventory_preamble_terminal_tail_andcoverage_guards_preserved=True,
        source_only_next_event_requires_completed35_not_chosen_by_numeric_adjacency_alone=True,
        no_current_English_orROM_change=True,new_credit=0,full_goal_complete=False))
