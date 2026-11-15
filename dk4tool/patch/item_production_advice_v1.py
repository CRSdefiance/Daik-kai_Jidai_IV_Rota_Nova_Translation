"""Use guarded dialogue rows for the original item advice messages."""

from types import FunctionType

from dk4tool.patch import ship_emergency_wrap_v1 as previous
from dk4tool.patch.mutiny_static_wrap_v1 import LITERAL_COPY, assembly as guarded_assembly


PRIOR = 0x01FFE0F8
PARENT, STACK_KEY = 0x02054014, 0x274
FIRST, LAST = 3033, 3056


def assembly():
    # Reuse the guarded LF and fallback logic from the verified portrait renderer.
    guard = FunctionType(guarded_assembly.__code__, guarded_assembly.__globals__ | {
        'SCOPE': {}, 'PRIOR': PRIOR,
    })()
    _, marker, body = guard.partition('\ncheck:\n')
    assert marker and 'guarded_break:' in body
    return f'''
    push {{r3-r5}}
    ldr r3, [sp, #0x270]
    ldr ip, ={PARENT:#x}
    cmp r3, ip
    bne fallback
    ldr r3, [sp, #{STACK_KEY + 12:#x}]
    ldr ip, ={FIRST:#x}
    cmp r3, ip
    blo fallback
    ldr ip, ={LAST:#x}
    cmp r3, ip
    bhi fallback
{body}'''


def transform(source, exact_parent_arm_sha):
    return FunctionType(previous.transform.__code__, vars(previous) | {
        'SOURCE': exact_parent_arm_sha, 'PRIOR': PRIOR, 'assembly': assembly,
    })(source)
