"""Final scoped audit of13 escape retentions,current labels and both release owners."""
from pathlib import Path
OLD=Path('scripts/verify_editorial_handoff_v2511c.py')
if __name__=='__main__':
 source=OLD.read_text()
 a=" packetpath=Path('work/analysis/escape_source_handoff_v2510/next13_direct_escape_source_packet.json');"
 start=source.index(a);end=source.index(" inv=read(",start)
 source=source[:start]+source[end:]
 changes={
 'editorial_handoff_verification_v2511c':'editorial_handoff_verification_v2519',
 'V2511c-audit-of-V2510':'V2519-audit-of-V2518',
 '1955':'1968','1299':'1312',
 'static_duel_contextual':'escape_contextual',
 'list(range(1931,1951))':'list(ESCAPE_IDS)',
 "final['retained_count']==20":"final['retained_count']==13",
 "{'original-duel-side0-actor-text':8,'original-duel-side1-actor-text':12}":"{'original-post-duel-companion-speech':13}",
 "final['current_native_static_duel_font_executions']==36":"final['current_native_direct_escape_expansion_font_cases']==1423 and final['unique_current_native_font_rasters']==1021",
 "final['current_native_copies']==40":"final['current_native_copies']==26",
 "final['historical_actual_holds']==6":"final['historical_actual_holds']==2",
 "final['historical_original_duel_terminal_transitions_current_bound']==1":"final['historical_defeat_and_title_transitions_current_bound']==4",
 "work/analysis/static_duel_history_v2505c/historical_static_duel_current_binding.json":"work/analysis/escape_history_v2516/historical_escape_current_binding.json",
 "history['actual_historical_challenge_name']=='Centurione'and'original_actor_IDs_1_32_and_conditional_Clifford_name_unchanged'not in history":"history['original_First_Mate_actor18_and_actual_captain1_unchanged'] and history['historical_IDs']==[1973]",
 'work/analysis/escape_source_handoff_v2510/handoff_receipt.json':'work/analysis/escape_completion_v2518/completion_receipt.json',
 "h['completed_this_goal_turn']==20 and h['fresh_integrated']==1968 and h['next_packet_records']==13 and h['next_packet_fresh_or_source_prose_credit']==0":"h['fresh_reconciliations']==13 and h['fresh_integrated']==1968",
 'work/analysis/static_duel_completion_v2506/remaining_historical_fresh_review_inventory.json':'work/analysis/escape_completion_v2518/remaining_historical_fresh_review_inventory.json',
 "inv['remaining']==188":"inv['remaining']==175",
 "'/COMMON/MESFILE.DK4':187":"'/COMMON/MESFILE.DK4':174",
 '# Current editorial handoff - V2510':'# Current editorial handoff - V2518',
 'completed_this_goal_turn=20,retained=20':'completed_this_goal_turn=13,retained=13',
 'all20_exact_clean_current_integrated_payloads_and_five_gates':'all13_exact_clean_current_integrated_payloads_and_five_gates',
 "next_corrected_direct_escape_packet=str(packetpath),next_packet_sha256=sha(packetpath.read_bytes()),next13_source_context_only_credit0_all_editorial_native_historical_reconciliation_pending=True,":"all13_fresh_source_current_native_and_historical_reconciliations_complete=True,",
 'remaining_historical_fresh_reviews=188':'remaining_historical_fresh_reviews=175',
 'all20_reviews_and_next13_source_packet_pass=True':'all13_escape_reviews_and_current_evidence_pass=True',
 'next13_credit=0':'new_justified_retentions=13',
 }
 for a,b in changes.items():
  assert a in source,a
  source=source.replace(a,b)
 assert 'packetpath'not in source
 needle=' ROOT.mkdir(parents=True)'
 extra=""" font=read('work/analysis/escape_font_review_v2517/native_font_proof.json');pipeline=read('work/analysis/escape_pipeline_v2514d/current_direct_pipeline.json')
 assert len(font['cases'])==1423 and font['unique_native_font_planes']==1021 and len(font['all162_exact_current_interjection_boundary_decisions'])==162
 assert len(pipeline['all13_current_direct_pipeline_cases'])==13 and pipeline['all_executed_section_code_matches_current_ROM']
 assert notes['corrected_direct_parent']==0x02053F40 and notes['corrected_direct_table_stack_offset']==0x274
 formatterpath=Path(notes['effective_direct_formatter_config']);formatter=read(formatterpath)
 assert sha(formatterpath.read_bytes())==notes['effective_direct_formatter_config_sha256']==manifest['relocations']['/__arm9__.bin']['escape_direct_formatting']['release_config_sha256']
 assert sha(Path(notes['effective_direct_manuscript']).read_bytes())==notes['effective_direct_manuscript_sha256']==formatter['dependencies'][notes['effective_direct_manuscript']]
"""
 assert source.count(needle)==1;source=source.replace(needle,extra+needle)
 compile(source,__file__,'exec')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
