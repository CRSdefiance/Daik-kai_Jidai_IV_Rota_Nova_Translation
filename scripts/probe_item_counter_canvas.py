"""Real Gallery counter image-header initialization, bitmap view and clear."""

import json
import struct
from pathlib import Path

from ndspy.code import loadOverlayTable
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_ordinary_name_fidelity_research import initialized

BASE, STACK, STOP = 0x02000000, 0x027F0000, 0x027FFF00


def verify(source):
    machine = initialized(source)
    image = NdsImage.open('out/all_routes_combined_v158_candidate.nds')
    overlays = loadOverlayTable(image.rom.arm9OverlayTable, lambda oid, fid: image.files[fid])
    overlay = overlays[0]
    machine.mem_write(overlay.ramAddress, bytes(overlay.data))
    # Decode the actual native R1 LDR at 02044F50. It is not the nearby
    # 022BD7EC text-image header referenced by other Gallery code.
    instruction = struct.unpack_from('<I', source, 0x44F50)[0]
    if instruction & 0xFFFFF000 != 0xE59F1000:
        raise ValueError('Native counter image selection differs')
    field = 0x44F50 + 8 + (instruction & 0xFFF)
    header_pointer = struct.unpack_from('<I', source, field)[0]
    if header_pointer != 0x022BD7D8:
        raise ValueError('Actual Gallery counter image header differs')
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    machine.emu_start(BASE + 0x10DD0C, STOP, count=1000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK:
        raise ValueError('Actual shared image-header initializer does not return')
    header = list(struct.unpack('<5I', machine.mem_read(header_pointer, 20)))
    pixels = (header_pointer + header[4]) & 0xFFFFFFFF
    palette = (header_pointer + header[3]) & 0xFFFFFFFF
    if header[:3] != [4, 64, 92] or pixels != 0x022C2330 or palette != BASE + 0x125A20:
        raise ValueError('Native counter backing image format/pitch/height/pointers differ')
    extent = 64 * 2 * 92
    machine.mem_write(pixels - 32, b'\xA5' * (extent + 64))
    bitmap = STACK + 0x20
    machine.mem_write(bitmap - 4, b'\xA5' * 4)
    machine.mem_write(bitmap + 0x74, b'\xA5' * 4)
    executed = set()
    writes = []

    def code(uc, address, size, _):
        if not (BASE <= address < BASE + len(source)
                or overlay.ramAddress <= address < overlay.ramAddress + len(overlay.data)):
            raise ValueError('Native counter construction/clear escaped mapped source')
        executed.add(address)

    def write(uc, access, address, size, value, _):
        if not ((STACK - 0x1000 <= address < address + size <= STACK + 0x94)
                or (pixels <= address < address + size <= pixels + extent)):
            raise ValueError('Native counter construction/clear escaped bitmap/stack/pixels')
        if pixels <= address < pixels + extent:
            writes.append([address, size])

    handles = [machine.hook_add(UC_HOOK_CODE, code), machine.hook_add(UC_HOOK_MEM_WRITE, write)]
    try:
        machine.emu_start(BASE + 0x44F30, BASE + 0x44F6C, count=100000)
    finally:
        for handle in handles:
            machine.hook_del(handle)
    actual = bytes(machine.mem_read(pixels, extent))
    expected = b''.join((bytes(72) + b'\xA5' * 56) if row < 36 else b'\xA5' * 128 for row in range(92))
    view = list(struct.unpack('<8I', machine.mem_read(bitmap + 0x10, 32)))
    if (machine.reg_read(UC_ARM_REG_PC) != BASE + 0x44F6C or machine.reg_read(UC_ARM_REG_SP) != STACK
            or view != [header_pointer, 5, 0, 0, 0, 0, 144, 36]
            or actual != expected or not {BASE + 0xD4524, BASE + 0xD3AFC, BASE + 0xD393C, 0x01FFB2DC} <= executed
            or bytes(machine.mem_read(pixels - 32, 32)) != b'\xA5' * 32
            or bytes(machine.mem_read(pixels + extent, 32)) != b'\xA5' * 32
            or bytes(machine.mem_read(bitmap - 4, 4)) != b'\xA5' * 4
            or bytes(machine.mem_read(bitmap + 0x74, 4)) != b'\xA5' * 4):
        raise ValueError(f'Native counter view/clear/guards differ: header={header}, view={view}, '
                         f'clear mismatch={sum(a != b for a, b in zip(actual, expected))}')
    return {'target_arm9_sha256': sha(source), 'header_literal_field': BASE + field,
            'header_pointer': header_pointer, 'native_header': header, 'native_view': view,
            'pixel_span': [pixels, pixels + extent], 'palette_pointer': palette,
            'actual_view_geometry': [144, 36], 'native_backing_geometry': [256, 92],
            'backing_format': 4, 'native_constructor_and_actual_overlay_clear_execute': True,
            'clear_only_view_preserves_adjacent_rows_columns_and_guards': True,
            'clear_write_count': len(writes), 'overlay_sha256': sha(bytes(overlay.data)),
            'parent_composition_counter_input_and_physical_GPU_verified': False}


def main():
    source = Path('work/analysis/item_interface_cache_research_arm9.bin').read_bytes()
    result = verify(source)
    Path('work/analysis/item_counter_canvas_native_proof.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('Pass: actual 022BD7D8 counter image initialization, 144x36 native view/overlay clear, backing rows/columns and guards.')


if __name__ == '__main__':
    main()
