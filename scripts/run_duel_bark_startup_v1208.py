"""Use the frozen no-save startup evidence protocol for V1206."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous


def main():
    source=inspect.getsource(previous.main).replace('duel_v1166_','duel_bark_v1206_').replace('V1166:','V1206:')
    env={**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/duel_bark_release_v1205'),
        'ROM':Path('out/all_routes_combined_v1206_candidate.nds')}
    exec(compile(source,__file__,'exec'),env);env['main']()


if __name__=='__main__':main()
