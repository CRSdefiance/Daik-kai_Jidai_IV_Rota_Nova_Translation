"""Add the four ship-captain instructions to the existing modal word wrapper."""

from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.regional_policy_wrap import ADDRESS, SIZE
from dk4tool.patch.regional_policy_wrap import ASM as PREVIOUS_ASM
from scripts.verify_village_wrap_v608 import read

SOURCE = '54e35ccaf340a40506a98b0bc3fb7b14091eacac3548fe305d8e553922aa8da1'
ASM = '''ldr r3,[sp,#0xc4]
ldr ip,parent
cmp r3,ip
bne fallback
ldr r3,[sp,#0xd0]
sub r3,r3,#127
cmp r3,#7
bls active
sub r3,r3,#142
cmp r3,#3
bls active
sub r3,r3,#52
cmp r3,#0
cmpne r3,#6
bne fallback
active:
push {r4-r6,lr}
sub sp,sp,#240
mov r4,r0
bl 0x02053914
mov r0,r4
mov r1,sp
bl 0x01ffca00
cmp r0,#0
addne r2,r0,#1
movne r0,r4
movne r1,sp
blne 0x020cec74
mov r0,#0
add sp,sp,#240
pop {r4-r6,pc}
fallback:
b 0x01ff9ce4
parent:
.word 0x020546e8
'''


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError('Captain modal wrap requires the complete pinned V640 ARM9')
    code = MainCodeFile(source, 0x02000000)
    before = [bytes(s.data) for s in code.sections]
    assert len(before) == 5 and code.sections[4].ramAddress == 0x01FFC000 and len(before[4]) == 4096
    ks = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    old = bytes(ks.asm(PREVIOUS_ASM, ADDRESS)[0]) + bytes(ks.asm('nop', ADDRESS + 124)[0])
    new = bytes(ks.asm(ASM, ADDRESS)[0])
    assert len(old) == len(new) == SIZE == 128
    at = ADDRESS - code.sections[4].ramAddress
    assert before[4][at:at + SIZE] == old
    code.sections[4].data[at:at + SIZE] = new
    result = bytes(code.save())
    after = MainCodeFile(result, 0x02000000)
    assert all(bytes(after.sections[i].data) == before[i] for i in range(4))
    restored = bytearray(after.sections[4].data)
    restored[at:at + SIZE] = old
    assert bytes(restored) == before[4]
    return result, {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(result),
                    'owned_wrapper': [ADDRESS, ADDRESS + SIZE],
                    'exact_original_modal_parent_return': 0x020546E8,
                    'added_native_message_IDs': list(range(269, 273)),
                    'retained_native_message_IDs': [*range(127, 135), 321, 327],
                    'unchanged_original_macro_expander': 0x02053914,
                    'unchanged_paragraph_helper': 0x01FFCA00,
                    'unchanged_fallback_dispatcher': 0x01FF9CE4,
                    'new_ASM_sha256': sha(ASM.encode('ascii')),
                    'old_ASM_sha256': sha(PREVIOUS_ASM.encode('ascii')),
                    'only128_existing_ITCM_bytes_change_no_growth': True,
                    'all_prose_fonts_graphics_native_tables_and_pool_bytes_unchanged': True,
                    'changed_records': ['COMMON_CAPTAIN_INSTRUCTIONS_MODAL_WORD_WRAP'],
                    'experimental': True, 'full_goal_complete': False}


def apply_release(source, path):
    config = read(Path(path))
    assert config['format'] == 'dk4-captain-prompt-wrap-v1'
    target, proof = transform(source)
    if config['proof'] != proof:
        raise ValueError('Captain modal wrapper source,scope or target differs')
    return target, proof
