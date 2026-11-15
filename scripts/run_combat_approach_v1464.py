"""Original encounter with one declared southwest/Carronade prebattle fixture."""
import inspect
import json
from pathlib import Path
from scripts import run_ship_sinking_live_v1350 as previous
from scripts.native_combat_approach_fixture_v1463 import apply_fixture,ROM
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    release = read('work/analysis/ship_loss_surrender_release_v1455/registered_release_verification.json')
    prior_path = Path('work/analysis/flagship_capture_replay_v1369/navigation.jsonl')
    terminal = read('work/analysis/flagship_capture_replay_v1369/terminal_preservation.json')
    assert sha(prior_path.read_bytes())==terminal['navigation_sha256']
    commands = [json.loads(line) for line in prior_path.read_text(encoding='utf-8').splitlines()]
    commands = [r for r in commands if r.get('until',100000)<=9000]
    assert commands[-1]['until']==9000 and sum('battle_fixture' in r for r in commands)==1
    commands += [{'until':9100,'buttons':['LEFT'],'duration':80},{'until':9400,'duration':1}]
    prefix = ''.join(json.dumps(row)+'\n' for row in commands)
    source = inspect.getsource(previous.main)
    for old,new in [
        ('work/analysis/ship_sinking_release_v1343/registered_release_verification.json','work/analysis/ship_loss_surrender_release_v1455/registered_release_verification.json'),
        ('9d455782724d98198b7bc3fdac7be755945e58d406e66a4634094d9a0eab301b',release['candidate_sha256']),
        ("journal.write_text('',encoding='utf-8')",'journal.write_text('+repr(prefix)+",encoding='utf-8')")]:
        assert source.count(old)==1,old
        source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,'ROM':ROM,'fixture':apply_fixture,
        'ROOT':Path('work/analysis/combat_approach_v1464'),
        'CAP':Path('E:/Rota Nova translations/Generated/work/emulation_v193/combat_approach_v1464_1456')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
