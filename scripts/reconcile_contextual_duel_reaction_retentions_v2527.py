"""Current side0 timed reactions using this legacy layer's registered schema."""
from pathlib import Path
OLD=Path('scripts/reconcile_contextual_mood_retentions_v2482.py')
source=OLD.read_text()
changes={
 "fonts['current_parent_projection_controls']==1 and fonts['current_parent_projection_is_shared_ordinary_control_not_current_battle_GPU']":"fonts['current_parent_projection_controls']==0 and fonts['current_distinct_duel_208x36_native_canvas_and_three144x12_crops']",
 "config['manuscript_sha256']":"config['dependencies'][str(registeredpath)]",
 "stage['proof']['reviewed_native_IDs']":"stage['proof']['native_IDs']",
 "consumer='252x96 canvas,body y60;216x36 parent crop at screen16,112;registered generated36-column3row pair-safe paragraph'":"display_contract='Original D458 side0/duration60 timed response;208x36 static-duel plane;24 cells x3 rows;three144x12 crops at x56,y212/232/252;single row at native y12;generated pair-phase completion before LF'",
 'historical_mood_current_binding':'historical_duel_reaction_current_binding',
 'scoped_historical_battle_returns_freshly_rechecked':'scoped_historical_cancellation_and_battle_transitions_freshly_rechecked',
 'new_current_mood_ID_visits':'new_current_timed_reaction_ID_visits',
 'current_shared_parent_is_ordinary_control_not_mood_gameplay=True':'current_Deck_or_shared_modal_projection_claim=False',
 'current_native_mood_font':'current_native_timed_reaction_font',
 'mood0_4_5':'timed_duel_side0_24x3',
 'current_parent_draw_controls=1,current_parent_is_ordinary_shared_geometry_control=True':'current_parent_draw_controls=0,current_Deck_or_shared_modal_projection_claim=False',
 'historical_returns_current_rechecked':'historical_defeat_and_title_transitions_current_bound',
 'historical_returns_rechecked':'historical_defeat_and_title_transitions_bound',
 'Historical-only battle/return binding':'Historical-only timed-action/defeat/title binding',
 'ordinary/battle timed_duel_side0_24x3 fonts':'original side0 timed-duel fonts',
 'mood-fixtures-and-returns':'pre-duel-fixtures-timed-inputs-and-title',
 'retentions-original-216x36-crop':'retentions-original-timed-duel-three144x12-crops',
}
for a,b in changes.items():
 assert a in source,a
 source=source.replace(a,b)
needle=' validate_natural_dialogue_batch(notes);'
assert needle in source
extra=""" assert fonts['complete_native_font_cases']==16 and len(fonts['all32_current_selected_and_direct_exclusion_scope_cases'])==32 and fonts['all16_original_side0_duration60_source_contract_preserved']
 assert all(r['consumer']=='original-duel-D458-side0-timed-action-feedback'for r in notes['records'])
 assert history['all_accepted_input_events_reconstructed_at_pause_frame_plus1']and history['two_rejected_gap_commands_apply_no_input']
 notes.update(original_timed_side=0,original_timed_duration=60,source_families_not_sequential_conversation=True)
"""
source=source.replace(needle,extra+needle)
exec(compile(source,__file__,'exec'),globals())
