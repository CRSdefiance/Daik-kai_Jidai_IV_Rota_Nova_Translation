"""Reuse the registered pirate bearing text for the three fleet-alert calls."""

from hashlib import sha256
from struct import unpack_from

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch import pirate_report_bearings_v1 as pirate


BASE = pirate.BASE
WRAPPER = pirate.WRAPPER
PIRATE_ENTRY = 0x01FFFAA4
MAPPER_ENTRY = 0x01FFFAB8
CALLSITES = {
    0x020775E8: (0x02118560,),
    0x020778D0: (0x02118560,),
    0x02077DDC: (0x02118560, 0x02118540),
}
TABLE_LITERALS = {
    0x02077770: 0x02118560,
    0x02077A4C: 0x02118560,
    0x02077ED4: 0x02118560,
    0x02077ED8: 0x02118540,
}
CALL_SCOPES = ((0x020775D8, 0x020775F0), (0x020778C0, 0x020778D8), (0x02077DB8, 0x02077DE4))
ORIGINAL_GUARD = bytes.fromhex('04402de5c8409fe5040051e1c4409f15040051110900001a')
FIRST_LITERAL, SECOND_LITERAL, WRAPPER_TAIL = 0x01FFFB78, 0x01FFFB7C, 0x01FFFAE8
BEARINGS = pirate.BEARINGS


def install(arm, clean, expected_sha):
    assert sha256(arm).hexdigest() == expected_sha
    code = MainCodeFile(arm, BASE)
    assert bytes(code.save()) == arm and len(code.sections) == 6
    main, tail = code.sections[0], code.sections[-1]
    assert main.ramAddress == BASE and not tail.bssSize
    assert tail.ramAddress + len(tail.data) == BASE - 4
    assembler = Ks(KS_ARCH_ARM, KS_MODE_ARM)

    def branch(address, target):
        return bytes(assembler.asm(f'bl {target:#x}', address)[0])

    for start, stop in CALL_SCOPES:
        lo, hi = start - BASE, stop - BASE
        assert arm[lo:hi] == clean[lo:hi]
    for pointer, value in TABLE_LITERALS.items():
        at = pointer - BASE
        assert unpack_from('<I', arm, at) == unpack_from('<I', clean, at) == (value,)
    for pointer, original, _ in BEARINGS:
        assert arm[pointer - BASE:pointer - BASE + len(original) + 1] == original + b'\0'

    pos = PIRATE_ENTRY - tail.ramAddress
    assert tail.data[pos:pos + len(ORIGINAL_GUARD)] == ORIGINAL_GUARD
    assert unpack_from('<2I', tail.data, FIRST_LITERAL - tail.ramAddress) == pirate.TABLES
    assert tail.data[WRAPPER_TAIL - tail.ramAddress:WRAPPER_TAIL - tail.ramAddress + 4] == bytes(
        assembler.asm(f'b {WRAPPER:#x}', WRAPPER_TAIL)[0])
    assert main.data[pirate.CALL - BASE:pirate.CALL - BASE + 4] == branch(pirate.CALL, PIRATE_ENTRY)

    # The pirate caller still checks the same two tables. Its guard can use ip
    # so the saved-r4 instruction can move to the common bearing entry.
    assert MAPPER_ENTRY == PIRATE_ENTRY + 20 and MAPPER_ENTRY + 4 == PIRATE_ENTRY + len(ORIGINAL_GUARD)
    guard = bytes(assembler.asm(f'''
        ldr ip, [pc, #{FIRST_LITERAL - PIRATE_ENTRY - 8}]
        cmp r1, ip
        ldrne ip, [pc, #{SECOND_LITERAL - PIRATE_ENTRY - 16}]
        cmpne r1, ip
        bne {WRAPPER_TAIL:#x}
        push {{r4}}
    ''', PIRATE_ENTRY)[0])
    assert len(guard) == len(ORIGINAL_GUARD)
    tail.data[pos:pos + len(guard)] = guard
    branches = []
    for address, tables in CALLSITES.items():
        at = address - BASE
        old, new = branch(address, WRAPPER), branch(address, MAPPER_ENTRY)
        assert main.data[at:at + 4] == old
        main.data[at:at + 4] = new
        branches.append(dict(address=address, tables=list(tables), before=old.hex(), after=new.hex()))
    result = bytes(code.save())
    assert len(result) == len(arm)
    undo = MainCodeFile(result, BASE)
    undo.sections[-1].data[pos:pos + len(guard)] = ORIGINAL_GUARD
    for row in branches:
        at = row['address'] - BASE
        undo.sections[0].data[at:at + 4] = bytes.fromhex(row['before'])
    assert bytes(undo.save()) == arm
    return result, dict(source_arm_sha256=expected_sha, target_arm_sha256=sha256(result).hexdigest(),
        changes=branches, pirate_entry=PIRATE_ENTRY, mapper_entry=MAPPER_ENTRY,
        guarded_pirate_tables=list(pirate.TABLES), old_guard=ORIGINAL_GUARD.hex(), new_guard=guard.hex(),
        unchanged_ARM9_length_and_section_arms=True, whole_ARM9_inverse_exact=True)

