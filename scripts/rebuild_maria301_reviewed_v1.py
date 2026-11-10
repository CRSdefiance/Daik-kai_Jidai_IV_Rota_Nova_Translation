"""Store32 complete Maria SC3 exchanges with the unchanged mixed-object guards."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.source_locked_derivation_v5118 import checked_text

ROOT = Path('work/Maria_B0_B32_clean_20261109')
assert load(ROOT/'offline_display_approval_v1.json')['every_final_page_directly_viewed_in_readable_sheets']
source = checked_text(Path('scripts/rebuild_reviewed_editorial_batch_v4.py').read_text(encoding='utf-8'), {
    "len(doc['records'])==323": "len(doc['records'])==301",
    "doc['physical_speech_objects']==len(layout['records'])==len(native['records'])==308":
        "doc['physical_speech_objects']==len(layout['records'])==len(native['records'])==299",
    '(260,48,15)': '(292,7,2)',
    'word=0x2200,': "word=int.from_bytes(source[:2],'little'),",
    'else:assert block==128 and not records and not compound and current==clean':
        "else:raise AssertionError('Unexpected unchanged reviewed Maria block: '+str(block))",
    'len(changed)==19': 'len(changed)==32',
    'unchanged_control_only_blocks=[128],speech_count=260,': 'unchanged_control_only_blocks=[],speech_count=292,',
    'style_physical_speech_count=48,total_rendered_speech_count=308,typed_choice_count=15,compound_objects=13,':
        'style_physical_speech_count=7,total_rendered_speech_count=299,typed_choice_count=2,compound_objects=2,',
    'ordinary_speeches=260,style_alternatives=48,menu_labels=15,changed_blocks=19,':
        'ordinary_speeches=292,style_alternatives=7,menu_labels=2,changed_blocks=32,',
    'B111-B130 complete source-bound reconstruction': 'Maria B0-B32 complete source-bound reconstruction',
})
exec(compile(source, __file__+'::same-complete-rebuilder-explicit-Maria32-block-scope', 'exec'), globals())
