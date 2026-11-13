"""Original duel with the ordinary pre-duel health prerequisite and timed A."""
import inspect
from pathlib import Path
from scripts import run_duel_bark_live_v1207 as previous
from scripts.native_duel_special_fixture_v1232 import ROM, apply_fixture


def main():
    source = inspect.getsource(previous.main)
    assert source.count('scripts/native_duel_bark_fixture_v1207.py') == 3
    source = source.replace('scripts/native_duel_bark_fixture_v1207.py', 'scripts/native_duel_special_fixture_v1232.py')
    source = source.replace('Duel reaction replay terminal;', 'Special observation with ordinary timed A terminal;')
    env = {**previous.__dict__, '__file__': __file__, 'ROM': ROM, 'apply_fixture': apply_fixture,
        'ROOT': Path('work/analysis/duel_special_live_v1232'),
        'CAP': Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_special_v1232_1224')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
