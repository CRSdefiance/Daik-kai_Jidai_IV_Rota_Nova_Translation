"""Replay the entire audited original battle/defeat/transfer journal on V1520."""
import inspect
from pathlib import Path
from scripts import run_ship_sinking_live_v1350 as previous
from scripts.native_retreat_transfer_fixture_v1523 import apply_fixture, ROM
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read

if __name__ == '__main__':
    release_path = 'work/analysis/retreat_transfer_release_v1519/registered_release_verification.json'
    release = read(release_path)
    prior = Path('work/analysis/stronger_fleet_anchor_v1502/navigation.jsonl')
    terminal = read(prior.parent / 'terminal_preservation.json')
    assert sha(prior.read_bytes()) == terminal['navigation_sha256']
    prefix = prior.read_text(encoding='utf-8')
    assert prefix.splitlines()[-1] == '{"stop": true}'
    source = inspect.getsource(previous.main)
    for old, new in [
        ('work/analysis/ship_sinking_release_v1343/registered_release_verification.json', release_path),
        ('9d455782724d98198b7bc3fdac7be755945e58d406e66a4634094d9a0eab301b', release['candidate_sha256']),
        ("journal.write_text('',encoding='utf-8')", 'journal.write_text(' + repr(prefix) + ",encoding='utf-8')")]:
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    env = {**previous.__dict__, '__file__': __file__, 'ROM': ROM, 'fixture': apply_fixture,
        'ROOT': Path('work/analysis/retreat_transfer_replay_v1524'),
        'CAP': Path('E:/Rota Nova translations/Generated/work/emulation_v193/retreat_transfer_v1524_1520')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
