"""Coherent48-byte own-fleet location fixture; all outcomes remain original."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_fatigue_shore_fixture_v1597b as prior
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import save

ROM=prior.ROM
ROOT=Path('work/analysis/fatigue_shore_fixture_v1602')
REQUEST={'fatigue_search_context':'coherent_region3_fleet_and_mobile_shore'}

def apply_fixture(arm,raw,request):
    assert request==REQUEST
    after,old=prior.apply_fixture(arm,raw,prior.REQUEST)
    cpu,get=get_machine(arm,raw);fleet=get(0xCB1A8)+4+132*get(0x2E58C)
    vt=struct.unpack('<I',cpu.mem_read(fleet,4))[0]
    getter=struct.unpack('<I',cpu.mem_read(vt+0x20,4))[0];assert getter==0x0202C1C4
    out=0x02470000;get(getter-0x02000000,out,fleet)
    before=struct.unpack('<2i',cpu.mem_read(out,8))
    assert before==struct.unpack('<2i',cpu.mem_read(fleet+0x34,8))
    shore=old['source_verified_shore']['map_point'];after=bytearray(after);at=fleet+0x34
    after[at-0x02000000:at-0x02000000+8]=struct.pack('<2i',*shore)
    after=bytes(after);owned=set(old['owned_bytes'])|set(range(at,at+8));assert len(owned)==48
    changes=[{'address':0x02000000+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b]
    assert all(c['address'] in owned for c in changes)
    check,query=get_machine(arm,after);query(getter-0x02000000,out,fleet)
    assert struct.unpack('<2i',check.mem_read(out,8))==tuple(shore) and query(0x797A0,out)==3
    return after,{'context':'coherent_region3_fleet_cached_and_five_mobile_coordinates','owned_bytes':sorted(owned),'changes':changes,
        'mobile_fixture_proof':old,'fleet':fleet,'original_virtual_point_getter':getter,'original_cached_point':list(before),'test_cached_point':shore,
        'only_original_five_mobile40_and_cached_fleet8_coordinate_bytes_owned':True,
        'all_other4MiB_bytes_including_fatigue_RNG_actors_roles_health_and_event_choices_exact':True,
        'artificial_location_fixture_not_earned_travel_discovery_or_event':True,
        'no_numeric_message_outcome_or_event_ID_injected':True,'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(after),
        'fixture_sha256':sha(Path(__file__).read_bytes())}

if __name__=='__main__':
    assert not ROOT.exists()
    raw=Path('E:/Rota Nova translations/Generated/work/emulation_v193/fatigue_search_pilot_v1587b_1578/frame_005000_arm9_ram.bin').read_bytes()
    after,proof=apply_fixture(NdsImage.open(ROM).read_file('/__arm9__.bin'),raw,REQUEST)
    ROOT.mkdir(parents=True);save(ROOT/'preflight.json',proof)
    print('48 coordinate bytes owned;original virtual getter sees region3 shore;all other4MiB exact.')
