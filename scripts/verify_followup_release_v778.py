"""Verify full inheritance,hard prose gates,native copies and clean-source patch."""

import inspect
from pathlib import Path

from dk4tool.patch import scheme_followup_editorial as owned
from scripts import verify_schemes_release_v776 as original
from scripts.prepare_followup_common_v778 import ROOT, MANUSCRIPT
from scripts.register_followup_release_v778 import CONFIG
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v778_candidate.nds')


def main():
    source = inspect.getsource(original.main)
    replacements = {
        "'out/all_routes_combined_v773_candidate.nds'": "'out/all_routes_combined_v776_candidate.nds'",
        "'all-routes-unified-v776'": "'all-routes-unified-v778'",
        "'release_stack_before_v776.json'": "'release_stack_before_v778.json'",
        "==956": "==978",
        "'all3612_other_strings_exact'": "'all3643_other_strings_exact'",
        "print('V776 complete inheritance,exact scoped contents,7336 copies,11 negative gates and clean-source patch pass. Actual scenes pending.',flush=True)":
            "print('V778 full inheritance,exact scoped contents,7336 copies,11 negative gates and exact clean patch pass. Actual scenes pending.',flush=True)",
    }
    for old, new in replacements.items():
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    effective = ROOT/'effective_release_verifier.py'
    effective.write_text(source, encoding='utf-8')
    env = {**original.__dict__, 'owned': owned, 'ROOT': ROOT, 'ROM': ROM, 'CONFIG': CONFIG,
           'MANUSCRIPT': MANUSCRIPT, '__file__': str(Path(__file__).resolve())}
    exec(compile(source, str(effective), 'exec'), env)
    env['main']()
    report = read(ROOT/'registered_verification.json')
    report['only_COMMON_ARM9_change_from_V776'] = report.pop('only_COMMON_ARM9_change_from_V773')
    save(ROOT/'registered_verification.json', report)


if __name__ == '__main__':
    main()
