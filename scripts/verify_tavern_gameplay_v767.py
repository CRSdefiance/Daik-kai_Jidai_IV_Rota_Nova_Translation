"""Actual complete Tavern glyphs,normal scene returns,models and New Game frames."""

import re
import struct
from pathlib import Path

from PIL import Image, ImageChops
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.probe_tavern_conversations_v764 import format_case
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_market_gameplay_v753 import snapshot, state
from scripts.verify_port_gameplay_v762 import capture, cstring
from scripts.verify_shipyard_gameplay_v760 import models, independent_font
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_release_v767')
ROM = Path('out/all_routes_combined_v767_candidate.nds')
BODY = (16, 294, 244, 366)
ADVANCE = (224, 360, 240, 376)


def persistent_objects(arm, raw):
    u = machine(arm); u.mem_write(BASE, raw)
    result = {}
    for label, fn, length in (('all207_actors_and_current_captain', 0xCB184, 0x1A04),
            ('all90_towns', 0xCB178, 4 + 90 * 108), ('all218_items', 0xCB190, 4 + 218 * 20),
            ('all124_goods_and_reserved_slot', 0xCB124, 4 + 125 * 16)):
        call(u, fn, ()); at = u.reg_read(UC_ARM_REG_R0)
        assert BASE <= at < BASE + len(raw) - length
        result[label] = {'address': at, 'bytes': length, 'sha256': sha(bytes(u.mem_read(at, length)))}
    return result


def main():
    pa, before_report, old_arm, before = capture('tavern_editorial_v767_final_v762')
    pb, after_report, arm, after = capture('tavern_editorial_v767_final_v767')
    assert before_report['frames'] == after_report['frames'] == 9201
    assert before_report['scripted_input_schedule'] == after_report['scripted_input_schedule']
    assert before_report['core_options'] == after_report['core_options'] and set(before) == set(after)
    assert after_report['ROM_sha256'] == sha(ROM.read_bytes())
    rom = NdsImage.open(ROM); common = rom.read_file('/COMMON/MESFILE.DK4')
    entries = common_message_entries(common, arm, clean=False); blocks = IlnkContainer.parse(common).blocks
    doc = {r['message_id']: r for r in read('translations/tavern_conversations_editorial_manuscript_v4.json')['records']}
    ptr, wrapped_ptr, owner = [struct.unpack_from('<I', arm, off)[0] for off in (0x5444C, 0x54450, 0x552A0)]
    selected = {5000: 821, 5200: 821, 7000: 827, 7200: 827, 8200: 823, 8400: 823}
    scenes, controls, animation_controls = [], [], []
    indicator_frames = {f: Image.open(before[f]['path']).convert('RGB').crop(ADVANCE).tobytes() for f in selected}
    for frame, capture_row in after.items():
        x, y = [Image.open(rows[frame]['path']).convert('RGB') for rows in (before, after)]
        diff = ImageChops.difference(x, y)
        if frame not in selected:
            if diff.getbbox() is None:
                controls.append(frame)
            else:
                phase = [f for f, pixels in indicator_frames.items() if pixels == y.crop(ADVANCE).tobytes()]
                assert phase, (frame, 'unrecognized original advance-icon animation')
                diff.paste((0, 0, 0), ADVANCE)
                assert diff.getbbox() is None, (frame, diff.getbbox())
                animation_controls.append({'frame': frame, 'all_other_pixels_including_unselected_text_exact': True,
                    'advance_icon_pixel_identical_to_original_frames': phase})
            continue
        number = selected[frame]; raw = snapshot(after_report, frame); template = entries[number].text
        assert cstring(raw, owner + 0x2030) == template
        assert raw.count(blocks[entries[number].block]) == 1
        printf = cstring(raw, ptr)
        match = re.fullmatch(b'(.*?)'.join(re.escape(p) for p in template.split(b'%s')), printf)
        assert match, (frame, number, printf)
        args = match.groups(); u = machine(arm); u.mem_write(BASE, raw)
        native = format_case(u, doc[number], args)
        assert not native['findings'] and bytes.fromhex(native['formatted_hex']) == cstring(raw, wrapped_ptr)
        plane = raster(arm, bytes.fromhex(native['formatted_hex']), 0x01FFCE40 - BASE, size=(228, 64), instruction_limit=1000000)
        assert plane == independent_font(arm, rom.read_file('/GRP/KANJI.FNT'), native['lines'])
        expected = {(16 + i % 228, 296 + i // 228) for i, value in enumerate(plane) if value == 1}
        actual = {(i, j) for j in range(BODY[1], BODY[3]) for i in range(BODY[0], BODY[2]) if y.getpixel((i, j)) == (0, 8, 0)}
        assert actual == expected, (frame, number, len(actual - expected), len(expected - actual))
        previous = {(i, j) for j in range(BODY[1], BODY[3]) for i in range(BODY[0], BODY[2]) if x.getpixel((i, j)) == (0, 8, 0)}
        shadows = {(i + 1, j + 1) for i, j in actual | previous}
        indicator_matches = [f for f, pixels in indicator_frames.items() if pixels == y.crop(ADVANCE).tobytes()]
        assert indicator_matches, (frame, 'unrecognized advance-icon phase')
        unexpected = [(i, j, x.getpixel((i, j)), y.getpixel((i, j))) for j in range(BODY[1], BODY[3]) for i in range(BODY[0], BODY[2]) if not (ADVANCE[0] <= i < ADVANCE[2] and ADVANCE[1] <= j < ADVANCE[3]) and (i, j) not in actual | previous | shadows and x.getpixel((i, j)) != y.getpixel((i, j))]
        assert not unexpected, (frame, number, len(unexpected), unexpected[:10])
        diff.paste((0, 0, 0), BODY); diff.paste((0, 0, 0), ADVANCE); assert diff.getbbox() is None
        scenes.append({'frame': frame, 'message_id': number, 'arguments': [v.decode('ascii') for v in args],
            'lines': native['lines'], 'capture': capture_row,
            'complete_independent_font_foreground_and_blank_paper_cells_exact': True,
            'whole_resident_template_block_and_all_pixels_outside_body_and_advance_icon_exact': True,
            'advance_icon_phase_pixel_identical_to_original_frames': indicator_matches})
    states = []
    for frame in after_report['exact_requested_capture_frames']:
        raw_a, raw_b = snapshot(before_report, frame), snapshot(after_report, frame)
        assert state(old_arm, raw_a) == state(arm, raw_b), (frame, 'native state')
        assert models(old_arm, raw_a) == models(arm, raw_b), (frame, 'company/fleet/ship models')
        objects_a, objects_b = persistent_objects(old_arm, raw_a), persistent_objects(arm, raw_b)
        assert objects_a == objects_b, (frame, 'persistent actor/town/item/goods objects')
        states.append({'frame': frame, 'native_state': state(arm, raw_b), 'active_models': models(arm, raw_b),
                       'persistent_actor_town_item_goods_objects_equal': objects_b})
    pna, a, _, start_before = capture('port_services_v762_newgame_762')
    pnb, b, _, start_after = capture('tavern_editorial_v767_newgame_v767')
    assert a['scripted_input_schedule'] == b['scripted_input_schedule'] and not b.get('battery_save_preloaded')
    assert set(start_before) == set(start_after) == {1, 60, 180, 1600, 2000, 3200, 4000}
    assert all(Path(start_before[f]['path']).read_bytes() == Path(start_after[f]['path']).read_bytes() for f in start_after)
    assert {r['message_id'] for r in scenes} == {821, 823, 827}
    assert {r['frame'] for r in scenes} == set(selected)
    tested = set(controls) | {r['frame'] for r in animation_controls}
    assert {7600, 8600, 9000, 9200} <= tested
    save(ROOT / 'gameplay_verification.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'six_complete_actual_holds': scenes, 'all_other_whole_screen_controls': controls,
        'unselected_captions_exact_except_verified_original_advance_icon_animation': animation_controls,
        'all_sampled_original_native_state_and_persistent_object_pairs': states,
        'New_Game7_unique_frames_byte_identical': sorted(start_after),
        'normal_toast_Tavern_menu_return_and_rumor_to_barmaid_transition': [7600, 8600, 9000, 9200],
        'capture_reports': [str(p) for p in (pa, pb, pna, pnb)],
        '28_other_IDs_have_source_native_font_coverage_with_family_gameplay_sampling': True,
        'no_savestate_RAM_fixture_or_original_save_changes': True,
        'no_full_route_hardware_all_gift_or_coordinate_event_activation_claim': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'Six actual whole-glyph holds,three IDs,{len(controls)} whole-screen controls,10 native object/state pairs and7 New Game frames pass.', flush=True)


if __name__ == '__main__': main()
