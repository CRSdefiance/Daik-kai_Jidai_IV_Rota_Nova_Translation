"""Fixture-free title/New Game controls for the registered sea-inspection candidate."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous

if __name__ == '__main__':
    source = inspect.getsource(previous.main).replace('duel_v1166_', 'sea_responses_v1563_').replace('V1166:', 'V1563:')
    source = source.replace('original_duel_cache_visibility_UI_dismissal_and_transitions_pending', 'original_special_target_inspection_and_transition_pending')
    env = {**previous.__dict__, '__file__': __file__, 'ROOT': Path('work/analysis/sea_responses_release_v1562'),
        'ROM': Path('out/all_routes_combined_v1563_candidate.nds')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
