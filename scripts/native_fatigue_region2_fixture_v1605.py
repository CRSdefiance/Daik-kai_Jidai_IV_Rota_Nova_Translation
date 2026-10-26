"""48-byte source-region2 location fixture with original event/RNG outcomes."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROM=Path('out/all_routes_combined_v1594_candidate.nds')
ROOT=Path('work/analysis/fatigue_region2_fixture_v1605')
CONTEXT=Path('work/analysis/fatigue_region2_shore_v1604/original_region_land_and_legal_shore_queries.json')
REQUEST={'fatigue_search_context':'coherent_source_region2_fleet_and_mobile_shore'}

def apply_fixture(arm,raw,request):
    assert request==REQUEST and len(raw)==0x400000
    assert sha(arm)==read('work/analysis/fatigue_status_release_v1593/registered_release_verification.json')['ARM9_sha256']
    shore=read(CONTEXT)['chosen_shore']
    assert shore['map_point']==[33500,5464] and shore['collision_free'] and shore['original_search_has_adjacent_land'] and shore['original_event_region']==2
    cpu,get=get_machine(arm,raw);fleets=get(0xCB1A8)
    assert get(0x2E58C)==get(0x7F244)==1 and struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12))==(0,0,0)
    fleet=fleets+4+132;after=bytearray(raw);owned=set();ships=[]
    for slot in range(5):
        mobile=get(0x36C70,fleet+12+8*slot);assert mobile and get(0x564C8,mobile)
        health=[get(0x5543C,mobile),get(0x55444,mobile)];assert health==([60,49] if slot==0 else [25,19])
        at=mobile+16;old=struct.unpack('<2i',cpu.mem_read(at,8));value=struct.pack('<2i',*[x*128 for x in shore['map_point']])
        after[at-0x02000000:at-0x02000000+8]=value;owned.update(range(at,at+8))
        ships.append({'slot':slot,'mobile':mobile,'original_fixed_position':list(old),'test_fixed_position':list(struct.unpack('<2i',value)),'Hull_Crew_preserved':health})
    vt=struct.unpack('<I',cpu.mem_read(fleet,4))[0];getter=struct.unpack('<I',cpu.mem_read(vt+0x20,4))[0];assert getter==0x0202C1C4
    out=0x02470000;get(getter-0x02000000,out,fleet);old=struct.unpack('<2i',cpu.mem_read(out,8))
    assert old==struct.unpack('<2i',cpu.mem_read(fleet+0x34,8))
    at=fleet+0x34;after[at-0x02000000:at-0x02000000+8]=struct.pack('<2i',*shore['map_point']);owned.update(range(at,at+8))
    after=bytes(after);assert len(owned)==48
    changes=[{'address':0x02000000+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b]
    assert all(c['address'] in owned for c in changes)
    check,query=get_machine(arm,after);query(getter-0x02000000,out,fleet)
    assert struct.unpack('<2i',check.mem_read(out,8))==tuple(shore['map_point']) and query(0x797A0,out)==2
    return after,{'context':'coherent_source_region2_shore','owned_bytes':sorted(owned),'changes':changes,'ships':ships,'fleet':fleet,
        'original_virtual_point_getter':getter,'original_cached_point':list(old),'test_cached_point':shore['map_point'],
        'shore_context':str(CONTEXT),'shore_context_sha256':sha(CONTEXT.read_bytes()),'source_verified_shore':shore,
        'only_original_five_mobile40_and_cached_fleet8_coordinate_bytes_owned':True,
        'all_other4MiB_bytes_including_fatigue_RNG_actors_roles_health_and_event_choices_exact':True,
        'artificial_location_fixture_not_earned_travel_discovery_or_event':True,'no_numeric_message_outcome_or_event_ID_injected':True,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(after),'fixture_sha256':sha(Path(__file__).read_bytes())}

if __name__=='__main__':
    assert not ROOT.exists()
    raw=Path('E:/Rota Nova translations/Generated/work/emulation_v193/fatigue_search_pilot_v1587b_1578/frame_005000_arm9_ram.bin').read_bytes()
    after,proof=apply_fixture(NdsImage.open(ROM).read_file('/__arm9__.bin'),raw,REQUEST)
    ROOT.mkdir(parents=True);save(ROOT/'preflight.json',proof)
    print('48 coordinate bytes only;source region2 shore,all other4MiB exact;original Search outcomes unchanged.')
