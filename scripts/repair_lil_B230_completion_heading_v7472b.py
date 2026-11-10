"""Correct an inspected, unexecuted copied heading before staging any completion targets."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B230_completion_heading_v7472b')
if __name__=='__main__':
    assert not ROOT.exists() and not Path('work/analysis/lil_B230_completion_v7472').exists();row=derive('scripts/complete_lil_B230_v7472.py','scripts/complete_lil_B230_v7472b.py',{'V7424':'V7472'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_preexecution_heading_repair.json',dict(tool=row,original_unexecuted_producer_preserved=True,only_copied_handoff_andconsole_heading_corrected=True,no_dialogue_runtime_counter_orcredit_change=True,new_credit=0,full_goal_complete=False))
