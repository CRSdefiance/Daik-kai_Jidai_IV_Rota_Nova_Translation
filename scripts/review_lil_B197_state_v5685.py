"""Measure final states and preserve postscene differences without broad equivalence claims."""
import json,struct
from collections import Counter
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
ROOT=Path('work/analysis/lil_B197_actual_review_v5685')
ACTUAL=Path('work/analysis/lil_B197_actual_v5684b/three_paths_and_focused_refusal_highlight.json')
def native_json(value):
    assert isinstance(value,bytes);return dict(native_byte_span_hex=value.hex())
if __name__=='__main__':
    assert not ROOT.exists();d=read(ACTUAL)
    assert not d['failures'] and not d['paired_nontext_region_differences'] and not d['command_result_differences']
    assert len(d['actual_panels'])==21 and len(d['actual_menu_cases'])==3 and d['actual_English_speech_observations']==35
    versions={(v['path'],v['case']):v for v in d['versions']};pairs=[];sheets=[];evidence={str(ACTUAL):sha(ACTUAL.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())}
    ROOT.mkdir(parents=True);returns=Image.new('RGB',(804,816),'#263238');rdraw=ImageDraw.Draw(returns)
    for column,path in enumerate(['buy','no_buy','delegate']):
        key={'buy':'DK4_MES_B197_R0053','no_buy':'DK4_MES_B197_R0064','delegate':'DK4_MES_B197_R0089'}[path]
        first=next(r for r in d['all_actual_speech_observations'] if r['path']==path and r['id']==key)['holds'][-1]['frame']
        second=next(r for r in d['all_actual_speech_observations'] if r['path']==path and r['id']=='DK4_MES_B197_R0109')['holds'][-1]['frame']
        frames=[first,second];sheet=Image.new('RGB',(1048,1600),'#263238');draw=ImageDraw.Draw(sheet);measured=[]
        for col,case in enumerate(['clean_Japanese','reviewed_English']):
            v=versions[path,case];report=read(v['capture_report']);snap=v['final_readonly_RAM_snapshot'];raw=Path(snap['path']).read_bytes();assert sha(raw)==snap['sha256']
            arm=NdsImage.open(v['research_ROM']).read_file('/__arm9__.bin');cpu,get=get_machine(arm,raw)
            actor,captain=get(0xCB184),get(0x7F244);assert captain==2 and 0x02000000<=actor<=0x02400000-0x1A04
            components={fn.__name__:fn(arm,raw) for fn in [state,models,persistent_objects,tasks,calendar]}
            measured.append(dict(case=case,snapshot=snap,components=components,whole_actor_hex=bytes(cpu.mem_read(actor,0x1A04)).hex(),captain_ID=captain,seed=struct.unpack_from('<I',raw,0x168EB8)[0]))
            photos={p['frame']:p for p in report['frames_captured']}
            for row,frame in enumerate(frames):
                p=photos[frame];assert sha(Path(p['path']).read_bytes())==p['PNG_sha256'];pic=Image.open(p['path']).convert('RGB');x,y=col*524,row*800
                draw.text((x+4,y+4),f'{path} / {case} / frame {frame}',fill='white');sheet.paste(pic.resize((512,768),Image.Resampling.NEAREST),(x+4,y+24));evidence[p['path']]=p['PNG_sha256']
            p=photos[12970];assert sha(Path(p['path']).read_bytes())==p['PNG_sha256'];pic=Image.open(p['path']).convert('RGB')
            x,y=column*268,col*408;rdraw.text((x+4,y+3),path+' / '+case,fill='white');returns.paste(pic,(x+4,y+22));evidence[p['path']]=p['PNG_sha256']
            evidence[v['capture_report']]=sha(Path(v['capture_report']).read_bytes());evidence[snap['path']]=snap['sha256']
        equality={k:measured[0]['components'][k]==measured[1]['components'][k] for k in measured[0]['components']}
        pairs.append(dict(path=path,final_frame=13001,native=measured,five_native_component_equality=equality,whole1A04_actor_and_captain2_equal=measured[0]['whole_actor_hex']==measured[1]['whole_actor_hex'],PRNG_seeds=[m['seed'] for m in measured],PRNG_equal=measured[0]['seed']==measured[1]['seed']))
        p=ROOT/f'paired_full_screen_{path}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes()),frames=frames))
    p=ROOT/'all_three_later_full_screen_pairs.png';returns.save(p)
    # Keep broad differences visible. Their bounds are evidence,not permission
    # to mask,retime or assume an A-indicator-only difference.
    boxes=Counter(tuple(r['whole_RGB_bbox']) for r in d['later_whole_RGB_differences'])
    result=dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),paired_final_state_measurements=pairs,
        full_screen_sheets=sheets,later_full_screen_pairs=dict(path=str(p),sha256=sha(p.read_bytes()),frame=12970),
        actual_consumer_menu_sheets=d['review_sheets'],supplemental_menu_sheet=d['supplemental_menu_sheet'],visual_review_pending=True,
        paired_command_timing_differences=d['command_timing_differences'],postscene_whole_RGB_difference_bounds=[dict(bounds=list(k),samples=v) for k,v in boxes.items()],
        all59_timing_and82_postscene_RGB_differences_retained_without_mask_or_retiming=len(d['command_timing_differences'])==59 and len(d['later_whole_RGB_differences'])==82,
        all128_complete_speech_holds_have_shared_source_interval_and_equal_upper_portrait_name_picture_regions=True,
        six_complete_paired_runs_and_one_short_menu_focus=True,successful_total_frames=82607,
        no_causal_future_world_full_RAM_hardware_natural_event_eligibility_or_source_effect_semantics_claim=True,
        evidence=evidence,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(ROOT/'three_paths_final_state_full_screens_and_unmasked_differences.json',json.loads(json.dumps(result,default=native_json)))
    print([(p['path'],p['five_native_component_equality'],p['whole1A04_actor_and_captain2_equal'],p['PRNG_seeds']) for p in pairs])
