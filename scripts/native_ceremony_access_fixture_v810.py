"""Original discovery flag plus the previously verified calendar fixture."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_ceremony_fixture_v809 import set_condition as calendar_fixture
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE


def set_condition(arm,raw,request):
    assert set(request)=={'mode','day'} and request['mode']=='ceremony-discovered-site'
    after,clock=calendar_fixture(arm,raw,dict(mode='ceremony-day',day=request['day']))
    source=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert all(arm[a:b]==source[a:b] for a,b in ((0x60DEC,0x60E4C),(0x87318,0x873F4)))
    u=machine(arm);u.mem_write(BASE,after)
    def get(fn,args=()):
        call(u,fn,args,instruction_limit=300000)
        return u.reg_read(UC_ARM_REG_R0)
    town=get(0xB6618);town_id=get(0xB65E4);site=get(0xB5170,(town,))
    assert town_id==22 and site==8
    obj=get(0xCB16C)+4+8*site;at=obj+4
    assert BASE<=at<BASE+len(after)
    before=after[at-BASE]
    # Execute the original discovery method independently. It may award fame
    # in this private machine; only its proven site flag is copied below.
    reward=get(0x87318,(obj,town_id,11))
    native=bytes(u.mem_read(at,1))[0];assert native==before|1
    result=bytearray(after);result[at-BASE]=native
    changes=[dict(address=BASE+i,before=a,after=b) for i,(a,b) in enumerate(zip(raw,result,strict=True)) if a!=b]
    allowed={r['address'] for r in clock['changes']}|{at}
    assert all(r['address'] in allowed for r in changes)
    return bytes(result),dict(synthetic_ceremony_discovered_site_fixture=True,
        source_clock_fixture=clock,original_site_object=obj,site_index=site,town_ID=town_id,
        flag_address=at,before_site_flags=before,after_site_flags=native,
        original_discovery_method=BASE+0x87318,original_discovery_method_reward_not_applied=reward,
        only_calendar_word_and_one_original_discovery_flag_owned=True,
        original_eligibility_UI_speaker_dialogue_selection_outcomes_and_time_handler_unchanged=True,
        earned_discovery_fame_time_or_daily_updates_not_claimed=True,
        all_other4MiB_bytes_exact=True,changes=changes,
        before_RAM_sha256=sha(raw),after_RAM_sha256=sha(result),ARM9_sha256=sha(arm))
