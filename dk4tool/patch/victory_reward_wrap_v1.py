"""Reuse the modal word wrapper with protected reward phrases."""

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch import diplomatic_outcome_wrap_v2 as phrases
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shared_notice_wrap_v1 import BASE, HOOK, NOTICE_PARENT


PRIOR = 0x01FFDBC0
EXTENT = 0x01FFB860
ENTRY = 0x01FFBAF0
PROTECTED = (b"from captured ships.", b"gold.")


def assembly():
    helper = phrases.ASM[phrases.ASM.index("\nwrap:\n"):]
    table = f"    .byte {phrases.TABLE}\n"
    tokens = b"".join(bytes([len(text)]) + text for text in PROTECTED) + b"\0"
    assert helper.count(table) == 1
    helper = helper.replace(table, f"    .byte {', '.join(map(str, tokens))}\n")
    match = "    cmp r0, r2\n    blo compare\n    mov r2, r3\n"
    assert helper.count(match) == 1
    # After matching "gold.", also protect the preceding decimal token.
    # The separator before that token stays available to the native wrapper.
    helper = helper.replace(match, """
    cmp r0, r2
    blo compare
    sub r8, r2, r7
    cmp r8, #5
    bne matched
    cmp r3, #2
    blo fallback
    sub ip, r3, #2
    ldrb r0, [r4, ip]
    cmp r0, #48
    blo fallback
    cmp r0, #57
    bhi fallback
scan_amount:
    cmp ip, #0
    beq fallback
    sub r8, ip, #1
    ldrb r0, [r4, r8]
    cmp r0, #32
    beq amount_start
    cmp r0, #48
    blo fallback
    cmp r0, #57
    bhi fallback
    mov ip, r8
    b scan_amount
amount_start:
    sub r8, r3, ip
    cmp r8, #11
    bhi fallback
    mov r3, ip
matched:
    mov r2, r3
""".lstrip("\n"))
    return f"""
    ldr r3, [sp, #0xc4]
    ldr ip, ={NOTICE_PARENT:#x}
    cmp r3, ip
    bne {PRIOR:#x}
    ldr r3, [sp, #0xd0]
    ldr ip, =301
    cmp r3, ip
    addne ip, ip, #4
    cmpne r3, ip
    bne {PRIOR:#x}
    push {{r4-r6, lr}}
    adr r6, wrap
    ldr ip, =0x01ffc941
    bx ip
{helper}"""


def transform(source, exact_source_sha256):
    if sha(source) != exact_source_sha256:
        raise ValueError("Exact registered reward wrap input required")
    code = MainCodeFile(source, BASE)
    assert bytes(code.save()) == source
    itcm = next(section for section in code.sections if section.ramAddress == 0x01FFC000)
    extension = next(section for section in code.sections if section.ramAddress == EXTENT)
    assert not extension.bssSize and extension.ramAddress + len(extension.data) == ENTRY
    assembler = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    payload = bytes(assembler.asm(assembly(), ENTRY)[0])
    end = ENTRY + len(payload)
    assert all(section is extension or end <= section.ramAddress
               or section.ramAddress + len(section.data) + section.bssSize <= ENTRY for section in code.sections)
    at = HOOK - itcm.ramAddress
    old_branch = bytes(assembler.asm(f"b {PRIOR:#x}", HOOK)[0])
    assert itcm.data[at:at + 4] == old_branch
    itcm.data[at:at + 4] = bytes(assembler.asm(f"b {ENTRY:#x}", HOOK)[0])
    extension.data.extend(payload)
    target = bytes(code.save())
    del extension.data[-len(payload):]
    itcm.data[at:at + 4] = old_branch
    assert bytes(code.save()) == source
    return target, dict(hook=HOOK, previous_dispatch=PRIOR, selector=ENTRY, end=end,
                        original_notice_parent=NOTICE_PARENT, scoped_message_IDs=[301, 305], complete_ARM9_inverse=True)
