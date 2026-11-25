"""Reuse complete native copy verification against the exact new research bytes."""

from pathlib import Path
from types import FunctionType

from scripts import verify_schemes_copies_v776 as original
from scripts.prepare_followup_common_v778 import ROOT


if __name__ == '__main__':
    run = FunctionType(original.main.__code__, {**original.__dict__, 'SOURCE': ROOT,
                                               'ROOT': ROOT/'native_copies', '__file__': str(Path(__file__).resolve())})
    run()
