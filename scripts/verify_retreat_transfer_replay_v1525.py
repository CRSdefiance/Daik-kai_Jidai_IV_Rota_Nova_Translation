"""Full original schedule/fixture/save/RAM audit for the V1520 transfer replay."""
from pathlib import Path
from scripts import verify_stronger_fleet_return_v1505 as previous

if __name__ == '__main__':
    source = Path(previous.__file__).read_text(encoding='utf-8')
    for old, new in [
        ('scripts.native_stronger_fleet_current_v1501 import apply_fixture,ROM', 'scripts.native_retreat_transfer_fixture_v1523 import apply_fixture,ROM'),
        ('dk4tool.patch.battle_reaction_editorial import current_entries', 'dk4tool.patch.retreat_transfer_editorial import current_entries'),
        ('work/analysis/battle_reaction_release_v1491/registered_release_verification.json', 'work/analysis/retreat_transfer_release_v1519/registered_release_verification.json'),
        ('work/analysis/stronger_fleet_return_verified_v1505', 'work/analysis/retreat_transfer_control_verified_v1525'),
        ('work/analysis/stronger_fleet_anchor_v1502', 'work/analysis/retreat_transfer_replay_v1524'),
        ('stronger_fleet_anchor_v1502_1492', 'retreat_transfer_v1524_1520'),
        ('scripts/run_stronger_fleet_anchor_v1502.py', 'scripts/run_retreat_transfer_replay_v1524.py'),
    ]:
        assert source.count(old) == 1, (old, source.count(old))
        source = source.replace(old, new)
    exec(compile(source, __file__, 'exec'), {'__name__': '__main__', '__file__': __file__})
