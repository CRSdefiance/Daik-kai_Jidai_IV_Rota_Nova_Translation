"""Exhaustive original-entry memberships/ABI and historical notice controls."""
import inspect
from pathlib import Path
from scripts import verify_powder_fire_runtime_v1308 as previous
from scripts import ship_loss_surrender_runtime_v1442 as runtime
from scripts import enemy_capture_runtime_v1417b as old_runtime

if __name__=='__main__':
    source = inspect.getsource(previous.main)
    for old,new in [
        ("'cac04b66961829b42b3d54bd69d901926434ff1ed24d1be0b2f96665020e8da5'","'db464eea08a5cdf5a0b840aa39f9a29fed0e13a52aa47f606e9060d71e590a76'"),
        ("{'0x2053f40':[0x7980]}","{'0x2053db8':[0x7AC0,0x7B80,0x7C60]}"),
        ('source_and_target_only_one_exact_new_membership','source_and_target_only_three_exact_new_memberships'),
        ('only_one_proven_direct_parent_table_membership_added','only_three_proven_role_parent_table_memberships_added'),
        ('Single fire-table membership,exhaustive native dispatch/ABI and historical modal/status regressions pass.',
         'Three loss/surrender memberships:exhaustive native dispatch/ABI and historical notice controls pass.')]:
        assert source.count(old)==1,old
        source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,'runtime':runtime,'old_runtime':old_runtime,
        'ROM':Path('out/all_routes_combined_v1430_candidate.nds'),
        'ROOT':Path('work/analysis/ship_loss_surrender_runtime_v1443')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
