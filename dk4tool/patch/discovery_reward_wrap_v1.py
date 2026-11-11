"""Use the registered paragraph layout for variable discovery and reward notices."""

import inspect

from dk4tool.patch import equipment_removal_wrap_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


SOURCE = '553f732a29709b07f81c29c810897ef36863fad758d44d33b4375b3087928646'
PRIOR = 0x01FFD9A8
SCOPE = (288, 292, 301, 305, 311)


def selector():
    lines = ['ldr r3, [sp, #0xc4]', f'ldr ip, ={previous.NOTICE_PARENT:#x}',
             'cmp r3, ip', f'bne {PRIOR:#x}', 'ldr r3, [sp, #0xd0]']
    for message in SCOPE:
        lines.extend((f'ldr ip, ={message}', 'cmp r3, ip', f'beq {previous.EQUIPMENT_PARAGRAPH:#x}'))
    lines.extend((f'b {PRIOR:#x}', '.ltorg'))
    return '\n'.join(lines)


def transform(source):
    original = inspect.getsource(previous.transform)
    start = original.index("    payload = assemble(f'''")
    stop = original.index("    stop = start", start)
    code = checked_text(original, {
        original[start:stop]: '    payload = assemble(selector(), start)\n',
        'Exact registered Captain Biographies ARM9 required': 'Exact registered Shipyard and Fleet Setup ARM9 required',
        'message_ID=MESSAGE, reused_paragraph=EQUIPMENT_PARAGRAPH':
            'message_IDs=SCOPE, reused_paragraph=EQUIPMENT_PARAGRAPH',
    })
    env = {**vars(previous), **globals()}
    exec(compile(code, __file__ + '::scoped-reward-modal-dispatch', 'exec'), env)
    return env['transform'](source)
