"""Fixture-free title/New Game controls for the registered retreat successor."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous

if __name__ == '__main__':
    source = inspect.getsource(previous.main).replace('duel_v1166_', 'retreat_transfer_v1520_').replace('V1166:', 'V1520:')
    source = source.replace('original_duel_cache_visibility_UI_dismissal_and_transitions_pending',
                            'original_retreat_transfer_dismissal_and_transition_pending')
    env = {**previous.__dict__, '__file__': __file__, 'ROOT': Path('work/analysis/retreat_transfer_release_v1519'),
           'ROM': Path('out/all_routes_combined_v1520_candidate.nds')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
