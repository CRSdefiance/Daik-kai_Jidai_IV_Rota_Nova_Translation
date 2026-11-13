"""Exact combined V1404 ancestry,preservation and clean-input reconstruction."""
import inspect
from pathlib import Path
from scripts import verify_battle_aftermath_release_v1267 as previous
from dk4tool.patch import battle_victory_editorial as owned
from dk4tool.patch.flagship_capture_precision import current_entries as previous_entries
from scripts.battle_victory_native_plan_v1396 import IDS,compiled


if __name__=='__main__':
    source = inspect.getsource(previous.main)
    for old,new in [
        ('all-routes-unified-v1266','all-routes-unified-v1404'),
        ('cdc860e53267dbef64ac9d40a1832b00fda6a4da6adbde2b61be830345d55dbd','dbf86d020cb868f443f9c6a9f68706e8cda28e9268ce0318a63ef765f4f3281c'),
        ('== [22,23]','== [23]'),
        ('assert set(changed) <= set(IDS)','assert changed == [2136,2137]'),
        ('all75_compiled_paragraphs_and3593_unselected_texts_preserved','all8_victory_paragraphs_and3666_unselected_or_retained_texts_preserved'),
        ('only_COMMON22_23_native_metadata_and_existing188_172_selector_spans_changed','only_COMMON23_native_metadata_changed_entire_runtime_and_selector_exact'),
        ('V1266 registered','V1404 registered')]:
        assert source.count(old)==1,old
        source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,'owned':owned,'previous_entries':previous_entries,
        'IDS':IDS,'compiled':compiled,'ROOT':Path('work/analysis/battle_victory_release_v1403'),
        'ROM':Path('out/all_routes_combined_v1404_candidate.nds'),'OLD':Path('out/all_routes_combined_v1364_candidate.nds')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
