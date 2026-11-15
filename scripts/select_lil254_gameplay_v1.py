"""Select the Lil display behaviors that need an ordinary-input emulator test."""

import inspect
from pathlib import Path

from scripts import select_lil278_gameplay_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path('work/Lil254_B312_B319_clean_20261110')
SAMPLE = {
    312: ('R0089', 'R0094', 'R0098', 'M754', 'R0117', 'R0140', 'R0175', 'R0282',
          'R0299', 'R0302', 'R0306'),
    313: ('R0009', 'R0013', 'R0016'),
    314: ('R0069', 'M684', 'S722', 'R0109', 'R0121', 'R0145'),
    315: ('R0010', 'R0013', 'R0016'),
    316: ('R0069', 'S562', 'R0097', 'M812', 'R0116', 'R0166', 'S1434', 'R0205', 'R0213',
          'S2354', 'R0291', 'R0330', 'R0334', 'R0384', 'R0391', 'R0410'),
    317: ('R0006', 'R0010', 'R0014', 'R0030', 'R0039', 'R0043'),
    318: ('R0010', 'R0014', 'R0026'),
    319: ('R0005', 'R0008', 'R0011', 'R0018', 'R0086', 'R0097', 'R0100', 'R0115'),
}
CHOICES = {(312, 754): (3, 2), (314, 684): (2, 1), (316, 812): (3, 1)}


if __name__ == '__main__':
    source = checked_text(inspect.getsource(previous.main), {
        "                    assert menus[block, offset]['caption_count'] == 2 and units":
            "                    count, target = CHOICES[block, offset]\n"
            "                    assert menus[block, offset]['caption_count'] == count and units",
        "                    extra.append(dict(start=opening + 60, duration=16, buttons=['DOWN']))":
            "                    for move in range(1, target + 1):\n"
            "                        extra.append(dict(start=opening + 60 * move, duration=16, buttons=['DOWN']))",
        'expected_cursor_index=1': 'expected_cursor_index=target',
        'Lil278_expedition_spices_temple': 'Lil254_wolf_ruins_trade',
        'all_eight_FE_texts_selected=True, all_three_two_choice_menus_selected=True':
            'all_seven_FE_texts_selected=True, both_menu_arities_selected=True',
    })
    env = {**vars(previous), 'ROOT': ROOT, 'SAMPLE': SAMPLE, 'CHOICES': CHOICES, '__file__': __file__}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
