"""Exercise all124 full commodity labels through existing market and price bodies."""

import copy
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.commodity_fidelity import BASE, TABLE, transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_sailing_footer_v317 import execute
from scripts.prepare_commodity_fidelity_v635 import CONFIG, ROOT
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.verify_commodity_market_native_v350 import wrapped
from scripts.verify_commodity_private_market_v353 import paint
from scripts.verify_village_wrap_v608 import read, save


def captured_machine(arm, folder):
    folder = Path(folder)
    ram = (folder / 'final_arm9_ram.bin').read_bytes()
    report = read(folder / 'capture_report.json')
    assert report['cold_boot'] and not report['savestate_loaded']
    assert sha(ram) == report['read_only_RAM_snapshot']['sha256']
    u = machine(arm)
    u.mem_write(BASE, ram)
    for section in MainCodeFile(arm, BASE).sections:
        if section.ramAddress in (BASE, 0x01FF8000, 0x01FFC000):
            u.mem_write(section.ramAddress, bytes(section.data))
    rom = NdsImage.open('work/clean.nds')
    for overlay in loadOverlayTable(rom.rom.arm9OverlayTable, lambda _id, fid: rom.files[fid]).values():
        u.mem_write(overlay.ramAddress, bytes(overlay.data))
    return u, {'historical_captured_RAM': str(folder / 'final_arm9_ram.bin'), 'sha256': sha(ram),
               'current_main_and_native_ITCM_sections_restaged': True,
               'supplied_historical_objects_not_new_current_gameplay': True}


def main():
    arm = (ROOT / 'target_arm9.bin').read_bytes()
    config = read(CONFIG)
    assert sha(arm) == config['target_arm9_sha256']
    rows = config['records']
    font = GameAsciiFont.from_arm9(arm)
    u, market_input = captured_machine(arm, 'work/emulation_v193/commodity_market_native_v350')
    bitmap, local = 0x0219089C, 0x02190910
    shared_header = bytes(u.mem_read(0x022BD83C, 20))
    shared_pixels = bytes(u.mem_read(0x022BFDD0, 464 * 96 // 2))
    ctx, text = STACK + 0x200, STACK + 0x300
    pointer, market = None, []
    for row in sorted(rows, key=lambda r: -len(r['English'])):
        name = row['English']
        packet = (name + '\nCrafts 100%').encode('ascii') + b'\0'
        had_allocation = pointer is not None
        u.mem_write(text - 16, b'\xA5' * 16 + packet + b'\xA5' * 16)
        if pointer is not None:
            u.mem_write(pointer + 32, b'\x99' * (184 * 36 // 2))
            heap_before = bytes(u.mem_read(0x023A5AA0, 0x3A560))
        call(u, 0xD5160, (ctx, bitmap, 1))
        call(u, 0x01FFC000 - BASE, (ctx, text))
        current = struct.unpack('<I', u.mem_read(0x01FFC680, 4))[0]
        assert 0x023A5AA0 <= current < current + 4096 <= 0x023E0000
        if pointer is not None:
            assert current == pointer
            after = bytearray(u.mem_read(0x023A5AA0, 0x3A560))
            start = current - 0x023A5AA0
            after[start:start + 4096] = heap_before[start:start + 4096]
            assert after == heap_before
        pointer = current
        header = struct.unpack('<5I', u.mem_read(pointer, 20))
        assert header[:3] == (4, 46, 36) and header[4] == 32
        assert (pointer + header[3]) & 0xFFFFFFFF == 0x02125A20
        height = 24 if len(name) > 14 else 12
        expected = bytearray(b'\x99' * (184 * 36 // 2) if had_allocation else bytes(184 * 36 // 2))
        for y in range(36):
            expected[y * 92:y * 92 + 56] = bytes(56)
        for y in range(height):
            expected[y * 92 + 56:y * 92 + 92] = bytes(36)
        paint(expected, font, name + '\nCrafts 100%', 0, 0)
        paint(expected, font, wrapped(name), 112, 0)
        assert bytes(u.mem_read(pointer + 32, len(expected))) == expected, name
        assert bytes(u.mem_read(text - 16, len(packet) + 32)) == b'\xA5' * 16 + packet + b'\xA5' * 16
        assert bytes(u.mem_read(0x022BD83C, 20)) == shared_header
        assert bytes(u.mem_read(0x022BFDD0, len(shared_pixels))) == shared_pixels
        assert struct.unpack('<2I', u.mem_read(local + 0x1C, 8)) == (112, 0)
        assert struct.unpack('<I', u.mem_read(local + 0x2C, 4))[0] == height
        assert struct.unpack('<I', u.mem_read(local + 0x40, 4))[0] == height
        market.append({'index': row['index'], 'English': name, 'Local_layout': wrapped(name),
                       'Local_height': height, 'whole184x36_private_image_exact': True,
                       'one_reused_native_heap_allocation_and_shared_atlas_unchanged': True})
    u, price_input = captured_machine(arm, 'work/emulation_v193/commodity_cargo_price_v355b')
    bitmap, parent = 0x02188950, 0x02188078
    assert parent + 0x8D8 == bitmap
    assert struct.unpack('<I', u.mem_read(bitmap, 4))[0] == 0x02160360
    assert struct.unpack('<I', u.mem_read(bitmap + 16, 4))[0] == 0x022BD83C
    call(u, 0xCB124, ())
    objects = u.reg_read(UC_ARM_REG_R0) + 4
    price = []
    for row in rows:
        # Use the real current table pointer, including complete suffix aliases,
        # rather than an aligned scratch copy of the label being tested.
        actual = struct.unpack_from('<I', arm, TABLE + row['index'] * 12)[0]
        u.mem_write(objects + row['index'] * 16 + 4, struct.pack('<I', actual))
        size = 464 * 96 // 2
        u.mem_write(0x022BFDD0, bytes(size))
        call(u, 0xBF338, (parent, row['index']))
        expected = bytearray(size)
        for n, c in enumerate(row['English']):
            glyph = font.decode(c)
            for y in range(11):
                for x in range(6):
                    if glyph.getpixel((x, y)):
                        px, py = 48 + n * 5 + x, 24 + y
                        assert 48 <= px < 144 and 24 <= py < 36
                        expected[(py * 464 + px) // 2] |= 1 << ((px % 2) * 4)
        assert bytes(u.mem_read(0x022BFDD0, size)) == expected, row['English']
        price.append({'index': row['index'], 'English': row['English'], 'actual_pointer': actual,
                      'complete_price_updater_96_pixel_view_and_all_other_bitmap_pixels_exact': True})
    source = NdsImage.open('out/all_routes_combined_v633_candidate.nds').read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    negative = []
    for label in ('missing-owner', 'wrong-name', 'overlapping-roots', 'wrong-source'):
        plan, candidate = copy.deepcopy(config), source
        if label == 'missing-owner':
            plan['records'].pop()
        elif label == 'wrong-name':
            plan['records'][90]['English'] = 'Iron'
        elif label == 'overlapping-roots':
            keys = list(plan['root_offsets'])
            plan['root_offsets'][keys[1]] = plan['root_offsets'][keys[0]]
        else:
            candidate = source[:-1] + bytes([source[-1] ^ 1])
        try:
            transform(candidate, clean, plan)
        except ValueError as error:
            negative.append({'case': label, 'rejected': str(error)})
        else:
            raise AssertionError(label)
    # The harness may admit only the already proven96-byte compact callback.
    corrupt = bytearray(arm)
    code = MainCodeFile(arm, BASE)
    needle = bytes(code.sections[4].data[0x71C:0x77C])
    assert arm.count(needle) == 1
    corrupt[arm.index(needle)] ^= 1
    try:
        execute(bytes(corrupt), 'Iron Ore', buffered_context=True, compact_source_origin=True)
    except ValueError as error:
        negative.append({'case': 'corrupt-compact-wrapper', 'rejected': str(error)})
    else:
        raise AssertionError('corrupt wrapper admitted')
    save(ROOT / 'consumer_native_proof.json', {'target_arm9_sha256': sha(arm),
                                              'all124_market_and_Local_cases': market,
                                              'all124_actual_pointer_Price_Info_cases': price,
                                              'historical_component_input_contracts': [market_input, price_input],
                                              'five_invalid_inputs_rejected': negative,
                                              'actual_final_ROM_cold_boots_and_all_other_graphics_pending': True,
                                              'script_sha256': sha(Path(__file__).read_bytes())})
    print('All124 Market/Local and124 real-pointer Price Info names pass;five negative controls rejected.')


if __name__ == '__main__':
    main()
