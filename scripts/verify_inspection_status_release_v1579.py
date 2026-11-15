"""Exact V1578 full-stack ancestry and clean-input xdelta reconstruction."""
import inspect
from pathlib import Path
from scripts import verify_battle_aftermath_release_v1267 as previous
from dk4tool.patch import inspection_status_editorial as owned
from dk4tool.patch.sea_responses_editorial import current_entries as previous_entries
from scripts.inspection_status_native_plan_v1573 import IDS, compiled

if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    for old, new in [
        ('all-routes-unified-v1266', 'all-routes-unified-v1578'),
        ('cdc860e53267dbef64ac9d40a1832b00fda6a4da6adbde2b61be830345d55dbd', 'ba126ed72ce7ee1288cc689286cc7c2d98bb2c727f91d5e074568a8953a385a1'),
        ('assert set(changed) <= set(IDS)', 'assert changed == list(IDS)'), ('== [22,23]', '== [4]'),
        ('all75_compiled_paragraphs_and3593_unselected_texts_preserved', 'all2_modal_statuses_and3666_unselected_texts_preserved'),
        ('only_COMMON22_23_native_metadata_and_existing188_172_selector_spans_changed', 'only_COMMON4_and_original_native_metadata_changed'),
        ('V1266 registered', 'V1578 registered')]:
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    env = {**previous.__dict__, '__file__': __file__, 'owned': owned, 'previous_entries': previous_entries,
        'IDS': IDS, 'compiled': compiled, 'ROOT': Path('work/analysis/inspection_status_release_v1577'),
        'ROM': Path('out/all_routes_combined_v1578_candidate.nds'), 'OLD': Path('out/all_routes_combined_v1563_candidate.nds')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
