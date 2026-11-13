"""Successor selects the source-bound Galley21 rectangle;keeps the first run."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
OLD=Path('scripts/run_cooking_current_v2319.py')
if __name__=='__main__':
 proof=Path('work/analysis/cooking_button_geometry_v2320/source_bound_Galley_touch.json');assert read(proof)['corrected_touch']==[150,154];source=OLD.read_text().replace('cooking_current_run_v2319','cooking_current_run_v2320').replace('cooking_current_v2319_V2284','cooking_current_v2320_V2284');assert source.count('[224,150]')==2;source=source.replace('[224,150]','[150,154]');exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/cooking_current_run_v2320/successor_provenance.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),initial_run_preserved_no_Cook_credit=True,reason='The prior touch224,150 hit native equipment slot29(role24),not Galley21. Current captured31-button geometry binds Galley21 torect130,134,170,174 andtouch150,154.',geometry_proof=str(proof),geometry_proof_sha256=sha(proof.read_bytes()),only_touch_target_changed=True,no_RAM_code_ROM_or_gameplay_fixture_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
