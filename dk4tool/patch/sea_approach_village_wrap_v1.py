"""Preserve literal arguments and compiled breaks in the original nine families."""

from types import FunctionType

from dk4tool.patch import ship_emergency_wrap_v1 as previous


SOURCE = '14064e129b89b0ac8ced25d85e52b6bddb7f540c28378ba12013d5c8356a7e60'
PRIOR = 0x01FFD748
STATIC = {(0x02053DB8, 0x27C): (0x02117E80, 0x02117E60, 0x02117E40, 0x02117E20)}
DYNAMIC = {
    (0x02053D24, 0x27C): (0x02117EC0,),
    (0x02053DB8, 0x27C): (0x02117EA0, 0x02117E00, 0x02117DE0),
}


def transform(source):
    assembly = FunctionType(previous.assembly.__code__, {**previous.assembly.__globals__,
        'STATIC': STATIC, 'DYNAMIC': DYNAMIC, 'PRIOR': PRIOR})
    build = FunctionType(previous.transform.__code__, {**previous.transform.__globals__,
        'SOURCE': SOURCE, 'PRIOR': PRIOR, 'assembly': assembly})
    target, proof = build(source)
    for label, scope in (('static', STATIC), ('dynamic', DYNAMIC)):
        proof[label] = [dict(parent=parent, stack_selector_offset=offset, tables=tables)
                        for (parent, offset), tables in scope.items()]
    return target, proof
