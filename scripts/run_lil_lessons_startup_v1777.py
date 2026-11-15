"""Fixture-free registered V1775 title and unchanged Rafael New Game controls."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous

if __name__=='__main__':
    source=inspect.getsource(previous.main).replace('duel_v1166_','lil_lessons_v1775_').replace('V1166:','V1775:')
    source=source.replace('original_duel_cache_visibility_UI_dismissal_and_transitions_pending',
        'Lil_lessons_registered_terminal_reconciliation_pending')
    env={**previous.__dict__,'__file__':__file__,
        'ROOT':Path('work/analysis/lil_lessons_release_v1774'),
        'ROM':Path('out/all_routes_combined_v1775_candidate.nds')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
