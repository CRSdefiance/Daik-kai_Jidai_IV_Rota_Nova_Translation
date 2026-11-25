"""Scope the existing literal portrait paragraph wrapper to the rumor exchange."""

from types import FunctionType

from dk4tool.patch import ship_emergency_wrap_v1 as previous


SOURCE = '866ae3e729c68538d63eed1005bef6b9f648bf164096856387bb966c1a56fd6a'
PRIOR = 0x01FFDC40
DYNAMIC = {
    (0x02053F40, 0x274): (0x021169C0, 0x02116A60, 0x02116AC0, 0x02116B20,
                          0x02116F00, 0x02117020, 0x02117100, 0x02117200),
    (0x02054014, 0x274): tuple(range(2796, 2806)),
}
HOOK = previous.HOOK
PARAGRAPH = previous.LITERAL_PARAGRAPH


def assembly():
    lines = ['push {r3}', 'ldr r3, [sp, #0x268]']
    for index, ((parent, _), _) in enumerate(DYNAMIC.items()):
        lines.extend((f'ldr ip, ={parent:#x}', 'cmp r3, ip', f'beq owner_{index}'))
    lines.append('b prior')
    for index, ((_, offset), ids) in enumerate(DYNAMIC.items()):
        lines.extend((f'owner_{index}:', f'ldr r3, [sp, #{offset + 4:#x}]'))
        for message in ids:
            lines.extend((f'ldr ip, ={message:#x}', 'cmp r3, ip', 'beq paragraph'))
        lines.append('b prior')
    lines.extend(('paragraph:', 'pop {r3}', f'b {PARAGRAPH:#x}',
                  'prior:', 'pop {r3}', f'b {PRIOR:#x}', '.ltorg'))
    return '\n'.join(lines)


def transform(source):
    native = FunctionType(previous.transform.__code__, vars(previous) | {
        'SOURCE': SOURCE, 'PRIOR': PRIOR, 'assembly': assembly})
    arm, proof = native(source)
    proof['dynamic'] = [dict(parent=parent, stack_selector_offset=offset, selectors=keys)
                        for (parent, offset), keys in DYNAMIC.items()]
    return arm, proof
