"""Complete cumulative V1676 ancestry and clean-input byte-exact patch proof."""
import inspect
from pathlib import Path
from scripts import verify_battle_aftermath_release_v1267 as previous
from dk4tool.patch import search_reports_editorial as owned
from dk4tool.patch.hot_spring_notice_editorial import current_entries as previous_entries
from scripts.search_reports_native_plan_v1661 import IDS, compiled

if __name__=='__main__':
    source=inspect.getsource(previous.main)
    for old,new in [('all-routes-unified-v1266','all-routes-unified-v1676'),
        ('cdc860e53267dbef64ac9d40a1832b00fda6a4da6adbde2b61be830345d55dbd','0d81ee2668d2ff535432e2a50a5df44b9c1a4b0f683fca407f5753348038e7b2'),
        ('assert set(changed) <= set(IDS)','assert changed == list(IDS)'),('== [22,23]','== [4,23]'),('== 471','== 473'),
        ('all471_batches114_accepted_layers_and_prior_profiles_preserved','all473_batches114_accepted_layers_and_prior_profiles_preserved'),
        ('all75_compiled_paragraphs_and3593_unselected_texts_preserved','all11_compiled_paragraphs_and3657_unselected_texts_preserved'),
        ('only_COMMON22_23_native_metadata_and_existing188_172_selector_spans_changed','only_COMMON4_23_metadata_and_existing188_172_runtime_banks_changed'),
        ('V1266 registered','V1676 registered')]:
        assert source.count(old)==1,old;source=source.replace(old,new)
    env={**previous.__dict__,'__file__':__file__,'owned':owned,'previous_entries':previous_entries,'IDS':IDS,'compiled':compiled,
        'ROOT':Path('work/analysis/search_reports_release_v1675'),'ROM':Path('out/all_routes_combined_v1676_candidate.nds'),
        'OLD':Path('out/all_routes_combined_v1637_candidate.nds')}
    exec(compile(source,__file__,'exec'),env);env['main']()
