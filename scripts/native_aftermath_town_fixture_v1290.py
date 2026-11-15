"""Sao Tome approach and existing Charles First Mate assignment before battle."""
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_aftermath_battle_fixture_v1269 import ROM, water
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read

BASE = 0x02000000


def apply_fixture(arm, raw, request):
    assert request == {'town_context':'SaoTomeFirstMate'} and len(raw) == 0x400000
    assert sha(arm) == read('translations/battle_aftermath_editorial_release_v1.json')['target_arm9_sha256']
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo, hi in [(0x34674,0x34688), (0xCD6B8,0xCD6CC), (0x82BA8,0x82BD0),
                   (0x71968,0x71A40), (0x6ED34,0x6EE90), (0x519D4,0x51A28)]:
        assert arm[lo:hi] == clean[lo:hi] and raw[lo:hi] == arm[lo:hi]
    cpu, get = get_machine(arm, raw)
    assert get(0x7F244) == get(0x2E58C) == 1
    assert list(struct.unpack('<2I', cpu.mem_read(get(0x3F0F8)+8, 8))) == [0,0]
    fleets, towns, actors = [get(fn) for fn in [0xCB1A8,0xCB178,0xCB184]]
    own, town, duty = fleets+4+132, towns+4+73*108, fleets+0x2090
    assert get(0x34674,own) == 115 and get(0x35320,own) == 2
    vt = struct.unpack('<I', cpu.mem_read(town,4))[0]
    name = get(struct.unpack('<I',cpu.mem_read(vt+8,4))[0]-BASE,town)
    assert bytes(cpu.mem_read(name,40)).split(b'\0')[0] == b'Sao Tome'
    eligible = []
    for index in range(63):
        fleet = fleets+4+132*index
        vt = struct.unpack('<I',cpu.mem_read(fleet,4))[0]
        if not get(struct.unpack('<I',cpu.mem_read(vt+0x10,4))[0]-BASE,fleet):
            continue
        company = get(0x35320,fleet)
        if get(0x34674,fleet) == 73 and company != 21 and get(0xB4AA8,town,company) > 0:
            eligible.append(index)
    assert eligible == [], eligible
    defenses = get(0xB3FD4,town,1)
    assert defenses == 100
    mobile = get(0x36C70,own+12)
    assert mobile and get(0x5543C,mobile) > 0 and get(0x55444,mobile) > 0
    port = get(0xCD6B8,73)
    point = list(struct.unpack('<2i',cpu.mem_read(port+12,8)))
    terrain = water(arm,[[point[0]+dx,point[1]+dy] for dx,dy in [(-60,0),(-80,0),(0,-60),(0,60),(60,0)]])
    water_point = next(row['map_point'] for row in terrain['queries'] if row['collision_free'])
    charles = actors+4+18*32
    assert get(0x7EE08,charles) == 18 and get(0x7E100,charles) == 0 and get(0x7E0B4,charles) in [1,2,3]
    assignments = [get(0x82BC4,duty,i) for i in range(31)]
    assert assignments[8] == 18 and assignments[15] == 208 and assignments.count(18) == 1
    model = get(0x82E04,duty)
    assert get(0x132C0,model,15) == 6 and get(0x82428,duty,1) == 0
    get(0x82BB8,duty,8,208)
    get(0x82BB8,duty,15,18)
    assert get(0x82428,duty,1) == charles and get(0x82478,duty,1) == 18
    after = bytearray(cpu.mem_read(BASE,0x400000))
    fields = {mobile+16:struct.pack('<2i',*[v*128 for v in water_point]), own+0x34:struct.pack('<2i',*water_point)}
    owned = {duty+6+8,duty+6+15}
    for at, data in fields.items():
        after[at-BASE:at-BASE+len(data)] = data
        owned.update(range(at,at+len(data)))
    changes = [{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a != b]
    assert len(owned) == 18 and all(row['address'] in owned for row in changes), changes
    assert after[actors-BASE:actors-BASE+0x1A04] == raw[actors-BASE:actors-BASE+0x1A04]
    assert after[towns-BASE:towns-BASE+4+114*108] == raw[towns-BASE:towns-BASE+4+114*108]
    for off in [0xD9858,0x51A20]:
        at = struct.unpack_from('<I',arm,off)[0]
        assert after[at-BASE:at-BASE+4] == raw[at-BASE:at-BASE+4]
    return bytes(after), {'context':'SaoTome_location_and_existing_First_Mate', 'town_ID':73,
        'source_port_point':point, 'source_verified_water_point':water_point, 'terrain':terrain,
        'original_eligible_docked_defender_IDs':eligible, 'original_defenses_unchanged':defenses,
        'First_Mate_existing_actor_ID':18, 'original_duty_setter':BASE+0x82BB8,
        'prior_assignment_slot':8, 'new_assignment_slot':15, 'existing_type6_room_unchanged':True,
        'only_location_and_two_ordinary_duty_assignment_bytes_changed':True,
        'owned_bytes':sorted(owned), 'changes':changes, 'all_actor_objects_IDs_health_towns_defenses_shares_diplomacy_RNG_and_events_exact':True,
        'no_numeric_message_eligibility_result_or_battle_state_injection':True,
        'before_RAM_sha256':sha(raw), 'after_RAM_sha256':sha(bytes(after)),
        'fixture_sha256':sha(Path(__file__).read_bytes()), 'not_earned_travel_or_role_assignment':True}
