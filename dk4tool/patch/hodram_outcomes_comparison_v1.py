"""Recompute saved paired timing, scene, final native state and complete later RGB comparisons."""
from pathlib import Path
from PIL import Image,ImageChops
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_shipyard_gameplay_v760 import models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_ceremony_prayer_gameplay_v814 import calendar
from scripts.verify_personal_gameplay_v841 import get_machine

def check_base_comparisons(data,parent,load,require):
    comparison=data['comparison'];require(len(comparison['groups'])==2,'two exact actual comparison blocks')
    summaries=[];total_rgb=0
    for number,declared in zip([47,48],comparison['groups'],strict=True):
        require(declared['block']==number,'exact paired comparison block');groups=data[f'actual{number}']['groups'];old,new=groups
        reports=[load(g['capture_report']) for g in groups];require(reports[0]['scripted_input_schedule']==reports[1]['scripted_input_schedule'],'unretimed paired controller input')
        photos=[{p['frame']:p for p in r['frames_captured']} for r in reports];cache={}
        def picture(which,frame):
            key=which,frame
            if key not in cache:
                photo=photos[which][frame];require(sha(Path(photo['path']).read_bytes())==photo['PNG_sha256'],'paired actual PNG integrity')
                cache[key]=Image.open(photo['path']).convert('RGB')
            return cache[key]
        diffs=[];durations=[];UI=[]
        for a,b in zip(old['command_pairs'],new['command_pairs'],strict=True):
            require((a['source_command_ordinal'],a['word'],a['native_result'])==(b['source_command_ordinal'],b['word'],b['native_result']),'paired original selected results/membership')
            fields={k:dict(clean=a[k],revised=b[k]) for k in ['start','returned','decoded_length','before_RNG','after_RNG','UI_before','UI_after'] if a[k]!=b[k]}
            if fields:diffs.append(dict(source_command_ordinal=a['source_command_ordinal'],canonical_source_offset=a['canonical_source_offset'],word=a['word'],different_fields=fields))
            if a['duration']!=b['duration']:durations.append(dict(source_command_ordinal=a['source_command_ordinal'],word=a['word'],clean=a['duration'],revised=b['duration']))
            if a['UI_before']!=b['UI_before'] or a['UI_after']!=b['UI_after']:UI.append(dict(source_command_ordinal=a['source_command_ordinal'],word=a['word'],clean=[a['UI_before'],a['UI_after']],revised=[b['UI_before'],b['UI_after']]))
        require((declared['command_comparison_differences'],declared['duration_differences'],declared['UI_request_differences'])==(diffs,durations,UI),'all actual command/timing/RNG/UI differences retained')
        scenes=[];missing=[]
        for a,b in zip(old['speeches'],new['speeches'],strict=True):
            require((a['id'],a['source_selector'])==(b['id'],b['source_selector']),'paired source-qualified speeches')
            common=sorted({p['frame'] for p in a['complete_holds']}&{p['frame'] for p in b['complete_holds']})
            if not common:missing.append(a['id']);continue
            f=common[-1];ia,ib=picture(0,f),picture(1,f)
            scenes.append(dict(id=a['id'],frame=f,clean=photos[0][f],revised=photos[1][f],upper_scene_portrait_RGB_equal=ia.crop((0,0,256,272)).tobytes()==ib.crop((0,0,256,272)).tobytes(),
                complete_header_region_RGB_equal=ia.crop((0,272,256,296)).tobytes()==ib.crop((0,272,256,296)).tobytes()))
        require(declared['scene_pairs']==scenes and declared['no_common_complete_hold']==missing,'all paired scene/portrait/header comparisons andunpaired intervals')
        native=[];arm=parent.read_file('/__arm9__.bin')
        require(sha(arm)=='12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b','exact native final-state query code')
        for group,report in zip(groups,reports,strict=True):
            snap=report['read_only_RAM_snapshot'];raw=Path(snap['path']).read_bytes();require(snap['read_only_export'] and len(raw)==4194304 and sha(raw)==snap['sha256'],'whole read-only final RAM')
            cpu,get=get_machine(arm,raw);actor=get(0xCB184);captain=get(0x7F244)
            components={fn.__name__:fn(arm,raw) for fn in [state,models,persistent_objects,tasks,calendar]};components['tasks']=dict(bytes=len(components['tasks']),sha256=sha(components['tasks']))
            native.append(dict(version=group['version'],snapshot=snap,captain_ID=captain,components=components,whole_actor_sha256=sha(bytes(cpu.mem_read(actor,0x1A04))),
                PRNG_seed=int.from_bytes(raw[0x168EB8:0x168EBC],'little'),disposable_CPU_queries_only_not_emulator_mutation=True))
        require(declared['final_native_values']==native,'every recomputed final native component/actor/captain/RNG value')
        equality={k:native[0]['components'][k]==native[1]['components'][k] for k in native[0]['components']}
        require(declared['five_native_component_equality']==equality and declared['whole_actors_equal']==(native[0]['whole_actor_sha256']==native[1]['whole_actor_sha256']),'computed final component/actor equality')
        require(declared['final_PRNG_seeds']==[n['PRNG_seed'] for n in native] and declared['raw_calendars_uninterpreted']==[n['components']['calendar'] for n in native],'exact raw RNG/calendar scope')
        require(declared['normal_returns']==[g['normal_return'] for g in groups] and declared['following_commands']==[g['following_original_cache_commands'] for g in groups],'both returns andfollowing original caches')
        require(declared['following_commands_equal']==(old['following_original_cache_commands']==new['following_original_cache_commands']),'following command comparison')
        threshold=max(g['normal_return']['frame'] for g in groups)+60;frames=sorted(f for f in photos[0] if f>threshold and f in photos[1]);late=[]
        for f in frames:
            ia,ib=picture(0,f),picture(1,f);box=ImageChops.difference(ia,ib).getbbox()
            late.append(dict(frame=f,clean=photos[0][f],revised=photos[1][f],whole_RGB_equal=ia.tobytes()==ib.tobytes(),changed_RGB_bbox=None if box is None else list(box)))
        require(declared['later_RGB_comparisons']==late and declared['later_RGB_difference_count']==sum(not r['whole_RGB_equal'] for r in late),'all complete later framebuffer comparisons retained')
        resource=None
        if number==46:
            display=[next(c for c in g['command_pairs'] if c['word']==0x4800) for g in groups];hide=[next(c for c in g['command_pairs'] if c['word']==0x4700) for g in groups]
            for g,c in zip(groups,display,strict=True):
                control=next(v for v in g['fixture']['all_original_exchange_commands'] if v['fixture_command_offset']==c['fixture_offset'])
                require(control['whole_command_hex']=='0048b5a8' and control['canonical_clean_offset']==140,'original4800 operand/source site')
            common=sorted(f for f in photos[0] if f in photos[1] and max(c['returned'] for c in display)+30<f<min(c['start'] for c in hide)-4)
            before=sorted(f for f in photos[0] if f in photos[1] and f<min(c['start'] for c in display));after=sorted(f for f in photos[0] if f in photos[1] and f>max(c['returned'] for c in hide)+30)
            require(common and before and after,'actual item display andhide sample intervals')
            resource=dict(original_4800_calls=display,original_4700_calls=hide,common_display_sample_frames=common,descriptor=[0,181,1,5],layout=[0,0,0],
                original_Red_Dye_item181_source_control_not_Rafael4821=True,selected_before_display_frame=before[-1],selected_item_display_frame=common[-1],selected_after_hide_frame=after[0],
                actual_full_original_resource_andhide_command_executions=True,descriptor_layout_from_exact_original_operand_and8190b_native_consumer_not_dialogue_UI_request_words=True,
                visual_item_card_andhide_review_pending=True)
        require(declared['original4800_4700_actual']==resource,'complete original item/hide observation andscope metadata')
        summaries.append(dict(block=number,command_differences=len(diffs),duration_differences=len(durations),later_RGB_samples=len(late),later_RGB_differences=sum(not r['whole_RGB_equal'] for r in late),
            final_captain_IDs=[n['captain_ID'] for n in native],five_native_component_equality=equality,whole_actors_equal=declared['whole_actors_equal'],final_PRNG_seeds=[n['PRNG_seed'] for n in native]))
        total_rgb+=len(late)
    require(total_rgb==186 and all(s['final_captain_IDs']==[1,1] for s in summaries),'186laterRGBpairs andboth initialized Hodram captain1 tails')
    return dict(groups=summaries,later_full_RGB_pairs_recomputed=total_rgb,no_every_frame_future_outcome_orfull_route_equivalence_claim=True)


def check_comparisons(data,parent,load,require):
    result=check_base_comparisons(data,parent,load,require);comparison=data['comparison'];later=data['later'];expected_groups=[]
    require(len(later['groups'])==2,'two later-difference characterization groups')
    for number,c in zip([47,48],comparison['groups'],strict=True):
        old,new=data['actual'+str(number)]['groups'];boundaries=[]
        for a,b in zip(old['command_pairs'],new['command_pairs'],strict=True):
            require(a['word']==b['word'] and a['source_command_ordinal']==b['source_command_ordinal'],'same original later-characterization membership')
            boundaries.append(dict(source_command_ordinal=a['source_command_ordinal'],word=a['word'],source_entry_frame=a['start'],English_entry_frame=b['start'],source_return_frame=a['returned'],English_return_frame=b['returned'],before_PRNG=[a['before_RNG'],b['before_RNG']],after_PRNG=[a['after_RNG'],b['after_RNG']],before_PRNG_equal=a['before_RNG']==b['before_RNG'],after_PRNG_equal=a['after_RNG']==b['after_RNG']))
        differences=[]
        for sample in c['later_RGB_comparisons']:
            if sample['whole_RGB_equal']:continue
            images=[Image.open(sample[k]['path']).convert('RGB') for k in ['clean','revised']]
            points=[(i%256,i//256) for i,(a,b) in enumerate(zip(images[0].get_flattened_data(),images[1].get_flattened_data(),strict=True)) if a!=b]
            require(ImageChops.difference(*images).getbbox()==tuple(sample['changed_RGB_bbox']),'actual later changed-pixel extent')
            differences.append(dict(frame=sample['frame'],source=sample['clean'],English=sample['revised'],changed_RGB_bbox=sample['changed_RGB_bbox'],changed_pixels=len(points),upper_screen_changed_pixels=sum(y<192 for x,y in points),lower_screen_changed_pixels=sum(y>=192 for x,y in points)))
        expected_groups.append(dict(block=number,command_boundary_PRNG_comparisons=boundaries,all_observed_script_entry_andreturn_PRNG_pairs_equal=all(b['before_PRNG_equal'] and b['after_PRNG_equal'] for b in boundaries),final_PRNG_seeds=c['final_PRNG_seeds'],final_PRNG_equal=c['final_PRNG_seeds'][0]==c['final_PRNG_seeds'][1],all_five_final_native_components_equal=all(c['five_native_component_equality'].values()),whole_actor_bytes_equal=c['whole_actors_equal'],final_captain_IDs=[v['captain_ID'] for v in c['final_native_values']],normal_returns=c['normal_returns'],actual_duration_differences=c['duration_differences'],actual_UI_request_differences=c['UI_request_differences'],later_RGB_pairs=len(c['later_RGB_comparisons']),later_RGB_differences=differences,later_RGB_difference_count=len(differences),no_new_emulation_orchanging_input_seed_RNG_flags_orresults=True))
    require(later['groups']==expected_groups,'every recomputed later pixel/PRNG/duration/native-state scope field')
    require([g['later_RGB_difference_count'] for g in expected_groups]==[0,13] and [g['final_PRNG_equal'] for g in expected_groups]==[True,False] and all(g['all_observed_script_entry_andreturn_PRNG_pairs_equal'] for g in expected_groups),'approved nonzero B48 later RGB/PRNG difference andmatching script boundaries')
    require(later['all_actual_differences_preserved_not_repaired_by_retiming_orseed_forcing'] and later['matching_selected_final_components_not_full_simulation_orfuture_outcome_equivalence'] and later['later_older_record_technical_reaudit_must_retain_this_scope'],'explicit later comparison limits')
    result.update(all_later_difference_scope_fields_recomputed=True,nonzero_B48_later_RGB_andPRNG_differences_preserved=True,new_emulator_runs=0)
    return result
