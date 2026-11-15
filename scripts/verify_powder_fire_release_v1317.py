"""Exact registered ancestry,reconstruction and preserved routes/graphics for V1316."""
import inspect
from pathlib import Path
from scripts import verify_battle_aftermath_release_v1267 as previous
from dk4tool.patch import powder_fire_editorial as owned
from dk4tool.patch.battle_aftermath_editorial import current_entries as previous_entries
from scripts.powder_fire_layout_v1304 import IDS
from scripts.powder_fire_native_plan_v1309 import compiled

if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    changes = [
        ('all-routes-unified-v1266','all-routes-unified-v1316'),
        ('cdc860e53267dbef64ac9d40a1832b00fda6a4da6adbde2b61be830345d55dbd','cac04b66961829b42b3d54bd69d901926434ff1ed24d1be0b2f96665020e8da5'),
        ('== [22,23]','== [22]'),
        ('all75_compiled_paragraphs_and3593_unselected_texts_preserved','all6_compiled_paragraphs_and3662_unselected_texts_preserved'),
        ('only_COMMON22_23_native_metadata_and_existing188_172_selector_spans_changed','only_COMMON22_native_metadata_and188_byte_table_changed_gate_code_exact'),
        ('V1266 registered','V1316 registered')]
    for old,new in changes:
        assert source.count(old) == 1,(old,source.count(old))
        source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,'owned':owned,'previous_entries':previous_entries,
        'IDS':IDS,'compiled':compiled,'ROOT':Path('work/analysis/powder_fire_release_v1315'),
        'ROM':Path('out/all_routes_combined_v1316_candidate.nds'),'OLD':Path('out/all_routes_combined_v1266_candidate.nds')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
