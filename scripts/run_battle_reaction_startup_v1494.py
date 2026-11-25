"""Ordinary fixture-free title/New Game controls on registered V1492."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous

if __name__=='__main__':
    source=inspect.getsource(previous.main).replace('duel_v1166_','battle_reaction_v1492_').replace('V1166:','V1492:')
    source=source.replace('original_duel_cache_visibility_UI_dismissal_and_transitions_pending',
        'original_reaction_scene_dismissal_and_transition_pending')
    env={**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/battle_reaction_release_v1491'),
        'ROM':Path('out/all_routes_combined_v1492_candidate.nds')}
    exec(compile(source,__file__,'exec'),env);env['main']()
