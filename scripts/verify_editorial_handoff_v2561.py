"""Final audit of eight withdrawal retentions and historical town-state scope."""
from pathlib import Path
OLD=Path('scripts/verify_editorial_handoff_v2545.py')
if __name__=='__main__':
 outer=OLD.read_text();needle="\n exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})";assert outer.count(needle)==1
 env={'__name__':'__main__','__file__':__file__};exec(compile(outer.replace(needle,'\n captured_effective_source=source'),__file__,'exec'),env);source=env['captured_effective_source']
 changes={
  'editorial_handoff_verification_v2545':'editorial_handoff_verification_v2561','V2545-audit-of-V2544':'V2561-audit-of-V2560',
  'IDS=tuple(range(2046,2052))':'IDS=tuple(range(2114,2122))','2005':'2027','1349':'1371','aftermath_fled_contextual':'aftermath_withdrawal_contextual',
  "final['retained_count']==6":"final['retained_count']==8",
  "{'original-53D44-role1-fled-victory-portrait':6}":"{'original-53D44-role1-withdrawal-portrait':8}",
  "final['current_native_aftermath_fled_font_executions']==6":"final['current_native_aftermath_withdrawal_font_executions']==8",
  "final['current_native_copies']==12":"final['current_native_copies']==16",
  "final['historical_report_and_sailing_return_transitions_current_bound']==2":"final['historical_withdrawal_and_sailing_return_transitions_current_bound']==3",
  'work/analysis/aftermath_fled_fonts_v2542b/native_font_proof.json':'work/analysis/aftermath_withdrawal_fonts_v2558/native_font_proof.json',
  "font['complete_native_font_cases']==6":"font['complete_native_font_cases']==8","len(font['all6_original_role1_pipelines'])==6":"len(font['all8_original_role1_pipelines'])==8",
  'work/analysis/aftermath_fled_history_v2543/historical_aftermath_fled_current_binding.json':'work/analysis/aftermath_withdrawal_history_v2559/historical_aftermath_withdrawal_current_binding.json',
  "history['historical_IDs']==[2046]":"history['historical_IDs']==[2114]",
  "history['only2046_has_individual_historical_activation_other5_use_family_sample']":"history['only2114_has_individual_historical_activation_other7_use_family_sample']",
  "len(context['original_three_outcome_prefixes'])==3":"len(context['original_mode2_withdrawal_prefix'])==1",
  'work/analysis/aftermath_fled_completion_v2544/completion_receipt.json':'work/analysis/aftermath_withdrawal_completion_v2560/completion_receipt.json',
  "h['fresh_reconciliations']==6":"h['fresh_reconciliations']==8",
  'work/analysis/aftermath_fled_completion_v2544/remaining_historical_fresh_review_inventory.json':'work/analysis/aftermath_withdrawal_completion_v2560/remaining_historical_fresh_review_inventory.json',
  "inv['remaining']==138":"inv['remaining']==116","'/COMMON/MESFILE.DK4':137":"'/COMMON/MESFILE.DK4':115",'# Current editorial handoff - V2544':'# Current editorial handoff - V2560',
  'completed_this_goal_turn=6,retained=6':'completed_this_goal_turn=8,retained=8',
  'all6_exact_clean_current_integrated_references_payloads_and_five_gates':'all8_exact_clean_current_integrated_references_payloads_and_five_gates',
  'remaining_historical_fresh_reviews=138':'remaining_historical_fresh_reviews=116','all6_flight_victory_reviews_and_evidence_pass=True':'all8_withdrawal_reviews_and_evidence_pass=True',
  'retentions=6,metadata_revisions=0':'retentions=8,metadata_revisions=0',
 }
 for a,b in changes.items():
  assert a in source,a
  source=source.replace(a,b)
 extra=""" assert notes['original_source_table']==0x02117D00 and history['no_inputs_or_fixtures5910_through7310']
 assert all(r['assigned_original_First_Mate_actor']and r['source_actor_ID']==18 for r in history['historical_holds'])
 states=history['nine_original_town_movement_withdrawal_and_return_states'];assert len(states)==9
 assert all(r['mode8_12_16']==[0,0,0]and r['town_battle_ID']==115 for r in states if r['frame']in(7410,7510))
 fixture=history['sole_fixture_disclosure'];assert len(fixture['owned_bytes'])==18 and len(fixture['changes'])==12 and fixture['not_earned_travel_or_role_assignment']
"""
 needle=' ROOT.mkdir(parents=True)';assert source.count(needle)==1;source=source.replace(needle,extra+needle)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
