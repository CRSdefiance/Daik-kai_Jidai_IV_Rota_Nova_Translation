"""Preserve all source/current controls across255 speeches,six choices andfive control-only blocks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/rebuild_reviewed_editorial_batch_v4.py').read_text(encoding='utf-8'), {
    "len(doc['records'])==323": "len(doc['records'])==261",
    "==len(native['records'])==308": "==len(native['records'])==255",
    "==(260,48,15)": "==(255,0,6)",
    'word=0x2200,': 'word=0x2100,',
    'block==128': 'block in [89,94,96,98,99]',
    'len(changed)==19': 'len(changed)==11',
    'unchanged_control_only_blocks=[128],speech_count=260': 'unchanged_control_only_blocks=[89,94,96,98,99],speech_count=255',
    'style_physical_speech_count=48,total_rendered_speech_count=308,typed_choice_count=15,compound_objects=13':
        'style_physical_speech_count=0,total_rendered_speech_count=255,typed_choice_count=6,compound_objects=3',
    'B111-B130 complete source-bound reconstruction': 'Rafael B85-B100 complete source-bound reconstruction',
    'ordinary_speeches=260,style_alternatives=48,menu_labels=15,changed_blocks=19':
        'ordinary_speeches=255,style_alternatives=0,menu_labels=6,changed_blocks=11',
})
exec(compile(source, __file__+'::same-complete-scene-inverses-Rafael261-andfive-control-only-blocks', 'exec'), globals())
