"""Approach the actual spawned Pasha fleet, preserving its identity and state."""
import struct
import inspect
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_battle_declaration_location_v1010 import dispatch_fixture as prior
from scripts import native_village_contexts_v618 as terrain_source
from scripts.native_battle_declaration_standoff_v999 import ROM
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read

BASE=0x02000000


def dispatch_fixture(arm,raw,request):
    if request!={'declaration_context':'approachVisiblePasha'}:return prior(arm,raw,request)
    assert len(raw)==0x400000
    assert sha(arm)==read('translations/battle_declaration_editorial_release_v1.json')['target_arm9_sha256']
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in ((0x6EE90,0x6F0C8),(0x2C1C4,0x2C1D8),(0x69B5C,0x69E00)):
        assert arm[lo:hi]==clean[lo:hi]
    cpu,get=get_machine(arm,raw)
    root,manager=get(0xCB1A8),get(0xCB19C)
    assert get(0x2E58C)==1 and get(0x7F244)==1
    candidates=[]
    for slot in range(4):
        fleet_id=raw[root+0x2080+4*slot-BASE]
        if fleet_id==64:continue
        fleet=root+4+fleet_id*0x84
        if get(0x35320,fleet)!=9:continue
        mobile=get(0x36C70,fleet+12)
        assert mobile and get(0x564C8,mobile) and get(0x34674,fleet)==115
        assert get(0x56598,mobile)//5==slot
        assert get(0x5543C,mobile)>0 and get(0x55444,mobile)>0
        candidates.append((slot,fleet_id,fleet,mobile))
    assert len(candidates)==1,candidates
    slot,fleet_id,fleet,enemy=candidates[0]
    vt=struct.unpack('<I',cpu.mem_read(enemy,4))[0]
    getter=struct.unpack('<I',cpu.mem_read(vt+0x5C,4))[0]
    get(getter-BASE,0x02460000,enemy)
    point=list(struct.unpack('<2i',cpu.mem_read(0x02460000,8)))
    points=[[point[0]+dx,point[1]+dy] for dx,dy in ((0,20),(20,0),(-20,0),(0,-20),(16,16),(-16,16))]
    body=inspect.getsource(terrain_source.terrain_queries)
    old='out/all_routes_combined_v604_candidate.nds';assert body.count(old)==1
    body=body.replace(old,str(ROM).replace('\\','/'))
    scope=dict(terrain_source.terrain_queries.__globals__)
    exec(compile(body,'<V1012-original-current-terrain>','exec'),scope)
    terrain=scope['terrain_queries'](arm,points)
    water=next(r['map_point'] for r in terrain['queries'] if r['collision_free'])
    own=root+4+0x84;mobile=get(0x36C70,own+12)
    fields={mobile+16:struct.pack('<2i',*[v*128 for v in water]),
            own+0x34:struct.pack('<2i',*water)}
    after=bytearray(raw);owned=set()
    for at,data in fields.items():
        after[at-BASE:at-BASE+len(data)]=data;owned.update(range(at,at+len(data)))
    after=bytes(after)
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b]
    assert len(owned)==16 and all(c['address'] in owned for c in changes)
    assert after[fleet-BASE:fleet-BASE+132]==raw[fleet-BASE:fleet-BASE+132]
    assert after[enemy-BASE:enemy-BASE+28]==raw[enemy-BASE:enemy-BASE+28]
    verify_cpu,verify=get_machine(arm,after)
    assert verify(0x7F244)==1 and verify(0x2E58C)==1
    return after,{'synthetic_declaration_context_fixture':True,'declaration_context':'approachVisiblePasha',
        'target_original_fleet_ID':fleet_id,'target_company_ID':9,'original_target_mobile':enemy,
        'original_target_selector_index':slot*5,'original_target_point_getter':getter,
        'original_target_point':point,'source_verified_water_point':water,'terrain':terrain,
        'declared_owned_fields':{str(k):v.hex() for k,v in fields.items()},'owned_bytes':sorted(owned),
        'changes':changes,'all_other4MiB_RAM_exact':True,'enemy_fleet_and_ship_entirely_unchanged':True,
        'no_actor_identity_outcome_message_or_renderer_injection':True,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(after),
        'fixture_sha256':sha(Path(__file__).read_bytes())}
