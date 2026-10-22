"""Approach an existing own regional fleet; preserve every identity/outcome byte."""
import inspect
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import native_village_contexts_v618 as terrain_source
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read

BASE=0x02000000
ROM=Path('out/all_routes_combined_v1034_candidate.nds')


def apply_fixture(arm,raw,request):
    assert request=={'reinforcement_context':'approachOwn57'} and len(raw)==0x400000
    assert sha(arm)==read('translations/reinforcement_sniping_editorial_release_v1.json')['target_arm9_sha256']
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in ((0x2C1C4,0x2C1D8),(0x36C70,0x36C94),(0x69B5C,0x69E00),(0x70BF8,0x71088)):
        assert arm[lo:hi]==clean[lo:hi]
    cpu,get=get_machine(arm,raw);root=get(0xCB1A8)
    assert get(0x2E58C)==1 and get(0x7F244)==1
    own,target=root+4+0x84,root+4+57*0x84
    assert get(0x35320,own)==get(0x35320,target)==2
    assert get(0x36948,target)==0 and get(0x36914,target)==1
    commander=get(0x3697C,target);actors=get(0xCB184)
    assert commander==actors+4+23*32
    mobile=get(0x36C70,own+12);assert mobile and get(0x564C8,mobile)
    point=list(struct.unpack('<2i',cpu.mem_read(target+0x34,8)))
    points=[[point[0]+dx,point[1]+dy] for dx,dy in ((0,20),(20,0),(-20,0),(0,-20),(16,16),(-16,16))]
    body=inspect.getsource(terrain_source.terrain_queries)
    old='out/all_routes_combined_v604_candidate.nds';assert body.count(old)==1
    body=body.replace(old,str(ROM).replace('\\','/'))
    env=dict(terrain_source.terrain_queries.__globals__)
    exec(compile(body,'<V1038-original-terrain-current-ROM>','exec'),env)
    terrain=env['terrain_queries'](arm,points)
    water=next(r['map_point'] for r in terrain['queries'] if r['collision_free'])
    fields={own+0x34:struct.pack('<2i',*water),mobile+16:struct.pack('<2i',*[v*128 for v in water])}
    result=bytearray(raw);owned=set()
    for at,data in fields.items():result[at-BASE:at-BASE+len(data)]=data;owned.update(range(at,at+len(data)))
    result=bytes(result)
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,result,strict=True)) if a!=b]
    assert len(owned)==16 and all(r['address'] in owned for r in changes)
    assert result[target-BASE:target-BASE+0x84]==raw[target-BASE:target-BASE+0x84]
    check,verify=get_machine(arm,result)
    assert verify(0x7F244)==1 and verify(0x2E58C)==1 and verify(0x3697C,target)==commander
    return result,{'synthetic_reinforcement_location_fixture':True,'context':'approachOwn57',
        'existing_player_regional_fleet_ID':57,'original_UI_formed_commander_actor_ID':23,
        'original_target_position':point,'source_verified_water_point':water,'terrain':terrain,
        'owned_bytes':sorted(owned),'declared_fields':{str(k):v.hex() for k,v in fields.items()},'changes':changes,
        'all_other4MiB_RAM_exact':True,'regional_fleet_and_all_actor_identity_records_unchanged':True,
        'no_numeric_message_selection_renderer_or_battle_outcome_injection':True,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(result),'fixture_sha256':sha(Path(__file__).read_bytes())}
