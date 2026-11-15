"""Reconstruct the complete 352-speech/21-caption scope with mixed two/three-choice menus."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/rebuild_reviewed_editorial_batch_v4.py').read_text(encoding='utf-8'), {
    "len(doc['records'])==323": "len(doc['records'])==373",
    "len(native['records'])==308": "len(native['records'])==352",
    '(260,48,15)': '(352,0,21)',
    'word=0x2200,': "word=int.from_bytes(source[:2],'little'),",
    'len(changed)==19': 'len(changed)==20',
    'unchanged_control_only_blocks=[128],speech_count=260,': 'unchanged_control_only_blocks=[],speech_count=352,',
    'style_physical_speech_count=48,total_rendered_speech_count=308,typed_choice_count=15,compound_objects=13,':
        'style_physical_speech_count=0,total_rendered_speech_count=352,typed_choice_count=21,compound_objects=10,',
    'ordinary_speeches=260,style_alternatives=48,menu_labels=15,changed_blocks=19,':
        'ordinary_speeches=352,style_alternatives=0,menu_labels=21,changed_blocks=20,',
    'B111-B130 complete source-bound reconstruction': 'B191-B210 complete source-bound reconstruction',
})
exec(compile(source, __file__ + '::same-full-rebuilder-mixed-menu-counts-source-locked', 'exec'), globals())
