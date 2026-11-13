"""Mixed-consumer successor preserving the compiler's required consumer enum."""
from pathlib import Path
OLD=Path('scripts/reconcile_contextual_mood_retentions_v2482.py')
source=OLD.read_text()
changes={
 "consumer='252x96 canvas,body y60;216x36 parent crop at screen16,112;registered generated36-column3row pair-safe paragraph'":"display_contract=('228x64 modal canvas;16px row stride;native generated x6 indent;screen origin16,296'if r['consumer']=='assignment-refusal-modal'else'252x96 canvas,body y60;216x36 parent crop at screen16,112;registered generated36-column3row pair-safe paragraph')",
 'historical_mood_current_binding':'historical_activity_special_current_binding',
 'new_current_mood_ID_visits':'new_current_activity_special_ID_visits',
 'current_shared_parent_is_ordinary_control_not_mood_gameplay':'current_shared_parent_is_ordinary_Deck_geometry_control_only',
 'current_native_mood_font':'current_native_mixed_consumer_font',
 'mood0_4_5':'activity_special_mixed_consumer',
 'ordinary/battle mood0_4_5 fonts':'mixed Deck/modal fonts',
 'ordinary/battle activity_special_mixed_consumer fonts':'mixed Deck/modal fonts',
 'mood-fixtures-and-returns':'activity-special-fixtures-and-returns',
 }
for a,b in changes.items():
 if a in source:source=source.replace(a,b)
assert "consumer='252x96"not in source
needle=' validate_natural_dialogue_batch(notes);'
assert needle in source
source=source.replace(needle," assert Counter(r['consumer']for r in notes['records'])=={'Deck-CabinInfoView':14,'assignment-refusal-modal':3};assert fonts['complete_native_font_cases']==23 and fonts['complete_Deck_native_font_cases']==20 and fonts['complete_modal_native_font_cases']==3\n"+needle)
exec(compile(source,__file__,'exec'),globals())
