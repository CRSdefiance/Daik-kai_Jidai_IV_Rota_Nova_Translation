"""Fixture-free startup controls for registered primary-town V2097."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous
if __name__=='__main__':
 source=inspect.getsource(previous.main).replace('duel_v1166_','primary_town_v2097_').replace('V1166:','V2097:')
 env={**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/town_services_release_v2099'),'ROM':Path('out/all_routes_combined_v2097_candidate.nds')}
 exec(compile(source,__file__,'exec'),env);env['main']()
