"""Keep compiler-generated breaks within the original mutiny portrait callers."""

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.mutiny_choice_labels_v1 import transform as localize_labels
from dk4tool.patch.sea_event_static_wrap_v1 import BASE, HOOK, LITERAL_COPY, SELECTOR as PRIOR


# Keys are the original caller return address and its local selector offset.
# The values name the original native table or the direct COMMON number.
SCOPE = {
    (0x02053DB8, 0x27C): (0x02118660, 0x021186C0, 0x02118720, 0x02118740),
    (0x02053F40, 0x274): (0x02117580, 0x021175A0, 0x02118640),
    (0x02053C14, 0x270): (0x02116800,),
    (0x02054014, 0x274): (508, 516, 553),
}
MAXIMUM_TEMPLATE = 144


def assembly():
    branches, matches = [], []
    for i, ((parent, offset), keys) in enumerate(SCOPE.items()):
        branches += [f'ldr ip, ={parent:#x}', 'cmp r3, ip', f'beq parent_{i}']
        matches += [f'parent_{i}:', f'ldr r3, [sp, #{offset + 12:#x}]']
        for key in keys:
            matches += [f'ldr ip, ={key:#x}', 'cmp r3, ip', 'beq check']
        matches += ['b fallback']
    return '\n'.join(['push {r3-r5}', 'ldr r3, [sp, #0x270]', *branches,
                      'b fallback', *matches, f'''
check:
    ldrb r3, [r1]
    cmp r3, #32
    bne full_first_row
    add r4, r1, #1
    add r5, r1, #{MAXIMUM_TEMPLATE - 2}
scan:
    cmp r4, r5
    bhs fallback
    ldrb r3, [r4], #1
    cmp r3, #0
    beq fallback
    cmp r3, #10
    bne scan
    b guarded_break
full_first_row:
    mov r4, r1
    add r5, r1, #36
full_row_scan:
    ldrb r3, [r4], #1
    cmp r3, #32
    blo fallback
    cmp r3, #126
    bhi fallback
    cmp r4, r5
    blo full_row_scan
    ldrb r3, [r4], #1
    cmp r3, #10
    bne fallback
guarded_break:
    ldrb r3, [r4]
    cmp r3, #32
    ldrbeq r3, [r4, #1]
    cmpeq r3, #32
    bne fallback
    pop {{r3-r5}}
    b {LITERAL_COPY:#x}
fallback:
    pop {{r3-r5}}
    b {PRIOR:#x}
    .ltorg
'''])


def transform(source, labels):
    localized, menu = localize_labels(source, labels)
    code = MainCodeFile(localized, BASE)
    assert bytes(code.save()) == localized and len(code.sections) == 6
    itcm, tail = code.sections[-2:]
    assert itcm.ramAddress == 0x01FFC000 and len(itcm.data) == 0x1000
    assert not tail.bssSize
    start = tail.ramAddress + len(tail.data)
    assembler = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    at = HOOK - itcm.ramAddress
    old = bytes(assembler.asm(f'b {PRIOR:#x}', HOOK)[0])
    assert itcm.data[at:at + 4] == old
    new = bytes(assembler.asm(f'b {start:#x}', HOOK)[0])
    extension = bytes(assembler.asm(assembly(), start)[0])
    stop = start + len(extension)
    assert stop <= BASE and len(extension) % 4 == 0
    assert all(section.ramAddress + len(section.data) + section.bssSize <= start or stop <= section.ramAddress
               for section in code.sections)
    itcm.data[at:at + 4] = new
    tail.data.extend(extension)
    target = bytes(code.save())

    inverse = MainCodeFile(target, BASE)
    assert bytes(inverse.sections[-1].data[-len(extension):]) == extension
    del inverse.sections[-1].data[-len(extension):]
    inverse.sections[-2].data[at:at + 4] = old
    assert bytes(inverse.save()) == localized
    scope = [dict(parent=parent, stack_selector_offset=offset, keys=values) for (parent, offset), values in SCOPE.items()]
    return target, menu, dict(hook=HOOK, prior_selector=PRIOR, mutiny_selector=start, selector_bytes=len(extension),
        target_ARM9_sha256=sha(target), source_ARM9_sha256=sha(localized), literal_copy=LITERAL_COPY,
        maximum_compiled_template_bytes=MAXIMUM_TEMPLATE, scope=scope, complete_serialized_ARM9_parent_inverse=True)
