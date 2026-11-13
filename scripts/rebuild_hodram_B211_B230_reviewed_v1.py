"""Source-locked complete reconstruction of the approved mixed-object Hodram batch."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.approve_hodram_B211_B230_display_v1 import VIEW
from scripts.source_locked_derivation_v5118 import checked_text

assert load(VIEW)['final_speech_pages_visually_approved']
source=checked_text(Path('scripts/rebuild_reviewed_editorial_batch_v4.py').read_text(encoding='utf-8'),{
    "len(doc['records'])==323":"len(doc['records'])==277",
    "len(native['records'])==308":"len(native['records'])==270",
    '(260,48,15)':'(241,29,7)',
    'word=0x2200,':"word=int.from_bytes(source[:2],'little'),",
    'block==128 and not records':'block==222 and not records',
    'unchanged_control_only_blocks=[128],speech_count=260,':'unchanged_control_only_blocks=[222],speech_count=241,',
    'style_physical_speech_count=48,total_rendered_speech_count=308,typed_choice_count=15,compound_objects=13,':
        'style_physical_speech_count=29,total_rendered_speech_count=270,typed_choice_count=7,compound_objects=7,',
    'ordinary_speeches=260,style_alternatives=48,menu_labels=15,':'ordinary_speeches=241,style_alternatives=29,menu_labels=7,',
    'B111-B130 complete source-bound reconstruction':'B211-B230 complete source-bound reconstruction',
})
exec(compile(source,__file__+'::source-locked-complete-scene-rebuilder','exec'),globals())
