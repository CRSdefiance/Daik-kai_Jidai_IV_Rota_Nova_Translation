"""Localize the five fixed target names at the original special victory call."""

from hashlib import sha256

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile


BASE = 0x02000000
CALL, WRAPPER, TABLE = 0x02071DBC, 0x02053D44, 0x021183C0
ALIASES = (
    ('化魚', 'Monster Fish'), ('大イカ', 'Giant Squid'), ('サメ', 'Shark'),
    ('白鯨', 'White Whale'), ('幽霊船', 'Ghost Ship'), ('Ghost', 'Ghost Ship'),
)


def install(arm, expected_sha):
    assert sha256(arm).hexdigest() == expected_sha
    code = MainCodeFile(arm, BASE)
    assert len(code.sections) == 6 and bytes(code.save()) == arm
    main, tail = code.sections[0], code.sections[-1]
    assert main.ramAddress == BASE and not tail.bssSize
    at, start = CALL - BASE, tail.ramAddress + len(tail.data)
    records, strings = [], []
    for index, (original, english) in enumerate(ALIASES):
        old = original.encode('cp932')
        assert len(old) < 8 and len(english) <= 18
        slot = ', '.join(str(n) for n in old.ljust(8, b'\0'))
        records.append(f'.byte {slot}\n.word alias_{index}')
        strings.append(f'alias_{index}: .asciz "{english}"')
    records, strings = '\n'.join(records), '\n'.join(strings)
    assembly = f"""
        cmp r2, #0
        beq original
        push {{r3-r7}}
        adr r4, aliases
        mov r7, #{len(ALIASES)}
    next_alias:
        mov r5, r4
        mov r6, r2
    next_byte:
        ldrb ip, [r5], #1
        ldrb r3, [r6], #1
        cmp ip, r3
        bne mismatch
        cmp ip, #0
        bne next_byte
        ldr r2, [r4, #8]
        b found
    mismatch:
        add r4, r4, #12
        subs r7, r7, #1
        bne next_alias
    found:
        pop {{r3-r7}}
    original:
        b {WRAPPER:#x}
    aliases:
        {records}
    {strings}
        .balign 4
    """
    assembler = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    original = bytes(assembler.asm(f'bl {WRAPPER:#x}', CALL)[0])
    assert main.data[at:at + 4] == original
    assert main.data[0x71F04:0x71F08] == TABLE.to_bytes(4, 'little')
    branch = bytes(assembler.asm(f'bl {start:#x}', CALL)[0])
    payload = bytes(assembler.asm(assembly, start)[0])
    stop = start + len(payload)
    assert stop <= BASE and len(payload) % 4 == 0
    assert all(section.ramAddress + len(section.data) + section.bssSize <= start or stop <= section.ramAddress
               for section in code.sections)
    main.data[at:at + 4] = branch
    tail.data.extend(payload)
    result = bytes(code.save())
    inverse = MainCodeFile(result, BASE)
    assert inverse.sections[0].data[at:at + 4] == branch
    assert inverse.sections[-1].data[-len(payload):] == payload
    inverse.sections[0].data[at:at + 4] = original
    del inverse.sections[-1].data[-len(payload):]
    assert bytes(inverse.save()) == arm
    return result, dict(call=CALL, wrapper=WRAPPER, table=TABLE, extension=start, bytes=len(payload),
        original_call_hex=original.hex(), localized_call_hex=branch.hex(), exact_inverse=True,
        source_ARM9_sha256=expected_sha, target_ARM9_sha256=sha256(result).hexdigest())
