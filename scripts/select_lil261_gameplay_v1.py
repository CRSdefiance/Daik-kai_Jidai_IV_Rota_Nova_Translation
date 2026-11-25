"""Select the remaining Lil batch's distinct display and transition behaviors."""

import inspect

from scripts import select_lil278_gameplay_v1 as previous
from scripts.save_lil261_clean_part_v1 import ROOT
from scripts.source_locked_derivation_v5118 import checked_text


SAMPLE = {
    323: ('S520', 'M674', 'R0104', 'S754', 'M934', 'R0144', 'R0173', 'R0212',
          'R0241', 'R0245', 'R0252', 'R0256'),
    324: ('R0093', 'M758', 'R0116', 'R0127', 'R0141', 'R0176', 'S1708', 'R0205', 'R0215'),
    325: ('R0044', 'R0065', 'R0074', 'R0078'),
    326: ('R0013', 'R0017', 'R0028'),
    327: ('R0005', 'R0008', 'R0025', 'R0031'),
    328: ('R0040',),
    329: ('R0012', 'R0038', 'R0049'),
    330: ('R0023', 'R0031', 'R0058', 'R0083', 'R0106', 'R0112'),
    331: ('R0008', 'R0024', 'R0028'),
    332: ('R0006', 'R0014'),
    333: ('S8', 'R0071', 'R0076', 'R0083'),
    334: ('R0010', 'R0013'),
    335: ('R0013', 'R0064', 'R0076', 'R0086', 'R0089', 'R0132', 'R0139', 'R0156'),
}


if __name__ == '__main__':
    source = checked_text(inspect.getsource(previous.main), {
        'Lil278_expedition_spices_temple': 'Lil261_fog_cave_commission_alchemy',
        'all_eight_FE_texts_selected=True': 'all_thirteen_FE_texts_selected=True',
    })
    env = {**vars(previous), 'ROOT': ROOT, 'SAMPLE': SAMPLE, '__file__': __file__}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
