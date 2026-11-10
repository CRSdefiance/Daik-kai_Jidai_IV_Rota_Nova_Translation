"""Measure existing final exports and expose all six unmasked postscene prompt differences."""
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
ROOT=Path('work/analysis/lil_B207_later_v6375')
ACTUAL=Path('work/analysis/lil_B207_actual_v6374/all13_English_panels_complete_native_holds24_commands_and_source_comparison.json')
if __name__=='__main__':
    assert not ROOT.exists();d=read(ACTUAL);assert len(d['later_whole_RGB_differences'])==6;values=[];durations=[];evidence={str(ACTUAL):sha(ACTUAL.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())}
    for v in d['versions']:
        snap=v['final_snapshot'];raw=Path(snap['path']).read_bytes();assert len(raw)==4194304 and sha(raw)==snap['sha256'];arm=NdsImage.open(v['research_ROM']).read_file('/__arm9__.bin');cpu,get=get_machine(arm,raw);actor,captain=get(0xCB184),get(0x7F244);assert captain==2 and 0x02000000<=actor<=0x02400000-0x1A04
        components={fn.__name__:fn(arm,raw) for fn in [state,models,persistent_objects,tasks,calendar]};components['tasks']=dict(bytes=len(components['tasks']),sha256=sha(components['tasks']));values.append(dict(language=v['language'],snapshot=snap,components=components,whole_actor_hex=bytes(cpu.mem_read(actor,0x1A04)).hex(),captain_ID=captain,seed=int.from_bytes(raw[0x168EB8:0x168EBC],'little')));evidence[snap['path']]=snap['sha256']
    for a,b in zip(d['versions'][0]['command_pairs'],d['versions'][1]['command_pairs'],strict=True):
        da,db=a['returned']-a['start'],b['returned']-b['start']
        if da!=db:durations.append(dict(source_offset=a['source_offset'],word=a['word'],source_duration=da,English_duration=db,delta=db-da))
    ROOT.mkdir(parents=True);sheet=Image.new('RGB',(1536,820),'#263238');draw=ImageDraw.Draw(sheet)
    for i,r in enumerate(d['later_whole_RGB_differences']):
        bounds=r['whole_RGB_difference_bbox'];assert 224<=bounds[0]<bounds[2]<=240 and 360<=bounds[1]<bounds[3]<=376
        x,y=i%3*512,i//3*410
        for j,label in enumerate(['source','English']):
            p=Path(r[label+'_capture']);assert sha(p.read_bytes())==r[label+'_capture_sha256'];draw.text((x+j*256+3,y+3),label+' '+str(r['frame']),fill='white');sheet.paste(Image.open(p).convert('RGB'),(x+j*256,y+24));evidence[str(p)]=sha(p.read_bytes())
    p=ROOT/'all_six_unmasked_postscene_prompt_pairs.png';sheet.save(p)
    equality={k:values[0]['components'][k]==values[1]['components'][k] for k in values[0]['components']};actor=values[0]['whole_actor_hex']==values[1]['whole_actor_hex'];rng=values[0]['seed']==values[1]['seed']
    save(ROOT/'original_final_native_getters_and_all_six_prompt_differences.json',dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),native_values=values,five_native_component_equality=equality,whole_actor_and_captain_equal=actor,final_PRNG_equal=rng,final_PRNG_seeds=[v['seed'] for v in values],command_duration_changes=durations,original_native_getters={fn.__name__:inspect.getsource(fn) for fn in [state,models,persistent_objects,tasks,calendar]},all_six_unmasked_later_differences=d['later_whole_RGB_differences'],all_postscene_differences_inside_advance_prompt_rectangle=True,broad_later_RGB_differences=[],review_sheet=dict(path=str(p),sha256=sha(p.read_bytes())),visual_review_pending=True,native_getters_applied_only_to_exported_copies=True,no_new_emulator_run_forced_state_pixel_edit_mask_or_retiming=True,no_whole_RAM_future_sequence_broad_simulation_or_complete_timing_cause_claim=True,evidence=evidence,new_review_credit=0,full_goal_complete=False));print(dict(native_component_equality=equality,whole_actor_equal=actor,final_PRNG_equal=rng,duration_changes=durations,six_unmasked_prompt_pairs=True))
