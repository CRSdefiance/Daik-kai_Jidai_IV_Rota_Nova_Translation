"""Recheck the user's sales-pitch formatting in V780 without changing the ROM."""

import inspect
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import verify_user_formatting_v776 as original
from scripts.verify_village_wrap_v608 import read, save


if __name__ == '__main__':
    source = inspect.getsource(original.main)
    assert 'v776' in source and 'V776' in source
    source = source.replace('v776', 'v780').replace('V776', 'V780')
    env = {**original.__dict__, '__file__': str(Path(__file__).resolve())}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
    path = Path('work/analysis/dialogue_formatting_user_recheck_v780/COMMON676_677.json')
    report = read(path)
    report['source_producer_sha256'] = sha(Path(original.__file__).read_bytes())
    report['effective_program_sha256'] = sha(source.encode())
    save(path, report)
