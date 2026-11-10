"""Run the qualified native page and macro checks for Rafael B241–B260."""
from types import FunctionType

from scripts import check_rafael_B166_B167_ordinary_v1 as native
from scripts.write_rafael_B241_B260_contextual_v1 import ROOT


if __name__ == '__main__':
    FunctionType(native.env['main'].__code__, {
        **native.env, 'IDENTITY': ROOT / 'scoped_runtime_v1.json', '__file__': __file__,
    })()
