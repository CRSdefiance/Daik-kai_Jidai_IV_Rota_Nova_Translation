"""Prepare independent real proof mutations, including distinct FE/source-cell/macro cases."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    changes={
        'B47':'B48','R53':'R347','r53':'r347','en53':'en347','R0053':'R0347',
        'Rafael_B47_atomic_challenges_v8011':'Rafael_B48_atomic_challenges_v8064',
        'Rafael_B47_atomic_positive_v8010':'Rafael_B48_atomic_positive_v8063',
        'validate_Rafael_B47_policy_v8005':'validate_Rafael_B48_policy_v8059',
        'Rafael_B47_release_paths_v8006':'Rafael_B48_release_paths_v8060',
        'indices[53]':'indices[347]','indices[63]':'indices[86]',
        'all15_native_ink':'all91_native_ink',
        'R53_both_complete_stored_pages_exact_to_viewed_sentence_boundary_pages':'R347_both_complete_stored_pages_exact_to_viewed',
        'relocated_predicates':'relocated_predicates_andqueries',
        'sixth-predicate-lost':'seventh-query-lost',
        'original61FF_A000_andcomplete_normal_end_bytes_exact':'all44_nonrelative_controls_threeA000_andcomplete_end_bytes_exact',
        'all_six_raw_predicates_current_unforced_values_preserved_including_unaligned_scratch_restore':'all_five_raw_predicates_andtwo_completion_queries_current_unforced_values_andunaligned_scratch_restore_preserved',
        'four_conditional_speeches_andJanus_header_not_claimed_as_actual_coverage':'thirteen_conditional_speeches_andthree_headers_not_claimed_as_actual_coverage',
        "('observed_original_exchange_commands',48)":"('observed_original_exchange_commands',163)",
        '],4719)':'],18399)',
        "add('later-calendar-difference-erased',p['later_scope_proof'],['groups',0,'five_native_component_equality','calendar'],True)":"add('later-calendar-equality-erased',p['later_scope_proof'],['groups',0,'five_native_component_equality','calendar'],False)",
        'positive_records=15':'positive_records=91',
        '    protected=[config,':'''    # Reuse only the trusted, immutable frozen contract during changed-proof cases.
    # Its dependency bytes are fully checked before and after the loop; all semantic
    # comparisons, modified proof loads, profile equality and commit traps remain active.
    from dk4tool.dialogue import rafael_B48_profile_v1 as frozen_module
    original_native_contract=frozen_module.contract
    trusted_contract=original_native_contract()
    trusted_snapshot=deepcopy(trusted_contract)
    original_owned_contract=owned.contract
    enFE=next(i for i,s in enumerate(actual['groups'][en]['speech_observations']) if s['source_selector']==254)
    add('FE-stale-nameplate',p['actual_proof'],['groups',en,'speech_observations',enFE,'complete_body_holds',0,'original_FE_absent_nameplate_preserved'],False)
    add('FE-wrong-geometry',p['actual_proof'],['groups',en,'speech_observations',enFE,'complete_body_holds',0,'native_geometry'],[216,64])
    add('FE-invented-name',p['actual_proof'],['groups',en,'speech_observations',enFE,'actual_name'],'Hans Letzel')
    add('FE-wrong-consumer',p['actual_proof'],['groups',en,'speech_observations',enFE,'kind'],'progressive')
    ja=next(i for i,g in enumerate(actual['groups']) if g['version']=='clean_Japanese')
    j129=next(i for i,s in enumerate(actual['groups'][ja]['speech_observations']) if s['id']=='DK4_MES_B48_R0129')
    add('source-R129-right-cell-erased',p['actual_proof'],['groups',ja,'speech_observations',j129,'complete_body_holds',0,'native_geometry'],[216,64])
    for group_index,g in enumerate(actual['groups']):
        add('later-reentry-scope-erased-'+str(group_index),p['actual_proof'],['groups',group_index,'complete_first_exchange_distinguished_from_later_fixture_reentry'],False)
    r370=indices[370]
    add('stored-FI-expansion-erased',p['native_stored_proof'],['records',r370,'expanded_stored_hex'],stored['records'][r370]['stored_hex'][2:])
    protected=[config,''',
        '        owned.check_dependencies=lambda conf:None;owned.commit_files=forbidden':'''        owned.check_dependencies=lambda conf:None;owned.commit_files=forbidden
        frozen_module.contract=lambda:trusted_contract
        owned.contract=lambda:trusted_contract''',
        '    finally:owned.load,owned.check_dependencies,owned.commit_files=original_load,original_deps,original_commit':'''    finally:
        owned.load,owned.check_dependencies,owned.commit_files=original_load,original_deps,original_commit
        frozen_module.contract=original_native_contract;owned.contract=original_owned_contract
    assert trusted_contract==trusted_snapshot==original_native_contract()''',
        'config_dependency_digests_deliberately_bypassed=True,all_shared_files_andROMs_preserved=True':'config_dependency_digests_deliberately_bypassed=True,trusted_frozen_contract_read_once_revalidated_after_all_cases=True,all_semantic_guards_andcommit_traps_active=True,all_shared_files_andROMs_preserved=True',
    }
    print(derive('scripts/challenge_Rafael_B47_atomic_v8011.py','scripts/challenge_Rafael_B48_atomic_v8064.py',changes))
