"""Registered title/New Game controls; the whole research ROM is byte-identical."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous

if __name__=='__main__':
    source=inspect.getsource(previous.main).replace('duel_v1166_','maria_opening_v2047_').replace('V1166:','V2047:')
    source=source.replace('original_duel_cache_visibility_UI_dismissal_and_transitions_pending',
        'registered_Maria_opening_editorial_ledger_completion_pending')
    env={**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/maria_opening_release_v2046'),
        'ROM':Path('out/all_routes_combined_v2047_candidate.nds')}
    exec(compile(source,__file__,'exec'),env);env['main']()
