"""Branch the original V1364 encounter through normal sailing controls only.

Reuse the hash-locked prebattle40-byte location fixture and ordinary encounter
prefix through9100. Later commands are append-only; no battle/duel mutation.
"""
import inspect
import json
from pathlib import Path
from scripts import run_ship_sinking_live_v1350 as previous
from scripts.native_flagship_capture_fixture_v1368 import apply_fixture,ROM
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha


if __name__=='__main__':
    release = read('work/analysis/flagship_precision_release_v1363/registered_release_verification.json')
    prior_path = Path('work/analysis/ship_sinking_live_v1353/navigation.jsonl')
    terminal = read('work/analysis/ship_sinking_live_v1353/terminal_preservation.json')
    assert sha(prior_path.read_bytes())==terminal['navigation_sha256']
    assert terminal['source_and_disposable_donors_unchanged']
    commands = [json.loads(line) for line in prior_path.read_text(encoding='utf-8').splitlines()]
    commands = [row for row in commands if row.get('until',100000)<=9100]
    assert commands[-1]['until']==9100
    assert sum('battle_fixture' in row for row in commands)==1
    assert not any('battle_fixture' in row for row in commands[1:])
    prefix = ''.join(json.dumps(row)+'\n' for row in commands)
    source = inspect.getsource(previous.main)
    for old,new in [
        ('work/analysis/ship_sinking_release_v1343/registered_release_verification.json','work/analysis/flagship_precision_release_v1363/registered_release_verification.json'),
        ('9d455782724d98198b7bc3fdac7be755945e58d406e66a4634094d9a0eab301b',release['candidate_sha256']),
        ("journal.write_text('',encoding='utf-8')",'journal.write_text('+repr(prefix)+",encoding='utf-8')")]:
        assert source.count(old)==1,old
        source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,'ROM':ROM,'fixture':apply_fixture,
        'ROOT':Path('work/analysis/ship_sinking_gunnery_v1373'),
        'CAP':Path('E:/Rota Nova translations/Generated/work/emulation_v193/ship_sinking_gunnery_v1373_1364')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
