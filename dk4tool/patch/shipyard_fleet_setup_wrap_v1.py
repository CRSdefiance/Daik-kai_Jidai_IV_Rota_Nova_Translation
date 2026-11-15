"""Wrap local-news and admiral prompts only after their name arguments expand."""

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.equipment_removal_wrap_v1 import EQUIPMENT_PARAGRAPH, HOOK, NOTICE_PARENT
from dk4tool.patch.grand_race_menu_release import sha


BASE = 0x02000000
SOURCE = '8c97d0ed46d5497723f273cd9eef8816ed226c8a6aa8cd298f64a84834da542c'
PRIOR = 0x01FFD97C
YES_NO_PARENT = 0x0205469C
SCOPE = ((NOTICE_PARENT, 261), (YES_NO_PARENT, 279))


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError('Exact registered Equipment and System ARM9 required')
    code = MainCodeFile(source, BASE)
    assert len(code.sections) == 6 and bytes(code.save()) == source
    dispatcher, tail = code.sections[-2:]
    assert dispatcher.ramAddress == 0x01FFC000 and len(dispatcher.data) == 0x1000
    assert tail.ramAddress == 0x01FFD000 and not tail.bssSize
    assert EQUIPMENT_PARAGRAPH < PRIOR < tail.ramAddress + len(tail.data)
    start = tail.ramAddress + len(tail.data)
    offset = HOOK - dispatcher.ramAddress
    assembler = Ks(KS_ARCH_ARM, KS_MODE_ARM)

    def assemble(text, address):
        return bytes(assembler.asm(text, address)[0])

    old, new = (assemble(f'b {address:#x}', HOOK) for address in (PRIOR, start))
    assert dispatcher.data[offset:offset + 4] == old
    entry = EQUIPMENT_PARAGRAPH - tail.ramAddress
    assert bytes(tail.data[entry:entry + 16]).hex() == '70402de908609fe508c09fe51cff2fe1'
    instructions = []
    for i, (parent, message) in enumerate(SCOPE):
        instructions.extend(('ldr r3, [sp, #0xc4]', f'ldr ip, ={parent:#x}', 'cmp r3, ip', f'bne next_{i}',
                             'ldr r3, [sp, #0xd0]', f'ldr ip, ={message}', 'cmp r3, ip',
                             f'beq {EQUIPMENT_PARAGRAPH:#x}', f'next_{i}:'))
    instructions.extend((f'b {PRIOR:#x}', '.ltorg'))
    payload = assemble('\n'.join(instructions), start)
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
        selector=start, selector_bytes=len(payload), previous_selector=PRIOR, scoped_parent_message_pairs=SCOPE,
        reused_paragraph=EQUIPMENT_PARAGRAPH, serialized_parent_inverse_exact=True)
