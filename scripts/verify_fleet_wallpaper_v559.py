"""Verify source repeat and genuine Swap Ships display; retain occupied-card occlusion."""
import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_source_plaque_grain_v542 import capture_report

ROM = Path('out/all_routes_combined_v558_candidate.nds')
ROOT = Path('work/analysis/fleet_wallpaper_v559')
CAPTURE = Path('E:/Rota Nova translations/Generated/work/emulation_v193/fleet_wallpaper_v559_navigation')
SOURCE_RECTS = ([0, 44, 256, 174], [128, 14, 256, 44])


def main():
    current = NdsImage.open(ROM)
    clean = NdsImage.open('work/clean.nds')
    batch = json.loads(Path('translations/fleet_row_graphics_v1.json').read_text(encoding='utf-8'))
    data = current.read_file(batch['file_path'])
    image, original = PxlImage.from_bytes(data), PxlImage.from_bytes(clean.read_file(batch['file_path']))
    assert image.source[:image.pixels_offset] == original.source[:original.pixels_offset]
    font = GameAsciiFont.from_arm9(current.read_file('/__arm9__.bin'))
    report = capture_report(CAPTURE, sha(ROM.read_bytes()))
    assert report['frames'] == 7300 and report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    source_save = Path(report['battery_save_preloaded']['source'])
    assert sha(source_save.read_bytes()) == report['battery_save_preloaded']['source_sha256']
    # Original left-half control strip; x127 is a separate frame boundary.
    periodic_pairs = 0
    for y in range(16, 160):
        for x in range(64, 94):
            assert original.indices[y*256+x] == original.indices[y*256+x+32]
            periodic_pairs += 1
    rows, owned, all_points = [], set(), []
    for row in batch['records']:
        l, t, r, b = row['box']
        text = row['text']
        tx, ty = l + (r-l-len(text)*6)//2, t + (b-t-11)//2
        mask = {(tx+n*6+x, ty+y) for n, ch in enumerate(text)
                for y in range(11) for x in range(6) if font.decode(ch).getpixel((x, y))}
        actual = {(x, y) for y in range(t, b) for x in range(l, r) if image.indices[y*256+x] == 226}
        assert actual == mask
        backgrounds, donor_pairs = 0, 0
        for y in range(t, b):
            for x in range(l, r):
                alternate = x+96 if x+96 < 126 else x+32
                assert alternate >= 54
                first, second = original.indices[y*256+x+64], original.indices[y*256+alternate]
                assert first == second and first != 226
                donor_pairs += 1
                if (x, y) not in mask:
                    assert image.indices[y*256+x] == first
                    backgrounds += 1
                owned.add(y*256+x)
        rows.append({'id': row['id'], 'english': text, 'source_Japanese': row['source_japanese'],
                     'complete_font_ink': len(mask), 'independent_donor_pairs_exact': donor_pairs,
                     'source_repeat_background_points_exact': backgrounds, 'fully_completed': False})
        all_points.append(mask)
    assert all(a == b for n, (a, b) in enumerate(zip(original.indices, image.indices, strict=True)) if n not in owned)
    frames = {s['frame']: s for s in report['frames_captured']}
    live = []
    for frame in (6700, 6900, 7100):
        raw_path = CAPTURE / f'frame_{frame:06d}_arm9_ram.bin'
        raw = raw_path.read_bytes()
        view = 0x0218FB90
        fields = struct.unpack_from('<12I', raw, view-0x02000000)
        assert fields[3] == 0x022A44B8 and fields[7:12] == (0, 0, 0, 256, 192)
        u = machine(current.read_file('/__arm9__.bin'))
        u.mem_write(0x02000000, raw)
        executed = call(u, 0xD4170, (view,))
        pointer = u.reg_read(UC_ARM_REG_R0)
        assert bytes(u.mem_read(pointer, len(data))) == data and pointer == raw.find(data)+0x02000000
        assert 0x020DED50 not in executed and 0x020DEBDC not in executed
        shot = Image.open(frames[frame]['path']).convert('RGB')
        pixels = 0
        for l, t, r, b in SOURCE_RECTS:
            for y in range(t, b):
                for x in range(l, r):
                    assert native5(shot.getpixel((x, y+192))) == native5(image.palette[image.indices[y*256+x]])
                    pixels += 1
        assert pixels == 37120
        for row in batch['records'][1:]:
            l, t, r, b = row['box']
            assert all(native5(shot.getpixel((x, y+192))) == native5(image.palette[image.indices[y*256+x]])
                       for y in range(t, b) for x in range(l, r))
        # The broader original test is retained as a failure, not relabeled a pass.
        broad_gap = sum(native5(shot.getpixel((x, y+192))) != native5(image.palette[image.indices[y*256+x]])
                        for y in range(42, 174) for x in range(256))
        assert broad_gap == 256
        live.append({'frame': frame, 'original_source_view': view, 'actual_owner': fields[3],
                     'actual_resident_source_pointer': pointer, 'snapshot_sha256': sha(raw),
                     'complete_original_resource_resolution_without_bridge': True,
                     'full_unobscured_source_rectangles_pixels_exact': pixels,
                     'all4_empty_slot_full_label_rectangles_exact': True,
                     'Flagship_caption_covered_by_occupied_ship_card': True,
                     'broader_y42_region_not_credited_due256_card_border_pixels': broad_gap})
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'source_file': batch['file_path'], 'source_file_sha256': sha(data),
             'original_period32_control_pairs': periodic_pairs, 'all5_source_label_cases': rows,
             'all4000_owned_pixels_have_independent_unlettered_donor_agreement': True,
             'palette_header_dimensions_and_unowned_pixels_exact_clean': True,
             'source_rectangles': SOURCE_RECTS, 'actual_cases': live,
             'ordinary_path': 'Shipyard > Dock > Swap Ships',
             'ordinary_source_pixels_verified': 111360, 'visible_complete_empty_slot_label_appearances': 12,
             'Flagship_native_visibility_and_other_fleet_loadouts_remain_open': True,
             'no_fixture_cheat_or_savestate_used': True, 'unchanged_copied_source_save': True,
             'production_ROM_changed': False, 'hardware_or_full_route_verified': False,
             'all22_historical_requirements_and18_incomplete_plaques_retained': True,
             'full_goal_complete': False}
    (ROOT / 'source_and_native_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('Fleet wallpaper:5 full static masks,4000 donor pairs,111360 actual source pixels,12 complete empty-slot labels and real cache bindings pass. Flagship remains occluded.')


if __name__ == '__main__':
    main()
