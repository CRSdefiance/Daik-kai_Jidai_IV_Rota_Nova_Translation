"""Model ARM946 copy alignment explicitly; execute the real native copy body."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
)

from dk4tool.patch.common_copy_alignment_release import BASE, SOURCE, transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts import probe_remaining_common_layout as loader
from scripts.execute_map_entity_tooltip_copy import STOP, machine_for

COPY, INPUT, OUTPUT = BASE + 0xCEC74, 0x02460000, 0x02462000


def arm946_machine(source):
    machine = machine_for(source)

    def cpu(uc, address, size, _):
        # ARM946 word LDR aligns down and rotates; STR aligns down. Unicorn's
        # default unaligned memory behavior is not an ARM946 hardware oracle.
        if address in (BASE + 0xCEC88, BASE + 0xCECB4):
            pointer = uc.reg_read(UC_ARM_REG_R1)
            width = 4 if address == BASE + 0xCEC88 else 2
            if pointer % width:
                value = int.from_bytes(uc.mem_read(pointer & ~(width - 1), width), 'little')
                shift = pointer % width * 8
                value = ((value >> shift) | (value << (32 - shift))) & 0xFFFFFFFF
                uc.reg_write(UC_ARM_REG_R3, value)
                uc.reg_write(UC_ARM_REG_R1, pointer + width)
                uc.reg_write(UC_ARM_REG_PC, address + 4)
        elif address in (BASE + 0xCEC90, BASE + 0xCECC0):
            pointer = uc.reg_read(UC_ARM_REG_R0)
            width = 4 if address == BASE + 0xCEC90 else 2
            if pointer % width:
                value = uc.reg_read(UC_ARM_REG_R3) & ((1 << (width * 8)) - 1)
                uc.mem_write(pointer & ~(width - 1), value.to_bytes(width, 'little'))
                uc.reg_write(UC_ARM_REG_R0, pointer + width)
                uc.reg_write(UC_ARM_REG_PC, address + 4)

    machine.hook_add(UC_HOOK_CODE, cpu)
    return machine


def matrix(source):
    machine = arm946_machine(source)
    lengths = list(range(34)) + [127, 128, 129, 255, 256, 257, 511, 512, 4095, 4096]
    cases = 0
    for count in lengths:
        for source_phase in range(4):
            for target_phase in range(4):
                raw = bytes((i * 17 + 43) % 256 for i in range(count))
                machine.mem_write(INPUT - 16, b'\xA5' * (count + 40))
                machine.mem_write(OUTPUT - 16, b'\xA5' * (count + 40))
                machine.mem_write(INPUT + source_phase, raw)
                before = bytes(machine.mem_read(INPUT - 16, count + 40))
                for reg, value in ((UC_ARM_REG_R0, OUTPUT + target_phase),
                                   (UC_ARM_REG_R1, INPUT + source_phase),
                                   (UC_ARM_REG_R2, count), (UC_ARM_REG_LR, STOP)):
                    machine.reg_write(reg, value)
                machine.emu_start(COPY, STOP, count=100000)
                expected = b'\xA5' * (16 + target_phase) + raw + b'\xA5' * (24 - target_phase)
                if (bytes(machine.mem_read(OUTPUT - 16, count + 40)) != expected
                        or bytes(machine.mem_read(INPUT - 16, count + 40)) != before
                        or machine.reg_read(UC_ARM_REG_PC) != STOP):
                    raise ValueError(f'ARM946 copy failure: {count}, {source_phase}, {target_phase}')
                cases += 1
    return cases


def main():
    image = NdsImage.open('out/all_routes_combined_v151_candidate.nds')
    source = image.read_file('/__arm9__.bin')
    if sha(source) != SOURCE:
        raise ValueError('Exact V151 required')
    repaired = transform(source)
    common = image.read_file('/COMMON/MESFILE.DK4')
    entries = common_message_entries(common, source, clean=False)
    original_factory = loader.machine_for
    machines = []

    def factory(raw):
        machine = arm946_machine(raw)
        machines.append(machine)
        return machine

    loader.machine_for = factory
    reproduction = []
    try:
        owner = struct.unpack_from('<I', source, 0x552A0)[0]
        for message in (8, 50, 51, 53, 120):
            entry = entries[message]
            try:
                loader.warm_copy(source, common, message, entry.text)
            except ValueError:
                pass
            else:
                raise ValueError('Reported failure was not reproduced')
            broken = bytes(machines[-1].mem_read(owner + 0x2030, 128)).split(b'\0', 1)[0]
            reproduction.append({'message_id': message, 'expected_hex': entry.text.hex(),
                                 'broken_hex': broken.hex(), 'broken_text': broken.decode('cp932', errors='replace')})
            machines.clear()
        preserved = []
        for message, entry in enumerate(entries):
            for cold in (False, True):
                loader.warm_copy(repaired, common, message, entry.text, cold_cache=cold)
                machines.clear()
            preserved.append(message)
            if message % 500 == 0:
                print(f'Native ARM946 warm/cold lookup: {message}/{len(entries)}', flush=True)
    finally:
        loader.machine_for = original_factory
    report = {'source_arm9_sha256': SOURCE, 'repair_arm9_sha256': sha(repaired),
              'reported_failures_reproduced': reproduction,
              'copy_alignment_matrix_cases': matrix(repaired),
              'all_common_messages_preserved_warm_and_cold': preserved,
              'native_lookup_cases': len(preserved) * 2,
              'limits': ['ARM946 copy alignment is modeled explicitly; not a full hardware emulator.',
                         'Cold filesystem open/read are host contracts; native ILNK/cache/copy execute.',
                         'Actual screenshots after repair and cold boot remain required.']}
    Path('work/analysis/common_copy_arm946_alignment_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f"Pass: {len(preserved)} COMMON messages, warm/cold; {report['copy_alignment_matrix_cases']} alignment cases.")


if __name__ == '__main__':
    main()
