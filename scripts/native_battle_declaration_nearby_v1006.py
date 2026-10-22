"""Declared30-unit approach within original655B8 radius32; original modal entry freezes sailing."""
import inspect
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_full_fleet_proximity_v653 as source
from scripts import native_village_contexts_v618 as terrain_source
from scripts.native_battle_declaration_context_v1000b import assign as context
from scripts.native_battle_declaration_standoff_v999 import apply_fixture as standoff, ROM
from scripts.verify_village_wrap_v608 import read


def dispatch_fixture(arm,raw,request):
    if request=='approach':return standoff(arm,raw,request)
    assert isinstance(request,dict) and set(request)=={'declaration_context'}
    action=request['declaration_context']
    if action!='approach30':return context(arm,raw,action)
    cfg=read('translations/battle_declaration_editorial_release_v1.json')
    assert sha(arm)==cfg['target_arm9_sha256']
    terrain=inspect.getsource(terrain_source.terrain_queries)
    old='out/all_routes_combined_v604_candidate.nds';assert terrain.count(old)==1
    terrain=terrain.replace(old,str(ROM).replace('\\','/'))
    scope=dict(terrain_source.terrain_queries.__globals__)
    exec(compile(terrain,'<V1006-current-original-terrain>','exec'),scope)
    body=inspect.getsource(source.apply_fixture)
    old='((0, 20), (20, 0), (-20, 0), (0, -20), (16, 16), (-16, 16))'
    new='((0, 30), (30, 0), (-30, 0), (0, -30), (24, 24), (-24, 24))'
    assert body.count(old)==1;body=body.replace(old,new)
    env={**source.apply_fixture.__globals__,'ARM':cfg['target_arm9_sha256'],
         'REFERENCE':ROM,'terrain_queries':scope['terrain_queries']}
    exec(compile(body,'<V1006-declared-60-unit-candidates>','exec'),env)
    after,proof=env['apply_fixture'](arm,raw,'approach')
    assert len(proof['owned_bytes'])==8
    proof.update(declaration_context=action,declared_coordinate_candidates=[[0,30],[30,0],[-30,0],[0,-30],[24,24],[-24,24]],
        no_renderer_message_selection_or_outcome_injection=True,
        fixture_successor_sha256=sha(Path(__file__).read_bytes()),
        original_proximity_sha256=sha(Path(source.__file__).read_bytes()),
        original_terrain_sha256=sha(Path(terrain_source.__file__).read_bytes()))
    return after,proof
