"""Verify V1344 ancestry,all preservation gates and exact clean-input patch."""
import inspect
from pathlib import Path
from scripts import verify_battle_aftermath_release_v1267 as previous
from dk4tool.patch import ship_sinking_editorial as owned
from dk4tool.patch.powder_fire_editorial import current_entries as previous_entries
from scripts.ship_sinking_native_plan_v1330 import IDS,compiled

if __name__=='__main__':
    source = inspect.getsource(previous.main)
    for old,new in [
        ('all-routes-unified-v1266','all-routes-unified-v1344'),
        ('cdc860e53267dbef64ac9d40a1832b00fda6a4da6adbde2b61be830345d55dbd','f27f98ab3c2d6fb56623e916c12da85355585a5d64622f9637f7c08ff9ddf8aa'),
        ('== [22,23]','== [22]'),
        ('all75_compiled_paragraphs_and3593_unselected_texts_preserved','all16_compiled_paragraphs_and3652_unselected_texts_preserved'),
        ('only_COMMON22_23_native_metadata_and_existing188_172_selector_spans_changed','only_COMMON22_native_metadata_and188_byte_table_changed_all_code_exact'),
        ('V1266 registered','V1344 registered')]:
        assert source.count(old)==1,old
        source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,'owned':owned,'previous_entries':previous_entries,
        'IDS':IDS,'compiled':compiled,'ROOT':Path('work/analysis/ship_sinking_release_v1343'),
        'ROM':Path('out/all_routes_combined_v1344_candidate.nds'),'OLD':Path('out/all_routes_combined_v1316_candidate.nds')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
