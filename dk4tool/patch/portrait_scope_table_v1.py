"""Fit the exact portrait scopes in the existing owned ITCM selector arena."""

from hashlib import sha256

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch import compact_portrait_selector_v1 as compact
from dk4tool.patch.fleet_report_amount_glyphs_v1 import amount_assembly


native = compact.native
STATIC, DYNAMIC, AMOUNT = 0, 0x40000000, 0x80000000
KEY_MASK = 0x3FFFFFFF


def assembly(scopes, fallback, guard, amount):
    groups = []
    assert len({parent for parent, _ in scopes}) == len(scopes)
    for (parent, offset), values in sorted(scopes.items()):
        assert 0 < offset < 0x1000 and offset % 4 == 0 and 0 < len(values) < 256
        assert all(0 < key <= KEY_MASK and mode in (STATIC, DYNAMIC, AMOUNT) for key, mode in values.items())
        groups.extend((f'.word {parent:#x}, {(len(values) << 16) | (offset + 12):#x}',
                       '.word ' + ', '.join(f'{key | mode:#x}' for key, mode in sorted(values.items()))))
    return f'''
        push {{r3-r5}}
        ldr r3,[sp,#0x270]
        adr ip,groups
    next_parent:
        ldmia ip!,{{r4,r5}}
        cmp r4,#0
        beq fallback
        cmp r4,r3
        addne ip,ip,r5,lsr #14
        bne next_parent
        mov r4,r5,lsr #16
        bic r5,r5,r4,lsl #16
        ldr r3,[sp,r5]
        tst r3,#0xc0000000
        bne fallback
    next_key:
        ldr r5,[ip],#4
        eor r5,r5,r3
        movs r5,r5,lsl #2
        beq matched
        subs r4,r4,#1
        bne next_key
    fallback:
        pop {{r3-r5}}
        b {fallback:#x}
    matched:
        ldr r5,[ip,#-4]
        tst r5,#0x80000000
        bne {amount:#x}
        tst r5,#0x40000000
        beq {guard:#x}
        pop {{r3-r5}}
        b {native.LITERAL_PARAGRAPH:#x}
    groups:
        {chr(10).join(groups)}
        .word 0,0
    '''


def transform(arm, receipt, amount_owner, additions):
    selector, fallback, guard = (receipt[key] for key in ('selector', 'previous_selector', 'existing_guard'))
    old_static = {tuple(key): tuple(values) for key, values in receipt['literal_scopes']}
    old_dynamic = {tuple(key): tuple(values) for key, values in receipt['dynamic_scopes']}
    scopes = {}
    for mode, mapping in ((STATIC, old_static), (DYNAMIC, old_dynamic)):
        for group, keys in mapping.items():
            scopes.setdefault(group, {}).update(dict.fromkeys(keys, mode))
    for group, keys in additions.items():
        scope = scopes.setdefault(group, {})
        assert keys.keys().isdisjoint(scope)
        scope.update(keys)

    code = MainCodeFile(arm, native.BASE)
    assert bytes(code.save()) == arm and len(code.sections) == 6
    itcm, tail = code.sections[-2:]
    at, hook = selector - tail.ramAddress, receipt['hook'] - itcm.ramAddress
    assert not tail.bssSize and 0 < at < len(tail.data)
    asm = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    assert bytes(itcm.data[hook:hook + 4]) == bytes(asm.asm(f'b {selector:#x}', receipt['hook'])[0])
    old = bytes(asm.asm(compact.assembly(old_static, old_dynamic, fallback, guard), selector)[0])
    assert len(old) == receipt['selector_bytes'] and bytes(tail.data[at:]) == old

    signature = bytes(asm.asm('pop {r3-r5}; push {r1-r7,lr}; sub sp,sp,#144')[0])
    amount_start = amount_owner['selector'] - tail.ramAddress
    amount_end = amount_start + amount_owner['selector_bytes']
    assert 0 < amount_start < amount_end <= at
    assert tail.data[amount_start:amount_end].count(signature) == 1
    amount_offset = tail.data.index(signature, amount_start, amount_end)
    amount = tail.ramAddress + amount_offset
    amount_code = bytes(asm.asm(amount_assembly(), amount)[0])
    assert amount_offset + len(amount_code) <= amount_end
    assert bytes(tail.data[amount_offset:amount_offset + len(amount_code)]) == amount_code

    new = bytes(asm.asm(assembly(scopes, fallback, guard, amount), selector)[0])
    assert selector + len(new) <= native.BASE and amount < selector and guard < selector
    tail.data[at:] = new
    target = bytes(code.save())
    inverse = MainCodeFile(target, native.BASE)
    assert bytes(inverse.sections[-1].data[at:]) == new
    inverse.sections[-1].data[at:] = old
    assert bytes(inverse.save()) == arm
    proof = dict(selector=selector, old_selector_bytes=len(old), selector_bytes=len(new),
        previous_selector=fallback, existing_guard=guard, hook=receipt['hook'], amount_wrapper=amount,
        amount_wrapper_sha256=sha256(amount_code).hexdigest(), source_ARM9_sha256=sha256(arm).hexdigest(),
        target_ARM9_sha256=sha256(target).hexdigest(), complete_serialized_ARM9_parent_inverse=True,
        inherited_scope_count=sum(map(len, old_static.values())) + sum(map(len, old_dynamic.values())),
        added_scope_count=sum(map(len, additions.values())), remaining_ITCM_bytes=native.BASE - selector - len(new))
    return target, scopes, proof
