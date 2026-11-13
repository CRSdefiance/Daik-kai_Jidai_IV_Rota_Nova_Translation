"""Cold-boot placement survey of existing fleet4;no altered gear or outcomes."""
import inspect,json
from pathlib import Path
from scripts import run_ship_sinking_live_v1350 as previous
from scripts.native_stronger_fleet_location_v1471 import apply_fixture,ROM
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    release=read('work/analysis/ship_loss_surrender_release_v1455/registered_release_verification.json')
    prior=Path('work/analysis/flagship_capture_replay_v1369/navigation.jsonl')
    assert sha(prior.read_bytes())==read(prior.parent/'terminal_preservation.json')['navigation_sha256']
    commands=[json.loads(s) for s in prior.read_text().splitlines()]
    commands=[r for r in commands if r.get('until',100000)<=5000]
    assert commands[-1]['until']==5000 and sum('battle_fixture' in r for r in commands)==1
    commands.append({'until':5100,'duration':1})
    prefix=''.join(json.dumps(r)+'\n' for r in commands)
    source=inspect.getsource(previous.main)
    for old,new in [
        ('work/analysis/ship_sinking_release_v1343/registered_release_verification.json','work/analysis/ship_loss_surrender_release_v1455/registered_release_verification.json'),
        ('9d455782724d98198b7bc3fdac7be755945e58d406e66a4634094d9a0eab301b',release['candidate_sha256']),
        ("journal.write_text('',encoding='utf-8')",'journal.write_text('+repr(prefix)+",encoding='utf-8')")]:
        assert source.count(old)==1,old
        source=source.replace(old,new)
    env={**previous.__dict__,'__file__':__file__,'ROM':ROM,'fixture':apply_fixture,
        'ROOT':Path('work/analysis/stronger_fleet_location_v1472'),
        'CAP':Path('E:/Rota Nova translations/Generated/work/emulation_v193/stronger_fleet_location_v1472_1456')}
    exec(compile(source,__file__,'exec'),env);env['main']()
