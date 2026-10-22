"""Verify complete observed map states; do not infer untraced visibility producers."""
import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_map_overlays_v552 import CAPTURE, ROM, SPECS
from scripts.verify_portrait_native_pixels_v202 import native5

ROOT = Path('work/analysis/map_states_v553')
EXPECTED_SHA = '499e0ad767b1badf899ab6873ad787f171651035c7d6316012af2b8afc8c77d3'


def colours(data):
    return [(v & 31, (v >> 5) & 31, (v >> 10) & 31)
            for v, in struct.iter_unpack('<H', data)]


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert sha(ROM.read_bytes()) == EXPECTED_SHA
    rom = NdsImage.open(ROM)
    clean = NdsImage.open('work/clean.nds')
    arm = rom.read_file('/__arm9__.bin')
    original_caption = clean.read_file('/__arm9__.bin')[0x14C79C:0x14C79C + 32].split(b'\0', 1)[0]
    assert original_caption.decode('cp932') == '北海'
    font = GameAsciiFont.from_arm9(arm)
    report = json.loads((CAPTURE / 'capture_report.json').read_text(encoding='utf-8'))
    assert report['ROM_sha256'] == EXPECTED_SHA
    assert report['cold_boot'] and not report['savestate_loaded']
    assert not report.get('battery_save_preloaded') and not report['callback_errors']
    cases = []
    for frame in (35400, 35600, 35800, 36000):
        shot = next(s for s in report['frames_captured'] if s['frame'] == frame)
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
        raw_path = CAPTURE / f'frame_{frame:06d}_arm9_ram.bin'
        raw = raw_path.read_bytes()
        image = Image.open(shot['path']).convert('RGB')
        assert image.size == (256, 384)
        actual = [native5(image.getpixel((x + 6, y + 208)))
                  for y in range(160) for x in range(244)]
        assert struct.unpack_from('<5I', raw, 0x279B38) == (4, 61, 160, 20, 52)
        palette = colours(raw[0x279B4C:0x279B6C])
        indices = [n for byte in raw[0x279B6C:0x279B6C + 19520]
                   for n in (byte & 15, byte >> 4)]
        composed = [palette[n] for n in indices]

        def put(x, y, colour, target=composed):
            assert 6 <= x < 250 and 208 <= y < 368
            target[(y - 208) * 244 + x - 6] = colour

        # Presence is an observed-state contract, not a proven native predicate.
        arrow_present = frame == 36000
        caption_present = frame in (35400, 35600)
        overlay_cases = []
        for spec in SPECS:
            data = rom.read_file(spec['path'])
            original = clean.read_file(spec['path'])
            atlas = PxlImage.from_bytes(data)
            old = PxlImage.from_bytes(original)
            sx, sy, ex, ey = spec['source']
            bank = spec['bank']
            fields = struct.unpack_from('<12I', raw, spec['view'] - 0x02000000)
            assert fields[3] == spec['owner'] and fields[7:9] == (sx, sy)
            assert fields[9] & 0xFFFF == bank
            assert fields[10:12] == (ex - sx, ey - sy)
            source_palette = data[20 + bank * 32:52 + bank * 32]
            assert source_palette == original[20 + bank * 32:52 + bank * 32]
            assert all(atlas.indices[y * atlas.width + x] == old.indices[y * old.width + x]
                       for y in range(sy, ey) for x in range(sx, ex))
            present = arrow_present if spec['view'] == 0x0218BCAC else True
            colour_bank = colours(source_palette)
            dx, dy = spec['destination']
            ink = 0
            for y in range(ey - sy):
                for x in range(ex - sx):
                    index = atlas.indices[(sy + y) * atlas.width + sx + x]
                    if index:
                        ink += 1
                        if present:
                            put(dx + x, dy + y, colour_bank[index])
            assert ink == spec['opaque']
            overlay_cases.append({'path': spec['path'], 'bank': bank,
                                  'source': spec['source'], 'present_in_observed_frame': present,
                                  'complete_source_ink_pixels': ink})
        caption_ink = 0
        if caption_present:
            text = raw[0x14C79C:0x14C79C + 32].split(b'\0', 1)[0].decode('ascii')
            assert text == 'N. Sea'
            # Exact observed primitive geometry; original painter/order is untraced.
            for y in range(248, 264):
                for x in range(123, 163):
                    put(x, y, (31, 31, 31))
            for n, ch in enumerate(text):
                glyph = font.decode(ch)
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x, y)):
                            put(125 + n * 6 + x, 250 + y, (0, 1, 0))
                            caption_ink += 1
            assert caption_ink == 66
            for y in range(229, 249):
                for x in range(123, 146):
                    if x in (123, 145) or y in (229, 248):
                        put(x, y, (0, 0, 31))
        mismatches = sum(a != b for a, b in zip(actual, composed, strict=True))
        assert mismatches == 0, (frame, mismatches)
        # Deliberately remove complete first/final glyphs to demonstrate sensitivity.
        negative_counts = []
        if caption_present:
            for n in (0, len(text) - 1):
                erased = composed.copy()
                glyph = font.decode(text[n])
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x, y)):
                            pos = (250 + y - 208) * 244 + 125 + n * 6 + x - 6
                            erased[pos] = (31, 31, 31)
                count = sum(a != b for a, b in zip(actual, erased, strict=True))
                assert count > 0
                negative_counts.append(count)
        visibility_field = struct.unpack_from('<I', raw, 0x18BCAC + 0x70)[0]
        cases.append({'frame': frame, 'snapshot': str(raw_path), 'snapshot_sha256': sha(raw),
                      'PNG_sha256': shot['PNG_sha256'], 'complete_map_pixels_exact': 39040,
                      'mismatches': mismatches, 'source_overlays': overlay_cases,
                      'caption': 'N. Sea' if caption_present else None,
                      'caption_ink_pixels_exact': caption_ink,
                      'first_final_glyph_erasure_negative_mismatches': negative_counts,
                      'observed_arrow_object_plus70_word': visibility_field,
                      'native_visibility_predicate_proven': False})
    proof = {'candidate': str(ROM), 'candidate_sha256': EXPECTED_SHA,
             'production_ROM_changed': False, 'capture_report': str(CAPTURE / 'capture_report.json'),
             'cases': cases, 'complete_observed_map_pixels_exact': 156160,
             'caption_source_Japanese': original_caption.decode('cp932'),
             'caption_English': 'N. Sea', 'caption_meaning': 'North Sea',
             'no_excluded_map_pixels': True,
             'caption_geometry_and_primitive_order_are_empirical': True,
             'original_visibility_and_caption_painters_remain_open': True,
             'unobserved_animation_states_and_mask_creation_remain_open': True,
             'legacy_CMMN_and_sepia_contexts_remain_open': True,
             'full_route_or_hardware_verification': False, 'full_goal_complete': False}
    (ROOT / 'observed_state_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Four ordinary map states: all156160 pixels exact; caption66 ink pixels and first/final negatives pass.')


if __name__ == '__main__':
    main()
