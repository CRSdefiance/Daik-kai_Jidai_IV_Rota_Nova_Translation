"""Scoped final audit of16 timed reactions and their legacy registered layer."""
from pathlib import Path
OLD=Path('scripts/verify_editorial_handoff_v2511c.py')
if __name__=='__main__':
 source=OLD.read_text()
 start=source.index(" packetpath=Path('work/analysis/escape_source_handoff_v2510/next13_direct_escape_source_packet.json');")
 end=source.index(' inv=read(',start);source=source[:start]+source[end:]
 changes={
 'from scripts.duel_editorial_layout_v1155 import compiled,ESCAPE_IDS':'from scripts.duel_bark_layout_v1200 import compiled',
 'editorial_handoff_verification_v2511c':'editorial_handoff_verification_v2528','V2511c-audit-of-V2510':'V2528-audit-of-V2527',
 '1955':'1984','1299':'1328','static_duel_contextual':'duel_reaction_contextual','list(range(1931,1951))':'list(range(1957,1973))',
 "final['retained_count']==20":"final['retained_count']==16",
 "{'original-duel-side0-actor-text':8,'original-duel-side1-actor-text':12}":"{'original-duel-D458-side0-timed-action-feedback':16}",
 "final['current_native_static_duel_font_executions']==36":"final['current_native_timed_reaction_font_executions']==16",
 "final['current_native_copies']==40":"final['current_native_copies']==32",
 "final['historical_actual_holds']==6":"final['historical_actual_holds']==4",
 "final['historical_original_duel_terminal_transitions_current_bound']==1":"final['historical_defeat_and_title_transitions_current_bound']==4",
 'work/analysis/static_duel_history_v2505c/historical_static_duel_current_binding.json':'work/analysis/duel_reaction_history_v2526/historical_duel_reaction_current_binding.json',
 "history['actual_historical_challenge_name']=='Centurione'and'original_actor_IDs_1_32_and_conditional_Clifford_name_unchanged'not in history":"history['all_accepted_input_events_reconstructed_at_pause_frame_plus1']and history['two_rejected_gap_commands_apply_no_input']and history['historical_IDs']==[1958,1966]",
 'work/analysis/escape_source_handoff_v2510/handoff_receipt.json':'work/analysis/duel_reaction_completion_v2527/completion_receipt.json',
 "h['completed_this_goal_turn']==20 and h['fresh_integrated']==1984 and h['next_packet_records']==13 and h['next_packet_fresh_or_source_prose_credit']==0":"h['fresh_reconciliations']==16 and h['fresh_integrated']==1984",
 'work/analysis/static_duel_completion_v2506/remaining_historical_fresh_review_inventory.json':'work/analysis/duel_reaction_completion_v2527/remaining_historical_fresh_review_inventory.json',
 "inv['remaining']==188":"inv['remaining']==159","'/COMMON/MESFILE.DK4':187":"'/COMMON/MESFILE.DK4':158",
 '# Current editorial handoff - V2510':'# Current editorial handoff - V2527',
 'completed_this_goal_turn=20,retained=20':'completed_this_goal_turn=16,retained=16',
 'all20_exact_clean_current_integrated_payloads_and_five_gates':'all16_exact_clean_current_integrated_payloads_and_five_gates',
 'next_corrected_direct_escape_packet=str(packetpath),next_packet_sha256=sha(packetpath.read_bytes()),next13_source_context_only_credit0_all_editorial_native_historical_reconciliation_pending=True,':'all16_timed_reaction_reconciliations_complete=True,',
 'remaining_historical_fresh_reviews=188':'remaining_historical_fresh_reviews=159',
 'all20_reviews_and_next13_source_packet_pass=True':'all16_timed_reaction_reviews_and_evidence_pass=True','next13_credit=0':'new_justified_retentions=16',
 }
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 assert 'packetpath'not in source
 needle=' ROOT.mkdir(parents=True)'
 extra=""" font=read('work/analysis/duel_reaction_fonts_v2525/native_font_proof.json');assert font['complete_native_font_cases']==16 and len(font['all32_current_selected_and_direct_exclusion_scope_cases'])==32
 assert notes['original_timed_side']==0 and notes['original_timed_duration']==60 and all(r['source_speaker_side']==0 for r in history['historical_holds'])
 stage=manifest['relocations']['/COMMON/MESFILE.DK4']['duel_bark_editorial'];configpath=Path(stage['release_config']);config=read(configpath)
 assert stage['proof']['native_IDs']==list(range(1957,1973))and sha(configpath.read_bytes())==stage['release_config_sha256']
 assert sha(Path(config['manuscript']).read_bytes())==config['dependencies'][config['manuscript']]
"""
 assert source.count(needle)==1;source=source.replace(needle,extra+needle)
 compile(source,__file__,'exec')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
