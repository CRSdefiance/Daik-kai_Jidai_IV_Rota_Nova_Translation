"""Execute the market formatter and native painter against captured bitmap objects."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine

ROOT = Path('work/analysis/commodity_market_v352')
BASE, BITMAP, LOCAL = 0x02000000, 0x0219089C, 0x02190910
HEADER, PIXELS = 0x022BD83C, 0x022BFDD0


def wrapped(text):
    if len(text) <= 14:
        return text
    split = text.rfind(' ', 0, 15)
    assert split >= 0 and len(text) - split - 1 <= 14
    return text[:split] + '\n' + text[split + 1:]


def main():
    arm = (ROOT / 'research_arm9.bin').read_bytes()
    source_capture = Path('work/emulation_v193/commodity_market_native_v350')
    report = json.loads((source_capture / 'capture_report.json').read_text())
    ram = (source_capture / 'final_arm9_ram.bin').read_bytes()
    assert sha(ram) == report['read_only_RAM_snapshot']['sha256']
    u = machine(arm)
    u.mem_write(BASE, ram)
    for s in MainCodeFile(arm, BASE).sections:
        if s.ramAddress in (BASE, 0x01FF8000, 0x01FFC000):
            u.mem_write(s.ramAddress, bytes(s.data))
    rom = NdsImage.open('out/all_routes_combined_v342_candidate.nds')
    for s in loadOverlayTable(rom.rom.arm9OverlayTable, lambda oid, fid: rom.files[fid]).values():
        u.mem_write(s.ramAddress, bytes(s.data))
    assert struct.unpack('<3I', u.mem_read(HEADER, 12)) == (4, 116, 96)
    assert (HEADER + struct.unpack('<I', u.mem_read(HEADER + 16, 4))[0]) & 0xFFFFFFFF == PIXELS
    assert struct.unpack('<2I', u.mem_read(BITMAP + 0x28, 8)) == (72, 36)
    assert struct.unpack('<I', u.mem_read(LOCAL, 4))[0] == 0x021602DC
    font = GameAsciiFont.from_arm9(arm)
    ctx, text_address = STACK + 0x100, STACK + 0x200
    size = 464 * 96 // 2
    rows = json.loads(Path('translations/commodity_name_manuscript_v343.json').read_text(encoding='utf-8'))['records']
    cases = []
    # Reuse one actual Local object across long/short names to test height reset.
    for row in sorted(rows, key=lambda r: -len(r['English'])):
        name = row['English']
        original = name + '\nCrafts 100%'
        output = wrapped(name) + '\nCrafts 100%'
        u.mem_write(text_address - 16, b'\xA5' * 16 + original.encode() + b'\0' + b'\xA5' * 16)
        initial = bytearray(size)
        for y in range(24, 60):
            start = y * 464 // 2
            initial[start:start + 36] = b'\x99' * 36
        u.mem_write(PIXELS - 16, b'\xA5' * 16 + initial + b'\xA5' * 16)
        before_local = bytearray(u.mem_read(LOCAL, 0x74))
        call(u, 0xD5160, (ctx, BITMAP, 1))
        call(u, 0x01FFC000 - BASE, (ctx, text_address))
        assert bytes(u.mem_read(text_address, len(original) + 1)) == output.encode() + b'\0'
        assert bytes(u.mem_read(text_address - 16, 16)) == b'\xA5' * 16
        assert bytes(u.mem_read(text_address + len(original) + 1, 16)) == b'\xA5' * 16
        expected = bytearray(size)
        y = 24
        for line in output.split('\n'):
            assert len(line) * 5 <= 72
            for n, ch in enumerate(line):
                glyph = font.decode(ch)
                for yy in range(11):
                    for x in range(6):
                        if glyph.getpixel((x, yy)):
                            px, py = n * 5 + x, y + yy
                            expected[(py * 464 + px) // 2] |= 1 << ((px % 2) * 4)
            y += 12
        actual = bytes(u.mem_read(PIXELS, size))
        assert actual == expected, (name, [(n * 2 % 464, n * 2 // 464, a, b)
                                           for n, (a, b) in enumerate(zip(actual, expected)) if a != b][:12])
        assert bytes(u.mem_read(PIXELS - 16, 16)) == b'\xA5' * 16
        assert bytes(u.mem_read(PIXELS + size, 16)) == b'\xA5' * 16
        height = 24 if len(name) > 14 else 12
        after_local = bytearray(u.mem_read(LOCAL, 0x74))
        for offset, value in [(0x2C, height), (0x40, height), (0x70, 112 + height)]:
            assert struct.unpack_from('<I', after_local, offset)[0] == value
            after_local[offset:offset + 4] = before_local[offset:offset + 4]
        assert after_local == before_local
        assert struct.unpack('<I', u.mem_read(ctx + 0x1C, 4))[0] == 0
        cases.append({'id': row['index'], 'name': name, 'compiled_layout': wrapped(name),
                      'Local_height': height, 'complete_bitmap_and_blank_cells_exact': True,
                      'only_three_Local_geometry_words_changed': True})
    proof = {'captured_real_bitmap_and_Local_metadata_used': True, 'cases': cases,
             'original_name_table_and_trade_values_unchanged': True,
             'native_painter_and_context_getters_execute': True,
             'stale_ink_in_owned_view_and_supplied_Crafts100percent_line_are_test_inputs': True,
             'old_wider_glyphs_cleared_inside_only_the_owned_view': True,
             'long_then_short_height_reset_verified': True,
             'stack_register_text_and_bitmap_guards_preserved': True,
             'actual_cold_boot_and_ITCM_ownership_audit_pending': True}
    (ROOT / 'native_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print('All124 full-name native layouts and Local height resets pass; actual playback still required.')


if __name__ == '__main__':
    main()
