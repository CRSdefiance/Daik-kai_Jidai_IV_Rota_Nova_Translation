"""Check Lil's three complete mixed-arity menus in the qualified native scope."""

import inspect
from pathlib import Path

from scripts import check_editorial_three_choice_explicit_route_v1 as three
from scripts import check_maria390_menus_v1 as previous
from scripts.check_editorial_compiled_pages_scope_reuse_v1 import qualified_current_native_context
from scripts.check_editorial_native_explicit_scope_v1 import two_choice
from scripts.source_locked_derivation_v5118 import checked_text


def three_choice():
    source = checked_text(three.source, {
        "    assert doc['current_ROM_sha256']==ctx.receipt()['candidate_sha256']":
            '    scope_reuse=qualified_current_native_context(doc,ctx)',
        'runtime=ctx.receipt(),': 'runtime=ctx.receipt(),native_context_reuse=scope_reuse,',
    })
    exec(compile(source, __file__, 'exec'),
         {'__file__': __file__, '__name__': '__main__', 'qualified_current_native_context': qualified_current_native_context})


def main():
    source = checked_text(inspect.getsource(previous.main), {
        'len(groups)==8 and sum(map(len,groups.values()))==17':
            'sorted(map(len,groups.values()))==[2,3,3]',
        "'/data/SC3.DK4'": "'/data/SC2.DK4'",
        "if count==2:sys.argv+=['--captain','3']": "sys.argv+=['--captain','2']",
        "runpy.run_module(module,run_name='__main__')": '(two_choice if count==2 else three_choice)()',
        'menus=8,captions=17,native_provider_alignments=48,bridged_modal_returns=150,':
            'menus=3,captions=8,native_provider_alignments=18,bridged_modal_returns=66,',
        'current_andtarget_normal_highlight_planes=68,target_normal_highlight_planes=34,':
            'current_andtarget_normal_highlight_planes=32,target_normal_highlight_planes=16,',
        'compiler_negatives=57,': 'compiler_negatives=23,',
        "Path('scripts/check_maria390_three_choice_v1.py')": "Path('scripts/check_editorial_three_choice_explicit_route_v1.py')",
        'PASS8 menus/17 captions/48 alignments/150 bridged returns/68 planes':
            'PASS 3 menus/8 captions/18 alignments/66 bridged returns/32 planes',
    })
    env = {**vars(previous), 'ROOT': Path('work/Lil254_B312_B319_clean_20261110'),
           'two_choice': two_choice, 'three_choice': three_choice, '__file__': __file__}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
