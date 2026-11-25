"""Exact V1542 full-stack ancestry and clean-input xdelta reconstruction."""
import inspect
from pathlib import Path
from scripts import verify_battle_aftermath_release_v1267 as previous
from dk4tool.patch import declaration_responses_editorial as owned
from dk4tool.patch.retreat_transfer_editorial import current_entries as previous_entries
from scripts.declaration_responses_native_plan_v1535b import IDS, compiled

if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    for old, new in [
        ('all-routes-unified-v1266', 'all-routes-unified-v1542'),
        ('cdc860e53267dbef64ac9d40a1832b00fda6a4da6adbde2b61be830345d55dbd', '237066f302fdc1150676a7322753b42af56944a7cb83bf57e3d265f4e155c22a'),
        ('assert set(changed) <= set(IDS)', 'assert changed == list(IDS)'), ('== [22,23]', '== [23]'),
        ('all75_compiled_paragraphs_and3593_unselected_texts_preserved', 'all8_war_responses_and3660_unselected_texts_preserved'),
        ('only_COMMON22_23_native_metadata_and_existing188_172_selector_spans_changed', 'only_COMMON23_native_metadata_and_existing188_selector_span_changed'),
        ('V1266 registered', 'V1542 registered')]:
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    env = {**previous.__dict__, '__file__': __file__, 'owned': owned, 'previous_entries': previous_entries,
        'IDS': IDS, 'compiled': compiled, 'ROOT': Path('work/analysis/declaration_responses_release_v1541'),
        'ROM': Path('out/all_routes_combined_v1542_candidate.nds'), 'OLD': Path('out/all_routes_combined_v1520_candidate.nds')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
