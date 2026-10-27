"""Position existing own fleets by a visible opponent; no ownership/result changes."""
import inspect
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import native_village_contexts_v618 as terrain_source
from scripts.native_reinforcement_pact_v1811 import location_fixture as prior
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read

BASE=0x02000000
ROM=Path('out/all_routes_combined_v1807_candidate.nds')


def apply_fixture(arm,raw,request):
    if request=={'reinforcement_context':'approachOwn57'}:return prior(arm,raw,request)
    assert request=={'reinforcement_context':'approachVisible8WithOwn57'} and len(raw)==0x400000
    assert sha(arm)==read('translations/reinforcement_faction_prose_release_v1.json')['required_ARM9_sha256']
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in ((0x2C1C4,0x2C1D8),(0x36C70,0x36C94),(0x655B8,0x65728),(0x70BF8,0x71088),(0x69B5C,0x69E00)):
        assert arm[lo:hi]==clean[lo:hi]
    cpu,get=get_machine(arm,raw);root=get(0xCB1A8);actors=get(0xCB184)
    assert get(0x2E58C)==get(0x7F244)==1
    own,friend,enemy=[root+4+n*0x84 for n in (1,57,8)]
    assert get(0x35320,own)==get(0x35320,friend)==2 and get(0x35320,enemy)==8
    assert get(0x3697C,friend)==actors+4+23*32
    mobiles=[get(0x36C70,f+12) for f in (own,friend,enemy)]
    assert all(mobiles) and all(get(0x564C8,m) for m in mobiles)
    point=list(struct.unpack('<2i',cpu.mem_read(enemy+0x34,8)))
    points=[[point[0]+dx,point[1]+dy] for dx,dy in ((0,20),(20,0),(-20,0),(0,-20),(16,16),(-16,16),
                                                         (0,40),(40,0),(-40,0),(0,-40),(32,32),(-32,32))]
    body=inspect.getsource(terrain_source.terrain_queries)
    old='out/all_routes_combined_v604_candidate.nds';assert body.count(old)==1
    body=body.replace(old,str(ROM).replace('\\','/'));env=dict(terrain_source.terrain_queries.__globals__)
    exec(compile(body,'<V1040-original-terrain-current-ROM>','exec'),env);terrain=env['terrain_queries'](arm,points)
    water=[r['map_point'] for r in terrain['queries'] if r['collision_free']]
    near=next(p for p in water if max(abs(a-b) for a,b in zip(p,point))<=20)
    support=next(p for p in water if p!=near and max(abs(a-b) for a,b in zip(p,near))<=80)
    fields={}
    for f,m,p in ((own,mobiles[0],near),(friend,mobiles[1],support)):
        fields[f+0x34]=struct.pack('<2i',*p);fields[m+16]=struct.pack('<2i',*[v*128 for v in p])
    result=bytearray(raw);owned=set()
    for at,data in fields.items():result[at-BASE:at-BASE+len(data)]=data;owned.update(range(at,at+len(data)))
    result=bytes(result)
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,result,strict=True)) if a!=b]
    assert len(owned)==32 and all(r['address'] in owned for r in changes)
    assert result[enemy-BASE:enemy-BASE+0x84]==raw[enemy-BASE:enemy-BASE+0x84]
    assert result[mobiles[2]-BASE:mobiles[2]-BASE+28]==raw[mobiles[2]-BASE:mobiles[2]-BASE+28]
    check,verify=get_machine(arm,result)
    assert verify(0x7F244)==verify(0x2E58C)==1 and verify(0x3697C,friend)==actors+4+23*32
    return result,{'synthetic_reinforcement_location_fixture':True,'context':'approachVisible8WithOwn57',
        'existing_opponent_fleet_ID':8,'existing_own_fleet_IDs':[1,57],
        'original_target_position':point,'source_verified_own_water_points':[near,support],'terrain':terrain,
        'owned_bytes':sorted(owned),'declared_fields':{str(k):v.hex() for k,v in fields.items()},'changes':changes,
        'all_other4MiB_RAM_exact':True,'opponent_entire_fleet_and_ship_unchanged':True,
        'actor_identities_ownership_policies_and_all_noncoordinate_fields_unchanged':True,
        'no_numeric_message_selection_renderer_or_battle_outcome_injection':True,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(result),'fixture_sha256':sha(Path(__file__).read_bytes())}
