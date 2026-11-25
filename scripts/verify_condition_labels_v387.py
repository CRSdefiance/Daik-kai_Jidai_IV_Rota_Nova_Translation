"""Verify exact native selectors and full rasters from real string addresses."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine
from scripts.verify_modal_cursor_native_v272 import raster
from scripts.verify_sailor_status_tables_v274 import verify_selectors

ROOT = Path('work/analysis/condition_labels_v387')


def main():
    target = (ROOT / 'research_arm9.bin').read_bytes()
    prior = NdsImage.open('out/all_routes_combined_v383_candidate.nds').read_file('/__arm9__.bin')
    plan = json.loads((ROOT / 'plan.json').read_text(encoding='utf-8'))
    changes = {(r['group'], r['state']): r for r in plan['pointer_changes']}
    before, after = verify_selectors(prior), verify_selectors(target)
    for a, b in zip(before, after, strict=True):
        group, state, old = a
        assert b[:2] == a[:2]
        expected = changes[group, state]['new_pointer'] if (group, state) in changes else old
        assert b[2] == expected
    font = GameAsciiFont.from_arm9(target)
    u = machine(target)
    cases = []
    sheet = Image.new('RGB', (520, 13 * 46 + 12), 'white')
    drawing = ImageDraw.Draw(sheet)
    for group, field, count in [('Mood', 0x1483B0, 6), ('Health', 0x1483C8, 7)]:
        for state in range(count):
            pointer = struct.unpack_from('<I', target, field + 4 * state)[0]
            raw = bytes(u.mem_read(pointer, 32)).split(b'\0', 1)[0]
            assert raw and raw.isascii() and len(raw) <= 8
            pixels, events, returned = raster(target, raw, width=48, height=16,
                                               wrapping=0, native_pointer=pointer)
            assert returned == len(raw)
            visible = [r for r in events if r['code'] != 32]
            assert [r['code'] for r in visible] == list(raw)
            assert [(r['x'], r['y']) for r in visible] == [(i * 6, 0) for i in range(len(raw))]
            expected = bytearray(48 * 16)
            for i, character in enumerate(raw.decode()):
                glyph = font.decode(character)
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x, y)):
                            expected[y * 48 + i * 6 + x] = 1
            assert pixels == expected
            changed = (group, state) in changes
            if not changed:
                assert raster(prior, raw, width=48, height=16, wrapping=0, native_pointer=pointer) == (pixels, events, returned)
            row = {'group': group, 'state': state, 'English': raw.decode(), 'native_pointer': pointer,
                   'complete_ink_pixels': sum(expected), 'all48x16_pixels_and_first_final_glyph_cells_exact': True,
                   'native_source_and_bitmap_guards_and_ABI_pass': True, 'changed': changed}
            cases.append(row)
            y = (len(cases) - 1) * 46 + 6
            drawing.text((8, y + 6), f'{group} {state}: {raw.decode()}', fill='black')
            preview = Image.frombytes('L', (48, 16), bytes(255 * n for n in pixels)).convert('RGB')
            sheet.paste(preview.resize((144, 48), Image.Resampling.NEAREST), (330, y))
    sheet.save(ROOT / 'native_condition_review.png')
    proof = {'source_arm9_sha256': sha(prior), 'target_arm9_sha256': sha(target),
             'all512_selector_values_and_original_fallbacks_guards_ABI_pass': True,
             'selectors_changed_only_for_three_reviewed_valid_states': True,
             'complete_native_rasters_from_actual_original_or_reserved_ITCM_string_pointers': cases,
             'other10_condition_rasters_exact_to_V383': True,
             'review_sheet': str(ROOT / 'native_condition_review.png'),
             'review_sheet_is_isolated_native_render_not_gameplay': True,
             'actual_alternate_condition_gameplay_not_proven': True,
             'all18_plaques_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'native_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('All512 selector cases and13 complete native48x16 rasters pass from real string pointers; other10 exact.')


if __name__ == '__main__':
    main()
