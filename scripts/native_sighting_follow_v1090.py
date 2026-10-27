"""Follow an unseen fleet with16 own-coordinate bytes;never rewrite its state."""
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_sighting_context_v1087d import apply_fixture as initial,water
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read

BASE=0x02000000


def apply_fixture(arm,raw,request):
    if request in ({'sighting_context':'closeReady28'},{'sighting_context':'closeAttack28'}):
        return initial(arm,raw,request)
    assert set(request)=={'sighting_context','own_point'} and request['sighting_context']=='followUnseen28'
    assert sha(arm)==read('translations/sighting_editorial_release_v1.json')['target_arm9_sha256'] and len(raw)==0x400000
    point=request['own_point'];assert isinstance(point,list) and len(point)==2 and all(type(v) is int for v in point)
    cpu,get=get_machine(arm,raw);root=get(0xCB1A8);own,enemy=root+4+132,root+4+28*132
    assert get(0x7F244)==get(0x2E58C)==1 and get(0x35320,own)==2 and get(0x35320,enemy)==9
    assert not cpu.mem_read(enemy+0x50,1)[0]&4,'Never reset or override a selected first-sighting event'
    target=list(struct.unpack('<2i',cpu.mem_read(enemy+0x34,8)))
    assert max(abs(a-b) for a,b in zip(point,target,strict=True))<=32
    terrain=water(arm,[point]);assert terrain['queries'][0]['collision_free']
    mobile=get(0x36C70,own+12);assert mobile and get(0x564C8,mobile)
    fields={own+0x34:struct.pack('<2i',*point),mobile+16:struct.pack('<2i',*[v*128 for v in point])}
    result=bytearray(raw);owned=set()
    for at,data in fields.items():result[at-BASE:at-BASE+len(data)]=data;owned.update(range(at,at+len(data)))
    result=bytes(result);assert len(owned)==16
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,result,strict=True)) if a!=b]
    assert all(c['address'] in owned for c in changes)
    assert raw[enemy-BASE:enemy-BASE+132]==result[enemy-BASE:enemy-BASE+132]
    assert raw[root-BASE+0x2080:root-BASE+0x2090]==result[root-BASE+0x2080:root-BASE+0x2090]
    for at in (struct.unpack_from('<I',arm,0xD9858)[0],struct.unpack_from('<I',arm,0x51A20)[0]):
        assert not set(range(at,at+4))&owned and raw[at-BASE:at-BASE+4]==result[at-BASE:at-BASE+4]
    return result,{'context':'followUnseen28','owned_bytes':sorted(owned),'changes':changes,
        'declared_fields':{str(k):v.hex() for k,v in fields.items()},'own_point':point,'original_enemy_cached_point':target,
        'terrain':terrain,'source_navigation_state':list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12))),
        'all_other4MiB_RAM_exact':True,'original_enemy_entire_record_and_loaded_fleet_groups_exact':True,
        'diplomacy_orders_ownership_actor_IDs_health_RNG_message_tables_and_results_not_owned_or_changed':True,
        'original_first_sighting_flag_untouched':True,'source_position_fixture_not_earned_movement':True,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(result),'fixture_sha256':sha(Path(__file__).read_bytes())}
