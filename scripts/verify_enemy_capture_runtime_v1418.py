"""Exhaust original gate memberships,ABI,guards and historical exits."""
import inspect
from pathlib import Path
from scripts import verify_powder_fire_runtime_v1308 as previous
from scripts import enemy_capture_runtime_v1417b as runtime
from scripts import ship_sinking_runtime_v1328 as old_runtime

if __name__=='__main__':
    source = inspect.getsource(previous.main)
    for old,new in [
        ("'cac04b66961829b42b3d54bd69d901926434ff1ed24d1be0b2f96665020e8da5'","'68cd0dd412ea00a294775c44069a6d7e1b8a29c65530aeefea371a01226b5a0e'"),
        ("{'0x2053f40':[0x7980]}","{'0x2053f40':[0x7B00]}"),
        ('Single fire-table membership,exhaustive native dispatch/ABI and historical modal/status regressions pass.',
         'Capture membership with rebased numeric codec:exhaustive native dispatch/ABI and historical modal/status regressions pass.')]:
        assert source.count(old)==1,old
        source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,'runtime':runtime,'old_runtime':old_runtime,
        'ROM':Path('out/all_routes_combined_v1404_candidate.nds'),
        'ROOT':Path('work/analysis/enemy_capture_runtime_v1418')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
