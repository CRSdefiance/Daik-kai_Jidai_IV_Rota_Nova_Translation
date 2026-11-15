"""Reconstruct the complete255-object scope,including both source-owned eight-slot objects."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/rebuild_reviewed_editorial_batch_v4.py').read_text(encoding='utf-8'),{
    "len(doc['records'])==323":"len(doc['records'])==255",
    "==len(native['records'])==308":"==len(native['records'])==243",
    "==(260,48,15)":"==(229,14,12)",
    'block==128':'block in [106,107]',
    'len(changed)==19':'len(changed)==18',
    'unchanged_control_only_blocks=[128],speech_count=260':'unchanged_control_only_blocks=[106,107],speech_count=229',
    'style_physical_speech_count=48,total_rendered_speech_count=308,typed_choice_count=15,compound_objects=13':
        'style_physical_speech_count=14,total_rendered_speech_count=243,typed_choice_count=12,compound_objects=6',
    'B111-B130 complete source-bound reconstruction':'Rafael B101-B120 complete255-object source-bound reconstruction',
    'ordinary_speeches=260,style_alternatives=48,menu_labels=15,changed_blocks=19':
        'ordinary_speeches=229,style_alternatives=14,menu_labels=12,changed_blocks=18',
})
exec(compile(source,__file__+'::same-complete-scene-inverses-Rafael255-andtwo-control-only-blocks', 'exec'),globals())
