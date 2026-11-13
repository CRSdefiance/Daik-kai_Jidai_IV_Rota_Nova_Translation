"""Whole8MiB memory and register contracts for the post-printf coordinate helper."""

import re
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0,
    UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_SP)

from dk4tool.patch import tavern_coordinate_runtime as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shipyard_editorial import LITERAL
from dk4tool.rom.nds import NdsImage
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE, SAVED, STACK, STOP
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_coordinates_v766')


def main():
    plan = read(ROOT / 'owned_runtime_plan.json')
    arm = NdsImage.open('out/all_routes_combined_v762_candidate.nds').read_file('/__arm9__.bin')
    assert sha(arm) == plan['source_ARM9_sha256']
    u = machine(arm)
    for patch in plan['patches']: u.mem_write(patch['address'], bytes.fromhex(patch['target_hex']))
    h = u.hook_add(UC_HOOK_CODE, lambda cpu, pc, size, unused: cpu.emu_stop(), begin=LITERAL, end=LITERAL)
    template = next(r['english'] for r in read('translations/tavern_conversations_editorial_manuscript_v3.json')['records'] if r['message_id'] == 842).removesuffix('{PAD}').encode('ascii')
    values = [b' ' + template.replace(b'%s', bytes.fromhex(r['argument_hex'])) for r in read('work/analysis/tavern_conversations_v763/native_context.json')['actual_coordinate_formatter_arguments_for842']]
    values += [b'', b'N', b'E ', b'W -10', b'N  north', b'S 0 E 180', b'N0 W0', b'FALCON FIONA FORTUNE FURY ICARUS', b' ', b'N ' + b' ' * 200 + b'1']
    results = []
    for raw in values:
        source = 0x02420810
        u.mem_write(source - 16, b'\xa5' * 288); u.mem_write(source, raw + b'\0')
        registers = {reg: 0xA5A51000 + i for i, reg in enumerate(SAVED)}
        registers.update({UC_ARM_REG_R0: 0x02420C10, UC_ARM_REG_R1: source,
                          UC_ARM_REG_R2: 0x12345678, UC_ARM_REG_R3: 0x55667788,
                          UC_ARM_REG_SP: STACK, UC_ARM_REG_LR: STOP})
        for reg, value in registers.items(): u.reg_write(reg, value)
        before = bytes(u.mem_read(BASE, 0x800000))
        u.emu_start(owned.COORD, STOP, count=10000)
        assert u.reg_read(UC_ARM_REG_PC) == LITERAL
        assert all(u.reg_read(reg) == value for reg, value in registers.items())
        expected = re.sub(rb'([NSEW]) +([0-9])', rb'\1\2', raw)
        memory = bytearray(before)
        memory[source - BASE:source - BASE + len(expected) + 1] = expected + b'\0'
        pushed = [registers[reg] for reg in (UC_ARM_REG_R0, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_LR)]
        memory[STACK - 24 - BASE:STACK - BASE] = struct.pack('<6I', *pushed)
        after = bytes(u.mem_read(BASE, 0x800000))
        assert after == memory, raw
        assert re.sub(rb'\s+', b'', raw) == re.sub(rb'\s+', b'', expected)
        results.append({'source_hex': raw.hex(), 'expected_hex': expected.hex(),
            'whole8MiB_exact_only_owned_input_prefix_and24_stack_bytes_changed': True,
            'all_R0_R5_R6_R11_SP_LR_restored': True, 'all_nonwhitespace_bytes_intact': True})
    u.hook_del(h)
    save(ROOT / 'coordinate_buffer_contracts.json', {'cases': results, 'count': len(results),
        'all94_real_coordinate_arguments_and10_edge_controls': True,
        'no_other_RAM_code_table_buffer_or_guard_byte_changes': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'module_sha256': sha(Path(owned.__file__).read_bytes())})
    print(f'{len(results)} complete8MiB memory/register comparisons pass;all letters/digits and guards intact.', flush=True)


if __name__ == '__main__': main()
