"""Existing Gerhard in existing Gunnery; native-bounded sailor complement prebattle."""
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_aftermath_town_fixture_v1290 import ROM, apply_fixture as previous
from scripts.verify_personal_gameplay_v841 import get_machine

BASE = 0x02000000


def apply_fixture(arm,raw,request):
    assert request == {'town_context':'SaoTomeGunnery'}
    after,parent = previous(arm,raw,{'town_context':'SaoTomeFirstMate'})
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in [(0xAAF38,0xAAFB0),(0xAB18C,0xAB1F0),(0x82BA8,0x82BD0),(0x132C0,0x132CC)]:
        assert arm[lo:hi] == clean[lo:hi]
    cpu,get = get_machine(arm,after)
    fleets,actors = get(0xCB1A8),get(0xCB184)
    duty = fleets+0x2090
    room_model = get(0x82E04,duty)
    assignments = [get(0x82BC4,duty,i) for i in range(31)]
    assert assignments[21] == 16 and assignments[9] == 208 and assignments.count(16) == 1
    assert get(0x132C0,room_model,9) == 8 and get(0x7B60,9) == 8
    actor = actors+4+16*32
    assert get(0x7EE08,actor) == 16 and get(0x7E958,actor) == 2
    assert get(0x7E100,actor) == 0 and get(0x7E0B4,actor) in [1,2,3] and get(0x15DE4,16,8) == 1
    get(0x82BA8,duty,21)
    get(0x82BB8,duty,9,16)
    assert get(0x82478,duty,9) == 16 and get(0x82478,duty,1) == 18
    aim = get(0x8235C,duty,9,6,0)
    own = fleets+4+132
    mobile = get(0x36C70,own+12)
    ship = get(0xAB158,mobile)
    hull,crew,capacity = get(0x183A0,ship),get(0x181BC,ship),get(0xAB18C,ship)
    assert (hull,crew,capacity) == (60,39,124)
    assert get(0x5543C,mobile) == 60 and get(0x55444,mobile) == 39
    get(0xAAF38,ship,capacity)
    assert get(0x181BC,ship) == capacity
    result = bytearray(cpu.mem_read(BASE,0x400000))
    struct.pack_into('<H',result,mobile+26-BASE,capacity)
    owned = set(parent['owned_bytes']) | {duty+6+21,duty+6+9} | set(range(ship+0x44,ship+0x46)) | set(range(mobile+26,mobile+28))
    changes = [{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,result,strict=True)) if a != b]
    assert len(owned) == 24 and all(row['address'] in owned for row in changes),changes
    assert result[actors-BASE:actors-BASE+0x1A04] == raw[actors-BASE:actors-BASE+0x1A04]
    for offset in [0xD9858,0x51A20]:
        at = struct.unpack_from('<I',arm,offset)[0]
        assert result[at-BASE:at-BASE+4] == raw[at-BASE:at-BASE+4]
    return bytes(result),{'context':'SaoTome_prebattle_existing_Gunner_and_native_crew_capacity',
        'parent_fixture_receipt':parent,'owned_bytes':sorted(owned),'changes':changes,
        'existing_owned_qualified_Gunner_actor_ID':16,'existing_First_Mate_actor_ID':18,
        'old_Gunner_assignment_slot':21,'new_Gunnery_slot':9,'existing_room_type8_unchanged':True,
        'native_Gunnery_Aim':aim,'native_add_sailors_setter':BASE+0xAAF38,
        'original_Hull_Crew_capacity':[hull,crew,capacity],'native_ship_sailor_complement_after':capacity,
        'all_actor_objects_IDs_abilities_health_towns_defenses_shares_diplomacy_RNG_events_and_other4MiB_bytes_exact':True,
        'Hull_unchanged_only_sailor_complement_filled_to_native_capacity':True,
        'prebattle_only_no_numeric_message_eligibility_result_or_battle_state_injection':True,
        'not_earned_travel_crew_assignment_or_recruitment':True,'before_RAM_sha256':sha(raw),
        'after_RAM_sha256':sha(bytes(result)),'fixture_sha256':sha(Path(__file__).read_bytes())}
