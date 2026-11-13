"""Fixture-free startup controls for registered Sharedtown V2171."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous
if __name__=='__main__':
 source=inspect.getsource(previous.main).replace('duel_v1166_','town_trade_port_v2171_').replace('V1166:','V2171:')
 env={**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/town_trade_port_release_v2172'),'ROM':Path('out/all_routes_combined_v2171_candidate.nds')}
 exec(compile(source,__file__,'exec'),env);env['main']()
