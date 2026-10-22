"""Private causal control: omit only the scheduler's discarded RAND call.

This is not a production fix. It removes timing-dependent seed pumping after
the final climb acknowledgment, without supplying actor/town outcomes or seed
values. The source immediately overwrites RAND's return with zero. The normal
generator, growth, daily updates, calendar and later simulation still execute.
"""

import struct

from keystone import Ks,KS_ARCH_ARM,KS_MODE_ARM

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_ceremony_athens_fixture_v816 import set_condition as eligibility
from scripts.verify_village_wrap_v608 import read

BASE=0x02000000
AT=BASE+0xC9DA0


def source_arm(arm):
    ceremony=read('translations/ceremony_editorial_release_v1.json')
    fmt=read('translations/levelup_stat_format_release_v1.json')
    if sha(arm)==fmt['target_arm9_sha256']:
        restored=bytearray(arm)
        for r in fmt['owned_patches']:
            at=r['address']-BASE;after=bytes.fromhex(r['after_hex']);before=bytes.fromhex(r['before_hex'])
            assert arm[at:at+len(after)]==after
            restored[at:at+len(before)]=before
        assert sha(bytes(restored))==ceremony['target_arm9_sha256']
        return bytes(restored)
    assert sha(arm) in (ceremony['source_arm9_sha256'],ceremony['target_arm9_sha256'])
    return arm


def set_condition(arm,raw,request):
    mapped=source_arm(arm)
    if request.get('mode')=='ceremony-Athens':
        after,receipt=eligibility(mapped,raw,request)
        if mapped!=arm:
            receipt.update(ARM9_sha256=sha(arm),same_source_native_eligibility_spans_under_V820_format_only_repack=True,
                original_guarded_eligibility_adapter_ARM9_sha256=sha(mapped))
        return after,receipt
    assert request=={'mode':'post-climb-disable-unused-yield-RAND'} and len(raw)==0x400000
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0xC9D98:0xC9DF0]==clean[0xC9D98:0xC9DF0]
    assert raw[0xC9D98:0xC9DF0]==arm[0xC9D98:0xC9DF0]
    ka=Ks(KS_ARCH_ARM,KS_MODE_ARM)
    before=bytes(ka.asm('bl 0x020d9834',AT)[0]);after_code=bytes(ka.asm('mov r0,r0',AT)[0])
    assert arm[AT-BASE:AT-BASE+4]==before
    assert arm[0xC9DA8:0xC9DAC]==bytes(ka.asm('mov r0,#0',BASE+0xC9DA8)[0])
    after=bytearray(raw);after[AT-BASE:AT-BASE+4]=after_code
    changes=[dict(address=BASE+i,before=a,after=b) for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b]
    assert all(AT<=r['address']<AT+4 for r in changes)
    return bytes(after),dict(synthetic_discarded_yield_RAND_control=True,mode=request['mode'],
        ARM9_sha256=sha(arm),callsite=AT,source_instruction=before.hex(),control_instruction=after_code.hex(),
        changes=changes,source_random_return_immediately_overwritten_with_zero=True,
        only4_instruction_bytes_change_no_seed_or_persistent_data_supplied=True,
        normal_generator_growth_daily_updates_time_and_wait_logic_unmodified=True,
        not_a_production_fix_and_not_ordinary_random_outcome_equivalence=True,
        before_RAM_sha256=sha(raw),after_RAM_sha256=sha(bytes(after)))
