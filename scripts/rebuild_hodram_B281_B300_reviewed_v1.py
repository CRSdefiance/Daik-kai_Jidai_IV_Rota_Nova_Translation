"""Rebuild the twenty source-bound reviewed blocks with unchanged native contracts."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.approve_hodram_B281_B300_display_v5 import VIEW
from scripts.source_locked_derivation_v5118 import checked_text

assert load(VIEW)['final_speech_pages_visually_approved']
source=checked_text(Path('scripts/rebuild_reviewed_editorial_batch_v4.py').read_text(encoding='utf-8'),{
    "len(doc['records'])==323":"len(doc['records'])==384",
    "doc['physical_speech_objects']==len(layout['records'])==len(native['records'])==308":"doc['physical_speech_objects']==len(layout['records'])==len(native['records'])==373",
    '(260,48,15)':'(242,131,11)',
    'word=0x2200,':"word=int.from_bytes(source[:2],'little'),",
    'else:assert block==128 and not records and not compound and current==clean':"else:raise AssertionError('Unexpected unchanged block in this qualified text scope: '+str(block))",
    'len(changed)==19':'len(changed)==20',
    'unchanged_control_only_blocks=[128],speech_count=260,':'unchanged_control_only_blocks=[],speech_count=242,',
    'style_physical_speech_count=48,total_rendered_speech_count=308,typed_choice_count=15,compound_objects=13,':'style_physical_speech_count=131,total_rendered_speech_count=373,typed_choice_count=11,compound_objects=23,',
    'ordinary_speeches=260,style_alternatives=48,menu_labels=15,changed_blocks=19,':'ordinary_speeches=242,style_alternatives=131,menu_labels=11,changed_blocks=20,',
    'B111-B130 complete source-bound reconstruction':'B281-B300 complete source-bound reconstruction',
})
exec(compile(source,__file__+'::same-complete-rebuilder-reviewed-twenty-block-scope','exec'),globals())
