"""Preserve13 original escape pipelines using the source V1316 snapshot."""
import inspect
from pathlib import Path
from scripts import verify_battle_aftermath_escape_v1262 as previous

if __name__=='__main__':
    source = inspect.getsource(previous.main)
    for old,new in [
        ('work/analysis/battle_aftermath_payload_v1259/native_payload_plan.json','work/analysis/ship_sinking_payload_v1337/native_payload_plan.json'),
        ('work/analysis/battle_aftermath_context_v1248d/source_context_and_consumer_frames.json','work/analysis/ship_sinking_context_v1325/source_and_consumer_binding.json')]:
        assert source.count(old)==1
        source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/ship_sinking_escape_v1340')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
