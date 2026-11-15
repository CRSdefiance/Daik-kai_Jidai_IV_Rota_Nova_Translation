"""Original hostility/attack-order prerequisites and own location;no event injection."""
import inspect
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import native_village_contexts_v618 as terrain_source
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read

BASE=0x02000000
ROM=Path('out/all_routes_combined_v1086_candidate.nds')


def water(arm,points):
    source=inspect.getsource(terrain_source.terrain_queries);old='out/all_routes_combined_v604_candidate.nds'
    assert source.count(old)==1
    source=source.replace(old,str(ROM).replace('\\','/'));env=dict(terrain_source.terrain_queries.__globals__)
    exec(compile(source,'<V1087-native-terrain-current-ROM>','exec'),env)
    return env['terrain_queries'](arm,points)


def apply_fixture(arm,raw,request):
    assert request in ({'sighting_context':'closeReady8'},{'sighting_context':'closeAttack8'},{'sighting_context':'compassReady8'})
    assert len(raw)==0x400000 and sha(arm)==read('translations/sighting_editorial_release_v1.json')['target_arm9_sha256']
    source=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in ((0x3C568,0x3C604),(0x3C8F4,0x3CB30),(0x3CB30,0x3CBF0),(0x77A58,0x77EC4),
        (0x774BC,0x77770),(0x7777C,0x77A40),(0x82478,0x825E4),(0x70BF8,0x71088)):
        assert arm[lo:hi]==source[lo:hi]
    cpu,get=get_machine(arm,raw);root=get(0xCB1A8);companies=get(0xCB160)
    assert get(0x7F244)==get(0x2E58C)==1
    own,enemy=root+4+132,root+4+8*132
    assert get(0x35320,own)==2 and get(0x35320,enemy)==8
    assert not cpu.mem_read(enemy+0x50,1)[0]&4,'Original first-sighting flag must already be clear;never reset it'
    mobile=get(0x36C70,own+12);assert mobile and get(0x564C8,mobile)
    target=list(struct.unpack('<2i',cpu.mem_read(enemy+0x34,8)))
    context=request['sighting_context'];incoming=context=='closeAttack8'
    points=[target] if context!='compassReady8' else [[target[0]+dx,target[1]+dy] for dx,dy in ((100,100),(0,100),(-100,100),(100,0))]
    terrain=water(arm,points);point=next(r['map_point'] for r in terrain['queries'] if r['collision_free'])
    company=companies+4+8*76
    before_relation=get(0x3CB30,company,2);before_order=[get(0x3C5FC,company),get(0x3C5F4,company)]
    get(0x3C8F4,company,2,0 if incoming else 2,21)
    fields={own+0x34:struct.pack('<2i',*point),mobile+16:struct.pack('<2i',*[n*128 for n in point]),
        companies+4+2*76+0x1F+8:bytes(cpu.mem_read(companies+4+2*76+0x1F+8,1))}
    if incoming:
        get(0x3C568,company,2)
        assert [get(0x3C5FC,company),get(0x3C5F4,company)]==[2,2]
        fields[company+0x48]=bytes(cpu.mem_read(company+0x48,2))
    assert get(0x3CB30,company,2)==(0 if incoming else 2)
    result=bytearray(raw);owned=set()
    for at,data in fields.items():result[at-BASE:at-BASE+len(data)]=data;owned.update(range(at,at+len(data)))
    result=bytes(result);assert len(owned)==(19 if incoming else 17)
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,result,strict=True)) if a!=b]
    assert all(r['address'] in owned for r in changes)
    assert result[enemy-BASE:enemy-BASE+132]==raw[enemy-BASE:enemy-BASE+132]
    assert not any(root+0x2080+i in owned for i in range(16))
    seed,flag=[struct.unpack_from('<I',arm,at)[0] for at in (0xD9858,0x51A20)]
    for at in (seed,flag):assert not set(range(at,at+4))&owned and result[at-BASE:at-BASE+4]==raw[at-BASE:at-BASE+4]
    verify_cpu,verify=get_machine(arm,result)
    assert verify(0x7F244)==verify(0x2E58C)==1 and verify(0x3CB30,company,2)==(0 if incoming else 2)
    return result,{'context':context,'owned_bytes':sorted(owned),'changes':changes,
        'declared_fields':{str(k):v.hex() for k,v in fields.items()},'original_enemy_fleet_ID':8,'actual_captain_ID':1,
        'original_own_position_set_to_native_water_point':point,'enemy_cached_point_unchanged':target,'terrain':terrain,
        'original_relation_setter':BASE+0x3C8F4,'before_relation':before_relation,'after_relation':0 if incoming else 2,
        'original_attack_order_setter':BASE+0x3C568 if incoming else None,
        'before_order':before_order,'after_order':[verify(0x3C5FC,company),verify(0x3C5F4,company)],
        'source_original_AI_attack_order_prerequisite_not_a_battle_outcome_override':incoming,
        'native_speaker_or_fallback_actor_ID':verify(0x82478,root+0x2090,1),
        'original_first_sighting_flag_untouched_and_all_other_enemy_fleet_bytes_exact':True,
        'all_actor_IDs_ownership_health_and_other4MiB_RAM_exact':True,
        'RNG_seed_and_initialization_flag_exact':True,'no_message_ID_table_renderer_or_result_injection':True,
        'synthetic_location_and_source_diplomatic_prerequisites_not_earned_progression':True,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(result),'fixture_sha256':sha(Path(__file__).read_bytes())}
