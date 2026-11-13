"""Fresh fixture-free registered V1945 startup/title/New Game controls."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous

if __name__=='__main__':
    source=inspect.getsource(previous.main).replace('duel_v1166_','lil_Speyer_v1945_').replace('V1166:','V1945:')
    source=source.replace('original_duel_cache_visibility_UI_dismissal_and_transitions_pending',
        'registered_Speyer_visual_reconciliation_and_editorial_completion_pending')
    env={**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/lil_Speyer_release_v1944'),
        'ROM':Path('out/all_routes_combined_v1945_candidate.nds')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
