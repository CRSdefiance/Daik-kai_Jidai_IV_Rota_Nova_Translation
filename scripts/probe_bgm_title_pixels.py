"""Execute native BGM centering and exact title pixels in the 128-pixel panel."""

import argparse
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, machine_for
from scripts.execute_scene_caption_raster import execute
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels

TEXT = 0x02431000


def center(source, text):
    machine = machine_for(source)
    machine.mem_write(TEXT, text.encode('ascii') + b'\0')
    machine.reg_write(UC_ARM_REG_R0, TEXT)
    machine.emu_start(BASE + 0x10927C, BASE + 0x1092A8, count=10000)
    if machine.reg_read(UC_ARM_REG_PC) != BASE + 0x1092A8:
        raise ValueError('Native BGM strlen/centering fails to reach draw call')
    tracking = struct.unpack('<i', machine.mem_read(STACK + 0x1C, 4))[0]
    x, y = struct.unpack('<2I', machine.mem_read(STACK + 0x24, 8))
    if (tracking, x, y) != (-1, 64 - len(text) * 5 // 2, 50):
        raise ValueError('Native BGM centering differs from mapped five-pixel tracking')
    return x, y, tracking


def verify(source, font, text, mode):
    x, y, tracking = center(source, text)
    native = execute(source, text, x=x, y=y, tracking=tracking, mode=mode,
                     surface_size=(128, 160))
    events = native['glyph_events']
    if [e['code'] for e in events] != list(text.encode('ascii')):
        raise ValueError('Native BGM title drops a leading, internal or final glyph')
    if any(e['kind'] != 'ascii' or e['x'] < 0 or e['x'] + 6 > 128
           or e['y'] != 50 or e['y'] + 12 > 160 for e in events):
        raise ValueError('Native BGM title clips or wraps outside the actual panel')
    if native['pixels'] != expected_pixels(source, font, events, mode, background=9):
        raise ValueError('Native BGM title pixels differ from independent font decoding')
    return native


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-v155', action='store_true')
    args = parser.parse_args()
    candidate_path = Path('out/all_routes_combined_v155_candidate.nds' if args.current_v155
                          else 'out/all_routes_combined_v143_candidate.nds')
    expected = ('d704b60955db30d27b3d48858107096934fd2af08ecd1f3bf3fc2ba4dd884b11' if args.current_v155
                else '2c4cf489bfaaff8b187744e085a0ee8314dc10e4054048f60e9156cf5d786984')
    rom = NdsImage.open(candidate_path)
    if sha(candidate_path.read_bytes()) != expected:
        raise ValueError('Exact complete source candidate required')
    source, font = rom.read_file('/__arm9__.bin'), rom.read_file('/GRP/KANJI.FNT')
    proof_path = Path('work/analysis/native_sound_selector_bounds_v155_proof.json' if args.current_v155
                      else 'work/analysis/native_sound_selector_bounds_proof.json')
    proof = json.loads(proof_path.read_text(encoding='utf-8'))
    if proof['candidate_sha256'] != expected:
        raise ValueError('BGM lookup proof source differs')
    cases = []
    sheet = Image.new('RGB', (536, 38 * 50), 'white')
    draw = ImageDraw.Draw(sheet)
    for index, row in enumerate(proof['native_title_cases']):
        for mode in (4, 16):
            native = verify(source, font, row['english'], mode)
            cases.append({'native_id': row['native_id'], 'english': row['english'], 'mode': mode,
                          'native_origin': list(center(source, row['english'])[:2]),
                          'pixels_sha256': sha(native['pixels']),
                          'complete_glyphs_inside_panel_and_independent_pixels_match': True})
            if mode == 16:
                panel = Image.new('RGB', (256, 192))
                panel.putdata([(255, 255, 255) if c == 9 else (128, 128, 128) if c == 14 else (0, 0, 0)
                               for c in struct.unpack('<49152H', native['pixels'])])
                ink = panel.crop((0, 48, 128, 64)).resize((512, 32), Image.Resampling.NEAREST)
                draw.text((10, index * 50), f'ID {row["native_id"]}', fill='black')
                sheet.paste(ink, (10, index * 50 + 15))
    destination = Path('work/qa/bgm_native_titles_v155' if args.current_v155 else 'work/qa/bgm_native_titles_v143')
    destination.mkdir(parents=True, exist_ok=True)
    sheet.save(destination / 'native_sheet.png')
    report = {'status': 'pass-native-bgm-title-centering-and-pixels-visual-review-pending',
              'candidate_sha256': expected, 'candidate_arm9_sha256': sha(source), 'cases': cases,
              'native_lookup_proof': str(proof_path), 'native_lookup_proof_sha256': sha(proof_path.read_bytes()),
              'limitations': 'Native strlen/centering and renderer execute across separate invocations. Parent bitmap setup/origin, glyph source copy, physical palette/routing, audio playback and input remain contracts. This proves title ink layout, not full Sound Setup gameplay.'}
    (destination / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} actual native BGM title pixel cases fit the 128-pixel panel with every glyph intact.')


if __name__ == '__main__':
    main()
