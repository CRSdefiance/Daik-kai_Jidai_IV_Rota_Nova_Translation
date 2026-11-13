"""Select the registered equipment paragraph formatter for the removal result."""

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shared_notice_wrap_v1 import BASE, HOOK, NOTICE_PARENT


SOURCE = '121a4618571093adaea33ed2e267a268ad2eea4963566fb3f4d0975b39fa834d'
PRIOR = 0x01FFD0FC
EQUIPMENT_PARAGRAPH = 0x01FFD04C
MESSAGE = 329


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError('Exact registered Captain Biographies ARM9 required')
    code = MainCodeFile(source, BASE)
    assert len(code.sections) == 6 and bytes(code.save()) == source
    dispatcher, tail = code.sections[-2:]
    assert dispatcher.ramAddress == 0x01FFC000 and len(dispatcher.data) == 0x1000
    assert tail.ramAddress == 0x01FFD000 and not tail.bssSize
    start = tail.ramAddress + len(tail.data)
    offset = HOOK - dispatcher.ramAddress
    assembler = Ks(KS_ARCH_ARM, KS_MODE_ARM)

    def assemble(text, address):
        return bytes(assembler.asm(text, address)[0])

    old, new = (assemble(f'b {address:#x}', HOOK) for address in (PRIOR, start))
    assert dispatcher.data[offset:offset + 4] == old
    entry = EQUIPMENT_PARAGRAPH - tail.ramAddress
    assert bytes(tail.data[entry:entry + 16]).hex() == '70402de908609fe508c09fe51cff2fe1'
    payload = assemble(f'''
        ldr r3, [sp, #0xc4]
        ldr ip, ={NOTICE_PARENT:#x}
        cmp r3, ip
        bne {PRIOR:#x}
        ldr r3, [sp, #0xd0]
        ldr ip, ={MESSAGE}
        cmp r3, ip
        beq {EQUIPMENT_PARAGRAPH:#x}
        b {PRIOR:#x}
        .ltorg
    ''', start)
    stop = start + len(payload)
    assert stop <= BASE and len(payload) % 4 == 0
    assert all(section.ramAddress + len(section.data) + section.bssSize <= start
               or stop <= section.ramAddress for section in code.sections)
    dispatcher.data[offset:offset + 4] = new
    tail.data.extend(payload)
    target = bytes(code.save())

    inverse = MainCodeFile(target, BASE)
    assert bytes(inverse.sections[-1].data[-len(payload):]) == payload
    inverse.sections[-2].data[offset:offset + 4] = old
    del inverse.sections[-1].data[-len(payload):]
    assert bytes(inverse.save()) == source
    return target, dict(source_ARM9_sha256=SOURCE, target_ARM9_sha256=sha(target), hook=HOOK,
        selector=start, selector_bytes=len(payload), previous_selector=PRIOR, notice_parent=NOTICE_PARENT,
        message_ID=MESSAGE, reused_paragraph=EQUIPMENT_PARAGRAPH, serialized_parent_inverse_exact=True)
