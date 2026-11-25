"""Eight ordinary no-save startup/title/New Game capture controls for V1224."""
import inspect
from pathlib import Path
from scripts import run_duel_startup_v1166 as previous


def main():
    source = inspect.getsource(previous.main).replace('duel_v1166_', 'duel_special_v1224_').replace('V1166:', 'V1224:')
    env = {**previous.__dict__, '__file__': __file__,
        'ROOT': Path('work/analysis/duel_special_release_v1223'),
        'ROM': Path('out/all_routes_combined_v1224_candidate.nds')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
