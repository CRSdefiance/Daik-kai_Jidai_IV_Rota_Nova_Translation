"""Source-owned two-route identity, display, control and measured-scope guards."""
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
BASE=0x02000000
POOL=0x02387A20

def audit_scope(image,clean,conf,mapping,seal,load,require):
    p=conf['proofs'];f,s,q,a,l,v,n,np,e,controls,loader,census=[load(p[k]) for k in ['native_font_proof','native_stored_proof','native_policy_validation','actual_proof','later_scope_proof','actual_view','speaker_name_review','native_name_proof','source_entry_proof','relocated_control_proof','native_loader_proof','native_caller_proof']]
    require((f['fresh_compiled_alignment_cases'],f['exact_reused_logical_alignment_cases'],f['distinct_native_pages'],f['fresh_native_page_renders'],f['distinct_prior_exact_reused_native_page_renders'])==(144,144,18,6,12),'complete native counts')
    require(f['all36_single_original_four_row_pages'] and f['all_first_internal_final_glyphs_bounds_canaries_consumption_andpair_phase_verified'],'complete native font/guards')
    require((s['stored_alignment_cases'],s['fresh_alignment_cases'],s['exact_reused_alignment_cases'],s['zero_ink_parity_tail_count'],s['distinct_fresh_stored_font_renders'])==(144,64,80,16,8) and s['all36_final_stored_targets_equal_reviewed_complete_ink'] and s['all_bounds_canaries_pairphase_zero_macros_andcomplete_consumption_pass'],'stored counts/ink')
    require(q['positive_count']==len(q['positive_cases'])==36 and q['negative_count']==len(q['negative_cases'])==174 and all(r['rejected'] and r['expected_guard'] and r['expected_guard'] in r['error'] for r in q['negative_cases']) and q['two_exact_R33_warnings16_infos_preserved'],'actual-changing policy guards')
    require(a['total_actual_speech_occurrences']==72 and a['distinct_file_qualified_speeches']==36 and a['all_jobs_terminal_andreaped'] and a['all_callbacks_readonly_andhost_slots_restored'] and a['all72_complete_leading_internal_final_body_andname_glyphs_bounds_andone_page_verified'] and a['all_four_R5_three_ellipsis_black18_lightgray18_masks_exact'],'complete actual display/source')
    require(v['all72_complete_source_English_speech_panes_individually_viewed'] and v['all12_six_speech_sheets_four_transition_sheets_one_unmasked_late_sheet_viewed'] and len(v['all72_panes_byte_equal_saved_whole_frame_crops'])==72 and len(v['viewed_sheets'])==17,'actual visual review')
    require(l['all36_source_English_upper_scene_portrait_complete_header_pairs_equal'] and l['no_full_RAM_every_frame_future_sequence_broad_simulation_orcausal_equivalence_claim'] and l['all_measured_differences_preserved_for_later_older_record_technical_reaudit'],'comparison limits')
    expected_components=[dict(state=True,models=True,persistent_objects=True,tasks=True,calendar=True),dict(state=True,models=False,persistent_objects=False,tasks=True,calendar=True)]
    expected_seeds=[[2470616159,2470616159],[3950740296,3249748893]]
    require(v['later_RGB_differences_by_route']==[3,53] and v['later_samples_each_route']==133 and v['PRNG_seeds_by_route']==expected_seeds and v['five_component_equality_by_route']==expected_components,'view retains late differences')
    observed=[]
    for route in [0,1]:
        groups=[g for g in a['groups'] if g['route']==route];require(len(groups)==2,'paired actual route')
        for g in groups:
            require(g['actual_unique_speeches']==len(g['speech_observations'])==18 and g['complete_body_holds']==g['complete_name_holds']==[63,70][route] and g['incomplete_sampled_holds']==0 and g['unidentified_trace_rows']==[] and g['native_terminal_result']==[0,0] and g['normal_return_sample_frame']==8170 and len(g['command_pairs'])==[30,28][route],'complete actual holds/commands')
        require(groups[0]['input_schedule_sha256']==groups[1]['input_schedule_sha256'],'identical source/English inputs')
        lg=l['groups'][route];require(lg['route']==route and lg['source_English_exits']==[8095,8094] and lg['all_original_initializer_andexchange_results_andUI_words_equal'] and len(lg['scene_portrait_header_pairs'])==18,'scene/native comparison')
        require(len(lg['command_comparison_differences'])==19 and len(lg['duration_differences'])==7 and lg['later_sample_count']==len(lg['later_full_RGB_comparisons'])==133 and len(lg['later_RGB_differences'])==[3,53][route],'measured timing/RGB counts')
        require(lg['captain_IDs']==[route,route] and lg['final_PRNG_seeds']==expected_seeds[route] and lg['five_native_component_equality']==expected_components[route] and lg['whole_actors_equal']==(route==0),'actual captains/state/RNG limits')
        en=next(g for g in groups if g['version']=='English')
        observed.append(dict(route=route,source_English_exits=[8095,8094],body_holds=en['complete_body_holds'],name_holds=en['complete_name_holds'],command_difference_rows=19,duration_changes=7,later_samples=133,later_RGB_differences=[3,53][route],component_equality=expected_components[route],actors_equal=route==0,captains=[route,route],PRNG_seeds=expected_seeds[route]))
        eg=e['groups'][route];event=eg['selected_source_events'][0]
        require((eg['route'],event['event_ID'],event['action_index'],event['script_block'],event['must_be_completed'],event['must_not_be_completed'])==(route,[246,237][route],[247,238][route],[246,237][route],[],[]),'exact EV entry/action/dependencies')
        require(sha(image.read_file(eg['event_file']))==eg['event_file_sha256'] and image.read_file(eg['event_file'])==clean.read_file(eg['event_file']),'source event file exact')
        cg=controls['groups'][route];require(cg['route']==route and len(cg['dispatch_cases'])==18 and len(cg['normal_terminal_seed_cases'])==25 and cg['target_A000_offset']==1494 and cg['target_normal_end_offset1502_four_bytes'] and cg['target_two_byte_storage_tail_separately_bound'],'final native controls')
        require(all(not t['flagged_terminal'] and t['native_result'][0]==0 and t['native_result'][1]==t['initial_value_word'] for t in cg['normal_terminal_seed_cases']),'all25 seeded ends')
    require(mapping['observed_comparison_contract']==seal['observed_comparison_contract']==observed,'sealed comparison contract')
    require(loader['fresh_native_whole_loads_andcache_hits']==668 and loader['fresh_initial_parent_modes']==1336 and loader['both_original_parent_modes_begin_payload_plus8'] and census['only_original_24070_interpreter_call_no_literal_alias'] and census['fresh_caller_censuses']==1,'loader/caller contracts')
    require(n['all_four_contextual_name_formatting_gates_true'] and n['all_broader207_name_role_alias_andearlier_consumers_open'] and len(n['records'])==4 and n['spoken_alias']['Japanese']=='フィリポ' and n['spoken_alias']['English']=='Filippo' and n['spoken_alias']['source_record_indices']==[9,16],'scoped source name/alias decisions')
    source=clean.read_file('/__arm9__.bin');current=image.read_file('/__arm9__.bin')
    payload=bytes(MainCodeFile(current,BASE).sections[3].data[:-48]);require(len(payload)==123264 and current.find(payload)==1517964,'original payload size/physical base')
    item=load(p['source_named_item_binding']);region=item['actor104_regional_secondary_storage_contract']
    require((region['pointer_field'],region['current_pointer'],region['current_deployed_payload_offset'],region['current_physical_ARM9_storage_offset'])==(1185924,37256672,960,1518924) and region['both_returned_name_strings_exclude_regional_literal'],'regional independent absolute/relative contract')
    def fields(row):
        pointer=row['pointer_field']
        if row.get('source_null'):
            require(row['current_null'] and source[pointer:pointer+4]==current[pointer:pointer+4]==bytes(4),'null middle');return
        require(int.from_bytes(source[pointer:pointer+4],'little')==row['source_pointer'] and int.from_bytes(current[pointer:pointer+4],'little')==row['current_pointer'],'name/item pointers')
        for arm,which in [(source,'source'),(current,'current')]:
            at=row[which+'_storage_offset'];raw=bytes.fromhex(row[which+'_terminated_hex']);require(raw[-1]==0 and 0 not in raw[:-1],'complete terminated field')
            if which=='current' and row['current_storage_kind']=='verified-current-staged-payload':
                require(pointer==1185924 and at==1518924 and raw==b'European\0' and row['current_pointer']==POOL+960==37256672 and at==1517964+960 and payload[960:960+len(raw)]==arm[at:at+len(raw)]==raw,'independent regional physical/deployed bytes')
            else:require(row[which+'_pointer']==BASE+at and arm[at:at+len(raw)]==raw,'static name/item bytes')
    consumer=load(p['current_consumer_proof'])
    for row in n['records']:
        actor=row['actor_ID'];route=row['route'];require(route in [0,1] and actor in [19,104] and row['english']=={19:'Carlo Sinat',104:'Trader'}[actor] and row['editorial_decision']=='retain-wording' and row['retention_reason'] and all(row['review'].values()) and row['full_catalogue_UI_unvisited'] and row['natural_optional_event_activation_andoriginal_location_unvisited'],'four exact scoped name retentions')
        require([r['Japanese'] for r in row['source_fields'] if r.get('Japanese')]=={19:['カルロ','シナート'],104:['交易所の親父','ヨーロッパ']}[actor] and row['source_fields'][2]['source_null'] and row['source_fields'][2]['current_null'],'name identity/null middle')
        for field in row['source_fields']:fields(field)
        getters=consumer['groups'][route]['native_four_distinct_name_consumers']['rows']
        require({(r['actor_ID'],r['consumer']):r['text'] for r in getters}=={(19,'progressive-nameplate'):'Carlo Sinat',(19,'full-catalogue'):'Carlo Sinat',(104,'progressive-nameplate'):'Trader',(104,'full-catalogue'):'Trader'},'both exact route getters')
        require(row['source_fields']==next(r['fields'] for r in consumer['groups'][route]['source_name_fields'] if r['actor_ID']==actor),'source fields agree with consumers')
    r=item['source_named_item'];require((r['record_ID'],r['Japanese'],r['English'],r['pointer_field'],r['source_storage_offset'],r['current_storage_kind'],r['current_storage_offset'])==('DK4_ITEM_POINTER_106','グレゴリウスの冠',"Gregory's Crown",1174528,1434712,'static-current-ARM9',1435852) and r['current_native_item_getter_card_bounds_mechanics_and_all_other_consumers_not_reviewed_here'],'item106 static identity andscope');fields(r)
    require(item['reported_papal_association_blessing_andconditional_find_not_confirmed_mechanic'] and item['no_item_or_actor_asset_change_or_duplicate_credit'],'prospective blessing/item scope')
    require(np['fresh_native_literal_alignment_cases']==40 and np['fresh_name_font_renderer_executions']==0 and np['distinct_exact_reused_native_font_planes']==5,'name font exact reuse')
    for g in np['groups']:
        require(len(g['name_planes'])==5 and sum(len(r['native_alignment']['cases']) for r in g['name_planes'])==20 and {r['text'] for r in g['name_planes']}=={'Carlo Sinat','Trader','Carlo','Sinat','European'},'five complete literal planes perroute')
        for r in g['name_planes']:require(sha(Path(r['native_plane']).read_bytes())==r['native_plane_sha256'],'complete name font plane')
