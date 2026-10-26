"""Fixture-free title/New Game controls for the registered sea-inspection candidate."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous

if __name__ == '__main__':
    source = inspect.getsource(previous.main).replace('duel_v1166_', 'inspection_status_v1578_').replace('V1166:', 'V1578:')
    source = source.replace('original_duel_cache_visibility_UI_dismissal_and_transitions_pending', 'original_special_target_inspection_and_transition_pending')
    env = {**previous.__dict__, '__file__': __file__, 'ROOT': Path('work/analysis/inspection_status_release_v1577'),
        'ROM': Path('out/all_routes_combined_v1578_candidate.nds')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
