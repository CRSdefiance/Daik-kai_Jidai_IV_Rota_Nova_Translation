"""Exact V1492 complete-stack ancestry and clean-input patch reconstruction."""
import inspect
from pathlib import Path
from scripts import verify_battle_aftermath_release_v1267 as previous
from dk4tool.patch import battle_reaction_editorial as owned
from dk4tool.patch.ship_loss_surrender_editorial import current_entries as previous_entries
from scripts.battle_reaction_native_plan_v1484 import IDS,compiled

if __name__=='__main__':
    source=inspect.getsource(previous.main)
    for old,new in [
        ('all-routes-unified-v1266','all-routes-unified-v1492'),
        ('cdc860e53267dbef64ac9d40a1832b00fda6a4da6adbde2b61be830345d55dbd','2d060af0572c64de56a3749c9feba863afe95edbeed2cb26683d1e9a6ff8ebbe'),
        ('assert set(changed) <= set(IDS)',"assert changed == [r['message_id'] for r in doc['records'] if r['editorial_decision']=='revise'] and len(changed)==16"),
        ('== [22,23]','== [23]'),
        ('all75_compiled_paragraphs_and3593_unselected_texts_preserved','all32_reaction_paragraphs_and3652_unselected_or_retained_texts_preserved'),
        ('only_COMMON22_23_native_metadata_and_existing188_172_selector_spans_changed','only_COMMON23_native_metadata_and_existing188_selector_span_changed'),
        ('V1266 registered','V1492 registered')]:
        assert source.count(old)==1,old
        source=source.replace(old,new)
    env={**previous.__dict__,'__file__':__file__,'owned':owned,'previous_entries':previous_entries,
        'IDS':IDS,'compiled':compiled,'ROOT':Path('work/analysis/battle_reaction_release_v1491'),
        'ROM':Path('out/all_routes_combined_v1492_candidate.nds'),'OLD':Path('out/all_routes_combined_v1456_candidate.nds')}
    exec(compile(source,__file__,'exec'),env);env['main']()
