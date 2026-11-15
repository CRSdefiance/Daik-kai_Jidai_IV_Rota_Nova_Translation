"""Captured CPU VRAM aliases and original active Town draw iterator diagnostics."""

import struct
from pathlib import Path

from ndspy.code import loadOverlayTable
from PIL import Image
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_INVALID, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE, UcError
from unicorn.arm_const import (
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
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, machine
from scripts.probe_worldmap_overlays_v638 import color5
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/town_scene_composition_v644')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/village_backgrounds_v643_narvik')
ROM = Path('out/all_routes_combined_v640_candidate.nds')
BANKS = [(0, 8), (8, 8), (16, 8), (24, 8), (32, 4), (36, 1), (37, 1), (38, 2), (40, 1)]


def page_map(io):
    regs = [io[0x240 + i + (i >= 7)] for i in range(9)]
    if regs != [0x83, 0x8B, 0x84, 0x81, 0x82, 0, 0x83, 0, 0x82]:
        raise ValueError('Only the source-reviewed captured bank configuration is modeled')
    pages = {}
    # Original refresh order I,H,G,F,E,A,B,C,D. No conflict in this capture.
    for bank, start in ((8, 384), (4, 256), (2, 128), (3, 0)):
        physical, count = BANKS[bank]
        for i in range(count):
            pages[start + i] = physical + i
        if bank == 8:
            pages[start + 1] = physical  # original I BOBJ wrap
    # Original MMU.cpp mirror fill at the declared four engine windows.
    for start, size in ((0, 32), (128, 8), (256, 16), (384, 8)):
        for i in range(size, 128):
            source = start + (i & (size - 1))
            if source in pages:
                pages[start + i] = pages[source]
    return regs, pages


def setup(rom, raw, io, lcdm, dtcm=None):
    u = machine(rom.read_file('/__arm9__.bin'))
    u.mem_write(BASE, raw)
    overlay = loadOverlayTable(rom.rom.arm9OverlayTable, lambda i, f: rom.files[f])[0]
    u.mem_write(overlay.ramAddress, bytes(overlay.data))
    regs, pages = page_map(io)
    for logical, physical in sorted(pages.items()):
        address = 0x06000000 + logical * 16384
        u.mem_map(address, 16384)
        u.mem_write(address, lcdm[physical * 16384:(physical + 1) * 16384])
    if dtcm is not None:
        assert len(dtcm) == 16384
        u.mem_write(0x027E0000, dtcm)
    return u, {'bank_registers_A_to_I': regs, 'logical_page_to_physical_LCDC_page': pages,
               'known_disabled_or_texture_banks_not_mapped_as_CPU_pixels': True,
               'unmapped_pages_not_zero_filled': True}


def main():
    frame = 15700
    rom = NdsImage.open(ROM)
    raw = (CAP / f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
    state = read(CAP / f'capture_native_state_{frame:06d}/native_state.json')
    io = Path(state['regions']['9REG']['path']).read_bytes()
    lcdm = Path(state['regions']['LCDM']['path']).read_bytes()
    assert state['DTCM_region'] == 0x027E0000
    dtcm = Path(state['regions']['DTCM']['path']).read_bytes()
    u, mapping = setup(rom, raw, io, lcdm, dtcm)
    context = 0x023117AC
    node = struct.unpack_from('<I', raw, context - BASE + 16)[0]
    nodes, methods, seen = [], {}, set()
    while node:
        assert node not in seen and len(seen) < 100
        seen.add(node)
        vt = struct.unpack_from('<I', raw, node - BASE)[0]
        active, draw = struct.unpack_from('<2I', raw, vt - BASE + 8)
        nodes.append({'node': node, 'visibility_method': active, 'draw_method': draw})
        methods[node] = draw
        node = struct.unpack_from('<I', raw, node - BASE + 8)[0]
    executed, callback_entries, reads, writes, invalid = set(), [], [], [], []

    def code(cpu, address, size, unused):
        executed.add(address)
        if address in set(methods.values()):
            node = cpu.reg_read(UC_ARM_REG_R0)
            callback_entries.append({'method': address, 'node': node, 'context': cpu.reg_read(UC_ARM_REG_R1)})

    def access(cpu, kind, address, size, value, unused):
        row = {'PC': cpu.reg_read(UC_ARM_REG_PC), 'address': address, 'size': size}
        (reads if kind == 16 else writes).append(row)

    def fail(cpu, kind, address, size, value, unused):
        invalid.append({'PC': cpu.reg_read(UC_ARM_REG_PC), 'address': address, 'size': size, 'access': kind})
        return False

    u.hook_add(UC_HOOK_CODE, code)
    u.hook_add(UC_HOOK_MEM_READ, access, begin=0x06000000, end=0x067FFFFF)
    u.hook_add(UC_HOOK_MEM_WRITE, access, begin=0x06000000, end=0x067FFFFF)
    u.hook_add(UC_HOOK_MEM_INVALID, fail)
    u.mem_write(0x022E1794, b'\xA5' * 98304)
    for reg, value in ((UC_ARM_REG_R4, context), (UC_ARM_REG_R5, context + 12), (UC_ARM_REG_SP, STACK)):
        u.reg_write(reg, value)
    saved = {reg: 0xB5B51000 + i for i, reg in enumerate((UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8,
                                                      UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11))}
    for reg, value in saved.items():
        u.reg_write(reg, value)
    error = None
    try:
        u.emu_start(0x020D32B8, 0x020D3314, count=50000000)
        assert u.reg_read(UC_ARM_REG_PC) == 0x020D3314 and u.reg_read(UC_ARM_REG_SP) == STACK
        assert u.reg_read(UC_ARM_REG_R4) == context and u.reg_read(UC_ARM_REG_R5) == 0
        assert all(u.reg_read(reg) == value for reg, value in saved.items())
    except (AssertionError, ValueError, UcError) as e:
        error = {'error': repr(e), 'PC': u.reg_read(UC_ARM_REG_PC)}
    out = bytes(u.mem_read(0x022E1794, 98304))
    actual = Image.open(CAP / 'frame_015700_navigation.png').convert('RGB')
    words = struct.unpack('<49152H', out)
    differences = {}
    for screen in (0, 1):
        pixels = [color5(actual.getpixel((x, y + screen * 192))) for y in range(192) for x in range(256)]
        differences[str(screen)] = sum((a & 32767) != b for a, b in zip(words, pixels, strict=True))
    im = Image.new('RGB', (256, 192))
    im.putdata([((c & 31) * 255 // 31, ((c >> 5) & 31) * 255 // 31, ((c >> 10) & 31) * 255 // 31) for c in words])
    im.save(ROOT / 'DTCM_restored_town_lower_plane_REPLAY.png')
    Path(ROOT / 'DTCM_restored_town_lower_plane.bin').write_bytes(out)
    save(ROOT / 'DTCM_restored_town_diagnostic.json', {'mapping': mapping, 'nodes': nodes,
        'executed_callback_entries': callback_entries, 'error': error, 'unmapped_accesses': invalid,
        'VRAM_reads': reads, 'VRAM_writes': writes, 'screen_RGB5_differences': differences,
        'executed_instruction_addresses': sorted(executed), 'not_yet_a_final_verification': True,
        'script_sha256': sha(Path(__file__).read_bytes())})
    print('error', error, 'callback_entries', len(callback_entries), 'VRAM reads/writes', len(reads), len(writes), 'differences', differences)


if __name__ == '__main__':
    main()
