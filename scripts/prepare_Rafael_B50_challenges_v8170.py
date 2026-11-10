"""Prepare independent B50 proof-corruption tests;each changes real data andtraps commits."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B50_atomic_challenge_tools_v8170')
TESTS='''    HISTORICAL_B49_MUTATION_SEED_LITERALS=(19668379,19668379)
    tests=[]
    def add(label,path,keys,value):
        old=original(path)
        for key in keys:old=old[key]
        assert old!=value,'Unchanged mutation:'+label
        tests.append(dict(case=label,modifications=[(str(path),keys,deepcopy(value))]))
    doc=original(APPROVED);indices={r['source_record_index']:i for i,r in enumerate(doc['records'])}
    for i,row in enumerate(doc['records']):
        add('prose-'+row['id'],APPROVED,['records',i,'english'],row['english']+'!')
        add('formatting-'+row['id'],APPROVED,['records',i,'review','formatting'],False)
        add('target-reference-'+row['id'],APPROVED,['records',i,'target_reference','offset'],row['target_reference']['offset']+2)
        add('actual-credit-erased-'+row['id'],APPROVED,['records',i,'actual_record_observed'],False)
    for gate in ['source','context','localization','naturalness']:
        add('speech-gate-'+gate,APPROVED,['records',0,'review',gate],False)
    for label,index,old,new in SEMANTIC:
        i=indices[index];text=doc['records'][i]['english'];assert old in text
        add('meaning-'+label,APPROVED,['records',i,'english'],text.replace(old,new))
    for key,value in [('file_path','/data/SC2.DK4'),('route',2),('route_identity','Lil'),('block',49),('current_ROM','work/clean.nds'),('current_ROM_sha256','0'*64),('current_ARM9_sha256','0'*64),('current_COMMON_sha256','0'*64),('target_locale','en-GB'),('translation_policy','natural-dialogue-v1')]:
        add('document-'+key,APPROVED,[key],value)
    for key,value in [('source_hex',doc['records'][0]['source_hex'][:-2]+'00'),('context','Invented wedding.'),('speaker','Grandpa'),('compiled_hex',doc['records'][0]['compiled_hex']+'20'),('source_complete_preamble_hex','000000000000')]:
        add('individual-'+key,APPROVED,['records',0,key],value)
    retention=next(i for i,r in enumerate(doc['records']) if r['decision']=='retention')
    add('unjustified-retention',APPROVED,['records',retention,'retention_reason'],'')
    add('missing-speech',APPROVED,['records'],doc['records'][:-1])
    add('duplicate-speech',APPROVED,['records',1],doc['records'][0])
    info=next(i for i,r in enumerate(doc['records']) if r['base_QA_report']['base_QA_issues'])
    add('lost-row-reason',APPROVED,['records',info,'row_count_reason'],'')
    add('invented-second-page',APPROVED,['records',indices[114],'native_page_count'],2)
    for i,row in enumerate(doc['records']):
        if row['qa_waivers']:
            for key,value in [('qa_waivers',[]),('qa_waiver_reason','A broad exception.')]:add('waiver-'+key+'-'+row['id'],APPROVED,['records',i,key],value)
            for field in ['id','source_hex','compiled_hex','line','last_word','next_word','exact_issue']:
                value=3 if field=='line' else ('changed' if field!='exact_issue' else dict(code='weak-line-ending',message='changed',severity='warning'))
                add('waiver-scope-'+field+'-'+row['id'],APPROVED,['records',i,'qa_waiver_scope',field],value)
    for flag in owned.FLAGS:add('map-flag-'+flag,MAP,[flag],False)
    group=original(MAP)['groups'][0]
    for key,value in [('source_header_hex','4353000000000000'),('target_header_hex','4353000000000000'),('source_block_sha256','0'*64),('target_tail_bytes',0),('block',49)]:add('map-group-'+key,MAP,['groups',0,key],value)
    add('invented-relative-site',MAP,['groups',0,'relative_fixups'],[dict(new_matched_skip_target=8)])
    for i,c in enumerate(group['command_map']):add('command-extent-'+str(i),MAP,['groups',0,'command_map',i,'new_extent'],c['new_extent']+2)
    native=original(p['native_font_proof'])
    for key,value in [('fresh_compiled_alignment_cases',19),('reused_compiled_alignment_cases',91),('complete_progressive_paragraphs',27),('complete_progressive_pages',29)]:add('native-'+key,p['native_font_proof'],[key],value)
    add('native-compiled',p['native_font_proof'],['records',0,'compiled_hex'],native['records'][0]['compiled_hex']+'20')
    duplicate=deepcopy(native['records']);duplicate[1]=deepcopy(duplicate[0]);add('native-duplicate',p['native_font_proof'],['records'],duplicate)
    add('native-page-missing',p['native_font_proof'],['records',indices[114],'pages'],[])
    stored=original(p['native_stored_proof'])
    for key,value in [('fresh_native_alignment_cases',59),('exact_reused_native_alignment_cases',51),('all28_native_ink_planes_exact_to_already_viewed',False),('all28_complete_stored_single_pages_exact_to_viewed',False)]:add('stored-'+key,p['native_stored_proof'],[key],value)
    add('stored-alignment',p['native_stored_proof'],['records',0,'complete_native_stored_proof','native_alignment','cases',0,'output_hex'],'00')
    add('stored-byte',p['native_stored_proof'],['records',0,'stored_hex'],stored['records'][0]['stored_hex']+'20')
    for index in [40,61,108]:
        i=indices[index];add('stored-name-expansion-'+str(index),p['native_stored_proof'],['records',i,'expanded_stored_hex'],stored['records'][i]['stored_hex'][2:])
    controls=original(p['relocated_control_proof'])
    add('native-carry-erased',p['relocated_control_proof'],['normal_seeded_ends',1,'native_result',1],controls['normal_seeded_ends'][1]['native_result'][1]^1)
    add('invented-predicate',p['relocated_control_proof'],['relocated_predicates_andqueries'],[dict(word=1)])
    for key in ['all_nine_nonrelative_controls_oneA000_4821_4720_4681_andcomplete_end_bytes_exact','zero_relative_predicate_query_sites_not_fabricated_execution_coverage','source_relocated4821_descriptor_layout_calls_andall_4MiB_ABI_guards_equal']:add('control-'+key,p['relocated_control_proof'],[key],False)
    add('loader-343',p['native_loader_proof'],['fresh_native_whole_loads_andcache_hits'],342)
    add('loader-parent-modes',p['native_loader_proof'],['fresh_initial_parent_modes'],685)
    add('caller-alias',p['native_caller_proof'],['only_original24070_interpreter_call_no_literal_alias'],False)
    add('invented-caller-relative',p['native_caller_proof'],['relative_operand_maps'],[dict(new_matched_skip_target=8)])
    policy=original(p['native_policy_validation'])
    add('policy-positive-missing',p['native_policy_validation'],['positives'],policy['positives'][:-1])
    add('policy-negative-unrejected',p['native_policy_validation'],['negatives',0,'rejected'],False)
    add('policy-wrong-guard',p['native_policy_validation'],['negatives',0,'expected_guard'],'guard-not-present')
    add('actual-sheet-unviewed',p['actual_approval'],['directly_viewed_sheets',0,'directly_viewed'],False)
    add('actual-control-scope-erased',p['actual_approval'],['observed_all37_original_commands_eachlanguage_and10_initializers'],False)
    add('actual-warning-scope-erased',p['actual_approval'],['exact_two_QA_waivers18_infos_all_original_diagnostics_preserved'],False)
    add('invented-native-only-list',p['actual_proof'],['native_only_unvisited_speech_IDs'],[doc['records'][0]['id']])
    names=original(p['speaker_name_review'])
    for i,n in enumerate(names['records']):
        add('wrong-name-'+str(n['actor_ID']),p['speaker_name_review'],['records',i,'name'],n['name']+'x')
        add('actual-header-erased-'+str(n['actor_ID']),p['speaker_name_review'],['records',i,'actual_B50_progressive_nameplate_verified'],False)
    actual=original(p['actual_proof'])
    for gi,g in enumerate(actual['groups']):
        for key,value in [('incomplete_sampled_holds',1),('native_terminal_result',[0,1]),('observed_original_exchange_commands',36),('exit_frame',g['exit_frame']+1),('unidentified_trace_rows',[dict(unknown=True)])]:add('actual-'+key+'-'+str(gi),p['actual_proof'],['groups',gi,key],value)
        for ci,c in enumerate(g['command_pairs']):
            if c['canonical_source_offset'] is not None:add('actual-canonical-command-'+str(gi)+'-'+str(ci),p['actual_proof'],['groups',gi,'command_pairs',ci,'canonical_source_offset'],c['canonical_source_offset']+2)
        for si,s in enumerate(g['speech_observations']):
            add('actual-complete-name-mask-'+str(gi)+'-'+str(si),p['actual_proof'],['groups',gi,'speech_observations',si,'complete_body_holds',0,'complete_name_mask_equal'],False)
        for ci,c in enumerate(g['command_pairs']):
            if c['canonical_source_offset'] is not None and c['word'] in [0x4821,0xA000,0x4720,0x4681]:
                add('actual-control-result-'+str(gi)+'-'+str(ci),p['actual_proof'],['groups',gi,'command_pairs',ci,'native_result'],[3,1])
    en=next(i for i,g in enumerate(actual['groups']) if g['version']=='English')
    for key,value in [('native_page_count',2),('ordinary_page_transitions',[dict(from_page=1,to_page=2)])]:add('invented-'+key,p['actual_proof'],['groups',en,'speech_observations',0,key],value)
    add('actual-body-mask',p['actual_proof'],['groups',en,'speech_observations',0,'complete_body_holds',0,'complete_black_ASCII_gray_CP932_gray_masks_equal'],False)
    add('hold-outside-interval',p['actual_proof'],['groups',en,'speech_observations',0,'complete_body_holds',0,'frame'],1)
    add('actual-page-unobserved',p['actual_proof'],['groups',en,'speech_observations',0,'actual_complete_page_holds',0],[])
    add('wrong-native-plane',p['actual_proof'],['groups',en,'speech_observations',0,'native_planes',0,'sha256'],'0'*64)
    add('source-linear-block',p['source_path_proof'],['groups',0,'block'],49)
    add('source-linear-sequence',p['source_path_proof'],['groups',0,'commands'],original(p['source_path_proof'])['groups'][0]['commands'][:-1])
    focus=original(p['focused_picture_transition_andrisk'])
    add('opaque-effect-bridge',p['focused_picture_transition_andrisk'],['source_4821_A000_4720_4681_original_effect_bodies_executed_no_opaque_bridge'],False)
    add('risk-causal-limit-erased',p['focused_picture_transition_andrisk'],['bounded_comparison_not_every_frame_orcomplete_causal_trace'],False)
    for gi,g in enumerate(focus['groups']):
        for ci,c in enumerate(g['controls']):add('focused-control-result-'+str(gi)+'-'+str(ci),p['focused_picture_transition_andrisk'],['groups',gi,'controls',ci,'native_result'],[0,0])
        for f in g['sampled_native_values']:
            seed=g['sampled_native_values'][f]['PRNG_seed'];add('risk-sample-seed-'+str(gi)+'-'+str(f),p['focused_picture_transition_andrisk'],['groups',gi,'sampled_native_values',f,'PRNG_seed'],seed^1)
    for i,r in enumerate(focus['sampled_phase_comparisons']):
        add('risk-component-metadata-'+str(i),p['focused_picture_transition_andrisk'],['sampled_phase_comparisons',i,'component_equality','models'],not r['component_equality']['models'])
    add('risk-underway-byte-erased',p['focused_picture_transition_andrisk'],['sampled_phase_comparisons',7,'regions','ship_0','all_byte_differences'],[])
    for key,value in [('source_English_exits',[10822,10822]),('whole_actors_equal',True),('final_PRNG_seeds',[1,1]),('later_sample_count',86)]:add('later-'+key,p['later_scope_proof'],['groups',0,key],value)
    add('later-calendar-equality',p['later_scope_proof'],['groups',0,'five_native_component_equality','calendar'],False)
    later=original(p['later_scope_proof']);add('later-RGB-erased',p['later_scope_proof'],['groups',0,'later_RGB_differences'],later['groups'][0]['later_RGB_differences'][:-1])
    for key,value in [('same_initial_seed',1),('exit_English_phase',0),('final_English_phase',0)]:add('RNG-'+key,p['RNG_scope_proof'],['groups',0,key],value)
    for key in ['earlier_contract_reused_only_for_exact_unchanged_code_not_fresh_every_call_causal_trace','exact_RNG_state_future_random_outcomes_orfull_simulation_equality_NOT_verified']:add('RNG-limit-'+key,p['RNG_scope_proof'],[key],False)
'''
if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('scripts/challenge_Rafael_B49_atomic_v8120.py').read_text('utf8')
    prefix=source[source.index('    tests=[]'):source.index('    # Reuse only the trusted')]
    receipt=derive('scripts/challenge_Rafael_B49_atomic_v8120.py','scripts/challenge_Rafael_B50_atomic_v8170.py',{
        prefix:TESTS,
        'scripts.validate_Rafael_B49_policy_v8113':'scripts.validate_Rafael_B50_policy_v8163',
        'scripts.Rafael_B49_release_paths_v8114':'scripts.Rafael_B50_release_paths_v8164',
        'Rafael_B49_atomic_challenges_v8120':'Rafael_B50_atomic_challenges_v8170',
        'Rafael_B49_atomic_positive_v8119':'Rafael_B50_atomic_positive_v8169',
        'r370=indices[388]':'r370=indices[108]',
        'positive_records=61':'positive_records=28','B49':'B50',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',receipt)
    print('Prepared B50 independent actual-changing proof corruptions withtrusted contract revalidation andprecommit traps.')
