"""Original warm/cold complete copies in the Palace repacked blocks."""
from pathlib import Path
from types import FunctionType
from dk4tool.patch.palace_editorial import ROOT
from scripts import verify_schemes_copies_v776 as original

if __name__=='__main__':
    FunctionType(original.main.__code__,{**original.__dict__,'SOURCE':ROOT,'ROOT':ROOT/'native_copies',
        '__file__':str(Path(__file__).resolve())})()
