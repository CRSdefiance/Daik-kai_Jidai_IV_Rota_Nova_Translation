"""Source-locked complete SC1 reconstruction, excluding completed B237."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.approve_hodram_B231_B250_display_v2 import VIEW
from scripts.source_locked_derivation_v5118 import checked_text

assert load(VIEW)['final_speech_pages_visually_approved']
source=checked_text(Path('scripts/rebuild_reviewed_editorial_batch_v4.py').read_text(encoding='utf-8'),{
    "len(doc['records'])==323":"len(doc['records'])==225",
    "doc['physical_speech_objects']==len(layout['records'])==len(native['records'])==308":
        "doc['physical_speech_objects']==len(layout['records'])==len(native['records'])==223",
    '(260,48,15)':'(209,14,2)',
    'word=0x2200,':"word=int.from_bytes(source[:2],'little'),",
    'block==128 and not records':'block==235 and not records',
    'len(changed)==19':'len(changed)==18',
    'unchanged_control_only_blocks=[128],speech_count=260,':'unchanged_control_only_blocks=[235],speech_count=209,',
    'style_physical_speech_count=48,total_rendered_speech_count=308,typed_choice_count=15,compound_objects=13,':
        'style_physical_speech_count=14,total_rendered_speech_count=223,typed_choice_count=2,compound_objects=3,',
    'ordinary_speeches=260,style_alternatives=48,menu_labels=15,changed_blocks=19,':
        'ordinary_speeches=209,style_alternatives=14,menu_labels=2,changed_blocks=18,',
    'B111-B130 complete source-bound reconstruction':'B231-B250 complete source-bound reconstruction excluding credited B237',
})
exec(compile(source,__file__+'::same-complete-rebuilder-new-exact-scope','exec'),globals())
