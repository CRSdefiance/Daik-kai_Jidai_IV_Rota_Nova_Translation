"""Explicit crowd-fixture adapter,derived from the unchanged expert adapter."""

import inspect
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import run_followup_expert_capture_v778 as original
from scripts.verify_village_wrap_v608 import read, save


if __name__ == '__main__':
    source = inspect.getsource(original.main)
    old, new = 'native_followup_expert_fixture_v778', 'native_followup_crowd_fixture_v778'
    assert source.count(old) == 2
    source = source.replace(old, new)
    env = {**original.__dict__, '__file__': str(Path(__file__).resolve())}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
    path = Path(original.sys.argv[original.sys.argv.index('--out')+1])/'capture_report.json'
    report = read(path)
    report['controlled_strategist_adapter']['source_adapter_sha256'] = sha(Path(original.__file__).read_bytes())
    report['controlled_strategist_adapter']['effective_adapter_program_sha256'] = sha(source.encode())
    save(path, report)
