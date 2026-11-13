"""Fixture-free ordinary title/New Game controls on registered V1404."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous


if __name__=='__main__':
    source = inspect.getsource(previous.main).replace('duel_v1166_','battle_victory_v1404_').replace('V1166:','V1404:')
    source = source.replace('original_duel_cache_visibility_UI_dismissal_and_transitions_pending',
        'original_victory_reward_UI_dismissal_and_return_pending')
    env = {**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/battle_victory_release_v1403'),
        'ROM':Path('out/all_routes_combined_v1404_candidate.nds')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
