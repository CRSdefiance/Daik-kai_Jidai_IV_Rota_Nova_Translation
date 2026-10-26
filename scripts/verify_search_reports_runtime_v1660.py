"""Exhaustive native dispatch/ABI and historical regression for the191 codec."""
import inspect
from pathlib import Path
from scripts import verify_powder_fire_runtime_v1308 as previous
from scripts import search_reports_runtime_v1659 as runtime
from scripts import hot_spring_runtime_v1614 as old_runtime

if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    for old, new in [
        ('cac04b66961829b42b3d54bd69d901926434ff1ed24d1be0b2f96665020e8da5', '0d81ee2668d2ff535432e2a50a5df44b9c1a4b0f683fca407f5753348038e7b2'),
        ("{'0x2053f40':[0x7980]}", "{'0x2053db8':[0x6e80,0x6ec0]}"),
        ('only_one_proven_direct_parent_table_membership_added', 'only_two_original_Search_speech_tables_added'),
        ('source_and_target_only_one_exact_new_membership', 'source_and_target_only_two_exact_Search_memberships'),
        ('Single fire-table membership,exhaustive native dispatch/ABI and historical modal/status regressions pass.',
         'Search tables and191 codec:exhaustive native dispatch/ABI and historical modal/status regressions pass.')]:
        assert old in source, old
        source = source.replace(old, new)
    env = {**previous.__dict__, '__file__': __file__, 'runtime': runtime, 'old_runtime': old_runtime,
           'ROM': Path('out/all_routes_combined_v1637_candidate.nds'), 'ROOT': Path('work/analysis/search_reports_runtime_v1660')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
