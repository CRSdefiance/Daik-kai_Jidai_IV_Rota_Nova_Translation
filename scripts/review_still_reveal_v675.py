"""Paired actual emulator crops and independent original-source reveal models."""

import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_movie_transition_bitmaps_v648 import rgb
from scripts.verify_still_reveal_v675 import ROOT, SCAN, band_words
from scripts.verify_village_wrap_v608 import read, save


def main():
    proof, pre = read(ROOT / 'proof.json'), read(ROOT / 'preflight.json')
    rom = NdsImage.open(pre['candidate'])
    data = rom.read_file(proof['original_source'])
    _, _, _, p, d = struct.unpack_from('<5I', data)
    palette = struct.unpack_from('<256H', data, p)
    source = [palette[i] | 32768 for i in data[d:]]
    cases = {c['frame']: c for c in proof['actual_upper_source_and_display_cases']}
    report = read(SCAN / 'capture_report.json')
    shots = {s['frame']: s for s in report['frames_captured']}
    frames = (3750, 3762, 3780, 3786, 3800, 3804, 3812, 3900)
    sheet = Image.new('RGB', (1024, 900), (25, 31, 37))
    draw, rows = ImageDraw.Draw(sheet), []
    for index, frame in enumerate(frames):
        case = cases[frame]
        mixed = case['mixed_source_frame_original_DMA_prediction']
        if mixed:
            before = band_words(source, mixed['previous_phase'])
            after = band_words(source, mixed['current_before_paint_phase'])
            cut = mixed['first_observed_upper_DMA_line'] * 256
            words = before[:cut] + after[cut:]
        else:
            words = band_words(source, case['observed_source_whole_bitmap_phase'])
        expected = Image.new('RGB', (256, 192))
        expected.putdata(rgb(words))
        actual = Image.open(shots[frame]['path']).convert('RGB').crop((0, 0, 256, 192))
        assert actual.tobytes() == expected.tobytes()
        x, y = (index % 2) * 512, (index // 2) * 225
        draw.text((x + 8, y + 8), f'{frame} actual emulator', fill='white')
        draw.text((x + 264, y + 8), f'{frame} original source model', fill='white')
        sheet.paste(actual, (x, y + 28))
        sheet.paste(expected, (x + 256, y + 28))
        rows.append({'frame': frame, 'actual_capture': shots[frame], 'all49152_RGB_pixels_exact': True})
    path = ROOT / 'actual_reveal_states.png'
    sheet.save(path)
    save(ROOT / 'review_packet.json', {'sheet': str(path), 'sha256': sha(path.read_bytes()),
        'frames': rows, 'purpose': 'actual and independently reconstructed reveal review; test evidence only',
        'not_guide_approval_or_full_Maria_opening_completion': True,
        'script_sha256': sha(Path(__file__).read_bytes())})
    print('V675 eight actual/source reveal pairs generated.', flush=True)


if __name__ == '__main__':
    main()
