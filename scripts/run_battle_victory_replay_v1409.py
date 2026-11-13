"""Complete original capture/victory/reward/sailing replay on registered V1404."""
import inspect
from pathlib import Path
from scripts import run_ship_sinking_live_v1350 as previous
from scripts.native_battle_victory_fixture_v1408 import apply_fixture,ROM
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha


if __name__=='__main__':
    release = read('work/analysis/battle_victory_release_v1403/registered_release_verification.json')
    prior_path = Path('work/analysis/flagship_capture_replay_v1369/navigation.jsonl')
    terminal = read('work/analysis/flagship_capture_replay_v1369/terminal_preservation.json')
    assert sha(prior_path.read_bytes())==terminal['navigation_sha256']
    assert terminal['source_and_disposable_donors_unchanged']
    prior = prior_path.read_text(encoding='utf-8')
    source = inspect.getsource(previous.main)
    for old,new in [
        ('work/analysis/ship_sinking_release_v1343/registered_release_verification.json','work/analysis/battle_victory_release_v1403/registered_release_verification.json'),
        ('9d455782724d98198b7bc3fdac7be755945e58d406e66a4634094d9a0eab301b',release['candidate_sha256']),
        ("journal.write_text('',encoding='utf-8')",'journal.write_text('+repr(prior)+",encoding='utf-8')")]:
        assert source.count(old)==1,old
        source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,'ROM':ROM,'fixture':apply_fixture,
        'ROOT':Path('work/analysis/battle_victory_replay_v1409'),
        'CAP':Path('E:/Rota Nova translations/Generated/work/emulation_v193/battle_victory_v1409_1404')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
