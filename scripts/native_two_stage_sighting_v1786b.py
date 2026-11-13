"""Location-only medium-band loading followed by a close first-contact test."""
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_close_follow_v1781 import ROM,water,position,BASE
from scripts.native_close_sighting_v1689 import apply_fixture as original_initial
from scripts.native_call_abi_v764 import call
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read

def apply_fixture(arm,raw,request):
    assert set(request)=={'sighting_context','own_point'}
    context=request['sighting_context'];assert context in ('loadReady8','holdLoadReady8','closeLoaded8')
    point=request['own_point'];assert isinstance(point,list) and len(point)==2 and all(type(v)is int for v in point)
    assert len(raw)==0x400000 and sha(arm)==read('translations/lil_lessons_editorial_release_v1.json')['required_runtime_arm9_sha256']
    cpu,get=get_machine(arm,raw);root=get(0xCB1A8);own,enemy=root+4+132,root+4+8*132
    assert get(0x7F244)==get(0x2E58C)==1 and get(0x35320,own)==2 and get(0x35320,enemy)==8
    assert not cpu.mem_read(enemy+0x50,1)[0]&4,'Never reset the original first-sighting flag'
    target,getter=position(cpu,enemy);groups=bytes(cpu.mem_read(root+0x2080,16))
    a,b=0x02660100,0x02660110;cpu.mem_write(a,struct.pack('<2i',*point));cpu.mem_write(b,struct.pack('<2i',*target))
    distance_class=get(0x513D0,a,b,0)
    if context=='closeLoaded8':
        assert 8 in groups[::4] and distance_class==0
        assert max(abs(x-y)for x,y in zip(point,target,strict=True))<=32
    else:
        assert distance_class==1 and 160<=max(abs(x-y)for x,y in zip(point,target,strict=True))<320
    terrain=water(arm,[point]);assert terrain['queries'][0]['collision_free']
    mobile=get(0x36C70,own+12);assert mobile and get(0x564C8,mobile)
    fields={own+0x34:struct.pack('<2i',*point),mobile+16:struct.pack('<2i',*[v*128 for v in point])}
    if context=='loadReady8':
        _,prior=original_initial(arm,raw,{'sighting_context':'closeReady8'})
        relation={int(k):bytes.fromhex(v)for k,v in prior['declared_fields'].items()
            if int(k)not in fields}
        assert len(relation)==1 and len(next(iter(relation.values())))==1
        fields.update(relation)
    result=bytearray(raw)
    for at,data in fields.items():result[at-BASE:at-BASE+len(data)]=data
    result=bytes(result);owned={at+i for at,data in fields.items()for i in range(len(data))}
    assert len(owned)==(17 if context=='loadReady8' else 16)
    changes=[{'address':BASE+i,'before':x,'after':y}for i,(x,y)in enumerate(zip(raw,result,strict=True))if x!=y]
    assert all(r['address']in owned for r in changes)
    verify_cpu,verify=get_machine(arm,result);assert verify(0x78C60,1)==115
    assert position(verify_cpu,own)[0]==point
    assert bytes(verify_cpu.mem_read(BASE,0x400000))==result
    assert result[enemy-BASE:enemy-BASE+132]==raw[enemy-BASE:enemy-BASE+132]
    assert result[root-BASE+0x2080:root-BASE+0x2090]==groups
    for at in (struct.unpack_from('<I',arm,0xD9858)[0],struct.unpack_from('<I',arm,0x51A20)[0]):
        assert not set(range(at,at+4))&owned and raw[at-BASE:at-BASE+4]==result[at-BASE:at-BASE+4]
    return result,{'context':context,'own_point':point,'original_target_point':target,
        'original_virtual_position_getter':getter,'original_distance_class':distance_class,
        'owned_bytes':sorted(owned),'changes':changes,'declared_fields':{str(k):v.hex()for k,v in fields.items()},
        'terrain':terrain,'native_known_town_scan':115,'loaded_groups_before_hex':groups.hex(),
        'original_fleet8_already_loaded_required_for_close_stage':context=='closeLoaded8',
        'enemy_record_loaded_groups_seen_flags_RNG_actor_health_and_outcomes_exact':True,
        'initial_relation_prerequisite_only':context=='loadReady8','all_other4MiB_bytes_exact':True,
        'no_message_table_renderer_or_result_injection':True,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(result),'fixture_sha256':sha(Path(__file__).read_bytes())}
