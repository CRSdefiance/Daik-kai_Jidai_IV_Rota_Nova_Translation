"""Read-only full native/RGB special scan for the predeclared timing cases."""
import argparse
import sys
from pathlib import Path
from types import FunctionType
from scripts import inspect_duel_special_capture_v1228 as previous


if __name__=='__main__':
    p=argparse.ArgumentParser(add_help=False)
    p.add_argument('--period',type=int,choices=(37,53,71),required=True)
    args,rest=p.parse_known_args()
    sys.argv=[__file__,*rest]
    env={**previous.__dict__,'__file__':__file__,
        'ROOT':Path(f'work/analysis/duel_special_actual_v1236_p{args.period}'),
        'CAP':Path(f'E:/Rota Nova translations/Generated/work/emulation_v193/duel_special_v1235_1224_p{args.period}')}
    FunctionType(previous.main.__code__,env)()
