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
    comparison=data['comparison'];require(len(comparison['groups'])==2,'two complete block exchange comparisons')
    summaries=[];total_rgb=0
    for number,declared in zip([31,53],comparison['groups'],strict=True):
        choice='whole'
        require(declared['block']==number and declared['ordinary_default_input_case'] is True,'exact paired block/default-input membership');groups=data['B31_actual' if number==31 else 'B53_actual']['groups'];old,new=groups
        require([g['version'] for g in groups]==['clean_Japanese','revised_English'],'exact comparison language order')
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
        require(declared['script_returns']==[g['normal_return'] for g in groups] and declared['following_commands']==[g['following_original_cache_commands'] for g in groups],'both returns andfollowing original caches')
        require(declared['following_commands_equal']==(old['following_original_cache_commands']==new['following_original_cache_commands']),'following command comparison')
        threshold=max(g['normal_return']['frame'] for g in groups)+60;frames=sorted(f for f in photos[0] if f>threshold and f in photos[1]);late=[]
        for f in frames:
            ia,ib=picture(0,f),picture(1,f);box=ImageChops.difference(ia,ib).getbbox()
            late.append(dict(frame=f,clean=photos[0][f],revised=photos[1][f],whole_RGB_equal=ia.tobytes()==ib.tobytes(),changed_RGB_bbox=None if box is None else list(box)))
        require(declared['later_RGB_comparisons']==late and declared['later_RGB_difference_count']==sum(not r['whole_RGB_equal'] for r in late),'all complete later framebuffer comparisons retained')
        require(declared['opaque_effect_semantics_not_inferred_from_structural_preservation'] is True and declared['unvisited_conditional_text_IDs']==old['unvisited_conditional_text_IDs']==new['unvisited_conditional_text_IDs']==(['DK4_MES_B31_R0013'] if number==31 else []),'exact unforced selected paths/short variant offline-only/opaque semantics uninferred')
        boundaries=[]
        for a,b in zip(old['command_pairs'],new['command_pairs'],strict=True):
            boundaries.append(dict(source_offset=a['canonical_source_offset'],before=[a['before_RNG'],b['before_RNG']],after=[a['after_RNG'],b['after_RNG']],equal=a['before_RNG']==b['before_RNG'] and a['after_RNG']==b['after_RNG']))
        unequal=[b['source_offset'] for b in boundaries if not b['equal']]
        require(unequal==[],'all measured script-boundary PRNG differences preserved')
        summaries.append(dict(block=number,choice=choice,script_boundary_PRNG=boundaries,command_differences=len(diffs),duration_differences=len(durations),later_RGB_samples=len(late),later_RGB_differences=sum(not r['whole_RGB_equal'] for r in late),
            final_captain_IDs=[n['captain_ID'] for n in native],five_native_component_equality=equality,whole_actors_equal=declared['whole_actors_equal'],final_PRNG_seeds=[n['PRNG_seed'] for n in native]))
        total_rgb+=len(late)
    require(total_rgb==68 and [s['later_RGB_samples'] for s in summaries]==[34,34] and all(s['final_captain_IDs']==[1,1] for s in summaries),'68laterRGBpairs andfour initialized Hodram captain1 snapshots')
    return dict(groups=summaries,later_full_RGB_pairs_recomputed=total_rgb,no_every_frame_future_outcome_orfull_route_equivalence_claim=True)


def check_comparisons(data,parent,load,require):
    result=check_base_comparisons(data,parent,load,require);proof=data['comparison']
    require(proof['total_actual_frames']==24004 and proof['initialized_original_Hodram_opening_not_optional_event_activation_original_location_orall_attainable_paths'] and proof['all_measured_differences_retained_no_input_state_seed_orresult_forcing'] and proof['no_every_frame_causality_future_outcome_broad_simulation_fullroute_orhardware_claim'],'original initialized-fixture scope andall measured limitations retained')
    for sheet in proof['review_sheets']:require(sha(Path(sheet['path']).read_bytes())==sheet['sha256'],'original comparison review sheet integrity')
    require([g['later_RGB_differences'] for g in result['groups']]==[0,0] and [g['duration_differences'] for g in result['groups']]==[0,0],'all measured laterRGB andcommand-duration comparisons retained')
    require([g['final_PRNG_seeds'] for g in result['groups']]==[list(map(int,['3325064553','3325064553']))]*2,'equal measured final PRNG values retained without future-outcome inference')
    result.update(new_emulator_runs=0,all_source_qualified_unforced_paths_andunvisited_short_B31_scope_checked=True,all_measured_PRNG_andRGB_differences_preserved=True)
    return result
