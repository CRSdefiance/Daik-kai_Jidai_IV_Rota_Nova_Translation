"""Read-only special scan bound to the separate ordinary timed-A run."""
from pathlib import Path
from types import FunctionType
from scripts import inspect_duel_special_capture_v1228 as previous


if __name__ == '__main__':
    env = {**previous.__dict__, '__file__': __file__,
        'ROOT': Path('work/analysis/duel_special_actual_v1234'),
        'CAP': Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_special_v1232_1224')}
    FunctionType(previous.main.__code__, env)()
