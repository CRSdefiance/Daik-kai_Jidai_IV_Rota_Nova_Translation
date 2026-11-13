"""Scoped final six-report audit using frozen special-call audit structure."""
from pathlib import Path
OLD=Path('scripts/verify_editorial_handoff_v2537.py')
if __name__=='__main__':
 source=OLD.read_text()
 start=source.index(" corrections=notes['speaker_metadata_corrections'];")
 end=source.index(" assert final['current_native_special_call_font_executions']",start)
 source=source[:start]+" corrections=notes['speaker_metadata_corrections'];assert corrections==final['speaker_metadata_corrections']==[]\n"+source[end:]
 changes={
 'from scripts.duel_special_layout_v1216 import compiled,IDS':'from scripts.battle_aftermath_native_plan_v1255 import compiled\nIDS=tuple(range(2046,2052))',
 'editorial_handoff_verification_v2537':'editorial_handoff_verification_v2545','V2537-audit-of-V2536':'V2545-audit-of-V2544',
 '1999':'2005','1343':'1349','duel_special_contextual':'aftermath_fled_contextual',
 "final['retained_count']==15":"final['retained_count']==6",
 "r['speaker_metadata_corrected']==(n==1987)":"not r['speaker_metadata_corrected']",
 "{'original-D4D0-static-duel-side0-duration120':15}":"{'original-53D44-role1-fled-victory-portrait':6}",
 "final['current_native_special_call_font_executions']==15":"final['current_native_aftermath_fled_font_executions']==6",
 "final['current_native_copies']==30":"final['current_native_copies']==12",
 "final['historical_actual_holds']==6":"final['historical_actual_holds']==2",
 "final['historical_special_combat_and_victory_transitions_current_bound']==4":"final['historical_report_and_sailing_return_transitions_current_bound']==2",
 'work/analysis/duel_special_fonts_v2534/native_font_proof.json':'work/analysis/aftermath_fled_fonts_v2542b/native_font_proof.json',
 "font['complete_native_font_cases']==15":"font['complete_native_font_cases']==6",
 "font['focused_excluded_prior_numeric_and_escape_controls']":"font['all6_original_role1_pipelines']",
 "font['all15_original_D4D0_side0_duration120_source_contract_preserved']":"font['all_executed_pipeline_instructions_current_ROM_byte_exact']and not font['findings']",
 'work/analysis/duel_special_history_v2535/historical_duel_special_current_binding.json':'work/analysis/aftermath_fled_history_v2543/historical_aftermath_fled_current_binding.json',
 "history['historical_IDs']==[1990]":"history['historical_IDs']==[2046]",
 "history['only1990_has_individual_actual_special_activation_other14_family_sample']":"history['only2046_has_individual_historical_activation_other5_use_family_sample']",
 "notes['original_special_side']==0 and notes['original_special_duration']==120 and all(r['source_speaker_side']==0 and r['duration']==120 for r in history['historical_holds'])":"notes['original_role_selector']==1 and notes['original_parent']==0x02053DB8 and notes['original_table_stack_offset']==0x27C and all(r['source_role_selector']==1 for r in history['historical_holds'])",
 "context['all208_original_native_special_method_selections']":"context['all208_original_voice_selections']",
 "len(context['all15_original_message_call_bindings'])==15":"len(context['original_three_outcome_prefixes'])==3",
 "['duel_special_editorial']":"['battle_aftermath_editorial']",
 "stage['proof']['native_IDs']==list(IDS)and len(stage['proof']['changed_records'])==15":"set(IDS)<=set(stage['proof']['native_IDs'])and len(stage['proof']['native_IDs'])==len(stage['proof']['changed_records'])==75",
 'work/analysis/duel_special_completion_v2536/completion_receipt.json':'work/analysis/aftermath_fled_completion_v2544/completion_receipt.json',
 "h['fresh_reconciliations']==15":"h['fresh_reconciliations']==6",
 "h['speaker_metadata_corrections']==1":"h['speaker_metadata_corrections']==0",
 'work/analysis/duel_special_completion_v2536/remaining_historical_fresh_review_inventory.json':'work/analysis/aftermath_fled_completion_v2544/remaining_historical_fresh_review_inventory.json',
 "inv['remaining']==144":"inv['remaining']==138","'/COMMON/MESFILE.DK4':143":"'/COMMON/MESFILE.DK4':137",
 '# Current editorial handoff - V2536':'# Current editorial handoff - V2544',
 'completed_this_goal_turn=15,retained=15':'completed_this_goal_turn=6,retained=6',
 'all15_exact_clean_current_integrated_references_payloads_and_five_gates':'all6_exact_clean_current_integrated_references_payloads_and_five_gates',
 'remaining_historical_fresh_reviews=144':'remaining_historical_fresh_reviews=138',
 'all15_special_reviews_and_evidence_pass=True':'all6_flight_victory_reviews_and_evidence_pass=True',
 'retentions=15,Fernando_metadata_normalizations=1':'retentions=6,metadata_revisions=0',
 }
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
