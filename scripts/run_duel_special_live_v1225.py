"""Cold original contact/duel with extended positive pre-duel HP;no forced move."""
import inspect
from pathlib import Path
from scripts import run_duel_bark_live_v1207 as previous
from scripts.native_duel_special_fixture_v1225 import ROM, apply_fixture


def main():
    source = inspect.getsource(previous.main)
    replacements = {
        'scripts/native_duel_bark_fixture_v1207.py': 'scripts/native_duel_special_fixture_v1225.py',
        'only_positive_health_ship_recovery_and_contact_before_duel': 'only_extended_positive_health_ship_recovery_and_contact_before_duel',
        'timed_reactions_require_ordinary_physical_button_inputs_after5902': 'original_special_requires_unmodified_native_eligibility_and_RNG_after5902',
        'Duel reaction replay terminal; source and disposable donors preserved.': 'Special-move replay terminal;source and disposable donors preserved.',
    }
    for old, new in replacements.items():
        assert source.count(old) >= 1
        source = source.replace(old, new)
    env = {**previous.__dict__, '__file__': __file__, 'ROM': ROM, 'apply_fixture': apply_fixture,
        'ROOT': Path('work/analysis/duel_special_live_v1225'),
        'CAP': Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_special_v1225_1224')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
