"""Disposable post-acknowledgment RNG caller trace; no production-ROM change.

At the explicit18200-frame pause, reuse the alternate-header code span as a
four-record direct-generator trace bank. An entry sentinel rejects evidence if that header path
is used afterward. The original generator resumes after its displaced seed
address load; operands, PRNG, stat data and calendars are not supplied.
Probe validity additionally requires matching uninstrumented game-state/RNG
controls. Instrumentation timing is not assumed transparent.
"""

import struct
from pathlib import Path

from keystone import Ks,KS_ARCH_ARM,KS_MODE_ARM

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_ceremony_athens_fixture_v816 import set_condition as eligibility
from scripts.verify_village_wrap_v608 import read

BASE=0x02000000
START,END,HOOK=BASE+0x7E3A8,BASE+0x7E448,BASE+0xD9834
ROOT=Path('work/analysis/ceremony_rand_v822')

ASM='''str lr,header_hit
b 0x0207e448
trace:
push {r0-r3,ip,lr}
adr r0,counter
ldr r1,[r0]
add r1,r1,#1
str r1,[r0]
and r1,r1,#3
adr r2,ring
add r2,r2,r1,lsl#4
ldr r1,[sp,#20]
str r1,[r2]
str r4,[r2,#4]
ldr r1,[sp,#28]
str r1,[r2,#12]
ldr r3,seed_address
ldr r1,[r3]
str r1,[r2,#8]
pop {r0-r3,ip,lr}
ldr r3,seed_address
b 0x020d9838
seed_address: .word 0x02168eb8
counter: .word 0
header_hit: .word 0
ring: .space 64
'''


def assembled():
    ka=Ks(KS_ARCH_ARM,KS_MODE_ARM)
    code=bytes(ka.asm(ASM,START)[0]);assert len(code)==END-START==160
    hook=bytes(ka.asm(f'b {START+8}',HOOK)[0]);assert len(hook)==4
    return {START:code,HOOK:hook}


def decode(raw):
    at=START-BASE
    counter,header=struct.unpack_from('<2I',raw,at+88)
    records=[]
    for n in range(max(1,counter-3),counter+1):
        caller,context_r4,seed,caller_stack_word=struct.unpack_from('<4I',raw,at+96+(n&3)*16)
        records.append(dict(sequence=n,caller_return=caller,callsite=caller-4,
            context_r4=context_r4,seed_before_generator=seed,caller_stack_word=caller_stack_word))
    return dict(total_generator_calls=counter,unexpected_alternate_header_return=header,last_four_calls=records)


def set_condition(arm,raw,request):
    if request.get('mode')=='ceremony-Athens':return eligibility(arm,raw,request)
    cfg=read('translations/ceremony_editorial_release_v1.json')
    assert sha(arm) in (cfg['source_arm9_sha256'],cfg['target_arm9_sha256']) and len(raw)==0x400000
    assert request=={'mode':'post-climb-RAND-callers'}
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[HOOK-BASE:HOOK-BASE+0x34]==clean[HOOK-BASE:HOOK-BASE+0x34]
    assert arm[START-BASE:END-BASE]==clean[START-BASE:END-BASE]
    assert raw[START-BASE:END-BASE]==arm[START-BASE:END-BASE]
    assert raw[HOOK-BASE:HOOK-BASE+4]==arm[HOOK-BASE:HOOK-BASE+4]
    after=bytearray(raw);allowed=set()
    for at,code in assembled().items():
        after[at-BASE:at-BASE+len(code)]=code
        allowed.update(range(at-BASE,at-BASE+len(code)))
    changes=[dict(address=BASE+i,before=a,after=b) for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b]
    assert all(c['address']-BASE in allowed for c in changes)
    assert raw[0x168EB8:0x168EBC]==after[0x168EB8:0x168EBC]
    assert decode(after)==dict(total_generator_calls=0,unexpected_alternate_header_return=0,last_four_calls=[])
    return bytes(after),dict(synthetic_read_only_value_RNG_instrumentation=True,
        mode=request['mode'],ARM9_sha256=sha(arm),temporary_code_span=[START,END],generator_entry=HOOK,
        changes=changes,ring_record_capacity=4,
        no_PRNG_actor_town_calendar_funds_inventory_or_native_outcome_supplied=True,
        no_production_ROM_registry_or_saved_donor_changes=True,
        unused_header_sentinel_and_uninstrumented_control_checks_required=True,
        code_ASM=ASM,before_RAM_sha256=sha(raw),after_RAM_sha256=sha(bytes(after)),
        producer_sha256=sha(Path(__file__).read_bytes()))
