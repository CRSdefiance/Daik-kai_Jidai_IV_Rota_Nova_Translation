"""Materialize B131–B150's checked ordinary, eight-style and two-choice objects."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/rebuild_reviewed_editorial_batch_v4.py').read_text(encoding='utf-8'), {
    "len(doc['records'])==323": "len(doc['records'])==329",
    "len(native['records'])==308": "len(native['records'])==319",
    '(260,48,15)': '(311,8,10)',
    'word=0x2200,': 'word=0x2100,',
    'speech_count=260,': 'speech_count=311,',
    'style_physical_speech_count=48,total_rendered_speech_count=308,typed_choice_count=15,compound_objects=13,':
    'style_physical_speech_count=8,total_rendered_speech_count=319,typed_choice_count=10,compound_objects=6,',
    'unchanged_control_only_blocks=[128]': 'unchanged_control_only_blocks=[]',
    'ordinary_speeches=260,style_alternatives=48,menu_labels=15,': 'ordinary_speeches=311,style_alternatives=8,menu_labels=10,',
    'B111-B130 complete source-bound reconstruction': 'B131-B150 complete source-bound reconstruction',
})
exec(compile(source, __file__ + '::same-complete-scene-rebuilder-new-exact-scope', 'exec'), globals())
