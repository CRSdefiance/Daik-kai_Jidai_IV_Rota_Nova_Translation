"""Verify full integration inheritance,hard prose gates and exact clean patch."""

import inspect
from pathlib import Path

from dk4tool.patch import barmaid_editorial as owned
from scripts import verify_schemes_release_v776 as original
from scripts.prepare_barmaid_common_v780 import ROOT, MANUSCRIPT
from scripts.register_barmaid_release_v780 import CONFIG
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v780_candidate.nds')


def main():
    source = inspect.getsource(original.main)
    for old, new in {
        "'out/all_routes_combined_v773_candidate.nds'": "'out/all_routes_combined_v778_candidate.nds'",
        "'all-routes-unified-v776'": "'all-routes-unified-v780'",
        "'release_stack_before_v776.json'": "'release_stack_before_v780.json'",
        '==956': '==989', "'all3612_other_strings_exact'": "'all3637_other_strings_exact'",
        "print('V776 complete inheritance,exact scoped contents,7336 copies,11 negative gates and clean-source patch pass. Actual scenes pending.',flush=True)":
            "print('V780 full inheritance,7336 copies,11 hard gates and exact clean-input patch pass. Actual scenes pending.',flush=True)",
    }.items():
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    (ROOT/'effective_release_verifier.py').write_text(source, encoding='utf-8')
    env = {**original.__dict__, 'owned': owned, 'ROOT': ROOT, 'ROM': ROM, 'CONFIG': CONFIG,
           'MANUSCRIPT': MANUSCRIPT, '__file__': str(Path(__file__).resolve())}
    exec(compile(source, str(ROOT/'effective_release_verifier.py'), 'exec'), env)
    env['main']()
    report = read(ROOT/'registered_verification.json')
    report['only_COMMON_ARM9_change_from_V778'] = report.pop('only_COMMON_ARM9_change_from_V773')
    report['negative_gates']['reversed_barmaid_captain_name_order'] = report['negative_gates'].pop('reversed_town_faction_order')
    save(ROOT/'registered_verification.json', report)


if __name__ == '__main__':
    main()
