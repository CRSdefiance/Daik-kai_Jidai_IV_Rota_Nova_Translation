"""Modal confirmation successor;keeps consumers and records transition scope precisely."""
from pathlib import Path
OLD=Path('scripts/reconcile_contextual_mood_retentions_v2482.py')
source=OLD.read_text()
changes={
 "fonts['current_parent_projection_controls']==1 and fonts['current_parent_projection_is_shared_ordinary_control_not_current_battle_GPU']":"fonts['current_parent_projection_controls']==0 and fonts['current_modal_font_consumers_no_Deck_parent_projection_claim']",
 "consumer='252x96 canvas,body y60;216x36 parent crop at screen16,112;registered generated36-column3row pair-safe paragraph'":"display_contract='228x64 native speech modal;35 columns,at most4 rows,16px stride;generated x6 indent and screen origin16,296;source expansion before wrapping'",
 'historical_mood_current_binding':'historical_battle_declaration_current_binding',
 'scoped_historical_battle_returns_freshly_rechecked':'scoped_historical_cancellation_and_battle_transitions_freshly_rechecked',
 'new_current_mood_ID_visits':'new_current_declaration_ID_visits',
 'current_shared_parent_is_ordinary_control_not_mood_gameplay=True':'current_Deck_parent_projection_claim=False',
 'current_native_mood_font':'current_native_modal_font',
 'mood0_4_5':'declaration_modal',
 'current_parent_draw_controls=1,current_parent_is_ordinary_shared_geometry_control=True':'current_parent_draw_controls=0,current_Deck_parent_projection_claim=False',
 'historical_returns_current_rechecked':'historical_cancellation_and_battle_transitions_current_rechecked',
 'historical_returns_rechecked':'historical_transitions_rechecked',
 'historical-only battle/return binding':'historical-only cancellation/battle-transition binding',
 'Historical-only battle/return binding':'Historical-only cancellation/battle-transition binding',
 'ordinary/battle declaration_modal fonts':'modal announcement/confirmation fonts',
 'mood-fixtures-and-returns':'declaration-fixtures-and-transitions',
 'font_previews=count':'font_previews=spec["font_executions"]',
 'retentions-original-216x36-crop':'retentions-original-228x64-modal',
 }
for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
needle=' validate_natural_dialogue_batch(notes);'
assert needle in source
source=source.replace(needle," formatting=read(spec['formatting_review']);assert len(formatting['all27_exact_current_case_decisions'])==27 and formatting['blocking_errors']==formatting['unwaived_warnings']==0 and formatting['all176_complete_native_previews_freshly_viewed'];assert fonts['complete_native_font_cases']==176\n for r in notes['records']:\n  r['current_case_bound_layout_decisions']=[w for w in formatting['all27_exact_current_case_decisions']if w['message_ID']==r['message_id']]\n  assert r['consumer']in('native-speech-announcement','native-speech-confirmation')\n"+needle)
exec(compile(source,__file__,'exec'),globals())
