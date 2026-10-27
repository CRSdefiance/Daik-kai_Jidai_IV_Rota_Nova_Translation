"""Source-bound Pasha location fixture avoids Hodram's original Speyer tutorial."""
import inspect
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import native_village_contexts_v618 as terrain_source
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read

BASE = 0x02000000
ROM = Path('out/all_routes_combined_v997_candidate.nds')
CASES = {'KnownJanus': (4,0,1), 'UnknownEmilio': (14,0,0), 'ReadyEmilio': (14,2,1)}


def assign(arm,raw,request):
    assert request in (*CASES,'approachPasha') and len(raw)==0x400000
    assert sha(arm)==read('translations/battle_declaration_editorial_release_v1.json')['target_arm9_sha256']
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans=((0x6EE90,0x6F0C8),(0x82478,0x825E4),(0x3CD2C,0x3CD78),
           (0x7DAF0,0x7DB14),(0x3CB30,0x3CB90),(0x34674,0x346A0),
           (0x36C70,0x36CC0),(0x5543C,0x55454),(0x69B5C,0x69E00))
    for lo,hi in spans:assert arm[lo:hi]==clean[lo:hi]
    rom=NdsImage.open(ROM)
    assert arm==rom.read_file('/__arm9__.bin')
    assert rom.read_file('/data/WORLDMAP.DK4')==NdsImage.open('work/clean.nds').read_file('/data/WORLDMAP.DK4')
    cpu,get=get_machine(arm,raw)
    root,actors,companies=get(0xCB1A8),get(0xCB184),get(0xCB160)
    assert (get(0x7F244),get(0x2E58C),get(0x397D8,companies))==(1,1,2)
    own,enemy=root+4+0x84,root+4+9*0x84
    assert get(0x35320,own)==2 and get(0x35320,enemy)==9
    assert get(0x34674,own)==get(0x34674,enemy)==115
    mobile=get(0x36C70,own+12)
    assert BASE<=mobile<BASE+len(raw)-28
    assert struct.unpack('<I',cpu.mem_read(mobile,4))[0]==0x02143A80
    assert get(0x5543C,mobile)>0 and get(0x55444,mobile)>0
    fields={};extra={}
    if request=='approachPasha':
        model=get(0x36C94,enemy+12)
        assert BASE<=model<BASE+len(raw)-140
        assert get(0x183A0,model)>0 and get(0x181BC,model)>0
        vt=struct.unpack('<I',cpu.mem_read(enemy,4))[0]
        getter=struct.unpack('<I',cpu.mem_read(vt+0x20,4))[0]
        get(getter-BASE,0x02460000,enemy)
        point=list(struct.unpack('<2i',cpu.mem_read(0x02460000,8)))
        candidates=[[point[0]+dx,point[1]+dy] for dx,dy in ((0,20),(20,0),(-20,0),(0,-20),(16,16),(-16,16))]
        body=inspect.getsource(terrain_source.terrain_queries)
        old='out/all_routes_combined_v604_candidate.nds';assert body.count(old)==1
        body=body.replace(old,str(ROM).replace('\\','/'))
        scope=dict(terrain_source.terrain_queries.__globals__)
        exec(compile(body,'<V1002-current-original-terrain>','exec'),scope)
        terrain=scope['terrain_queries'](arm,candidates)
        water=next(r['map_point'] for r in terrain['queries'] if r['collision_free'])
        fields[mobile+16]=struct.pack('<2i',*[v*128 for v in water])
        extra={'original_enemy_cached_point':point,'source_verified_water_point':water,'terrain':terrain,
               'target_original_persisted_Hull_Crew':[get(0x183A0,model),get(0x181BC,model)],
               'original_enemy_model':model,'target_mobile_before':get(0x36C70,enemy+12)}
    else:
        actor,relation,flag=CASES[request]
        obj=actors+4+actor*32
        assert get(0x7E100,obj)==0 and get(0x7E0B4,obj) in (1,2,3)
        controller=root+0x2090;model=get(0x82E04,controller)
        for slot in range(31):
            if get(0x132C0,model,slot)==6 or get(0x82BC4,controller,slot)==actor:
                fields[controller+6+slot]=b'\xD0'
        fields[model+0x1E+12]=b'\x06';fields[controller+6+12]=bytes([actor])
        company=companies+4+9*76;leader=get(0x3CD2C,company)
        assert actors+4<=leader<actors+4+208*32 and (leader-actors-4)%32==0
        relation_at=companies+4+2*76+0x1F+9
        assert raw[relation_at-BASE] in (0,2) and raw[leader+26-BASE] in (0,1)
        fields[relation_at]=bytes([relation]);fields[leader+26]=bytes([flag])
        extra={'First_Mate_actor_ID':actor,'target_original_leader_object':leader,
               'target_original_leader_ID':(leader-actors-4)//32,
               'relation_byte_address':relation_at,'relation':relation,'leader_branch_byte26':flag}
    after=bytearray(raw);owned=set()
    for at,data in fields.items():
        assert BASE<=at<BASE+len(raw)-len(data)
        after[at-BASE:at-BASE+len(data)]=data;owned.update(range(at,at+len(data)))
    after=bytes(after)
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b]
    assert all(c['address'] in owned for c in changes)
    verify_cpu,verify=get_machine(arm,after)
    if request!='approachPasha':
        assert verify(0x82478,controller,1)==actor
        assert verify(0x3CB30,company,2)==relation and verify(0x7DB0C,leader)==flag
        for at in (obj,actors+0x19E4):assert raw[at-BASE:at-BASE+32]==after[at-BASE:at-BASE+32]
    assert verify(0x7F244)==1 and verify(0x2E58C)==1
    return after,{'synthetic_declaration_context_fixture':True,'declaration_context':request,
        'target_original_fleet_ID':9,'target_company_ID':9,'target_faction':'Pasha',
        **extra,'declared_owned_fields':{str(k):v.hex() for k,v in fields.items()},
        'owned_bytes':sorted(owned),'changes':changes,'all_other4MiB_RAM_exact':True,
        'no_battle_outcome_message_ID_renderer_or_captain_identity_injection':True,
        'earned_story_event_or_progression_not_claimed':True,
        'source_guard_spans':[list(s) for s in spans],
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(after),
        'fixture_sha256':sha(Path(__file__).read_bytes()),
        'original_terrain_helper_sha256':sha(Path(terrain_source.__file__).read_bytes())}
