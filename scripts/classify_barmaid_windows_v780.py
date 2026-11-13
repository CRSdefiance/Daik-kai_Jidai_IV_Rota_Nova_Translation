"""Classify three exact byte-scan coincidences through native code and typed data."""

import math
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R9, UC_ARM_REG_R10

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.context_barmaid_dialogue_v779 import CURRENT
from scripts.native_machine_scoped_v764 import machine
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/barmaid_integration_v780')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    arm = NdsImage.open(CURRENT).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0xE5784:0xE579C] == clean[0xE5784:0xE579C]
    assert arm[0x82F3C:0x82F4C] == clean[0x82F3C:0x82F4C]
    assert arm[0xE5788:0xE5790].hex() == '00009405029009e0'
    assert arm[0x82F40:0x82F48].hex() == '0000930502008003'
    u = machine(arm)
    instruction_cases = []
    for equal in (False, True):
        u.mem_write(0x02430000, struct.pack('<I', 0xFFFFFFFF))
        u.mem_write(0x02430102, b'\xAA\xAA')
        for register, value in ((UC_ARM_REG_R0, 42), (UC_ARM_REG_R10, 42 if equal else 41),
                                (UC_ARM_REG_R4, 0x02430000), (UC_ARM_REG_R2, 0xFFFFFFFD),
                                (UC_ARM_REG_R9, 11), (UC_ARM_REG_R5, 0),
                                (UC_ARM_REG_R6, 0x02430100), (UC_ARM_REG_R1, 2)):
            u.reg_write(register, value)
        visited = []
        h = u.hook_add(UC_HOOK_CODE, lambda c, p, s, d: visited.append(p), begin=0x020E5784, end=0x020E5798)
        u.emu_start(0x020E5784, 0x020E579C, count=100)
        u.hook_del(h)
        assert visited == list(range(0x020E5784, 0x020E579C, 4))
        value = struct.unpack('<I', u.mem_read(0x02430000, 4))[0]
        half = struct.unpack('<H', u.mem_read(0x02430102, 2))[0]
        assert value == (0xFFFFFFFD if equal else 0xFFFFFFFF)
        assert half == (0 if equal else 0xAAAA) and u.reg_read(UC_ARM_REG_R9) == 9
        instruction_cases.append({'window': 0x020E5789, 'equal': equal, 'executed_ARM_PCs': visited,
                                  'loaded_and_masked_data_word': value, 'cleared_halfword': half})
    for equal in (False, True):
        u.mem_write(0x02430000, struct.pack('<I', 0xA0))
        u.reg_write(UC_ARM_REG_R3, 0x02430000)
        u.reg_write(UC_ARM_REG_R1, 1 if equal else 2)
        u.reg_write(UC_ARM_REG_R0, 0xDEADBEEF)
        visited = []
        h = u.hook_add(UC_HOOK_CODE, lambda c, p, s, d: visited.append(p), begin=0x02082F3C, end=0x02082F48)
        u.emu_start(0x02082F3C, 0x02082F4C, count=100)
        u.hook_del(h)
        assert visited == list(range(0x02082F3C, 0x02082F4C, 4))
        value = struct.unpack('<I', u.mem_read(0x02430000, 4))[0]
        assert value == (0xA2 if equal else 0xA0)
        instruction_cases.append({'window': 0x02082F41, 'equal': equal, 'executed_ARM_PCs': visited,
                                  'conditional_OR_data_result': value})
    start, end = 0x12A510, 0x12E510
    expected = b''.join(struct.pack('<hh', round(4096*math.sin(2*math.pi*i/4096)),
                                    round(4096*math.cos(2*math.pi*i/4096))) for i in range(4096))
    assert arm[start:end] == clean[start:end] == expected
    assert arm[0x6DB38:0x6DB54] == clean[0x6DB38:0x6DB54]
    samples = []
    for i in range(4096):
        u.reg_write(UC_ARM_REG_R0, i)
        u.emu_start(0x0206DB38, 0x0206DB54, count=100)
        actual = tuple((u.reg_read(r)+2**31) % 2**32-2**31 for r in (UC_ARM_REG_R0, UC_ARM_REG_R1))
        want = struct.unpack_from('<hh', expected, i*4)
        assert actual == want
        samples.append(actual)
    exclusions = [['absolute', 'section0', 0x020E5789, 0x02059400],
                  ['absolute', 'section0', 0x02082F41, 0x02059300],
                  ['absolute', 'section0', 0x0212B171, 0x0205930E]]
    save(ROOT/'classified_source_windows.json', {
        'source_ROM_sha256': sha(CURRENT.read_bytes()), 'source_ARM9_sha256': sha(arm),
        'exact_classified_references': exclusions, 'native_ARM_conditional_cases': instruction_cases,
        'word_spans': [{'address': a+0x02000000, 'hex': arm[a:b].hex()} for a, b in ((0xE5784, 0xE579C), (0x82F3C, 0x82F4C))],
        'numeric_table': {'address': start+0x02000000, 'bytes': end-start, 'sha256': sha(expected),
                          'all4096_signed_halfword_pairs_equal_independent_math': True,
                          'native_signed_halfword_loader_cases': len(samples),
                          'loader_source_hex': arm[0x6DB38:0x6DB54].hex(),
                          'candidate_window_is_inside_typed_numeric_pair': True},
        'only_three_exact_unchanged_source_windows_classified_no_alignment_waiver': True,
        'no_ROM_changes_or_actual_gameplay_claim': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Three exact scan hits classified:two executed ARM instruction windows and one complete4096-pair numeric table with native signed loads.', flush=True)


if __name__ == '__main__':
    main()
