"""Store thirteen complete exchanges over the registered market fix with qualified native reuse."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.qualify_maria270_market_parent_v1 import qualify

ROOT=Path('work/Maria_B37_B50_clean_20261109')
assert load(ROOT/'offline270_display_approval_v2.json')['all272_selected_body_pages_directly_viewed']
source=checked_text(Path('scripts/rebuild_reviewed_editorial_batch_v4.py').read_text(encoding='utf-8'),{
    "len(doc['records'])==323":"len(doc['records'])==270",
    "doc['physical_speech_objects']==len(layout['records'])==len(native['records'])==308":
        "doc['physical_speech_objects']==len(layout['records'])==len(native['records'])==266",
    '(260,48,15)':'(266,0,4)',
    "image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==native['runtime']['candidate_sha256']":
        "image,qualified_parent=qualify(native['runtime']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==qualified_parent['target_candidate_sha256']\n    assert doc['exact_registered_market_parent_reuse']==qualified_parent",
    "assert sha(arm)==native['runtime']['ARM9_sha256'] and sha(archive)":
        "assert sha(arm)==qualified_parent['target_ARM9_sha256'] and sha(archive)",
    'word=0x2200,':"word=int.from_bytes(source[:2],'little'),",
    'else:assert block==128 and not records and not compound and current==clean':
        "else:raise AssertionError('Unexpected unchanged reviewed Maria270 block: '+str(block))",
    'len(changed)==19':'len(changed)==13',
    'unchanged_control_only_blocks=[128],speech_count=260,':'unchanged_control_only_blocks=[],speech_count=266,',
    'style_physical_speech_count=48,total_rendered_speech_count=308,typed_choice_count=15,compound_objects=13,':
        'style_physical_speech_count=0,total_rendered_speech_count=266,typed_choice_count=4,compound_objects=2,',
    'ordinary_speeches=260,style_alternatives=48,menu_labels=15,changed_blocks=19,':
        'ordinary_speeches=266,style_alternatives=0,menu_labels=4,changed_blocks=13,',
    'B111-B130 complete source-bound reconstruction':'Maria B37-B49 complete source-bound reconstruction on registered market-fix parent',
    "registered_right_bound_runtime_andprevious_name_fields_preserved=True,":
        "registered_right_bound_runtime_andprevious_name_fields_preserved=True, registered_market_format_fix_preserved=True, exact_registered_market_parent_reuse=qualified_parent,",
})
exec(compile(source,__file__+'::same-mixed-native-storage-guards-explicit270-scope-andregistered-market-parent','exec'),globals())
