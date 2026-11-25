"""Measure paired B203 timing,state and complete transitions without broad equivalence claims."""
import argparse,inspect
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
ROOT=Path('work/analysis/lil_B203_actual_review_v6045')
ACTUAL=Path('work/analysis/lil_B203_actual_v6044/twenty_two_actual_panels_source_matched_controls_and_complete_native_holds.json')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['stage','viewed']);mode=parser.parse_args().phase
    if mode=='stage':
        assert not ROOT.exists();d=read(ACTUAL);assert not d['failures'] and not d['paired_region_differences'] and d['complete_matching_holds']==86 and d['actual_unique_speech_panels']==d['complete_matching_observations']==22
        assert [v['fixture_exit_frame'] for v in d['versions']]==[8374,8373] and len(d['actual_timing_differences'])==23 and len(d['later_whole_RGB_differences'])==18
        evidence={str(ACTUAL):sha(ACTUAL.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())};measured=[];photos={};arms=[];rng=[];duration=[]
        for v in d['versions']:
            rp=Path(v['capture_report']);r=read(rp);snap=r['read_only_RAM_snapshot'];raw=Path(snap['path']).read_bytes();assert snap['read_only_export'] and len(raw)==4194304 and sha(raw)==snap['sha256'];arm=NdsImage.open(r['ROM']).read_file('/__arm9__.bin');arms.append(arm)
            values={fn.__name__:fn(arm,raw) for fn in [state,models,persistent_objects,tasks,calendar]};values['tasks']=dict(bytes=len(values['tasks']),sha256=sha(values['tasks']));cpu,get=get_machine(arm,raw);actor,captain=get(0xCB184),get(0x7F244);assert captain==2 and 0x02000000<=actor<=0x02400000-0x1A04
            measured.append(dict(case=v['case'],snapshot=snap,components=values,whole_actor_hex=bytes(cpu.mem_read(actor,0x1A04)).hex(),captain_ID=captain,seed=int.from_bytes(raw[0x168EB8:0x168EBC],'little')));photos[v['case']]={p['frame']:p for p in r['frames_captured']};evidence[str(rp)]=sha(rp.read_bytes());evidence[snap['path']]=snap['sha256']
        assert arms[0]==arms[1]
        for a,b in zip(d['versions'][0]['command_pairs'],d['versions'][1]['command_pairs'],strict=True):
            assert (a['source_offset'],a['word'],a['native_result'])==(b['source_offset'],b['word'],b['native_result'])
            da,db=a['returned']-a['start'],b['returned']-b['start']
            if da!=db:duration.append(dict(source_offset=a['source_offset'],word=a['word'],source_duration=da,English_duration=db,delta=db-da))
            if (a['before_RNG'],a['after_RNG'])!=(b['before_RNG'],b['after_RNG']):rng.append(dict(source_offset=a['source_offset'],word=a['word'],Japanese=[a['before_RNG'],a['after_RNG']],English=[b['before_RNG'],b['after_RNG']]))
        assert all(r['word']==0x4000 for r in duration)
        assert all(r['difference_bbox']==[224,360,240,376] and r['nontext_region_difference_bbox'] is None for r in d['later_whole_RGB_differences'])
        selected=[('speech '+str(i),next(r for r in d['actual_panels'] if r['id']==f'DK4_MES_B203_R{i:04d}')['holds'][-1]['frame']) for i in [21,35,54,67,70,80]]
        selected += [('offer1000',next(r for r in d['actual_panels'] if r['id'].endswith('0074'))['holds'][-1]['frame']),('accept100',next(r for r in d['actual_panels'] if r['id'].endswith('0077'))['holds'][-1]['frame']),('generated acquisition',8350),('following B43',8410),('later town',12970),('prompt sample',d['later_whole_RGB_differences'][0]['frame'])]
        assert next(r for r in d['all_sampled_frame_comparisons'] if r['frame']==8350)['whole_RGB_equal']
        ROOT.mkdir(parents=True);sheets=[]
        for start in range(0,len(selected),6):
            sheet=Image.new('RGB',(1536,820),'#263238');draw=ImageDraw.Draw(sheet)
            for i,(label,frame) in enumerate(selected[start:start+6]):
                x,y=i%3*512,i//3*410
                for j,case in enumerate(['clean_Japanese','reviewed_English']):
                    p=photos[case][frame];assert sha(Path(p['path']).read_bytes())==p['PNG_sha256'];pic=Image.open(p['path']).convert('RGB');assert pic.size==(256,384);draw.text((x+256*j+3,y+3),case+' '+label+' '+str(frame),fill='white');sheet.paste(pic,(x+256*j,y+24));evidence[p['path']]=p['PNG_sha256']
            p=ROOT/f'paired_complete_scene_return_sheet{start//6+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
        equality={k:measured[0]['components'][k]==measured[1]['components'][k] for k in measured[0]['components']}
        save(ROOT/'paired_transitions_timing_RNG_and_native_state.json',dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),native_final_component_equality=equality,native_final_state_measurements=measured,whole_actor_and_captain_equal=measured[0]['whole_actor_hex']==measured[1]['whole_actor_hex'],final_PRNG_equal=measured[0]['seed']==measured[1]['seed'],original_native_getters={fn.__name__:inspect.getsource(fn) for fn in [state,models,persistent_objects,tasks,calendar]},
            actual_command_duration_changes=duration,within_scene_RNG_differences=rng,command_start_return_differences=d['actual_timing_differences'],later_whole_RGB_differences=d['later_whole_RGB_differences'],all_later_differences_bounded_to_advance_prompt=True,source_English_exit_frames=[8374,8373],complete_source_matched_native_holds=86,
            all_actual_consumer_sheets=d['review_sheets'],paired_full_screen_sheets=sheets,visual_review_pending=True,source_only_names_title_context_and_prior_artifacts_preserved=True,generated_item_acquired_notice_same_frame_whole_RGB_equal_at8350=True,
            no_causal_explanation_full_RAM_future_RNG_or_broad_simulation_equivalence_claim=True,no_masking_retiming_or_pixel_edit=True,native_getters_only_on_exported_copies=True,
            original_inputs_roster_funds_conditions_RNG_and_results_unforced=True,initialized_Amsterdam_B22_not_natural_event203_activation_original_location_earned_inventory_full_route_or_hardware=True,
            following_B43_source_item_and_Local_Product_terminology_unresolved_no_new_credit=True,
            new_English_cold_boots=1,new_English_frames=13001,reused_prior_Japanese_cold_boots=1,reused_prior_Japanese_frames=13001,total_successful_paired_frames=26002,terminal_reaped_English_session=26932,evidence=evidence,full_goal_complete=False))
        print(dict(final_native_groups=equality,actor_equal=measured[0]['whole_actor_hex']==measured[1]['whole_actor_hex'],PRNG=[m['seed'] for m in measured],duration_changes=duration,RNG_witnesses=len(rng),sheets=len(sheets)))
    else:
        p=ROOT/'paired_transitions_timing_RNG_and_native_state.json';d=read(p);out=ROOT/'viewed22_panels_complete_return_and_honest_measured_scope.json';assert not out.exists();actual=read(d['actual_proof']);assert sha(Path(d['actual_proof']).read_bytes())==d['actual_proof_sha256']
        sheets=d['all_actual_consumer_sheets']+d['paired_full_screen_sheets'];assert len(sheets)==6
        for s in sheets:assert sha(Path(s['path']).read_bytes())==s['sha256']
        save(out,dict(previous_visual_analysis=str(p),previous_visual_analysis_sha256=sha(p.read_bytes()),actual_proof=d['actual_proof'],actual_proof_sha256=d['actual_proof_sha256'],viewed_sheets=[dict(**s,viewed=True,viewed_after_image_return=True,original_detail=True) for s in sheets],
            review='Viewed all22 complete English panels and both full-screen paired sheets. The uncertain specimen observation,Chinese medicinal context,unspoken-title book explanation,expensive-looking gift hesitation,teasing companion interest and embarrassed reading request retain the full source exchange. R67 keeps the teasing clause intact after the chuckle;R70 keeps the reading admission intact after the hesitant reaction. The1000/100 gold proposals remain distinct and prospective,and the FE/FI notice remains a separate Charm+1 display. Original Lil/Mikhail/Mysterious Old Man portraits,nameplates and Mikhail middle-name omission agree;Unknown nationality remains metadata. The existing book card and generated acquired notice are unchanged. No dropped glyph,clipping,overflow,unintended or blank page was found. Both versions complete B203 and continue to unchanged B43 teaching dialogue,then later town/port UI. Source item/Local Product wording stays an unresolved separate lead. Eighteen later differences are advance-prompt pixels. Native queried final-state and PRNG measurements are retained separately;no full causal or broad simulation-equivalence claim.',
            actual_unique_speech_panels=22,complete_native_holds=86,offline_only_display_IDs=[],all31_original_commands_and9_initializers_observed=True,all86_complete_holds_match_same_frame_source_upper_portrait_name_picture_regions=True,
            original_command_words_paths_results_and_input_schedule_equal=True,no_open_translation_specific_display_control_or_return_finding=True,representative_shared_rules_approved=True,English_scene_and_source_returns_observed=True,generated_item_acquired_notice_same_frame_whole_RGB_equal_at8350=True,
            source_English_exit_frames=d['source_English_exit_frames'],command_timing_differences=23,later_prompt_differences=18,all_later_differences_bounded_to_advance_prompt=True,
            measured_state_proof=str(p),measured_state_proof_sha256=sha(p.read_bytes()),native_final_component_equality=d['native_final_component_equality'],whole_actor_and_captain_equal=d['whole_actor_and_captain_equal'],final_PRNG_equal=d['final_PRNG_equal'],
            no_causal_explanation_full_RAM_future_RNG_or_broad_simulation_equivalence_claim=True,no_pixels_masked_retimed_or_edited=True,
            no_natural_event203_activation_original_location_earned_inventory_full_effects_full_route_or_hardware_claim=True,
            new_English_runs=1,new_English_frames=13001,reused_prior_source_runs=1,reused_prior_source_frames=13001,total_successful_frames=26002,all_jobs_terminal_and_reaped=True,registered_release_and_current_startup_pending=True,visual_review_pending=False,evidence={**d['evidence'],str(p):sha(p.read_bytes())},new_review_credit=0,full_goal_complete=False))
        print('Six actual/full-screen sheets viewed;22 panels/86 native holds and complete return approved. Timing/RNG/state limitations retained;registered integration pending.')
