"""Execute stack rendering and its original virtual composition call contract."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R10,
    UC_ARM_REG_SP,
)

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_town_direct_labels_v494 import BASE, CACHE, ENTRY, ROOT, TRAMPOLINE
from scripts.probe_button_prompt_native import STACK, STOP, call, machine


def main():
    arm = (ROOT / 'research_arm9.bin').read_bytes()
    plan = json.loads((ROOT / 'runtime_plan.json').read_text())
    assert sha(arm) == plan['target_arm9_sha256']
    u = machine(arm)
    u.mem_write(0x02387A20, bytes(MainCodeFile(arm, BASE).sections[3].data[:-48]))
    font = GameAsciiFont.from_arm9(arm)
    metrics = struct.unpack_from('<I', arm, 0xD5088)[0]
    u.mem_write(metrics + 4, struct.pack('<2I', 6, 12))
    source, destination, vtable, stub, strings = 0x02450000, 0x02450100, 0x02450200, 0x02450300, 0x02451000
    u.mem_write(source - 16, b'\xA5' * 112)
    u.mem_write(source, bytes(96))
    u.mem_write(source + 48, struct.pack('<I', 0x0211A65C))
    u.mem_write(destination, struct.pack('<I', vtable))
    u.mem_write(vtable + 12, struct.pack('<I', stub))
    captured, originals = [], []
    # Execute the actual stock-loop initializer/capture hooks. SL is the
    # original compact displayed-row index, independent of skipped stock IDs.
    u.mem_write(CACHE - 4, b'\xA5' + bytes(3))
    cache_after = bytes(u.mem_read(CACHE + 24, 8))
    u.mem_write(CACHE, b'\xCC' * 24)
    for entry, row, pointer in ((plan['initialize'], 99, 0),
                                *((plan['capture'], i, strings + i * 128) for i in range(5))):
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.reg_write(UC_ARM_REG_LR, STOP)
        u.reg_write(UC_ARM_REG_R10, row)
        u.reg_write(UC_ARM_REG_R1, pointer)
        u.emu_start(entry, STOP, count=100)
        assert u.reg_read(UC_ARM_REG_PC) == STOP and u.reg_read(UC_ARM_REG_SP) == STACK
        if entry == plan['initialize']:
            assert u.reg_read(UC_ARM_REG_R10) == 0
            assert struct.unpack('<I', u.mem_read(CACHE + 20, 4))[0] == 0
        else:
            assert u.reg_read(UC_ARM_REG_R10) == row
            assert struct.unpack('<I', u.mem_read(CACHE + row * 4, 4))[0] == pointer
            assert struct.unpack('<I', u.mem_read(CACHE + 20, 4))[0] == row + 1
    assert bytes(u.mem_read(CACHE + 24, 8)) == cache_after

    def hook(cpu, address, size, data):
        if address == TRAMPOLINE:
            originals.append([cpu.reg_read(UC_ARM_REG_R0), cpu.reg_read(UC_ARM_REG_R1)])
            cpu.reg_write(UC_ARM_REG_R0, 1)
        elif address == stub:
            assert cpu.reg_read(UC_ARM_REG_R0) == destination
            assert cpu.reg_read(UC_ARM_REG_R3) == 1
            view, descriptor = cpu.reg_read(UC_ARM_REG_R1), cpu.reg_read(UC_ARM_REG_R2)
            header = struct.unpack('<I', cpu.mem_read(view + 16, 4))[0]
            h = struct.unpack('<5I', cpu.mem_read(header, 20))
            assert h[:3] == (4, 24, 12)
            assert (header + h[3]) & 0xFFFFFFFF == 0x02125A20
            assert h[4] == 20
            geometry = struct.unpack('<7i', cpu.mem_read(descriptor, 28))
            args = struct.unpack('<3I', cpu.mem_read(cpu.reg_read(UC_ARM_REG_SP), 12))
            assert args == (0, source + 32, source + 60)
            packed = bytes(cpu.mem_read(header + 20, 576))
            pixels = bytes(n for b in packed for n in (b & 15, b >> 4))
            captured.append((geometry, pixels))
        else:
            return
        cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))

    u.hook_add(UC_HOOK_CODE, hook)
    manuscript = json.loads(Path('translations/commodity_name_manuscript_v343.json').read_text(encoding='utf-8'))
    results = []
    for start in range(0, 124, 5):
        rows = manuscript['records'][start:start + 5]
        pointers = []
        for i, row in enumerate(rows):
            pointer = strings + i * 128
            u.mem_write(pointer, row['English'].encode() + b'\0')
            pointers.append(pointer)
        u.mem_write(CACHE, struct.pack('<6I', *(pointers + [0] * (5 - len(pointers))), len(pointers)))
        original_source = bytes(u.mem_read(source - 16, 112))
        captured.clear()
        call(u, ENTRY - BASE, (source, destination), instruction_limit=1000000)
        assert u.reg_read(UC_ARM_REG_R0) == 1
        assert len(captured) == len(rows)
        assert bytes(u.mem_read(source - 16, 112)) == original_source
        for i, (row, (geometry, pixels)) in enumerate(zip(rows, captured)):
            assert geometry == (-1, 152, 88 + i * 16, 0, 0, 96, 12)
            expected = bytearray(96 * 12)
            for n, c in enumerate(row['English']):
                for y in range(11):
                    for x in range(6):
                        if font.decode(c).getpixel((x, y)):
                            assert n * 5 + x < 96
                            expected[y * 96 + n * 5 + x] = 1
            assert pixels == expected, row['English']
            results.append({'id': row['index'], 'text': row['English'], 'complete_mask_exact': True})
    captured.clear()
    u.mem_write(source + 48, struct.pack('<I', 0))
    call(u, ENTRY - BASE, (source, destination))
    assert not captured and u.reg_read(UC_ARM_REG_R0) == 1
    proof = {'target_arm9_sha256': sha(arm), 'all124_complete_native_masks': results,
             'original_composition_invoked_first': True, 'virtual_copy_contract': 'bounded stub; real destination gameplay still required',
             'all_visible_stock_positions_and_original_origin_pointers_preserved': True,
             'source_view_and_canaries_unchanged': True, 'ABI_and_stack_restored': True,
             'actual_stock_loop_capture_and_count_reset_bounded': True,
             'unrelated_descriptor_fallback_exact': True, 'actual_GPU_pending': True, 'full_goal_complete': False}
    (ROOT / 'native_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print('124 complete native masks and virtual copy arguments pass; real GPU verification pending.')


if __name__ == '__main__':
    main()
