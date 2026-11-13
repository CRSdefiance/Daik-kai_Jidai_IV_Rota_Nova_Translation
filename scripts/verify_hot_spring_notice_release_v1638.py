"""Exact cumulative V1637 ancestry and clean-input patch reconstruction."""
import inspect
from pathlib import Path
from scripts import verify_battle_aftermath_release_v1267 as previous
from dk4tool.patch import hot_spring_notice_editorial as owned
from dk4tool.patch.hot_spring_editorial import current_entries as previous_entries
from scripts.hot_spring_notice_plan_v1632 import IDS,compiled
if __name__=='__main__':
    source=inspect.getsource(previous.main)
    for old,new in [('all-routes-unified-v1266','all-routes-unified-v1637'),
        ('cdc860e53267dbef64ac9d40a1832b00fda6a4da6adbde2b61be830345d55dbd','cb049635c45b6bc75add4ada18db69ae2ece4aa05b9270a3553ed9ed74a228e4'),
        ('assert set(changed) <= set(IDS)','assert changed == list(IDS)'),('== [22,23]','== [4]'),('== 471','== 473'),
        ('all471_batches114_accepted_layers_and_prior_profiles_preserved','all473_batches114_accepted_layers_and_prior_profiles_preserved'),
        ('all75_compiled_paragraphs_and3593_unselected_texts_preserved','all1_Experience_notice_and3667_unselected_texts_preserved'),
        ('only_COMMON22_23_native_metadata_and_existing188_172_selector_spans_changed','only_COMMON4_and_original_native_metadata_changed'),
        ('V1266 registered','V1637 registered')]:
        assert source.count(old)==1,old;source=source.replace(old,new)
    env={**previous.__dict__,'__file__':__file__,'owned':owned,'previous_entries':previous_entries,'IDS':IDS,'compiled':compiled,
        'ROOT':Path('work/analysis/hot_spring_notice_release_v1636'),'ROM':Path('out/all_routes_combined_v1637_candidate.nds'),'OLD':Path('out/all_routes_combined_v1622_candidate.nds')}
    exec(compile(source,__file__,'exec'),env);env['main']()
