"""Preserve later timing/world differences and measure final exported state without another boot."""
import inspect
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
ROOT=Path('work/analysis/lil_B209_later_v6475')
ACTUAL=Path('work/analysis/lil_B209_actual_v6474/six_English_objects_eight_native_pages24_commands_and_source_differences.json')
if __name__=='__main__':
    assert not ROOT.exists();d=read(ACTUAL);source=read(d['source_actual_proof']);assert len(d['later_same_frame_RGB_differences'])==187 and not d['failures'];values=[];evidence={str(ACTUAL):sha(ACTUAL.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())}
    for language,snap,rom in [('source',d['final_source_snapshot'],source['research_ROM']),('English',d['final_English_snapshot'],d['candidate'])]:
        raw=Path(snap['path']).read_bytes();assert len(raw)==4194304 and sha(raw)==snap['sha256'];arm=NdsImage.open(rom).read_file('/__arm9__.bin');cpu,get=get_machine(arm,raw);actor,captain=get(0xCB184),get(0x7F244);assert captain==2 and 0x02000000<=actor<=0x02400000-0x1A04
        groups={f.__name__:f(arm,raw) for f in [state,models,persistent_objects,tasks,calendar]};groups['tasks']=dict(bytes=len(groups['tasks']),sha256=sha(groups['tasks']));values.append(dict(language=language,snapshot=snap,components=groups,whole_actor_hex=bytes(cpu.mem_read(actor,0x1A04)).hex(),captain_ID=captain,final_D0_actor=get(0x2434C,208),seed=int.from_bytes(raw[0x168EB8:0x168EBC],'little')));evidence[snap['path']]=snap['sha256']
    following=[]
    for language,commands in [('source',source['following_native_commands']),('English',d['following_commands'])]:
        ends=[r for r in commands if r['block']==120 and r['word']==0 and r['native_result'][0]==0];assert len(ends)==1;following.append(dict(language=language,B120_end_frame=ends[0]['frame'],B120_end=ends[0]))
    end=max(v['B120_end_frame'] for v in following);diffs=d['later_same_frame_RGB_differences'];prompt=lambda r:(lambda b:224<=b[0]<b[2]<=240 and 360<=b[1]<b[3]<=376)(r['bounds']);narrow=[r for r in diffs if prompt(r)];broad=[r for r in diffs if not prompt(r)]
    during=[r for r in diffs if r['frame']<=end];after=[r for r in diffs if r['frame']>end+60];selected=[broad[i] for i in [0,len(broad)//2,len(broad)-1]]
    ROOT.mkdir(parents=True);sheet=Image.new('RGB',(1536,410),'#263238');draw=ImageDraw.Draw(sheet)
    for i,r in enumerate(selected):
        for j,language in enumerate(['source','English']):
            p=Path(r[language+'_capture']);assert sha(p.read_bytes())==r[language+'_sha256'];x=i*512+j*256;draw.text((x+3,3),language+' frame'+str(r['frame']),fill='white');sheet.paste(Image.open(p).convert('RGB'),(x,24));evidence[str(p)]=sha(p.read_bytes())
    sp=ROOT/'first_middle_final_unmasked_later_source_English_pairs.png';sheet.save(sp);equal={k:values[0]['components'][k]==values[1]['components'][k] for k in values[0]['components']}
    save(ROOT/'all187_later_differences_original_final_getters_and_honest_scope.json',dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),native_values=values,five_native_component_equality=equal,whole_actor_and_captain_equal=values[0]['whole_actor_hex']==values[1]['whole_actor_hex'],final_PRNG_equal=values[0]['seed']==values[1]['seed'],final_PRNG_seeds=[v['seed'] for v in values],both_final_D0_fallbacks=[v['final_D0_actor'] for v in values],command_duration_changes=d['command_duration_changes'],source_English_scene_exits=[d['source_exit_frame'],d['English_exit_frame']],source_English_reading_time_difference_frames=d['English_exit_frame']-d['source_exit_frame'],following_B120_ends=following,all187_later_same_frame_RGB_differences=diffs,prompt_bounded_differences=narrow,broader_later_differences=broad,later_differences_while_either_following_B120_not_finished=during,later_differences_after_both_B120_ends_plus60=after,selected_first_middle_final_pairs=selected,review_sheet=dict(path=str(sp),sha256=sha(sp.read_bytes())),visual_review_pending=True,original_native_getter_sources={f.__name__:inspect.getsource(f) for f in [state,models,persistent_objects,tasks,calendar]},native_getters_run_only_on_readonly_export_copies=True,no_new_boot_state_injection_pixel_mask_edit_or_input_retiming=True,do_not_claim_same_later_dialogue_progression_or_final_sailing_notice=True,source_final_Arnhem_notice_and_English_final_unobstructed_sailing_reviewed_separately=True,no_whole_RAM_future_sequence_broad_simulation_equivalence_or_complete_cause_claim=True,measured_differences_retained_for_later_older_record_technical_reaudit=True,new_review_credit=0,new_emulator_runs=0,evidence=evidence,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(component_equality=equal,actor_equal=values[0]['whole_actor_hex']==values[1]['whole_actor_hex'],seeds=[v['seed'] for v in values],cash=[v['components']['state']['cash'] for v in values],calendar=[v['components']['calendar'] for v in values],D0=[v['final_D0_actor'] for v in values],B120_end_frames=[v['B120_end_frame'] for v in following],later_RGB=187,prompt_only=len(narrow),broader=len(broad),while_following_active=len(during),after_both_following=len(after)))
