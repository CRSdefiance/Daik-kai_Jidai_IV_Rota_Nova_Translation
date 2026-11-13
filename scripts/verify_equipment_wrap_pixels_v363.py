"""Full expanded item/name confirmations through the actual228x48 contract."""

import json
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.rom.nds import NdsImage
from scripts.execute_modal_v362 import execute
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels

ROOT = Path('work/analysis/equipment_wrap_v363')


def main():
    arm = (ROOT / 'research_arm9.bin').read_bytes()
    image = NdsImage.open('out/all_routes_combined_v360_candidate.nds')
    original = image.read_file('/__arm9__.bin')
    font = image.read_file('/GRP/KANJI.FNT')
    geometry = json.loads(Path('work/analysis/equipment_confirmation_v362/actual_geometry.json').read_text())
    items = json.loads((ROOT / 'native_item_names.json').read_text(encoding='utf-8'))
    actors = ['Rafael Castor', 'Hodram Joakim Bergstrom', 'Lil Argot',
              'Camille Marinus Overijssel', 'Maria Huamei Li']
    u = machine(arm)
    source, output = STACK + 0x100, STACK + 0x300
    cases = []
    for actor in actors:
        for item in items:
            text = f"  {actor} equipped {item['text']}."
            assert text.isascii()
            u.mem_write(source - 16, b'\xA5' * 16 + text.encode() + b'\0' + b'\xA5' * 16)
            u.mem_write(output - 16, b'\xA5' * 272)
            call(u, 0x01FFCA00 - 0x02000000, (source, output))
            length = u.reg_read(UC_ARM_REG_R0)
            assert length > 0
            compiled = bytes(u.mem_read(output, length)).decode()
            assert ' '.join(compiled.split()) == ' '.join(text.split())
            assert bytes(u.mem_read(source, len(text) + 1)) == text.encode() + b'\0'
            assert bytes(u.mem_read(output - 16, 16)) == b'\xA5' * 16
            assert bytes(u.mem_read(output + 240, 16)) == b'\xA5' * 16
            for mode in (4, 16):
                native = execute(original, compiled, modal=True, mode=mode, kanji_font=font,
                                 modal_guarded=True, confirmation_contract=geometry)
                events = [e for e in native['glyph_events'] if e['code'] != 32]
                expected_codes = [ord(c) for c in compiled if c not in ' \n']
                assert [e['code'] for e in events] == expected_codes
                assert len({(e['x'], e['y']) for e in events}) == len(events)
                assert all(0 <= e['x'] and e['x'] + 6 <= 228 and 0 <= e['y'] and e['y'] + 11 <= 48 for e in events)
                assert native['pixels'] == expected_pixels(original, font, native['glyph_events'], mode, background=9)
                cursor = 0
                for word in text.split():
                    selected = events[cursor:cursor + len(word)]
                    assert len({e['y'] for e in selected}) == 1, (actor, item['text'], word)
                    cursor += len(word)
            cases.append({'actor': actor, 'item_id': item['id'], 'item': item['text'],
                          'compiled_layout': compiled, 'both_pixel_formats_full_pixels_exact': True,
                          'all_words_unsplit_and_first_final_letters_in_bounds': True})
    proof = {'cases': cases, 'expansions': len(cases), 'native_pixel_cases': len(cases) * 2,
             'captured_actual_confirmation_geometry': geometry,
             'item_names_are_native_getter_outputs_not_all_equippable_availability': True,
             'source_prose_and_name_values_unchanged': True,
             'actual_short_equipment_confirmation_and_long_item_path_pending': True,
             'all18_plaques_remain_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'pixel_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print(f'{len(cases)} expansions/{len(cases)*2} full native rasters pass without split words or missing letters.')


if __name__ == '__main__':
    main()
