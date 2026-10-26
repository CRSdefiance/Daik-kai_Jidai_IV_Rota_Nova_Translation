"""Independent eight-response audit:source intent,blank guards,history and release."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/verify_editorial_handoff_v2593.py').read_text()
 changes={'battle_victory':'declaration_responses','v2593':'v2611','V2593':'V2611','v2592':'v2610','V2592':'V2610','v2590':'v2608','v2591c':'v2609','native_plan_v1396':'native_plan_v1535b','range(2130,2138)':'range(2201,2209)','2054':'2077','1398':'1421',"'original-53D44-logical-role1-legacy-battle-victory-portrait'":"'original-53F0C-company-leader-NPC-war-response-portrait'"}
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 a="row['source_native_macros']==(['IC first-person plus plural tachi localized grammatically as we']if n==2132 else [])";assert a in source;source=source.replace(a,"row['source_native_macros']==[]and row['native_argument_count']==0 and '%'not in row['english']")
 a=source.index(' assert jp[2132]');b=source.index(' receiptpath=',a)
 source=source[:a]+""" assert notes['original_entry']==0x02053F0C and notes['original_parent']==0x02053F40 and notes['original_table_stack_offset']==0x274 and notes['original_source_table']==0x021184E0 and notes['original_company_leader_getter']==0x0203CD2C and notes['native_argument_count']==0
 context=read(notes['native_context_proof']);assert context['original_signed_eight_members']==IDS and len(context['all208_original_voice_selections'])==208 and context['actual_company_ID']==4 and context['actual_actor_ID']==28 and context['actual_source_voice']==4 and context['actual_message_ID']==2205 and context['CPU_prefix_stops_before_speech_hostility_setters_or_battle']and context['no_actor_ID_roster_RNG_hostility_or_result_changes']
 call=context['current_original6F024_leader_speech_prefix'];assert len(call)==1 and call[0]['arguments']==[context['actual_actor_object'],0x021184E0]
 for row in context['original_source_code']:assert sha(arm[row['start']:row['end']])==row['sha256']
 font=read('work/analysis/declaration_responses_fonts_v2608/native_font_proof.json');cases=font['cases'];assert len(cases)==font['complete_native_font_cases']==font['all8_original_direct_leader_pipelines']==8 and len(font['invalid_compiler_inputs_rejected'])==14 and len(font['all16_native_cold_warm_copies'])==16 and not font['findings']and font['all_original_actor_models_unchanged']and font['no_actor_or_roster_fixture']and font['blank_space_font_freshly_verified_zero_ink']
 assert[c['message_ID']for c in cases]==IDS and len(font['review_sheets'])==1
 for c in cases:
  n=c['message_ID'];native=c['native_pipeline'];assert c['source_voice']==n-2201 and native['input_hex']==entries[n].text.hex()and native['original_entry']==0x02053F0C and native['parent']==0x02053F40 and native['selector_offset']==0x274 and native['selector']==0x021184E0
  assert c['all_executed_pipeline_instructions_current_ROM_including_deployed_pool']and c['all_actor_models_unchanged_after_complete_pipeline']and c['current_historical_formatted_bytes_lines_font_events_and_blank_guards_equal']and c['full228x64_native_and_independent_font_exact']and c['complete_first_final_letters_uniform6px_margins_bounds_and_blank_paper_pass']and not c['findings']and not c['weak_line_end_indices']
  assert ' '.join(c['lines'])==entries[n].text.decode('ascii')and 1<=len(c['lines'])<=4 and all(0<len(v)<=35 for v in c['lines'])
  for index,line in enumerate(c['lines']):
   events=[e for e in c['complete_ordered_glyph_events']if e['y']==16*index and 6<=e['x']<6+6*len(line)];guards=[]
   while events and events[0]['code']==32 and events[0]['x']==6:guards.append(events.pop(0))
   assert len(guards)<=1 and(not guards or index>0)and guards==c['native_zero_ink_continuation_guards'][index]['zero_ink_guard_events']and[e['code']for e in events]==list(line.encode('ascii'))and[e['x']for e in events]==[6+6*i for i in range(len(line))]
 assert next(c for c in cases if c['message_ID']==2205)['existing_actor_ID']==28
 assert final['current_native_declaration_responses_font_executions']==8 and final['current_native_copies']==16 and final['historical_actual_holds']==2 and final['historical_declaration_response_battle_and_return_transitions_current_bound']==6
 history=read('work/analysis/declaration_responses_history_v2609/historical_declaration_responses_current_binding.json');assert history['historical_IDs']==[2205]and len(history['historical_holds'])==2 and history['only2205_has_individual_historical_activation_other7_use_family_sample']and history['no_new_current_battle_emulator_runs_or_family_visits']and history['no_fixtures_after4800']and history['all_accepted_input_events_reconstructed_at_pause_frame_plus1']
 assert all(c['source_company_ID']==4 and c['source_company_leader_getter']==0x0203CD2C and c['source_actor_ID']==28 and c['source_voice']==4 and c['matching_foreground_pixels']==815 for c in history['historical_holds'])and len(history['seven_negative_controls_current_binding_on_offline_clones'])==7 and all(c['rejected']for c in history['seven_negative_controls_current_binding_on_offline_clones'])
 states=history['natural_combat_outcome_and_original_dismissal_states'];assert len(states)==14 and states[-1]['frame']==9200 and states[-1]['mode']==[0,0,0]and len(states[-1]['fleets'][0]['ships'])==4
 flow=history['scoped_historical_cancellation_and_battle_transitions_freshly_rechecked'];assert[f['frame']for f in flow]==[6020,6150,6300,8800,9000,9200]and all(f['historical_only_not_current_startup_or_unreviewed_prose_credit']for f in flow)
 for row in history['source_combat_result_role_selection_and_RNG_current_historical_equal']:assert sha(arm[row['start']:row['end']])==row['sha256']
 pixelpath=Path(history['old_new_two_screen907_glyph_differences_and43_other_whole_frames_proof']);pixelproof=read(pixelpath);assert sha(pixelpath.read_bytes())==history['old_new_two_screen907_glyph_differences_and43_other_whole_frames_proof_sha256']and len(pixelproof['complete_actual2205_holds'])==2 and all(r['whole256x384_changed_pixels']==907 and r['every_changed_pixel_exact_old_new_native_glyph_symmetric_difference']for r in pixelproof['complete_actual2205_holds'])and len(pixelproof['all_other_sampled_whole_frames_exact_to_V1520'])==43
 previous=read('work/analysis/editorial_handoff_verification_v2605/verified_handoff.json');assert previous['ledger_sha256']==sha(Path('work/analysis/declaration_responses_completion_v2610/editorial_review_current_v1.json.before').read_bytes())
"""+source[b:]
 changes={"inv['remaining']==89":"inv['remaining']==66","'/COMMON/MESFILE.DK4':88":"'/COMMON/MESFILE.DK4':65",'remaining_historical_fresh_reviews=89':'remaining_historical_fresh_reviews=66',
 'all8_exact_clean_current_integrated_references_five_gates_registered_prose_and_IC_plural_binding_verified=True':'all8_exact_clean_current_integrated_references_five_gates_registered_prose_and_no_invented_argument_or_macro_verified=True',
 'all8_native_legacy_cells_ordered_glyphs_pair_blanks_ABI_and_actor_model_preservation_verified=True':'all8_native_visible_glyphs_literal_personal_I_narrow_zero_ink_guards_and_actor_model_preservation_verified=True',
 'historical_two_holds_six_corruptions_fourteen_states_nine_transitions_verified=True':'historical_two_holds_seven_corruptions_fourteen_states_six_transitions_verified=True',
 'all8_legacy_victory_reviews_fonts_IC_plural_and_historical_flow_pass=True':'all8_NPC_war_response_reviews_fonts_blank_guards_and_historical_flow_pass=True'}
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
