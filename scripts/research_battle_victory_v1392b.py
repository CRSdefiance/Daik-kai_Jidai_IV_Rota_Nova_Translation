"""Correct the source probe's assumption about the original leading font cell.

V1392 stopped before writing evidence. The unchanged original formatter emits
one leading space for this legacy selector;assert that exact captured byte.
"""
import inspect
from pathlib import Path
from scripts import research_battle_victory_v1392 as previous


if __name__=='__main__':
    source = inspect.getsource(previous.main)
    old = "    assert formatted==en[2131].text==b'Admiral, victory is ours!'"
    new = "    assert en[2131].text==b'Admiral, victory is ours!'\n    assert formatted==b' '+en[2131].text"
    assert source.count(old)==1
    source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/battle_victory_context_v1392b')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
