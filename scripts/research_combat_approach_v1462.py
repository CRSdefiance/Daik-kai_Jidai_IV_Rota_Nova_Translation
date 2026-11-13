"""Read-only original terrain census near the existing Speyer encounter."""
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_ship_sinking_fixture_v1351 as previous
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/combat_approach_v1462')
ROM = Path('out/all_routes_combined_v1456_candidate.nds')

if __name__=='__main__':
    assert not ROOT.exists()
    release = read('work/analysis/ship_loss_surrender_release_v1455/registered_release_verification.json')
    assert sha(ROM.read_bytes())==release['candidate_sha256']
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    water = FunctionType(previous.water.__code__,{**previous.__dict__,'ROM':ROM})
    origin = [21176,3416]
    offsets = [(x,y) for y in [-200,-160,-120,-100,-80,-40,0,80,120,160,200] for x in [-400,-300,-200,-160,-120,-100,-80,-40,0,80,160]]
    points = [[origin[0]+x,origin[1]+y] for x,y in offsets]
    result = water(arm,points)
    for row,(x,y) in zip(result['queries'],offsets,strict=True):
        row['offset_from_original_loaded_enemy'] = [x,y]
    ROOT.mkdir(parents=True)
    save(ROOT/'original_terrain_approach_census.json',{'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],
        'source_existing_enemy_actual_point':origin,'original_terrain':result,
        'source_actual_position_evidence':'work/analysis/ship_sinking_fixture_v1352/prebattle_fixture_preflight.json',
        'no_RAM_ROM_location_or_event_mutation':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Offset columns',[-400,-300,-200,-160,-120,-100,-80,-40,0,80,160])
    for y in [-200,-160,-120,-100,-80,-40,0,80,120,160,200]:
        print('y',y, ''.join('.' if r['collision_free'] else '#' for r in result['queries'] if r['offset_from_original_loaded_enemy'][1]==y))
    print('121 original collision queries saved;no location or outcome edited.',flush=True)
