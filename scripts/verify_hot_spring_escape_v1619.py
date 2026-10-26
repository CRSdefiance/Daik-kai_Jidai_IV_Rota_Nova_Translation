"""Preserve all13 prior direct escape formats through the rebased native gate."""
import inspect
from pathlib import Path
from scripts import verify_battle_aftermath_escape_v1262 as previous
from scripts.verify_village_wrap_v608 import read
if __name__=='__main__':
    source=inspect.getsource(previous.main)
    old='work/analysis/battle_aftermath_payload_v1259/native_payload_plan.json';assert source.count(old)==1
    source=source.replace(old,'work/analysis/hot_spring_payload_v1615/native_payload_plan.json')
    context=read('work/analysis/hot_spring_source_v1610/original_hot_spring13_source_context.json')
    old="context = read('work/analysis/battle_aftermath_context_v1248d/source_context_and_consumer_frames.json')";assert source.count(old)==1
    source=source.replace(old,'context = '+repr({k:context[k] for k in ['snapshot','snapshot_sha256']}))
    env={**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/hot_spring_escape_v1619')}
    exec(compile(source,__file__,'exec'),env);env['main']()
