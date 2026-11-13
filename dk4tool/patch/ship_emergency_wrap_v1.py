"""Wrap the original emergency reports and preserve literal ship-name arguments."""

from types import FunctionType

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.crew_loss_portrait_wrap_v1 import WRAPPER as LITERAL_PARAGRAPH
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.mutiny_static_wrap_v1 import assembly as static_assembly
from dk4tool.patch.sea_event_static_wrap_v1 import BASE, HOOK, LITERAL_COPY


SOURCE = '8dfa942f2f5e8ddd5888c0578c4bae9081d19557ee1d33e3ac288feb35618382'
PRIOR = 0x01FFD45C
STATIC = {(0x02053DB8, 0x27C): (0x02118620,), (0x02054014, 0x274): (609,)}
DYNAMIC = {(0x02053F40, 0x274): (0x02118600, 0x021185C0), (0x02053DB8, 0x27C): (0x02118580,)}


def assembly():
    source = FunctionType(static_assembly.__code__, {**static_assembly.__globals__, 'SCOPE': STATIC, 'PRIOR': PRIOR})()
    push = 'push {r3-r5}\n'
    assert source.startswith(push)
    out = []
    for i, ((parent, offset), keys) in enumerate(DYNAMIC.items()):
        out.extend(('ldr r3, [sp, #0x270]', f'ldr ip, ={parent:#x}', 'cmp r3, ip', f'bne next_dynamic_{i}',
                    f'ldr r3, [sp, #{offset + 12:#x}]'))
        for key in keys:
            out.extend((f'ldr ip, ={key:#x}', 'cmp r3, ip', 'beq dynamic_wrap'))
        out.append(f'next_dynamic_{i}:')
    out.append('b static_dispatch')
    out.extend(('dynamic_wrap:', 'pop {r3-r5}', f'b {LITERAL_PARAGRAPH:#x}', 'static_dispatch:'))
    return push + '\n'.join(out) + '\n' + source[len(push):]


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError('Exact registered mutiny ARM9 required')
    code = MainCodeFile(source, BASE)
    assert bytes(code.save()) == source and len(code.sections) == 6
    itcm, tail = code.sections[-2:]
    assert itcm.ramAddress == 0x01FFC000 and len(itcm.data) == 0x1000 and not tail.bssSize
    at = HOOK - itcm.ramAddress
    start = tail.ramAddress + len(tail.data)
    assembler = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    old = bytes(assembler.asm(f'b {PRIOR:#x}', HOOK)[0])
    assert itcm.data[at:at + 4] == old
    new = bytes(assembler.asm(f'b {start:#x}', HOOK)[0])
    payload = bytes(assembler.asm(assembly(), start)[0])
    stop = start + len(payload)
    assert stop <= BASE and len(payload) % 4 == 0
    assert all(section.ramAddress + len(section.data) + section.bssSize <= start or stop <= section.ramAddress
               for section in code.sections)
    itcm.data[at:at + 4] = new
    tail.data.extend(payload)
    target = bytes(code.save())
    inverse = MainCodeFile(target, BASE)
    assert bytes(inverse.sections[-1].data[-len(payload):]) == payload
    del inverse.sections[-1].data[-len(payload):]
    inverse.sections[-2].data[at:at + 4] = old
    assert bytes(inverse.save()) == source
    return target, dict(source_ARM9_sha256=sha(source), target_ARM9_sha256=sha(target),
        hook=HOOK, previous_selector=PRIOR, selector=start, selector_bytes=len(payload),
        dynamic_wrapper=LITERAL_PARAGRAPH, literal_copy=LITERAL_COPY,
        complete_serialized_ARM9_parent_inverse=True)
