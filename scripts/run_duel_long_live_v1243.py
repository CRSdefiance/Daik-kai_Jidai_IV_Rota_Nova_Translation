"""Original long duel with declared native-range health/luck prerequisites."""
import inspect
from pathlib import Path
from scripts import run_duel_long_live_v1240 as previous
from scripts.native_duel_long_fixture_v1242 import ROM,apply_fixture


def main():
    source=inspect.getsource(previous.main)
    old='scripts/native_duel_long_fixture_v1239.py'
    assert source.count(old)==1
    source=source.replace(old,'scripts/native_duel_long_fixture_v1242.py')
    source=source.replace("'duel_long_live_v1240'","'duel_long_live_v1243'")
    source=source.replace('work/analysis/duel_long_live_v1240','work/analysis/duel_long_live_v1243')
    source=source.replace('duel_long_v1240_1224','duel_long_v1243_1224')
    source=source.replace('special_requires_unmodified_native_luck_eligibility_and_RNG_after5902',
        'special_uses_disclosed_pre_duel_luck100_original_eligibility_and_unmodified_RNG')
    env={**previous.__dict__,'__file__':__file__,'ROM':ROM,'apply_fixture':apply_fixture}
    exec(compile(source,__file__,'exec'),env);env['main']()


if __name__=='__main__':main()
