"""Materialize exact557 scope with unchanged full relocation/inverse guards and FU."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

TEMPLATE=Path('scripts/rebuild_reviewed_editorial_batch_v4.py')
source=checked_text(TEMPLATE.read_text(encoding='utf-8'),{
    'from dk4tool.script.reviewed_scene_rebuild_v3 import rebuild_block':'from dk4tool.script.reviewed_scene_rebuild_with_fu_andcompounds_v1 import rebuild_block',
    "len(doc['records'])==323":"len(doc['records'])==557",
    "==len(native['records'])==308":"==len(native['records'])==549",
    '==(260,48,15)':'==(549,0,8)',
    'word=0x2200,':'word=0x2100,',
    'else:assert block==128 and not records and not compound and current==clean':"else:raise AssertionError(('Expected every reviewed source block to change',block))",
    'len(changed)==19':'len(changed)==20',
    'unchanged_control_only_blocks=[128],speech_count=260':'unchanged_control_only_blocks=[],speech_count=549',
    'style_physical_speech_count=48,total_rendered_speech_count=308,typed_choice_count=15,compound_objects=13':
        'style_physical_speech_count=0,total_rendered_speech_count=549,typed_choice_count=8,compound_objects=4',
    'B111-B130 complete source-bound reconstruction':'Rafael B141-B160 complete557-object source-bound reconstruction',
    'ordinary_speeches=260,style_alternatives=48,menu_labels=15,changed_blocks=19':
        'ordinary_speeches=549,style_alternatives=0,menu_labels=8,changed_blocks=20',
    "[Path(__file__),Path('dk4tool/script/reviewed_scene_rebuild.py')":
        "[TEMPLATE,Path(__file__),Path('dk4tool/script/reviewed_scene_rebuild_with_fu_andcompounds_v1.py'),Path('dk4tool/script/reviewed_scene_rebuild.py')",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-full-rebuild-557-scope-and-FU','exec'),globals())
