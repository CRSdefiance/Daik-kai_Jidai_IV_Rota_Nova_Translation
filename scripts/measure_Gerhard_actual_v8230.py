"""Measure paired selected scenes, timing/RNG and bounded later captures/state without replay."""
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
ROOT=Path('work/analysis/Gerhard_actual_comparison_v8230')
ACTUAL=Path('work/analysis/Gerhard_actual_v8229/six_paired_runs_actual_five_surname_bodies_headers_conditions_andnormal_returns.json')
REFERENCE=Path('work/analysis/Gerhard_reference_v8215/research_image_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists();actual,reference=map(read,[ACTUAL,REFERENCE]);assert not actual['unresolved']
    ROOT.mkdir(parents=True);groups=[];sheets=[]
    for scope,number in [('whole',27),('whole',74),('intro-display',27)]:
        previous,revised=[next(g for g in actual['groups'] if g['scope']==scope and g['block']==number and g['version']==version) for version in ['parent_English','revised_English']]
        reports=[read(g['capture_report']) for g in [previous,revised]]
        assert reports[0]['scripted_input_schedule']==reports[1]['scripted_input_schedule']
        photos=[{p['frame']:p for p in report['frames_captured']} for report in reports];images={}
        def picture(which,frame):
            key=which,frame
            if key not in images:
                p=photos[which][frame];path=Path(p['path']);assert sha(path.read_bytes())==p['PNG_sha256'];images[key]=Image.open(path).convert('RGB')
            return images[key]
        scenes=[];no_common=[]
        for a,b in zip(previous['speeches'],revised['speeches'],strict=True):
            assert a['id']==b['id'] and a['source_selector']==b['source_selector']
            first=max(a['start'],b['start'])+20;last=min(a['returned'],b['returned'])-4
            common=sorted(f for f in photos[0] if f in photos[1] and first<f<last)
            if not common:no_common.append(dict(id=a['id'],source_selector=a['source_selector'],parent_interval=[a['start'],a['returned']],revised_interval=[b['start'],b['returned']]));continue
            frame=common[-1];ia,ib=picture(0,frame),picture(1,frame)
            scenes.append(dict(id=a['id'],source_selector=a['source_selector'],frame=frame,parent_capture=photos[0][frame],revised_capture=photos[1][frame],
                upper_scene_andportrait_RGB_equal=ia.crop((0,0,256,272)).tobytes()==ib.crop((0,0,256,272)).tobytes(),
                whole_header_region_RGB_equal=ia.crop((0,272,256,296)).tobytes()==ib.crop((0,272,256,296)).tobytes(),
                Gerhard_header_spelling_andwidth_change_expected=a['source_selector']==16,
                exact_name_ink_coverage_is_separate262_hold_native_mask_proof=True))
        differences=[];durations=[]
        for i,(a,b) in enumerate(zip(previous['command_pairs'],revised['command_pairs'],strict=True)):
            assert (a['source_command_ordinal'],a['word'],a['native_result'])==(b['source_command_ordinal'],b['word'],b['native_result'])
            fields={k:dict(parent=a[k],revised=b[k]) for k in ['start','returned','decoded_length','before_RNG','after_RNG','UI_before','UI_after'] if a[k]!=b[k]}
            if fields:differences.append(dict(index=i,canonical_source_offset=a['canonical_source_offset'],word=a['word'],different_fields=fields))
            if a['duration']!=b['duration']:durations.append(dict(index=i,canonical_source_offset=a['canonical_source_offset'],word=a['word'],parent=a['duration'],revised=b['duration']))
        values=[]
        for proof,report in zip([previous,revised],reports,strict=True):
            snap=report['read_only_RAM_snapshot'];raw=Path(snap['path']).read_bytes();assert snap['read_only_export'] and len(raw)==4194304 and sha(raw)==snap['sha256']
            arm=NdsImage.open(proof['fixture']['research_ROM']).read_file('/__arm9__.bin')
            assert sha(arm)==reference['current_ARM9_sha256' if proof['version']=='parent_English' else 'research_ARM9_sha256']
            if proof['version']=='revised_English':
                slot=reference['only_changed_name_span'];inverse=bytearray(arm);inverse[slot['offset']:slot['offset']+12]=bytes.fromhex(slot['current_hex']);assert sha(bytes(inverse))==reference['current_ARM9_sha256']
            cpu,get=get_machine(arm,raw);actor=get(0xCB184);captain=get(0x7F244);assert captain==2
            components={fn.__name__:fn(arm,raw) for fn in [state,models,persistent_objects,tasks,calendar]}
            components['tasks']=dict(bytes=len(components['tasks']),sha256=sha(components['tasks']))
            values.append(dict(version=proof['version'],snapshot=snap,components=components,whole_actor_sha256=sha(bytes(cpu.mem_read(actor,0x1A04))),captain_ID=captain,
                PRNG_seed=int.from_bytes(raw[0x168EB8:0x168EBC],'little'),native_component_queries_on_disposable_CPU_only_not_mutating_emulator=True))
        threshold=max(previous['normal_return']['frame'],revised['normal_return']['frame'])+60
        frames=sorted(f for f in photos[0] if f>threshold and f in photos[1]);assert frames
        rgb=[]
        for frame in frames:
            ia,ib=picture(0,frame),picture(1,frame);delta=ImageChops.difference(ia,ib)
            rgb.append(dict(frame=frame,parent=photos[0][frame],revised=photos[1][frame],whole_RGB_equal=ia.tobytes()==ib.tobytes(),changed_RGB_bbox=delta.getbbox(),
                parent_RGB_sha256=sha(ia.tobytes()),revised_RGB_sha256=sha(ib.tobytes())))
        chosen=[frames[0],frames[len(frames)//2],frames[-1]];sheet=Image.new('RGB',(1536,410),'#263238');draw=ImageDraw.Draw(sheet)
        for i,frame in enumerate(chosen):
            for j,label in enumerate(['previous','revised']):
                x=(i*2+j)*256;draw.text((x+3,3),label+f' {scope} B{number} frame{frame}',fill='white');sheet.paste(picture(j,frame),(x,24))
        path=ROOT/f'{scope}_B{number}_return_midpoint_final_pairs.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
        equality={k:values[0]['components'][k]==values[1]['components'][k] for k in values[0]['components']}
        group=dict(scope=scope,block=number,selected_scene_andportrait_pairs=scenes,no_common_held_scene_capture=no_common,
            upper_scene_portrait_RGB_difference_IDs=[r['id'] for r in scenes if not r['upper_scene_andportrait_RGB_equal']],
            unchanged_actor_header_RGB_difference_IDs=[r['id'] for r in scenes if r['source_selector']!=16 and not r['whole_header_region_RGB_equal']],
            original_results_membership_andchoice_result_equal=True,command_comparison_differences=differences,duration_differences=durations,
            all_UI_request_words_equal=all(a['UI_before']==b['UI_before'] and a['UI_after']==b['UI_after'] for a,b in zip(previous['command_pairs'],revised['command_pairs'],strict=True)),
            normal_returns=[previous['normal_return'],revised['normal_return']],final_native_values=values,five_native_component_equality=equality,
            captain_IDs=[v['captain_ID'] for v in values],whole_actors_equal=values[0]['whole_actor_sha256']==values[1]['whole_actor_sha256'],final_PRNG_seeds=[v['PRNG_seed'] for v in values],
            later_full_RGB_comparisons=rgb,later_RGB_differences=[r for r in rgb if not r['whole_RGB_equal']],later_sample_count=len(rgb),selected_unmasked_late_frames=chosen,
            raw_calendars_no_invented_date_interpretation=[v['components']['calendar'] for v in values],
            following_commands_equal=previous['following_original_cache_commands']==revised['following_original_cache_commands'],
            following_commands=[previous['following_original_cache_commands'],revised['following_original_cache_commands']])
        groups.append(group)
        print(scope,number,'sceneRGBdiff',len(group['upper_scene_portrait_RGB_difference_IDs']),'unchangedHeaderDiff',len(group['unchanged_actor_header_RGB_difference_IDs']),
            'commanddiff',len(differences),'durationdiff',len(durations),'UIequal',group['all_UI_request_words_equal'],'components',equality,
            'actorsEqual',group['whole_actors_equal'],'seeds',group['final_PRNG_seeds'],'laterRGB',len(group['later_RGB_differences']),'of',len(rgb),flush=True)
    save(ROOT/'three_actual_pairs_scene_timing_RNG_final_components_later_RGB_scope.json',dict(
        actual=str(ACTUAL),actual_sha256=sha(ACTUAL.read_bytes()),groups=groups,review_sheets=sheets,visual_review_pending=True,
        all_measured_fields_retained_without_input_retiming_orstate_seed_forcing=True,
        Gerhard_nameplate_ink_andwidth_change_intentional_andcovered_by262_exact_actual_nameholds=True,
        source_scope_original_conditions_andfocused_intro_limits_preserved=True,
        no_every_frame_future_sequence_arbitrary_effect_causality_broad_simulation_orfullroute_equivalence_claim=True,
        later_older_record_technical_reaudit_retains_alltiming_RNG_andcomponent_limits=True,
        new_emulator_runs=0,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,REFERENCE,Path(__file__),*[Path(fn.__code__.co_filename) for fn in [state,models,persistent_objects,tasks,calendar]]]}))
    print('Measured3 actual pairs without replay;bounded later-state/RGB differences retained;direct review pending.')
