"""Bind the read-only original-state inspector to the stationary town test."""
from pathlib import Path
from types import FunctionType
from scripts import inspect_aftermath_town_v1292 as previous

if __name__ == '__main__':
    main = FunctionType(previous.main.__code__, {**previous.__dict__,'__file__':__file__,
        'CAP':Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_hold_v1297_1266')})
    main()
