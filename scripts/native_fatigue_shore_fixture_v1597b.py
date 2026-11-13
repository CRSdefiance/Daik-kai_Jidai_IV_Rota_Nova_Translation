"""Isolated40-byte own-fleet location fixture at a source-verified expedition shore."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROM=Path('out/all_routes_combined_v1594_candidate.nds')
ROOT=Path('work/analysis/fatigue_shore_fixture_v1597b')
CONTEXT=Path('work/analysis/fatigue_shore_context_v1587c/original_region_land_and_legal_shore_queries.json')
REQUEST={'fatigue_search_context':'source_verified_region3_shore_before_Search'}
def apply_fixture(arm,raw,request):
    assert request==REQUEST and len(raw)==0x400000
    assert sha(arm)==read('work/analysis/fatigue_status_release_v1593/registered_release_verification.json')['ARM9_sha256']
    context=read(CONTEXT);shore=context['chosen_shore']
    assert shore['map_point']==[5292,3724] and shore['collision_free'] and shore['original_search_has_adjacent_land'] and shore['original_event_region']==3
    cpu,get=get_machine(arm,raw);fleets=get(0xCB1A8)
    assert get(0x2E58C)==get(0x7F244)==1 and struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12))==(0,0,0)
    after=bytearray(raw);owned=set();ships=[]
    for slot in range(5):
        mobile=get(0x36C70,fleets+4+132+12+8*slot)
        assert mobile and get(0x564C8,mobile)
        health=[get(0x5543C,mobile),get(0x55444,mobile)]
        assert health==([60,49] if slot==0 else [25,19])
        old=struct.unpack('<2i',cpu.mem_read(mobile+16,8))
        at=mobile+16;value=struct.pack('<2i',*[x*128 for x in shore['map_point']])
        after[at-0x02000000:at-0x02000000+8]=value;owned.update(range(at,at+8))
        ships.append({'slot':slot,'mobile':mobile,'original_fixed_position':list(old),'test_fixed_position':list(struct.unpack('<2i',value)),'Hull_Crew_preserved':health})
    after=bytes(after);changes=[{'address':0x02000000+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b]
    assert len(owned)==40 and all(c['address'] in owned for c in changes)
    return after,{'context':'source_verified_region3_Search_shore','owned_bytes':sorted(owned),'changes':changes,'ships':ships,
        'shore_context':str(CONTEXT),'shore_context_sha256':sha(CONTEXT.read_bytes()),'source_verified_shore':shore,
        'only_original_five_own_mobile_coordinate_fields_changed':True,'all_other4MiB_bytes_including_fatigue_RNG_actors_roles_health_and_event_choices_exact':True,
        'artificial_location_fixture_not_earned_travel_discovery_or_event':True,'no_numeric_message_outcome_or_event_ID_injected':True,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(after),'fixture_sha256':sha(Path(__file__).read_bytes())}
if __name__=='__main__':
    assert not ROOT.exists()
    raw=Path('E:/Rota Nova translations/Generated/work/emulation_v193/fatigue_search_pilot_v1587b_1578/frame_005000_arm9_ram.bin').read_bytes()
    after,proof=apply_fixture(NdsImage.open(ROM).read_file('/__arm9__.bin'),raw,REQUEST)
    ROOT.mkdir(parents=True);save(ROOT/'preflight.json',proof)
    print('40 coordinate bytes only;source region3 legal water adjacent to land;fatigue,actors,health,RNG and event choice unchanged.')
