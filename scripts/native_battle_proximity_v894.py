"""V893-only coordinate approach using retained original native/terrain fixtures."""

import inspect
from pathlib import Path
from types import FunctionType

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import native_full_fleet_proximity_v653 as source
from scripts import native_village_contexts_v618 as terrain_source
from scripts.verify_village_wrap_v608 import read

ROM=Path('out/all_routes_combined_v893_candidate.nds')
SOURCE=Path('scripts/native_full_fleet_proximity_v653.py')
TERRAIN_SOURCE=Path('scripts/native_village_contexts_v618.py')


def apply_fixture(arm,raw,action):
    config=read('translations/battle_personal_editorial_release_v1.json')
    if sha(arm)!=config['target_arm9_sha256'] or action!='approach' or len(raw)!=0x400000:
        raise ValueError('Only pinned V893 coordinate approach is allowed;no recovery or outcome writes')
    rom=NdsImage.open(ROM);clean=NdsImage.open('work/clean.nds');clean_arm=clean.read_file('/__arm9__.bin')
    assert arm==rom.read_file('/__arm9__.bin')
    ranges=((0xCB1A8,0xCB1B4),(0x2E58C,0x2E598),(0x36914,0x36940),(0x36C70,0x36C94),
        (0x5543C,0x55454),(0xAB158,0xAB18C),(0x18398,0x183A8),(0x181B4,0x181C4),
        (0x69B5C,0x69E00),(0x3F0F8,0x3F100))
    assert all(arm[a:b]==clean_arm[a:b] for a,b in ranges)
    assert rom.read_file('/data/WORLDMAP.DK4')==clean.read_file('/data/WORLDMAP.DK4')
    assert rom.rom.arm9OverlayTable==clean.rom.arm9OverlayTable
    original=SOURCE.read_bytes();original_terrain=TERRAIN_SOURCE.read_bytes()
    text=inspect.getsource(terrain_source.terrain_queries)
    old="out/all_routes_combined_v604_candidate.nds";assert text.count(old)==1
    effective=text.replace(old,str(ROM).replace('\\','/'))
    context={**terrain_source.terrain_queries.__globals__}
    exec(compile(effective,'<V894-current-source-terrain>','exec'),context)
    delegated=FunctionType(source.apply_fixture.__code__,{**source.apply_fixture.__globals__,
        'ARM':config['target_arm9_sha256'],'REFERENCE':ROM,'terrain_queries':context['terrain_queries']})
    after,receipt=delegated(arm,raw,action)
    assert len(receipt['owned_bytes'])==8
    assert all(c['address'] in receipt['owned_bytes'] for c in receipt['changes'])
    assert receipt['no_enemy_stats_war_outcome_reward_inventory_or_resource_flags_changed']
    assert SOURCE.read_bytes()==original and TERRAIN_SOURCE.read_bytes()==original_terrain
    receipt.update(current_ROM_sha256=sha(ROM.read_bytes()),source_fixture_sha256=sha(original),
        source_terrain_sha256=sha(original_terrain),source_helpers_unchanged=True,
        explicit_successor_uses_current_ROM_instead_of_missing_historical_dependency=True,
        terrain_function_only_ROM_path_changed=True,current_native_getters_and_terrain_exact_clean=True,
        current_terrain_effective_source_sha256=sha(effective.encode('utf-8')),
        wrapper_sha256=sha(Path(__file__).read_bytes()),actual_battle_mode_not_assigned_by_fixture=True)
    return after,receipt
