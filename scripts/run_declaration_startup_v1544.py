"""Fixture-free title/New Game controls for the registered NPC-response candidate."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous

if __name__ == '__main__':
    source = inspect.getsource(previous.main).replace('duel_v1166_', 'declaration_responses_v1542_').replace('V1166:', 'V1542:')
    source = source.replace('original_duel_cache_visibility_UI_dismissal_and_transitions_pending', 'original_revised_NPC_response_and_transition_pending')
    env = {**previous.__dict__, '__file__': __file__, 'ROOT': Path('work/analysis/declaration_responses_release_v1541'),
        'ROM': Path('out/all_routes_combined_v1542_candidate.nds')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
