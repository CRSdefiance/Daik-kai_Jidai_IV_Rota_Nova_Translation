"""Original full encounter/reward/return control on registered V1492."""
from pathlib import Path

if __name__=='__main__':
    source=Path('scripts/run_enemy_capture_replay_v1434.py').read_text(encoding='utf-8')
    for old,new,count in [
        ('scripts.native_enemy_capture_fixture_v1433 import apply_fixture,ROM','scripts.native_battle_reaction_control_v1496 import apply_fixture,ROM',1),
        ('work/analysis/enemy_capture_release_v1429/registered_release_verification.json','work/analysis/battle_reaction_release_v1491/registered_release_verification.json',2),
        ("'work/analysis/enemy_capture_replay_v1434'","'work/analysis/battle_reaction_control_v1497'",1),
        ('enemy_capture_v1434_1430','battle_reaction_control_v1497_1492',1)]:
        assert source.count(old)==count,(old,source.count(old))
        source=source.replace(old,new)
    exec(compile(source,__file__,'exec'),{**globals(),'__name__':'__main__'})
