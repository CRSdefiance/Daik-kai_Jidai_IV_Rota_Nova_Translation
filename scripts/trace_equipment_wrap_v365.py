"""Trace the real varargs caller using read-only exported production context."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_SP,
)

from scripts.probe_button_prompt_native import STACK, machine


def run(message):
    root = Path('work/emulation_v193/equipment_long_v365')
    arm = Path('work/analysis/equipment_wrap_v365/research_arm9.bin').read_bytes()
    uc = machine(arm)
    uc.mem_write(0x02000000, (root / 'final_arm9_ram.bin').read_bytes())
    uc.mem_write(0x01FF8000, (root / 'native_state/arm9_itcm.bin').read_bytes())
    uc.mem_write(0x02430000, b'Rafael Castor\0')
    uc.mem_write(0x02430100, b'Travels of Marco Polo\0')
    uc.reg_write(UC_ARM_REG_SP, STACK)
    uc.reg_write(UC_ARM_REG_LR, 0x027E0000)
    uc.reg_write(UC_ARM_REG_R0, message)
    uc.reg_write(UC_ARM_REG_R1, 0x02430000)
    uc.reg_write(UC_ARM_REG_R2, 0x02430100)
    rows = []

    def trace(u, address, size, _):
        if address in (0x01FFC900, 0x01FFCA00, 0x01FFC944, 0x0205479C, 0x01FF9CE4):
            sp = u.reg_read(UC_ARM_REG_SP)
            row = {'address': hex(address), 'sp': hex(sp),
                   'stack_c4': hex(struct.unpack('<I', u.mem_read(sp + 0xC4, 4))[0]),
                   'stack_d0': hex(struct.unpack('<I', u.mem_read(sp + 0xD0, 4))[0])}
            rows.append(row)
            if address == 0x01FFCA00:
                pointer = u.reg_read(UC_ARM_REG_R0)
                row['input'] = bytes(u.mem_read(pointer, 120)).split(b'\0')[0].hex()
            if address == 0x01FFC944:
                row['length'] = u.reg_read(UC_ARM_REG_R0)
        if address == 0x0205479C:
            u.emu_stop()

    uc.hook_add(UC_HOOK_CODE, trace)
    uc.emu_start(0x020546B8, 0x027E0000, count=100000)
    output = struct.unpack('<I', uc.mem_read(0x02054894, 4))[0]
    result = {'message': message, 'calls': rows, 'output': bytes(uc.mem_read(output, 160)).split(b'\0')[0].decode()}
    assert result['output'] == ('  ' if message == 321 else '') + 'Rafael Castor equipped Travels of\n  Marco Polo.'
    assert rows[0]['stack_d0'] == hex(message)
    assert any(row['address'] == '0x1ffca00' for row in rows)
    return result


def main():
    results = [run(message) for message in (321, 327)]
    Path('work/analysis/equipment_wrap_v365/caller_trace.json').write_text(json.dumps(results, indent=2) + '\n')
    print('Real native varargs caller, COMMON lookup, sprintf and scoped helper pass for321/327.')


if __name__ == '__main__':
    main()
