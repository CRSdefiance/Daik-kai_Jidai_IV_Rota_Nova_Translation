"""Fixture-free title/New Game controls after the notice-only repack."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous
if __name__=='__main__':
    source=inspect.getsource(previous.main).replace('duel_v1166_','hot_spring_notice_v1637_').replace('V1166:','V1637:')
    source=source.replace('original_duel_cache_visibility_UI_dismissal_and_transitions_pending','original_optional_hot_spring_notice_and_transition_pending')
    env={**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/hot_spring_notice_release_v1636'),'ROM':Path('out/all_routes_combined_v1637_candidate.nds')}
    exec(compile(source,__file__,'exec'),env);env['main']()
