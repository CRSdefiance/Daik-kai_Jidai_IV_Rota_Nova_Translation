"""Actual drinking-refusal and town/commodity rumor branches with original returns."""

import re
import struct
from pathlib import Path

from PIL import Image, ImageChops

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_tavern_gameplay_v767 import (ROM, ROOT, BODY, ADVANCE, capture,
    snapshot, state, models, persistent_objects, cstring, machine, BASE, format_case,
    raster, independent_font)
from scripts.verify_village_wrap_v608 import read, save


def main():
    rom = NdsImage.open(ROM); arm = rom.read_file('/__arm9__.bin')
    common = rom.read_file('/COMMON/MESFILE.DK4'); blocks = IlnkContainer.parse(common).blocks
    entries = common_message_entries(common, arm, clean=False)
    rows = {r['message_id']: r for r in read('translations/tavern_conversations_editorial_manuscript_v4.json')['records']}
    printf_ptr, wrapped_ptr, cache = [struct.unpack_from('<I', arm, off)[0] for off in (0x5444C, 0x54450, 0x552A0)]
    base_report = read('E:/Rota Nova translations/Generated/work/emulation_v193/tavern_editorial_v767_final_v762/capture_report.json')
    icons = {r['frame']: Image.open(r['path']).convert('RGB').crop(ADVANCE).tobytes() for r in base_report['frames_captured'] if r['frame'] in (5000, 5200, 7000, 7200, 8200, 8400)}
    holds, controls, states, reports = [], [], [], []
    town_animation = read(ROOT / 'Town_tooltip_animation.json')
    assert town_animation['identical_two_original_pixel_variants_no_new_bitmap_palette_or_text']
    specs = [('barmaid_probe', 10200, 850, (9400, 9800, 10600)), ('decline', 9800, 826, (9400, 10200, 10600, 10800))]
    for mode, frame, n, control_frames in specs:
        pa, a, old_arm, before = capture(f'tavern_editorial_v767_{mode}_v762')
        pb, b, _, after = capture(f'tavern_editorial_v767_{mode}_v767')
        assert a['scripted_input_schedule'] == b['scripted_input_schedule'] and a['frames'] == b['frames']
        assert a['core_options'] == b['core_options']
        raw = snapshot(b, frame); template = entries[n].text
        assert cstring(raw, cache + 0x2030) == template and raw.count(blocks[entries[n].block]) == 1
        match = re.fullmatch(b'(.*?)'.join(re.escape(p) for p in template.split(b'%s')), cstring(raw, printf_ptr))
        assert match, (mode, n, cstring(raw, printf_ptr))
        args = match.groups(); cpu = machine(arm); cpu.mem_write(BASE, raw)
        expected = format_case(cpu, rows[n], args)
        assert not expected['findings'] and bytes.fromhex(expected['formatted_hex']) == cstring(raw, wrapped_ptr)
        plane = raster(arm, bytes.fromhex(expected['formatted_hex']), 0x01FFCE40 - BASE, size=(228, 64), instruction_limit=1000000)
        assert plane == independent_font(arm, rom.read_file('/GRP/KANJI.FNT'), expected['lines'])
        x, y = [Image.open(r[frame]['path']).convert('RGB') for r in (before, after)]
        actual = {(i, j) for j in range(BODY[1], BODY[3]) for i in range(BODY[0], BODY[2]) if y.getpixel((i, j)) == (0, 8, 0)}
        predicted = {(16 + i % 228, 296 + i // 228) for i, value in enumerate(plane) if value == 1}
        assert actual == predicted, (mode, n, 'complete glyph plane', len(actual - predicted), len(predicted - actual))
        old_glyphs = {(i, j) for j in range(BODY[1], BODY[3]) for i in range(BODY[0], BODY[2]) if x.getpixel((i, j)) == (0, 8, 0)}
        shadows = {(i + 1, j + 1) for i, j in actual | old_glyphs}
        assert all(x.getpixel((i, j)) == y.getpixel((i, j)) for j in range(BODY[1], BODY[3]) for i in range(BODY[0], BODY[2]) if not (ADVANCE[0] <= i < ADVANCE[2] and ADVANCE[1] <= j < ADVANCE[3]) and (i, j) not in actual | old_glyphs | shadows)
        phase = [f for f, pixels in icons.items() if pixels == y.crop(ADVANCE).tobytes()]
        assert phase
        diff = ImageChops.difference(x, y); diff.paste((0, 0, 0), BODY); diff.paste((0, 0, 0), ADVANCE)
        assert diff.getbbox() is None
        holds.append({'mode': mode, 'frame': frame, 'message_id': n, 'arguments': [v.decode('ascii') for v in args],
            'lines': expected['lines'], 'capture': after[frame], 'complete_native_glyph_blank_paper_and_outside_pixels_exact': True,
            'advance_icon_matches_original_phase_frames': phase})
        for f in control_frames:
            x, y = [Image.open(r[f]['path']).convert('RGB') for r in (before, after)]
            diff = ImageChops.difference(x, y)
            if diff.getbbox() is None:
                controls.append({'mode': mode, 'frame': f, 'complete_two_screen_frame_exact': True})
            else:
                if mode == 'decline' and f in (10600, 10800):
                    bounds = tuple(town_animation['tooltip_bounds'])
                    phase_sha = sha(y.crop(bounds).tobytes())
                    assert phase_sha in town_animation['original_native_pixel_phase_frames']
                    diff.paste((0, 0, 0), bounds); assert diff.getbbox() is None
                    controls.append({'mode': mode, 'frame': f, 'all_pixels_outside_original_Town_tooltip_exact': True,
                        'tooltip_pixel_phase_sha256': phase_sha, 'native_401_frame_animation_proof': str(ROOT / 'Town_tooltip_animation.json')})
                    continue
                phase = [j for j, pixels in icons.items() if pixels == y.crop(ADVANCE).tobytes()]
                assert phase, (mode, f, 'unrecognized advance animation')
                diff.paste((0, 0, 0), ADVANCE); assert diff.getbbox() is None, (mode, f, diff.getbbox())
                controls.append({'mode': mode, 'frame': f, 'all_other_pixels_including_unselected_caption_exact': True,
                    'advance_icon_pixel_identical_to_original_frames': phase})
        for f in (frame, *control_frames):
            old_raw, new_raw = snapshot(a, f), snapshot(b, f)
            assert state(old_arm, old_raw) == state(arm, new_raw)
            assert models(old_arm, old_raw) == models(arm, new_raw)
            assert persistent_objects(old_arm, old_raw) == persistent_objects(arm, new_raw)
            states.append({'mode': mode, 'frame': f, 'native_state': state(arm, new_raw),
                'all_active_company_fleet_ships_and_ordinary_actor_town_item_goods_objects_equal': True})
        reports += [str(pa), str(pb)]
    assert holds[0]['arguments'] == ['Athens', 'Armor'] and holds[1]['arguments'] == []
    save(ROOT / 'extra_gameplay_verification.json', {'candidate_sha256': sha(ROM.read_bytes()), 'two_additional_complete_actual_holds': holds,
        'whole_frame_YesNo_menu_and_Town_returns': controls, 'all_sampled_native_state_and_object_pairs': states,
        'capture_reports': reports, 'natural_paid_drink_and_declined_another_cup_branches': True,
        'no_savestate_RAM_fixture_or_original_save_mutation': True, 'producer_sha256': sha(Path(__file__).read_bytes()),
        'no_full_route_all_gift_or_actual_coordinate_activation_claim': True, 'full_goal_complete': False})
    print(f'Two more actual paragraphs826/850,seven complete UI/return frames and{len(states)} source-state pairs pass.', flush=True)


if __name__ == '__main__': main()
