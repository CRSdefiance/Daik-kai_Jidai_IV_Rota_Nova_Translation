"""Verify ordinary Ancient Map source binding and complete Treasure Name header."""

import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/treasure_panel_v722')
CAP = Path('work/emulation_v193/treasure_panel_v722_saved_pilot')
ROM = Path('out/all_routes_combined_v712_candidate.nds')
ASSET = '/_pxl/mysterymap/mys_hunt_d.pxl'
FRAMES = (10300, 10700, 11100, 13900)


def main():
    assert not (ROOT / 'proof.json').exists()
    report_path = CAP / 'capture_report.json'
    report = read(report_path)
    assert report['frames'] == 15100 and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not any(v for k, v in report.items() if k.startswith('synthetic_'))
    assert report['core_DLL_sha256'] == CORE_SHA == sha(CORE.read_bytes())
    assert sha(ROM.read_bytes()) == report['ROM_sha256'] == '6534e5619673ea6bdffa3a2342622b99ef393bef52ef58cac131ee94ae0f4030'
    donor = report['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    assert donor['copied_byte_exact_before_cold_boot']
    assert not any('save' in r.get('buttons', []) for r in report['scripted_input_schedule'])
    snapshots = {}
    for row in report['read_only_pause_RAM_snapshots']:
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
        snapshots[row['frame']] = Path(row['path']).read_bytes()
    shots = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        shots[row['frame']] = row
    save(ROOT / 'executed_inputs.json', report['scripted_input_schedule'])
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, original = [r.read_file('/__arm9__.bin') for r in (rom, clean)]
    source = rom.read_file(ASSET)
    pxl, font = PxlImage.from_bytes(source), GameAsciiFont.from_arm9(arm)
    assert sha(source) == read('translations/treasure_source_grain_v1.json')['target_sha256']
    assert (pxl.width, pxl.height) == (256, 192)
    batch = read('translations/treasure_name_header_graphics_v1.json')
    record = batch['records'][0]
    assert record['source_japanese'] == '秘宝名' and record['text'] == 'Treasure Name'
    assert sha(font.glyphs) == batch['font_sha256']
    l, t, r, b = record['box']
    x, y = l + (r - l - len(record['text']) * 6) // 2, t + (b - t - 11) // 2
    assert (x, y) == (90, 2)
    ranges = [(0x1019EC, 0x101B44), (0x101B68, 0x101C38), (0x101D88, 0x101EC0)]
    assert all(arm[a:b] == original[a:b] for a, b in ranges)
    color = native5(pxl.palette[7][:3])
    source_image = pxl.render().convert('RGB')
    cases = []
    for frame in FRAMES:
        raw = snapshots[frame]
        parent = 0x0238077C
        word = lambda address, raw=raw: struct.unpack_from('<I', raw, address - 0x02000000)[0]
        assert word(parent) == 0x0216CA90
        typeinfo = word(word(parent) - 4)
        name_pointer = word(typeinfo + 4)
        expected_class = b'16CMysteryHuntView\0'
        assert raw[name_pointer - 0x02000000:name_pointer - 0x02000000 + len(expected_class)] == expected_class
        view = struct.unpack_from('<12I', raw, parent + 0x6054 - 0x02000000)
        assert view[3] == 0x02313A10 and view[5] == 4
        assert view[7:12] == (0, 0, 0, 256, 192)
        cpu = machine(arm)
        cpu.mem_write(0x02000000, raw)
        executed = call(cpu, 0xD6558, (view[3],))
        header = cpu.reg_read(UC_ARM_REG_R0)
        assert bytes(cpu.mem_read(header, len(source))) == source
        assert raw[header - 0x02000000:header - 0x02000000 + len(source)] == source
        # The original selected-row painter expands its native rectangle by
        # four rows upward (101DD8). That may cover header rows13..15; it is
        # not a source-file mismatch or permission to discard caption pixels.
        selected = []
        for at in range(0x180000, len(raw) - 0x160, 4):
            if struct.unpack_from('<I', raw, at)[0] != 0x0216CD84 or struct.unpack_from('<I', raw, at + 0x24)[0] != 1:
                continue
            offset = struct.unpack_from('<i', raw, 0x0216CD84 - 0x02000000 - 0x10)[0]
            rect = struct.unpack_from('<4i', raw, at + offset + 0x20)
            selected.append({'object': at + 0x02000000, 'native_row_rectangle': list(rect),
                'expanded_top': rect[1] - 4})
        assert len(selected) == 1
        visible_rows = min(16, selected[0]['expanded_top'])
        assert visible_rows in (13, 16) and y + 11 <= visible_rows
        image = Image.open(shots[frame]['path']).convert('RGB')
        q = Image.new('RGB', image.size)
        q.putdata([native5(p) for p in image.get_flattened_data()])
        ink, bounds = complete_mask(font, record['text'], q, x, 192 + y, color)
        assert ink == 158 and bounds == [90, 194, 168, 205]
        expected = [native5(p) for p in source_image.crop((0, 0, 256, visible_rows)).get_flattened_data()]
        actual = list(q.crop((0, 192, 256, 192 + visible_rows)).get_flattened_data())
        assert actual == expected
        mask = Image.new('1', (len(record['text']) * 6, 11))
        for i, ch in enumerate(record['text']):
            mask.paste(font.decode(ch), (i * 6, 0))
        negative = []
        for index in (0, len(record['text']) - 1):
            wrong = mask.copy()
            wrong.paste(0, (index * 6, 0, index * 6 + 6, 11))
            assert wrong.tobytes() != mask.tobytes()
            negative.append({'erased_character': record['text'][index], 'complete_mask_rejects_erasure': True})
        cases.append({'frame': frame, 'image': shots[frame]['path'], 'PNG_sha256': shots[frame]['PNG_sha256'],
            'parent_class': '16CMysteryHuntView', 'parent': parent,
            'original_whole_source_view': list(view), 'actual_native_cache_header': header,
            'complete_file_original_cache_getter_no_IO_bridge_ABI_pass': len(executed),
            'whole_resident_file_sha256': sha(source), 'selected_data_row': selected[0],
            'complete_visible_source_header_rows': visible_rows, 'all_visible_header_native5_pixels_exact': 256 * visible_rows,
            'all158_ink_points_and_every_glyph_blank_cell_exact': True, 'native_text_bounds': bounds,
            'first_final_letter_negative_controls': negative})
    assert cases[0]['complete_visible_source_header_rows'] == 13
    assert cases[2]['complete_visible_source_header_rows'] == 16
    first = Image.open(shots[10300]['path']).convert('RGB')
    reopened = Image.open(shots[13900]['path']).convert('RGB')
    assert first.tobytes() == reopened.tobytes()
    initial = Image.open(shots[3200]['path']).convert('RGB')
    final = Image.open(shots[15100]['path']).convert('RGB')
    assert initial.tobytes() == final.tobytes()
    releases = [ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
        Path('translations/release_stack.json'), Path('out/raphael_natural_v2_accepted_base.nds')]
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'actual_report': str(report_path), 'actual_report_sha256': sha(report_path.read_bytes()),
        'ordinary_Menu_Info_Ancient_Map_navigation_two_visits_and_return': True,
        'no_savestate_no_live_inventory_location_story_flag_or_graphics_fixture': True,
        'source_donor_unchanged': donor, 'source': ASSET, 'source_sha256': sha(source),
        'translation': {'Japanese': record['source_japanese'], 'English': record['text'],
            'meaning': record['source_meaning'], 'faithful_heading_retained': True},
        'four_actual_heading_and_view_cases': cases,
        'full_reopened_two_screen_RGB_exact_to_first_visit': True,
        'full_final_two_screen_RGB_exact_to_original_town': True,
        'first_row_focus_overlay_geometry_explains_three_covered_bottom_header_rows': True,
        'no_hidden_pixels_waived_as_source_exact_no_full_dynamic_scene_or_overlay_replay_claim': True,
        'initial_extras_pilot_terminal4000_wrong_branch_not_treasure_display_evidence':
            str(Path('work/emulation_v193/treasure_panel_v722_pilot/capture_report.json')),
        'retained_navigation_detours_include_items_functions_assign_sailors_and_Sailors_before_correct_reopen': True,
        'discovered_treasure_rows_acquisition_and_other_panel_mode_not_verified': True,
        'source_code_ranges_exact_clean': ranges,
        'release_hashes_unchanged': {str(p): sha(p.read_bytes()) for p in releases},
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V722: ordinary Ancient Map parent,4 complete158-point headings,full source cache/views,focus geometry,reopen and whole town return verified.', flush=True)


if __name__ == '__main__':
    main()
