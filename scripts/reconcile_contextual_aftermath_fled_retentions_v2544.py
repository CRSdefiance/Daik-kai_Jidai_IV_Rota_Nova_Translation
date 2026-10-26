"""Reconcile a six-record subset of the registered75 aftermath layer."""
from pathlib import Path
OLD=Path('scripts/reconcile_contextual_mood_retentions_v2482.py');source=OLD.read_text()
changes={
 "fonts['current_parent_projection_controls']==1 and fonts['current_parent_projection_is_shared_ordinary_control_not_current_battle_GPU']":"fonts['current_parent_projection_controls']==0 and fonts['current_portrait_consumer_no_Deck_or_duel_projection_claim']",
 "config['manuscript_sha256']":"config['dependencies'][str(registeredpath)]",
 "stage['proof']['reviewed_native_IDs']==ids":"set(ids)<=set(stage['proof']['native_IDs'])",
 "historical_changed_records=stage['proof']['changed_records'],new_revisions=0":"historical_changed_records=stage['proof']['changed_records'],registered_layer_native_IDs=stage['proof']['native_IDs'],selected_contextual_native_IDs=ids,new_revisions=0",
 "context['candidate_sha256']":"context['current_ROM_sha256']",
 "consumer='252x96 canvas,body y60;216x36 parent crop at screen16,112;registered generated36-column3row pair-safe paragraph'":"display_contract='Original53D44 role1 speech;parent02053DB8/table stack+27C;228x64 portrait body,35 cells x4 rows,16px row stride,uniform native x6 at screen16,296;compiler-owned presentation guard and generated pair-safe post-macro wrapping'",
 'historical_mood_current_binding':'historical_aftermath_fled_current_binding',
 'scoped_historical_battle_returns_freshly_rechecked':'scoped_historical_cancellation_and_battle_transitions_freshly_rechecked',
 'new_current_mood_ID_visits':'new_current_aftermath_fled_ID_visits',
 'current_shared_parent_is_ordinary_control_not_mood_gameplay=True':'current_Deck_or_duel_projection_claim=False',
 'current_native_mood_font':'current_native_aftermath_fled_font',
 'mood0_4_5':'aftermath_fled_role1_35x4',
 'current_parent_draw_controls=1,current_parent_is_ordinary_shared_geometry_control=True':'current_parent_draw_controls=0,current_Deck_or_duel_projection_claim=False',
 'historical_returns_current_rechecked':'historical_report_and_sailing_return_transitions_current_bound',
 'historical_returns_rechecked':'historical_report_and_sailing_return_transitions_bound',
 'Historical-only battle/return binding':'Historical-only flight-report/dismissal binding',
 'ordinary/battle aftermath_fled_role1_35x4 fonts':'original role1 portrait-speech fonts',
 'mood-fixtures-and-returns':'pre-duel-fixtures-flight-report-and-sailing-return',
 'retentions-original-216x36-crop':'retentions-original-role1-228x64-portrait',
}
for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
needle=' validate_natural_dialogue_batch(notes);'
extra=""" assert fonts['complete_native_font_cases']==6 and len(fonts['all6_original_role1_pipelines'])==6 and fonts['all_executed_pipeline_instructions_current_ROM_byte_exact']and not fonts['findings']
 assert all(r['consumer']=='original-53D44-role1-fled-victory-portrait'for r in notes['records'])
 assert history['only2046_has_individual_historical_activation_other5_use_family_sample']and history['all_accepted_input_events_reconstructed_at_pause_frame_plus1']and history['no_inputs5773_through10982']
 notes.update(original_role_selector=1,original_parent=0x02053DB8,original_table_stack_offset=0x27C,original_source_table=0x02117900,source_voice_alternatives_not_sequential_conversation=True)
"""
assert needle in source;source=source.replace(needle,extra+needle)
exec(compile(source,__file__,'exec'),globals())
