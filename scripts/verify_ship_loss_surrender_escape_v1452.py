"""Earlier direct escape pipelines on exact V1430 source RAM after the24-report repair."""
import inspect
from pathlib import Path
from scripts import verify_battle_aftermath_escape_v1262 as previous
from scripts.verify_village_wrap_v608 import read

if __name__=='__main__':
    source = inspect.getsource(previous.main)
    old = 'work/analysis/battle_aftermath_payload_v1259/native_payload_plan.json'
    assert source.count(old)==1
    source = source.replace(old,'work/analysis/ship_loss_surrender_payload_v1447/native_payload_plan.json')
    context = read('work/analysis/ship_loss_surrender_context_v1439/source_and_original_loss_surrender_context.json')
    old = "context = read('work/analysis/battle_aftermath_context_v1248d/source_context_and_consumer_frames.json')"
    assert source.count(old)==1
    source = source.replace(old,'context = '+repr({'snapshot':context['snapshot'],'snapshot_sha256':context['snapshot_sha256']}))
    env = {**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/ship_loss_surrender_escape_v1452')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
