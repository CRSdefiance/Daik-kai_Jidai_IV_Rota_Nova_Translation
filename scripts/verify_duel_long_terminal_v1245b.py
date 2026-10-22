"""Successor binds victory to observed frame8622;8502 still had4 enemy HP.

The first verifier passed31 fixture/identity/RNG/input and six special-hold
checks, then correctly rejected its premature HP-zero expectation. No output
proof or guide directory had been written. No captured state is changed.
"""
import inspect
from pathlib import Path
from scripts import verify_duel_long_terminal_v1245 as previous


if __name__=='__main__':
    source=inspect.getsource(previous.main)
    replacements={
        '(8502,[87,0])':'(8502,[87,4]),(8622,[87,0])',
        "(8502,'original natural duel victory')":"(8622,'original natural duel victory')",
    }
    for old,new in replacements.items():
        assert source.count(old)==1;source=source.replace(old,new)
    env={**previous.__dict__,'__file__':__file__,
         'ROOT':Path('work/analysis/duel_long_terminal_v1245b')}
    exec(compile(source,__file__,'exec'),env);env['main']()
