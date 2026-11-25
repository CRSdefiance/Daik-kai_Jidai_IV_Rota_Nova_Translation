"""Bind complete Lil role headers and run the scoped menu and alert checks."""

import argparse
import inspect

from scripts import check_maria390_menus_v1 as menus
from scripts import diagnose_maria363_FE_scope_v1 as alerts
from scripts import project_maria363_native_roles_v1 as roles
from scripts.check_editorial_native_explicit_scope_v1 import two_choice
from scripts.save_lil261_clean_part_v1 import ROOT
from scripts.source_locked_derivation_v5118 import checked_text


def roles_main():
    source = checked_text(inspect.getsource(roles.main), {
        "{'ordinary-speech':6,'4100-style-alternative':85}": "{'ordinary-speech':6,'4100-style-alternative':119}",
        'Bound6 ordinary and85 virtual-style controls': 'Bound 6 ordinary and 119 virtual-style controls',
    })
    env = {**vars(roles), 'ROOT': ROOT, '__file__': __file__}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()


def alerts_main():
    source = checked_text(inspect.getsource(alerts.main), {
        "ROOT/'plan_v6/automatic_plans.json'": "ROOT/'plan_v1/automatic_plans.json'",
        'captain=3': 'captain=2',
        'assert len(rows)==38': 'assert len(rows)==13',
    })
    env = {**vars(alerts), 'ROOT': ROOT, '__file__': __file__}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()


def menus_main():
    source = checked_text(inspect.getsource(menus.main), {
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
    env = {**vars(menus), 'ROOT': ROOT, 'two_choice': two_choice, '__file__': __file__}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=('roles', 'alerts', 'menus'))
    args = parser.parse_args()
    {'roles': roles_main, 'alerts': alerts_main, 'menus': menus_main}[args.stage]()
