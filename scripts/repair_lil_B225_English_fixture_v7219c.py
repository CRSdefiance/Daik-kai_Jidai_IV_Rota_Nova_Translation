"""Bind the actual inherited filename from the initial receipt;preserve both stopped preparations."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B225_English_fixture_repair_v7219c')
if __name__=='__main__':
    receipt=Path('work/analysis/lil_B225_English_fixture_v7203/complete_B225_English_B22_fixture.json');f=read(receipt)['fixtures'][0];old=Path(f['research_ROM']);new=Path('out/lil_B225_English_v7219_reviewed_English_RESEARCH_ONLY.nds')
    assert not ROOT.exists() and sha(old.read_bytes())==f['research_ROM_sha256'] and old.name=='lil_B225_English_v7154_reviewed_English_RESEARCH_ONLY.nds' and not new.exists() and not Path('work/analysis/lil_B225_English_fixture_v7219').exists() and not Path('scripts/run_lil_B225_English_v7220.py').exists()
    target='scripts/research_lil_B225_English_fixture_v7219c.py';assert not Path(target).exists();r=derive('scripts/research_lil_B225_English_fixture_v7219.py',target,{'English_v7154_reviewed_English':'English_v7219_reviewed_English'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_receipt_bound_ROM_filename.json',dict(tool=r,initial_fixture_receipt=str(receipt),initial_fixture_receipt_sha256=sha(receipt.read_bytes()),original_ROM=str(old),original_ROM_sha256=sha(old.read_bytes()),preflight_stops7219_and7219b_preserved=True,no_ROM_written_or_overwritten_by_either_stop=True,new_credit=0))
