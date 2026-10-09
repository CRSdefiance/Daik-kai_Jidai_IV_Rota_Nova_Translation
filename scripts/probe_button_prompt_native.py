"""Run native English glyphs and atlas sizing with a controlled loaded resource.

The resource owner/header binding is an input contract here. This does not prove
file loading, native widget construction, GPU palette/alpha or input behavior.
"""

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

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_copy_arm946_alignment import arm946_machine
from scripts.research_button_prompt import ROM, SOURCE_ROM, TEXT, make

BASE, STACK, STOP = 0x02000000, 0x027F0000, 0x027E0000
HEADER, POINT, STRING, VIEW = 0x02440000, 0x02442000, 0x02442100, 0x02443000
SAVED = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
         UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)


def machine(source):
    uc = arm946_machine(source)
    uc.mem_map(0x01FF0000, 0x10000)
    for section in MainCodeFile(source, BASE).sections:
        uc.mem_write(section.ramAddress, bytes(section.data))
    return uc


def call(uc, offset, args):
    uc.reg_write(UC_ARM_REG_SP, STACK)
    uc.reg_write(UC_ARM_REG_LR, STOP)
    for reg, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), args):
        uc.reg_write(reg, value)
    saved = {reg: 0xA5A51000 + index for index, reg in enumerate(SAVED)}
    for reg, value in saved.items():
        uc.reg_write(reg, value)
    executed = set()
    handle = uc.hook_add(UC_HOOK_CODE, lambda u, a, s, d: executed.add(a))
    try:
        uc.emu_start(BASE + offset, STOP, count=100000)
    finally:
        uc.hook_del(handle)
    if (uc.reg_read(UC_ARM_REG_PC) != STOP or uc.reg_read(UC_ARM_REG_SP) != STACK
            or any(uc.reg_read(reg) != value for reg, value in saved.items())):
        raise ValueError('Complete native prompt routine or saved-register ABI failed')
    return executed


def glyphs(source, loose, mask, origin):
    uc = machine(source)
    p = PxlImage.from_bytes(loose)
    p.indices[:] = bytes(len(p.indices))
    blank = p.to_bytes()
    uc.mem_write(HEADER - 16, b'\xA5' * (len(blank) + 32))
    uc.mem_write(HEADER, blank)
    uc.mem_write(POINT, struct.pack('<2I', *origin))
    uc.mem_write(STRING, TEXT.encode('ascii') + b'\0')
    uc.mem_write(STACK, struct.pack('<I', 14))
    executed = call(uc, 0xD1604, (0, HEADER, POINT, STRING))
    result = PxlImage.from_bytes(bytes(uc.mem_read(HEADER, len(blank))))
    expected = bytes(14 if value else 0 for value in mask.tobytes())
    if (bytes(result.indices) != expected or
            not {BASE + x for x in (0xD1604, 0xD16B4, 0xD1820)} <= executed
            or bytes(uc.mem_read(HEADER - 16, 16)) != b'\xA5' * 16
            or bytes(uc.mem_read(HEADER + len(blank), 16)) != b'\xA5' * 16
            or result.source[:result.pixels_offset] != blank[:p.pixels_offset]):
        raise ValueError('Native glyph pixels, first character or image guards differ')
    return {'native_routine': BASE + 0xD1604, 'native_pixel_sha256': sha(expected),
            'complete_english': TEXT, 'origin': list(origin), 'glyph_cells': len(TEXT),
            'first_and_final_glyph_exact': True, 'complete_raster_and_ABI_exact': True}


def dimensions(source, loose, index=20):
    uc = machine(source)
    # Concrete native PXL getter vtable: its first member is BEE88 and reads
    # resource+4. The loaded header/class is supplied, not a proven loader result.
    if source[0xBEE88:0xBEE90] != bytes.fromhex('040090e51eff2fe1'):
        raise ValueError('Concrete native PXL header getter changed')
    resource = struct.unpack_from('<I', source, 0x115EA8 + 20 * 4)[0]
    uc.mem_write(resource, struct.pack('<5I', BASE + 0x15EE00, HEADER, 0, 0, 0))
    uc.mem_write(HEADER, loose)
    uc.mem_write(VIEW - 16, b'\xA5' * (0x30 + 32))
    uc.mem_write(VIEW, bytes(0x30))
    call(uc, 0xD3D80, (VIEW,))
    executed = call(uc, 0x470B4, (index, VIEW))
    extent = struct.unpack('<2I', uc.mem_read(VIEW + 0x28, 8))
    selected = struct.unpack('<I', uc.mem_read(VIEW + 0xC, 4))[0]
    if (extent != (156, 24) or selected != resource
            or not {BASE + x for x in (0x470B4, 0xBEE88, 0xD4018, 0xD3A1C, 0xD3F60)} <= executed
            or bytes(uc.mem_read(VIEW - 16, 16)) != b'\xA5' * 16
            or bytes(uc.mem_read(VIEW + 0x30, 16)) != b'\xA5' * 16
            or bytes(uc.mem_read(HEADER, len(loose))) != loose):
        raise ValueError('Full native atlas size/view adoption or guards differ')
    return {'selector_input': index, 'selected_resource': resource, 'dimensions': list(extent),
            'native_bitmap_initializer_getter_view_adoption_ABI_pass': True,
            'resource_binding': 'controlled-existing-native-PXL-getter-and-loaded-header-contract'}


def main():
    if sha(ROM.read_bytes()) != SOURCE_ROM:
        raise ValueError('Exact V159 required')
    rom = NdsImage.open(ROM)
    source = rom.read_file('/__arm9__.bin')
    loose, _, mask, origin = make(rom)
    report = {'status': 'pass-scoped-native-glyph-and-image-sizing-research',
              'source_rom_sha256': SOURCE_ROM, 'source_arm9_sha256': sha(source),
              'glyphs': glyphs(source, loose, mask, origin),
              'dimensions': [dimensions(source, loose, index) for index in (20, 21, 255)],
              'limitations': ['Loaded image/resource class binding is an explicit controlled input.',
                              'No native file load, widget/GPU/palette/alpha or hardware key proof.']}
    Path('work/analysis/button_prompt_native_research.json').write_text(
        json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(report['status'])


if __name__ == '__main__':
    main()
