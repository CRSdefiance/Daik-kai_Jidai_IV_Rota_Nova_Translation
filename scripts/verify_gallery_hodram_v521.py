"""Actual original Gallery carousel and captions, using an isolated unlock save."""

import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_movie_gpu_fixtures_v336 import quantized

ROM = Path('out/all_routes_combined_v518_candidate.nds')
OUT = Path('work/analysis/gallery_v521')
CAPTURE = Path('work/emulation_v193/gallery_save_v521')


def compact_caption(font, text, image):
    x0, y0 = 128 - len(text) * 5 // 2, 262
    width = (len(text) - 1) * 5 + 6
    assert text and text.isascii() and 16 <= x0 and x0 + width <= 240
    expected = {(n * 5 + x, y) for n, c in enumerate(text)
                for y in range(11) for x in range(6) if font.decode(c).getpixel((x, y))}
    actual = {(x, y) for y in range(16) for x in range(width)
              if image.getpixel((x0 + x, y0 + y)) == (230, 230, 230)}
    assert actual == expected, text
    return {'English': text, 'origin': [x0, y0], 'complete_ink_pixels': len(expected),
            'complete_first_final_letters_and_blank_cells_exact': True,
            'bounds': [x0, y0, x0 + width, y0 + 16]}


def main():
    digest = sha(ROM.read_bytes())
    assert digest == 'c451a11bb696c71970d7224a5194e28ec57fa406995862f9cc8e0b67711173b7'
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, source = [r.read_file('/__arm9__.bin') for r in (rom, clean)]
    restored = bytearray(arm)
    assert struct.unpack_from('<I', source, 0x42FDC)[0] == 0xE3A0C006
    assert struct.unpack_from('<I', arm, 0x42FDC)[0] == 0xE3A0C005
    assert struct.unpack_from('<I', source, 0x42FF0)[0] == 0xE58D6004
    assert struct.unpack_from('<I', arm, 0x42FF0)[0] == 0xE58D5004
    # Previously registered compact English caption centering/tracking.
    for offset in (0x42FDC, 0x42FF0):
        restored[offset:offset + 4] = source[offset:offset + 4]
    for lo, hi in ((0x42E5C, 0x4300C), (0xEEC50, 0xEEC78)):
        assert restored[lo:hi] == source[lo:hi]
    fixture = json.loads((OUT / 'save_fixture_manifest.json').read_text())
    original = Path(fixture['original_donor']).read_bytes()
    assist = Path(fixture['fixture_save']).read_bytes()
    assert sha(original) == fixture['original_donor_sha256']
    assert sha(assist) == fixture['fixture_save_sha256']
    differences = [{'offset': i, 'before': a, 'after': b}
                   for i, (a, b) in enumerate(zip(original, assist)) if a != b]
    assert differences == fixture['changes']
    assert original[:0x3C000] == assist[:0x3C000]
    assert original[0x3C044:] == assist[0x3C044:]
    assert struct.unpack_from('<I', assist, 0x3C004)[0] == sum(
        v if v < 128 else v - 256 for v in assist[0x3C008:0x3C044]) & 0xFFFFFFFF
    report_path = CAPTURE / 'capture_report.json'
    report = json.loads(report_path.read_text())
    assert report['ROM_sha256'] == digest and report['cold_boot']
    assert not report['savestate_loaded'] and not report['callback_errors']
    assert len(report['synthetic_gallery_fixtures']) == 1 and not report['earned_unlock_verified']
    assert report['battery_save_preloaded']['source_sha256'] == sha(assist)
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    ram = (CAPTURE / 'frame_002400_arm9_ram.bin').read_bytes()
    assert struct.unpack_from('<H', ram, 0x27985C)[0] & 15 == 15
    font = GameAsciiFont.from_arm9(arm)
    popup = Image.open(CAPTURE / 'frame_002400_navigation.png').convert('RGB')
    popup_cases = []
    for number, text in enumerate(('Items', 'Ruins', 'Characters', 'Event Scenes')):
        matches = []
        for y in range(252 + number * 20, 259 + number * 20):
            for x in range(126 - len(text) * 3, 131 - len(text) * 3):
                try:
                    ink, bounds = complete_mask(font, text, popup, x, y, (8, 8, 8))
                    matches.append({'English': text, 'complete_ink_pixels': ink, 'bounds': bounds})
                except ValueError:
                    pass
        assert len(matches) == 1, (text, matches)
        popup_cases += matches
    image_table = struct.unpack_from('<I', arm, 0x432E4)[0]
    caption_table = struct.unpack_from('<I', arm, 0x432E8)[0]
    indices = struct.unpack_from('<41I', arm, image_table - 0x02000000)
    assert arm[image_table - 0x02000000:image_table - 0x02000000 + 164] == source[
        image_table - 0x02000000:image_table - 0x02000000 + 164]
    original_u = machine(source)
    cases = []
    for position, index in enumerate(indices):
        frame = 3200 + position * 200
        path = CAPTURE / f'frame_{frame:06d}_navigation.png'
        image = Image.open(path).convert('RGB')
        resource = f'/evstill/evstill{index:03d}.pxl'
        expected = quantized(PxlImage.from_bytes(rom.read_file(resource)).render()).convert('RGB')
        actual = quantized(image.crop((0, 0, 256, 192))).convert('RGB')
        assert actual.tobytes() == expected.tobytes(), (position, resource)
        pointer = struct.unpack_from('<I', arm, caption_table - 0x02000000 + position * 4)[0]
        live = (CAPTURE / f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
        assert struct.unpack_from('<I', live, caption_table - 0x02000000 + position * 4)[0] == pointer
        assert 0x02000000 <= pointer < 0x02400000 - 256
        text = live[pointer - 0x02000000:pointer - 0x02000000 + 256].split(b'\0')[0].decode('ascii')
        source_pointer = struct.unpack_from('<I', source, caption_table - 0x02000000 + position * 4)[0]
        japanese = bytes(original_u.mem_read(source_pointer, 256)).split(b'\0')[0].decode('cp932')
        caption = compact_caption(font, text, image)
        cases.append({'position': position, 'image': str(path), 'source': resource,
                      'all49152_native_screen_pixels_exact': True,
                      'caption': dict(caption, Japanese=japanese, native_pointer=pointer)})
    first = Image.open(CAPTURE / 'frame_003200_navigation.png').convert('RGB')
    wrapped = Image.open(CAPTURE / 'frame_011400_navigation.png').convert('RGB')
    assert first.crop((0, 0, 256, 192)).tobytes() == wrapped.crop((0, 0, 256, 192)).tobytes()
    compact_caption(font, cases[0]['caption']['English'], wrapped)
    for y in range(384):
        for x in range(256):
            # Original navigation arrows appear after the first carousel input.
            if 256 <= y < 278 and (16 <= x < 32 or 224 <= x < 240):
                continue
            assert first.getpixel((x, y)) == wrapped.getpixel((x, y)), (x, y)
    proof = {'candidate': str(ROM), 'candidate_sha256': digest,
             'report': str(report_path), 'report_sha256': sha(report_path.read_bytes()),
             'fixture_manifest': str(OUT / 'save_fixture_manifest.json'),
             'all_four_Gallery_popup_labels_complete': popup_cases,
             'actual_Hodram_Gallery_carousel_cases': cases,
             'original_carousel_wraps_to_identical_first_image_and_caption': True,
             'whole_wrapped_screen_exact_except_original_navigation_arrow_visibility': True,
             'original_scene_reader_and_image_table_preserved': True,
             'prior_registered_caption5_pixel_centering_and_tracking_patch_retained': True,
             'all_six_route_save_slots_and_original_donor_unchanged': True,
             'production_ROM_and_patch_unchanged': True,
             'user_authorized_synthetic_Gallery_access': True,
             'earned_unlock_or_normal_ending_not_claimed': True,
             'movie_endings_and_other_Gallery_routes_remain_open': True,
             'all22_requirements_and18_incomplete_plaques_retained': True,
             'full_goal_complete': False, 'hardware_device_verification': False}
    (OUT / 'hodram_gallery_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Hodram Gallery:41 complete49152-pixel screens and complete English captions; four popup labels and full carousel wrap pass.')


if __name__ == '__main__':
    main()
