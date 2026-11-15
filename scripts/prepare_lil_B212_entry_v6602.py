"""Bind B212 to the clean event table using the exact current snapshot guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B212_entry_tools_v6602')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/prove_lil_B211_entry_v6558.py','scripts/prove_lil_B212_entry_v6602.py',{'B211':'B212','lil_B211_entry_v6558':'lil_B212_entry_v6602','lil_B211_source_v6550c/twelve_clean_current_complete_exchange_source_references.json':'lil_B212_source_v6594b/all14_clean_current_complete_exchange_with_two_three_choices.json','in [211]':'in [212]','current_V6541_native_v6549':'current_V6584_native_v6593'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_entry_producer.json',dict(proof=proof,no_native_numbers_or_guards_changed=True,full_goal_complete=False))
