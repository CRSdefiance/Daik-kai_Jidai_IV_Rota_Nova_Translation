"""Exact V1364 ancestry,preservation and clean-input patch reconstruction."""
import inspect
from pathlib import Path
from scripts import verify_battle_aftermath_release_v1267 as previous
from dk4tool.patch import flagship_capture_precision as owned
from dk4tool.patch.ship_sinking_editorial import current_entries as previous_entries
from scripts.flagship_precision_native_plan_v1356 import IDS,compiled

if __name__=='__main__':
    source = inspect.getsource(previous.main)
    for old,new in [
        ('all-routes-unified-v1266','all-routes-unified-v1364'),
        ('cdc860e53267dbef64ac9d40a1832b00fda6a4da6adbde2b61be830345d55dbd','9d455782724d98198b7bc3fdac7be755945e58d406e66a4634094d9a0eab301b'),
        ('== [22,23]','== [22]'),
        ('all75_compiled_paragraphs_and3593_unselected_texts_preserved','only2015_corrected_all3667_unselected_texts_preserved'),
        ('only_COMMON22_23_native_metadata_and_existing188_172_selector_spans_changed','only_COMMON22_native_metadata_changed_entire_runtime_and_selector_exact'),
        ('V1266 registered','V1364 registered')]:
        assert source.count(old)==1,old
        source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,'owned':owned,'previous_entries':previous_entries,
        'IDS':IDS,'compiled':compiled,'ROOT':Path('work/analysis/flagship_precision_release_v1363'),
        'ROM':Path('out/all_routes_combined_v1364_candidate.nds'),'OLD':Path('out/all_routes_combined_v1344_candidate.nds')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
