"""Measure paired final state and build complete screens without broad equivalence claims."""
import struct,json
from pathlib import Path
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

ROOT=Path('work/analysis/lil_B196_actual_review_v5629b')
ACTUAL=Path('work/analysis/lil_B196_actual_v5628b/three_paired_paths_native_panels_menus_and_separate_endings.json')
def native_json(value):
    assert isinstance(value,bytes);return {'native_byte_span_hex':value.hex()}

if __name__=='__main__':
    assert not ROOT.exists();d=read(ACTUAL)
    assert not d['failures'] and len(d['actual_panels'])==13 and len(d['actual_menu_cases'])==13
    assert not d['command_timing_differences'] and not d['later_whole_RGB_differences']
    versions={(v['path'],v['case']):v for v in d['versions']};pairs=[];fullscreens=[];evidence={str(ACTUAL):sha(ACTUAL.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())}
    choices=[('first_buy',[3970,4210]),('all_pass',[5170,12970]),('deepest_buy',[4990,12970])]
    ROOT.mkdir(parents=True)
    for path,frames in choices:
        measured=[];photos=[];reports=[]
        for case in ['clean_Japanese','reviewed_English']:
            v=versions[path,case];report=read(v['capture_report']);snap=v['final_readonly_RAM_snapshot'];raw=Path(snap['path']).read_bytes();assert sha(raw)==snap['sha256']
            arm=NdsImage.open(v['research_ROM']).read_file('/__arm9__.bin');cpu,get=get_machine(arm,raw)
            actor,captain=get(0xCB184),get(0x7F244);assert captain==2 and 0x02000000<=actor<=0x02400000-0x1A04
            components={fn.__name__:fn(arm,raw) for fn in [state,models,persistent_objects,tasks,calendar]}
            measured.append(dict(case=case,snapshot=snap,components=components,whole_actor_hex=bytes(cpu.mem_read(actor,0x1A04)).hex(),captain_ID=captain,seed=struct.unpack_from('<I',raw,0x168EB8)[0]))
            photos.append({p['frame']:p for p in report['frames_captured']});reports.append(report)
            evidence[v['capture_report']]=sha(Path(v['capture_report']).read_bytes());evidence[snap['path']]=snap['sha256']
        equality={k:measured[0]['components'][k]==measured[1]['components'][k] for k in measured[0]['components']}
        pairs.append(dict(path=path,final_frame=13001,native=measured,five_native_component_equality=equality,whole1A04_actor_and_captain2_equal=measured[0]['whole_actor_hex']==measured[1]['whole_actor_hex'],PRNG_seeds=[m['seed'] for m in measured],PRNG_equal=measured[0]['seed']==measured[1]['seed']))
        sheet=Image.new('RGB',(1048,1600),'#263238');draw=ImageDraw.Draw(sheet)
        for row,frame in enumerate(frames):
            for col,case in enumerate(['clean_Japanese','reviewed_English']):
                p=photos[col][frame];assert sha(Path(p['path']).read_bytes())==p['PNG_sha256'];pic=Image.open(p['path']).convert('RGB');x,y=col*524,row*800
                draw.text((x+4,y+4),f'{path} / {case} / frame {frame}',fill='white');sheet.paste(pic.resize((512,768),Image.Resampling.NEAREST),(x+4,y+24));evidence[p['path']]=p['PNG_sha256']
        p=ROOT/f'paired_full_screen_{path}.png';sheet.save(p);fullscreens.append(dict(path=str(p),sha256=sha(p.read_bytes()),frames=frames))
    assert all(all(p['five_native_component_equality'].values()) and p['whole1A04_actor_and_captain2_equal'] and p['PRNG_equal'] for p in pairs)
    result=dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),paired_final_state_measurements=pairs,
        full_screen_sheets=fullscreens,actual_consumer_menu_sheets=d['review_sheets'],visual_review_pending=True,
        six_cold_boots13001_frames_each78006_total=True,all_source_conditions_RNG_and_funds_unforced=True,
        actual_13_unique_speech_panels24_speech_observations13_menu_cases=True,
        eleven_unvisited_speech_objects_remain_native_offline_coverage=True,
        no_difference_in_measured_command_timings_or_sampled_postscene_RGB=True,
        no_causal_future_world_full_RAM_hardware_or_original_event_eligibility_claim=True,
        item_presentation_and_notice_not_a_complete_inventory_semantics_audit=True,
        evidence=evidence,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(ROOT/'three_paths_final_state_and_full_screen_analysis.json',json.loads(json.dumps(result,default=native_json)))
    print([(p['path'],p['PRNG_seeds'],p['five_native_component_equality']) for p in pairs])
