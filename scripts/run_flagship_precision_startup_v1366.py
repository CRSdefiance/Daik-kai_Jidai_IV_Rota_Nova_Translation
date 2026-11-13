"""Ordinary no-save startup/title/New Game controls for V1364."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous

if __name__=='__main__':
    source = inspect.getsource(previous.main).replace('duel_v1166_','flagship_precision_v1364_').replace('V1166:','V1364:')
    source = source.replace('original_duel_cache_visibility_UI_dismissal_and_transitions_pending',
        'original_capture_replay_cache_visibility_UI_dismissal_and_transitions_pending')
    env = {**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/flagship_precision_release_v1363'),
        'ROM':Path('out/all_routes_combined_v1364_candidate.nds')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
