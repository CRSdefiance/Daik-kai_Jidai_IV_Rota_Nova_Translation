"""Complete native warm/cold selection copies for all 3668 research messages."""

from pathlib import Path
from types import FunctionType

from scripts import verify_schemes_copies_v776 as original
from scripts.prepare_item_common_v788 import ROOT


if __name__ == '__main__':
    FunctionType(original.main.__code__, {**original.__dict__, 'SOURCE': ROOT,
        'ROOT': ROOT/'native_copies', '__file__': str(Path(__file__).resolve())})()
