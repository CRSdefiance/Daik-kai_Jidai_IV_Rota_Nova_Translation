"""Separate controlled PRNG input for original daily-update comparison."""

import struct

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_item_roles_v789 import ARMS,set_condition as roles
from scripts.native_machine_scoped_v764 import machine

SEED=548127170
BASE=0x02000000


def set_condition(arm,raw,request):
    if request=={'mode':'item-and-letter-roles'}: return roles(arm,raw,request)
    if sha(arm) not in ARMS or len(raw)!=0x400000 or request!={'mode':'synchronize-post-acknowledgment-RNG'}:
        raise ValueError('Exact ROM and explicit post-acknowledgment PRNG input required')
    source=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x519D4:0x51A28]==source[0x519D4:0x51A28]
    assert arm[0xD9824:0xD9868]==source[0xD9824:0xD9868]
    address=struct.unpack_from('<I',arm,0xD9830)[0]
    assert address==struct.unpack_from('<I',arm,0xD9858)[0]==0x02168EB8
    cpu=machine(arm);cpu.mem_write(BASE,raw)
    before=bytes(cpu.mem_read(BASE,0x800000))
    call(cpu,0xD9824,(SEED,))
    after_native=bytes(cpu.mem_read(BASE,0x800000))
    changed={i for i,(a,b) in enumerate(zip(before,after_native,strict=True)) if a!=b}
    assert changed<=set(range(address-BASE,address-BASE+4))
    result=bytearray(raw)
    original=struct.unpack_from('<I',result,address-BASE)[0]
    struct.pack_into('<I',result,address-BASE,SEED)
    assert bytes(result)==after_native[:0x400000]
    changes=[{'address':BASE+i,'before':raw[i],'after':result[i]} for i in range(address-BASE,address-BASE+4) if raw[i]!=result[i]]
    return bytes(result),{'synthetic_identical_PRNG_input_fixture':True,'mode':request['mode'],
        'ARM9_sha256':sha(arm),'original_srand_function':0x020D9824,'PRNG_state_address':address,
        'reference_actual_V783_frame18800_seed':SEED,'prior_seed':original,'changes':changes,
        'only_original_srand_word_changes_entire8MiB':True,
        'source_rand_and_srand_sha256':sha(source[0xD9824:0xD9868]),
        'simulation_data_calendar_cash_documents_and_text_not_edited':True,
        'ordinary_random_stream_or_earned_daily_outcome_parity_not_claimed':True,
        'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(result)}
