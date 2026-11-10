"""Use complete source/current inverses for539 speeches andthe unchanged control-only block68."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/rebuild_reviewed_editorial_batch_v4.py').read_text(encoding='utf-8'),{
    "len(doc['records'])==323":"len(doc['records'])==539",
    "==len(native['records'])==308":"==len(native['records'])==539",
    "==(260,48,15)":"==(539,0,0)",
    'block==128':'block==68',
    'unchanged_control_only_blocks=[128],speech_count=260':'unchanged_control_only_blocks=[68],speech_count=539',
    'style_physical_speech_count=48,total_rendered_speech_count=308,typed_choice_count=15,compound_objects=13':
        'style_physical_speech_count=0,total_rendered_speech_count=539,typed_choice_count=0,compound_objects=0',
    'B111-B130 complete source-bound reconstruction':'Rafael B61–B80 complete source-bound reconstruction',
    'ordinary_speeches=260,style_alternatives=48,menu_labels=15,changed_blocks=19':
        'ordinary_speeches=539,style_alternatives=0,menu_labels=0,changed_blocks=19',
})
exec(compile(source,__file__+'::same-complete-scene-inverses-Rafael539-with-control-only68','exec'),globals())
