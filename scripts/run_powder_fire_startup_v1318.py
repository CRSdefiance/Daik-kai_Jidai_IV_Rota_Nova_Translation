"""Ordinary no-save title/New Game controls for the complete V1316 candidate."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous

if __name__ == '__main__':
    source = inspect.getsource(previous.main).replace('duel_v1166_','powder_fire_v1316_').replace('V1166:','V1316:')
    source = source.replace('original_duel_cache_visibility_UI_dismissal_and_transitions_pending',
        'original_powder_fire_revised_scene_dismissal_and_transitions_pending')
    env = {**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/powder_fire_release_v1315'),
        'ROM':Path('out/all_routes_combined_v1316_candidate.nds')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
