"""Cold original long duel with disclosed low fencing before combat only."""
import inspect
from pathlib import Path
from scripts import run_duel_bark_live_v1207 as previous
from scripts.native_duel_long_fixture_v1239 import ROM,apply_fixture


def main():
    source=inspect.getsource(previous.main)
    old='scripts/native_duel_bark_fixture_v1207.py'
    assert source.count(old)==2
    source=source.replace(old,'scripts/native_duel_long_fixture_v1239.py')
    old="commands += [{'until':5782,'duration':1},{'until':5902,'duration':1}]"
    assert source.count(old)==1
    source=source.replace(old,old+"\n    commands += [{'until':n,'duration':1} for n in range(5942,11003,40)]")
    source=source.replace('only_positive_health_ship_recovery_and_contact_before_duel',
        'disclosed_low_fencing_health_and_equipment_prerequisite_before_duel')
    source=source.replace('timed_reactions_require_ordinary_physical_button_inputs_after5902',
        'special_requires_unmodified_native_luck_eligibility_and_RNG_after5902')
    source=source.replace('Duel reaction replay terminal;','Long original duel terminal;')
    env={**previous.__dict__,'__file__':__file__,'ROM':ROM,'apply_fixture':apply_fixture,
        'ROOT':Path('work/analysis/duel_long_live_v1240'),
        'CAP':Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_long_v1240_1224')}
    exec(compile(source,__file__,'exec'),env);env['main']()


if __name__=='__main__':main()
