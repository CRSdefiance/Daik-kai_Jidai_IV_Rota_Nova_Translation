"""Scope the ship prerequisite survey to unmodified model getters.

The predecessor included a larger AI span with existing localized callers and
stopped before writing its result. It receives no source-equality or test credit.
"""
import inspect
from pathlib import Path
from scripts import research_town_artillery_v1296 as previous

if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    old = '(0xAB8A0,0xAB940),(0x70400,0x705F8)'
    assert source.count(old) == 1
    source = source.replace(old,'(0xAB8A0,0xAB940)')
    source = source.replace('source_model_getters_and_AI_code_equal_clean','source_model_getters_equal_clean')
    env = {**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/town_artillery_v1296b')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
