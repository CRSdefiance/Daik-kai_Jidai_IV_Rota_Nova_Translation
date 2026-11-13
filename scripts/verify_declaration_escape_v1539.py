"""Earlier13 direct escape pipelines retain exact output after the NPC table addition."""
import inspect
from pathlib import Path
from scripts import verify_battle_aftermath_escape_v1262 as previous
from scripts.verify_village_wrap_v608 import read

if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    old = 'work/analysis/battle_aftermath_payload_v1259/native_payload_plan.json'
    assert source.count(old) == 1
    source = source.replace(old, 'work/analysis/declaration_responses_payload_v1535b/native_payload_plan.json')
    context = read('work/analysis/declaration_responses_context_v1531/source_and_original_actor_context.json')
    old = "context = read('work/analysis/battle_aftermath_context_v1248d/source_context_and_consumer_frames.json')"
    assert source.count(old) == 1
    source = source.replace(old, 'context = ' + repr({k: context[k] for k in ['snapshot', 'snapshot_sha256']}))
    env = {**previous.__dict__, '__file__': __file__, 'ROOT': Path('work/analysis/declaration_responses_escape_v1539')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
