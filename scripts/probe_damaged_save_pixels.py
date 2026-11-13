"""Render complete damaged-save drafts through the unchanged native modal path."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import BASE
from scripts.probe_common_tribute_modal_pixels import verify
from scripts.probe_damaged_save_message import SOURCE


def main():
    current = NdsImage.open('out/all_routes_combined_v144_candidate.nds')
    source = current.read_file('/__arm9__.bin')
    renderer = NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')
    font = current.read_file('/GRP/KANJI.FNT')
    if (sha(source) != SOURCE
            or MainCodeFile(source, BASE).sections[1].data[:6944] != MainCodeFile(renderer, BASE).sections[1].data
            or any(source[a:b] != renderer[a:b] for a, b in ((0x548A8, 0x54988),
                                                           (0xD1500, 0xD5B00), (0x125A60, 0x125E75)))):
        raise ValueError('Current native modal/font path differs from renderer')
    proof_path = Path('work/analysis/damaged_save_message_proof.json')
    proof = json.loads(proof_path.read_text(encoding='utf-8'))
    selected = [proof['cases'][n] for n in (0, 8, 9, 98, 99, 255)]
    destination = Path('work/qa/damaged_save_native')
    destination.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1024, len(selected) * 224), 'white')
    draw = ImageDraw.Draw(sheet)
    cases = []
    for index, case in enumerate(selected):
        text = case['complete_text']
        for mode in (4, 16):
            native = verify(renderer, font, text, mode, guarded=True)
            events = [event for event in native['glyph_events'] if event['code'] != 32]
            cursor, split_words = 0, []
            for word in text.split():
                rows = {event['y'] for event in events[cursor:cursor + len(word)]}
                if len(rows) > 1:
                    split_words.append(word)
                cursor += len(word)
            cases.append({'display_number': case['display_number'], 'mode': mode,
                          'complete_text': text, 'pixels_sha256': sha(native['pixels']),
                          'complete_glyph_order_and_independent_pixels': True,
                          'split_words': split_words, 'formatting_approved': False})
            if mode == 16:
                panel = Image.new('RGB', (256, 192))
                panel.putdata([(255, 255, 255) if c == 9 else (128, 128, 128) if c == 14
                               else (0, 0, 0) for c in struct.unpack('<49152H', native['pixels'])])
                panel = panel.crop((0, 0, 256, 96)).resize((1024, 192), Image.Resampling.NEAREST)
                draw.text((8, index * 224 + 4), f"Save {case['display_number']}; split words: {split_words}", fill='black')
                sheet.paste(panel, (0, index * 224 + 24))
    sheet_path = destination / 'native_sheet.png'
    sheet.save(sheet_path)
    report = {'status': 'pass-native-damaged-save-glyphs-pixels-word-layout-review-pending',
              'candidate_changed': False, 'prepared_proof_sha256': sha(proof_path.read_bytes()),
              'native_sheet_sha256': sha(sheet_path.read_bytes()), 'cases': cases,
              'limits': 'Native preparation and renderer execute separately; full load-error caller/widgets/input and physical gameplay remain pending.'}
    (destination / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f"{len(cases)} native damaged-save raster cases pass; split words: {sorted({w for c in cases for w in c['split_words']})}")


if __name__ == '__main__':
    main()
