"""Source-defined historic-site facility flag,discovery and calendar inputs."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_ceremony_access_fixture_v810 import set_condition as discovered_fixture
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE


def set_condition(arm,raw,request):
    assert set(request)=={'mode','day'} and request['mode']=='ceremony-site-access'
    after,prior=discovered_fixture(arm,raw,dict(mode='ceremony-discovered-site',day=request['day']))
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert all(arm[a:b]==clean[a:b] for a,b in ((0xB5050,0xB508C),(0xB811C,0xB8174),(0x2B0C4,0x2B0F0)))
    u=machine(arm);u.mem_write(BASE,after)
    def get(fn,args=()):
        call(u,fn,args,instruction_limit=300000)
        return u.reg_read(UC_ARM_REG_R0)
    town=get(0xB6618);assert get(0xB65E4)==22
    at=town+12;before=struct.unpack_from('<I',after,at-BASE)[0]
    old_count=get(0xB811C);old_flag=get(0xB507C,(town,11))
    get(0xB5050,(town,11,1))
    value=struct.unpack('<I',u.mem_read(at,4))[0]
    assert value==before|(1<<11) and get(0xB507C,(town,11))==1<<11
    assert get(0xB811C)==9
    result=bytearray(after);struct.pack_into('<I',result,at-BASE,value)
    changes=[dict(address=BASE+i,before=a,after=b) for i,(a,b) in enumerate(zip(raw,result,strict=True)) if a!=b]
    allowed={r['address'] for r in prior['changes']}|set(range(at,at+4))
    assert all(r['address'] in allowed for r in changes)
    return bytes(result),dict(synthetic_ceremony_facility_access_fixture=True,
        discovery_and_clock_inputs=prior,town_ID=22,site_index=8,facility_type=11,
        original_facility_setter=BASE+0xB5050,original_facility_predicate=BASE+0xB507C,
        original_icon_count_callback=BASE+0xB811C,old_icon_count=old_count,new_icon_count=9,
        town_facility_mask_address=at,before_facility_mask=before,after_facility_mask=value,
        before_facility11_flag=old_flag,after_facility11_flag=1<<11,
        only_calendar_word_site_discovery_flag_and_town_facility_mask_owned=True,
        source_UI_state_dialogue_eligibility_handlers_effects_and_time_functions_not_replaced=True,
        earned_access_discovery_fame_calendar_or_campaign_progress_not_claimed=True,
        all_other4MiB_bytes_exact=True,changes=changes,
        before_RAM_sha256=sha(raw),after_RAM_sha256=sha(result),ARM9_sha256=sha(arm))
