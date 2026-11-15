"""Preserve the registered candidate and exact reconstruction with all earlier pins."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B204_retention_tools_v6164')
if __name__=='__main__':
    assert not ROOT.exists();tool=derive('scripts/pin_lil_B203_v6054.py','scripts/pin_lil_B204_v6164.py',{'B203':'B204','retention_v6054':'retention_v6164','release_v6051':'release_v6161','V6050':'V6160'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_pin_tool.json',dict(tool=tool,preserve_every_prior_ROM_and_pin=True,full_goal_complete=False));print('V6160/reconstruction retention tool prepared;no pruning.')
