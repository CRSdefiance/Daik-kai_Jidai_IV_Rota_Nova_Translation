"""Replay audited navigation,then add only the user-authorized original refill."""
import inspect,json
from pathlib import Path
from scripts import run_ship_sinking_live_v1350 as previous
from scripts.native_hot_spring_provisions_v1642 import apply_fixture,ROM,REQUEST
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read
if __name__=='__main__':
    audit=read('work/analysis/hot_spring_notice_first_run_v1643a/terminal_location_only_replay_preservation.json')['preservation_audit']
    assert sha(Path(audit['terminal_report']).read_bytes())==audit['terminal_report_sha256'] and audit['terminal_frame']==20700
    source_journal=Path('work/analysis/hot_spring_notice_live_v1641/navigation.jsonl');commands=[json.loads(line) for line in source_journal.read_text(encoding='utf-8').splitlines()]
    assert commands[-1]=={'stop':True}
    commands=commands[:-1]+[{'until':20730,'duration':1,'battle_fixture':REQUEST}]
    prefix=''.join(json.dumps(r)+'\n' for r in commands)
    release_path='work/analysis/hot_spring_notice_release_v1636/registered_release_verification.json';release=read(release_path);source=inspect.getsource(previous.main)
    for a,b in [('work/analysis/ship_sinking_release_v1343/registered_release_verification.json',release_path),
        ('9d455782724d98198b7bc3fdac7be755945e58d406e66a4634094d9a0eab301b',release['candidate_sha256']),
        ("journal.write_text('',encoding='utf-8')",'journal.write_text('+repr(prefix)+",encoding='utf-8')")]:
        assert source.count(a)==1;source=source.replace(a,b)
    env={**previous.__dict__,'__file__':__file__,'ROM':ROM,'fixture':apply_fixture,'ROOT':Path('work/analysis/hot_spring_notice_supplied_v1643'),
        'CAP':Path('E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_notice_supplied_v1643_1637')}
    exec(compile(source,__file__,'exec'),env);env['main']()
