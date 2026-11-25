"""Fresh ordinary V1986 startup/title/New Game controls without fixtures."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous

if __name__ == '__main__':
    source = inspect.getsource(previous.main).replace('duel_v1166_','lil_Lookout_v1986_').replace('V1166:','V1986:')
    source = source.replace('original_duel_cache_visibility_UI_dismissal_and_transitions_pending',
        'registered_Lookout_final_contextual_reconciliation_pending')
    env = {**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/lil_Lookout_release_v1985'),
        'ROM':Path('out/all_routes_combined_v1986_candidate.nds')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
