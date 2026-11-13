"""Replay original crew-loss outcome and continue with current-count preservation."""
import inspect,json
from pathlib import Path
from scripts import run_ship_sinking_live_v1350 as previous
from scripts.native_hot_spring_resilient_v1644 import apply_fixture,ROM
from scripts.verify_village_wrap_v608 import read
if __name__=='__main__':
    report=read('E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_notice_supplied_v1643_1637/capture_report.json');assert report['frames']==21700
    source_journal=Path('work/analysis/hot_spring_notice_supplied_v1643/navigation.jsonl');commands=[json.loads(s) for s in source_journal.read_text(encoding='utf-8').splitlines()]
    assert commands[-1]=={'stop':True};prefix=''.join(json.dumps(r)+'\n' for r in commands[:-1])
    release_path='work/analysis/hot_spring_notice_release_v1636/registered_release_verification.json';release=read(release_path);source=inspect.getsource(previous.main)
    for a,b in [('work/analysis/ship_sinking_release_v1343/registered_release_verification.json',release_path),
        ('9d455782724d98198b7bc3fdac7be755945e58d406e66a4634094d9a0eab301b',release['candidate_sha256']),
        ("journal.write_text('',encoding='utf-8')",'journal.write_text('+repr(prefix)+",encoding='utf-8')")]:
        assert source.count(a)==1;source=source.replace(a,b)
    env={**previous.__dict__,'__file__':__file__,'ROM':ROM,'fixture':apply_fixture,'ROOT':Path('work/analysis/hot_spring_notice_resilient_v1645'),
        'CAP':Path('E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_notice_resilient_v1645_1637')}
    exec(compile(source,__file__,'exec'),env);env['main']()
