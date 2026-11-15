"""Full current actual covering-fire glyphs,inputs andnormal source transition."""
import inspect
import json
from pathlib import Path
from scripts import verify_covering_fire_gameplay_v1042 as previous
from scripts.native_covering_fire_v1816 import apply_fixture
from scripts.verify_reinforcement_faction_actual_v1813 import current_entries
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/covering_fire_actual_v1819')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/covering_fire_v1817_1807')
RUN=Path('work/analysis/covering_fire_run_v1817')

if __name__=='__main__':
    source=inspect.getsource(previous.main)
    changes=[('work/analysis/reinforcement_sniping_v1041/terminal_preservation.json',str(RUN/'terminal_preservation.json').replace('\\','/')),('translations/reinforcement_sniping_editorial_manuscript_v2.json','translations/reinforcement_sniping_editorial_manuscript_v4.json'),("font=read(doc['native_font_proof'])","font=read('work/analysis/covering_fire_current_v1818/current567_layouts_and22_native_planes.json')"),("'reinforcement_and_admiral_shot_actual_scenes_still_pending':True,","'admiral_shot_actual_scene_still_pending':True,")]
    for old,new in changes:
        assert source.count(old)==1,(old,source.count(old));source=source.replace(old,new)
    env={**previous.__dict__,'__file__':__file__,'ROOT':ROOT,'FOLDER':CAP,'ROM':Path('out/all_routes_combined_v1807_candidate.nds'),'apply_fixture':apply_fixture,'current_entries':current_entries}
    exec(compile(source,__file__,'exec'),env);env['main']()
    plan=read(RUN/'run_plan.json');report=read(CAP/'capture_report.json');journal=read(CAP/'navigation_command_journal.json')
    commands=[json.loads(s)for s in(RUN/'navigation.jsonl').read_text().splitlines()if s]
    assert commands==[r['command']for r in journal['commands_received']]and all(r['validation_passed']for r in journal['commands_received'])
    assert commands[-1]=={'stop':True}
    schedule=list(read(plan['inputs']))
    for r in journal['commands_received']:
        c=r['command']
        if c.get('buttons')or c.get('touch'):
            event={'start':r['frame']+1,'duration':c['duration'],'buttons':c.get('buttons',[])}
            if c.get('touch'):event['touch']=c['touch']
            schedule.append(event)
    assert schedule==report['scripted_input_schedule']
    save(ROOT/'terminal_command_input_binding.json',{'commands_sha256':sha((RUN/'navigation.jsonl').read_bytes()),'harness_journal_sha256':sha((CAP/'navigation_command_journal.json').read_bytes()),'all_commands_validated_and_full_actual_input_schedule_exact':True,'terminal_frame':6310,'no_message_RNG_or_result_override':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
