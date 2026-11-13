"""Prepare independent direct-ROM/credit/scope audit before changing the shared ledger."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_completion_audit_tools_v8784');assert not root.exists()
    source=Path('scripts/audit_Hodram_B52_completion_v8717.py').read_text('utf-8')
    a=source.index('    typed=next(');z=source.index("    assert new['current_integrated_candidate']",a)
    scope="""    scope=read(completion.RELEASE)['actual_scope_limits']
    assert scope['actual_unique_speech_IDs']==['DK4_MES_B31_R0018','DK4_MES_B53_R0007'] and scope['unvisited_conditional_text_IDs']==['DK4_MES_B31_R0013']
    assert (scope['complete_page_occurrences'],scope['complete_body_name_holds'],scope['total_actual_frames'])==(4,76,24004)
    assert [g['later_RGB_difference_count'] for g in scope['measured_comparisons']]==[0,0]
    assert all(g['whole_actors_equal'] and all(g['five_native_component_equality'].values()) for g in scope['measured_comparisons'])
    pending=new[completion.NEXT_KEY]
    assert pending['blocks']==[54,55,56,57,58,59,60] and pending['physical_speeches']==82 and pending['typed_choice_labels']==0 and pending['completion_credit_added']==0 and pending['current_English_forall_seven_blocks_still_unconsulted']
    pendingkeys={historical_key(r) for group in pending['source_groups'] for r in group['records']}
    assert len(pendingkeys)==82 and not pendingkeys&newkeys
    prior=read(completion.PRIOR);oldscope=read(old[prior['unfinished_scope']]['path']);newscope=read(new[completion.SCOPE]['path'])
    assert all(newscope[k]==v for k,v in oldscope.items()) and set(newscope)-set(oldscope)=={completion.KEY,completion.NEXT_KEY,'latest_next_focus_v8783'}
"""
    receipt=derive('scripts/audit_Hodram_B52_completion_v8717.py','scripts/audit_Hodram_B31_B53_completion_v8784.py',{
        source[a:z]:scope,
        'complete_Hodram_B52_v8715':'complete_Hodram_B31_B53_v8783',
        'Hodram_B52_completion_audit_v8717':'Hodram_B31_B53_completion_audit_v8784',
        '==[5,5,5,2,3]':'==[3,3,3,3,0]',
        "doc['records']+doc['typed_choice_records']":"doc['records']",
        'len(oldkeys)==7229 and len(newkeys)==7234':'len(oldkeys)==7234 and len(newkeys)==7237',
        'len(rows)==5 and Counter(r[\'decision\'] for r in rows)==dict(revision=2,retention=3)':'len(rows)==3 and Counter(r[\'decision\'] for r in rows)==dict(revision=3)',
        "blocks=[IlnkContainer.parse(i.read_file('/data/SC1.DK4')).blocks[52] for i in [clean,predecessor,current]]":"banks=[IlnkContainer.parse(i.read_file('/data/SC1.DK4')).blocks for i in [clean,predecessor,current]]",
        '    for row,before in zip(rows,approved,strict=True):':'    for row,before in zip(rows,approved,strict=True):\n        blocks=[bank[row["block"]] for bank in banks]',
        "assert not row['individually_activated_in_current_build'] and row['actual_initialized_source_andEnglish_selected_paths_observed']":"assert not row['individually_activated_in_current_build'] and row['actual_initialized_source_andEnglish_selected_paths_observed']==(row['id']!='DK4_MES_B31_R0013')\n        assert row['offline_only_variant_with_complete_native_andrepresentative_sameconsumer_evidence']==(row['id']=='DK4_MES_B31_R0013')",
        "assert row['actual_live_owner_RAM_VRAM_palette_andunowned_backing_byte_identity_unobserved']":"assert row['opaque_effect_gameplay_semantics_outer_eligibility_andfuture_causality_remain_unproven']",
        "['/data/SC1.DK4']==154":"['/data/SC1.DK4']==157",
        'five_disjoint_new_keys_only':'three_disjoint_new_keys_only',
        'counter_deltas=[5,5,5,2,3]':'counter_deltas=[3,3,3,3,0]',
        'three_speeches_two_typed_choices_exact_source_predecessor_final_ROM_references':'three_speeches_two_blocks_nochoices_exact_source_predecessor_final_ROM_references',
        'canonical_choice_ID13_preserved_despite_final_physical_record12':'canonical_source_IDs13_18_7_andall_final_recordindices_preserved',
        'all_actual_vs_offline_long_divergence_andfocused_agreement_limits_preserved':'two_observed_utterances_andshort_B31_offline_scope_all_bounded_comparison_limits_preserved',
        'no_natural_activation_orlive_backing_scope_upgrade':'no_natural_activation_fullcatalogue_orunvisited_variant_scope_upgrade',
        'next_three_B31_B53_clean_glosses_disjoint_uncredited_older_English_unread':'next82_B54_B60_clean_glosses_disjoint_uncredited_older_English_unread',
        'Independent B52 completion audit:exactly5new keys/2revisions/3retentions;all directROMrefs andwhole priorinverse. Choice13->physical12 preserved;three nextglosses uncredited. Full scope active.':'Independent B31/B53 completion audit:exactly3new keys/allrevisions;all direct source/predecessor/final ROMrefs andfull priorinverse. Shortvariant offline,next82meanings uncredited,all oldscopevalues exact. Full scope active.',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,all_original_direct_ROM_reference_approved_word_pendingflag_counter_delta_inverse_anddocument_guards_preserved=True,
        both_source_blocks_three_exact_disjoint_keys_zero_retention_duplicates_andall82_next_positions_uncredited=True,
        source_coverage_current_positions_names_actual_vs_offline_andall_prior_scope_values_independently_checked=True,
        no_shared_ledger_ROM_orregistry_mutation_by_preparer=True,full_goal_complete=False))
