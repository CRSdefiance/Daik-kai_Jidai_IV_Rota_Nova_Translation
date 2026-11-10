"""Measure existing exported state and retain unmasked later differences; no replay."""
from collections import Counter
from pathlib import Path
import inspect
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_shipyard_gameplay_v760 import models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_ceremony_prayer_gameplay_v814 import calendar
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B206_later_v6320')
ACTUAL=Path('work/analysis/lil_B206_actual_v6319/all24_English_panels55_observations217_native_holds_five_menus_three_same_code_paths.json')
if __name__=='__main__':
    assert not ROOT.exists();d=read(ACTUAL);measured=[];durations=[]
    evidence={str(ACTUAL):sha(ACTUAL.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())}
    versions={(v['path'],v['language']):v for v in d['versions']}
    for path in ['buy','high_price','pitch_refusal']:
        values=[];left,right=[versions[path,c] for c in ['source','English']]
        for v in [left,right]:
            snap=v['final_snapshot'];raw=Path(snap['path']).read_bytes();assert sha(raw)==snap['sha256'] and len(raw)==4194304
            arm=NdsImage.open(v['research_ROM']).read_file('/__arm9__.bin');cpu,get=get_machine(arm,raw);actor,captain=get(0xCB184),get(0x7F244)
            assert captain==2 and 0x02000000<=actor<=0x02400000-0x1A04
            components={fn.__name__:fn(arm,raw) for fn in [state,models,persistent_objects,tasks,calendar]}
            components['tasks']=dict(bytes=len(components['tasks']),sha256=sha(components['tasks']))
            values.append(dict(language=v['language'],snapshot=snap,components=components,whole_actor_hex=bytes(cpu.mem_read(actor,0x1A04)).hex(),captain_ID=captain,seed=int.from_bytes(raw[0x168EB8:0x168EBC],'little')))
            evidence[snap['path']]=snap['sha256']
        measured.append(dict(path=path,final_frame=16001,native=values,five_native_component_equality={k:values[0]['components'][k]==values[1]['components'][k] for k in values[0]['components']},whole_actor_and_captain_equal=values[0]['whole_actor_hex']==values[1]['whole_actor_hex'],PRNG_seeds=[v['seed'] for v in values],PRNG_equal=values[0]['seed']==values[1]['seed'],source_English_exit_frames=[left['exit_frame'],right['exit_frame']]))
        for a,b in zip(left['command_pairs'],right['command_pairs'],strict=True):
            assert (a['source_offset'],a['word'],a['native_result'])==(b['source_offset'],b['word'],b['native_result'])
            da,db=a['returned']-a['start'],b['returned']-b['start']
            if da!=db:durations.append(dict(path=path,source_offset=a['source_offset'],word=a['word'],source_duration=da,English_duration=db,delta=db-da))
    prompt=[];broad=[]
    for r in d['later_whole_RGB_differences']:
        (prompt if r['whole_RGB_difference_bbox']==[224,360,240,376] else broad).append(r)
    selected=[]
    for path in ['buy','high_price']:
        rows=[r for r in broad if r['path']==path];assert rows
        selected.extend(rows[i] for i in [0,len(rows)//2,len(rows)-1])
    ROOT.mkdir(parents=True);sheet=Image.new('RGB',(1536,820),'#263238');draw=ImageDraw.Draw(sheet)
    for i,r in enumerate(selected):
        xx,yy=i%3*512,i//3*410
        for j,label in enumerate(['source','English']):
            p=Path(r[label+'_capture']);assert sha(p.read_bytes())==r[label+'_capture_sha256'];evidence[str(p)]=sha(p.read_bytes())
            draw.text((xx+256*j+3,yy+3),r['path']+' '+label+' '+str(r['frame']),fill='white');sheet.paste(Image.open(p).convert('RGB'),(xx+256*j,yy+24))
    p=ROOT/'representative_earliest_middle_final_broad_differences.png';sheet.save(p)
    save(ROOT/'unmasked_later_inventory_and_original_final_native_getters.json',dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),paired_final_state_measurements=measured,command_duration_changes=durations,original_native_getters={fn.__name__:inspect.getsource(fn) for fn in [state,models,persistent_objects,tasks,calendar]},prompt_bounded_samples=prompt,all_broad_later_samples=broad,all114_whole_RGB_differences_preserved=d['later_whole_RGB_differences'],postscene_difference_bounds=[dict(bounds=list(k),samples=v) for k,v in Counter(tuple(r['whole_RGB_difference_bbox']) for r in d['later_whole_RGB_differences']).items()],selected_first_middle_last_per_affected_path=selected,representative_sheet=dict(path=str(p),sha256=sha(p.read_bytes())),visual_review_pending=True,native_getters_applied_to_exported_copies_only=True,no_new_emulator_run_or_forced_state=True,no_mask_retiming_or_pixel_edit=True,no_causal_or_world_equivalence_claim=True,evidence=evidence,new_review_credit=0,full_goal_complete=False))
    print([(r['path'],r['five_native_component_equality'],r['whole_actor_and_captain_equal'],r['PRNG_seeds'],r['source_English_exit_frames']) for r in measured]);print(dict(prompt=len(prompt),broad=len(broad),sampled_pairs=len(selected),duration_changes=len(durations)))
