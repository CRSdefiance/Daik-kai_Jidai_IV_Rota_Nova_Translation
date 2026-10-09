import struct

import pytest

from dk4tool.patch.grand_race_waiting_widget import (
    END,
    INIT_START,
    START,
    encode_immediate,
    immediate,
    initializer,
    rewrite_function,
)


def test_rotated_arm_immediates_cover_new_frame_and_all_shifted_objects():
    for value in (0x27C, 0xF8, 0x108, 0x198, 0x274):
        assert immediate(encode_immediate(value)) == value
    with pytest.raises(ValueError, match='Unencodable'):
        encode_immediate(0x12345678)


def test_initializer_executes_three_nonoverlapping_linkable_widgets():
    # Execute the emitted initializer, with poisoned stack memory. This checks
    # actual opcodes, loop target and writes, rather than a parallel field list.
    code = initializer()
    registers = [0xBAD0BAD0] * 16
    registers[9], registers[13] = 0, 0x100000
    memory = {0xF89CC: 0x216B290, 0xF89D8: 0x212EC9C,
              0xF89DC: 0x216B470, 0x212EC9C: 16, 0x212ECA0: 64}
    position, steps = INIT_START, 0
    zero = False
    while position < INIT_START + 4 * len(code):
        steps += 1
        assert steps < 100
        instruction = code[(position - INIT_START) // 4]
        next_position = position + 4
        if instruction == 0xE1A00000:
            pass
        elif instruction >> 24 == 0x1A:
            if not zero:
                displacement = instruction & 0xFFFFFF
                if displacement & 0x800000:
                    displacement -= 1 << 24
                next_position = position + 8 + displacement * 4
        elif instruction & 0x0C000000 == 0x04000000:
            base, register = (instruction >> 16) & 15, (instruction >> 12) & 15
            address = (position + 8 if base == 15 else registers[base]) + (instruction & 0xFFF)
            if instruction & 0x00100000:
                registers[register] = memory[address]
            else:
                memory[address] = registers[register]
        else:
            opcode, base, register = (instruction >> 21) & 15, (instruction >> 16) & 15, (instruction >> 12) & 15
            value = immediate(instruction)
            assert opcode in (2, 4, 13)
            result = {2: registers[base] - value, 4: registers[base] + value, 13: value}[opcode]
            registers[register] = result
            if instruction & 0x00100000:
                zero = result == 0
        position = next_position
    for address in (0x100098, 0x1000B8, 0x1000D8):
        assert memory[address] == 0x216B290
        assert [memory[address + field] for field in (4, 8, 0x1C)] == [0, 0, 0]
    assert 0x1000F8 not in memory  # first following object stays untouched
    assert registers[0:2] == [64, 16]
    assert registers[6] == 0x216B470
    assert registers[9] == 0 and registers[13] == 0x100000


def test_frame_relocation_preserves_conditions_and_moves_late_fields():
    raw = bytearray(END)
    # Neutral non-SP instructions elsewhere isolate the frame rewrite behavior.
    for offset in range(START, END, 4):
        struct.pack_into('<I', raw, offset, 0xE1A00000)
    examples = {START: 0xE24DDF97, 0xF85CC: 0xE3590002,
                0xF86A0: 0xE58D0254, 0xF86A4: 0xE28D0F5E,
                0xF8920: 0x128DDF97, 0xF8938: 0xB28DDF97}
    for offset, value in examples.items():
        struct.pack_into('<I', raw, offset, value)
    result, _ = rewrite_function(raw)
    get = lambda offset: struct.unpack_from('<I', result, offset)[0]
    assert immediate(get(START)) == 636
    assert immediate(get(0xF8920)) == 636 and get(0xF8920) >> 28 == 1
    assert immediate(get(0xF8938)) == 636 and get(0xF8938) >> 28 == 11
    assert get(0xF86A0) & 0xFFF == 0x274
    assert immediate(get(0xF86A4)) == 0x198
