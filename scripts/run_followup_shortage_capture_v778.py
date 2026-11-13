"""Exact named town-condition adapter with the declared two-byte shortage fixture."""

import inspect
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import run_town_condition_capture_v774 as original
from scripts.verify_village_wrap_v608 import read, save


if __name__ == '__main__':
    source = inspect.getsource(original.main)
    assert source.count('native_town_condition_fixture_v774') == 2
    source = source.replace('native_town_condition_fixture_v774', 'native_followup_shortage_fixture_v778')
    source = source.replace('Amsterdam Boom', 'Amsterdam Shortage')
    env = {**original.__dict__, '__file__': str(Path(__file__).resolve())}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
    path = Path(original.sys.argv[original.sys.argv.index('--out')+1])/'capture_report.json'
    report = read(path)
    report['controlled_town_condition_adapter']['source_adapter_sha256'] = sha(Path(original.__file__).read_bytes())
    report['controlled_town_condition_adapter']['effective_adapter_program_sha256'] = sha(source.encode())
    save(path, report)
