"""Preserve independent once-only accounting, direct three-ROM references and every unfinished-scope value."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_completion_audit_tools_v8871');assert not root.exists()
    source=Path('scripts/audit_Hodram_B31_B53_completion_v8784.py').read_text(encoding='utf-8')
    a=source.index('    pending=new[completion.NEXT_KEY]');z=source.index('    prior=read(completion.PRIOR)',a)
    pending="""    pending=new[completion.NEXT_KEY]
    assert pending['blocks']==list(range(61,71)) and pending['physical_speeches']==224 and pending['typed_choice_labels']==0 and pending['completion_credit_added']==0 and pending['current_English_forall_ten_blocks_still_unconsulted']
    assert pending['first_meanings_completed']==44 and pending['other_first_meanings_pending']==180 and not pending['all224_glossed']
    pendingkeys={historical_key(r) for group in pending['source_groups'] for r in group['records']}
    assert len(pendingkeys)==224 and not pendingkeys&newkeys
    source_rows={r['id']:r for g in pending['source_groups'] for r in g['records']}
    meaning_rows=[r for g in pending['first_meaning_groups'] for r in g['records']]
    assert len(meaning_rows)==44 and len({r['id'] for r in meaning_rows})==44
    for r in meaning_rows:
        assert all(r[k]==source_rows[r['id']][k] for k in ['source_hex','source_reference','source_selector','source_Japanese'])
        assert r['source_meaning_gloss'] and r['whole_exchange_fidelity_note'] and r['current_English_dialogue_still_unconsulted']
"""
    result=derive('scripts/audit_Hodram_B31_B53_completion_v8784.py','scripts/audit_Hodram_B54_B60_completion_v8871.py',{
      source[a:z]:pending,
      'Independently audit exactly five B52 credits':'Independently audit exactly82 B54-B60 credits',
      'complete_Hodram_B31_B53_v8783':'complete_Hodram_B54_B60_v8870','Hodram_B31_B53_completion_audit_v8784':'Hodram_B54_B60_completion_audit_v8871',
      '==[3,3,3,3,0]':'==[82,82,82,46,36]',
      'len(oldkeys)==7234 and len(newkeys)==7237':'len(oldkeys)==7237 and len(newkeys)==7319',
      "len(rows)==3 and Counter(r['decision'] for r in rows)==dict(revision=3)":"len(rows)==82 and Counter(r['decision'] for r in rows)==dict(revision=46,retention=36)",
      "(row['id']!='DK4_MES_B31_R0013')":"(row['id'] in final['actual_unique_speech_IDs'])",
      "(row['id']=='DK4_MES_B31_R0013')":"(row['id'] in final['offline_only_text_IDs'])",
      'offline_only_variant_with_complete_native_andrepresentative_sameconsumer_evidence':'offline_only_speech_with_complete_native_andrepresentative_sameconsumer_evidence',
      "scope['actual_unique_speech_IDs']==['DK4_MES_B31_R0018','DK4_MES_B53_R0007'] and scope['unvisited_conditional_text_IDs']==['DK4_MES_B31_R0013']":"len(scope['actual_unique_speech_IDs'])==63 and len(scope['offline_only_text_IDs'])==19 and len(scope['unvisited_conditional_text_IDs'])==18",
      '==(4,76,24004)':'==(150,676,130014)',
      "[g['later_RGB_difference_count'] for g in scope['measured_comparisons']]==[0,0]":"[g['later_RGB_difference_count'] for g in scope['measured_comparisons']]==[3,0,0,3,65,61,11]",
      "all(g['whole_actors_equal'] and all(g['five_native_component_equality'].values()) for g in scope['measured_comparisons'])":"not scope['measured_comparisons'][5]['whole_actors_equal'] and scope['measured_comparisons'][6]['whole_actors_equal'] and all(scope['measured_comparisons'][6]['five_native_component_equality'].values())",
      "old[prior['unfinished_scope']]":"old['unfinished_editorial_scope_v8861']",
      'latest_next_focus_v8783':'latest_next_focus_v8870',
      "['/data/SC1.DK4']==157":"['/data/SC1.DK4']==239",
      'three_disjoint_new_keys_only':'eighty_two_disjoint_new_keys_only','counter_deltas=[3,3,3,3,0]':'counter_deltas=[82,82,82,46,36]',
      'three_speeches_two_blocks_nochoices_exact_source_predecessor_final_ROM_references':'82_speeches_seven_blocks_nochoices_exact_source_predecessor_final_ROM_references',
      'canonical_source_IDs13_18_7_andall_final_recordindices_preserved':'all82_canonical_source_IDs_andall_final_recordindices_preserved',
      'two_observed_utterances_andshort_B31_offline_scope_all_bounded_comparison_limits_preserved':'63_observed_utterances19_offline_all_main_focused_actor_RNG_RGB_andbounded_comparison_limits_preserved',
      'next82_B54_B60_clean_glosses_disjoint_uncredited_older_English_unread':'next224_B61_B70_candidates_first44_meanings180_notglossed_disjoint_uncredited_older_English_unread',
      'Independent B31/B53 completion audit:exactly3new keys/allrevisions;all direct source/predecessor/final ROMrefs andfull priorinverse. Shortvariant offline,next82meanings uncredited,all oldscopevalues exact. Full scope active.':'Independent B54-B60 completion audit:82new keys/46revisions36retentions;all direct source/predecessor/final ROMrefs andfull priorinverse.63actual19offline;next224 candidates/first44 meanings uncredited;all oldscopevalues exact.Full scope active.',
    })
    root.mkdir(parents=True);save(root/'source_locked_completion_auditor.json',dict(auditor=result,full_prior_ledger_inverse_all82_approved_records_three_ROM_references_onceonly_deltas_andall_document_bytes_preserved=True,63actual19offline_all_main_focused_differences_andnext224_inventory44_meanings180_pending_explicitly_verified=True,no_staged_audit_orcredit_before_release_startup_andcompletion_stage=True,new_credit=0,full_goal_complete=False))
