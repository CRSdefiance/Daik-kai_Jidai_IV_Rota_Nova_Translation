"""Narrow legacy-layer adapter; allow only Fernando1987 metadata normalization."""
from pathlib import Path
OLD=Path('scripts/reconcile_contextual_mood_retentions_v2482.py')
source=OLD.read_text()
changes={
 "doc['speaker_metadata_corrections']==[]":"len(doc['speaker_metadata_corrections'])==1 and doc['speaker_metadata_corrections'][0]['message_id']==1987 and doc['speaker_metadata_corrections'][0]['source_actor_ID']==20 and doc['speaker_metadata_corrections'][0]['before']=='Ｆernando' and doc['speaker_metadata_corrections'][0]['after']=='Fernando'",
 "not r['speaker_metadata_corrected']":"r['speaker_metadata_corrected']==(r['message_id']==1987)",
 "fonts['current_parent_projection_controls']==1 and fonts['current_parent_projection_is_shared_ordinary_control_not_current_battle_GPU']":"fonts['current_parent_projection_controls']==0 and fonts['current_distinct_duel_208x36_native_canvas_and_three144x12_crops']",
 "config['manuscript_sha256']":"config['dependencies'][str(registeredpath)]",
 "stage['proof']['reviewed_native_IDs']":"stage['proof']['native_IDs']",
 "context['candidate_sha256']":"context['current_ROM_sha256']",
 "consumer='252x96 canvas,body y60;216x36 parent crop at screen16,112;registered generated36-column3row pair-safe paragraph'":"display_contract='Original numeric D4D0 side0/duration120 special;208x36 static-duel plane;24 cells x3 rows;three144x12 crops at x56,y212/232/252;single row at native y12;generated pair-phase completion before LF'",
 'speaker_metadata_corrections=[]':'speaker_metadata_corrections=doc["speaker_metadata_corrections"]',
 'speaker_metadata_corrections=0':'speaker_metadata_corrections=len(doc["speaker_metadata_corrections"])',
 'historical_mood_current_binding':'historical_duel_special_current_binding',
 'scoped_historical_battle_returns_freshly_rechecked':'scoped_historical_cancellation_and_battle_transitions_freshly_rechecked',
 'new_current_mood_ID_visits':'new_current_special_call_ID_visits',
 'current_shared_parent_is_ordinary_control_not_mood_gameplay=True':'current_Deck_or_shared_modal_projection_claim=False',
 'current_native_mood_font':'current_native_special_call_font',
 'mood0_4_5':'numeric_special_side0_24x3',
 'current_parent_draw_controls=1,current_parent_is_ordinary_shared_geometry_control=True':'current_parent_draw_controls=0,current_Deck_or_shared_modal_projection_claim=False',
 'historical_returns_current_rechecked':'historical_special_combat_and_victory_transitions_current_bound',
 'historical_returns_rechecked':'historical_special_combat_and_victory_transitions_bound',
 'Historical-only battle/return binding':'Historical-only special/combat/victory binding',
 'ordinary/battle numeric_special_side0_24x3 fonts':'original numeric side0 special-call fonts',
 'mood-fixtures-and-returns':'pre-duel-fixtures-special-and-victory',
 'retentions-original-216x36-crop':'retentions-original-special-duel-three144x12-crops',
}
for a,b in changes.items():
 assert a in source,a
 source=source.replace(a,b)
needle=' validate_natural_dialogue_batch(notes);'
assert needle in source
extra=""" assert fonts['complete_native_font_cases']==15 and len(fonts['focused_excluded_prior_numeric_and_escape_controls'])==6 and fonts['all15_original_D4D0_side0_duration120_source_contract_preserved']
 assert all(r['consumer']=='original-D4D0-static-duel-side0-duration120'for r in notes['records'])
 assert history['all_accepted_input_events_reconstructed_at_pause_frame_plus1']and history['no_inputs5773_through10982']and history['only1990_has_individual_actual_special_activation_other14_family_sample']
 assert len(context['all208_original_native_special_method_selections'])==208 and all(r['side']==0 and r['duration']==120 for r in context['all15_original_message_call_bindings'])
 assert next(r for r in notes['records']if r['message_id']==1987)['speaker']=='Fernando'
 notes.update(original_special_side=0,original_special_duration=120,source_families_not_sequential_conversation=True,metadata_normalization_changes_no_ROM_body_or_identity=True)
"""
source=source.replace(needle,extra+needle)
exec(compile(source,__file__,'exec'),globals())
