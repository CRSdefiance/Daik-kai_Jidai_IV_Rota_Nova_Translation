"""Complete original9200-frame input/fixture/save/RAM and battle-return audit."""
from pathlib import Path
from scripts import verify_stronger_fleet_return_v1505 as previous

if __name__ == '__main__':
    source = Path(previous.__file__).read_text(encoding='utf-8')
    for old, new in [
        ('scripts.native_stronger_fleet_current_v1501 import apply_fixture,ROM', 'scripts.native_declaration_fixture_v1545 import apply_fixture,ROM'),
        ('dk4tool.patch.battle_reaction_editorial import current_entries', 'dk4tool.patch.declaration_responses_editorial import current_entries'),
        ('work/analysis/battle_reaction_release_v1491/registered_release_verification.json', 'work/analysis/declaration_responses_release_v1541/registered_release_verification.json'),
        ('work/analysis/stronger_fleet_return_verified_v1505', 'work/analysis/declaration_responses_control_verified_v1547'),
        ('work/analysis/stronger_fleet_anchor_v1502', 'work/analysis/declaration_responses_replay_v1546'),
        ('stronger_fleet_anchor_v1502_1492', 'declaration_responses_v1546_1542'),
        ('scripts/run_stronger_fleet_anchor_v1502.py', 'scripts/run_declaration_replay_v1546.py')]:
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    exec(compile(source, __file__, 'exec'), {'__name__': '__main__', '__file__': __file__})
