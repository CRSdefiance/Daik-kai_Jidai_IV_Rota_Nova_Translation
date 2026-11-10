"""Rebuild39 complete residual SC1 blocks with the original mixed-object guards."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.source_locked_derivation_v5118 import checked_text

ROOT=Path('work/Hodram_B0_B41_clean_20261107')
assert load(ROOT/'offline_visual_approval_v1.json')['final_all389_pages_directly_viewed_or_exact_reused']
source=checked_text(Path('scripts/rebuild_reviewed_editorial_batch_v4.py').read_text(encoding='utf-8'),{
    "len(doc['records'])==323":"len(doc['records'])==394",
    "doc['physical_speech_objects']==len(layout['records'])==len(native['records'])==308":
        "doc['physical_speech_objects']==len(layout['records'])==len(native['records'])==388",
    '(260,48,15)':'(341,47,6)',
    "doc['current_ROM_sha256']==native['runtime']['candidate_sha256']":
        "doc['current_ROM_sha256']==doc['exact_existing_native_context_reuse']['target_candidate_sha256']",
    'word=0x2200,':"word=int.from_bytes(source[:2],'little'),",
    'else:assert block==128 and not records and not compound and current==clean':
        "else:raise AssertionError('Unexpected unchanged reviewed block: '+str(block))",
    'len(changed)==19':'len(changed)==39',
    'unchanged_control_only_blocks=[128],speech_count=260,':'unchanged_control_only_blocks=[],speech_count=341,',
    'style_physical_speech_count=48,total_rendered_speech_count=308,typed_choice_count=15,compound_objects=13,':
        'style_physical_speech_count=47,total_rendered_speech_count=388,typed_choice_count=6,compound_objects=10,',
    'ordinary_speeches=260,style_alternatives=48,menu_labels=15,changed_blocks=19,':
        'ordinary_speeches=341,style_alternatives=47,menu_labels=6,changed_blocks=39,',
    'B111-B130 complete source-bound reconstruction':'B0-B41 residual complete source-bound reconstruction',
})
exec(compile(source,__file__+'::same-complete-rebuilder-exact-current-scope-and39-blocks','exec'),globals())
