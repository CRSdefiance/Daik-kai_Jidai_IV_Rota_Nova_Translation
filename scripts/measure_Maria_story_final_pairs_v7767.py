"""Measure all actual scene pairs, timings andlate-state differences without causal claims."""
import inspect
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_shipyard_gameplay_v760 import models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_ceremony_prayer_gameplay_v814 import calendar
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_story_final_comparison_v7767')
ACTUAL=Path('work/analysis/maria_story_final_actual_binding_v7766/six_final_v3_actual_groups_two_fresh_four_exact_reused.json')
if __name__=='__main__':
    assert not ROOT.exists();actual=read(ACTUAL);assert not actual['unresolved'];groups=[];ROOT.mkdir(parents=True);sheets=[]
    for number in [34,108]:
        source,english=[next(g for g in actual['groups'] if g['block']==number and g['version']==v) for v in ['clean_Japanese','English']]
        assert source['input_schedule_sha256']==english['input_schedule_sha256'];pairs=[]
        for a,b in zip(source['speech_observations'],english['speech_observations'],strict=True):
            assert a['id']==b['id'] and a['source_selector']==b['source_selector'] and a['actual_name']==b['actual_name']
            ha,hb=[s['pages'][0]['complete_body_andname_holds'][-1] for s in [a,b]]
            ia,ib=[Image.open(h['capture']).convert('RGB') for h in [ha,hb]]
            pairs.append(dict(id=a['id'],source_selector=a['source_selector'],name=a['actual_name'],source_capture=ha,English_capture=hb,
                whole_upper_scene_portrait_header_RGB_equal=ia.crop((0,0,256,296)).tobytes()==ib.crop((0,0,256,296)).tobytes(),
                portrait_header_RGB_equal=ia.crop((0,192,256,296)).tobytes()==ib.crop((0,192,256,296)).tobytes(),
                upper_scene_RGB_equal=ia.crop((0,0,256,192)).tobytes()==ib.crop((0,0,256,192)).tobytes()))
        differences=[];durations=[];result_diffs=[];UI_diffs=[]
        for i,(a,b) in enumerate(zip(source['command_pairs'],english['command_pairs'],strict=True)):
            assert a['exchange_command_ordinal']==b['exchange_command_ordinal'] and a['canonical_source_offset']==b['canonical_source_offset'] and a['word']==b['word']
            if a['native_result']!=b['native_result']:result_diffs.append(dict(index=i,source=a['native_result'],English=b['native_result']))
            if a['UI_after']!=b['UI_after']:UI_diffs.append(dict(index=i,source=a['UI_after'],English=b['UI_after']))
            fields={k:dict(source=a[k],English=b[k]) for k in ['start','returned','decoded_length','before_RNG','after_RNG'] if a[k]!=b[k]}
            if fields:differences.append(dict(index=i,canonical_source_offset=a['canonical_source_offset'],exchange_command_ordinal=a['exchange_command_ordinal'],different_fields=fields))
            da,db=a['returned']-a['start'],b['returned']-b['start']
            if da!=db:durations.append(dict(index=i,canonical_source_offset=a['canonical_source_offset'],source_duration=da,English_duration=db))
        values=[];photos=[]
        for proof in [source,english]:
            report=read(proof['capture_report']);snap=report['read_only_RAM_snapshot'];raw=Path(snap['path']).read_bytes()
            assert snap['read_only_export'] and len(raw)==4194304 and sha(raw)==snap['sha256']
            arm=NdsImage.open(proof['fixture']['research_ROM']).read_file('/__arm9__.bin')
            assert sha(arm)=='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
            cpu,get=get_machine(arm,raw);actor=get(0xCB184);captain=get(0x7F244);assert captain==3
            components={fn.__name__:fn(arm,raw) for fn in [state,models,persistent_objects,tasks,calendar]}
            components['tasks']=dict(bytes=len(components['tasks']),sha256=sha(components['tasks']))
            values.append(dict(version=proof['version'],snapshot=snap,components=components,
                whole_actor_sha256=sha(bytes(cpu.mem_read(actor,0x1A04))),captain_ID=captain,PRNG_seed=int.from_bytes(raw[0x168EB8:0x168EBC],'little')))
            photos.append({p['frame']:p for p in report['frames_captured']})
        threshold=max(source['exit_frame'],english['exit_frame'])+60;frames=sorted(f for f in photos[0] if f>threshold and f in photos[1]);assert frames
        rgb=[]
        for frame in frames:
            a,b=[Image.open(p[frame]['path']).convert('RGB') for p in photos];delta=ImageChops.difference(a,b)
            rgb.append(dict(frame=frame,source=photos[0][frame],English=photos[1][frame],whole_RGB_equal=a.tobytes()==b.tobytes(),
                changed_RGB_bbox=delta.getbbox(),source_RGB_sha256=sha(a.tobytes()),English_RGB_sha256=sha(b.tobytes())))
        chosen=[frames[0],frames[len(frames)//2],frames[-1]];sheet=Image.new('RGB',(1536,410),'#263238');draw=ImageDraw.Draw(sheet)
        for i,frame in enumerate(chosen):
            for j,p in enumerate(photos):
                x=(i*2+j)*256;draw.text((x+3,3),f'B{number} '+('JP' if j==0 else 'EN')+f' frame{frame}',fill='white')
                sheet.paste(Image.open(p[frame]['path']).convert('RGB'),(x,24))
        path=ROOT/f'B{number}_unmasked_return_midpoint_final_pairs.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
        equality={k:values[0]['components'][k]==values[1]['components'][k] for k in values[0]['components']}
        groups.append(dict(block=number,source_English_exits=[source['exit_frame'],english['exit_frame']],scene_portrait_header_pairs=pairs,
            actual_initializer_andexchange_result_differences=result_diffs,actual_UI_request_differences=UI_diffs,
            command_comparison_differences=differences,duration_differences=durations,final_native_values=values,
            five_native_component_equality=equality,whole_actors_equal=values[0]['whole_actor_sha256']==values[1]['whole_actor_sha256'],
            final_PRNG_seeds=[v['PRNG_seed'] for v in values],later_full_RGB_comparisons=rgb,later_RGB_differences=[r for r in rgb if not r['whole_RGB_equal']],
            later_sample_count=len(rgb),selected_unmasked_late_frames=chosen,
            source_andEnglish_following_commands=[source['following_commands'],english['following_commands']],
            unreturned_following_dialogues=[source['unreturned_following_dialogues'],english['unreturned_following_dialogues']],
            raw_calendars_no_invented_date_interpretation=[v['components']['calendar'] for v in values]))
        print('COMPARE',number,'pairs',len(pairs),'upperRGBsame',sum(p['whole_upper_scene_portrait_header_RGB_equal'] for p in pairs),
            'results/UI diffs',len(result_diffs),len(UI_diffs),'command/duration diffs',len(differences),len(durations),
            'components',equality,'actorSame',groups[-1]['whole_actors_equal'],'seeds',groups[-1]['final_PRNG_seeds'],
            'lateRGBdifferences',len(groups[-1]['later_RGB_differences']),'of',len(rgb),flush=True)
    save(ROOT/'two_final_pairs_measured_portraits_timing_RNG_states_RGB_limits.json',dict(
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),groups=groups,review_sheets=sheets,review_sheets_visual_pending=True,
        all_measured_differences_preserved_no_controller_retiming_RNG_orstate_forcing=True,
        no_fullRAM_everyframe_futuresequence_broad_simulation_orcausal_equivalence_claim=True,
        incidental_later_Chun_no_sailors_food_water_andnavigation_messages_no_new_editorial_credit=True,
        later_older_record_technical_reaudit_kept_separate_withall_measurements=True,
        source_owned_final_getter_sources={fn.__name__:inspect.getsource(fn) for fn in [state,models,persistent_objects,tasks,calendar]},
        evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,Path(__file__)]},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
