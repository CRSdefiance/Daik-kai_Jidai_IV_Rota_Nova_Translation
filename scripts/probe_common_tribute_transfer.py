"""Execute actual tribute subtraction/credit arithmetic with bounded objects."""

import json
import struct
from pathlib import Path

from unicorn import UC_ARCH_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_MODE_ARM, Uc
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R4,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_R10,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

BASE, SENDER, RECEIVER = 0x02000000, 0x02201000, 0x02202000


def execute(source, sender_balance, receiver_balance):
    if not all(0 <= n <= 0xFFFFFFFF for n in (sender_balance, receiver_balance)):
        raise ValueError('Treasuries must be uint32 values')
    divisor = struct.unpack_from('<I', source, 0x2DEF0)[0]
    cap = struct.unpack_from('<I', source, 0x3CCC4)[0]
    if divisor != 0x51EB851F or cap != 99_999_999:
        raise ValueError('Native tribute divisor or treasury cap differs')
    amount = ((sender_balance * divisor) >> 32) >> 5
    if amount != sender_balance // 100:
        raise ValueError('Native reciprocal arithmetic differs from one percent')
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(BASE, 0x200000)
    machine.mem_map(0x02200000, 0x10000)
    machine.mem_write(BASE, source)
    for address, balance in ((SENDER, sender_balance), (RECEIVER, receiver_balance)):
        machine.mem_write(address, b'\xa5' * 64)
        machine.mem_write(address + 12, struct.pack('<I', balance))
    for register, value in ((UC_ARM_REG_R10, SENDER), (UC_ARM_REG_R7, RECEIVER), (UC_ARM_REG_R6, divisor)):
        machine.reg_write(register, value)
    writes = []

    def write_hook(uc, access, address, size, value, _):
        if (address, size) not in ((SENDER + 12, 4), (RECEIVER + 12, 4)):
            raise ValueError('Tribute writes outside the two treasury fields')
        writes.append((address, size))

    machine.hook_add(UC_HOOK_MEM_WRITE, write_hook)

    def skip_hook(uc, address, size, _):
        if address == BASE + 0x2DE98:
            uc.emu_stop()

    machine.hook_add(UC_HOOK_CODE, skip_hook)
    machine.emu_start(BASE + 0x2DE3C, BASE + 0x2DE6C, count=1000)
    stop = BASE + (0x2DE98 if amount == 0 else 0x2DE6C)
    if machine.reg_read(UC_ARM_REG_PC) != stop or machine.reg_read(UC_ARM_REG_R4) != amount:
        raise ValueError('Native transfer did not finish with the full tribute amount')
    expected_sender = sender_balance - amount
    expected_receiver = receiver_balance if amount == 0 else min(receiver_balance + amount, cap)
    for address, balance in ((SENDER, expected_sender), (RECEIVER, expected_receiver)):
        raw = bytes(machine.mem_read(address, 64))
        if raw != b'\xa5' * 12 + struct.pack('<I', balance) + b'\xa5' * 48:
            raise ValueError('Native transfer direction, amount or adjacent guards differ')
    return {'sender_before': sender_balance, 'receiver_before': receiver_balance,
            'tribute': amount, 'sender_after': expected_sender, 'receiver_after': expected_receiver,
            'native_field_writes': len(writes), 'adjacent_fields_intact': True}


def main():
    clean = NdsImage.open('work/clean.nds')
    source = clean.read_file('/__arm9__.bin')
    if sha(source) != '0d1541022ef95afe02ad7a1a381a1fc3e5e74442a5f0408f436d68a5d306d731':
        raise ValueError('Exact clean native ARM9 required')
    cases = [execute(source, sender, receiver)
             for sender in (0, 1, 99, 100, 101, 9999, 10_000, 99_999_999, 0xFFFFFFFF)
             for receiver in (0, 99_999_998, 99_999_999)]
    report = {'status': 'pass-native-tribute-transfer-not-complete-display-proof',
              'source_arm9_sha256': sha(source), 'cases': cases,
              'native_source_spans': [{'lo': lo, 'hi': hi, 'sha256': sha(source[lo:hi])}
                                      for lo, hi in ((0x2DE3C, 0x2DE6C), (0x3CC80, 0x3CCD0))],
              'ordinary_treasury_cap': 99_999_999, 'ordinary_tribute_max': 999_999,
              'raw_uint32_tribute_max': 42_949_672,
              'limitations': 'Runs the actual transfer/getter/setter instructions. Source eligibility, full caller, actor variants, sprintf and presentation are outside this probe.'}
    Path('work/analysis/common_tribute_transfer_proof.json').write_text(
        json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('27 native cases prove payer subtraction, recipient credit, zero-amount skip, cap and intact adjacent fields.')


if __name__ == '__main__':
    main()
