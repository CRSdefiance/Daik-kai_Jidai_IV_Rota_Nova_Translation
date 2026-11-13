"""One45-byte prebattle own-position/Carronade fixture;enemy and health unchanged."""
import struct
from pathlib import Path
from types import FunctionType
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import native_ship_sinking_fixture_v1351 as original
from scripts.native_loss_surrender_fixture_v1460 import apply_fixture as baseline,ROM
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/combat_approach_fixture_v1463')
BASE = 0x02000000

def apply_fixture(arm,raw,request):
    assert request=={'ship_sinking_context':'five_ship_approach'}
    after,parent = baseline(arm,raw,request)
    terrain_path = Path('work/analysis/combat_approach_v1462/original_terrain_approach_census.json')
    terrain = read(terrain_path)
    assert terrain['candidate_sha256']==sha(ROM.read_bytes())
    assert parent['prior_actual_loaded_enemy_map_point']==terrain['source_existing_enemy_actual_point']==[21176,3416]
    chosen = next(r for r in terrain['original_terrain']['queries'] if r['offset_from_original_loaded_enemy']==[-200,120])
    assert chosen['collision_free'] and chosen['map_point']==[20976,3536]
    water = FunctionType(original.water.__code__,{**original.__dict__,'ROM':ROM})
    current_terrain = water(arm,[chosen['map_point']])
    assert current_terrain['queries'][0]['collision_free']
    assert current_terrain['WORLDMAP_sha256']==terrain['original_terrain']['WORLDMAP_sha256']
    cpu,get = get_machine(arm,after);fleets = get(0xCB1A8)
    assert list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12)))==[0,0,0]
    assert get(0xAB784,5)==5 and get(0x48144,5)==224 and get(0xAB784,7)==0
    census_path = Path('work/analysis/ship_cannon_setup_v1377/source_cannon_setup.json');census = read(census_path)
    result,owned,items,positions = bytearray(after),set(parent['owned_bytes']),[],[]
    fixed = [v*128 for v in chosen['map_point']]
    for expected,kind in zip(census['actual_prebattle_five_ship_cannons'],[5,7,7,7,7],strict=True):
        slot = expected['slot'];link = fleets+4+132+12+8*slot
        mobile,model = get(0x36C70,link),get(0x36C94,link)
        assert mobile==expected['mobile'] and model==expected['model']
        assert [get(0x5543C,mobile),get(0x55444,mobile)]==expected['actual_Hull_Crew']
        assert get(0xAB71C,mobile)==expected['native_battery_multiplier']
        field = model+0x4A;old = get(0x1856C,model)
        assert old==result[field-BASE]==expected['current_cannon_type']
        result[field-BASE] = kind;owned.add(field)
        value = struct.pack('<2i',*fixed);at = mobile+16
        assert set(range(at,at+8))<=owned
        result[at-BASE:at-BASE+8] = value
        positions.append({'slot':slot,'mobile':mobile,'point_before':expected.get('source_fixed_point'),
            'original_location_fixture_point':parent['source_verified_water_point'],'after_fixed_point':fixed})
        items.append({'slot':slot,'model':model,'field':field,'before':old,'after':kind,
            'native_strength_after':get(0xAB784,kind),'equipment':'original Carronade' if kind==5 else 'original NoGun type7'})
    result = bytes(result)
    changes = [{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,result,strict=True)) if a!=b]
    assert len(owned)==45 and all(c['address'] in owned for c in changes)
    assert {BASE+i for i,(a,b) in enumerate(zip(after,result,strict=True)) if a!=b}<=owned
    return result,{'context':'five_ship_southwest_approach_original_Carronade_escort_NoGun',
        'owned_bytes':sorted(owned),'changes':changes,'cannon_equipment':items,'positions':positions,
        'source_verified_water_point':chosen['map_point'],'source_fixed_point':fixed,'terrain':current_terrain,
        'source_terrain_census':str(terrain_path),'source_terrain_census_sha256':sha(terrain_path.read_bytes()),
        'source_cannon_census':str(census_path),'source_cannon_census_sha256':sha(census_path.read_bytes()),
        'baseline_location_receipt':parent,'baseline_point_is_intermediate_CPU_construction_not_separate_live_fixture':True,
        'only40_own_live_position_bytes_and5_original_cannon_type_bytes_owned':True,
        'all_other4MiB_including_health_crew_actors_IDs_RNG_enemy_and_results_exact':True,
        'five_original_ships_relative_positions_preserved':True,'prebattle_only_no_later_fixture_permitted':True,
        'actual_NoGun_suppression_cannon_damage_surrender_and_sinking_must_be_observed_not_assumed':True,
        'not_earned_travel_or_equipment_purchase_or_original_event_completion':True,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(result),'fixture_sha256':sha(Path(__file__).read_bytes())}

if __name__=='__main__':
    assert not ROOT.exists()
    cap = Path('E:/Rota Nova translations/Generated/work/emulation_v193/loss_surrender_control_v1461b_1456')
    report = read(cap/'capture_report.json');assert report['ROM_sha256']==sha(ROM.read_bytes())
    snapshot = next(r for r in report['read_only_pause_RAM_snapshots'] if r['frame']==4800)
    raw = Path(snapshot['path']).read_bytes();assert sha(raw)==snapshot['sha256']
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    after,receipt = apply_fixture(arm,raw,{'ship_sinking_context':'five_ship_approach'})
    ROOT.mkdir(parents=True);save(ROOT/'prebattle_fixture_preflight.json',receipt)
    print('Southwest clear-water approach [20976,3536] +original Carronade/NoGun:45 owned bytes;all health,crew,enemy,RNG/results exact.',flush=True)
