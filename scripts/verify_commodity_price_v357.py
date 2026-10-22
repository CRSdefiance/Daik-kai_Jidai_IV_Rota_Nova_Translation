"""Complete original Price Info updater with captured bitmap and supplied names."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine

ROOT = Path('work/analysis/commodity_price_v357')


def main():
    arm = (ROOT / 'research_arm9.bin').read_bytes()
    ram = Path('work/emulation_v193/commodity_cargo_price_v355b/final_arm9_ram.bin').read_bytes()
    u = machine(arm)
    u.mem_write(0x02000000, ram)
    for s in MainCodeFile(arm, 0x02000000).sections:
        if s.ramAddress in (0x02000000, 0x01FF8000, 0x01FFC000):
            u.mem_write(s.ramAddress, bytes(s.data))
    rom = NdsImage.open('out/all_routes_combined_v342_candidate.nds')
    for s in loadOverlayTable(rom.rom.arm9OverlayTable, lambda oid, fid: rom.files[fid]).values():
        u.mem_write(s.ramAddress, bytes(s.data))
    bitmap, owner_anchor = 0x02188950, 0x02188078
    assert owner_anchor + 0x8D8 == bitmap
    assert struct.unpack('<I', u.mem_read(bitmap, 4))[0] == 0x02160360
    assert struct.unpack('<I', u.mem_read(bitmap + 16, 4))[0] == 0x022BD83C
    assert struct.unpack('<2I', u.mem_read(bitmap + 0x1C, 8)) == (0, 12)
    call(u, 0xCB124, ())
    objects = u.reg_read(UC_ARM_REG_R0) + 4
    text = STACK + 0x100
    font = GameAsciiFont.from_arm9(arm)
    rows = json.loads(Path('translations/commodity_name_manuscript_v343.json').read_text(encoding='utf-8'))['records']
    cases = []
    for row in rows:
        value = row['English'].encode() + b'\0'
        u.mem_write(text, value)
        u.mem_write(objects + row['index'] * 16 + 4, struct.pack('<I', text))
        size = 464 * 96 // 2
        u.mem_write(0x022BFDD0, bytes(size))
        call(u, 0xBF338, (owner_anchor, row['index']))
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
        assert bytes(u.mem_read(text, len(value))) == value
        cases.append({'id': row['index'], 'name': row['English'],
                      'complete_original_updater_and_native_pixels_exact': True,
                      'source_name_box': [48, 24, 144, 36]})
    proof = {'cases': cases, 'captured_bitmap_used': bitmap,
             'owner_anchor_supplied_from_native_bitmap_offset_not_runtime_dispatch_trace': True,
             'all124_full_names_fit_and_all_first_final_glyphs_exact': True,
             'actual_selected_commodity_name_and_other_screen_pixels_pending': True}
    (ROOT / 'native_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print('Original Price Info updater: all124 complete names fit the96-pixel source view.')


if __name__ == '__main__':
    main()
