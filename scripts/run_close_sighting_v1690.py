"""Original regional-donor cold boot;pause before a live-fleet8 close test."""
import inspect
from pathlib import Path
from scripts import run_sighting_incoming_v1109 as previous
from scripts.native_close_sighting_v1689 import apply_fixture,ROM

if __name__=='__main__':
    source=inspect.getsource(previous.main)
    for old,new in [("choices=('compassAttack8',)","choices=('closeReady8',)"),
                    ('work/analysis/sighting_incoming_v1109_','work/analysis/close_sighting_v1690_'),
                    ('sighting_incoming_v1109_1105_','close_sighting_v1690_1676_'),
                    ('scripts/native_sighting_context_v1109.py','scripts/native_close_sighting_v1689.py')]:
        assert old in source,old;source=source.replace(old,new)
    lo=source.index('    commands += [');hi=source.index("    journal=root/'navigation.jsonl'",lo)
    source=source[:lo]+source[hi:]
    env={**previous.__dict__,'__file__':__file__,'ROM':ROM,'apply_fixture':apply_fixture}
    exec(compile(source,__file__,'exec'),env);env['main']()
