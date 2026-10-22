"""Correct the two occurrences of the release binding in the unexecuted replay body.

V1461 stopped before creating a run because its replacement-count assertion
expected one occurrence;the release is both read and rebound in the adapter.
"""
from pathlib import Path

if __name__=='__main__':
    source = Path('scripts/run_enemy_capture_replay_v1434.py').read_text(encoding='utf-8')
    for old,new,count in [
        ('scripts.native_enemy_capture_fixture_v1433 import apply_fixture,ROM','scripts.native_loss_surrender_fixture_v1460 import apply_fixture,ROM',1),
        ('work/analysis/enemy_capture_release_v1429/registered_release_verification.json','work/analysis/ship_loss_surrender_release_v1455/registered_release_verification.json',2),
        ("'work/analysis/enemy_capture_replay_v1434'","'work/analysis/loss_surrender_control_v1461b'",1),
        ('enemy_capture_v1434_1430','loss_surrender_control_v1461b_1456',1)]:
        assert source.count(old)==count,(old,source.count(old))
        source = source.replace(old,new)
    exec(compile(source,__file__,'exec'),{**globals(),'__name__':'__main__'})
