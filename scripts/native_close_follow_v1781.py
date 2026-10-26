"""Own-position-only following of original fleet8, bounded outside known ports."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_close_sighting_v1689 import apply_fixture as original_initial,water
from scripts.native_call_abi_v764 import call
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read,save

BASE=0x02000000
ROM=Path('out/all_routes_combined_v1775_candidate.nds')
ROOT=Path('work/analysis/close_follow_preflight_v1781')
SNAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/close_sighting_v1690_1676_closeReady8/frame_005100_arm9_ram.bin')
INITIAL={'sighting_context':'openWaterReady8'}
FOLLOW={'sighting_context':'followOpenWater8'}

def position(cpu,obj):
    vtable=struct.unpack('<I',cpu.mem_read(obj,4))[0]
    getter=struct.unpack('<I',cpu.mem_read(vtable+0x20,4))[0]
    output=0x02660000;cpu.mem_write(output,bytes(16))
    call(cpu,getter-BASE,(output,obj))
    return list(struct.unpack('<2i',cpu.mem_read(output,8))),getter

def apply_fixture(arm,raw,request):
    assert request in (INITIAL,FOLLOW) and len(raw)==0x400000
    assert sha(arm)==read('translations/lil_lessons_editorial_release_v1.json')['required_runtime_arm9_sha256']
    cpu,get=get_machine(arm,raw);root=get(0xCB1A8);own,enemy=root+4+132,root+4+8*132
    assert get(0x7F244)==get(0x2E58C)==1 and get(0x35320,own)==2 and get(0x35320,enemy)==8
    assert not cpu.mem_read(enemy+0x50,1)[0]&4,'Never reset an original seen flag'
    target,getter=position(cpu,enemy)
    assert target==list(struct.unpack('<2i',cpu.mem_read(enemy+0x34,8)))
    assert bytes(cpu.mem_read(BASE,0x400000))==raw
    mobile=get(0x36C70,own+12);assert mobile and get(0x564C8,mobile)
    initial=request==INITIAL
    if initial:
        result,prior=original_initial(arm,raw,{'sighting_context':'closeReady8'})
        assert prior['original_own_position_set_to_native_water_point']==target
        fields={int(k):bytes.fromhex(v)for k,v in prior['declared_fields'].items()}
        assert len(prior['owned_bytes'])==17
        terrain=prior['terrain']
    else:
        terrain=water(arm,[target]);assert terrain['queries'][0]['collision_free']
        fields={own+0x34:struct.pack('<2i',*target),mobile+16:struct.pack('<2i',*[v*128 for v in target])}
        result=bytearray(raw)
        for at,data in fields.items():result[at-BASE:at-BASE+len(data)]=data
        result=bytes(result)
    owned={at+i for at,data in fields.items()for i in range(len(data))}
    assert len(owned)==(17 if initial else 16)
    changes=[{'address':BASE+i,'before':a,'after':b}for i,(a,b)in enumerate(zip(raw,result,strict=True))if a!=b]
    assert all(r['address']in owned for r in changes)
    assert result[enemy-BASE:enemy-BASE+132]==raw[enemy-BASE:enemy-BASE+132]
    assert result[root-BASE+0x2080:root-BASE+0x2090]==raw[root-BASE+0x2080:root-BASE+0x2090]
    verify_cpu,verify=get_machine(arm,result)
    known_town=verify(0x78C60,1)
    assert known_town==115,('Refuse location inside known-town docking radius',known_town,target)
    assert bytes(verify_cpu.mem_read(BASE,0x400000))==result
    observed,_=position(verify_cpu,own);assert observed==target
    for at in (struct.unpack_from('<I',arm,0xD9858)[0],struct.unpack_from('<I',arm,0x51A20)[0]):
        assert not set(range(at,at+4))&owned and raw[at-BASE:at-BASE+4]==result[at-BASE:at-BASE+4]
    return result,{'context':request['sighting_context'],'owned_bytes':sorted(owned),'changes':changes,
        'declared_fields':{str(k):v.hex()for k,v in fields.items()},'original_enemy_fleet_ID':8,
        'original_virtual_position_getter':getter,'target_original_virtual_position':target,
        'native_known_town_scan':known_town,'no_known_town_within_original_docking_radius':True,
        'terrain':terrain,'terrain_runtime_ROM':'out/all_routes_combined_v1676_candidate.nds',
        'unchanged_source_terrain_and_runtime_inherited_from_V1676':True,
        'initial_source_diplomatic_prerequisite_only':initial,
        'initial_fixture_source':'scripts/native_close_sighting_v1689.py'if initial else None,
        'enemy_record_loaded_groups_seen_flags_RNG_actor_health_and_outcomes_exact':True,
        'all_other4MiB_bytes_exact_outside_declared_location_and_initial_relation_fields':True,
        'no_message_table_renderer_or_result_injection':True,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(result),'fixture_sha256':sha(Path(__file__).read_bytes())}

if __name__=='__main__':
    assert not ROOT.exists()
    image=NdsImage.open(ROM);old=NdsImage.open('out/all_routes_combined_v1676_candidate.nds')
    arm=image.read_file('/__arm9__.bin');assert old.read_file('/__arm9__.bin')==arm
    for path in ('/data/mapname.DK4',):
        if path in {p for _,p,_ in image.iter_files()}:assert image.read_file(path)==old.read_file(path)
    prior=read('work/analysis/close_sighting_negative_v1693/terminal_negative_close_range_proof.json')
    assert sha(SNAP.read_bytes())==next(r['RAM_sha256']for r in prior['states']if r['frame']==5100)
    raw=SNAP.read_bytes();after,receipt=apply_fixture(arm,raw,INITIAL)
    cpu,get=get_machine(arm,after);bearings=[]
    for x,y in ((0,0),(1,0),(2,2),(10,10),(32,32),(100,100)):
        addr=get(0x6567C,x,y);bearings.append({'relative_vector':[x,y],'argument_hex':cstring(after,addr).hex()})
    assert bearings[0]['argument_hex']==b'vicinity'.hex()
    ROOT.mkdir(parents=True)
    save(ROOT/'source_open_water_preflight.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'old_snapshot':str(SNAP),'old_snapshot_sha256':sha(raw),'old_snapshot_not_current_live_gameplay':True,
        'exact_runtime_unchanged_from_old_snapshot_ROM':True,'original_initial_proposed_fixture':receipt,
        'native_close_bearing_cases':bearings,
        'new_test_requirement':'Follow original moving fleet8 at one-frame intervals immediately while closing Info;stop before any known port radius ororiginal event selection.',
        'no_live_test_or_editorial_completion_credit':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'preflight_known_town':receipt['native_known_town_scan'],'owned_initial_bytes':17,
        'bearings':bearings,'no_gameplay_claim':True},flush=True)
