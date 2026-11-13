"""One source-terrain-checked prebattle move of the existing five-ship fleet.

No health,crew,role,actor,enemy,diplomacy,RNG,eligibility or outcome edits.
All five ships retain their original relative positions and stored models.
"""
import struct
from pathlib import Path
from types import FunctionType
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_village_contexts_v618 import terrain_queries as original_terrain
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

BASE = 0x02000000
ROM = Path('out/all_routes_combined_v1344_candidate.nds')
ROOT = Path('work/analysis/ship_sinking_fixture_v1351')


def water(arm,points):
    class Current:
        @staticmethod
        def open(path):
            return NdsImage.open(ROM if path=='out/all_routes_combined_v604_candidate.nds' else path)
    return FunctionType(original_terrain.__code__,{**original_terrain.__globals__,'NdsImage':Current})(arm,points)


def apply_fixture(arm,raw,request):
    assert request=={'ship_sinking_context':'five_ship_approach'} and len(raw)==0x400000
    release = read('work/analysis/ship_sinking_release_v1343/registered_release_verification.json')
    assert sha(arm)==release['ARM9_sha256']
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in [(0x36C70,0x36CB8),(0x5543C,0x55454),(0xAB158,0xAB18C),
                  (0x69B5C,0x69E00),(0x72734,0x7288C),(0x753F0,0x75560)]:
        assert arm[lo:hi]==clean[lo:hi]
    cpu,get = get_machine(arm,raw)
    fleets = get(0xCB1A8)
    assert get(0x2E58C)==get(0x7F244)==1
    assert list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12)))==[0,0,0]
    assert all(bytes(cpu.mem_read(fleets+0x2080+4*i,1))==b'\x40' for i in [1,2,3])
    own,enemy = fleets+4+132,fleets+4+5*132
    assert get(0x35320,own)==2 and get(0x35320,enemy)==5
    assert get(0x34674,own)==get(0x34674,enemy)==115
    assert get(0x82478,fleets+0x2090,1)==16 and get(0x82478,fleets+0x2090,9)==18
    ships = []
    for slot in range(5):
        mobile,model = get(0x36C70,own+12+8*slot),get(0x36C94,own+12+8*slot)
        assert mobile and model and get(0x564C8,mobile)
        health = [get(0x5543C,mobile),get(0x55444,mobile)]
        persisted = [get(0x183A0,model),get(0x181BC,model)]
        assert health==persisted==([60,49] if slot==0 else [25,19])
        point = list(struct.unpack('<2i',cpu.mem_read(mobile+16,8)))
        ships.append({'slot':slot,'mobile':mobile,'model':model,'Hull_Crew':health,
            'source_fixed_point':point,'name':bytes(cpu.mem_read(model+8,24)).split(b'\0')[0].decode('ascii')})
    assert [s['name'] for s in ships]==['Vestaros','Latina','Latina','Latina','Latina']
    assert len({tuple(s['source_fixed_point']) for s in ships})==1
    enemy_model = get(0x36C94,enemy+12)
    assert enemy_model and not get(0x36C70,enemy+12)
    assert bytes(cpu.mem_read(enemy_model+8,24)).split(b'\0')[0]==b'Hanse Cog'
    assert [get(0x183A0,enemy_model),get(0x181BC,enemy_model)]==[30,13]
    vtable = struct.unpack('<I',cpu.mem_read(enemy,4))[0]
    method = struct.unpack('<I',cpu.mem_read(vtable+0x20,4))[0]
    get(method-BASE,0x02460000,enemy)
    point = list(struct.unpack('<2i',cpu.mem_read(0x02460000,8)))
    candidates = [[point[0]+x,point[1]+y] for x,y in [(0,20),(20,0),(-20,0),(0,-20),(40,0),(-40,0)]]
    terrain = water(arm,candidates)
    target = next(r['map_point'] for r in terrain['queries'] if r['collision_free'])
    fixed = [v*128 for v in target]
    fields = {s['mobile']+16:struct.pack('<2i',*fixed) for s in ships}
    after,owned = bytearray(raw),set()
    for address,value in fields.items():
        after[address-BASE:address-BASE+len(value)] = value
        owned.update(range(address,address+len(value)))
    after = bytes(after)
    changes = [{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b]
    assert len(owned)==40 and all(r['address'] in owned for r in changes)
    for root,length in [(get(0xCB184),0x1A04),(get(0xCB178),4+114*108),
                        (get(0xCB160),4+21*76),(fleets,4+63*132)]:
        assert raw[root-BASE:root-BASE+length]==after[root-BASE:root-BASE+length]
    for offset in [0xD9858,0x51A20]:
        address = struct.unpack_from('<I',arm,offset)[0]
        assert not owned.intersection(range(address,address+4))
        assert raw[address-BASE:address-BASE+4]==after[address-BASE:address-BASE+4]
    return after,{'context':'five_ship_approach','owned_bytes':sorted(owned),'changes':changes,
        'declared_fields':{str(k):v.hex() for k,v in fields.items()},'existing_five_ships':ships,
        'original_existing_enemy_fleet':5,'original_offscreen_enemy_model':enemy_model,'enemy_Hull_Crew_unchanged':[30,13],
        'original_enemy_position_getter':method,'original_enemy_cached_map_point':point,
        'source_verified_water_point':target,'terrain':terrain,'target_fixed_point':fixed,
        'prebattle_mode000_and_no_other_party_slots_verified':True,
        'all_five_relative_positions_preserved_and_only40_location_bytes_owned':True,
        'all_actors_IDs_roles_crew_health_stored_fleets_towns_companies_RNG_and_results_unchanged':True,
        'own_cached_fleet_position_left_for_original_next_frame_update':True,
        'no_earned_travel_or_sinking_outcome_or_translation_completion_claim':True,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(after),
        'fixture_sha256':sha(Path(__file__).read_bytes())}


if __name__=='__main__':
    assert not ROOT.exists()
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    raw = Path('E:/Rota Nova translations/Generated/work/emulation_v193/ship_sinking_v1350_1344/frame_004800_arm9_ram.bin').read_bytes()
    after,receipt = apply_fixture(arm,raw,{'ship_sinking_context':'five_ship_approach'})
    ROOT.mkdir(parents=True)
    save(ROOT/'prebattle_fixture_preflight.json',receipt)
    print(f'One prebattle move:40 owned bytes,{len(receipt["changes"])} changed;all five health/crew/roles/enemy/RNG/results exact.',flush=True)
