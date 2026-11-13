"""Ordinary no-save full-screen startup controls for registered V1266."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous


if __name__ == '__main__':
    source = inspect.getsource(previous.main).replace('duel_v1166_','battle_aftermath_v1266_').replace('V1166:','V1266:')
    source = source.replace('original_duel_cache_visibility_UI_dismissal_and_transitions_pending',
        'original_aftermath_surrender_and_defense_scenes_dismissal_transitions_pending')
    env = {**previous.__dict__,'__file__':__file__,
        'ROOT':Path('work/analysis/battle_aftermath_release_v1265'),
        'ROM':Path('out/all_routes_combined_v1266_candidate.nds')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
