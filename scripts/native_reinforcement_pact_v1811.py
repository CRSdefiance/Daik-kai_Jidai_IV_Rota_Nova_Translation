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
ROM=Path('out/all_routes_combined_v1807_candidate.nds')


def location_fixture(arm,raw,request):
    assert request=={'reinforcement_context':'approachOwn57'} and len(raw)==0x400000
    assert sha(arm)==read('translations/reinforcement_faction_prose_release_v1.json')['required_ARM9_sha256']
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


"""Original alliance/assistance and war methods; actual encounter selects the message."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
prior=location_fixture
from scripts.verify_personal_gameplay_v841 import get_machine

BASE=0x02000000


def apply_fixture(arm,raw,request):
    if request!={'reinforcement_context':'prepareAssistancePactAtFirstSight'}:return prior(arm,raw,request)
    after,receipt=prior(arm,raw,{'reinforcement_context':'approachOwn57'})
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in ((0x3C8F4,0x3CB30),(0x3C740,0x3C748),(0x3CFC8,0x3CFEC),
                  (0x773D8,0x77E68),(0x3CB30,0x3CBF0)):
        assert arm[lo:hi]==clean[lo:hi]
    cpu,get=get_machine(arm,after);companies=get(0xCB160)
    player=companies+4+2*76;ally=companies+4+7*76;enemy=companies+4+8*76
    assert get(0x397D8,companies)==2
    assert get(0x3CB30,ally,2)==get(0x3CB30,enemy,2)==0 and get(0x3C740,ally)==21
    get(0x3C8F4,ally,2,1,8)
    get(0x3C8F4,enemy,2,2,21)
    assert get(0x3CB30,ally,2)==1 and get(0x3C740,ally)==8
    assert get(0x3CB30,enemy,2)==2
    native=bytes(cpu.mem_read(BASE,len(raw)))
    extra={player+0x1F+7,player+0x1F+8,ally+0x47}
    delta={BASE+i for i,(a,b) in enumerate(zip(after,native,strict=True)) if a!=b}
    assert delta==extra
    owned=set(receipt['owned_bytes'])|extra
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,native,strict=True)) if a!=b]
    assert len(owned)==19 and all(c['address'] in owned for c in changes)
    receipt.update(context='prepareAssistancePactAtFirstSight',owned_bytes=sorted(owned),changes=changes,
        original_relation_and_support_method=0x0203C8F4,
        original_assistance_setter=0x0203CB00,original_assistance_getter=0x0203C740,
        original_method_calls=[{'company_ID':7,'arguments':[2,1,8]},{'company_ID':8,'arguments':[2,2,21]}],
        source_native_faction_state_fields=sorted(extra),
        original_supporting_company_ID=7,original_existing_opponent_company_ID=8,
        source_native_relations={'company7_to_player':1,'company8_to_player':2},
        source_native_assistance_target=8,
        every_other_RAM_byte_including_all_actor_identities_and_ship_stats_exact=True,
        no_numeric_message_event_selection_or_battle_outcome_injection=True,
        fixture_sha256=sha(Path(__file__).read_bytes()),after_RAM_sha256=sha(native))
    return native,receipt
