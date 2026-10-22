"""Retain all thirteen approved direct escape paths on exact V1364 RAM."""
import inspect
from pathlib import Path
from scripts import verify_battle_aftermath_escape_v1262 as previous
from scripts.verify_village_wrap_v608 import read


if __name__=='__main__':
    source = inspect.getsource(previous.main)
    old = 'work/analysis/battle_aftermath_payload_v1259/native_payload_plan.json'
    assert source.count(old)==1
    source = source.replace(old,'work/analysis/battle_victory_payload_v1396/native_payload_plan.json')
    context = read('work/analysis/battle_victory_context_v1392b/source_and_original_victory_context.json')['prior_actual_2131']
    old = "context = read('work/analysis/battle_aftermath_context_v1248d/source_context_and_consumer_frames.json')"
    assert source.count(old)==1
    source = source.replace(old,'context = '+repr({'snapshot':context['snapshot'],'snapshot_sha256':context['snapshot_sha256']}))
    env = {**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/battle_victory_escape_v1400')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
