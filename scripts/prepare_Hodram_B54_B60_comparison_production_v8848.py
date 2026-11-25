"""Preserve every measured main/focused comparison; differing outcomes remain explicit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_comparison_tools_v8848');assert not root.exists()
    main=read('work/analysis/Hodram_B54_B60_comparison_v8821/paired_selected_path_comparison.json')
    focus=read('work/analysis/Hodram_B60_focus_comparison_v8824/paired_selected_path_comparison.json')
    seeds=[[str(v) for v in g['final_PRNG_seeds']] for g in main['groups']+focus['groups']]
    old_tail="""    result=check_base_comparisons(data,parent,load,require);proof=data['comparison']
    require(proof['total_actual_frames']==24004 and proof['initialized_original_Hodram_opening_not_optional_event_activation_original_location_orall_attainable_paths'] and proof['all_measured_differences_retained_no_input_state_seed_orresult_forcing'] and proof['no_every_frame_causality_future_outcome_broad_simulation_fullroute_orhardware_claim'],'original initialized-fixture scope andall measured limitations retained')
    for sheet in proof['review_sheets']:require(sha(Path(sheet['path']).read_bytes())==sheet['sha256'],'original comparison review sheet integrity')
    require([g['later_RGB_differences'] for g in result['groups']]==[0,0] and [g['duration_differences'] for g in result['groups']]==[0,0],'all measured laterRGB andcommand-duration comparisons retained')
    require([g['final_PRNG_seeds'] for g in result['groups']]==[list(map(int,['3325064553','3325064553']))]*2,'equal measured final PRNG values retained without future-outcome inference')
    result.update(new_emulator_runs=0,all_source_qualified_unforced_paths_andunvisited_short_B31_scope_checked=True,all_measured_PRNG_andRGB_differences_preserved=True)
    return result"""
    new_tail="""    result=check_base_comparisons(data,parent,load,require)
    for key,frames in [('comparison',116012),('focus_comparison',14002)]:
        proof=data[key]
        require(proof['total_actual_frames']==frames and proof['initialized_original_Hodram_opening_not_optional_event_activation_original_location_orall_attainable_paths'] and proof['all_measured_differences_retained_no_input_state_seed_orresult_forcing'] and proof['no_every_frame_causality_future_outcome_broad_simulation_fullroute_orhardware_claim'],'original initialized-fixture scope andall measured limitations retained')
        for sheet in proof['review_sheets']:require(sha(Path(sheet['path']).read_bytes())==sheet['sha256'],'original comparison review sheet integrity')
    require([g['later_RGB_differences'] for g in result['groups']]==[3,0,0,3,65,61,11] and [g['duration_differences'] for g in result['groups']]==[1,0,0,9,2,2,2],'all measured laterRGB andcommand-duration differences retained')
    require([g['final_PRNG_seeds'] for g in result['groups']]==EXPECTED_SEEDS,'all measured final PRNG values retained without future-outcome inference')
    require(not result['groups'][5]['whole_actors_equal'] and not result['groups'][5]['five_native_component_equality']['persistent_objects'],'long B60 actor/persistent differences remain')
    require(result['groups'][6]['whole_actors_equal'] and all(result['groups'][6]['five_native_component_equality'].values()),'bounded focused B60 component equality remains')
    prefix=[]
    for version in ['clean_Japanese','revised_English']:
        old=next(g for g in data['B60_actual']['groups'] if g['version']==version)
        new=next(g for g in data['focus_actual']['groups'] if g['version']==version)
        a,b=load(old['capture_report']),load(new['capture_report'])
        require(b['scripted_input_schedule']==[v for v in a['scripted_input_schedule'] if v['start']<6640] and b['scripted_input_schedule'][-1]['start']==6400,'focused ordinary input prefix/no later A6640 suffix')
        x,y=load(old['observer']),load(new['observer'])
        xx=[r for r in x['rows'] if r['frame']<=6640];yy=[r for r in y['rows'] if r['frame']<=6640]
        require(len(xx)==len(yy)==(41 if version=='clean_Japanese' else 40),'all81 observed pre-next-input callbacks')
        keys=['frame','kind','WRAM_sha256','DTCM_sha256','ITCM_sha256','CPU128_hex']
        require(all(all(i[k]==j[k] for k in keys) for i,j in zip(xx,yy,strict=True)),'exact own-language main/focused fullmemory CPU andTCM prefix')
        prefix.append(dict(version=version,matching_callbacks=len(xx)))
    result.update(focused_prefix=prefix,new_emulator_runs=0,all_source_qualified_unforced_paths_and19_offline_records_scope_checked=True,all_measured_PRNG_RGB_timing_followingcommands_andlongactor_differences_preserved=True,no_immediate_return_mainRAM_causality_orfuture_equivalence_claim=True)
    return result""".replace('EXPECTED_SEEDS','[[int(v) for v in row] for row in '+repr(seeds)+']')
    module=derive('dk4tool/patch/hodram_B31_B53_comparison_v1.py','dk4tool/patch/hodram_B54_B60_comparison_v1.py',{
        "comparison=data['comparison'];require(len(comparison['groups'])==2,'two complete block exchange comparisons')":"comparison=data['comparison'];require(len(comparison['groups'])==6 and len(data['focus_comparison']['groups'])==1,'six main andone focused complete exchange comparisons')",
        "for number,declared in zip([31,53],comparison['groups'],strict=True):":"for index,(number,declared) in enumerate(zip([54,56,57,58,59,60,60],comparison['groups']+data['focus_comparison']['groups'],strict=True)):",
        "choice='whole'":"choice='focus' if index==6 else 'whole'",
        "groups=data['B31_actual' if number==31 else 'B53_actual']['groups']":"groups=data['focus_actual' if index==6 else 'B'+str(number)+'_actual']['groups']",
        "==(['DK4_MES_B31_R0013'] if number==31 else [])":"==[r['id'] for r in data['manuscript']['records'] if r['block']==number and r['id'] not in {s['id'] for s in old['speeches']}]",
        'exact unforced selected paths/short variant offline-only/opaque semantics uninferred':'exact unforced selected paths/18B58 conditionals offline-only/opaque semantics uninferred',
        "require(unequal==[],'all measured script-boundary PRNG differences preserved')":"require(unequal==[r['canonical_source_offset'] for r in diffs if any(k in r['different_fields'] for k in ['before_RNG','after_RNG'])],'all measured script-boundary PRNG differences preserved')",
        'total_rgb==68':'total_rgb==335',
        "[s['later_RGB_samples'] for s in summaries]==[34,34]":"[s['later_RGB_samples'] for s in summaries]==[22,43,56,77,65,61,11]",
        '68laterRGBpairs andfour initialized Hodram captain1 snapshots':'335laterRGBpairs and14 initialized Hodram captain1 snapshots',
        old_tail:new_tail,
    })
    validation=derive('scripts/validate_Hodram_B31_B53_comparison_v8766.py','scripts/validate_Hodram_B54_B60_comparison_v8849.py',{
        'hodram_B31_B53_comparison_v1':'hodram_B54_B60_comparison_v1','Hodram_B31_B53_verified_inputs_v8763':'Hodram_B54_B60_verified_inputs_v8846',
        'Hodram_B31_B53_comparison_validation_v8766':'Hodram_B54_B60_comparison_validation_v8849',
        'Hodram_B31_B53_actual_validation_v8764':'Hodram_B54_B60_actual_validation_v8847',
        'B31/B53 comparison production:':'B54-B60 comparison production:','Frozen Hodram-B31-B53 contract changed':'Frozen Hodram-B54-B60 contract changed',
        'all_four_whole_fixture_inverses_all_saved_trace_fields_body_name_holds_andnormal_returns_independently_checked':'all_twelve_whole_fixture_inverses_fourteen_saved_runs_all_pages_FE_body_name_holds_andnormal_returns_independently_checked',
        "actual['negative_count']==13":"actual['negative_count']==16",
        "['later_full_RGB_pairs_recomputed']==68 and len(result['groups'])==2":"['later_full_RGB_pairs_recomputed']==335 and len(result['groups'])==7",
        "[g['command_differences'] for g in result['groups']]==[2,1] and all(all(g['five_native_component_equality'].values()) and g['whole_actors_equal'] for g in result['groups'])":"[g['command_differences'] for g in result['groups']]==[4,2,5,58,9,10,10] and not result['groups'][5]['whole_actors_equal'] and result['groups'][6]['whole_actors_equal']",
        "__setitem__(1,0)":"__setitem__(1,1)",
        '    assert len(cases)==12 and':"    reject('suppressed-long-B60-actor-divergence',lambda d:d['comparison']['groups'][5].__setitem__('whole_actors_equal',True))\n    reject('missing-focused-comparison',lambda d:d['focus_comparison']['groups'].pop())\n    reject('suppressed-focused-RGB-differences',lambda d:d['focus_comparison']['groups'][0].__setitem__('later_RGB_difference_count',0))\n    reject('invented-equal-focused-RNG',lambda d:d['focus_comparison']['groups'][0]['final_PRNG_seeds'].__setitem__(1,d['focus_comparison']['groups'][0]['final_PRNG_seeds'][0]))\n    assert len(cases)==16 and",
        'four_saved_complete_final_snapshots_native_components_wholeactors_captain_RNG_calendar_and68_full_RGBpairs_recomputed':'fourteen_saved_complete_final_snapshots_native_components_wholeactors_captain_RNG_calendar_and335_full_RGBpairs_recomputed',
        'all_three_decodedlength_differences_andzero_duration_UI_request_boundary_RNG_followingcommand_differences_preserved':'all_measured_decodedlength_duration_UI_request_boundary_RNG_followingcommand_longactor_andRGB_differences_preserved',
        'no_future_simulation_natural_activation_fullcatalogue_fullroute_hardware_orunvisited_shortvariant_claim':'no_future_simulation_natural_activation_fullcatalogue_fullroute_hardware_or19_unvisited_record_claim',
        'Comparison production:4saved final snapshots/5native components/actors/captain1/RNG/calendar/68fullRGBpairs pass;12semantic defects reject. No capture replay,ROMcommit orcredit.':'Comparison production:14saved final snapshots/5native components/actors/captain1/RNG/calendar/335fullRGBpairs and81prefixcallbacks pass;16semantic defects reject. All differences retained;no capture replay,ROMcommit orcredit.',
    })
    root.mkdir(parents=True);save(root/'source_locked_comparisons.json',dict(module=module,validation=validation,all_original_saved_RAM_native_component_actor_calendar_RNG_input_command_scene_portrait_header_andfull_later_framebuffer_checks_preserved=True,long_B60_actor_divergence_andfocused_bounded_equality_both_required=True,all81_own_language_prefix_callbacks_independently_compared=True,no_causality_orfuture_equivalence_claim=True,no_new_capture_orcredit=True,new_credit=0,full_goal_complete=False))
