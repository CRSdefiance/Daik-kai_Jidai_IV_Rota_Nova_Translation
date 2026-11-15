"""Prepare a source-locked retention tool without changing existing pins."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B221_pin_tools_v7013')
if __name__=='__main__':
    assert not ROOT.exists()
    row=derive('scripts/pin_lil_B220_v6958.py','scripts/pin_lil_B221_v7013.py',{'B220':'B221','retention_v6958':'retention_v7013','release_v6957':'release_v7012','V6956':'V7011'})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tool.json',row)
