"""Combined V1430 ancestry,preservation and exact clean-input reconstruction."""
import inspect
from pathlib import Path
from scripts import verify_battle_aftermath_release_v1267 as previous
from dk4tool.patch import enemy_capture_editorial as owned
from dk4tool.patch.battle_victory_editorial import current_entries as previous_entries
from scripts.enemy_capture_native_plan_v1423 import IDS,compiled

if __name__=='__main__':
    source = inspect.getsource(previous.main)
    for old,new in [
        ('all-routes-unified-v1266','all-routes-unified-v1430'),
        ('cdc860e53267dbef64ac9d40a1832b00fda6a4da6adbde2b61be830345d55dbd','68cd0dd412ea00a294775c44069a6d7e1b8a29c65530aeefea371a01226b5a0e'),
        ('== [22,23]','== [22]'),('assert set(changed) <= set(IDS)','assert changed == list(IDS)'),
        ('all75_compiled_paragraphs_and3593_unselected_texts_preserved','all8_capture_paragraphs_and3660_unselected_texts_preserved'),
        ('only_COMMON22_23_native_metadata_and_existing188_172_selector_spans_changed','only_COMMON22_native_metadata_and_existing188_172_selector_spans_changed'),
        ('V1266 registered','V1430 registered')]:
        assert source.count(old)==1,old
        source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,'owned':owned,'previous_entries':previous_entries,
        'IDS':IDS,'compiled':compiled,'ROOT':Path('work/analysis/enemy_capture_release_v1429'),
        'ROM':Path('out/all_routes_combined_v1430_candidate.nds'),'OLD':Path('out/all_routes_combined_v1404_candidate.nds')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
