"""Fixture-free cold-boot Search pilot;ordinary controls only."""
import inspect,json
from pathlib import Path
from scripts import run_ship_sinking_live_v1350 as previous
from scripts.verify_village_wrap_v608 import read
if __name__=='__main__':
    release_path='work/analysis/fatigue_status_release_v1593/registered_release_verification.json'
    release=read(release_path)
    commands=[json.loads(line) for line in Path('work/analysis/fatigue_search_pilot_v1587b/navigation.jsonl').read_text(encoding='utf-8').splitlines()]
    prefix=''.join(json.dumps(r)+'\n' for r in commands)
    source=inspect.getsource(previous.main)
    for old,new in [('work/analysis/ship_sinking_release_v1343/registered_release_verification.json',release_path),
        ('9d455782724d98198b7bc3fdac7be755945e58d406e66a4634094d9a0eab301b',release['candidate_sha256']),
        ("journal.write_text('',encoding='utf-8')",'journal.write_text('+repr(prefix)+",encoding='utf-8')")]:
        assert source.count(old)==1;source=source.replace(old,new)
    def forbidden_fixture(*args):raise AssertionError('This pilot permits no fixture')
    env={**previous.__dict__,'__file__':__file__,'ROM':Path('out/all_routes_combined_v1594_candidate.nds'),'fixture':forbidden_fixture,
        'ROOT':Path('work/analysis/fatigue_increase_actual_v1597'),
        'CAP':Path('E:/Rota Nova translations/Generated/work/emulation_v193/fatigue_increase_actual_v1597_1594')}
    exec(compile(source,__file__,'exec'),env);env['main']()
