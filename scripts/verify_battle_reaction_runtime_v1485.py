"""Exhaustive original selector/ABI and historical notice checks for four scopes."""
import inspect
from pathlib import Path
from scripts import verify_powder_fire_runtime_v1308 as previous
from scripts import battle_reaction_runtime_v1483 as runtime
from scripts import ship_loss_surrender_runtime_v1442b as old_runtime

if __name__=='__main__':
    source=inspect.getsource(previous.main)
    for old,new in [
        ("'cac04b66961829b42b3d54bd69d901926434ff1ed24d1be0b2f96665020e8da5'","'2d060af0572c64de56a3749c9feba863afe95edbeed2cb26683d1e9a6ff8ebbe'"),
        ("{'0x2053f40':[0x7980]}","{'0x2053f40':[0x7F40,0x7F80,0x8000,0x8060]}"),
        ('source_and_target_only_one_exact_new_membership','source_and_target_only_four_exact_new_memberships'),
        ('only_one_proven_direct_parent_table_membership_added','only_four_proven_actor_parent_table_memberships_added'),
        ('Single fire-table membership,exhaustive native dispatch/ABI and historical modal/status regressions pass.',
         'Four reaction-table memberships:exhaustive native dispatch/ABI and historical notice controls pass.')]:
        assert source.count(old)==1,old
        source=source.replace(old,new)
    env={**previous.__dict__,'__file__':__file__,'runtime':runtime,'old_runtime':old_runtime,
        'ROM':Path('out/all_routes_combined_v1456_candidate.nds'),'ROOT':Path('work/analysis/battle_reaction_runtime_v1485')}
    exec(compile(source,__file__,'exec'),env);env['main']()
