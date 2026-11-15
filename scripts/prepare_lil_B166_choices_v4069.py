"""Create the separate B166 typed-menu consumer proof without modifying its predecessor."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B166_choice_tools_v4069')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/prove_lil_B164_choices_v3975.py','scripts/prove_lil_B166_choices_v4069.py',{'lil_B164_choices_v3975':'lil_B166_choices_v4069','lil_B164_source_v3960/all49_clean_current_complete_context_with_typed_choice':'lil_B166_source_v4054/all44_clean_current_complete_context_with_typed_choice','lil_B164_choice_manuscript_v1':'lil_B166_choice_manuscript_v1','[(164,1654)]':'[(166,2152)]'})
    ROOT.mkdir(parents=True);save(ROOT/'separate_menu_proof_successor.json',dict(tool=proof,no_ROM_registry_ledger_credit_change=True,full_goal_complete=False));print('Separate B166 typed-menu proof created.')
