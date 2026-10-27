"""Cold boot with declared coherent location fixtures and normal Search inputs."""
import inspect,json
from pathlib import Path
from scripts import run_ship_sinking_live_v1350 as previous
from scripts.native_fatigue_shore_fixture_v1602 import apply_fixture,ROM,REQUEST
from scripts.verify_village_wrap_v608 import read

if __name__=='__main__':
    release_path='work/analysis/fatigue_status_release_v1593/registered_release_verification.json'
    release=read(release_path)
    commands=[{'until':4900,'duration':1},{'until':5000,'buttons':['A'],'duration':4},
        {'until':5012,'buttons':['A'],'duration':4,'battle_fixture':REQUEST},
        {'until':5100,'buttons':['Y'],'duration':4},{'until':5200,'buttons':['Y'],'duration':4},
        {'until':5300,'buttons':['A'],'duration':4},{'until':5400,'duration':1},
        {'until':5500,'buttons':['B'],'duration':4},{'until':5600,'buttons':['Y'],'duration':4},
        {'until':5650,'duration':1},{'until':5680,'duration':1,'battle_fixture':REQUEST},
        {'until':5800,'buttons':['A'],'duration':4},{'until':5900,'duration':1}]
    prefix=''.join(json.dumps(r)+'\n' for r in commands)
    source=inspect.getsource(previous.main)
    for old,new in [('work/analysis/ship_sinking_release_v1343/registered_release_verification.json',release_path),
        ('9d455782724d98198b7bc3fdac7be755945e58d406e66a4634094d9a0eab301b',release['candidate_sha256']),
        ("journal.write_text('',encoding='utf-8')",'journal.write_text('+repr(prefix)+",encoding='utf-8')")]:
        assert source.count(old)==1;source=source.replace(old,new)
    env={**previous.__dict__,'__file__':__file__,'ROM':ROM,'fixture':apply_fixture,
        'ROOT':Path('work/analysis/fatigue_recovery_live_v1603'),
        'CAP':Path('E:/Rota Nova translations/Generated/work/emulation_v193/fatigue_recovery_live_v1603_1594')}
    exec(compile(source,__file__,'exec'),env);env['main']()
