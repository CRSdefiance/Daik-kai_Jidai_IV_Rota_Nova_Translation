"""Prepare fresh whole-archive loader/parent modes and fourteen-command reference census."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B211_loader_census_tools_v6570')
if __name__=='__main__':
    assert not ROOT.exists();proofs=[]
    proofs.append(derive('scripts/verify_lil_B210_loader_v6524.py','scripts/verify_lil_B211_loader_v6570.py',{'B210':'B211','loader_v6524':'loader_v6570','reference_v6515':'reference_v6566','V6488':'V6541'}))
    proofs.append(derive('scripts/verify_lil_B210_references_v6525.py','scripts/verify_lil_B211_references_v6571.py',{'B210':'B211','reference_census_v6525':'reference_census_v6571','loader_v6524':'loader_v6570','reference_v6515':'reference_v6566','[210]':'[211]','==12':'==14','all12_commands':'all14_commands','all12_clean_current_target':'all14_clean_current_target','native_commands_each=12':'native_commands_each=14','12-command':'14-command'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(proofs=proofs,source14_commands12_speeches_three_FE_one_FI_A000_and_end=True,whole336_blocks_two_parent_modes_and_three_shipped_censuses_required=True,all_native_constants_and_unmodified_loader_instructions_preserved=True,full_goal_complete=False))
