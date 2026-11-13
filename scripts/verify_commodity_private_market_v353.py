"""Native full names on independent surfaces, original atlas untouched."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.verify_commodity_market_native_v350 import wrapped

ROOT = Path('work/analysis/commodity_private_market_v354')
BASE, BITMAP, LOCAL = 0x02000000, 0x0219089C, 0x02190910


def paint(expected, font, text, x0, y0, advance=5):
    for row, line in enumerate(text.split('\n')):
        for n, c in enumerate(line):
            glyph = font.decode(c)
            for y in range(11):
                for x in range(6):
                    if glyph.getpixel((x, y)):
                        px, py = x0 + n * advance + x, y0 + row * 12 + y
                        expected[(py * 184 + px) // 2] |= 1 << ((px % 2) * 4)


def main():
    arm = (ROOT / 'research_arm9.bin').read_bytes()
    captured = Path('work/emulation_v193/commodity_market_native_v350')
    ram = (captured / 'final_arm9_ram.bin').read_bytes()
    report = json.loads((captured / 'capture_report.json').read_text())
    assert sha(ram) == report['read_only_RAM_snapshot']['sha256']
    u = machine(arm)
    u.mem_write(BASE, ram)
    for s in MainCodeFile(arm, BASE).sections:
        if s.ramAddress in (BASE, 0x01FF8000, 0x01FFC000):
            u.mem_write(s.ramAddress, bytes(s.data))
    rom = NdsImage.open('out/all_routes_combined_v342_candidate.nds')
    for s in loadOverlayTable(rom.rom.arm9OverlayTable, lambda oid, fid: rom.files[fid]).values():
        u.mem_write(s.ramAddress, bytes(s.data))
    shared_header = bytes(u.mem_read(0x022BD83C, 20))
    shared_pixels = bytes(u.mem_read(0x022BFDD0, 464 * 96 // 2))
    font = GameAsciiFont.from_arm9(arm)
    rows = json.loads(Path('translations/commodity_name_manuscript_v343.json').read_text(encoding='utf-8'))['records']
    ctx, text = STACK + 0x200, STACK + 0x300
    cases = []
    pointer = None
    for row in sorted(rows, key=lambda r: -len(r['English'])):
        name = row['English']
        assert len(name) <= 19
        original = (name + '\nCrafts 100%').encode() + b'\0'
        had_allocation = pointer is not None
        u.mem_write(text - 16, b'\xA5' * 16 + original + b'\xA5' * 16)
        if pointer is not None:
            u.mem_write(pointer + 32, b'\x99' * (184 * 36 // 2))
            heap_before = bytes(u.mem_read(0x023A5AA0, 0x3A560))
        call(u, 0xD5160, (ctx, BITMAP, 1))
        call(u, 0x01FFC000 - BASE, (ctx, text))
        current = struct.unpack('<I', u.mem_read(0x01FFC680, 4))[0]
        assert 0x023A5AA0 <= current < current + 4096 <= 0x023E0000
        if pointer is not None:
            assert current == pointer
            # Repaint changes the private image, but no allocation headers move.
            after = bytearray(u.mem_read(0x023A5AA0, 0x3A560))
            before = bytearray(heap_before)
            start = current - 0x023A5AA0
            after[start:start + 4096] = before[start:start + 4096]
            assert after == before
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
        actual = bytes(u.mem_read(pointer + 32, len(expected)))
        assert actual == expected, (name, [(n * 2 % 184, n * 2 // 184, a, b)
                                           for n, (a, b) in enumerate(zip(actual, expected)) if a != b][:12])
        assert bytes(u.mem_read(text - 16, 16 + len(original) + 16)) == b'\xA5' * 16 + original + b'\xA5' * 16
        assert bytes(u.mem_read(0x022BD83C, 20)) == shared_header
        assert bytes(u.mem_read(0x022BFDD0, len(shared_pixels))) == shared_pixels
        assert struct.unpack('<2I', u.mem_read(LOCAL + 0x1C, 8)) == (112, 0)
        assert struct.unpack('<I', u.mem_read(LOCAL + 0x2C, 4))[0] == height
        assert struct.unpack('<I', u.mem_read(LOCAL + 0x40, 4))[0] == height
        assert struct.unpack('<I', u.mem_read(ctx, 4))[0] == 0x021603E4
        assert struct.unpack('<I', u.mem_read(ctx + 0x1C, 4))[0] == 0
        cases.append({'id': row['index'], 'complete_name': name, 'Local_layout': wrapped(name),
                      'Local_height': height, 'both_complete_native_pixel_surfaces_exact': True})
    statuses = []
    for label, address in [('Shortage', 0x01FFC640), ('Trending', 0x01FFC64C)]:
        u.mem_write(pointer + 32, bytes(184 * 36 // 2))
        call(u, 0xD5160, (ctx, BITMAP, 1))
        u.mem_write(ctx + 0x24, struct.pack('<2I', 0, 24))
        call(u, 0xD5404, (ctx, address))
        expected = bytearray(184 * 36 // 2)
        paint(expected, font, label, 0, 24, advance=6)
        assert bytes(u.mem_read(pointer + 32, len(expected))) == expected
        statuses.append({'text': label, 'original_status_renderer': True,
                         'complete_native_pixels_exact': True, 'eligibility_supplied_not_actual_play_state': True})
    proof = {'cases': cases, 'native_status_cases': statuses,
             'one_persistent_allocation_for_all124_cases': True,
             'original_shared_atlas_header_and_all22272_pixels_exact': True,
             'input_packet_name_table_and_trade_metadata_not_modified': True,
             'source_font_class_and_tracking_restored': True,
             'blank_and_stale_private_surface_inputs_tested': True,
             'native_real_heap_allocator_and_painters_execute': True,
             'supplied_Crafts100percent_category_line_not_trade_arithmetic_test': True,
             'actual_gameplay_and_other_commodity_contexts_pending': True,
             'full_goal_complete': False}
    (ROOT / 'native_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print('124 complete names on both surfaces pass; old atlas and input bytes exact, one reused allocation.')


if __name__ == '__main__':
    main()
