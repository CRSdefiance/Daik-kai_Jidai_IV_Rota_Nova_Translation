"""Amsterdam approach and original pre-battle diplomacy prerequisite only."""
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_aftermath_battle_fixture_v1269 import ROM,water
from scripts.verify_personal_gameplay_v841 import get_machine,rtti
from scripts.verify_village_wrap_v608 import read

BASE = 0x02000000


def apply_fixture(arm,raw,request):
    assert request == {'city_context':'Amsterdam'} and len(raw) == 0x400000
    assert sha(arm) == read('translations/battle_aftermath_editorial_release_v1.json')['target_arm9_sha256']
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = ((0x34674,0x34688),(0x36C70,0x36C94),(0xCD6B8,0xCD6CC),
        (0x3C8F4,0x3CB30),(0x3CB30,0x3CBF0),(0x6ED34,0x6EE90),(0x519D4,0x51A28))
    assert all(arm[a:b] == clean[a:b] and raw[a:b] == arm[a:b] for a,b in spans)
    cpu,get = get_machine(arm,raw)
    assert get(0x7F244) == get(0x2E58C) == 1
    mode = get(0x3F0F8)
    assert list(struct.unpack('<2I',cpu.mem_read(mode+8,8))) == [0,0]
    fleets,companies,towns,actors = (get(fn) for fn in (0xCB1A8,0xCB160,0xCB178,0xCB184))
    own,defender = fleets+4+132,fleets+4+2*132
    assert get(0x34674,own) == 115,'Depart normally before an isolated location fixture'
    assert get(0x35320,own) == 2 and get(0x35320,defender) == 1
    assert get(0x34674,defender) == 2
    assert get(0x7EE08,get(0x3697C,defender)) == 2
    mobile = get(0x36C70,own+12)
    assert mobile and get(0x564C8,mobile) and get(0x5543C,mobile) > 0 and get(0x55444,mobile) > 0
    town = towns+4+2*108
    vt = struct.unpack('<I',cpu.mem_read(town,4))[0]
    assert rtti(raw,vt) == '5CTown' and get(0xB4AA8,town,1) > 0
    port = get(0xCD6B8,2)
    point = list(struct.unpack('<2i',cpu.mem_read(port+12,8)))
    candidates = [[point[0]+x,point[1]+y] for x,y in ((0,-60),(-60,0),(60,0),(0,60),(0,-40),(-40,0),(40,0),(0,40))]
    terrain = water(arm,candidates)
    water_point = next(r['map_point'] for r in terrain['queries'] if r['collision_free'])
    relation_before = get(0x3CB30,companies+4+76,2)
    get(0x3C8F4,companies+4+76,2,2,21)
    assert get(0x3CB30,companies+4+76,2) == 2
    after = bytearray(cpu.mem_read(BASE,0x400000))
    struct.pack_into('<2i',after,mobile+16-BASE,*[v*128 for v in water_point])
    owned = set(range(mobile+16,mobile+24)) | {companies+4+2*76+0x1F+1,companies+4+76+0x1F+2}
    changes = [{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a != b]
    assert all(c['address'] in owned for c in changes),changes
    assert after[defender-BASE:defender-BASE+132] == raw[defender-BASE:defender-BASE+132]
    assert after[towns-BASE:towns-BASE+4+114*108] == raw[towns-BASE:towns-BASE+4+114*108]
    assert after[actors-BASE:actors-BASE+0x1A04] == raw[actors-BASE:actors-BASE+0x1A04]
    for off in (0xD9858,0x51A20):
        at = struct.unpack_from('<I',arm,off)[0]
        assert not owned.intersection(range(at,at+4)) and after[at-BASE:at-BASE+4] == raw[at-BASE:at-BASE+4]
    return bytes(after),{'context':'Amsterdam_city_approach','owned_bytes':sorted(owned),'changes':changes,
        'town_ID':2,'source_port_point':point,'source_verified_water_point':water_point,'terrain':terrain,
        'active_ship':mobile,'original_defender_fleet_ID':2,'original_defender_captain_ID':2,
        'native_relation_setter':BASE+0x3C8F4,'relation_before':relation_before,'relation_after':2,
        'only_active_ship_position_and_original_diplomatic_prerequisite':True,
        'all_actor_objects_IDs_defender_fleet_town_defenses_shares_and_RNG_exact':True,
        'no_city_surrender_defender_choice_battle_state_event_or_numeric_message_injection':True,
        'original_input_and_unforced_defender_RNG_still_required':True,
        'normal_travel_and_earned_hostility_not_claimed':True,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(bytes(after)),
        'fixture_sha256':sha(Path(__file__).read_bytes())}
