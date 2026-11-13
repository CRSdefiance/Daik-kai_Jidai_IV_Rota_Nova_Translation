"""Run native tribute digits and sprintf; this does not approve window layout."""

import json
from pathlib import Path

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R5,
    UC_ARM_REG_R9,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, STOP, machine_for

OUTPUT, FORMAT, NAME = 0x02420020, 0x02421000, 0x02422000


def income_contribution(source, income, status):
    """Execute the amount arithmetic; getter inputs remain explicit contracts."""
    if not 0 <= income <= 65535 or not 0 <= status <= 255:
        raise ValueError('Town income/status outside native field extents')
    machine = machine_for(source)
    machine.reg_write(UC_ARM_REG_R0, income)
    machine.reg_write(UC_ARM_REG_R5, 3)
    machine.emu_start(BASE + 0xB24CC, BASE + 0xB24E0, count=100)
    if machine.reg_read(UC_ARM_REG_PC) != BASE + 0xB24E0:
        raise ValueError('Town income division did not finish')
    machine.reg_write(UC_ARM_REG_R0, status)
    machine.emu_start(BASE + 0xB24E8, BASE + 0xB2500, count=100)
    actual = machine.reg_read(UC_ARM_REG_R9)
    expected = income // 10
    if status == 3:
        expected = expected * 3 // 2
    elif status == 4:
        expected //= 2
    if machine.reg_read(UC_ARM_REG_PC) != BASE + 0xB2500 or actual != expected:
        raise ValueError('Town tribute native contribution differs')
    return actual


def execute(source, text, amount, name=None):
    if not 0 <= amount <= 0x7FFFFFFF:
        raise ValueError('Native digit converter requires a nonnegative signed integer')
    if name is not None:
        if not name or len(name) > 18 or b'\0' in name:
            raise ValueError('Faction name must fit the native eighteen-byte editor')
        name.decode('cp932')
    if text.count('%s') != (1 if name is None else 2):
        raise ValueError('Tribute argument count differs')
    raw = text.encode('cp932')
    digits = ''.join(chr(ord('０') + int(c)) for c in str(amount)).encode('cp932')
    values = [digits] if name is None else [name, digits]
    expected = raw
    for value in values:
        expected = expected.replace(b'%s', value, 1)
    expected += b'\0'
    if len(expected) > 512:
        raise ValueError('Diagnostic output exceeds bounded buffer')
    machine = machine_for(source)
    machine.reg_write(UC_ARM_REG_R0, amount)
    machine.emu_start(BASE + 0xABF50, STOP, count=10000)
    pointer = machine.reg_read(UC_ARM_REG_R0)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK:
        raise ValueError('Native digit converter did not return with balanced stack')
    if bytes(machine.mem_read(pointer, len(digits) + 1)) != digits + b'\0':
        raise ValueError('Native digits differ from full amount')
    machine.mem_write(OUTPUT - 32, b'\xa5' * 576)
    machine.mem_write(FORMAT, raw + b'\0')
    if name is not None:
        machine.mem_write(NAME, name + b'\0')
    for register, value in ((UC_ARM_REG_R0, OUTPUT), (UC_ARM_REG_R1, FORMAT),
                            (UC_ARM_REG_R2, pointer if name is None else NAME),
                            (UC_ARM_REG_R3, 0 if name is None else pointer),
                            (UC_ARM_REG_LR, STOP)):
        machine.reg_write(register, value)
    executed = set()

    def code(uc, address, size, _):
        if not BASE <= address <= BASE + len(source) - size:
            raise ValueError('Printf executes outside native source')
        executed.add(address - BASE)

    def write(uc, access, address, size, value, _):
        if not ((OUTPUT <= address and address + size <= OUTPUT + 512)
                or (STACK - 0x10000 <= address and address + size <= STACK)):
            raise ValueError('Printf writes outside diagnostic output/stack')

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(BASE + 0xD7720, STOP, count=100000)
    actual = bytes(machine.mem_read(OUTPUT - 32, 576))
    if actual != b'\xa5' * 32 + expected + b'\xa5' * (544 - len(expected)):
        raise ValueError('Printf loses complete text/NUL or changes adjacent guards')
    if (machine.reg_read(UC_ARM_REG_PC) != STOP
            or machine.reg_read(UC_ARM_REG_SP) != STACK
            or machine.reg_read(UC_ARM_REG_R0) != len(expected) - 1):
        raise ValueError('Printf return length/stack differs')
    if not {0xD7720, 0xD7754, 0xD7950} <= executed:
        raise ValueError('Native sprintf helpers were not executed')
    return {'amount': amount, 'name_hex': None if name is None else name.hex(),
            'expanded_text': expected[:-1].decode('cp932'),
            'bytes_with_nul': len(expected), 'native_helpers_executed': True,
            'output_guards_intact': True, 'stack_balanced': True}


def main():
    source = NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')
    if sha(source) != '863776d944118cc12418a91ed32e24cac1755aeac70ace682fdfa0897818b7eb':
        raise ValueError('Exact V142 ARM9 required')
    manuscript = json.loads(Path('translations/common_tribute_repairs_manuscript_v2.json').read_text(encoding='utf-8'))
    cases = []
    contributions = [{'income': income, 'status': status,
                      'amount': income_contribution(source, income, status)}
                     for income in (0, 1, 9, 10, 65534, 65535)
                     for status in (0, 3, 4, 255)]
    for record in manuscript['records']:
        text = record['english'].removesuffix('{PAD}')
        names = (None,) if record['message_id'] != 83 else (b'A', b'ABCDEFGHIJKLMNOPQR', 'あ' .encode('cp932') * 9)
        for name in names:
            for amount in (0, 1, 9, 10, 999999, 42949672, 2147483647):
                cases.append({'message_id': record['message_id'], **execute(source, text, amount, name)})
    report = {'status': 'pass-native-substitution-not-window-layout',
              'arm9_sha256': sha(source), 'cases': cases,
              'town_contribution_cases': contributions,
              'town_sum_upper_bound': 19 + 90 * income_contribution(source, 65535, 3),
              'native_source_spans': [{'lo': lo, 'hi': hi, 'sha256': sha(source[lo:hi])}
                                      for lo, hi in ((0xB2450, 0xB25CC), (0xB3FD4, 0xB3FE0),
                                                     (0xB2620, 0xB2624), (0xABF50, 0xAC000))],
              'limitations': 'Synthetic bounded arguments exercise actual ABF50 and sprintf. Town income eligibility/bounds, wrappers and window rendering are not approved by this probe.'}
    Path('work/analysis/common_tribute_printf_proof.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'{len(cases)} native tribute substitution cases pass; window layout remains pending.')


if __name__ == '__main__':
    main()
