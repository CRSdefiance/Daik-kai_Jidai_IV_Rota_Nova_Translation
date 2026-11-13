"""Use the later proved 188-byte metadata ownership, not the old V772 map.

The predecessor stopped before writing output: V772 predates the metadata
compaction already installed and verified by V1184c. No runtime bytes change.
"""
import inspect
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import verify_battle_aftermath_runtime_v1254 as previous
from scripts import escape_direct_runtime_v1183b as old_runtime
from scripts.verify_village_wrap_v608 import read


if __name__ == '__main__':
    proof = Path('work/analysis/escape_direct_runtime_v1184c/runtime_plan.json')
    plan = read(proof)
    assert plan['runtime_module_sha256'] == sha(Path(old_runtime.__file__).read_bytes())
    assert [old_runtime.CONTRACTS,old_runtime.CONTRACTS+188] in plan['private_spans']
    assert [old_runtime.GATE,old_runtime.GATE+172] in plan['private_spans']
    source = inspect.getsource(previous.main)
    old = 'work/analysis/recruitment_owned_v772/owned_runtime_plan.json'
    assert source.count(old) == 1
    source = source.replace(old,str(proof).replace('\\','/'))
    env = {**previous.__dict__,'__file__':__file__,
        'ROOT':Path('work/analysis/battle_aftermath_runtime_v1254b')}
    # Bind scope to the same new output directory while keeping its code frozen.
    from types import FunctionType
    env['scope'] = FunctionType(previous.scope.__code__,env)
    exec(compile(source,__file__,'exec'),env)
    env['main']()
