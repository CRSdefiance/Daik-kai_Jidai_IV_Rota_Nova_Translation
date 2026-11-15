"""Verify the original shared date crop and ordinary visible month/day cells."""

import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_source_plaque_grain_v542 import capture_report

ROM = Path('out/all_routes_combined_v558_candidate.nds')
ROOT = Path('work/analysis/action_consumers_v562')
CAPTURE = Path('E:/Rota Nova translations/Generated/work/emulation_v193/action_consumers_v562_navigation')
BASE = 0x02000000
VIEW = 0x02192140
OWNER = 0x02313F60


def literal_owner(u, address):
    word = int.from_bytes(u.mem_read(address, 4), 'little')
    assert word & 0x0FFF0000 == 0x059F0000 and (word >> 12) & 15 == 1
    delta = word & 0xFFF
    literal = address + 8 + (delta if word & (1 << 23) else -delta)
    return int.from_bytes(u.mem_read(literal, 4), 'little')


def main():
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm = current.read_file('/__arm9__.bin')
    original_arm = clean.read_file('/__arm9__.bin')
    original, mapped = machine(original_arm), machine(arm)
    # Read mapped MainCode sections rather than assuming raw ARM9 file offsets.
    start, end = 0x020B977C, 0x020B97B0
    assert bytes(original.mem_read(start, end-start)) == bytes(mapped.mem_read(start, end-start))
    owners = {f'{a:08X}': literal_owner(original, a)
              for a in (0x02007130, 0x0200DFDC, 0x0200E00C, 0x020B979C)}
    assert list(owners.values()) == [0x02313F74] * 3 + [OWNER]
    data = current.read_file('/_pxl/__frame.pxl')
    atlas = PxlImage.from_bytes(data)
    original_data = clean.read_file('/_pxl/__frame.pxl')
    assert data[:atlas.pixels_offset] == original_data[:atlas.pixels_offset]
    palette = struct.unpack_from('<16H', data, 20 + 9 * 32)
    colour = tuple((palette[9] >> shift) & 31 for shift in (0, 5, 10))
    assert colour == (31, 31, 31)
    batch = json.loads(Path('translations/frame_action_buttons_graphics_v7.json').read_text(encoding='utf-8'))
    rows = batch['records'][-2:]
    assert [(r['text'], r['box']) for r in rows] == [('M', [104, 116, 110, 124]), ('D', [128, 116, 133, 124])]
    assert sum(atlas.indices[y*256+x] != 0 for y in range(112, 128) for x in range(104, 136)) == 34
    report = capture_report(CAPTURE, sha(ROM.read_bytes()))
    assert report['frames'] == 4700 and not report['savestate_loaded']
    assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    source_save = Path(report['battery_save_preloaded']['source'])
    assert sha(source_save.read_bytes()) == report['battery_save_preloaded']['source_sha256']
    assert not any(report.get(k) for k in ('synthetic_location_fixtures', 'synthetic_inventory_fixtures',
                                         'synthetic_condition_fixtures', 'synthetic_gallery_fixtures'))
    frames = {r['frame']: r for r in report['frames_captured']}
    cases = []
    for frame, context in ((3200, 'Syracuse town'), (3500, 'Port submenu'), (4300, 'Sail submenu')):
        raw_path = CAPTURE / f'frame_{frame:06d}_arm9_ram.bin'
        raw = raw_path.read_bytes()
        fields = struct.unpack_from('<12I', raw, VIEW-BASE)
        assert fields[3] == OWNER
        assert fields[7:9] == (104, 112) and fields[9] & 255 == 9 and fields[10:12] == (32, 16)
        u = machine(arm)
        u.mem_write(BASE, raw)
        executed = call(u, 0xD4170, (VIEW,))
        pointer = u.reg_read(UC_ARM_REG_R0)
        assert pointer == BASE + raw.find(data) and bytes(u.mem_read(pointer, len(data))) == data
        assert 0x020DED50 not in executed and 0x020DEBDC not in executed
        image = Image.open(frames[frame]['path']).convert('RGB')
        cells = []
        for row in rows:
            l, t, r, b = row['box']
            mask = {(x, y) for y in range(b-t) for x in range(r-l) if atlas.indices[(t+y)*256+l+x] == 9}
            matches = []
            for dy in range(320, 352):
                for dx in range(80, 176):
                    if all((native5(image.getpixel((dx+x, dy+y))) == colour) == ((x, y) in mask)
                           for y in range(b-t) for x in range(r-l)):
                        matches.append([dx, dy])
            expected = [122+l-104, 333]
            assert matches == [expected], (frame, row['text'], matches)
            cells.append({'text': row['text'], 'source_Japanese': row['source_japanese'],
                          'source_cell': row['box'], 'actual_destination': expected,
                          'complete_ink_pixels_exact': len(mask), 'full_cell_ink_and_blank_pattern_points': (r-l)*(b-t),
                          'unique_complete_cell_match': True, 'crop_contains_entire_cell': True})
        cases.append({'frame': frame, 'context': context, 'view': VIEW, 'owner': OWNER,
                      'source_rectangle': [104, 112, 136, 128], 'palette_bank_low_byte': 9,
                      'resident_file_pointer': pointer, 'resident_file_exact': True,
                      'RAM_sha256': sha(raw), 'PNG': frames[frame]['path'], 'PNG_sha256': frames[frame]['PNG_sha256'],
                      'glyph_cases': cells})
    appearances = sum(len(case['glyph_cases']) for case in cases)
    ink_points = sum(cell['complete_ink_pixels_exact'] for case in cases for cell in case['glyph_cases'])
    pattern_points = sum(cell['full_cell_ink_and_blank_pattern_points'] for case in cases for cell in case['glyph_cases'])
    assert (appearances, ink_points, pattern_points) == (6, 102, 264)
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'source_file': '/_pxl/__frame.pxl', 'source_file_sha256': sha(data),
             'original_constructor_call': 0x020B97AC, 'original_constructor_region_byte_exact_current': True,
             'original_literal_owners': owners, 'three_marker_owner_leads_rejected_as_frame_date_consumers': True,
             'prior_exact_origin_census_did_not_cover_this_broader_view': True,
             'actual_cases': cases, 'complete_visible_glyph_appearances': appearances,
             'complete_visible_glyph_ink_pixels': ink_points, 'full_cell_pattern_points_checked': pattern_points,
             'capture_report': str(CAPTURE/'capture_report.json'),
             'capture_report_sha256': sha((CAPTURE/'capture_report.json').read_bytes()),
             'source_save_unchanged': True, 'ordinary_copied_save_cold_boot_without_fixtures': True,
             'numeric_date_arithmetic_or_other_date_renderers_verified': False,
             'other5_miniature_controls_actual_consumers_remain_open': True,
             'zero_index_transparency_and_entire512_pixel_composite_not_claimed': True,
             'production_ROM_changed': False, 'hardware_or_full_route_verified': False,
             'all18_plaques_remain_incomplete': True, 'full_goal_complete': False}
    (ROOT/'date_native_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('Original 32x16 date crop/resident frame verified; 6 complete M/D appearances, 102 ink and 264 full-cell pattern points pass.')


if __name__ == '__main__':
    main()
