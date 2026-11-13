"""Cold-boot pilot of original loading after one declared existing-fleet activation."""
import inspect
import json
from pathlib import Path
from scripts import run_ship_sinking_live_v1350 as previous
from scripts.native_sea_registration_fixture_v1552g import apply_fixture, ROM
from scripts.verify_village_wrap_v608 import read

if __name__ == '__main__':
    release_path = 'work/analysis/declaration_responses_release_v1541/registered_release_verification.json'
    release = read(release_path)
    commands = [{'until': 4900, 'duration': 1, 'battle_fixture': {'sea_inspection_context': 'register_original_Monster_Fish'}}, {'until': 5000, 'buttons': ['A'], 'duration': 4}, {'until': 5100, 'duration': 1}]
    prefix = ''.join(json.dumps(r) + '\n' for r in commands)
    source = inspect.getsource(previous.main)
    for old, new in [
        ('work/analysis/ship_sinking_release_v1343/registered_release_verification.json', release_path),
        ('9d455782724d98198b7bc3fdac7be755945e58d406e66a4634094d9a0eab301b', release['candidate_sha256']),
        ("journal.write_text('',encoding='utf-8')", 'journal.write_text(' + repr(prefix) + ",encoding='utf-8')")]:
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    env = {**previous.__dict__, '__file__': __file__, 'ROM': ROM, 'fixture': apply_fixture,
        'ROOT': Path('work/analysis/sea_registration_live_v1552h'),
        'CAP': Path('E:/Rota Nova translations/Generated/work/emulation_v193/sea_registration_live_v1552h_1542')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
