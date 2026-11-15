"""Bind the unchanged six leaves to the actual current V6110 snapshot."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B204_current_control_tools_v6139')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/prove_lil_B204_controls_v6069.py','scripts/prove_lil_B204_controls_v6139.py',{'scripts.current_build_native_context_v4774':'scripts.current_build_native_context_v6097','lil_B204_controls_v6069':'lil_B204_controls_v6139','work/analysis/lil_B204_source_v6062/all20_clean_current_complete_context.json':'work/analysis/lil_B204_current_v6118/all20_clean_current_complete_context.json','work/analysis/lil_B204_voices_v6063/current_native_input.json':'work/analysis/lil_B204_current_v6118/current_native_input.json'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',dict(tool=tool,all_native_addresses_source_leaves_picture_descriptor_and_end_checks_preserved=True,full_goal_complete=False));print('Fresh current six-leaf/picture/end verifier prepared;no native addresses or source data changed.')
