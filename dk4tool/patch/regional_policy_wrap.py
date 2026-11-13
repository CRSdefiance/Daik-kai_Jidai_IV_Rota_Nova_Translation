"""Route all eight regional policy notices through the existing guarded wrapper."""

import json
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha

SOURCE = 'a5eb5fda8fc13f49e75466dcc4e5139a0a9b85e664ec2b970a2a9a51aad52cd3'
ADDRESS, SIZE = 0x01FFC900, 128
ASM = '''ldr r3,[sp,#0xc4]
ldr ip,parent
cmp r3,ip
bne fallback
ldr r3,[sp,#0xd0]
sub r3,r3,#320
cmp r3,#1
cmpne r3,#7
beq active
add r3,r3,#320
sub r3,r3,#127
cmp r3,#7
bhi fallback
active:
push {r4-r6,lr}
sub sp,sp,#240
mov r4,r0
bl 0x02053914
mov r0,r4
mov r1,sp
bl 0x01ffca00
cmp r0,#0
beq done
add r2,r0,#1
mov r0,r4
mov r1,sp
bl 0x020cec74
done:
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
        raise ValueError('Regional word wrapping requires the complete pinned V615 ARM9')
    code = MainCodeFile(source, 0x02000000)
    before = [bytes(s.data) for s in code.sections]
    assert len(before) == 5 and code.sections[4].ramAddress == 0x01FFC000 and len(before[4]) == 4096
    ks = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    at = ADDRESS - code.sections[4].ramAddress
    compiled = bytes(ks.asm(ASM, ADDRESS)[0])
    assert len(compiled) == 124
    compiled += bytes(ks.asm('nop', ADDRESS + len(compiled))[0])
    assert len(compiled) == SIZE
    # Original owner is the existing scoped modal wrapper, including its
    # literal pool and terminal zero word; no adjacent helper is consumed.
    assert before[4][at:at + 4] == bytes.fromhex('c4309de5')
    assert before[4][at + 0x70:at + 0x7C] == bytes.fromhex('e84605024101000047010000')
    assert before[4][at + 0x7C:at + SIZE] == bytes(4)
    code.sections[4].data[at:at + SIZE] = compiled
    result = bytes(code.save())
    parsed = MainCodeFile(result, 0x02000000)
    assert all(bytes(parsed.sections[i].data) == before[i] for i in range(4))
    restored = bytearray(parsed.sections[4].data)
    restored[at:at + SIZE] = before[4][at:at + SIZE]
    assert restored == before[4]
    return result, {'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(result),
                    'owned_original_modal_wrapper': [ADDRESS, ADDRESS + SIZE],
                    'original_modal_parent_return': 0x020546E8,
                    'added_native_message_IDs': list(range(127, 135)),
                    'retained_existing_modal_message_IDs': [321, 327],
                    'existing_paragraph_word_wrapper': 0x01FFCA00,
                    'original_macro_expander_always_runs_first': 0x02053914,
                    'original_fallback_dispatcher': 0x01FF9CE4,
                    'ASM_sha256': sha(ASM.encode('ascii')),
                    'only_existing128_byte_wrapper_changes_no_section_pool_cache_growth': True,
                    'changed_records': ['COMMON_REGIONAL_POLICY_FAMILY_GUARDED_WORD_WRAP'],
                    'experimental': True, 'full_goal_complete': False}


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-regional-policy-wrap-v1'
    target, proof = transform(source)
    if config['proof'] != proof:
        raise ValueError('Regional word-wrap source,scope or complete target differs')
    return target, proof
