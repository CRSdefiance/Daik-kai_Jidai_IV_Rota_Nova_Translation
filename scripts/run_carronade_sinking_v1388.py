"""Cold original encounter with one declared original Carronade loadout."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read


if __name__=='__main__':
    path = Path('scripts/run_ship_sinking_loadout_v1379.py')
    assert sha(path.read_bytes())==read('work/analysis/ship_sinking_loadout_v1379/run_plan.json')['runner_sha256']
    source = path.read_text(encoding='utf-8')
    for old,new in [
        ('from scripts.native_ship_cannon_fixture_v1378 import apply_fixture','from scripts.native_carronade_fixture_v1387 import apply_fixture'),
        ("'ROOT':Path('work/analysis/ship_sinking_loadout_v1379')","'ROOT':Path('work/analysis/carronade_sinking_v1388')"),
        ('ship_sinking_loadout_v1379_1364','carronade_sinking_v1388_1364'),
        ('<=9100','<=9000'),('==9100','==9000')]:
        assert source.count(old)==1,old
        source = source.replace(old,new)
    exec(compile(source,__file__,'exec'),{**globals(),'__name__':'__main__'})
