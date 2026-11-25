"""Keep the admiral appointment phrase intact after both name fields expand."""

import inspect
from types import FunctionType

from dk4tool.patch import diplomatic_outcome_wrap_v2 as phrases
from dk4tool.patch import shipyard_fleet_setup_wrap_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


PHRASE = b'as admiral?'
TABLE = ', '.join(str(value) for value in bytes([len(PHRASE)]) + PHRASE + b'\0')


def paragraph_helper():
    source = phrases.ASM[phrases.ASM.index('\nwrap:\n'):]
    assert source.endswith(f'    .byte {phrases.TABLE}\n    .align 2\n')
    return source.replace(f'    .byte {phrases.TABLE}\n', f'    .byte {TABLE}\n')


def transform(source):
    code = checked_text(inspect.getsource(previous.transform), {
        "f'beq {EQUIPMENT_PARAGRAPH:#x}', f'next_{i}:'":
            "('beq wrap_admiral' if message == 279 else f'beq {EQUIPMENT_PARAGRAPH:#x}'), f'next_{i}:'",
        "    payload = assemble('\\n'.join(instructions), start)":
            "    assert instructions.pop() == '.ltorg'\n"
            "    instructions.extend(ADAPTED_PARAGRAPH_ENTRY)\n"
            "    payload = assemble('\\n'.join(instructions) + paragraph_helper(), start)",
        'reused_paragraph=EQUIPMENT_PARAGRAPH, serialized_parent_inverse_exact=True':
            'reused_paragraph=EQUIPMENT_PARAGRAPH, protected_admiral_suffix=PHRASE.decode(), serialized_parent_inverse_exact=True',
    })
    env = {**vars(previous), **globals(), 'ADAPTED_PARAGRAPH_ENTRY': (
        'wrap_admiral:', 'push {r4-r6, lr}', 'adr r6, wrap', 'ldr ip, =0x01ffc941', 'bx ip',
    )}
    exec(compile(code, __file__ + '::registered-paragraph-suffix-helper', 'exec'), env)
    return FunctionType(env['transform'].__code__, env)(source)
