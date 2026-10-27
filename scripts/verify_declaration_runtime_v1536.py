"""Exhaustive original-entry gate/ABI and inherited controls for the NPC war table."""
import inspect
from pathlib import Path
from scripts import verify_powder_fire_runtime_v1308 as previous
from scripts import declaration_responses_runtime_v1534 as runtime
from scripts import retreat_transfer_runtime_v1509b as old_runtime

if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    for old, new in [
        ('cac04b66961829b42b3d54bd69d901926434ff1ed24d1be0b2f96665020e8da5', '237066f302fdc1150676a7322753b42af56944a7cb83bf57e3d265f4e155c22a'),
        ("{'0x2053f40':[0x7980]}", "{'0x2053f40':[0x84e0]}"),
        ('Single fire-table membership,exhaustive native dispatch/ABI and historical modal/status regressions pass.',
         'One exact NPC war-response table:exhaustive native dispatch/ABI and historical controls pass.')]:
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    env = {**previous.__dict__, '__file__': __file__, 'runtime': runtime, 'old_runtime': old_runtime,
        'ROM': Path('out/all_routes_combined_v1520_candidate.nds'), 'ROOT': Path('work/analysis/declaration_responses_runtime_v1536')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
