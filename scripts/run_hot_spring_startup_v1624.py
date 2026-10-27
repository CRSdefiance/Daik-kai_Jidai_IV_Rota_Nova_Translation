"""Fixture-free title/New Game controls for integrated hot-spring candidate."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous
if __name__=='__main__':
    source=inspect.getsource(previous.main).replace('duel_v1166_','hot_spring_v1622_').replace('V1166:','V1622:')
    source=source.replace('original_duel_cache_visibility_UI_dismissal_and_transitions_pending','original_hot_spring_and_transition_pending')
    env={**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/hot_spring_release_v1621'),'ROM':Path('out/all_routes_combined_v1622_candidate.nds')}
    exec(compile(source,__file__,'exec'),env);env['main']()
