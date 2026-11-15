"""Ordinary no-save startup controls for the registered V1344 candidate."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous

if __name__=='__main__':
    source = inspect.getsource(previous.main).replace('duel_v1166_','ship_sinking_v1344_').replace('V1166:','V1344:')
    source = source.replace('original_duel_cache_visibility_UI_dismissal_and_transitions_pending',
        'original_sinking_events_GPU_dismissal_and_transitions_pending')
    env = {**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/ship_sinking_release_v1343'),
        'ROM':Path('out/all_routes_combined_v1344_candidate.nds')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
