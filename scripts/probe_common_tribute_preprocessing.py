"""Execute actual COMMON vsprintf and macro preprocessing; report name corruption."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, machine_for
from scripts.probe_common_tribute_printf import FORMAT, NAME

ARGUMENTS, DIGITS = 0x02423000, 0x02424000


def execute(source, text, name, *, display_name_capacity=18):
    name.decode('cp932')
    if display_name_capacity not in (18, 36):
        raise ValueError('Unmapped stored/display name capacity')
    if not name or len(name) > display_name_capacity or b'\0' in name or text.count('%s') != 2:
        raise ValueError('Complete two-argument notice and bounded name required')
    digits = '８８４６２９'.encode('cp932')
    expected = text.encode('cp932').replace(b'%s', name, 1).replace(b'%s', digits, 1)
    formatted, expanded = struct.unpack_from('<2I', source, 0x54890)
    machine = machine_for(source)
    for at, raw in ((FORMAT, text.encode('cp932')), (NAME, name), (DIGITS, digits)):
        machine.mem_write(at, raw + b'\0')
    machine.mem_write(ARGUMENTS, struct.pack('<2I', NAME, DIGITS))
    for buffer in (formatted, expanded):
        machine.mem_write(buffer - 32, b'\xa5' * 320)
    for register, value in ((UC_ARM_REG_R0, 0), (UC_ARM_REG_R1, FORMAT),
                            (UC_ARM_REG_R2, ARGUMENTS), (UC_ARM_REG_R3, 0)):
        machine.reg_write(register, value)
    executed = set()

    def code(uc, address, size, _):
        if not BASE <= address <= BASE + len(source) - size:
            raise ValueError('Preprocessing executes outside native ARM9')
        executed.add(address - BASE)

    def write(uc, access, address, size, value, _):
        if not ((STACK - 0x10000 <= address and address + size <= STACK)
                or any(buffer <= address and address + size <= buffer + 256
                       for buffer in (formatted, expanded))):
            raise ValueError('Native preprocessing writes outside buffers/stack')

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(BASE + 0x54774, BASE + 0x5479C, count=100000)
    if machine.reg_read(UC_ARM_REG_PC) != BASE + 0x5479C or not {0xCE898, 0x53914} <= executed:
        raise ValueError('Actual vsprintf and macro preprocessing did not finish')
    outputs = []
    for buffer in (formatted, expanded):
        block = bytes(machine.mem_read(buffer - 32, 320))
        raw = block[32:].split(b'\0', 1)[0]
        if block[:32] != b'\xa5' * 32 or block[33 + len(raw):] != b'\xa5' * (287 - len(raw)):
            raise ValueError('Preprocessing changes adjacent output guards')
        outputs.append(raw)
    if outputs[0] != expected:
        raise ValueError('Actual COMMON vsprintf changes complete substituted text')
    return {'name': name.decode('cp932'), 'expected': expected.decode('cp932'),
            'formatted': outputs[0].decode('cp932'), 'expanded': outputs[1].decode('cp932'),
            'name_preserved_after_macros': outputs[1] == expected,
            'native_vsprintf_and_macros_executed': True,
            'executed_offsets': sorted(executed)}


def main():
    source = NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')
    if sha(source) != '863776d944118cc12418a91ed32e24cac1755aeac70ace682fdfa0897818b7eb':
        raise ValueError('Exact V142 ARM9 required')
    manuscript = json.loads(Path('translations/common_tribute_repairs_manuscript_v2.json').read_text(encoding='utf-8'))
    text = next(row['english'].removesuffix('{PAD}') for row in manuscript['records'] if row['message_id'] == 83)
    cases = [execute(source, text, name) for name in (b'A', b'Fleet', b'Indigo', b'ABCDEFGHIJKLMNOPQR', 'あ'.encode('cp932') * 9)]
    report = {'status': 'native-name-corruption-reproduced', 'arm9_sha256': sha(source),
              'cases': cases, 'limitations': 'Runs 54774 through 5479C, including actual CE898 and 53914. Loader, widgets, progressive wrapping and physical display remain outside scope.'}
    Path('work/analysis/common_tribute_preprocessing_proof.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{sum(not case["name_preserved_after_macros"] for case in cases)}/{len(cases)} bounded names are corrupted by actual COMMON preprocessing.')


if __name__ == '__main__':
    main()
