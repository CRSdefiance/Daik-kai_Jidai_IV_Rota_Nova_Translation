"""Save each remaining Lil decision with its exact clean and current references."""

import inspect
from pathlib import Path

from scripts import checkpoint_lil254_contextual_v1 as previous
from scripts.save_lil261_clean_part_v1 import ROOT
from scripts.source_locked_derivation_v5118 import checked_text


ARCHIVE = Path('translations/editorial_checkpoints/Lil261_clean_20261110_v1')
DECISIONS = [ARCHIVE / f'{scope}_comparisons.txt' for scope in ('B323_B324', 'B325_B331', 'B332_B335')]
RELEASE = Path('work/lil254_B312_B319_release_v1/registered_release_verification.json')


if __name__ == '__main__':
    source = checked_text(inspect.getsource(previous.comparisons), {
        'list(range(312, 320))': 'list(range(323, 336))',
        "len(roles['source_records']) == 160 and roles['source_selectors'] == [207, 208, 211, 214, 215, 218]":
            "len(roles['source_records']) == 125 and roles['source_selectors'] == [207, 208, 211, 214]",
        "len(names['records']) == 10 and names['original_native_name_getters'] == 20":
            "len(names['records']) == 9 and names['original_native_name_getters'] == 18",
        "len(objects['style_records']) == 158 and len(objects['choice_records']) == 8":
            "len(objects['style_records']) == 119 and len(objects['choice_records']) == 6",
        "len(objects['style_objects']) == 27 and objects['native_style_getter_cases'] == 216":
            "len(objects['style_objects']) == 18 and objects['native_style_getter_cases'] == 144",
        '== 254': '== 261',
        'all254_contextual_comparisons_v1.json': 'all261_contextual_comparisons_v1.json',
        'scoped_names_macros_reference_v1.json': 'scoped_names_macros_v2.json',
    })
    env = {**vars(previous), 'ROOT': ROOT, 'DECISIONS': DECISIONS, '__file__': __file__}
    exec(compile(source, __file__, 'exec'), env)
    path, counts = env['comparisons'](previous.load(RELEASE))
    print(path, dict(counts))
