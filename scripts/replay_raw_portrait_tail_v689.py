"""Replay the actual post-read chooser tails, recording source-buffer reads."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE, UC_MEM_READ, arm_const

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine
from scripts.trace_raw_portrait_tail_v689 import FOLDER, ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save


def payload_access(address, size, dtcm_base):
    if not 0x02000000 <= address < 0x03000000 or dtcm_base <= address < dtcm_base + 0x4000:
        return False
    physical = 0x02000000 + ((address - 0x02000000) & 0x3FFFFF)
    return physical < 0x02233040 + 14144 and physical + size > 0x02233040


def execute(row, stop, raw_override=None):
    cpu = struct.unpack('<32I', bytes.fromhex(row['CPU128_hex']))
    raw, dtcm = Path(row['RAM']).read_bytes(), Path(row['DTCM']).read_bytes()
    assert sha(raw) == row['RAM_sha256'] and sha(dtcm) == row['DTCM_sha256']
    u = machine(NdsImage.open(ROM).read_file('/__arm9__.bin'))
    u.mem_write(0x02000000, raw)
    if raw_override is not None:
        assert len(raw_override) == 14144
        u.mem_write(0x02233040, raw_override)
    dtcm_base = int.from_bytes(bytes.fromhex(row['MDTC_hex']), 'little')
    assert dtcm_base == 0x027E0000
    u.mem_write(dtcm_base, dtcm)
    assert not cpu[20] & 0x20
    u.reg_write(arm_const.UC_ARM_REG_CPSR, cpu[20])
    regs = [getattr(arm_const, 'UC_ARM_REG_R' + str(n)) for n in range(13)]
    regs += [arm_const.UC_ARM_REG_SP, arm_const.UC_ARM_REG_LR]
    for reg, value in zip(regs, cpu[4:19], strict=True):
        u.reg_write(reg, value)
    reads, writes, instructions = [], [], set()

    def memory(uc, access, address, size, value, _):
        if payload_access(address, size, dtcm_base):
            entry = {'PC': uc.reg_read(arm_const.UC_ARM_REG_PC), 'address': address,
                     'bytes': size, 'value': value}
            (reads if access == UC_MEM_READ else writes).append(entry)

    h1 = u.hook_add(UC_HOOK_MEM_READ | UC_HOOK_MEM_WRITE, memory)
    h2 = u.hook_add(UC_HOOK_CODE, lambda _u, pc, _s, _d: instructions.add(pc))
    try:
        u.emu_start(cpu[2], stop, count=100000)
    finally:
        u.hook_del(h1)
        u.hook_del(h2)
    source = machine(NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'))
    differences = [pc for pc in instructions if bytes(u.mem_read(pc, 4)) != bytes(source.mem_read(pc, 4))]
    result = {'start_PC': cpu[2], 'stop_PC': u.reg_read(arm_const.UC_ARM_REG_PC),
        'intended_stop': stop, 'unique_executed_instructions': len(instructions),
        'raw_payload_reads': reads, 'raw_payload_writes': writes,
        'executed_instruction_words_different_from_original': differences,
        'registers': [u.reg_read(reg) for reg in regs], 'CPSR': u.reg_read(arm_const.UC_ARM_REG_CPSR),
        'executed_code_sha256': sha(b''.join(struct.pack('<I', pc) + bytes(u.mem_read(pc, 4))
                                           for pc in sorted(instructions)))}
    return u, result


def main():
    rows = read(FOLDER / 'observer/events.json')['rows']
    cases = []
    for index in range(4):
        start = rows[index * 2 + 1]
        following = rows[index * 2 + 2]
        target_cpu = struct.unpack('<32I', bytes.fromhex(following['CPU128_hex']))
        u, result = execute(start, target_cpu[2])
        expected = Path(following['RAM']).read_bytes()
        actual = bytes(u.mem_read(0x02000000, 0x400000))
        differences = [i for i, (a, b) in enumerate(zip(actual, expected, strict=True)) if a != b]
        result.update({'raw_block': 14 + index,
            'actual_following_CPU_registers_match': result['registers'] == list(target_cpu[4:19]),
            'actual_following_CPSR_match': result['CPSR'] == target_cpu[20],
            'actual_following_complete_RAM_differences': len(differences),
            'actual_following_first_RAM_difference_addresses': [0x02000000 + i for i in differences[:20]]})
        cases.append(result)
        print(index, result, flush=True)
    save(ROOT / 'native_tail_diagnostic.json', {'cases': cases,
        'script_sha256': sha(Path(__file__).read_bytes()), 'not_yet_final_reconciled_proof': True})


if __name__ == '__main__':
    main()
