"""Exhaustive native role-table routing/ABI and inherited modal/status controls."""
import inspect
from pathlib import Path
from scripts import verify_powder_fire_runtime_v1308 as previous
from scripts import sea_responses_runtime_v1555 as runtime
from scripts import declaration_responses_runtime_v1534 as old_runtime

if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    for old, new in [
        ('cac04b66961829b42b3d54bd69d901926434ff1ed24d1be0b2f96665020e8da5', 'b8b256650bb426e99012be06fd060114da0fbf32f763b5c3434204dda8f50437'),
        ("{'0x2053f40':[0x7980]}", "{'0x2053db8':[0x86e0]}"),
        ('only_one_proven_direct_parent_table_membership_added', 'only_one_proven_role_parent_table_membership_added'),
        ('Single fire-table membership,exhaustive native dispatch/ABI and historical modal/status regressions pass.',
         'One original creature/ghost inspection role table:exhaustive native dispatch/ABI and historical controls pass.')]:
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    env = {**previous.__dict__, '__file__': __file__, 'runtime': runtime, 'old_runtime': old_runtime,
        'ROM': Path('out/all_routes_combined_v1542_candidate.nds'), 'ROOT': Path('work/analysis/sea_responses_runtime_v1557')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
