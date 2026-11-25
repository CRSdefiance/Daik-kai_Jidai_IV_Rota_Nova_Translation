"""Original selector/ABI/historical controls for the exact retreat-table scope."""
import inspect
from pathlib import Path
from scripts import verify_powder_fire_runtime_v1308 as previous
from scripts import retreat_transfer_runtime_v1509b as runtime
from scripts import battle_reaction_runtime_v1483 as old_runtime

if __name__=='__main__':
    source=inspect.getsource(previous.main)
    for old,new in [
        ("'cac04b66961829b42b3d54bd69d901926434ff1ed24d1be0b2f96665020e8da5'","'96d0eda08db4f6da69a936a44db1f41abcc1cd6ce202370a9edc5517eb5400fd'"),
        ("{'0x2053f40':[0x7980]}","{'0x2053db8':[0x7080]}"),
        ('only_one_proven_direct_parent_table_membership_added','only_one_proven_role_parent_table_membership_added'),
        ('Single fire-table membership,exhaustive native dispatch/ABI and historical modal/status regressions pass.',
         'One replacement-ship retreat membership:exhaustive native dispatch/ABI and historical controls pass.')]:
        assert source.count(old)==1,old
        source=source.replace(old,new)
    env={**previous.__dict__,'__file__':__file__,'runtime':runtime,'old_runtime':old_runtime,
        'ROM':Path('out/all_routes_combined_v1492_candidate.nds'),'ROOT':Path('work/analysis/retreat_transfer_runtime_v1510')}
    exec(compile(source,__file__,'exec'),env);env['main']()
