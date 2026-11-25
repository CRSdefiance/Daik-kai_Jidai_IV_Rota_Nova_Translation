"""Successor recognizes the existing, hash-locked54160 formatter branch.

V1248's broad clean-code check included that previously registered branch and
failed before any output. All other source instructions remain exact; the
specific existing branch is checked explicitly, not silently ignored.
"""
import inspect
from pathlib import Path
from scripts import research_battle_aftermath_context_v1248 as previous


if __name__=='__main__':
    source=inspect.getsource(previous.main)
    old='((0x53D44,0x54170),(0x71968,0x71A40)'
    assert source.count(old)==1
    source=source.replace(old,'((0x53D44,0x54160),(0x54164,0x54170),(0x71968,0x71A40)')
    old='assert arm[lo:hi]==source[lo:hi]'
    assert source.count(old)==1
    source=source.replace(old,old+"\n    assert arm[0x54160:0x54164].hex()=='75a3feeb' and source[0x54160:0x54164].hex()=='ebfdffeb'")
    env={**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/battle_aftermath_context_v1248b')}
    exec(compile(source,__file__,'exec'),env);env['main']()
