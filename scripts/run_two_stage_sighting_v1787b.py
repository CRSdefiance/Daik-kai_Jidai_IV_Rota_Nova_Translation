"""Fresh cold-load for the source-derived wider-band then close approach."""
import inspect
from scripts import run_sighting_incoming_v1109 as previous
from scripts.native_two_stage_sighting_v1786b import apply_fixture,ROM

if __name__=='__main__':
    source=inspect.getsource(previous.main)
    for old,new in [("choices=('compassAttack8',)","choices=('twoStageReady8',)"),
        ('work/analysis/sighting_incoming_v1109_','work/analysis/two_stage_sighting_v1787_'),
        ('sighting_incoming_v1109_1105_','two_stage_sighting_v1787_1775_'),
        ('scripts/native_sighting_context_v1109.py','scripts/native_two_stage_sighting_v1786b.py')]:
        assert old in source;source=source.replace(old,new)
    lo=source.index('    commands += [');hi=source.index("    journal=root/'navigation.jsonl'",lo);source=source[:lo]+source[hi:]
    env={**previous.__dict__,'__file__':__file__,'ROM':ROM,'apply_fixture':apply_fixture}
    exec(compile(source,__file__,'exec'),env);env['main']()
