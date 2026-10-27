"""Fresh registered startup/title controls; story/choices bind identical research."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous

if __name__=='__main__':
    source=inspect.getsource(previous.main).replace('duel_v1166_','rafael_opening_v2013_').replace('V1166:','V2013:')
    source=source.replace('original_duel_cache_visibility_UI_dismissal_and_transitions_pending',
        'registered_Rafael_opening_final_editorial_ledger_completion_pending')
    env={**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/rafael_opening_release_v2012'),
        'ROM':Path('out/all_routes_combined_v2013_candidate.nds')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
