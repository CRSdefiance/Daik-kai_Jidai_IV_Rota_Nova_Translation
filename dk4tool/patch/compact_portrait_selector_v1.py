"""Add portrait table scopes while sharing the exact preceding break guard."""

from types import FunctionType

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch import ship_emergency_wrap_v1 as native


def shared_guard(arm, receipt):
    selector = receipt['selector']
    fallback = receipt['previous_selector']
    original_static = {tuple(key): tuple(values) for key, values in receipt['literal_scopes']}
    original_dynamic = {tuple(key): tuple(values) for key, values in receipt['dynamic_scopes']}
    reproduce = FunctionType(native.assembly.__code__, vars(native) | {
        'STATIC': original_static, 'DYNAMIC': original_dynamic, 'PRIOR': fallback,
    })
    tail = MainCodeFile(arm, native.BASE).sections[-1]
    start = selector - tail.ramAddress
    payload = bytes(tail.data[start:start + receipt['selector_bytes']])
    asm = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    assert payload == bytes(asm.asm(reproduce(), selector)[0])
    marker = bytes(asm.asm('ldrb r3, [r1]; cmp r3, #32', selector)[0])
    assert payload.count(marker) == 1
    return selector + payload.index(marker), fallback


def assembly(static, dynamic, previous, guard):
    parent_specs = sorted(static.keys() | dynamic.keys())
    out = ['push {r3-r5}', 'ldr r3, [sp, #0x270]']
    blocks, tables = [], []
    for i, spec in enumerate(parent_specs):
        parent, offset = spec
        static_keys, dynamic_keys = static.get(spec, ()), dynamic.get(spec, ())
        out.extend((f'ldr ip, ={parent:#x}', 'cmp r3, ip', f'beq parent_{i}'))
        blocks.extend((f'parent_{i}:', f'ldr r3, [sp, #{offset + 12:#x}]'))
        for key in dynamic_keys:
            blocks.extend((f'ldr ip, ={key:#x}', 'cmp r3, ip', 'beq dynamic_wrap'))
        if static_keys:
            blocks.extend((f'adr ip, table_{i}', f'mov r4, #{len(static_keys)}', 'b check_table'))
            tables.append(f'table_{i}: .word ' + ', '.join(f'{key:#x}' for key in static_keys))
        else:
            blocks.append('b fallback')
    out.append('b fallback')
    return '\n'.join((*out, *blocks,
        'check_table:', 'ldr r5, [ip], #4', 'cmp r3, r5', f'beq {guard:#x}',
        'subs r4, r4, #1', 'bne check_table',
        'fallback:', 'pop {r3-r5}', f'b {previous:#x}',
        'dynamic_wrap:', 'pop {r3-r5}', f'b {native.LITERAL_PARAGRAPH:#x}',
        *tables, '.ltorg'))
