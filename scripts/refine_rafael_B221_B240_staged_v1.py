"""Refresh only the two staged closings whose phrasal verbs split in the first pass."""
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text

parent = Path(__file__).with_name('check_rafael_B221_B240_staged_v1.py')
source = checked_text(parent.read_text(encoding='utf-8'), {
    "OUT = ROOT / 'staged_native_v1'": "OUT = ROOT / 'staged_native_delta_v1'",
    "    for lines in wrap_options(row['localized_letter_close'], source_y // 16):":
        """    lines_by_id = {
        'DK4_MES_B226_R0068': ('If I hear anything else,', 'I will write again.'),
        'DK4_MES_B235_R0048': ('If it interests you,', 'why not look into it?'),
    }
    for lines in [lines_by_id[row['id']]]:""",
    "        ident, prefix = row['id'], row['source_selector']":
        """        ident, prefix = row['id'], row['source_selector']
        if ident not in {'DK4_MES_B226_R0068', 'DK4_MES_B235_R0048'}:
            continue""",
    'assert len(records) == 4': 'assert len(records) == 2',
    '(912, 320)': '(912, 160)',
    'all_four_staged_pages.png': 'two_refined_staged_pages.png',
    'pages=4': 'pages=2',
    "(STAGED, n['SOURCE'], n['MACROS'], Path(__file__))": "(STAGED, n['SOURCE'], n['MACROS'], parent, Path(__file__))",
})
if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-staging-and-renderer-with-two-coherent-closings', 'exec'), globals())

