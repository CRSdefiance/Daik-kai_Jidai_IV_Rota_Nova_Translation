"""Single prebattle own-position fixture near an unchanged original stronger fleet."""
import struct
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_ship_sinking_fixture_v1351 as terrain_source
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROM=Path('out/all_routes_combined_v1456_candidate.nds')
ROOT=Path('work/analysis/stronger_fleet_fixture_v1471')
BASE=0x02000000

def apply_fixture(arm,raw,request):
    assert request=={'ship_sinking_context':'five_ship_approach'} and len(raw)==0x400000
    release=read('work/analysis/ship_loss_surrender_release_v1455/registered_release_verification.json')
    assert sha(arm)==release['ARM9_sha256']
    census_path=Path('work/analysis/original_fleet_guns_v1469/original_fleet_census.json')
    census=read(census_path)
    assert census['candidate_sha256']==release['candidate_sha256']
    target=next(f for f in census['stronger_original_fleets_at_sea'] if f['fleet']==4)
    cpu,get=get_machine(arm,raw);fleets=get(0xCB1A8)
    assert list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12)))==[0,0,0]
    assert get(0x2E58C)==get(0x7F244)==1
    enemy=fleets+4+4*132
    assert get(0x35320,enemy)==target['company']==4 and get(0x34674,enemy)==115
    assert not get(0x36C70,enemy+12)
    vt=struct.unpack('<I',cpu.mem_read(enemy,4))[0]
    method=struct.unpack('<I',cpu.mem_read(vt+0x20,4))[0]
    get(method-BASE,0x02460000,enemy)
    point=list(struct.unpack('<2i',cpu.mem_read(0x02460000,8)))
    assert point==target['cached_map_point']==[20136,4343]
    candidates=[[point[0]+x,point[1]+y] for x,y in [(0,20),(20,0),(-20,0),(0,-20),(40,0),(-40,0)]]
    water=FunctionType(terrain_source.water.__code__,{**terrain_source.__dict__,'ROM':ROM})
    terrain=water(arm,candidates)
    chosen=next(r['map_point'] for r in terrain['queries'] if r['collision_free'])
    after=bytearray(raw);owned=set();ships=[]
    for slot in range(5):
        link=fleets+4+132+12+8*slot;mobile=get(0x36C70,link);model=get(0x36C94,link)
        assert mobile and model and get(0x564C8,mobile)
        hc=[get(0x5543C,mobile),get(0x55444,mobile)]
        assert hc==([60,49] if slot==0 else [25,19])
        before=list(struct.unpack('<2i',cpu.mem_read(mobile+16,8)))
        at=mobile+16;value=struct.pack('<2i',*[v*128 for v in chosen])
        after[at-BASE:at-BASE+8]=value;owned.update(range(at,at+8))
        ships.append({'slot':slot,'mobile':mobile,'model':model,'Hull_Crew':hc,
            'original_cannon_type':get(0x1856C,model),'source_fixed_point':before})
    assert len({tuple(s['source_fixed_point']) for s in ships})==1
    assert [s['original_cannon_type'] for s in ships]==[1,0,0,0,0]
    after=bytes(after)
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b]
    assert len(owned)==40 and all(c['address'] in owned for c in changes)
    return after,{'context':'existing_stronger_fleet4_location_only','owned_bytes':sorted(owned),'changes':changes,
        'own_five_original_ships':ships,'original_existing_enemy_fleet':4,'source_cached_point':point,
        'source_verified_water_point':chosen,'terrain':terrain,'source_census':str(census_path),
        'source_census_sha256':sha(census_path.read_bytes()),'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(after),
        'all_other4MiB_enemy_health_crew_equipment_actors_IDs_RNG_eligibility_and_results_exact':True,
        'relative_positions_preserved':True,'sole_prebattle_fixture_no_later_mutation_permitted':True,
        'cached_point_not_assumed_equal_to_actual_loaded_point':True,
        'no_earned_travel_or_original_event_or_completion_credit':True,
        'fixture_sha256':sha(Path(__file__).read_bytes())}

if __name__=='__main__':
    assert not ROOT.exists()
    report=read('E:/Rota Nova translations/Generated/work/emulation_v193/loss_surrender_control_v1461b_1456/capture_report.json')
    snapshot=next(r for r in report['read_only_pause_RAM_snapshots'] if r['frame']==4800)
    raw=Path(snapshot['path']).read_bytes();assert sha(raw)==snapshot['sha256']
    after,receipt=apply_fixture(NdsImage.open(ROM).read_file('/__arm9__.bin'),raw,{'ship_sinking_context':'five_ship_approach'})
    ROOT.mkdir(parents=True);save(ROOT/'prebattle_fixture_preflight.json',receipt)
    print('Fleet4 original stronger guns;only40 own position bytes proposed at',receipt['source_verified_water_point'])
