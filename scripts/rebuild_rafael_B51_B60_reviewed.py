"""Use complete source/current inverses for245 speeches andtwo native choice objects."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/rebuild_reviewed_editorial_batch_v4.py').read_text(encoding='utf-8'),{
    "len(doc['records'])==323":"len(doc['records'])==249",
    "==len(native['records'])==308":"==len(native['records'])==245",
    "==(260,48,15)":"==(245,0,4)",
    'word=0x2200,':'word=0x2100,',
    'else:assert block==128 and not records and not compound and current==clean':
        "else:raise AssertionError('Every complete B51–B60 block is expected to change')",
    'len(changed)==19':'len(changed)==10',
    'unchanged_control_only_blocks=[128],speech_count=260':'unchanged_control_only_blocks=[],speech_count=245',
    'style_physical_speech_count=48,total_rendered_speech_count=308,typed_choice_count=15,compound_objects=13':
        'style_physical_speech_count=0,total_rendered_speech_count=245,typed_choice_count=4,compound_objects=2',
    'B111-B130 complete source-bound reconstruction':'Rafael B51–B60 complete source-bound reconstruction',
    'ordinary_speeches=260,style_alternatives=48,menu_labels=15,changed_blocks=19':
        'ordinary_speeches=245,style_alternatives=0,menu_labels=4,changed_blocks=10',
})
exec(compile(source,__file__+'::same-complete-scene-inverses-Rafael-mixed-scope','exec'),globals())
