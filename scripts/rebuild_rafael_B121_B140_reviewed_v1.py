"""Apply the unchanged full inverse rebuild to the exact351-object/two-control-block scope."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

TEMPLATE=Path('scripts/rebuild_reviewed_editorial_batch_v4.py')
source=checked_text(TEMPLATE.read_text(encoding='utf-8'),{
    "len(doc['records'])==323":"len(doc['records'])==351",
    "==len(native['records'])==308":"==len(native['records'])==341",
    "==(260,48,15)":"==(307,34,10)",
    'word=0x2200,':'word=0x2100,',
    'block==128':'block in [130,131]',
    'len(changed)==19':'len(changed)==18',
    'unchanged_control_only_blocks=[128],speech_count=260':'unchanged_control_only_blocks=[130,131],speech_count=307',
    'style_physical_speech_count=48,total_rendered_speech_count=308,typed_choice_count=15,compound_objects=13':
        'style_physical_speech_count=34,total_rendered_speech_count=341,typed_choice_count=10,compound_objects=11',
    'B111-B130 complete source-bound reconstruction':'Rafael B121-B140 complete351-object source-bound reconstruction',
    'ordinary_speeches=260,style_alternatives=48,menu_labels=15,changed_blocks=19':
        'ordinary_speeches=307,style_alternatives=34,menu_labels=10,changed_blocks=18',
    '[Path(__file__),Path(\'dk4tool/script/reviewed_scene_rebuild.py\')':
        '[TEMPLATE,Path(__file__),Path(\'dk4tool/script/reviewed_scene_rebuild.py\')',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-controls-inverses-new351-scope','exec'),globals())
