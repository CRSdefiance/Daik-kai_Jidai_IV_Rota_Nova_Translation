"""Run original macro expansion and verify exact equipment-only hook scope."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from scripts.probe_button_prompt_native import STACK, call, machine

ROOT = Path('work/analysis/equipment_wrap_v365')


def run(arm, parent, message, hooked):
    u = machine(arm)
    staged = MainCodeFile(arm, 0x02000000).sections[3]
    u.mem_write(0x02387A20, bytes(staged.data[:-48]))
    text, output = 0x0242C020, 0x0242D020
    raw = b'  Rafael Castor equipped Travels of Marco Polo.'
    u.mem_write(text - 16, b'\xA5' * 16 + raw + b'\0' + b'\xA5' * 16)
    u.mem_write(output - 16, b'\xA5' * 288)
    u.mem_write(STACK + 0xC4, struct.pack('<I', parent))
    u.mem_write(STACK + 0xD0, struct.pack('<I', message))
    call(u, 0x01FFC900 - 0x02000000 if hooked else 0x53914, (output, text, 0))
    value = bytes(u.mem_read(output, 256)).split(b'\0', 1)[0]
    assert bytes(u.mem_read(text, len(raw) + 1)) == raw + b'\0'
    assert bytes(u.mem_read(output - 16, 16)) == b'\xA5' * 16
    assert bytes(u.mem_read(output + 256, 16)) == b'\xA5' * 16
    return value


def main():
    arm = (ROOT / 'research_arm9.bin').read_bytes()
    rows = []
    for parent, message in [(0x020546E8, 321), (0x020546E8, 327), (0x020546E8, 326),
                            (0x020546E8, 328), (0x02054764, 327),
                            (0x020546E8, 83)]:
        old = run(arm, parent, message, False)
        new = run(arm, parent, message, True)
        if parent == 0x020546E8 and message in (321, 327):
            assert new == b'  Rafael Castor equipped Travels of\n  Marco Polo.'
        elif message != 83:
            assert new == old
        else:
            # The inherited83 wrapper remains active and keeps its own policy.
            assert b' '.join(new.split()) == b' '.join(old.split())
        rows.append({'parent': parent, 'message': message, 'old': old.decode(), 'new': new.decode()})
    (ROOT / 'scope_proof.json').write_text(json.dumps({'cases': rows,
        'actual_original_macro_expander_executes': True,
        'equipment321/327_only_new_scope_and_other_message_passthrough_verified': True,
        'input_stack_register_and_output_guards_preserved': True,
        'actual_equipment_confirmation_still_pending': True}, indent=2) + '\n')
    print('Native equipment321/327 scope, unrelated messages and inherited83 behavior pass.')


if __name__ == '__main__':
    main()
