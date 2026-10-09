"""Prove complete manuscript glyph order and pixels through the native renderer."""

import hashlib
import json
import struct
from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts.compile_scene_caption_single_dispatch import compile_scoped_dispatch
from scripts.execute_scene_caption_raster import execute


def expected_pixels(source, text, x, y, mode, *, advance=5, style=1):
    if advance not in (5, 6):
        raise ValueError('Unmapped reference glyph advance')
    font = GameAsciiFont.from_arm9(source)
    palette = struct.unpack_from('<I', source, 0xD181C)[0] - 0x02000000
    if not 0 <= style < 16:
        raise ValueError('Unmapped reference glyph style')
    color = struct.unpack_from('<H', source, palette + style * 2)[0]
    pitch = 256 if mode == 16 else 64
    output = bytearray((b'\x09\x00' if mode == 16 else b'\x99\x99') * (pitch * 192))
    for index, character in enumerate(text):
        bitmap = font.decode(character)
        for row in range(11):
            for column in range(6):
                ink = bool(bitmap.getpixel((column, row)))
                px, py = x + index * advance + column, y + row
                if mode == 16:
                    if ink:
                        struct.pack_into('<H', output, (py * 256 + px) * 2, color)
                else:
                    offset, shift = (py * 256 + px) // 2, (px % 2) * 4
                    output[offset] = (output[offset] & ~(15 << shift)) | ((style if ink else 0) << shift)
    return bytes(output)


def main():
    directory = Path('work/analysis/scene_caption_complete_tracking_v137')
    source = (directory / 'proposed_arm9.bin').read_bytes()
    prior = json.loads((directory / 'report.json').read_text())
    digest = lambda data: hashlib.sha256(data).hexdigest()
    if digest(source) != prior['proposed_arm9_sha256']:
        raise ValueError('Tracking proposal hash differs')
    manuscript = Path('translations/scene_caption_manuscript_v2.json')
    if digest(manuscript.read_bytes()) != prior['manuscript_sha256']:
        raise ValueError('Manuscript changed')
    proposed = compile_scoped_dispatch(source)
    cases = []
    for entry in json.loads(manuscript.read_text(encoding='utf-8'))['records']:
        text = entry['english']
        x = 128 - len(text) * 5 // 2
        for mode in (16, 4):
            result = execute(proposed, text, x=x, mode=mode)
            expected = [{'code': ord(c), 'style': 1, 'x': x + i * 5, 'y': 70} for i, c in enumerate(text)]
            if result['glyphs'] != expected or result['final_x'] != x + len(text) * 5:
                raise ValueError(f'Complete native glyph order/advance failed: {entry["id"]}')
            if result['pixels'] != expected_pixels(source, text, x, 70, mode):
                raise ValueError(f'Complete native pixel raster failed: {entry["id"]}, mode {mode}')
            cases.append({'id': entry['id'], 'mode': mode, 'glyph_count': len(text),
                          'pixels_sha256': digest(result['pixels']), 'x': x,
                          'final_x': result['final_x'], 'stack_and_registers_preserved': True})
    compatibility = []
    for text in ('A', 'Maria', 'Grand Race', 'A B!', 'Yahoo!'):
        for mode in (16, 4):
            for tracking in (0, 1, -2):
                before = execute(source, text, mode=mode, tracking=tracking)
                after = execute(proposed, text, mode=mode, tracking=tracking)
                for field in ('glyphs', 'pixels', 'final_x', 'copy_calls'):
                    if before[field] != after[field]:
                        raise ValueError('Existing non-minus-one renderer behavior changed')
                compatibility.append({'text': text, 'mode': mode, 'tracking': tracking})
    for font_class in ('generic', 'controller-icons'):
        for text in ('港町', 'A港町B', 'L1', 'R1'):
            for mode in (16, 4):
                for tracking in (0, 1, -2, -1):
                    if font_class == 'generic' and tracking == -1 and text != '港町':
                        continue  # Uniform five-pixel generic ASCII is intentional.
                    before = execute(source, text, mode=mode, tracking=tracking, font_class=font_class)
                    after = execute(proposed, text, mode=mode, tracking=tracking, font_class=font_class)
                    for field in ('glyphs', 'cp932_glyphs', 'pixels', 'final_x', 'copy_calls'):
                        if before[field] != after[field]:
                            raise ValueError(f'Native class/CP932 compatibility changed: {font_class}/{text}')
                    compatibility.append({'text': text, 'mode': mode, 'tracking': tracking,
                                          'font_class': font_class})
    output = Path('work/analysis/scene_caption_complete_scoped_raster_v137')
    output.mkdir(parents=True, exist_ok=True)
    (output / 'proposed_arm9.bin').write_bytes(proposed)
    report = {'status': 'pass-native-ascii-caption-glyphs-and-full-buffer-pixels',
              'source_arm9_sha256': digest(source), 'proposed_arm9_sha256': digest(proposed),
              'manuscript_sha256': digest(manuscript.read_bytes()), 'cases': cases,
              'compatibility_cases': compatibility, 'rom_written': False,
              'limitations': ['Initialized runtime font metrics (6 by 12) and bitmap type 5 are contracts.',
                             'Bitmap origin getter and eleven-byte glyph copy are modeled; all renderer/callback/painter bodies execute.',
                             'CP932 ITCM pixel painting is modeled; complete byte/glyph requests and positions execute.',
                             'Both literal font classes sharing D4DA8 are locked; computed/overlay class ownership still requires release coverage.',
                             'Physical screen routing, wrapper callers and gameplay remain pending.']}
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f'{len(cases)} complete native caption rasters; {len(compatibility)} unchanged-spacing cases pass.')


if __name__ == '__main__':
    main()
