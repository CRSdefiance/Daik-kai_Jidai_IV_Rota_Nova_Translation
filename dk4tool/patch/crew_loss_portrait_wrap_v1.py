"""Preserve literal ship names in the crew notices and format the three portrait tables."""

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha


BASE = 0x02000000
SOURCE_SHA256 = '6e18fd50a5d7c861c098b12a3eaba269b7f545285bc9309b68c323688bab7519'
ENTRY = 0x01FFCF3C
LEGACY = 0x02132020
WRAPPER = 0x02147B98
SELECTOR = 0x01FFD068
MODAL_EXIT = 0x01FFD048
MODAL_FALLBACK = 0x01FFC900
SCOPE = {0x02053F40: (0x02116EE0, 0x02116F60), 0x02053EF4: (0x02117000,)}

ASM = '''
    push {r3}
    ldr r3, [sp, #0x268]
    ldr ip, =0x02053f40
    cmp r3, ip
    beq notice
    ldr ip, =0x02053ef4
    cmp r3, ip
    bne legacy
    ldr r3, [sp, #0x278]
    ldr ip, =0x02117000
    cmp r3, ip
    beq wrap
    b legacy
notice:
    ldr r3, [sp, #0x278]
    ldr ip, =0x02116ee0
    cmp r3, ip
    beq wrap
    ldr ip, =0x02116f60
    cmp r3, ip
    beq wrap
legacy:
    pop {r3}
    b 0x02132020
wrap:
    pop {r3}
    b 0x02147b98
    .ltorg
'''
MODAL_ASM = '''
    sub ip, r3, #336
    sub ip, ip, #2
    cmp ip, #1
    bhi 0x01ffc900
    push {lr}
    bl 0x01ff9fac
    mov r0, #0
    pop {pc}
'''


def transform(source):
    if sha(source) != SOURCE_SHA256:
        raise ValueError('Exact registered shared-notice ARM9 required')
    code = MainCodeFile(source, BASE)
    assert bytes(code.save()) == source
    itcm, tail = code.sections[-2:]
    prefix = bytes(tail.data)
    assert len(code.sections) == 6 and tail.ramAddress + len(prefix) == SELECTOR
    assert itcm.ramAddress == 0x01FFC000 and len(itcm.data) == 0x1000
    assembler = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    old = bytes(assembler.asm(f'b {LEGACY:#x}', ENTRY)[0])
    new = bytes(assembler.asm(f'b {SELECTOR:#x}', ENTRY)[0])
    portrait = bytes(assembler.asm(ASM, SELECTOR)[0])
    modal = SELECTOR + len(portrait)
    extension = portrait + bytes(assembler.asm(MODAL_ASM, modal)[0])
    at = ENTRY - itcm.ramAddress
    modal_at = MODAL_EXIT - tail.ramAddress
    old_modal = bytes(assembler.asm(f'bhi {MODAL_FALLBACK:#x}', MODAL_EXIT)[0])
    new_modal = bytes(assembler.asm(f'bhi {modal:#x}', MODAL_EXIT)[0])
    assert itcm.data[at:at + 4] == old and len(extension) % 4 == 0
    assert tail.data[modal_at:modal_at + 4] == old_modal
    assert SELECTOR + len(extension) <= BASE and all(
        section.ramAddress + len(section.data) + section.bssSize <= SELECTOR
        or SELECTOR + len(extension) <= section.ramAddress for section in code.sections)
    itcm.data[at:at + 4] = new
    tail.data[modal_at:modal_at + 4] = new_modal
    tail.data.extend(extension)
    target = bytes(code.save())
    restored = MainCodeFile(target, BASE)
    assert restored.sections[-2].data[at:at + 4] == new
    expected_tail = prefix[:modal_at] + new_modal + prefix[modal_at + 4:] + extension
    assert bytes(restored.sections[-1].data) == expected_tail
    restored.sections[-2].data[at:at + 4] = old
    restored.sections[-1].data[modal_at:modal_at + 4] = old_modal
    del restored.sections[-1].data[len(prefix):]
    assert bytes(restored.save()) == source
    return target, dict(source_ARM9_sha256=sha(source), target_ARM9_sha256=sha(target),
        entry=ENTRY, legacy=LEGACY, selector=SELECTOR, selector_bytes=len(extension),
        native_wrap_entry=WRAPPER, pairs=[(parent, table) for parent, tables in SCOPE.items() for table in tables],
        modal_exit=MODAL_EXIT, modal_literal_copy_selector=modal, literal_notice_IDs=[338, 339],
        earlier_ITCM_allocation_preserved_except_one_scoped_branch=True, complete_serialized_parent_inverse=True)
