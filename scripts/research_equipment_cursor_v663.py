"""Original lower Sailor Info painter with explicit isolated SDK-clock inputs."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable
from PIL import Image
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_R8,
    UC_ARM_REG_R9,
    UC_ARM_REG_R10,
    UC_ARM_REG_R11,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL, cache_plan
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, machine
from scripts.research_town_scene_v644 import setup
from scripts.verify_movie_transition_bitmaps_v648 import rgb
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/equipment_cursor_v663')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/equipment_cursor_v663_current')


def paint(frame, visible, erase_footer_cell=None):
    rom = NdsImage.open(read(ROOT / 'preflight.json')['candidate'])
    raw = (CAP / f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
    state = read(CAP / f'capture_native_state_{frame:06d}/native_state.json')
    region = lambda k: Path(state['regions'][k]['path']).read_bytes()
    lcdm = bytearray(region('LCDM'))
    for offset in (0x40000, 0x60000):
        lcdm[offset:offset + 98304] = bytes(98304)
    dtcm = bytearray(region('DTCM'))
    if erase_footer_cell is not None:
        for y in range(12):
            for x in range(erase_footer_cell, erase_footer_cell + 6):
                i = y * 256 + x
                dtcm[i // 2] &= 0x0F if i & 1 else 0xF0
    u, mapping = setup(rom, raw, region('9REG'), bytes(lcdm), bytes(dtcm))
    u.mem_write(0x01FF0000, region('ITCM'))
    u.mem_write(0x01FF8000, region('ITCM'))
    origin = struct.unpack_from('<Q', raw, 0x170374)[0]
    ticks = origin + (0 if visible else 0x77DAF)
    executed, clock_calls, footer, written = {}, [], [], set()
    guards = [bytes(u.mem_read(a, 16)) for a in (0x022E1794 - 16, 0x022F9794)]

    def code(cpu, address, size, data):
        executed[address] = size
        if address == 0x020CA668:
            footer.append(cpu.reg_read(UC_ARM_REG_R0))
        if address == 0x020E4F98:
            clock_calls.append({'SDK_GetTick': address, 'ticks': ticks,
                                'caller_return': cpu.reg_read(UC_ARM_REG_LR)})
            cpu.reg_write(UC_ARM_REG_R0, ticks & 0xFFFFFFFF)
            cpu.reg_write(UC_ARM_REG_R1, ticks >> 32)
            cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))

    def write(cpu, kind, address, size, value, data):
        assert not 0x06000000 <= address < 0x06800000, 'Unexpected VRAM writes'
        if 0x022E1794 <= address < 0x022F9794:
            assert address + size <= 0x022F9794
            written.update(range(address, address + size))

    def memory_read(cpu, kind, address, size, value, data):
        if 0x022E1794 <= address < 0x022F9794:
            assert all(p in written for p in range(address, address + size))
        assert not 0x022F9794 <= address < 0x02311794, 'Upper output reused as source'
        if 0x06000000 <= address < 0x06800000:
            page = (address - 0x06000000) // 16384
            physical = mapping['logical_page_to_physical_LCDC_page'][page] * 16384 + (address & 16383)
            assert not any(physical < end and physical + size > start
                           for start, end in ((0x40000, 0x58000), (0x60000, 0x78000)))

    handle = u.hook_add(UC_HOOK_CODE, code)
    h2 = u.hook_add(UC_HOOK_MEM_WRITE, write)
    h3 = u.hook_add(UC_HOOK_MEM_READ, memory_read)
    saved = {r: 0xB6630000 + i for i, r in enumerate((UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11))}
    try:
        u.mem_write(0x022E1794, b'\xA5' * 98304)
        u.reg_write(UC_ARM_REG_R4, 0x023117C4)
        u.reg_write(UC_ARM_REG_R5, 0x023117C4 + 12)
        u.reg_write(UC_ARM_REG_SP, STACK)
        for reg, value in saved.items():
            u.reg_write(reg, value)
        u.emu_start(0x020D32B8, 0x020D3314, count=12000000)
        assert u.reg_read(UC_ARM_REG_PC) == 0x020D3314
        assert u.reg_read(UC_ARM_REG_SP) == STACK and u.reg_read(UC_ARM_REG_R4) == 0x023117C4
        assert u.reg_read(UC_ARM_REG_R5) == 0 and all(u.reg_read(r) == v for r, v in saved.items())
    finally:
        u.hook_del(handle)
        u.hook_del(h2)
        u.hook_del(h3)
    assert len(written) == 98304
    assert [bytes(u.mem_read(a, 16)) for a in (0x022E1794 - 16, 0x022F9794)] == guards
    assert len(clock_calls) == 1 and clock_calls[0]['caller_return'] == 0x02000FA8
    registered = machine(rom.read_file('/__arm9__.bin'))
    arm = rom.read_file('/__arm9__.bin')
    plan = cache_plan(arm)
    payload = bytes(MainCodeFile(arm, BASE).sections[3].data[:-48])
    assert plan['payload_bytes'] == len(payload) and plan['pool_span'][0] == POOL
    registered.mem_write(POOL, payload)
    overlay = loadOverlayTable(rom.rom.arm9OverlayTable, lambda i, f: rom.files[f])[0]
    registered.mem_write(overlay.ramAddress, bytes(overlay.data))
    for address, size in executed.items():
        assert bytes(u.mem_read(address, size)) == bytes(registered.mem_read(address, size)), hex(address)
    lower = bytes(u.mem_read(0x022E1794, 98304))
    name = f'native_lower_{frame}_{"on" if visible else "off"}'
    if erase_footer_cell is not None:
        name += f'_negative_cell_{erase_footer_cell}'
    (ROOT / (name + '.bin')).write_bytes(lower)
    image = Image.new('RGB', (256, 192))
    image.putdata(rgb([v for v, in struct.iter_unpack('<H', lower)]))
    image.save(ROOT / (name + '.png'))
    actual = Image.open(CAP / f'frame_{frame:06d}_cold_boot.png').convert('RGB').crop((0, 192, 256, 384))
    differences = [i for i, (a, b) in enumerate(zip(image.get_flattened_data(), actual.get_flattened_data(), strict=True)) if a != b]
    return {'frame': frame, 'controlled_blink_visible': visible,
            'clock_calls': clock_calls, 'lower_sha256': sha(lower),
            'footer_headers': footer, 'whole98304_bytes_written_over_poison': True,
            'no_output_read_before_write_no_visible_VRAM_source_no_VRAM_write': True,
            'original_fragment_ABI_guards_and_registered_instruction_bytes_pass': True,
            'complete_lower_RGB_difference_count': len(differences), 'first_differences': differences[:20],
            'executed': sorted(executed)}


def main():
    rows = []
    for visible in (False, True):
        row = paint(6400, visible)
        rows.append(row)
        print('Native lower result', {k: v for k, v in row.items() if k not in ('executed', 'clock_calls')}, flush=True)
    save(ROOT / 'lower_paint_research.json', rows)


if __name__ == '__main__':
    main()
