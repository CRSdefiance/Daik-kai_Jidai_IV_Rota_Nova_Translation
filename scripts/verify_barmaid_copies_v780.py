"""Full warm/cold original message-copy verification against the new research bytes."""

from pathlib import Path
from types import FunctionType

from scripts import verify_schemes_copies_v776 as original
from scripts.prepare_barmaid_common_v780 import ROOT


if __name__ == '__main__':
    FunctionType(original.main.__code__, {**original.__dict__, 'SOURCE': ROOT,
                                         'ROOT': ROOT/'native_copies', '__file__': str(Path(__file__).resolve())})()
