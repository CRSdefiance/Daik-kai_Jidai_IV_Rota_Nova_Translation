"""Exact V1563 full-stack ancestry and clean-input xdelta reconstruction."""
import inspect
from pathlib import Path
from scripts import verify_battle_aftermath_release_v1267 as previous
from dk4tool.patch import sea_responses_editorial as owned
from dk4tool.patch.declaration_responses_editorial import current_entries as previous_entries
from scripts.sea_responses_native_plan_v1556 import IDS, compiled

if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    for old, new in [
        ('all-routes-unified-v1266', 'all-routes-unified-v1563'),
        ('cdc860e53267dbef64ac9d40a1832b00fda6a4da6adbde2b61be830345d55dbd', 'b8b256650bb426e99012be06fd060114da0fbf32f763b5c3434204dda8f50437'),
        ('assert set(changed) <= set(IDS)', 'assert changed == [2209,2210,2211,2212,2215]'), ('== [22,23]', '== [23]'),
        ('all75_compiled_paragraphs_and3593_unselected_texts_preserved', 'all8_sea_responses_and3663_unselected_or_retained_texts_preserved'),
        ('only_COMMON22_23_native_metadata_and_existing188_172_selector_spans_changed', 'only_COMMON23_native_metadata_and_existing188_selector_span_changed'),
        ('V1266 registered', 'V1563 registered')]:
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    env = {**previous.__dict__, '__file__': __file__, 'owned': owned, 'previous_entries': previous_entries,
        'IDS': IDS, 'compiled': compiled, 'ROOT': Path('work/analysis/declaration_responses_release_v1562'),
        'ROM': Path('out/all_routes_combined_v1563_candidate.nds'), 'OLD': Path('out/all_routes_combined_v1542_candidate.nds')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
