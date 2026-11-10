"""Keep the Square's temporary bitmap off the live ASCII helper instructions."""

import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.square_caption_cells import paint

BASE = 0x02000000
ENTRY, END = 0x01FFC388, 0x01FFC504
OLD_BUFFER = 0x01FFC1A0
ORIGINAL = 0x0239AFEC


def stack_painter():
    # The eight saved registers and 448-byte local preserve 8-byte alignment.
    # All fallback branches precede the allocation. The native painter consumes
    # the temporary view synchronously; the original view is restored on return.
    source = '''
push {r4-r10,lr}
mov r4,r0
mov r10,r1
ldr r5,[r4,#44]
cmp r5,#0
beq fallback
ldr r6,[r5,#16]
cmp r6,#0
beq fallback
ldr r2,[r6]
cmp r2,#4
bne fallback
ldr r2,[r6,#4]
cmp r2,#16
bne fallback
ldr r2,[r6,#8]
cmp r2,#12
bne fallback
ldr r2,[r5,#40]
cmp r2,#64
bne fallback
ldr r2,[r5,#44]
cmp r2,#12
bne fallback
ldmib r4,{r2,r3}
orr r2,r2,r3
ldr r3,[r4,#36]
orr r2,r2,r3
ldr r3,[r4,#40]
orrs r2,r2,r3
bne fallback
ldr r2,[r4,#12]
cmp r2,#64
bne fallback
ldr r2,[r4,#16]
cmp r2,#12
bne fallback
ldr r7,[r6,#16]
add r7,r6,r7
sub sp,sp,#448
mov r8,sp
mov r2,#4
str r2,[r8]
mov r2,#17
str r2,[r8,#4]
mov r2,#12
str r2,[r8,#8]
ldr r2,[r6,#12]
add r2,r6,r2
sub r2,r2,r8
str r2,[r8,#12]
mov r2,#20
str r2,[r8,#16]
mov r0,r7
add r1,r8,#20
mov r2,#12
copy_in_row:
mov r3,#16
copy_in_halfword:
ldrh r9,[r0],#2
strh r9,[r1],#2
subs r3,r3,#1
bne copy_in_halfword
mov r9,#0
strh r9,[r1],#2
subs r2,r2,#1
bne copy_in_row
str r8,[r5,#16]
mov r2,#68
str r2,[r5,#40]
str r2,[r4,#12]
mov r0,r4
mov r1,r10
bl ORIGINAL
mov r10,r0
str r6,[r5,#16]
mov r2,#64
str r2,[r5,#40]
str r2,[r4,#12]
add r0,r8,#20
mov r1,r7
mov r2,#12
copy_out_row:
mov r3,#16
copy_out_halfword:
ldrh r9,[r0],#2
strh r9,[r1],#2
subs r3,r3,#1
bne copy_out_halfword
add r0,r0,#2
subs r2,r2,#1
bne copy_out_row
mov r0,r10
add sp,sp,#448
pop {r4-r10,pc}
fallback:
mov r0,r4
mov r1,r10
pop {r4-r10,lr}
b ORIGINAL
'''.replace('ORIGINAL', str(ORIGINAL))
    body = bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(source, ENTRY)[0])
    if len(body) != END - ENTRY:
        raise ValueError('Square scratch repair must retain the exact helper span')
    return body


def propose(source):
    sections = MainCodeFile(source, BASE).sections
    section = sections[4]
    if section.ramAddress != 0x01FFC000 or len(section.data) != 4096:
        raise ValueError('Unexpected fixed helper section')
    offset = ENTRY - section.ramAddress
    old = paint(ENTRY, OLD_BUFFER, ORIGINAL)
    if bytes(section.data[offset:offset + len(old)]) != old:
        raise ValueError('Exact inherited Square bitmap painter required')
    physical = source.find(bytes(section.data))
    if physical < 0 or source.find(bytes(section.data), physical + 1) >= 0:
        raise ValueError('Helper section does not have unique physical storage')
    start = physical + offset
    body = stack_painter()
    target = bytearray(source)
    target[start:start + len(body)] = body
    restored = bytearray(target)
    restored[start:start + len(old)] = old
    if restored != source:
        raise ValueError('Repair changed unowned ROM bytes')
    return bytes(target), dict(
        source_ARM9_sha256=sha(source), target_ARM9_sha256=sha(target),
        helper_address=ENTRY, helper_end=END, helper_file_offset=start,
        helper_bytes=len(body), helper_sha256=sha(body),
        former_static_scratch=[OLD_BUFFER, OLD_BUFFER + 448],
        font_helper_preserved=[0x01FFC200, 0x01FFC300],
        temporary_stack_bytes=448, saved_register_bytes=32,
        stack_alignment=8, temporary_header_and_pixels_bytes=428,
        original_fallback_before_allocation=True,
        font_glyphs_metrics_and_all_other_code_preserved=True,
        all_section_extents_and_staged_payload_preserved=True,
        changed_records=['SQUARE_BITMAP_SCRATCH_OFF_ASCII_CODE'])


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-square-font-scratch-20261027-v1':
        raise ValueError('Unsupported Square/font scratch repair')
    for name, digest in config['dependencies'].items():
        if sha(Path(name).read_bytes()) != digest:
            raise ValueError('Square scratch dependency changed: ' + name)
    if sha(source) != config['source_ARM9_sha256']:
        raise ValueError('Exact reported punctuation/font predecessor required')
    target, proof = propose(source)
    if proof != config['proof'] or sha(target) != config['target_ARM9_sha256']:
        raise ValueError('Square scratch repair differs from registered proof')
    return target, proof


def validate_storage(source):
    """Reject the demonstrated collision even in a newly derived profile."""
    instruction = struct.unpack_from('<I', source, 0xD16CC)[0]
    if instruction & 0x0F000000 != 0x0B000000:
        return dict(applicable=False)
    delta = instruction & 0xFFFFFF
    if delta & 0x800000:
        delta -= 0x1000000
    destination = BASE + 0xD16CC + 8 + delta * 4
    if not OLD_BUFFER <= destination < OLD_BUFFER + 448:
        return dict(applicable=False)
    section = MainCodeFile(source, BASE).sections[4]
    offset = ENTRY - section.ramAddress
    if bytes(section.data[offset:offset + END - ENTRY]) != stack_painter():
        raise ValueError('ASCII helper overlaps the Square bitmap scratch; the per-call scratch repair is required')
    return dict(applicable=True, ASCII_helper=destination,
        Square_scratch='448-byte per-call stack buffer', runtime_code_and_bitmap_disjoint=True)
