"""Preserve the failed bare-LF contrast and detect missing first/final glyphs."""

from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.personal_chatter_layout_v836 import compiled, layout
from scripts.probe_personal_fonts_v836 import ROOT, ROM, CAP, execute
from scripts.verify_village_wrap_v608 import read, save


def main():
    rom = NdsImage.open(ROM)
    raw = (CAP / 'frame_015200_arm9_ram.bin').read_bytes()
    doc = read('translations/personal_chatter_editorial_manuscript_v1.json')
    proof = read(ROOT / 'native_font_proof.json')
    row = next(r for r in doc['records'] if r['message_id'] == 1375)
    lines = layout(row['english'])
    bare = '\n'.join(lines).encode('ascii')
    failed = False
    try:
        execute(rom, raw, row['actor_ID'], bare, lines)
    except AssertionError as error:
        assert error.args[0][0] == 'independent complete words/coordinates'
        failed = True
    assert failed
    before, a = execute(rom, raw, row['actor_ID'], bare)
    after, b = execute(rom, raw, row['actor_ID'], compiled(row), lines)
    assert before['native_text_bytes_consumed'] == len(bare)
    assert before['native_glyph_request_lines_including_trailing_blank_cells'][0].endswith('S')
    assert before['native_glyph_request_lines_including_trailing_blank_cells'][1].startswith('neaking')
    assert after['independent_authored_words_at_x0_12px_rows_match_every_pixel'] and a != b
    sheet = Image.new('RGB', (1028, 224), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, (plane, title) in enumerate(((a, 'Rejected bare LF: S on previous row'), (b, 'Generated phase space: complete aligned words'))):
        draw.text((i * 514 + 5, 5), title, fill='white')
        image = Image.frombytes('L', (252, 96), bytes(0 if v else 255 for v in plane))
        sheet.paste(image.resize((504, 192), Image.Resampling.NEAREST), (i * 514 + 5, 27))
    path = ROOT / 'bare_LF_rejected_vs_generated_phase_2x.png'
    sheet.save(path)
    font = GameAsciiFont.from_arm9(rom.read_file('/__arm9__.bin'))
    controls = []
    for case in proof['cases']:
        image = Image.open(case['preview']).convert('L')
        assert sha(Path(case['preview']).read_bytes()) == case['preview_sha256']
        for y, line in enumerate(case['generated_native_lines']):
            for index in (0, len(line) - 1):
                glyph = font.decode(line[index])
                ink = [(index * 6 + x, 60 + y * 12 + row) for row in range(11) for x in range(6) if glyph.getpixel((x, row))]
                assert ink and all(image.getpixel(p) == 0 for p in ink)
                damaged = image.copy()
                for p in ink:
                    damaged.putpixel(p, 255)
                assert damaged.tobytes() != image.tobytes()
                controls.append({'message_id': case['message_id'], 'row': y, 'character_index': index,
                                 'character': line[index], 'all_original_glyph_ink_present': True,
                                 'erasing_complete_glyph_is_detected': True})
    rejected = []
    for text in (' Leading indent', 'Double  spacing', 'Manual\nbreak', 'An argument %s', 'A macro {FI}', '日本語', 'A' * 43):
        try:
            compiled({'english': text})
        except ValueError:
            rejected.append(text)
        else:
            raise AssertionError(('invalid authored paragraph accepted', text))
    save(ROOT / 'phase_and_letter_controls.json', {
        'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'bare_LF_full_byte_consumption_still_has_wrong_glyph_positions': before,
        'encoded_odd_row_pre_LF_space_preserves_full_words_and_zero_indent': after,
        'contrast_sheet': str(path), 'contrast_sheet_sha256': sha(path.read_bytes()),
        'all25_first_and_final_glyph_erasure_controls': controls,
        'invalid_authored_spacing_break_formatting_and_oversize_word_rejections': rejected,
        'all144_native_three_row_parities_proof': str(ROOT / 'native_font_proof.json'),
        'native_font_proof_sha256': sha((ROOT / 'native_font_proof.json').read_bytes()),
        'compiler_sha256': sha(Path('scripts/personal_chatter_layout_v836.py').read_bytes()),
        'no_global_other_consumer_safety_or_actual_gameplay_claim': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'Bare LF rejected by complete pixels;generated phase repair passes. {len(controls)} first/final glyph erasure controls and7 invalid-author controls pass.',flush=True)


if __name__ == '__main__':
    main()
