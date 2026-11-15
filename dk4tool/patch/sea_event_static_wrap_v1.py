"""Keep compiler-generated row breaks in scoped sea-event portrait text."""

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha


BASE = 0x02000000
SOURCE_SHA256 = '3a371296ed3b4a1a02df711bd3b1daf27134170120ba08ce8068b77deec628f9'
HOOK = 0x01FFCF3C
PRIOR = 0x01FFD068
SELECTOR = 0x01FFD36C
LITERAL_COPY = 0x01FF9FAC
QUEUED, CAPTAIN = 0x02053DB8, 0x02053C14
TABLES = {QUEUED: tuple(range(0x02118800, 0x02118980, 32)), CAPTAIN: (0x02116730,)}
MAXIMUM_TEMPLATE = 120

# R1 points to the original formatted input. Match a compiler-generated LF
# with two continuation spaces only inside the owned source voice tables.
# These compiled templates contain no source substitutions or macro tokens.
ASM = f'''
    push {{r3-r5}}
    ldr r3, [sp, #0x270]
    ldr ip, ={QUEUED:#x}
    cmp r3, ip
    beq queued
    ldr ip, ={CAPTAIN:#x}
    cmp r3, ip
    bne fallback
    ldr r3, [sp, #0x27c]
    ldr ip, ={TABLES[CAPTAIN][0]:#x}
    cmp r3, ip
    bne fallback
    b check
queued:
    ldr r3, [sp, #0x288]
    ldr ip, ={TABLES[QUEUED][0]:#x}
    sub r3, r3, ip
    cmp r3, #{TABLES[QUEUED][-1] - TABLES[QUEUED][0]}
    bhi fallback
    tst r3, #31
    bne fallback
check:
    ldrb r3, [r1]
    cmp r3, #32
    bne fallback
    add r4, r1, #1
    add r5, r1, #{MAXIMUM_TEMPLATE - 2}
scan:
    cmp r4, r5
    bhs fallback
    ldrb r3, [r4], #1
    cmp r3, #0
    beq fallback
    cmp r3, #10
    bne scan
    ldrb r3, [r4]
    cmp r3, #32
    ldrbeq r3, [r4, #1]
    cmpeq r3, #32
    bne fallback
    pop {{r3-r5}}
    b {LITERAL_COPY:#x}
fallback:
    pop {{r3-r5}}
    b {PRIOR:#x}
    .ltorg
'''


def transform(source):
    if sha(source) != SOURCE_SHA256:
        raise ValueError('Exact registered diplomacy ARM9 required')
    code = MainCodeFile(source, BASE)
    assert bytes(code.save()) == source and len(code.sections) == 6
    itcm, tail = code.sections[-2:]
    prefix = bytes(tail.data)
    assert itcm.ramAddress == 0x01FFC000 and len(itcm.data) == 0x1000
    assert tail.ramAddress + len(prefix) == SELECTOR and not tail.bssSize
    assembler = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    branch = bytes(assembler.asm(f'b {SELECTOR:#x}', HOOK)[0])
    original = bytes(assembler.asm(f'b {PRIOR:#x}', HOOK)[0])
    extension = bytes(assembler.asm(ASM, SELECTOR)[0])
    offset = HOOK - itcm.ramAddress
    assert itcm.data[offset:offset + 4] == original and len(extension) % 4 == 0
    assert SELECTOR + len(extension) <= BASE and all(
        section.ramAddress + len(section.data) + section.bssSize <= SELECTOR
        or SELECTOR + len(extension) <= section.ramAddress for section in code.sections)
    itcm.data[offset:offset + 4] = branch
    tail.data.extend(extension)
    target = bytes(code.save())

    restored = MainCodeFile(target, BASE)
    assert bytes(restored.sections[-1].data) == prefix + extension
    assert restored.sections[-2].data[offset:offset + 4] == branch
    restored.sections[-2].data[offset:offset + 4] = original
    del restored.sections[-1].data[len(prefix):]
    assert bytes(restored.save()) == source
    return target, dict(source_ARM9_sha256=sha(source), target_ARM9_sha256=sha(target),
        hook=HOOK, prior=PRIOR, selector=SELECTOR, selector_bytes=len(extension),
        tables=TABLES, maximum_template_bytes=MAXIMUM_TEMPLATE, literal_copy=LITERAL_COPY,
        complete_serialized_ARM9_parent_inverse=True)
