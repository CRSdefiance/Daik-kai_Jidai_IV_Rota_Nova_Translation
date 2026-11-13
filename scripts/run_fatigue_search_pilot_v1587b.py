"""Fixture-free cold-boot Search pilot;ordinary controls only."""
import inspect,json
from pathlib import Path
from scripts import run_ship_sinking_live_v1350 as previous
from scripts.verify_village_wrap_v608 import read
if __name__=='__main__':
    release_path='work/analysis/inspection_status_release_v1577/registered_release_verification.json'
    release=read(release_path)
    commands=[{'until':4900,'duration':1},{'until':5000,'buttons':['A'],'duration':4},{'until':5100,'duration':1},
        {'until':5200,'buttons':['Y'],'duration':4},{'until':5300,'buttons':['Y'],'duration':4}]
    prefix=''.join(json.dumps(r)+'\n' for r in commands)
    source=inspect.getsource(previous.main)
    for old,new in [('work/analysis/ship_sinking_release_v1343/registered_release_verification.json',release_path),
        ('9d455782724d98198b7bc3fdac7be755945e58d406e66a4634094d9a0eab301b',release['candidate_sha256']),
        ("journal.write_text('',encoding='utf-8')",'journal.write_text('+repr(prefix)+",encoding='utf-8')")]:
        assert source.count(old)==1;source=source.replace(old,new)
    def forbidden_fixture(*args):raise AssertionError('This pilot permits no fixture')
    env={**previous.__dict__,'__file__':__file__,'ROM':Path('out/all_routes_combined_v1578_candidate.nds'),'fixture':forbidden_fixture,
        'ROOT':Path('work/analysis/fatigue_search_pilot_v1587b'),
        'CAP':Path('E:/Rota Nova translations/Generated/work/emulation_v193/fatigue_search_pilot_v1587b_1578')}
    exec(compile(source,__file__,'exec'),env);env['main']()
