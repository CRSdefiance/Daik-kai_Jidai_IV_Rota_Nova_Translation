"""Cold replay of the complete original capture encounter on registered V1364."""
import inspect
from pathlib import Path
from scripts import run_ship_sinking_live_v1350 as previous
from scripts.native_flagship_capture_fixture_v1368 import apply_fixture,ROM
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    release = read('work/analysis/flagship_precision_release_v1363/registered_release_verification.json')
    prior_path = Path('work/analysis/ship_sinking_live_v1353/navigation.jsonl')
    prior = prior_path.read_text(encoding='utf-8')
    terminal = read('work/analysis/ship_sinking_live_v1353/terminal_preservation.json')
    assert sha(prior_path.read_bytes())==terminal['navigation_sha256']
    assert terminal['source_and_disposable_donors_unchanged']
    source = inspect.getsource(previous.main)
    for old,new in [
        ('work/analysis/ship_sinking_release_v1343/registered_release_verification.json','work/analysis/flagship_precision_release_v1363/registered_release_verification.json'),
        ('9d455782724d98198b7bc3fdac7be755945e58d406e66a4634094d9a0eab301b',release['candidate_sha256']),
        ("journal.write_text('',encoding='utf-8')",'journal.write_text('+repr(prior)+",encoding='utf-8')")]:
        assert source.count(old)==1,old
        source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,'ROM':ROM,'fixture':apply_fixture,
        'ROOT':Path('work/analysis/flagship_capture_replay_v1369'),
        'CAP':Path('E:/Rota Nova translations/Generated/work/emulation_v193/flagship_capture_v1369_1364')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
