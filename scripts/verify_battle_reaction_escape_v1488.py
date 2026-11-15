"""Earlier13 original direct escape pipelines on exact current V1456 RAM."""
import inspect
from pathlib import Path
from scripts import verify_battle_aftermath_escape_v1262 as previous
from scripts.verify_village_wrap_v608 import read

if __name__=='__main__':
    source=inspect.getsource(previous.main)
    old='work/analysis/battle_aftermath_payload_v1259/native_payload_plan.json'
    assert source.count(old)==1
    source=source.replace(old,'work/analysis/battle_reaction_payload_v1484/native_payload_plan.json')
    context=read('work/analysis/battle_reactions_context_v1479/source_and_original_reaction_context.json')
    old="context = read('work/analysis/battle_aftermath_context_v1248d/source_context_and_consumer_frames.json')"
    assert source.count(old)==1
    source=source.replace(old,'context = '+repr({'snapshot':context['snapshot']['path'],'snapshot_sha256':context['snapshot']['sha256']}))
    env={**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/battle_reaction_escape_v1488')}
    exec(compile(source,__file__,'exec'),env);env['main']()
