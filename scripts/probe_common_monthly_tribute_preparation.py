"""Run the actual portrait-window sprintf/macro segment for monthly tribute."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R9,
    UC_ARM_REG_R10,
    UC_ARM_REG_R11,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, machine_for
from scripts.probe_common_tribute_guarded_wrap import wrap_expanded

TEXT, ARGUMENTS, DIGITS = 0x02423000, 0x02424000, 0x02425000


def execute(source, text, amount, actor, *, word_wrapped=False,
            parent_return=BASE + 0x53F40, selector_table=BASE + 0x1189C0):
    if text.count('%s') != 1 or not 0 <= amount <= 42949672 or not actor:
        raise ValueError('One amount substitution and nonzero portrait actor required')
    formatted = struct.unpack_from('<I', source, 0x5444C)[0]
    expanded = struct.unpack_from('<I', source, 0x54450)[0]
    digits = ''.join(chr(ord('０') + int(c)) for c in str(amount)).encode('cp932')
    raw = text.encode('cp932')
    expected = raw.replace(b'%s', digits)
    machine = machine_for(source)
    resident = ndspy.code.MainCodeFile(source, BASE).sections[1]
    machine.mem_map(0x01FF8000, 0x8000)
    machine.mem_write(resident.ramAddress, bytes(resident.data))
    machine.mem_write(STACK + 0x264, struct.pack('<I', parent_return))
    machine.mem_write(STACK + 0x274, struct.pack('<I', selector_table))
    machine.mem_write(TEXT, raw + b'\0')
    machine.mem_write(DIGITS, digits + b'\0')
    machine.mem_write(ARGUMENTS, struct.pack('<I', DIGITS))
    for buffer in (formatted, expanded):
        machine.mem_write(buffer - 32, b'\xa5' * 320)
    for register, value in ((UC_ARM_REG_R9, TEXT), (UC_ARM_REG_R10, actor),
                            (UC_ARM_REG_R11, ARGUMENTS)):
        machine.reg_write(register, value)
    executed = set()

    def code(uc, address, size, _):
        executed.add(address)

    def write(uc, access, address, size, value, _):
        if not (STACK - 0x10000 <= address and address + size <= STACK or any(
                buffer <= address and address + size <= buffer + 256 for buffer in (formatted, expanded))):
            raise ValueError('Portrait preparation writes beyond buffers or stack')

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(BASE + 0x54144, BASE + 0x54164, count=100000)
    if machine.reg_read(UC_ARM_REG_PC) != BASE + 0x54164 or machine.reg_read(UC_ARM_REG_SP) != STACK:
        raise ValueError('Portrait preparation fails to reach native window construction')
    if not {BASE + 0xCE898, BASE + 0x53914} <= executed:
        raise ValueError('Portrait preparation bypasses native formatter or macros')
    expanded_expected = wrap_expanded(expected.decode('cp932')).encode('cp932') if word_wrapped else expected
    if (0x01FF9BC8 in executed) != word_wrapped:
        raise ValueError('Monthly wrapping helper scope differs from expected caller/table')
    for buffer, wanted in ((formatted, expected), (expanded, expanded_expected)):
        block = bytes(machine.mem_read(buffer - 32, 320))
        if block != b'\xa5' * 32 + wanted + b'\0' + b'\xa5' * (287 - len(wanted)):
            raise ValueError('Portrait preparation changes prose, digits, leading characters or guards')
    return {'actor': actor, 'amount': amount, 'complete_prepared_text': expanded_expected.decode('cp932'),
            'word_wrapper_invoked': word_wrapped,
            'native_formatter_and_macros_executed': True, 'buffers_guarded': True}


def main():
    source = NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')
    manuscript = json.loads(Path('translations/common_tribute_repairs_manuscript_v2.json').read_text(encoding='utf-8'))
    cases = [{'message_id': row['message_id'], **execute(source, row['english'].removesuffix('{PAD}'), amount, actor)}
             for row in manuscript['records'] if 76 <= row['message_id'] <= 82
             for amount in (0, 9, 10, 999999, 42949672) for actor in (1, 19)]
    report = {'status': 'pass-native-monthly-portrait-formatting-segment', 'arm9_sha256': sha(source),
              'cases': cases, 'limitations': 'Executes actual 02054144 through 02054164 with supplied actor, paragraph and amount string. Actor selection, COMMON lookup, widget construction, rendering and gameplay are not proven by this segment.'}
    Path('work/analysis/common_monthly_tribute_preparation_proof.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} native monthly portrait formatting cases preserve complete prose and amounts.')


if __name__ == '__main__':
    main()
import ndspy.code
