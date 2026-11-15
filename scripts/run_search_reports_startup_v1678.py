"""Fixture-free title/New Game controls after cumulative Search report changes."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous
if __name__=='__main__':
    source=inspect.getsource(previous.main).replace('duel_v1166_','search_reports_v1676_').replace('V1166:','V1676:')
    source=source.replace('original_duel_cache_visibility_UI_dismissal_and_transitions_pending','original_revised_Search_reports_and_transitions_pending')
    env={**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/search_reports_release_v1675'),
         'ROM':Path('out/all_routes_combined_v1676_candidate.nds')}
    exec(compile(source,__file__,'exec'),env);env['main']()
