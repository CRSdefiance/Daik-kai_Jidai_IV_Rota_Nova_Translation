"""Fixture-free startup controls for registered Square V2143."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous
if __name__=='__main__':
 source=inspect.getsource(previous.main).replace('duel_v1166_','square_v2143_').replace('V1166:','V2143:')
 env={**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/square_release_v2145'),'ROM':Path('out/all_routes_combined_v2143_candidate.nds')}
 exec(compile(source,__file__,'exec'),env);env['main']()
