"""Fixture-free title menu cold boot for registered V2284."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous
if __name__=='__main__':
 source=inspect.getsource(previous.main).replace('duel_v1166_','refit_spritsail_v2289_').replace('V1166:','V2284:')
 env={**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/refit_spritsail_runs_v2287'),'ROM':Path('out/all_routes_combined_v2284_candidate.nds')}
 exec(compile(source,__file__,'exec'),env);env['main']()
