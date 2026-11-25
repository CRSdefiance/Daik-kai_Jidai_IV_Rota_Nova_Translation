"""Keep reviewed closing phrases together in the scoped diplomacy formatter."""

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch import diplomatic_outcome_wrap_v1 as v1
from dk4tool.patch.grand_race_menu_release import sha


ENTRY = 0x01FFD180
NATIVE_WRAP = 0x01FFCA00
PHRASES = {
    353: 'fell through.',
    354: 'has been canceled.',
    359: 'truce offer!',
    367: 'against each other.',
    372: 'are going around.',
    375: 'received the letter.',
    377: 'market share.',
    378: 'market share.',
}
MASK = sum(1 << (number - v1.FIRST_ID) for number in PHRASES)
SUFFIXES = tuple(dict.fromkeys(PHRASES.values()))
TABLE = ', '.join(str(value) for value in (
    b''.join(bytes([len(phrase)]) + phrase.encode('ascii') for phrase in SUFFIXES) + b'\0'
))

# The native width logic reads its caller's stack. The paragraph body has an
# unused word at sp+4 and an output buffer at sp+8. The width code also reads
# the saved LR's Thumb bit. Preserve both and restore the temporary markers.
ASM = f'''
    ldr r3, [sp, #0xd0]
    ldr ip, ={v1.FIRST_ID}
    sub r3, r3, ip
    cmp r3, #31
    bhi {v1.PARAGRAPH_ENTRY:#x}
    ldr ip, ={MASK:#x}
    mov ip, ip, lsr r3
    tst ip, #1
    beq {v1.PARAGRAPH_ENTRY:#x}
    push {{r4-r6, lr}}
    adr r6, wrap
    ldr ip, =0x01ffc941
    bx ip
wrap:
    push {{r4-r8, lr}}
    mov r4, r0
    mov r5, r1
    mov r6, #0
measure:
    ldrb r0, [r4, r6]
    cmp r0, #0
    beq measured
    cmp r0, #31
    beq fallback
    add r6, r6, #1
    cmp r6, #236
    bls measure
    b fallback
measured:
    adr r7, suffixes
next_suffix:
    ldrb r8, [r7], #1
    cmp r8, #0
    beq fallback
    add r2, r7, r8
    subs r3, r6, r8
    blo advance
    subne ip, r3, #1
    ldrbne r0, [r4, ip]
    cmpne r0, #32
    bne advance
    add ip, r4, r3
    mov r0, r7
compare:
    ldrb r1, [ip], #1
    ldrb r8, [r0], #1
    cmp r1, r8
    bne advance
    cmp r0, r2
    blo compare
    mov r2, r3
    mov r8, #31
mark:
    ldrb r0, [r4, r2]
    cmp r0, #32
    strbeq r8, [r4, r2]
    add r2, r2, #1
    cmp r2, r6
    blo mark
    mov r0, r4
    mov r1, r5
    pop {{r4-r8, lr}}
    str lr, [sp, #4]
    adr lr, return_thumb
    orr lr, lr, #1
    b {NATIVE_WRAP:#x}
restore_markers:
    ldr lr, [sp, #4]
    mov r3, r4
restore_input:
    ldrb r2, [r3], #1
    cmp r2, #31
    moveq r2, #32
    strbeq r2, [r3, #-1]
    cmp r2, #0
    bne restore_input
    cmp r0, #0
    moveq r0, r4
    addeq r1, sp, #8
    beq {NATIVE_WRAP:#x}
    add r3, sp, #8
    mov r1, #0
restore_output:
    ldrb r2, [r3, r1]
    cmp r2, #31
    moveq r2, #32
    strbeq r2, [r3, r1]
    add r1, r1, #1
    cmp r1, r0
    blo restore_output
    bx lr
advance:
    mov r7, r2
    b next_suffix
fallback:
    mov r0, r4
    mov r1, r5
    pop {{r4-r8, lr}}
    b {NATIVE_WRAP:#x}
return_thumb:
    .hword 0x4778, 0x46c0
    b restore_markers
    .ltorg
suffixes:
    .byte {TABLE}
    .align 2
'''


def transform(source):
    prior, ownership = v1.transform(source)
    code = MainCodeFile(prior, v1.BASE)
    tail = code.sections[-1]
    prefix = bytes(tail.data)
    offset = v1.SELECTOR - tail.ramAddress
    assert tail.ramAddress + len(prefix) == ENTRY
    assembler = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    original = bytes(assembler.asm(v1.ASM, v1.SELECTOR)[0])
    assert prefix[offset:] == original
    scoped = v1.ASM.replace(f'{v1.PARAGRAPH_ENTRY:#x}', f'{ENTRY:#x}')
    selector = bytes(assembler.asm(scoped, v1.SELECTOR)[0])
    extension = bytes(assembler.asm(ASM, ENTRY)[0])
    assert len(original) == len(selector) and ENTRY + len(extension) <= v1.BASE
    changed = [(int.from_bytes(original[at:at + 4], 'little'),
                int.from_bytes(selector[at:at + 4], 'little'))
               for at in range(0, len(selector), 4) if original[at:at + 4] != selector[at:at + 4]]
    assert len(changed) == 4 and all(before >> 24 == after >> 24
                                    and (before >> 24) & 0xF == 0xA for before, after in changed)
    tail.data[offset:] = selector + extension
    target = bytes(code.save())

    restored = MainCodeFile(target, v1.BASE)
    assert bytes(restored.sections[-1].data) == prefix[:offset] + selector + extension
    restored.sections[-1].data[offset:] = original
    assert bytes(restored.save()) == prior
    return target, ownership | dict(target_ARM9_sha256=sha(target), phrase_entry=ENTRY,
        phrase_helper_bytes=len(extension), closing_phrases=PHRASES,
        existing_phrase_unaware_formatter_unchanged=True, previous_stage_inverse_exact=True)
