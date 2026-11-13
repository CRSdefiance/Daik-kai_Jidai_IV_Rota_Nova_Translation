"""Fixture-free registered V1711 title and unchanged Rafael New Game controls."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous

if __name__ == '__main__':
    source = inspect.getsource(previous.main).replace('duel_v1166_', 'lil_opening_v1711_').replace('V1166:', 'V1711:')
    source = source.replace('original_duel_cache_visibility_UI_dismissal_and_transitions_pending',
        'Lil_complete_scene_terminal_reconciliation_pending')
    env = {**previous.__dict__, '__file__':__file__,
        'ROOT':Path('work/analysis/lil_opening_release_v1710'),
        'ROM':Path('out/all_routes_combined_v1711_candidate.nds')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
