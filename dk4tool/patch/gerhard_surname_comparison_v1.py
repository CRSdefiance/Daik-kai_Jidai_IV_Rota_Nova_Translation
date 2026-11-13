"""Recompute every saved timing difference, sampled RGB comparison and final native component value."""
from pathlib import Path
from PIL import Image,ImageChops
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_shipyard_gameplay_v760 import models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_ceremony_prayer_gameplay_v814 import calendar
from scripts.verify_personal_gameplay_v841 import get_machine

def check_comparisons(comparison,actual,parent,reference,load,require):
    require(len(comparison['groups'])==3,'three comparison scopes')
    counts=[]
    for declared,(scope,number) in zip(comparison['groups'],[('whole',27),('whole',74),('intro-display',27)],strict=True):
        require(declared['scope']==scope and declared['block']==number,'exact comparison scope')
        groups=[next(g for g in actual['groups'] if (g['scope'],g['block'],g['version'])==(scope,number,v)) for v in ['parent_English','revised_English']]
        reports=[load(g['capture_report']) for g in groups]
        require(reports[0]['scripted_input_schedule']==reports[1]['scripted_input_schedule'],'original unretimed controller schedule')
        photos=[{p['frame']:p for p in r['frames_captured']} for r in reports]
        def picture(which,frame):
            photo=photos[which][frame]
            require(sha(Path(photo['path']).read_bytes())==photo['PNG_sha256'],'sampled actual PNG integrity')
            return Image.open(photo['path']).convert('RGB')
        differences=[];durations=[];uiequal=True
        for i,(a,b) in enumerate(zip(groups[0]['command_pairs'],groups[1]['command_pairs'],strict=True)):
            require((a['source_command_ordinal'],a['word'],a['native_result'])==(b['source_command_ordinal'],b['word'],b['native_result']),'paired selected original membership/results')
            fields={k:dict(parent=a[k],revised=b[k]) for k in ['start','returned','decoded_length','before_RNG','after_RNG','UI_before','UI_after'] if a[k]!=b[k]}
            if fields:differences.append(dict(index=i,canonical_source_offset=a['canonical_source_offset'],word=a['word'],different_fields=fields))
            if a['duration']!=b['duration']:durations.append(dict(index=i,canonical_source_offset=a['canonical_source_offset'],word=a['word'],parent=a['duration'],revised=b['duration']))
            uiequal &= a['UI_before']==b['UI_before'] and a['UI_after']==b['UI_after']
        require(declared['command_comparison_differences']==differences and declared['duration_differences']==durations,'every original command/timing/RNG/UI difference retained')
        require(declared['all_UI_request_words_equal']==uiequal and declared['original_results_membership_andchoice_result_equal'],'selected UI/result comparison')
        require(declared['normal_returns']==[g['normal_return'] for g in groups],'both measured normal returns')
        scenes=[];missing=[]
        for a,b in zip(groups[0]['speeches'],groups[1]['speeches'],strict=True):
            require(a['id']==b['id'] and a['source_selector']==b['source_selector'],'paired original speech identities')
            first=max(a['start'],b['start'])+20;last=min(a['returned'],b['returned'])-4
            common=sorted(f for f in photos[0] if f in photos[1] and first<f<last)
            if not common:
                missing.append(dict(id=a['id'],source_selector=a['source_selector'],parent_interval=[a['start'],a['returned']],revised_interval=[b['start'],b['returned']]));continue
            frame=common[-1];x,y=picture(0,frame),picture(1,frame)
            scenes.append(dict(id=a['id'],source_selector=a['source_selector'],frame=frame,parent_capture=photos[0][frame],revised_capture=photos[1][frame],
                upper_scene_andportrait_RGB_equal=x.crop((0,0,256,272)).tobytes()==y.crop((0,0,256,272)).tobytes(),
                whole_header_region_RGB_equal=x.crop((0,272,256,296)).tobytes()==y.crop((0,272,256,296)).tobytes(),
                Gerhard_header_spelling_andwidth_change_expected=a['source_selector']==16,exact_name_ink_coverage_is_separate262_hold_native_mask_proof=True))
        require(declared['selected_scene_andportrait_pairs']==scenes and declared['no_common_held_scene_capture']==missing,'every sampled scene/portrait/header comparison andunmatched interval')
        require(declared['upper_scene_portrait_RGB_difference_IDs']==[s['id'] for s in scenes if not s['upper_scene_andportrait_RGB_equal']] and declared['unchanged_actor_header_RGB_difference_IDs']==[s['id'] for s in scenes if s['source_selector']!=16 and not s['whole_header_region_RGB_equal']],'all actual scene/header differences')
        values=[]
        for g,report,source in zip(groups,reports,[parent,reference],strict=True):
            snap=report['read_only_RAM_snapshot'];raw=Path(snap['path']).read_bytes()
            require(snap['read_only_export'] and len(raw)==4194304 and sha(raw)==snap['sha256'],'final whole read-only RAM integrity')
            arm=source.read_file('/__arm9__.bin');cpu,get=get_machine(arm,raw);actor=get(0xCB184);captain=get(0x7F244)
            require(captain==(0 if scope=='whole' and number==27 else 2),'disclosed wholeB27 finalcaptain0/context limit')
            components={fn.__name__:fn(arm,raw) for fn in [state,models,persistent_objects,tasks,calendar]}
            components['tasks']=dict(bytes=len(components['tasks']),sha256=sha(components['tasks']))
            values.append(dict(version=g['version'],snapshot=snap,components=components,whole_actor_sha256=sha(bytes(cpu.mem_read(actor,0x1A04))),captain_ID=captain,
                PRNG_seed=int.from_bytes(raw[0x168EB8:0x168EBC],'little'),native_component_queries_on_disposable_CPU_only_not_mutating_emulator=True))
            terminal=load(g['terminal']);trace=load(terminal['observer']);fixture=NdsImage.open(g['fixture']['research_ROM']);banks={r:IlnkContainer.parse(fixture.read_file(f'/data/SC{r}.DK4')).blocks for r in range(4)}
            following=[]
            for i,row in enumerate(trace['rows']):
                resident=row['source'];require(row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'] and resident['classification']=='original_SC_cache','following original cache/readonly observer')
                payload=banks[resident['route']][resident['block']]
                require(resident['actual_sha256']==resident['registered_sha256']==sha(payload) and resident['whole_resident_payload_exact_ROM'],'following original resident payload identity')
                if row['kind']=='after_command' and i>g['command_pairs'][-1]['return_row']:
                    following.append(dict(frame=row['frame'],route=resident['route'],block=resident['block'],offset=resident['instruction_offset'],word=resident['first_word'],native_result=row['result_words']))
            require(following==g['following_original_cache_commands'],'complete recorded following-command scope')
        require(declared['final_native_values']==values,'every recomputed final native component/actor/captain/RNG value')
        equality={k:values[0]['components'][k]==values[1]['components'][k] for k in values[0]['components']}
        require(declared['five_native_component_equality']==equality and declared['captain_IDs']==[v['captain_ID'] for v in values] and declared['whole_actors_equal']==(values[0]['whole_actor_sha256']==values[1]['whole_actor_sha256']),'computed bounded component/actor/captain comparison')
        require(declared['final_PRNG_seeds']==[v['PRNG_seed'] for v in values] and declared['raw_calendars_no_invented_date_interpretation']==[v['components']['calendar'] for v in values],'every raw final RNG/calendar value')
        require(declared['following_commands']==[g['following_original_cache_commands'] for g in groups] and declared['following_commands_equal']==(groups[0]['following_original_cache_commands']==groups[1]['following_original_cache_commands']),'following original command comparison')
        threshold=max(g['normal_return']['frame'] for g in groups)+60;frames=sorted(f for f in photos[0] if f>threshold and f in photos[1]);rgb=[]
        for frame in frames:
            a,b=picture(0,frame),picture(1,frame);box=ImageChops.difference(a,b).getbbox()
            rgb.append(dict(frame=frame,parent=photos[0][frame],revised=photos[1][frame],whole_RGB_equal=a.tobytes()==b.tobytes(),changed_RGB_bbox=None if box is None else list(box),parent_RGB_sha256=sha(a.tobytes()),revised_RGB_sha256=sha(b.tobytes())))
        require(declared['later_full_RGB_comparisons']==rgb and declared['later_RGB_differences']==[r for r in rgb if not r['whole_RGB_equal']] and declared['later_sample_count']==len(rgb),'every later full RGB measurement')
        require(declared['selected_unmasked_late_frames']==[frames[0],frames[len(frames)//2],frames[-1]],'unaltered reviewed late-frame selections')
        counts.append(dict(scope=scope,block=number,command_differences=len(differences),duration_differences=len(durations),scene_pairs=len(scenes),later_RGB_samples=len(rgb),later_RGB_differences=sum(not r['whole_RGB_equal'] for r in rgb)))
    return dict(every_saved_timing_RNG_UI_scene_later_RGB_andfinal_native_value_recomputed=True,groups=counts,
        measured_fixture_limits_not_everyframe_cause_futureoutcome_orfullsimulation_proof=True)
