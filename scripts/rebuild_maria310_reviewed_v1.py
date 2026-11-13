"""Reconstruct seven complete SC3 exchanges with all original inverses/allocation guards."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.source_locked_derivation_v5118 import checked_text
assert load('work/Maria_B51_B57_clean_20261109/offline_display_approval_v1.json')['all318_final_pages_directly_viewed_or_exact_visual_reuse']
source=checked_text(Path('scripts/rebuild_reviewed_editorial_batch_v4.py').read_text(encoding='utf-8'),{
    "len(doc['records'])==323":"len(doc['records'])==310",
    "doc['physical_speech_objects']==len(layout['records'])==len(native['records'])==308":
        "doc['physical_speech_objects']==len(layout['records'])==len(native['records'])==310",
    '(260,48,15)':'(310,0,0)',
    'else:assert block==128 and not records and not compound and current==clean':
        "else:raise AssertionError('Unexpected unchanged reviewed Maria310 block: '+str(block))",
    'len(changed)==19':'len(changed)==7',
    'unchanged_control_only_blocks=[128],speech_count=260,':'unchanged_control_only_blocks=[],speech_count=310,',
    'style_physical_speech_count=48,total_rendered_speech_count=308,typed_choice_count=15,compound_objects=13,':
        'style_physical_speech_count=0,total_rendered_speech_count=310,typed_choice_count=0,compound_objects=0,',
    'ordinary_speeches=260,style_alternatives=48,menu_labels=15,changed_blocks=19,':
        'ordinary_speeches=310,style_alternatives=0,menu_labels=0,changed_blocks=7,',
    'B111-B130 complete source-bound reconstruction':'Maria B51-B57 complete source-bound reconstruction',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-whole-block-archive-NDS-inverses-andallocation310','exec'),globals())
