"""Bind current status destination and its original IP-register exit contract.

V1254 stopped at an obsolete ownership map. V1254b reached905, then missed
the already relocated status hook. The original STATUS_EXIT loads IP with
the current Thumb status destination. Both are harness bindings, not ROM fixes.
"""
import inspect
from pathlib import Path
from types import FunctionType, SimpleNamespace

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
    old_status = previous.historical.runtime.previous.previous.previous.previous.STATUS
    assert old_status == 0x021479D4
    env = {**previous.__dict__,'__file__':__file__,
        'ROOT':Path('work/analysis/battle_aftermath_runtime_v1254c'),
        'bank':SimpleNamespace(**{**previous.bank.__dict__,'STATUS':old_status})}
    scope = inspect.getsource(previous.scope)
    old = 'assert cpu.reg_read(UC_ARM_REG_R12) == bank.GATE|1'
    new = 'assert cpu.reg_read(UC_ARM_REG_R12) == ((bank.STATUS if route == bank.STATUS else bank.GATE)|1)'
    assert scope.count(old) == 1
    scope = scope.replace(old,new)
    exec(compile(scope,__file__,'exec'),env)
    exec(compile(source,__file__,'exec'),env)
    env['main']()
