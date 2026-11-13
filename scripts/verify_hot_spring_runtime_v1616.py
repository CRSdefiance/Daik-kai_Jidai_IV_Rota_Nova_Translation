"""Exhaustive native selector/ABI/status regression for fixed-bank hot-spring keys."""
import inspect
from pathlib import Path
from scripts import verify_powder_fire_runtime_v1308 as previous
from scripts import hot_spring_runtime_v1614 as runtime
from scripts import sea_responses_runtime_v1555 as old_runtime
if __name__=='__main__':
    source=inspect.getsource(previous.main)
    for old,new in [('cac04b66961829b42b3d54bd69d901926434ff1ed24d1be0b2f96665020e8da5','ba0c910644725ef54a3d817b1754a861244c11fe7c95a06974f32440773bbf54'),
        ("{'0x2053f40':[0x7980]}","{'0x2053db8':[0x6d60,0x6d80]}"),
        ('only_one_proven_direct_parent_table_membership_added','only_two_proven_role_parent_table_memberships_added'),
        ('source_and_target_only_one_exact_new_membership','source_and_target_only_two_exact_new_memberships'),
        ('Single fire-table membership,exhaustive native dispatch/ABI and historical modal/status regressions pass.',
         'Two original hot-spring tables:all524288 native selector/ABI cases and historical modal/status controls pass.')]:
        assert old in source,old;source=source.replace(old,new)
    env={**previous.__dict__,'__file__':__file__,'runtime':runtime,'old_runtime':old_runtime,
        'ROM':Path('out/screenshot_text_repairs_20261022_candidate.nds'),'ROOT':Path('work/analysis/hot_spring_runtime_v1616')}
    exec(compile(source,__file__,'exec'),env);env['main']()
