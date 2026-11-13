"""Exact complete-stack V1456 ancestry and clean-input patch reconstruction."""
import inspect
from pathlib import Path
from scripts import verify_battle_aftermath_release_v1267 as previous
from dk4tool.patch import ship_loss_surrender_editorial as owned
from dk4tool.patch.enemy_capture_editorial import current_entries as previous_entries
from scripts.ship_loss_surrender_native_plan_v1447 import IDS,compiled

if __name__=='__main__':
    source = inspect.getsource(previous.main)
    for old,new in [
        ('all-routes-unified-v1266','all-routes-unified-v1456'),
        ('cdc860e53267dbef64ac9d40a1832b00fda6a4da6adbde2b61be830345d55dbd','db464eea08a5cdf5a0b840aa39f9a29fed0e13a52aa47f606e9060d71e590a76'),
        ('assert set(changed) <= set(IDS)','assert changed == list(IDS)'),
        ('all75_compiled_paragraphs_and3593_unselected_texts_preserved','all24_loss_surrender_paragraphs_and3644_unselected_texts_preserved'),
        ('V1266 registered','V1456 registered')]:
        assert source.count(old)==1,old
        source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,'owned':owned,'previous_entries':previous_entries,
        'IDS':IDS,'compiled':compiled,'ROOT':Path('work/analysis/ship_loss_surrender_release_v1455'),
        'ROM':Path('out/all_routes_combined_v1456_candidate.nds'),'OLD':Path('out/all_routes_combined_v1430_candidate.nds')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
