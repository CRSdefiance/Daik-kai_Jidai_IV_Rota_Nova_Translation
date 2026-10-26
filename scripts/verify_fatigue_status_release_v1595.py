"""Exact V1594 full-stack ancestry and clean-input xdelta reconstruction."""
import inspect
from pathlib import Path
from scripts import verify_battle_aftermath_release_v1267 as previous
from dk4tool.patch import fatigue_status_editorial as owned
from dk4tool.patch.inspection_status_editorial import current_entries as previous_entries
from scripts.fatigue_status_native_plan_v1589 import IDS, compiled

if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    for old, new in [
        ('all-routes-unified-v1266', 'all-routes-unified-v1594'),
        ('cdc860e53267dbef64ac9d40a1832b00fda6a4da6adbde2b61be830345d55dbd', 'd29f08026385628b47fcc0aa996402501975f986dbe2426ba348be723b37e79b'),
        ('assert set(changed) <= set(IDS)', 'assert changed == list(IDS)'), ('== [22,23]', '== [4]'),
        ('all75_compiled_paragraphs_and3593_unselected_texts_preserved', 'all2_fatigue_statuses_and3666_unselected_texts_preserved'),
        ('only_COMMON22_23_native_metadata_and_existing188_172_selector_spans_changed', 'only_COMMON4_and_original_native_metadata_changed'),
        ('V1266 registered', 'V1594 registered')]:
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    env = {**previous.__dict__, '__file__': __file__, 'owned': owned, 'previous_entries': previous_entries,
        'IDS': IDS, 'compiled': compiled, 'ROOT': Path('work/analysis/fatigue_status_release_v1593'),
        'ROM': Path('out/all_routes_combined_v1594_candidate.nds'), 'OLD': Path('out/all_routes_combined_v1578_candidate.nds')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
