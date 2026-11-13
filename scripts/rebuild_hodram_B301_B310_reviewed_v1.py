"""Rebuild all ten reviewed blocks, including the B308 style-only exchange."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.approve_hodram_B301_B310_display_v6 import VIEW
from scripts.source_locked_derivation_v5118 import checked_text

assert load(VIEW)['final_speech_pages_visually_approved']
source=checked_text(Path('scripts/rebuild_reviewed_editorial_batch_v4.py').read_text(encoding='utf-8'),{
    "len(doc['records'])==323":"len(doc['records'])==234",
    "doc['physical_speech_objects']==len(layout['records'])==len(native['records'])==308":
        "doc['physical_speech_objects']==len(layout['records'])==len(native['records'])==225",
    '(260,48,15)':'(73,152,9)',
    'word=0x2200,':"word=int.from_bytes(source[:2],'little'),",
    'else:assert block==128 and not records and not compound and current==clean':
        "else:raise AssertionError('Unexpected unchanged block in this qualified text scope: '+str(block))",
    'len(changed)==19':'len(changed)==10',
    'unchanged_control_only_blocks=[128],speech_count=260,':'unchanged_control_only_blocks=[],speech_count=73,',
    'style_physical_speech_count=48,total_rendered_speech_count=308,typed_choice_count=15,compound_objects=13,':
        'style_physical_speech_count=152,total_rendered_speech_count=225,typed_choice_count=9,compound_objects=27,',
    'ordinary_speeches=260,style_alternatives=48,menu_labels=15,changed_blocks=19,':
        'ordinary_speeches=73,style_alternatives=152,menu_labels=9,changed_blocks=10,',
    'B111-B130 complete source-bound reconstruction':'B301-B310 complete source-bound reconstruction',
})
exec(compile(source,__file__+'::same-complete-rebuilder-ten-reviewed-block-scope','exec'),globals())
