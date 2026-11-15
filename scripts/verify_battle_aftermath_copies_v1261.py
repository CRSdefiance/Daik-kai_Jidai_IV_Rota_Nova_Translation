"""All7336 native copies and180 cache sequences after aftermath repacking."""
import inspect
from pathlib import Path
from dk4tool.patch.duel_editorial import owned_entries, COMPONENT_SHA
from scripts import verify_duel_cache_copies_v1163 as previous


if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    replacements = {
        'work/analysis/duel_native_release_v1162/final_payload_plan.json':
        'work/analysis/battle_aftermath_payload_v1259/native_payload_plan.json',
        "prefix = plan['new_code_prefix']":
        "prefix = {'block':21,'component_bytes':1480,'component_sha256':COMPONENT_SHA}",
    }
    for old,new in replacements.items():
        assert source.count(old) == 1
        source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,'entries':owned_entries,'COMPONENT_SHA':COMPONENT_SHA,
        'ROOT':Path('work/analysis/battle_aftermath_copies_v1261')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
