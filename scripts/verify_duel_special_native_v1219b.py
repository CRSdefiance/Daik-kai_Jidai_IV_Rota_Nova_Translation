"""Successor: excluded escape calls retain their original leading guard byte.

V1219's15 special and36 preserved fonts passed; its escape exclusion comparison
incorrectly used prose instead of the stored source consumer input. Do not
strip the guard or change the escape renderer to satisfy that comparison.
"""
import inspect
from pathlib import Path
from dk4tool.patch.duel_bark_editorial import current_entries
from scripts import verify_duel_special_native_v1219 as previous


def main():
    rom = previous.NdsImage.open(previous.SOURCE)
    before = current_entries(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'))
    source = inspect.getsource(previous.main)
    old = "table, n, old[n]['english'].encode('ascii')))"
    assert source.count(old) == 1
    source = source.replace(old, 'table, n, before[n].text))')
    env = {**previous.__dict__, '__file__': __file__, 'before': before,
           'ROOT': Path('work/analysis/duel_special_native_v1219b')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
