"""Reconcile the20 static rows of a registered33-row distinct-consumer layer."""
from pathlib import Path
OLD=Path('scripts/reconcile_contextual_mood_retentions_v2482.py')
source=OLD.read_text()
changes={
 "fonts['current_parent_projection_controls']==1 and fonts['current_parent_projection_is_shared_ordinary_control_not_current_battle_GPU']":"fonts['current_parent_projection_controls']==0 and fonts['current_distinct_duel_208x36_native_canvas_and_three144x12_crops']",
 "stage['proof']['reviewed_native_IDs']==ids":"set(ids)<=set(stage['proof']['reviewed_native_IDs'])",
 "historical_changed_records=stage['proof']['changed_records'],new_revisions=0":"historical_changed_records=stage['proof']['changed_records'],registered_layer_native_IDs=stage['proof']['reviewed_native_IDs'],selected_static_native_IDs=ids,new_revisions=0",
 "consumer='252x96 canvas,body y60;216x36 parent crop at screen16,112;registered generated36-column3row pair-safe paragraph'":"display_contract='208x36 static-duel canvas;24 cells x3 rows;three144x12 original crops at screen x56,y212/232/252;single-row text starts at native y12;generated pair-phase completion before LF'",
 'historical_mood_current_binding':'historical_static_duel_current_binding',
 'scoped_historical_battle_returns_freshly_rechecked':'scoped_historical_cancellation_and_battle_transitions_freshly_rechecked',
 'new_current_mood_ID_visits':'new_current_static_duel_ID_visits',
 'current_shared_parent_is_ordinary_control_not_mood_gameplay=True':'current_Deck_or_shared_modal_projection_claim=False',
 'current_native_mood_font':'current_native_static_duel_font',
 'mood0_4_5':'static_duel24x3',
 'current_parent_draw_controls=1,current_parent_is_ordinary_shared_geometry_control=True':'current_parent_draw_controls=0,current_Deck_or_shared_modal_projection_claim=False',
 'historical_returns_current_rechecked':'historical_original_duel_terminal_transitions_current_bound',
 'historical_returns_rechecked':'historical_original_duel_terminal_transitions_bound',
 'Historical-only battle/return binding':'Historical-only original duel/return binding',
 'ordinary/battle static_duel24x3 fonts':'distinct static-duel fonts',
 'mood-fixtures-and-returns':'pre-duel-fixtures-original-combat-and-return',
 'font_previews=count':'font_previews=spec["font_executions"]',
 'retentions-original-216x36-crop':'retentions-original-static-duel-three144x12-crops',
}
for a,b in changes.items():
 assert a in source,a
 source=source.replace(a,b)
needle=' validate_natural_dialogue_batch(notes);'
assert needle in source
source=source.replace(needle," assert fonts['complete_native_font_cases']==36 and len(fonts['all53_current_scope_cases'])==53 and fonts['all1356_name_template_generated_layout_bindings_rechecked_without_repeating_unchanged_rasters'];assert all(r['consumer']in('original-duel-side0-actor-text','original-duel-side1-actor-text')for r in notes['records']);assert history['actual_historical_challenge_name']=='Centurione'\n"+needle)
exec(compile(source,__file__,'exec'),globals())
