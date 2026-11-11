"""Extend the registered literal-copy guard to three static sailing-alert tables."""

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.sea_event_static_wrap_v1 import ASM, BASE, QUEUED, SELECTOR, TABLES


SOURCE_SHA256 = 'dca374a6982027e523e3f2e4733c1c02aab4796f6321583a408a95b9ca6cb7ee'
NEW_TABLES = (0x02118760, 0x02118780, 0x021187A0)


def transform(source):
    if sha(source) != SOURCE_SHA256:
        raise ValueError('Exact registered sea-event ARM9 required')
    code = MainCodeFile(source, BASE)
    assert bytes(code.save()) == source and len(code.sections) == 6
    tail = code.sections[-1]
    offset = SELECTOR - tail.ramAddress
    assembler = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    original = bytes(assembler.asm(ASM, SELECTOR)[0])
    assert offset >= 0 and bytes(tail.data[offset:]) == original

    first, last = TABLES[QUEUED][0], TABLES[QUEUED][-1]
    original_check = f'''    ldr ip, ={first:#x}
    sub r3, r3, ip
    cmp r3, #{last - first}
    bhi fallback
    tst r3, #31
    bne fallback
'''
    assert ASM.count(original_check) == 1
    new_check = f'''    ldr ip, ={NEW_TABLES[0]:#x}
    sub r3, r3, ip
    cmp r3, #{last - NEW_TABLES[0]}
    bhi fallback
    tst r3, #31
    bne fallback
    cmp r3, #{NEW_TABLES[-1] - NEW_TABLES[0]}
    bls check
    cmp r3, #{first - NEW_TABLES[0]}
    blo fallback
'''
    updated = bytes(assembler.asm(ASM.replace(original_check, new_check), SELECTOR)[0])
    assert not tail.bssSize and SELECTOR + len(updated) <= BASE
    assert all(section.ramAddress + len(section.data) + section.bssSize <= SELECTOR
               or SELECTOR + len(updated) <= section.ramAddress for section in code.sections[:-1])
    tail.data[offset:] = updated
    target = bytes(code.save())

    inverse = MainCodeFile(target, BASE)
    assert bytes(inverse.sections[-1].data[offset:]) == updated
    inverse.sections[-1].data[offset:] = original
    assert bytes(inverse.save()) == source
    return target, dict(selector=SELECTOR, original_tables=TABLES, added_queued_tables=NEW_TABLES,
        source_selector_sha256=sha(original), target_selector_sha256=sha(updated),
        source_ARM9_sha256=sha(source), target_ARM9_sha256=sha(target),
        complete_serialized_ARM9_parent_inverse=True)
