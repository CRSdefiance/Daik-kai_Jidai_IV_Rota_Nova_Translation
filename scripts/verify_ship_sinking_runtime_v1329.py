"""Exhaustive native original-entry scope/ABI and preserved historical exits."""
import inspect
from pathlib import Path
from scripts import verify_powder_fire_runtime_v1308 as previous
from scripts import ship_sinking_runtime_v1328 as runtime
from scripts import powder_fire_runtime_v1307 as old_runtime

if __name__=='__main__':
    source = inspect.getsource(previous.main)
    changes = [
        ("'cac04b66961829b42b3d54bd69d901926434ff1ed24d1be0b2f96665020e8da5'","'f27f98ab3c2d6fb56623e916c12da85355585a5d64622f9637f7c08ff9ddf8aa'"),
        ("{'0x2053f40':[0x7980]}","{'0x2053db8':[0x79C0],'0x2053f40':[0x7A80]}"),
        ('source_and_target_only_one_exact_new_membership','source_and_target_only_two_exact_new_memberships'),
        ('only_one_proven_direct_parent_table_membership_added','only_two_proven_role_and_direct_parent_memberships_added'),
        ('Single fire-table membership,exhaustive native dispatch/ABI and historical modal/status regressions pass.',
         'Two sinking-table memberships,exhaustive native dispatch/ABI and historical modal/status regressions pass.')]
    for old,new in changes:
        assert source.count(old)==1,old
        source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,'runtime':runtime,'old_runtime':old_runtime,
        'ROM':Path('out/all_routes_combined_v1316_candidate.nds'),
        'ROOT':Path('work/analysis/ship_sinking_runtime_v1329')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
