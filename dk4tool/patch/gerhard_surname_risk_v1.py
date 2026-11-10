"""Recompute bounded RAM measurements and preserve the disclosed fixture limits; no simulation-equivalence claim."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.focus_Rafael_B50_picture_risk_v8160 import regions as original_regions,normalized_rows
from scripts.source_locked_derivation_v5118 import checked_text

def check_bounded_risk(comparison,focus,actual,load,require,reference):
    require(len(comparison['groups'])==3 and len(focus['groups'])==2,'three measured pairs/two exact replay groups')
    wanted=[('whole',27),('whole',74),('intro-display',27)]
    require([(g['scope'],g['block']) for g in comparison['groups']]==wanted,'exact measured fixture scopes')
    require([len(g['command_comparison_differences']) for g in comparison['groups']]==[1,74,8],'all measured command differences retained')
    require([len(g['duration_differences']) for g in comparison['groups']]==[0,19,2],'all measured duration differences retained')
    require([g['later_sample_count'] for g in comparison['groups']]==[328,164,106],'all later sample counts retained')
    require([len(g['later_RGB_differences']) for g in comparison['groups']]==[0,0,29],'all later RGB differences retained')
    require(all(g['all_UI_request_words_equal'] for g in comparison['groups']),'selected UI request equality retained')
    require(all(not g['upper_scene_portrait_RGB_difference_IDs'] and not g['unchanged_actor_header_RGB_difference_IDs'] for g in comparison['groups']),'tested scene/portrait/unchanged header equality')
    require(sum(len(g['selected_scene_andportrait_pairs']) for g in comparison['groups'])==117,'117 selected scene/portrait pairs')
    require(comparison['whole_B27_tail_NOT_normal_Lil_route_continuity_ororiginal_optional_event_context_proof'],'captain0 wholeB27 fixture limitation')
    for g in comparison['groups'][:2]:
        require(all(g['five_native_component_equality'].values()) and g['whole_actors_equal'] and g['final_PRNG_seeds'][0]==g['final_PRNG_seeds'][1],'bounded whole-script final equality')
    g=comparison['groups'][2]
    require(g['five_native_component_equality']==dict(state=True,models=False,persistent_objects=False,tasks=True,calendar=True) and not g['whole_actors_equal'],'focused intro final differences retained')
    require(g['normal_returns']==[dict(frame=5695,native_result=[0,0],complete_four_byte_end=True),dict(frame=5694,native_result=[0,0],complete_four_byte_end=True)],'focused intro measured normal return difference')
    adapter=checked_text(inspect.getsource(original_regions),{'assert get(0x7F244)==0':'assert get(0x7F244)==2'})
    require(focus['source_owned_native_regions_adapter']==adapter,'source-owned exact captain2 native regions adapter')
    env=dict(original_regions.__globals__);exec(compile(adapter,__file__+'::unchanged-native-regions','exec'),env)
    frames=[3970,4330,4810,5770,6310,9730,10510,12000]
    require(focus['declared_RAM_sample_frames']==frames and len(focus['sampled_comparisons'])==8,'exact eight read-only RAM phases')
    require(focus['all_same_ROM_input_horizon_observer_rows_selected_framebuffers_andfinal_RAM_reproduce_exactly_perversion'],'exact same-input replay obligation')
    require(focus['total_Gerhard_scene_frames_including_replay']==int('176008') and focus['new_actual_frames']==24002,'complete original/replay frame scope')
    require(focus['original_full_B27_production_branch_conditions_NOT_executed_bythis_focused_display_fixture'],'focused display outercondition limit')
    groups=[];rawgroups=[]
    for group in focus['groups']:
        version=group['version'];require(version in ['parent_English','revised_English'],'exact focused replay version')
        source=next(g for g in actual['groups'] if g['scope']=='intro-display' and g['version']==version)
        terminal=load(group['terminal']);report=load(terminal['report']);trace=load(terminal['observer']);initial=load(source['capture_report']);initial_trace=load(load(source['terminal'])['observer'])
        require(terminal['terminal'] and terminal['frames']==report['frames']==12001 and terminal['all_callbacks_readonly_andhost_slots_restored'],'terminal exact replay')
        require(sha(Path(terminal['report']).read_bytes())==terminal['report_sha256'] and sha(Path(terminal['observer']).read_bytes())==terminal['observer_sha256'],'replay report/trace digests')
        require(normalized_rows(trace)==normalized_rows(initial_trace) and not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact'],'every exact replay observer association')
        require(report['scripted_input_schedule']==initial['scripted_input_schedule'] and report['ROM_sha256']==initial['ROM_sha256']==source['fixture']['research_ROM_sha256'],'same ROM inputs andhorizon')
        require(report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors'],'replay coldboot/no state forcing')
        snapshots={s['frame']:s for s in report['read_only_capture_RAM_snapshots']};require(list(snapshots)==frames,'all eight actual snapshot exports')
        photos={p['frame']:p for p in report['frames_captured']};oldphotos={p['frame']:p for p in initial['frames_captured']}
        arm=NdsImage.open(source['fixture']['research_ROM']).read_file('/__arm9__.bin')
        require(sha(arm)==reference['current_ARM9_sha256' if version=='parent_English' else 'research_ARM9_sha256'],'exact replay ARM9 identity')
        values={};regions={}
        for frame in frames:
            stored=group['sampled_native_values'][str(frame)];snap=snapshots[frame]
            require(stored['snapshot']==snap and snap['read_only_export'],'snapshot/frame/provenance binding')
            raw=Path(snap['path']).read_bytes();require(len(raw)==4194304 and sha(raw)==snap['sha256'],'whole read-only snapshot integrity')
            measured,regions[frame]=env['regions'](arm,raw)
            require(measured=={k:v for k,v in stored.items() if k!='snapshot'},'independently recomputed native phase values')
            require(photos[frame]['PNG_sha256']==oldphotos[frame]['PNG_sha256'] and photos[frame]['framebuffer_sha256']==oldphotos[frame]['framebuffer_sha256'],'replay selected PNG/framebuffer equality')
            require(sha(Path(photos[frame]['path']).read_bytes())==photos[frame]['PNG_sha256'],'actual replay PNG integrity')
            values[frame]=measured
        final=report['read_only_RAM_snapshot'];oldfinal=initial['read_only_RAM_snapshot']
        require(final['sha256']==oldfinal['sha256']==sha(Path(final['path']).read_bytes()),'exact replay final whole RAM')
        groups.append(values);rawgroups.append(regions)
    for index,frame in enumerate(frames):
        before,after=[g[frame] for g in groups];stored=focus['sampled_comparisons'][index]
        equality={k:before[k]==after[k] for k in ['state','models','persistent_objects','tasks','calendar','whole_actor_sha256']}
        require(stored['frame']==frame and stored['component_equality']==equality,'computed phase component equality')
        require(stored['parent_PRNG_seed']==before['PRNG_seed'] and stored['revised_PRNG_seed']==after['PRNG_seed'],'computed raw phase RNG states')
        require(stored['raw_calendar_values']==[before['calendar'],after['calendar']],'computed raw calendar values')
        expected={}
        for key in rawgroups[0][frame]:
            a,b=rawgroups[0][frame][key],rawgroups[1][frame][key];require(len(a)==len(b),'same bounded native region extent')
            changes=[dict(offset=i,parent=p,revised=q) for i,(p,q) in enumerate(zip(a,b,strict=True)) if p!=q]
            expected[key]=dict(bytes=len(a),changed_bytes=len(changes),changes=changes,parent_sha256=sha(a),revised_sha256=sha(b))
        require(stored['bounded_native_model_andpersistent_byte_differences']==expected,'independently recomputed every bounded byte difference')
    require(all(all(s['component_equality'].values()) for s in focus['sampled_comparisons'][:7]),'first seven bounded native component sets equal')
    require({k:v['changed_bytes'] for k,v in focus['sampled_comparisons'][-1]['bounded_native_model_andpersistent_byte_differences'].items() if v['changed_bytes']}==dict(fleet=2,all207_actors_and_current_captain=150,all90_towns=54),'final sampled2/150/54 byte differences')
    return dict(eight_native_RAM_phase_values_andall_byte_differences_recomputed=True,exact_replay_rows_selected_framebuffers_andfinalRAM_revalidated=True,
        all_original_fixture_timing_RNG_component_calendar_RGB_andlater_reaudit_limits_preserved=True,
        no_everyframe_cause_futureoutcome_natural_branch_orbroad_simulation_equivalence_claim=True)
