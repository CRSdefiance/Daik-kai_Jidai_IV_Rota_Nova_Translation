"""Run the qualified native page checker on Rafael B201–B220."""
from types import FunctionType

from scripts import check_rafael_B166_B167_ordinary_v1 as native
from scripts.plan_rafael_B201_B220_v1 import IDENTITY


if __name__ == '__main__':
    FunctionType(native.env['main'].__code__, {**native.env, 'IDENTITY':IDENTITY, '__file__':__file__})()

