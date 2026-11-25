"""Measure actual scene pairs and later exported state without replay or timing assumptions."""
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
ROOT=Path('work/analysis/Rafael_B45_actual_comparison_v7896')
ACTUAL=Path('work/analysis/Rafael_B45_actual_v7895b/paired12_source_English_actual_body_name_FE_branch_andnormal_return_audit.json')
if __name__=='__main__':
    assert not ROOT.exists();actual=read(ACTUAL);groups=[];sheet=Image.new('RGB',(1536,410),'#263238');draw=ImageDraw.Draw(sheet)
    for route in [0]:
        source,english=[next(g for g in actual['groups'] if g['route']==route and g['version']==v) for v in ['clean_Japanese','English']]
        assert source['input_schedule_sha256']==english['input_schedule_sha256'];pairs=[]
        for a,b in zip(source['speech_observations'],english['speech_observations'],strict=True):
            assert a['id']==b['id'] and a['source_selector']==b['source_selector'] and a['actual_name']==b['actual_name']
            ha,hb=a['selected_capture'],b['selected_capture'];ia,ib=[Image.open(h['capture']).convert('RGB') for h in [ha,hb]]
            assert ia.crop((0,0,256,296)).tobytes()==ib.crop((0,0,256,296)).tobytes(),(route,a['id'])
            pairs.append(dict(id=a['id'],source_selector=a['source_selector'],name=a['actual_name'],source_capture=ha,English_capture=hb,whole_upper_scene_portrait_andcomplete_header_RGB_equal=True))
        diffs=[];durations=[]
        for i,(a,b) in enumerate(zip(source['command_pairs'],english['command_pairs'],strict=True)):
            assert a['exchange_command_ordinal']==b['exchange_command_ordinal'] and a['canonical_source_offset']==b['canonical_source_offset'] and a['word']==b['word']
            assert a['native_result']==b['native_result'] and a['UI_after']==b['UI_after']
            fields={k:dict(source=a[k],English=b[k]) for k in ['start','returned','decoded_length','before_RNG','after_RNG'] if a[k]!=b[k]}
            if fields:diffs.append(dict(index=i,canonical_source_offset=a['canonical_source_offset'],exchange_command_ordinal=a['exchange_command_ordinal'],different_fields=fields))
            da,db=a['returned']-a['start'],b['returned']-b['start']
            if da!=db:durations.append(dict(index=i,canonical_source_offset=a['canonical_source_offset'],source_duration=da,English_duration=db))
        values=[];reports=[];photos=[]
        for proof in [source,english]:
            report=read(proof['capture_report']);reports.append(report);snap=report['read_only_RAM_snapshot'];raw=Path(snap['path']).read_bytes()
            assert snap['read_only_export'] and len(raw)==4194304 and sha(raw)==snap['sha256']
            arm=NdsImage.open(proof['fixture']['research_ROM']).read_file('/__arm9__.bin');assert sha(arm)=='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
            cpu,get=get_machine(arm,raw);actor=get(0xCB184);captain=get(0x7F244);assert captain==route
            components={fn.__name__:fn(arm,raw) for fn in [state,models,persistent_objects,tasks,calendar]};components['tasks']=dict(bytes=len(components['tasks']),sha256=sha(components['tasks']))
            values.append(dict(version=proof['version'],snapshot=snap,components=components,whole_actor_sha256=sha(bytes(cpu.mem_read(actor,0x1A04))),captain_ID=captain,PRNG_seed=int.from_bytes(raw[0x168EB8:0x168EBC],'little')))
            photos.append({p['frame']:p for p in report['frames_captured']})
        threshold=max(source['exit_frame'],english['exit_frame'])+60;frames=sorted(f for f in photos[0] if f>threshold and f in photos[1]);assert frames[0]==6730 and frames[-1]==16001
        rgb=[]
        for f in frames:
            a,b=[Image.open(p[f]['path']).convert('RGB') for p in photos];delta=ImageChops.difference(a,b)
            rgb.append(dict(frame=f,source=photos[0][f],English=photos[1][f],whole_RGB_equal=a.tobytes()==b.tobytes(),changed_RGB_bbox=delta.getbbox(),source_RGB_sha256=sha(a.tobytes()),English_RGB_sha256=sha(b.tobytes())))
        chosen=[frames[0],frames[len(frames)//2],frames[-1]]
        for i,f in enumerate(chosen):
            for j,p in enumerate(photos):
                x,y=(i*2+j)*256,route*410;draw.text((x+3,y+3),f'route{route} '+('JP' if j==0 else 'EN')+f' frame{f}',fill='white');sheet.paste(Image.open(p[f]['path']).convert('RGB'),(x,y+24))
        equality={k:values[0]['components'][k]==values[1]['components'][k] for k in values[0]['components']}
        groups.append(dict(route=route,route_identity=source['route_identity'],source_English_exits=[source['exit_frame'],english['exit_frame']],scene_portrait_header_pairs=pairs,all12_whole_upper_scene_portrait_andheader_RGB_equal=True,all_original_initializer_andexchange_results_andUI_words_equal=True,command_comparison_differences=diffs,duration_differences=durations,final_native_values=values,five_native_component_equality=equality,captain_IDs=[v['captain_ID'] for v in values],whole_actors_equal=values[0]['whole_actor_sha256']==values[1]['whole_actor_sha256'],final_PRNG_seeds=[v['PRNG_seed'] for v in values],later_full_RGB_comparisons=rgb,later_RGB_differences=[r for r in rgb if not r['whole_RGB_equal']],later_sample_count=len(rgb),selected_unmasked_late_frames=chosen,source_andEnglish_following_commands=[source['following_commands'],english['following_commands']],unreturned_following_dialogues=[source['unreturned_following_dialogues'],english['unreturned_following_dialogues']],raw_calendars_no_invented_date_interpretation=[v['components']['calendar'] for v in values]))
        print(dict(route=route,scene_pairs=12,exits=groups[-1]['source_English_exits'],command_diffs=len(diffs),duration_diffs=len(durations),components=equality,actors_equal=groups[-1]['whole_actors_equal'],seeds=groups[-1]['final_PRNG_seeds'],RGB_differences=len(groups[-1]['later_RGB_differences']),late_samples=len(rgb)))
    ROOT.mkdir(parents=True);path=ROOT/'Rafael_unmasked_return_midpoint_final_source_English_pairs.png';sheet.save(path)
    save(ROOT/'12_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGB_limits.json',dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),groups=groups,all12_source_English_upper_scene_portrait_complete_header_pairs_equal=True,all_actual_body_andsource_control_checks_pass_independently=True,review_sheet=str(path),review_sheet_sha256=sha(path.read_bytes()),review_sheet_visual_pending=True,no_controller_retiming_RNG_orstate_forcing_ornew_emulator_runs=True,no_full_RAM_every_frame_future_sequence_broad_simulation_orcausal_equivalence_claim=True,incidental_following_dialogue_sailing_andresource_messages_no_new_editorial_credit=True,all_measured_differences_preserved_for_later_older_record_technical_reaudit=True,source_owned_final_getter_sources={fn.__name__:inspect.getsource(fn) for fn in [state,models,persistent_objects,tasks,calendar]},producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
