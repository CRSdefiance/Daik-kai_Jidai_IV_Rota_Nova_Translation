"""Fixture-free ordinary title/New Game controls on registered V1456."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous

if __name__=='__main__':
    source = inspect.getsource(previous.main).replace('duel_v1166_','loss_surrender_v1456_').replace('V1166:','V1456:')
    source = source.replace('original_duel_cache_visibility_UI_dismissal_and_transitions_pending',
        'original_loss_surrender_event_dismissal_and_return_pending')
    env = {**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/ship_loss_surrender_release_v1455'),
        'ROM':Path('out/all_routes_combined_v1456_candidate.nds')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
