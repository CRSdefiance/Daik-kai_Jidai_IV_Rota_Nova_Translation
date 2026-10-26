"""Eight city-challenge final audit with explicit direct-parent/speaker checks."""
from pathlib import Path
OLD=Path('scripts/verify_editorial_handoff_v2545.py')
if __name__=='__main__':
 outer=OLD.read_text();needle="\n exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})";assert outer.count(needle)==1
 env={'__name__':'__main__','__file__':__file__};exec(compile(outer.replace(needle,'\n captured_effective_source=source'),__file__,'exec'),env);source=env['captured_effective_source']
 changes={
  'editorial_handoff_verification_v2545':'editorial_handoff_verification_v2569','V2545-audit-of-V2544':'V2569-audit-of-V2568','IDS=tuple(range(2046,2052))':'IDS=tuple(range(2038,2046))',
  '2005':'2035','1349':'1379','aftermath_fled_contextual':'aftermath_city_contextual',"final['retained_count']==6":"final['retained_count']==8",
  "{'original-53D44-role1-fled-victory-portrait':6}":"{'original-53F0C-defending-captain-city-challenge-portrait':8}",
  "final['current_native_aftermath_fled_font_executions']==6":"final['current_native_aftermath_city_font_executions']==8","final['current_native_copies']==12":"final['current_native_copies']==16",
  "final['historical_report_and_sailing_return_transitions_current_bound']==2":"final['historical_challenge_and_defender_battle_entry_transitions_current_bound']==3",
  'work/analysis/aftermath_fled_fonts_v2542b/native_font_proof.json':'work/analysis/aftermath_city_fonts_v2566/native_font_proof.json',
  "font['complete_native_font_cases']==6":"font['complete_native_font_cases']==8","len(font['all6_original_role1_pipelines'])==6":"len(font['all8_original_direct_defender_pipelines'])==8",
  'work/analysis/aftermath_fled_history_v2543/historical_aftermath_fled_current_binding.json':'work/analysis/aftermath_city_history_v2567/historical_aftermath_city_current_binding.json',
  "history['historical_IDs']==[2046]":"history['historical_IDs']==[2043]","history['only2046_has_individual_historical_activation_other5_use_family_sample']":"history['only2043_has_individual_historical_activation_other7_use_family_sample']",
  "notes['original_role_selector']==1 and notes['original_parent']==0x02053DB8 and notes['original_table_stack_offset']==0x27C and all(r['source_role_selector']==1 for r in history['historical_holds'])":"notes['original_entry']==0x02053F0C and notes['original_parent']==0x02053F40 and notes['original_table_stack_offset']==0x274 and all(r['original_entry']==0x02053F0C and r['source_actor_ID']==46 for r in history['historical_holds'])",
  "len(history['six_negative_controls_current_binding_on_offline_clones'])==6":"len(history['eight_negative_controls_current_binding_on_offline_clones'])==8",
  "history['six_negative_controls_current_binding_on_offline_clones']":"history['eight_negative_controls_current_binding_on_offline_clones']",
  "len(context['original_three_outcome_prefixes'])==3":"len(context['three_current_original_city_defender_captain_bindings'])==3",
  'work/analysis/aftermath_fled_completion_v2544/completion_receipt.json':'work/analysis/aftermath_city_completion_v2568/completion_receipt.json',"h['fresh_reconciliations']==6":"h['fresh_reconciliations']==8",
  'work/analysis/aftermath_fled_completion_v2544/remaining_historical_fresh_review_inventory.json':'work/analysis/aftermath_city_completion_v2568/remaining_historical_fresh_review_inventory.json',
  "inv['remaining']==138":"inv['remaining']==108","'/COMMON/MESFILE.DK4':137,":"'/COMMON/MESFILE.DK4':107,",'# Current editorial handoff - V2544':'# Current editorial handoff - V2568',
  'completed_this_goal_turn=6,retained=6':'completed_this_goal_turn=8,retained=8','all6_exact_clean_current_integrated_references_payloads_and_five_gates':'all8_exact_clean_current_integrated_references_payloads_and_five_gates',
  'remaining_historical_fresh_reviews=138':'remaining_historical_fresh_reviews=108','all6_flight_victory_reviews_and_evidence_pass=True':'all8_direct_city_reviews_and_evidence_pass=True','retentions=6,metadata_revisions=0':'retentions=8,metadata_revisions=0',
 }
 for a,b in changes.items():
  assert a in source,a
  source=source.replace(a,b)
 extra=""" assert notes['original_source_table']==0x021178C0 and notes['source_speaker_is_defending_fleet_captain']
 assert font['no_actor_or_roster_fixture']and font['all_original_actor_model_bytes_unchanged']and font['CPU_actor_or_roster_fixtures']==[]
 assert all(r['native_pipeline']['original_entry']==0x02053F0C and r['native_pipeline']['parent']==0x02053F40 and r['native_pipeline']['selector_offset']==0x274 for r in font['cases'])
 states=history['eight_original_challenge_and_battle_entry_mode_states'];assert len(states)==8 and states[-2]['mode8_12_16']==states[-1]['mode8_12_16']==[0,1,22]
 fixture=history['sole_fixture_disclosure'];assert len(fixture['owned_bytes'])==16 and len(fixture['changes'])==10 and fixture['only_own_cached_and_live_position_changed']
 assert history['original_presence_share_and_unforced_one_in_three_choice_preserved']and history['older_war_pilot1283b_not_used_for_credit']
"""
 needle=' ROOT.mkdir(parents=True)';assert source.count(needle)==1;source=source.replace(needle,extra+needle)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
