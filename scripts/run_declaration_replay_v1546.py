"""Replay the full original declaration/battle/defeat/retreat journal on V1542."""
from pathlib import Path
from scripts import run_retreat_transfer_replay_v1524 as previous

if __name__ == '__main__':
    source = Path(previous.__file__).read_text(encoding='utf-8')
    for old, new in [
        ('scripts.native_retreat_transfer_fixture_v1523 import apply_fixture, ROM', 'scripts.native_declaration_fixture_v1545 import apply_fixture, ROM'),
        ('work/analysis/retreat_transfer_release_v1519/registered_release_verification.json', 'work/analysis/declaration_responses_release_v1541/registered_release_verification.json'),
        ('work/analysis/retreat_transfer_replay_v1524', 'work/analysis/declaration_responses_replay_v1546'),
        ('retreat_transfer_v1524_1520', 'declaration_responses_v1546_1542')]:
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    exec(compile(source, __file__, 'exec'), {'__name__': '__main__', '__file__': __file__})
