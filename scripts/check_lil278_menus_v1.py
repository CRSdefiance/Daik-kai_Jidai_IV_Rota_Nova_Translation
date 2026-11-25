"""Verify the three Lil two-choice menus using exact native scope reuse."""

import inspect
from pathlib import Path

from scripts import check_maria390_menus_v1 as previous
from scripts.check_editorial_native_explicit_scope_v1 import two_choice
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    source = checked_text(inspect.getsource(previous.main), {
        "'menu_native_v1'": "'menu_native_v2'",
        'len(groups)==8 and sum(map(len,groups.values()))==17': 'len(groups)==3 and sum(map(len,groups.values()))==6',
        'count in (2,3)': 'count==2',
        "'/data/SC3.DK4'": "'/data/SC2.DK4'",
        "if count==2:sys.argv+=['--captain','3']": "sys.argv+=['--captain','2']",
        "runpy.run_module(module,run_name='__main__')": 'two_choice()',
        'menus=8,captions=17,native_provider_alignments=48,bridged_modal_returns=150,':
            'menus=3,captions=6,native_provider_alignments=18,bridged_modal_returns=54,',
        'current_andtarget_normal_highlight_planes=68,target_normal_highlight_planes=34,':
            'current_andtarget_normal_highlight_planes=24,target_normal_highlight_planes=12,',
        'compiler_negatives=57,': 'compiler_negatives=21,',
        "Path('scripts/check_maria390_three_choice_v1.py')":
            "Path('scripts/check_editorial_native_explicit_scope_v1.py')",
        'PASS8 menus/17 captions/48 alignments/150 bridged returns/68 planes':
            'PASS 3 menus/6 captions/18 alignments/54 bridged returns/24 planes',
    })
    env = {**vars(previous), 'ROOT': Path('work/Lil278_B299_B311_clean_20261110'),
           'two_choice': two_choice, '__file__': __file__}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
