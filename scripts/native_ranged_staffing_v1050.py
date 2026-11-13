"""Native-clamped own staffing and bounded still-live recovery; no RNG/outcome edits."""
import inspect
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import native_village_contexts_v618 as terrain_source
from scripts.native_reinforcement_lookout_v1043 import apply_fixture as prior
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read

BASE=0x02000000
ROM=Path('out/all_routes_combined_v1034_candidate.nds')


def water(arm,points):
    body=inspect.getsource(terrain_source.terrain_queries);old='out/all_routes_combined_v604_candidate.nds'
    assert body.count(old)==1;body=body.replace(old,str(ROM).replace('\\','/'));env=dict(terrain_source.terrain_queries.__globals__)
    exec(compile(body,'<V1050-original-terrain-current-ROM>','exec'),env)
    return env['terrain_queries'](arm,points)


def guarded(arm,raw):
    assert len(raw)==0x400000
    assert sha(arm)==read('translations/reinforcement_sniping_editorial_release_v1.json')['target_arm9_sha256']
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in ((0xAAF38,0xAAFB0),(0xAB158,0xAB1F0),(0x181B4,0x181C4),(0x18398,0x183A8),
                  (0x5543C,0x55454),(0x73B18,0x73C10),(0x519D4,0x51A10)):
        assert arm[lo:hi]==clean[lo:hi]


def install(raw,fields):
    result=bytearray(raw);owned=set()
    for at,data in fields.items():result[at-BASE:at-BASE+len(data)]=data;owned.update(range(at,at+len(data)))
    return bytes(result),owned


def delta(raw,after,owned):
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b]
    assert all(c['address'] in owned for c in changes)
    return changes


def apply_fixture(arm,raw,request):
    if request not in ({'reinforcement_context':'staffForRangedBattle'}, {'reinforcement_context':'recoverRangedOwn'}):
        return prior(arm,raw,request)
    guarded(arm,raw)
    if request=={'reinforcement_context':'recoverRangedOwn'}:
        cpu,get=get_machine(arm,raw);root=get(0xCB1A8);own=root+4+132;enemy=root+4+8*132
        assert get(0x7F244)==get(0x2E58C)==1 and get(0x35320,own)==2 and get(0x35320,enemy)==8
        assert list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12)))==[0,1,8]
        mobile,opponent=[get(0x36C70,f+12) for f in (own,enemy)]
        assert mobile and opponent and get(0x564C8,mobile) and get(0x564C8,opponent)
        model=get(0xAB158,mobile);hull,crew=get(0x183A0,model),get(0x181BC,model)
        assert (hull,crew)==(60,124)
        live=[get(0x5543C,mobile),get(0x55444,mobile)]
        assert all(0<v<=maximum for v,maximum in zip(live,(hull,crew),strict=True))
        assert get(0x5543C,opponent)>0 and get(0x55444,opponent)>0
        point=list(struct.unpack('<2i',cpu.mem_read(enemy+0x34,8)))
        points=[[point[0]+dx,point[1]+dy] for dx,dy in ((0,120),(120,0),(-120,0),(0,-120),(80,80),(-80,80))]
        terrain=water(arm,points);near=next(r['map_point'] for r in terrain['queries'] if r['collision_free'])
        fields={own+0x34:struct.pack('<2i',*near),mobile+16:struct.pack('<2i',*[v*128 for v in near]),
                mobile+24:struct.pack('<2H',hull,crew)}
        result,owned=install(raw,fields);assert len(owned)==20
        return result,{'synthetic_ranged_own_live_recovery_fixture':True,'context':'recoverRangedOwn',
            'owned_bytes':sorted(owned),'changes':delta(raw,result,owned),'fields':{str(k):v.hex() for k,v in fields.items()},
            'prior_live_Hull_Crew':live,'persisted_model_bounds_unchanged':[hull,crew],
            'source_verified_ranged_water_point':near,'terrain':terrain,
            'no_dead_or_disabled_vessel_revived':True,'enemy_and_other_fleet_stats_entirely_unchanged':True,
            'all_other4MiB_RAM_exact':True,'no_RNG_message_or_battle_outcome_injection':True,
            'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(result),'fixture_sha256':sha(Path(__file__).read_bytes())}
    after,receipt=prior(arm,raw,{'reinforcement_context':'prepareLookoutAndRange'})
    cpu,get=get_machine(arm,after);root=get(0xCB1A8);con=root+0x2090;roommodel=get(0x82E04,con)
    assert get(0x7B60,8)==8 and get(0x132C0,roommodel,9)==8
    assert get(0x82BC4,con,8)==18 and get(0x82BC4,con,9)==208
    assert get(0x15DE4,18,8)==1 and get(0x7E958,get(0xCB184)+4+18*32)==2
    fields={con+6+8:b'\xD0',con+6+9:bytes([18])};staff=[]
    for n,expected in ((1,(60,39,124)),(57,(25,16,24))):
        fleet=root+4+n*132;mobile=get(0x36C70,fleet+12);model=get(0xAB158,mobile)
        hull,crew,capacity=get(0x183A0,model),get(0x181BC,model),get(0xAB18C,model)
        assert (hull,crew,capacity)==expected and get(0x5543C,mobile)>0 and get(0x55444,mobile)>0
        get(0xAAF38,model,capacity);assert get(0x181BC,model)==capacity
        fields[model+0x44]=struct.pack('<H',capacity)
        fields[mobile+24]=struct.pack('<2H',hull,capacity)
        staff.append({'fleet_ID':n,'original_add_crew_method':0x020AAF38,'capacity_getter':0x020AB18C,
            'before_crew':crew,'native_clamped_crew':capacity,'persisted_Hull_unchanged':hull})
    friend=root+4+57*132;mobile=get(0x36C70,friend+12);enemy=root+4+8*132
    point=list(struct.unpack('<2i',cpu.mem_read(enemy+0x34,8)));main=receipt['new_own_ranged_water_point']
    points=[[point[0]+dx,point[1]+dy] for dx,dy in ((0,180),(180,0),(-180,0),(0,-180),(120,120),(-120,120))]
    terrain=water(arm,points)
    support=next(r['map_point'] for r in terrain['queries'] if r['collision_free'] and
                 max(abs(a-b) for a,b in zip(r['map_point'],main))<=160)
    fields[friend+0x34]=struct.pack('<2i',*support);fields[mobile+16]=struct.pack('<2i',*[v*128 for v in support])
    result,extra=install(after,fields);owned=set(receipt['owned_bytes'])|extra
    assert len(owned)==49
    verify_cpu,verify=get_machine(arm,result)
    assert verify(0x82478,con,7)==16 and verify(0x8235C,con,7,6,0)==166
    assert verify(0x82478,con,8)==18 and verify(0x8235C,con,8,6,0)==134
    assert verify(0x7F244)==verify(0x2E58C)==1
    receipt.update(context='staffForRangedBattle',owned_bytes=sorted(owned),changes=delta(raw,result,owned),
        original_native_clamped_staffing=staff,existing_qualified_Gunnery_actor_ID=18,
        original_Gunnery_role8_room_type8_slot9=True,native_Gunnery_Aim134=True,
        support_ranged_water_point=support,support_terrain=terrain,
        all49_owned_coordinate_assignment_Luck_and_own_staffing_bytes_declared=True,
        enemy_stats_RNG_original_eligibility_and_outcomes_unchanged=True,
        fixture_sha256=sha(Path(__file__).read_bytes()),after_RAM_sha256=sha(result))
    return result,receipt
