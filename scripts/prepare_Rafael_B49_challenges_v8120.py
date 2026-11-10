"""Prepare distinct semantic precommit challenges for B49; no FE or multi-page assumptions."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B49_challenge_tools_v8120')
if __name__=='__main__':
    assert not ROOT.exists()
    src=Path('scripts/challenge_Rafael_B48_atomic_v8064.py').read_text('utf8')
    multipage=src[src.index("    add('actual-page2-unobserved'"):src.index("    for key,value in [('source_English_exits'",src.index("    add('actual-page2-unobserved'"))]
    feblock=src[src.index('    enFE=next'):src.index('    for group_index,g in enumerate(actual',src.index('    enFE=next'))]
    new_actual='''    add('actual-first-page-unobserved',p['actual_proof'],['groups',en,'speech_observations',0,'actual_complete_page_holds',0],[])
    add('invented-second-page',p['actual_proof'],['groups',en,'speech_observations',0,'native_page_count'],2)
    add('invented-page-turn',p['actual_proof'],['groups',en,'speech_observations',0,'ordinary_page_transitions'],[dict(from_page=1,to_page=2)])
    add('wrong-native-plane',p['actual_proof'],['groups',en,'speech_observations',0,'native_planes',0,'sha256'],'0'*64)
    add('wrong-actual-canonical-source',p['actual_proof'],['groups',en,'command_pairs',12,'canonical_source_offset'],74)
    for gi,g in enumerate(actual['groups']):
        ci=next(i for i,c in enumerate(g['command_pairs']) if c['word']==0xC281)
        for field,value in [('decoded_length',4),('native_result',[3,1]),('canonical_source_offset',74)]:
            add('actual-C281-'+field+'-'+str(gi),p['actual_proof'],['groups',gi,'command_pairs',ci,field],value)
    flow=original(p['source_path_proof'])
    add('source-composition-count',p['source_path_proof'],['structural_compositions_evaluated'],1)
    add('source-branch-union-erased',p['source_path_proof'],['all154_commands61_speeches_in_structural_union'],False)
    add('source-representative-paths-erased',p['source_path_proof'],['representative_text_paths'],[])
    focus=original(p['focused_C281_transition'])
    add('C281-opaque-bridge-misclaimed',p['focused_C281_transition'],['groups',0,'original_C281_effect_body_executed_in_core_no_opaque_bridge'],False)
    add('C281-focused-result',p['focused_C281_transition'],['groups',0,'C281_command','native_result'],[0,0])
    add('focused-Camille-truncated-name',p['focused_C281_transition'],['groups',0,'actual_complete_Lil_Camille_nameplates',1,'name'],'Camille Overijsse')
    add('focused-conditional-header-invented',p['focused_C281_transition'],['groups',0,'observed_nameplate_actors'],[0,2,4,5,9])
'''
    result=derive('scripts/challenge_Rafael_B48_atomic_v8064.py','scripts/challenge_Rafael_B49_atomic_v8120.py',{
        'validate_Rafael_B48_policy_v8059':'validate_Rafael_B49_policy_v8113',
        'Rafael_B48_release_paths_v8060':'Rafael_B49_release_paths_v8114',
        'Rafael_B48_atomic_challenges_v8064':'Rafael_B49_atomic_challenges_v8120',
        'Rafael_B48_atomic_positive_v8063':'Rafael_B49_atomic_positive_v8119',
        'B48':'B49','positive_records=91':'positive_records=61',
        'r347=indices[347]':'r347=indices[244]',
        "'R347-lost-second-page',APPROVED,['records',r347,'native_page_count'],1":"'invented-second-page',APPROVED,['records',r347,'native_page_count'],2",
        "indices[86],'actual_record_observed'":"indices[32],'actual_record_observed'",
        "native['records'][r347]['pages'][:1]":"[]",
        'native-R347-page-missing':'native-single-page-missing',
        "('R347_both_complete_stored_pages_exact_to_viewed',False)":"('all61_complete_stored_single_pages_exact_to_viewed',False)",
        'all91_native_ink':'all61_native_ink',
        'all44_nonrelative_controls_threeA000_andcomplete_end_bytes_exact':'all37_nonrelative_controls_sevenA000_C281_andcomplete_end_bytes_exact',
        'all_five_raw_predicates_andtwo_completion_queries_current_unforced_values_andunaligned_scratch_restore_preserved':'all13_raw_predicates_andone_completion_query_current_unforced_values_andunaligned_scratch_restore_preserved',
        'seventh-query-lost':'fourteenth-predicate-query-lost',
        'thirteen_conditional_speeches_andthree_headers_not_claimed_as_actual_coverage':'eleven_conditional_speeches_andthree_headers_not_claimed_as_actual_coverage',
        'exact_two_QA_waivers_with_all_original_diagnostics_preserved':'exact_three_QA_waivers22_infos_all_original_diagnostics_preserved',
        "    add('wrong-Janus-name',p['speaker_name_review'],['records',1,'name'],'Janus Pasha')":"    janus=next(i for i,n in enumerate(names['records']) if n['actor_ID']==4)\n    add('wrong-Janus-name',p['speaker_name_review'],['records',janus,'name'],'Janus Pasha')",
        "['records',1,'actual_B48_progressive_nameplate_verified']":"['records',janus,'actual_B49_progressive_nameplate_verified']",
        "    en347=next(i for i,s in enumerate(actual['groups'][en]['speech_observations']) if s['id']=='DK4_MES_B48_R0347')\n":'',
        multipage:new_actual,
        "('whole_actors_equal',True)":"('whole_actors_equal',False)",
        feblock:'',
        'r370=indices[370]':'r370=indices[388]',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared B49 proof-corruption challenges including full C281/path/name scope; no shared input mutations.')
