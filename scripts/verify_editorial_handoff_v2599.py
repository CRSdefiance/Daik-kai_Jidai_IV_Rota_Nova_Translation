"""Independent eight-report audit with208 name cases and source-selected speaker."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/verify_editorial_handoff_v2593.py').read_text()
 changes={'battle_victory':'enemy_capture','v2593':'v2599','V2593':'V2599','v2592':'v2598','V2592':'V2598','v2590':'v2596','v2591c':'v2597b','native_plan_v1396':'native_plan_v1423','range(2130,2138)':'range(2082,2090)','2054':'2062','1398':'1406',"'original-53D44-logical-role1-legacy-battle-victory-portrait'":"'original-53F0C-attacker-selector8-named-enemy-ship-capture-portrait'"}
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 a="row['source_native_macros']==(['IC first-person plus plural tachi localized grammatically as we']if n==2132 else [])"
 assert a in source;source=source.replace(a,"row['source_native_macros']==[]and row['native_argument_count']==1 and row['english'].count('%s')==1 and j.text.count(b'%s')==1")
 a=source.index(' assert jp[2132]');b=source.index(' receiptpath=',a)
 source=source[:a]+""" assert notes['original_entry']==0x02053F0C and notes['original_parent']==0x02053F40 and notes['original_table_stack_offset']==0x274 and notes['original_source_table']==0x02117B00 and notes['original_attacker_selector']==0x02055DC4 and notes['original_attacker_selector_argument']==8 and notes['native_ship_name_arguments']==1
 context=read(notes['native_context_proof']);assert len(context['all208_original_voice_selections'])==208 and context['actual_actor_ID']==18 and context['actual_source_voice']==0 and context['target_Hull_Crew']==[30,0]and context['target_name']=='Hanse Cog'and context['CPU_prefix_stops_before_speech_or_outcomes']and context['no_actor_ID_roster_name_or_result_changes']
 for row in context['original_source_code']:assert sha(arm[row['start']:row['end']])==row['sha256']
 call=context['current_original7402C_posteligibility_prefix'];assert len(call)==1 and call[0]['arguments']==[context['actual_actor_object'],0x02117B00,context['target_name_pointer']]
 font=read('work/analysis/enemy_capture_fonts_v2596/native_font_proof.json');cases=font['cases'];assert len(cases)==font['complete_native_font_cases']==font['all208_original_direct_named_capture_pipelines']==208 and len(font['invalid_compiler_inputs_rejected'])==15 and len(font['all16_native_cold_warm_copies'])==16 and not font['findings']and font['no_actor_or_roster_fixture']and font['all_original_actor_models_unchanged']
 assert[r['message_ID']for r in font['all8_complete_native_cases']]==IDS and len(font['review_sheets'])==8 and sum(bool(c['preview'])for c in cases)==64
 variants={}
 for c in cases:
  n=c['message_ID'];native=c['native_pipeline'];name=bytes.fromhex(c['name_hex']);value=entries[n].text;variants.setdefault(n,[]).append(c['variant'])
  assert native['input_hex']==value.replace(b'%s',name).hex()and native['original_entry']==0x02053F0C and native['parent']==0x02053F40 and native['selector_offset']==0x274 and native['selector']==0x02117B00
  assert c['all_executed_pipeline_instructions_current_ROM_including_deployed_pool']and c['all_actor_models_unchanged_after_complete_pipeline']and c['current_historical_formatted_bytes_lines_full_font_and_glyph_events_equal']and c['full228x64_native_and_independent_font_exact']and c['all_name_bytes_complete_leading_trailing_glyphs_uniform6px_margin_bounds_and_blank_paper_pass']and not c['findings']and not c['weak_line_end_indices']
  assert ' '.join(c['lines'])==value.replace(b'%s',name).decode('cp932')and 1<=len(c['lines'])<=4 and all(len(v.encode('cp932'))<=35 for v in c['lines'])and 1<=len(name)<=18
  if len(c['lines'])>1 and len(c['lines'][-1].split())==1:assert c['complete_atomic_runtime_ship_name_on_final_row']and c['atomic_name_review_reason']
 assert set(variants)==set(IDS)and all(v==list(range(26))for v in variants.values())
 assert final['current_native_enemy_capture_font_executions']==208 and final['current_native_copies']==16 and final['historical_actual_holds']==2 and final['historical_named_capture_flagship_victory_rewards_cargo_and_sailing_transitions_current_bound']==10
 history=read('work/analysis/enemy_capture_history_v2597b/historical_enemy_capture_current_binding.json');assert history['historical_IDs']==[2082]and len(history['historical_holds'])==2 and history['only2082_has_individual_historical_activation_other7_use_family_sample']and history['no_new_current_battle_emulator_runs_or_family_visits']and history['no_fixtures_after4800']and history['all_accepted_input_events_reconstructed_at_pause_frame_plus1']
 assert all(c['source_actor_ID']==18 and c['matching_foreground_pixels']==437 and c['target_name']=='Hanse Cog'and c['target_Hull_Crew']==[30,0]for c in history['historical_holds'])and len(history['seven_negative_controls_current_binding_on_offline_clones'])==7 and all(c['rejected']for c in history['seven_negative_controls_current_binding_on_offline_clones'])
 states=history['natural_combat_outcome_and_original_dismissal_states'];assert len(states)==15 and states[-1]['frame']==13200 and states[-1]['mode']==[0,0,0]
 flow=history['scoped_historical_cancellation_and_battle_transitions_freshly_rechecked'];assert[f['frame']for f in flow]==[10780,10850,11000,11200,11400,11600,12400,12700,12900,13200]and 'discard' in flow[7]['visually_reviewed_state']and 'blink' in flow[1]['visually_reviewed_state']
 for row in history['source_combat_result_role_selection_and_RNG_current_historical_equal']:assert sha(arm[row['start']:row['end']])==row['sha256']
"""+source[b:]
 changes={"['font_previews']==8":"['font_previews']==64","inv['remaining']==89":"inv['remaining']==81","'/COMMON/MESFILE.DK4':88":"'/COMMON/MESFILE.DK4':80",'remaining_historical_fresh_reviews=89':'remaining_historical_fresh_reviews=81',
 'all8_exact_clean_current_integrated_references_five_gates_registered_prose_and_IC_plural_binding_verified=True':'all8_exact_clean_current_integrated_references_five_gates_registered_prose_and_one_runtime_name_verified=True',
 'all8_native_legacy_cells_ordered_glyphs_pair_blanks_ABI_and_actor_model_preservation_verified=True':'all208_native_literal_name_wrap_fonts_events_and_actor_model_preservation_verified=True',
 'historical_two_holds_six_corruptions_fourteen_states_nine_transitions_verified=True':'historical_two_holds_seven_corruptions_fifteen_states_ten_transitions_verified=True',
 'all8_legacy_victory_reviews_fonts_IC_plural_and_historical_flow_pass=True':'all8_named_capture_reviews_208_name_fonts_and_historical_flow_pass=True'}
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
