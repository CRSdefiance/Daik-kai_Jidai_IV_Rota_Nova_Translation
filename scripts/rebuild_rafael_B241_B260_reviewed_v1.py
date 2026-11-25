"""Rebuild the final Rafael B241–B260 dialogue in a research image."""
from pathlib import Path

from scripts.assemble_rafael_B241_B260_offline_v2 import FINAL_NATIVE, OUT, ROOT
from scripts.rebuild_rafael_B221_B240_reviewed_v1 import REGISTRY, TEMPLATE, source as previous
from scripts.source_locked_derivation_v5118 import checked_text


CURRENT = ROOT / 'current_effective.json/current_effective.json'
VISUAL = OUT / 'visual_review.json'
source = checked_text(previous, {
    "len(doc['records'])==270": "len(doc['records'])==292",
    "==len(native['records'])==263": "==len(native['records'])==286",
    '==(234,29,7)': '==(272,14,6)',
    'block==231': 'block==244',
    'len(changed)==19': 'len(changed)==18',
    'unchanged_control_only_blocks=[231],speech_count=234': 'unchanged_control_only_blocks=[244],speech_count=272',
    'style_physical_speech_count=29,total_rendered_speech_count=263,typed_choice_count=7,compound_objects=7':
        'style_physical_speech_count=14,total_rendered_speech_count=286,typed_choice_count=6,compound_objects=5',
    'ordinary_speeches=234,style_alternatives=29,menu_labels=7,changed_blocks=19':
        'ordinary_speeches=272,style_alternatives=14,menu_labels=6,changed_blocks=18',
    'Rafael B221–B240 complete source-bound reconstruction': 'Rafael B241–B260 complete source-bound reconstruction',
    "==(279,7,3)": "==(294,6,2)",
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::same-reviewed-rebuild-with-exact-292-object-scope', 'exec'), globals())
