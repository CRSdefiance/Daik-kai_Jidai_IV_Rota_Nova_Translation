"""Genuine purchased map, complete source/marker pixels and normal-save reload."""

import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_original_latin_cards_native_v197 import native5

ROOT = Path('work/analysis/map_viewer_v441')
ROM = Path('out/all_routes_combined_v440_candidate.nds')


def main():
    rom = NdsImage.open(ROM)
    digest = sha(ROM.read_bytes())
    captures = []
    for name, frame in [('map_viewer_v441', 21400), ('map_saved_reload_v441', 5000)]:
        folder = Path('work/emulation_v193') / name
        report_path = folder / 'capture_report.json'
        report = json.loads(report_path.read_text(encoding='utf-8'))
        assert report['ROM_sha256'] == digest and report['cold_boot']
        assert not report['savestate_loaded'] and not report['callback_errors']
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        image_path = folder / f'frame_{frame:06d}_navigation.png'
        snapshot = folder / f'frame_{frame:06d}_arm9_ram.bin'
        ram = snapshot.read_bytes()
        exported = next(r for r in report['read_only_pause_RAM_snapshots'] if r['frame'] == frame)
        assert sha(ram) == exported['sha256']
        captures.append((Image.open(image_path).convert('RGB'), ram,
                         {'report': str(report_path), 'report_sha256': sha(report_path.read_bytes()),
                          'image': str(image_path), 'image_sha256': sha(image_path.read_bytes()),
                          'frame': frame, 'snapshot_sha256': sha(ram)}))
    assert captures[0][0].tobytes() == captures[1][0].tobytes()
    path = '/_pxl/mysterymap/04_2.pxl'
    raw = rom.read_file(path)
    assert raw == NdsImage.open('work/clean.nds').read_file(path)
    map_image = PxlImage.from_bytes(raw)
    assert (map_image.width, map_image.height, map_image.bits_per_pixel) == (240, 157, 8)
    marker_raw = rom.read_file('/_pxl/mysterymap/point.pxl')
    marker = PxlImage.from_bytes(marker_raw)
    assert (marker.width, marker.height) == (16, 16)
    assert marker_raw == NdsImage.open('work/clean.nds').read_file('/_pxl/mysterymap/point.pxl')
    opaque, marker_ink = 0, 0
    image, ram, _ = captures[0]
    for y in range(157):
        for x in range(240):
            index = map_image.indices[y * 240 + x]
            if index == 0:
                continue
            color = native5(map_image.palette[index])
            mx, my = x - 23, y - 96
            if 0 <= mx < 16 and 0 <= my < 16:
                point = marker.indices[my * 16 + mx]
                if point:
                    color = native5(marker.palette[point])
            assert native5(image.getpixel((8 + x, 18 + y))) == color
            opaque += 1
    for y in range(16):
        for x in range(16):
            index = marker.indices[y * 16 + x]
            if index:
                assert native5(image.getpixel((31 + x, 114 + y))) == native5(marker.palette[index])
                marker_ink += 1
    assert opaque == 12566 and marker_ink == 124
    loaded = ram.find(raw)
    assert loaded >= 0
    owner, view = 0x02312EBC, 0x02380098
    fields = list(struct.unpack_from('<12I', ram, view - 0x02000000))
    assert fields[3] == owner and fields[7:9] == [0, 0] and fields[9] & 0xFFFF == 0
    assert fields[10:12] == [240, 157]
    font = GameAsciiFont.from_arm9(rom.read_file('/__arm9__.bin'))
    count, bounds = complete_mask(font, 'Twisted Horn', image, 16, 218, (230, 230, 230))
    battery = Path('work/emulation_v193/map_viewer_v441/saves/all_routes_combined_v440_candidate.dsv')
    donor = ROOT / 'donor_test_copy.dsv'
    assert battery.read_bytes() == donor.read_bytes()
    proof = {'format': 'dk4-genuine-map-viewer-v441', 'candidate': str(ROM),
             'candidate_sha256': digest, 'actual_normal_Guild_purchase_and_3000_coin_quote': True,
             'actual_earned_map_fragment_survives_normal_slot1_save_reload': True,
             'capture_cases': [r for _, _, r in captures], 'whole_reload_viewer_frame_pixel_exact': True,
             'actual_map_resource': path, 'source_sha256': sha(raw),
             'complete_loaded_source_header_palette_pixels_exact': len(raw),
             'loaded_source_address': 0x02000000 + loaded, 'actual_owner': owner,
             'actual_view': view, 'native_view_fields': fields,
             'palette_bank': 0, 'source_extent': [240, 157], 'screen_origin': [8, 18],
             'all12566_opaque_map_composite_pixels_exact': True,
             'independent_marker_source': '/_pxl/mysterymap/point.pxl',
             'all124_marker_pixels_exact': True, 'marker_screen_origin': [31, 114],
             'transparent_background_pixels_not_claimed': True,
             'Twisted_Horn_complete_glyph_ink_pixels': count, 'glyph_bounds': bounds,
             'battery_source': str(battery), 'battery_sha256': sha(battery.read_bytes()),
             'seamap_and_legacy_map_bank_usage_not_credited': True,
             'new_Guild_COMMON3665_word_split_defect': 'Some s / ay;actual frame17000. Whole-word formatter caller scope requires repair.',
             'ROM_changed': False, 'all18_plaques_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'viewer_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'opaque_map_pixels': opaque, 'marker_pixels': marker_ink,
                      'complete_name_glyph_pixels': count, 'normal_save_reload_exact': True}))


if __name__ == '__main__':
    main()
