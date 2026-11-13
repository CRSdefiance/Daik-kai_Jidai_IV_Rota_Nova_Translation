"""Localize only the original pirate portraits' nine bearing arguments."""

from hashlib import sha256

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile


BASE = 0x02000000
CALL, WRAPPER = 0x02077C80, 0x02053D44
TABLES = (0x021169A0, 0x02116A40)
BEARINGS = (
    (0x0214511C, b'vicinity', b'nearby'),
    (0x02145128, b'N', b'to the north'),
    (0x0214512C, b'NE', b'to the northeast'),
    (0x02145134, b'E', b'to the east'),
    (0x02145138, b'SE', b'to the southeast'),
    (0x02145140, b'S', b'to the south'),
    (0x02145144, b'SW', b'to the southwest'),
    (0x0214514C, b'W', b'to the west'),
    (0x02145150, b'NW', b'to the northwest'),
)


def install(arm, expected_sha):
    assert sha256(arm).hexdigest() == expected_sha
    code = MainCodeFile(arm, BASE)
    assert bytes(code.save()) == arm and len(code.sections) == 6
    main, tail = code.sections[0], code.sections[-1]
    assert main.ramAddress == BASE and not tail.bssSize
    at, start = CALL - BASE, tail.ramAddress + len(tail.data)
    for pointer, original, _ in BEARINGS:
        assert arm[pointer - BASE:pointer - BASE + len(original) + 1] == original + b'\0'
    names = {pointer: f'bearing_{i}' for i, (pointer, _, _) in enumerate(BEARINGS)}
    begin, stop = BEARINGS[0][0], BEARINGS[-1][0]
    table = ', '.join(f'{names[p]} - offsets' if p in names else '0' for p in range(begin, stop + 1, 4))
    words = '\n'.join(f'{names[p]}: .asciz "{english.decode("ascii")}"' for p, _, english in BEARINGS)
    assembly = f"""
        push {{r4}}
        ldr r4, ={TABLES[0]:#x}
        cmp r1, r4
        ldrne r4, ={TABLES[1]:#x}
        cmpne r1, r4
        bne original
        ldr ip, ={begin:#x}
        sub ip, r2, ip
        cmp ip, #{stop - begin}
        bhi original
        tst ip, #3
        bne original
        adr r4, offsets
        ldrb ip, [r4, ip, lsr #2]
        cmp ip, #0
        addne r2, r4, ip
    original:
        pop {{r4}}
        b {WRAPPER:#x}
    offsets: .byte {table}
    {words}
        .balign 4
        .ltorg
    """
    assembler = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    branch = bytes(assembler.asm(f'bl {WRAPPER:#x}', CALL)[0])
    assert main.data[at:at + 4] == branch
    payload = bytes(assembler.asm(assembly, start)[0])
    stop = start + len(payload)
    assert stop <= BASE and len(payload) % 4 == 0
    assert all(part.ramAddress + len(part.data) + part.bssSize <= start or stop <= part.ramAddress
               for part in code.sections)
    patched = bytes(assembler.asm(f'bl {start:#x}', CALL)[0])
    main.data[at:at + 4] = patched
    tail.data.extend(payload)
    candidate = bytes(code.save())
    inverse = MainCodeFile(candidate, BASE)
    assert inverse.sections[0].data[at:at + 4] == patched
    assert bytes(inverse.sections[-1].data[-len(payload):]) == payload
    inverse.sections[0].data[at:at + 4] = branch
    del inverse.sections[-1].data[-len(payload):]
    assert bytes(inverse.save()) == arm
    return candidate, dict(call=CALL, wrapper=WRAPPER, tables=list(TABLES), extension=start,
        bytes=len(payload), source_ARM9_sha256=expected_sha, target_ARM9_sha256=sha256(candidate).hexdigest(),
        original_call_hex=branch.hex(), localized_call_hex=patched.hex(), exact_inverse=True)
