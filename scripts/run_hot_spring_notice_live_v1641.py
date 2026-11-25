"""Replay all audited original navigation,then continue the unforced optional path."""
import inspect,json
from pathlib import Path
from scripts import run_ship_sinking_live_v1350 as previous
from scripts.native_hot_spring_notice_location_v1640 import apply_fixture,ROM
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read
if __name__=='__main__':
    old=read('work/analysis/hot_spring_actual_v1628b/two_original_hot_spring_discovery_and_minus15_visits.json')['preservation_audit']
    report=read(old['terminal_report']);assert sha(Path(old['terminal_report']).read_bytes())==old['terminal_report_sha256']
    assert report['frames']==13600 and report['ROM_sha256']=='cb049635c45b6bc75add4ada18db69ae2ece4aa05b9270a3553ed9ed74a228e4'
    journal=Path('work/analysis/hot_spring_live_v1626/navigation.jsonl');commands=[json.loads(line) for line in journal.read_text(encoding='utf-8').splitlines()]
    assert commands[-1]=={'stop':True}
    prefix=''.join(json.dumps(r)+'\n' for r in commands[:-1])
    release_path='work/analysis/hot_spring_notice_release_v1636/registered_release_verification.json';release=read(release_path)
    source=inspect.getsource(previous.main)
    for a,b in [('work/analysis/ship_sinking_release_v1343/registered_release_verification.json',release_path),
        ('9d455782724d98198b7bc3fdac7be755945e58d406e66a4634094d9a0eab301b',release['candidate_sha256']),
        ("journal.write_text('',encoding='utf-8')",'journal.write_text('+repr(prefix)+",encoding='utf-8')")]:
        assert source.count(a)==1;source=source.replace(a,b)
    env={**previous.__dict__,'__file__':__file__,'ROM':ROM,'fixture':apply_fixture,'ROOT':Path('work/analysis/hot_spring_notice_live_v1641'),
        'CAP':Path('E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_notice_live_v1641_1637')}
    exec(compile(source,__file__,'exec'),env);env['main']()
