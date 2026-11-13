"""Use the frozen ordinary startup capture and comparison protocol for V1189."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous


def main():
    source=inspect.getsource(previous.main).replace('duel_v1166_','escape_direct_v1189_').replace('V1166:','V1189:')
    env={**previous.__dict__,'__file__':__file__,
         'ROOT':Path('work/analysis/escape_direct_release_v1188'),'ROM':Path('out/all_routes_combined_v1189_candidate.nds')}
    exec(compile(source,__file__,'exec'),env);env['main']()


if __name__=='__main__':main()
