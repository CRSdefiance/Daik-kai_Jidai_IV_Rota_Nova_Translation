"""Fresh fixture-free registered V1909 startup/title/New Game controls."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous

if __name__ == '__main__':
    source = inspect.getsource(previous.main).replace('duel_v1166_', 'lil_London_v1909_').replace('V1166:', 'V1909:')
    env = {**previous.__dict__, '__file__':__file__,
        'ROOT':Path('work/analysis/lil_London_release_v1908b'),
        'ROM':Path('out/all_routes_combined_v1909_candidate.nds')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()

