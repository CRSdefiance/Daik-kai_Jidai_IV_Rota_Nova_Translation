"""Original warm/cold message copies for the complete shared research bank."""

from pathlib import Path
from types import FunctionType

from scripts import verify_schemes_copies_v776 as original

ROOT = Path('work/analysis/shared_integration_v782')


if __name__ == '__main__':
    FunctionType(original.main.__code__, {**original.__dict__, 'SOURCE': ROOT,
                                         'ROOT': ROOT/'native_copies', '__file__': str(Path(__file__).resolve())})()
