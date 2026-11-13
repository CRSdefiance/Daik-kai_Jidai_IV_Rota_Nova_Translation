"""Send the scoped diplomacy notices to the existing modal word formatter."""

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha


BASE = 0x02000000
SOURCE_SHA256 = 'b6430c8c06a65f2a877bab814922cc2501cb9103c505d146d3b422f51ddd558c'
HOOK = 0x01FFC8EC
EXISTING_SELECTOR = 0x01FFD020
PARAGRAPH_ENTRY = 0x01FFD04C
SELECTOR = 0x01FFD0FC
NOTICE_PARENT = 0x020546E8
YES_NO_PARENT = 0x0205469C
NOTICE_IDS = (349, 351, 353, 354, 355, 357, 358, 359, 360, 361, 362, 363, 364,
              365, 366, 367, 369, 370, 372, 375, 377, 378, 379, 381, 382)
YES_NO_IDS = (350, 356)
FIRST_ID = 349
MASK = sum(1 << (number - FIRST_ID) for number in NOTICE_IDS if number < FIRST_ID + 32)

ASM = f'''
    ldr r3, [sp, #0xc4]
    ldr ip, ={NOTICE_PARENT:#x}
    cmp r3, ip
    beq notices
    ldr ip, ={YES_NO_PARENT:#x}
    cmp r3, ip
    bne {EXISTING_SELECTOR:#x}
    ldr r3, [sp, #0xd0]
    ldr ip, ={YES_NO_IDS[0]}
    cmp r3, ip
    beq {PARAGRAPH_ENTRY:#x}
    add ip, ip, #{YES_NO_IDS[1] - YES_NO_IDS[0]}
    cmp r3, ip
    beq {PARAGRAPH_ENTRY:#x}
    b {EXISTING_SELECTOR:#x}
notices:
    ldr r3, [sp, #0xd0]
    ldr ip, ={FIRST_ID}
    sub r3, r3, ip
    sub ip, r3, #32
    cmp ip, #1
    bls {PARAGRAPH_ENTRY:#x}
    cmp r3, #31
    bhi {EXISTING_SELECTOR:#x}
    ldr ip, ={MASK:#x}
    mov ip, ip, lsr r3
    tst ip, #1
    bne {PARAGRAPH_ENTRY:#x}
    b {EXISTING_SELECTOR:#x}
    .ltorg
'''


def transform(source):
    if sha(source) != SOURCE_SHA256:
        raise ValueError('Exact registered crew-notice ARM9 required')
    code = MainCodeFile(source, BASE)
    assert bytes(code.save()) == source and len(code.sections) == 6
    itcm, tail = code.sections[-2:]
    prefix = bytes(tail.data)
    assert itcm.ramAddress == 0x01FFC000 and len(itcm.data) == 0x1000
    assert tail.ramAddress + len(prefix) == SELECTOR and not tail.bssSize
    assembler = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    old = bytes(assembler.asm(f'b {EXISTING_SELECTOR:#x}', HOOK)[0])
    branch = bytes(assembler.asm(f'b {SELECTOR:#x}', HOOK)[0])
    allocation = bytes(assembler.asm(ASM, SELECTOR)[0])
    offset = HOOK - itcm.ramAddress
    assert itcm.data[offset:offset + 4] == old and len(allocation) % 4 == 0
    assert SELECTOR + len(allocation) <= BASE and all(
        section.ramAddress + len(section.data) + section.bssSize <= SELECTOR
        or SELECTOR + len(allocation) <= section.ramAddress for section in code.sections)
    itcm.data[offset:offset + 4] = branch
    tail.data.extend(allocation)
    target = bytes(code.save())

    restored = MainCodeFile(target, BASE)
    assert restored.sections[-2].data[offset:offset + 4] == branch
    assert bytes(restored.sections[-1].data) == prefix + allocation
    restored.sections[-2].data[offset:offset + 4] = old
    del restored.sections[-1].data[len(prefix):]
    assert bytes(restored.save()) == source
    return target, dict(source_ARM9_sha256=sha(source), target_ARM9_sha256=sha(target),
        hook=HOOK, original_selector=EXISTING_SELECTOR, selector=SELECTOR,
        selector_bytes=len(allocation), reused_paragraph_entry=PARAGRAPH_ENTRY,
        notice_IDs=NOTICE_IDS, yes_no_IDs=YES_NO_IDS, serialized_parent_inverse_exact=True)
