"""Seal the first six clean-only exchanges in the next Rafael intake."""
import inspect
from pathlib import Path

from scripts import seal_rafael_B261_B264_clean_v1 as earlier
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path('work/Rafael_B281_B300_clean_20261106')
OUTPUT = ROOT/'B281_B286_clean_drafts_v1.json'
PACKET = ROOT/'clean_source_packet.json'
STYLES = ROOT/'clean_style_objects.json'
MENUS = ROOT/'clean_choice_objects.json'
DRAFT = Path('translations/rafael_B281_B286_clean_drafts_v1.txt')
BLOCKS = list(range(281, 287))

source = checked_text(inspect.getsource(earlier.main), {
    "len(rows) == 57 and sum(row.get('kind') == 'actor-style-alternative' for row in rows) == 16":
        "len(rows) == 32 and not any(row.get('kind') == 'actor-style-alternative' for row in rows)",
    "sum(row.get('kind') == 'typed-choice-label' for row in rows) == 5":
        "not any(row.get('kind') == 'typed-choice-label' for row in rows)",
    'records_count=57, ordinary_speeches=36, style_alternatives=16':
        'records_count=32, ordinary_speeches=32, style_alternatives=0',
    'typed_captions=5': 'typed_captions=0',
    'Sealed 57 clean-source drafts across four complete Rafael exchanges.':
        'Sealed 32 clean-source drafts across six complete Rafael exchanges.',
})

if __name__ == '__main__':
    env = {**vars(earlier), **globals()}
    exec(compile(source, __file__ + '::clean-first-six-exchanges', 'exec'), env)
    env['main']()
