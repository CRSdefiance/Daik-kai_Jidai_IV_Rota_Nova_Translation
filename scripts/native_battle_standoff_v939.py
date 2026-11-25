"""Declared100-unit coordinate approach;native combat state and outcomes unchanged."""

import inspect
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import native_full_fleet_proximity_v653 as source
from scripts import native_village_contexts_v618 as terrain_source
from scripts.verify_village_wrap_v608 import read

ROM=Path('out/all_routes_combined_v938_candidate.nds')


def apply_fixture(arm,raw,action):
    config=read('translations/battle_survey_lookout_editorial_release_v1.json')
    if sha(arm)!=config['target_arm9_sha256'] or action!='approach' or len(raw)!=0x400000:
        raise ValueError('Only pinned V938 declared stand-off coordinate approach is allowed')
    clean=NdsImage.open('work/clean.nds');clean_arm=clean.read_file('/__arm9__.bin');rom=NdsImage.open(ROM)
    assert arm==rom.read_file('/__arm9__.bin')
    for a,b in ((0xCB1A8,0xCB1B4),(0x2E58C,0x2E598),(0x36914,0x36940),(0x36C70,0x36C94),
        (0x5543C,0x55454),(0xAB158,0xAB18C),(0x18398,0x183A8),(0x181B4,0x181C4),(0x69B5C,0x69E00),(0x3F0F8,0x3F100)):
        assert arm[a:b]==clean_arm[a:b]
    assert rom.read_file('/data/WORLDMAP.DK4')==clean.read_file('/data/WORLDMAP.DK4')
    assert rom.rom.arm9OverlayTable==clean.rom.arm9OverlayTable
    source_path=Path('scripts/native_full_fleet_proximity_v653.py');before=source_path.read_bytes()
    terrain_path=Path('scripts/native_village_contexts_v618.py');terrain_before=terrain_path.read_bytes()
    terrain=inspect.getsource(terrain_source.terrain_queries)
    old='out/all_routes_combined_v604_candidate.nds';assert terrain.count(old)==1
    terrain=terrain.replace(old,str(ROM).replace('\\','/'));context={**terrain_source.terrain_queries.__globals__}
    exec(compile(terrain,'<V939-current-terrain>','exec'),context)
    text=inspect.getsource(source.apply_fixture)
    old='((0, 20), (20, 0), (-20, 0), (0, -20), (16, 16), (-16, 16))'
    new='((0, 100), (100, 0), (-100, 0), (0, -100), (80, 80), (-80, 80))'
    assert text.count(old)==1;effective=text.replace(old,new)
    environment={**source.apply_fixture.__globals__,'ARM':config['target_arm9_sha256'],'REFERENCE':ROM,'terrain_queries':context['terrain_queries']}
    exec(compile(effective,'<V939-declared-coordinate-candidates>','exec'),environment)
    after,receipt=environment['apply_fixture'](arm,raw,action)
    assert len(receipt['owned_bytes'])==8 and all(c['address'] in receipt['owned_bytes'] for c in receipt['changes'])
    assert receipt['no_enemy_stats_war_outcome_reward_inventory_or_resource_flags_changed']
    assert source_path.read_bytes()==before and terrain_path.read_bytes()==terrain_before
    receipt.update(declared_coordinate_candidates=[[0,100],[100,0],[-100,0],[0,-100],[80,80],[-80,80]],
        purpose='Observe original manual naval combat before immediate boarding;no battle mode or result injection.',
        source_fixture_sha256=sha(before),source_terrain_sha256=sha(terrain_before),
        effective_coordinate_source_sha256=sha(effective.encode('utf-8')),
        current_native_and_terrain_code_exact_clean=True,source_helpers_unchanged=True,
        wrapper_sha256=sha(Path(__file__).read_bytes()),actual_battle_mode_not_assigned_by_fixture=True)
    return after,receipt
