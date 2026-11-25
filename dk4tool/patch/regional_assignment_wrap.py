"""Guard the original three-field regional order notification after expansion."""

import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_hook import branch_link

SOURCE = '6405fc1a888cbc5318246ab0ef664d3993567dd3149e189bc9781180e7bcda08'
ADDRESS, END, HOOK = 0x01FFC828, 0x01FFC900, 0x54798
ASM = '''ldr r3,[sp,#0xc4]
ldr ip,parent
cmp r3,ip
bne fallback
ldr r3,[sp,#0xcc]
ldr ip,caller
cmp r3,ip
bne fallback
push {r4-r8,lr}
sub sp,sp,#240
mov r4,r0
bl 0x02053914
mov r5,r4
mov r6,sp
mov r7,#0
mov r8,#0
next:
cmp r7,#236
bhs reject
ldrb r3,[r5],#1
cmp r3,#0
beq commit
cmp r3,#10
beq newline
cmp r3,#32
blo reject
strb r3,[r6],#1
add r7,r7,#1
b next
newline:
cmp r7,#233
bhi reject
add r8,r8,#1
cmp r8,#2
bhi reject
strb r3,[r6],#1
mov r3,#32
strb r3,[r6],#1
strb r3,[r6],#1
add r7,r7,#3
b next
commit:
cmp r8,#2
bne reject
strb r3,[r6]
mov r0,r4
mov r1,sp
add r2,r7,#1
bl 0x020cec74
reject:
mov r0,#0
add sp,sp,#240
pop {r4-r8,pc}
fallback:
b 0x01ffc900
parent:
.word 0x02054764
caller:
.word 0x0208ae38
'''


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError('Regional assignment guards require complete pinned V616 ARM9')
    code = MainCodeFile(source, 0x02000000)
    before = [bytes(s.data) for s in code.sections]
    assert len(before) == 5 and code.sections[4].ramAddress == 0x01FFC000 and len(before[4]) == 4096
    section = code.sections[4]
    at, span = ADDRESS - section.ramAddress, END - ADDRESS
    assert before[4][at:at + span] == bytes(span)
    # The preceding name-editor helper returns at C820; C824 is its literal.
    # There is no fall-through from that function into this original zero gap.
    assert before[4][0x820:0x828] == bytes.fromhex('7080bde800c6ff01')
    units = [(s.ramAddress, bytes(s.data)) for s in code.sections]
    clean = NdsImage.open('work/clean.nds')
    units += [(s.ramAddress, bytes(s.data)) for s in loadOverlayTable(
        clean.rom.arm9OverlayTable, lambda _, index: clean.rom.files[index]).values()]
    aliases = [(base + i, struct.unpack_from('<I', data, i)[0]) for base, data in units
               for i in range(len(data) - 3) if ADDRESS <= struct.unpack_from('<I', data, i)[0] < END]
    if aliases:
        raise ValueError('Regional notification gap has an existing unaligned reference')
    ks = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    compiled = bytes(ks.asm(ASM, ADDRESS)[0])
    if len(compiled) > span:
        raise ValueError(f'Complete notification wrapper needs {len(compiled)} bytes in {span}')
    assert len(compiled) % 4 == 0
    section.data[at:at + span] = compiled.ljust(span, b'\0')
    assert struct.unpack_from('<I', source, HOOK)[0] == branch_link(0x02000000 + HOOK, END)
    assert struct.unpack_from('<I', source, 0x8AE34)[0] == branch_link(0x0208AE34, 0x0205473C)
    struct.pack_into('<I', code.sections[0].data, HOOK, branch_link(0x02000000 + HOOK, ADDRESS))
    result = bytes(code.save())
    parsed = MainCodeFile(result, 0x02000000)
    assert all(bytes(parsed.sections[i].data) == before[i] for i in (1, 2, 3))
    restored = bytearray(parsed.sections[0].data)
    restored[HOOK:HOOK + 4] = before[0][HOOK:HOOK + 4]
    assert restored == before[0]
    helper = bytearray(parsed.sections[4].data)
    helper[at:at + span] = before[4][at:at + span]
    assert helper == before[4]
    return result, {'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(result),
                    'original_owned_zero_gap': [ADDRESS, END], 'compiled_bytes': len(compiled),
                    'all_original_unaligned_main_autoload_overlay_aliases': aliases,
                    'original_macro_call': HOOK, 'original_macro_expander': 0x02053914,
                    'exact_notification_parent_return': 0x02054764, 'exact_original_assignment_caller': 0x0208AE38,
                    'other_callers_tail_to_unchanged_V616_dispatcher': END,
                    'original_three_fields_and_all_text_preserved_two_guards_after_each_LF': True,
                    'scratch_bytes': 240, 'max_output_bytes_before_NUL': 235,
                    'all_section_extents_staged_pool_cache_startup_arenas_and_other_bytes_preserved': True,
                    'ASM_sha256': sha(ASM.encode('ascii')),
                    'changed_records': ['REGIONAL_ORDER_CONFIRMATION_FAMILY_GUARDED_NEWLINES'],
                    'experimental': True, 'full_goal_complete': False}


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-regional-assignment-wrap-v1'
    target, proof = transform(source)
    if config['proof'] != proof:
        raise ValueError('Regional assignment source,ownership,scope or target differs')
    return target, proof
