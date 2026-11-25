"""Cold-load the preserved regional donor in V1775;pause before close follow."""
import inspect
from scripts import run_sighting_incoming_v1109 as previous
from scripts.native_close_follow_v1781 import apply_fixture,ROM

if __name__=='__main__':
    source=inspect.getsource(previous.main)
    replacements=[("choices=('compassAttack8',)","choices=('openWaterReady8',)"),
        ('work/analysis/sighting_incoming_v1109_','work/analysis/close_follow_v1782_'),
        ('sighting_incoming_v1109_1105_','close_follow_v1782_1775_'),
        ('scripts/native_sighting_context_v1109.py','scripts/native_close_follow_v1781.py')]
    for old,new in replacements:
        assert old in source;source=source.replace(old,new)
    lo=source.index('    commands += [');hi=source.index("    journal=root/'navigation.jsonl'",lo)
    source=source[:lo]+source[hi:]
    env={**previous.__dict__,'__file__':__file__,'ROM':ROM,'apply_fixture':apply_fixture}
    exec(compile(source,__file__,'exec'),env);env['main']()
