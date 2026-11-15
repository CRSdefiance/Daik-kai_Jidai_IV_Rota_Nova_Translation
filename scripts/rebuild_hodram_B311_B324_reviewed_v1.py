"""Rebuild fourteen complete reviewed blocks through the qualified mixed-object rebuilder."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.prepare_hodram_B311_B324_storage_v1 import VIEW
from scripts.source_locked_derivation_v5118 import checked_text

assert load(VIEW)['final_all389_pages_directly_viewed_or_exact_reused']
source = checked_text(Path('scripts/rebuild_reviewed_editorial_batch_v4.py').read_text(encoding='utf-8'), {
    "len(doc['records'])==323": "len(doc['records'])==400",
    "doc['physical_speech_objects']==len(layout['records'])==len(native['records'])==308":
        "doc['physical_speech_objects']==len(layout['records'])==len(native['records'])==387",
    '(260,48,15)': '(151,236,13)',
    'word=0x2200,': "word=int.from_bytes(source[:2],'little'),",
    'else:assert block==128 and not records and not compound and current==clean':
        "else:raise AssertionError('Unexpected unchanged block in this qualified text scope: '+str(block))",
    'len(changed)==19': 'len(changed)==14',
    'unchanged_control_only_blocks=[128],speech_count=260,': 'unchanged_control_only_blocks=[],speech_count=151,',
    'style_physical_speech_count=48,total_rendered_speech_count=308,typed_choice_count=15,compound_objects=13,':
        'style_physical_speech_count=236,total_rendered_speech_count=387,typed_choice_count=13,compound_objects=44,',
    'ordinary_speeches=260,style_alternatives=48,menu_labels=15,changed_blocks=19,':
        'ordinary_speeches=151,style_alternatives=236,menu_labels=13,changed_blocks=14,',
    'B111-B130 complete source-bound reconstruction': 'B311-B324 complete source-bound reconstruction',
})
exec(compile(source, __file__+'::same-complete-rebuilder-fourteen-reviewed-block-scope', 'exec'), globals())
