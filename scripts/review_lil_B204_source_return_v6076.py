"""Preserve observed B204 return and later B120,not an assumed B43/town endpoint."""
from pathlib import Path
from PIL import Image,ImageDraw
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B204_source_return_v6076')
RUN=Path('work/analysis/lil_B204_source_run_v6071_clean_Japanese')
PATHS=Path('work/analysis/lil_B204_source_paths_v6072/one_actual_source_path_and_complete_command_intervals.json')
if __name__=='__main__':
    assert not ROOT.exists();plan,terminal,paths=map(read,[RUN/'run_plan.json',RUN/'terminal.json',PATHS]);cap=Path(plan['capture_folder']);report,trace=map(read,[cap/'capture_report.json',cap/'observer/commands.json'])
    assert terminal['terminal'] and report['frames']==13001 and not trace['errors'] and not trace['mismatches'] and paths['source_end1308_return_frame']==7894
    later=[r for r in trace['rows'] if r['kind']=='before_command' and r['source']['block']!=22]
    assert later[0]['frame']==9101 and later[0]['source']['block']==120 and all(r['source']['block']==120 for r in later)
    assert later[-1]['source']['instruction_offset']==2234
    selected=[];ROOT.mkdir(parents=True);sheet=Image.new('RGB',(1040,2400),'#263238');draw=ImageDraw.Draw(sheet)
    for i,f in enumerate([7870,7930,8350,9070,9190,13001]):
        r=next(p for p in report['frames_captured'] if p['frame']==f);p=Path(r['path']);assert sha(p.read_bytes())==r['PNG_sha256'];im=Image.open(p).convert('RGB');assert im.size==(256,384)
        x,y=i%2*520,i//2*800;draw.text((x+4,y+3),'Actual Japanese source fixture frame'+str(f),fill='white');sheet.paste(im.resize((512,768),Image.Resampling.NEAREST),(x+4,y+24));selected.append(r)
    picture=ROOT/'actual_scene_end_and_later_B120.png';sheet.save(picture)
    save(ROOT/'complete_source_return_and_following_block.json',dict(source_paths=str(PATHS),source_paths_sha256=sha(PATHS.read_bytes()),
        complete20_objects35_commands_observed=True,source_end_return_frame=7894,first_following_SC_command=dict(frame=9101,route=2,block=120,offset=8,word=later[0]['source']['first_word']),
        final_following_observed_command=dict(frame=later[-1]['frame'],route=2,block=120,offset=2234,word=later[-1]['source']['first_word']),
        later_source_block_list=sorted({r['source']['block'] for r in later}),selected_frames=selected,sheet=str(picture),sheet_sha256=sha(picture.read_bytes()),visual_review_pending=True,
        no_immediate_town_B43_or_idle_town_endpoint_claim=True,initialized_Amsterdam_fixture_not_natural_event_activation_or_original_location=True,
        no_full_route_effect_or_hardware_claim=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [PATHS,RUN/'terminal.json',RUN/'run_plan.json',cap/'capture_report.json',cap/'observer/commands.json',Path(__file__)]}))
    print('B204 ends7894;following B120 starts9101 and remains observed at13001. Six exact source frames ready for visual review;no B43/town endpoint assumed.')
