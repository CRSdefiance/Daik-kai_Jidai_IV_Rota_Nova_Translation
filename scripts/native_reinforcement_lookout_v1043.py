"""Original-qualified Lookout and ranged approach; original shot RNG remains intact."""
import inspect
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import native_village_contexts_v618 as terrain_source
from scripts.native_reinforcement_proximity_v1040 import apply_fixture as prior
from scripts.verify_personal_gameplay_v841 import get_machine

BASE=0x02000000
ROM=Path('out/all_routes_combined_v1034_candidate.nds')


def apply_fixture(arm,raw,request):
    if request!={'reinforcement_context':'prepareLookoutAndRange'}:return prior(arm,raw,request)
    after,receipt=prior(arm,raw,{'reinforcement_context':'approachVisible8WithOwn57'})
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in ((0x7DCC8,0x7DE20),(0x7E750,0x7E7B4),(0x8235C,0x82478),(0x82478,0x825E4),
                  (0x8205C,0x820D8),(0x15DE4,0x15E90),(0x73B18,0x73C10),(0x519D4,0x51A10)):
        assert arm[lo:hi]==clean[lo:hi]
    cpu,get=get_machine(arm,after);root=get(0xCB1A8);con=root+0x2090;actors=get(0xCB184)
    actor=actors+4+16*32
    assert get(0x7E958,actor)==2 and get(0x15DE4,16,1)==1
    assert get(0x82BC4,con,21)==16 and get(0x82BC4,con,3)==208
    assert get(0x7B60,7)==1
    level=get(0x7E728,actor);aim=get(0x7DCC8,actor,6);luck=cpu.mem_read(actor+13,1)[0]
    assert (level,aim,luck)==(37,133,64)
    get(0x7E750,actor,5,100-luck)
    assert cpu.mem_read(actor+13,1)==b'\x64' and get(0x7DCC8,actor,6)==166
    assert get(0x7E728,actor)==level
    enemy=root+4+8*0x84;own=root+4+0x84;mobile=get(0x36C70,own+12)
    point=list(struct.unpack('<2i',cpu.mem_read(enemy+0x34,8)))
    points=[[point[0]+dx,point[1]+dy] for dx,dy in ((0,120),(120,0),(-120,0),(0,-120),(80,80),(-80,80))]
    body=inspect.getsource(terrain_source.terrain_queries);old='out/all_routes_combined_v604_candidate.nds'
    assert body.count(old)==1;body=body.replace(old,str(ROM).replace('\\','/'));env=dict(terrain_source.terrain_queries.__globals__)
    exec(compile(body,'<V1043-original-terrain-current-ROM>','exec'),env);terrain=env['terrain_queries'](arm,points)
    water=next(r['map_point'] for r in terrain['queries'] if r['collision_free'])
    fields={own+0x34:struct.pack('<2i',*water),mobile+16:struct.pack('<2i',*[v*128 for v in water]),
            con+6+21:b'\xD0',con+6+3:bytes([16]),actor+13:b'\x64'}
    result=bytearray(after);owned=set(receipt['owned_bytes'])
    for at,data in fields.items():result[at-BASE:at-BASE+len(data)]=data;owned.update(range(at,at+len(data)))
    result=bytes(result);verify_cpu,verify=get_machine(arm,result)
    assert verify(0x82478,con,7)==16 and verify(0x8205C,con,1)==32
    assert verify(0x8235C,con,7,6,0)==166 and verify(0x7E728,actor)==37
    assert verify(0x7F244)==verify(0x2E58C)==1
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,result,strict=True)) if a!=b]
    assert len(owned)==35 and all(c['address'] in owned for c in changes)
    receipt.update(context='prepareLookoutAndRange',owned_bytes=sorted(owned),changes=changes,
        declared_Lookout_and_range_fields={str(k):v.hex() for k,v in fields.items()},
        original_Lookout_qualification_actor_ID=16,original_attribute_method=0x0207E750,
        Luck_before_after=[64,100],Aim_before_after=[133,166],unchanged_level=37,
        new_own_ranged_water_point=water,ranged_terrain=terrain,
        only35_coordinate_assignment_and_Luck_bytes_owned=True,
        original_shot_target_checks_RNG2000_and_native_outcomes_unchanged=True,
        fixture_sha256=sha(Path(__file__).read_bytes()),after_RAM_sha256=sha(result))
    return result,receipt
