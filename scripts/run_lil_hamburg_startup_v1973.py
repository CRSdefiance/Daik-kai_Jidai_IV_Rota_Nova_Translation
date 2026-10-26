"""Fresh fixture-free registered V1971 title and New Game controls."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous

if __name__ == '__main__':
    source = inspect.getsource(previous.main).replace('duel_v1166_','lil_Hamburg_v1971_').replace('V1166:','V1971:')
    source = source.replace('original_duel_cache_visibility_UI_dismissal_and_transitions_pending',
        'registered_Hamburg_visual_reconciliation_and_editorial_completion_pending')
    env = {**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/lil_Hamburg_release_v1970'),
        'ROM':Path('out/all_routes_combined_v1971_candidate.nds')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
