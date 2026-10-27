"""Exact V1520 ancestry and full clean-input xdelta reconstruction."""
import inspect
from pathlib import Path
from scripts import verify_battle_aftermath_release_v1267 as previous
from dk4tool.patch import retreat_transfer_editorial as owned
from dk4tool.patch.battle_reaction_editorial import current_entries as previous_entries
from scripts.retreat_transfer_native_plan_v1514 import IDS, compiled

if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    for old, new in [
        ('all-routes-unified-v1266', 'all-routes-unified-v1520'),
        ('cdc860e53267dbef64ac9d40a1832b00fda6a4da6adbde2b61be830345d55dbd',
         '96d0eda08db4f6da69a936a44db1f41abcc1cd6ce202370a9edc5517eb5400fd'),
        ('assert set(changed) <= set(IDS)', 'assert changed == list(IDS)'),
        ('== [22,23]', '== [28]'),
        ('all75_compiled_paragraphs_and3593_unselected_texts_preserved', 'all7_retreat_paragraphs_and3661_unselected_texts_preserved'),
        ('only_COMMON22_23_native_metadata_and_existing188_172_selector_spans_changed',
         'only_COMMON28_native_metadata_and_existing188_selector_span_changed'),
        ('V1266 registered', 'V1520 registered')]:
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    env = {**previous.__dict__, '__file__': __file__, 'owned': owned, 'previous_entries': previous_entries,
        'IDS': IDS, 'compiled': compiled, 'ROOT': Path('work/analysis/retreat_transfer_release_v1519'),
        'ROM': Path('out/all_routes_combined_v1520_candidate.nds'), 'OLD': Path('out/all_routes_combined_v1492_candidate.nds')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
