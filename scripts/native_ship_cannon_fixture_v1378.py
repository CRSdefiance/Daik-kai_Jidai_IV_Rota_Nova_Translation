"""Prebattle original cannon equipment only,plus the established location fixture.

The original game must determine firing,damage and outcomes. No battle flags,
enemy objects,actor identities,health,crew,RNG or result data are supplied.
"""
import struct
from pathlib import Path
from scripts.native_flagship_capture_fixture_v1368 import apply_fixture as previous
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha

BASE = 0x02000000


def apply_fixture(arm,raw,request):
    census = read('work/analysis/ship_cannon_setup_v1377/source_cannon_setup.json')
    after,parent = previous(arm,raw,request)
    cpu,get = get_machine(arm,after)
    fleets = get(0xCB1A8)
    assert list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12)))==[0,0,0]
    assert get(0xAB784,4)==5 and get(0xAB784,7)==0
    result,owned,items = bytearray(after),set(parent['owned_bytes']),[]
    for expected,kind in zip(census['actual_prebattle_five_ship_cannons'],[4,7,7,7,7],strict=True):
        slot = expected['slot']
        model = get(0x36C94,fleets+4+132+12+8*slot)
        mobile = get(0x36C70,fleets+4+132+12+8*slot)
        assert model==expected['model'] and mobile==expected['mobile']
        field = model+0x4A
        old = get(0x1856C,model)
        assert old==result[field-BASE]==expected['current_cannon_type']
        assert get(0xAB71C,mobile)==expected['native_battery_multiplier']
        assert [get(0x5543C,mobile),get(0x55444,mobile)]==expected['actual_Hull_Crew']
        result[field-BASE] = kind
        owned.add(field)
        items.append({'slot':slot,'model':model,'field':field,'before':old,'after':kind,
            'native_strength_after':get(0xAB784,kind),
            'equipment':'original Heavy Cannon' if kind==4 else 'original NoGun type7'})
    result = bytes(result)
    changes = [{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,result,strict=True)) if a!=b]
    assert len(owned)==45 and all(c['address'] in owned for c in changes)
    assert {BASE+i for i,(a,b) in enumerate(zip(after,result,strict=True)) if a!=b}=={i['field'] for i in items}
    return result,{'context':'five_ship_prebattle_location_and_original_cannon_loadout',
        'parent_location_fixture':parent,'owned_bytes':sorted(owned),'changes':changes,
        'cannon_equipment':items,'source_census':'work/analysis/ship_cannon_setup_v1377/source_cannon_setup.json',
        'source_census_sha256':sha(Path('work/analysis/ship_cannon_setup_v1377/source_cannon_setup.json').read_bytes()),
        'only40_live_position_bytes_and5_original_cannon_type_bytes_owned':True,
        'entire_other4MiB_including_all_health_crew_actors_IDs_RNG_enemy_and_results_exact':True,
        'prebattle_only_no_later_fixture_permitted':True,
        'actual_NoGun_firing_suppression_and_original_outcomes_must_be_observed_not_assumed':True,
        'not_earned_travel_or_equipment_purchase_or_sinking_completion':True,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(result),
        'fixture_sha256':sha(Path(__file__).read_bytes())}
