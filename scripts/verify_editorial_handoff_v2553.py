"""Scoped14-record final audit and exact complete-exchange references."""
from pathlib import Path
OLD=Path('scripts/verify_editorial_handoff_v2545.py')
if __name__=='__main__':
 outer=OLD.read_text();needle=" exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})";assert outer.count(needle)==1
 env={'__name__':'__main__','__file__':__file__};exec(compile(outer.replace(needle,' captured_effective_source=source'),__file__,'exec'),env);source=env['captured_effective_source']
 changes={
 'editorial_handoff_verification_v2545':'editorial_handoff_verification_v2553','V2545-audit-of-V2544':'V2553-audit-of-V2552',
 'IDS=tuple(range(2046,2052))':'IDS=(*range(2016,2022),*range(2138,2146))','2005':'2019','1349':'1363','aftermath_fled_contextual':'aftermath_defeat_contextual',
 "final['retained_count']==6":"final['retained_count']==14",
 "{'original-53D44-role1-fled-victory-portrait':6}":"{'original-53D44-role1-paired-defeat-portrait':14}",
 "final['current_native_aftermath_fled_font_executions']==6":"final['current_native_aftermath_defeat_font_executions']==14",
 "final['current_native_copies']==12":"final['current_native_copies']==28",
 "final['historical_actual_holds']==2":"final['historical_actual_holds']==4",
 "final['historical_report_and_sailing_return_transitions_current_bound']==2":"final['historical_paired_defeat_GameOver_title_transitions_current_bound']==4",
 'work/analysis/aftermath_fled_fonts_v2542b/native_font_proof.json':'work/analysis/aftermath_defeat_fonts_v2550/native_font_proof.json',
 "font['complete_native_font_cases']==6":"font['complete_native_font_cases']==14",
 "len(font['all6_original_role1_pipelines'])==6":"len(font['all14_original_role1_pipelines'])==14",
 'work/analysis/aftermath_fled_history_v2543/historical_aftermath_fled_current_binding.json':'work/analysis/aftermath_defeat_history_v2551b/historical_aftermath_defeat_current_binding.json',
 "history['historical_IDs']==[2046]":"history['historical_IDs']==[2016,2138]",
 "history['only2046_has_individual_historical_activation_other5_use_family_sample']":"history['only2016_and2138_have_individual_historical_activation_other12_use_family_sample']",
 "len(history['six_negative_controls_current_binding_on_offline_clones'])==6":"len(history['fourteen_negative_controls_current_binding_on_offline_clones'])==14",
 "history['six_negative_controls_current_binding_on_offline_clones']":"history['fourteen_negative_controls_current_binding_on_offline_clones']",
 "len(context['all208_original_voice_selections'])==208":"len(context['all416_original_selected_voice_choices'])==416",
 'work/analysis/aftermath_fled_completion_v2544/completion_receipt.json':'work/analysis/aftermath_defeat_completion_v2552/completion_receipt.json',
 "h['fresh_reconciliations']==6":"h['fresh_reconciliations']==14",
 'work/analysis/aftermath_fled_completion_v2544/remaining_historical_fresh_review_inventory.json':'work/analysis/aftermath_defeat_completion_v2552/remaining_historical_fresh_review_inventory.json',
 "inv['remaining']==138":"inv['remaining']==124","'/COMMON/MESFILE.DK4':137":"'/COMMON/MESFILE.DK4':123",
 '# Current editorial handoff - V2544':'# Current editorial handoff - V2552',
 'completed_this_goal_turn=6,retained=6':'completed_this_goal_turn=14,retained=14',
 'all6_exact_clean_current_integrated_references_payloads_and_five_gates':'all14_exact_clean_current_integrated_references_payloads_and_five_gates',
 'remaining_historical_fresh_reviews=138':'remaining_historical_fresh_reviews=124',
 'all6_flight_victory_reviews_and_evidence_pass=True':'all14_paired_defeat_reviews_and_evidence_pass=True',
 'retentions=6,metadata_revisions=0':'retentions=14,metadata_revisions=0',
 }
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 extra=""" assert len(context['all208_complete_original_voice_report_pairs'])==208
 for r in notes['records']:
  n=r['message_id'];expected=sorted({tuple(v[key])for v in context['all208_complete_original_voice_report_pairs']for key in('source_mode0_messages','source_mode1_messages')if n in v[key]})
  assert r['source_selected_complete_report_pairs']==[list(v)for v in expected]
 supplement=read(notes['fresh_ordinary_supplement']);term=Path(supplement['ordinary_sailor_crew_term_reference'])
 assert sha(term.read_bytes())==supplement['ordinary_sailor_crew_term_reference_sha256']and supplement['reference_exact_table_row']in term.read_text()
 assert history['no_inputs5773_through6922']and len(history['preserved1973_escape_holds_context_only_no_duplicate_credit'])==2
"""
 needle=' ROOT.mkdir(parents=True)';assert source.count(needle)==1;source=source.replace(needle,extra+needle)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
