"""Cold-boot pilot of original loading after one declared existing-fleet activation."""
import inspect
import json
from pathlib import Path
from scripts import run_ship_sinking_live_v1350 as previous
from scripts.native_inspection_status_lookout_fixture_v1581 import apply_fixture, ROM
from scripts.verify_village_wrap_v608 import read

if __name__ == '__main__':
    release_path = 'work/analysis/inspection_status_release_v1577/registered_release_verification.json'
    release = read(release_path)
    commands = [json.loads(line) for line in Path('work/analysis/sea_inspection_actual_v1567/navigation.jsonl').read_text(encoding='utf-8').splitlines()]
    assert commands.pop()=={'stop':True}
    commands += [{'until':6200,'buttons':['A'],'duration':4},{'until':6300,'duration':1},{'stop':True}]
    prefix = ''.join(json.dumps(r) + '\n' for r in commands)
    source = inspect.getsource(previous.main)
    for old, new in [
        ('work/analysis/ship_sinking_release_v1343/registered_release_verification.json', release_path),
        ('9d455782724d98198b7bc3fdac7be755945e58d406e66a4634094d9a0eab301b', release['candidate_sha256']),
        ("journal.write_text('',encoding='utf-8')", 'journal.write_text(' + repr(prefix) + ",encoding='utf-8')")]:
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    env = {**previous.__dict__, '__file__': __file__, 'ROM': ROM, 'fixture': apply_fixture,
        'ROOT': Path('work/analysis/inspection_status_lookout_v1582'),
        'CAP': Path('E:/Rota Nova translations/Generated/work/emulation_v193/inspection_status_lookout_v1582_1578')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
