"""Fixture-free V1807 registered startup/title/New Game controls."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous

if __name__=='__main__':
    source=inspect.getsource(previous.main).replace('duel_v1166_','reinforcement_faction_v1807_').replace('V1166:','V1807:')
    env={**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/reinforcement_faction_release_v1805'),'ROM':Path('out/all_routes_combined_v1807_candidate.nds')}
    exec(compile(source,__file__,'exec'),env);env['main']()
