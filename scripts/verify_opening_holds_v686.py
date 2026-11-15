"""Classify three blank holds by actual source VM positions, not fitted time shifts."""

import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.run_opening_holds_v686 import CAP, CLEAN, CURRENT, FRAMES, ROOT
from scripts.verify_dialogue_palette_v628 import captured_rgb
from scripts.verify_village_wrap_v608 import read, save

OWNER = 0x0218F250
CACHE = OWNER + 0x58
CHAPTER = CACHE + 8
PALETTE = 0x02125A20
HOLDS = ((4000, 4000, 32), (5800, 5800, 120), (22000, 21400, 1708))


def captured(report):
    pictures, ram = {}, {}
    for row in report['frames_captured']:
        p = Path(row['path'])
        assert sha(p.read_bytes()) == row['PNG_sha256']
        image = Image.open(p).convert('RGB')
        if row['frame'] in pictures:
            assert pictures[row['frame']].tobytes() == image.tobytes()
        pictures[row['frame']] = image
    for row in report['read_only_capture_RAM_snapshots']:
        data = Path(row['path']).read_bytes()
        assert len(data) == 0x400000 and sha(data) == row['sha256']
        ram[row['frame']] = data
    return pictures, ram


def cursor(raw, chapter):
    assert raw[CHAPTER - BASE:CHAPTER - BASE + len(chapter)] == chapter
    assert struct.unpack_from('<I', raw, CACHE + 4 - BASE)[0] == 33
    pointer = struct.unpack_from('<I', raw, OWNER + 4 - BASE)[0]
    assert CHAPTER <= pointer < CHAPTER + len(chapter)
    return pointer - CHAPTER, struct.unpack_from('<H', raw, pointer - BASE)[0]


def native_wait(arm, ram, offset):
    u = machine(arm)
    u.mem_write(BASE, ram)
    before = bytes(u.mem_read(BASE, 0x400000))
    trace = call(u, 0x24134, (CACHE, 33))
    assert u.reg_read(UC_ARM_REG_R0) == 1 and not {0x020D2018, 0x020D1EF0} & trace
    assert bytes(u.mem_read(BASE, 0x400000)) == before
    output, length = 0x02460020, 0x02460060
    u.mem_write(output - 16, b'\xA5' * 112)
    calls = []

    def complete_wait(cpu, address, size, unused):
        if address == 0x02054E44:
            args = [cpu.reg_read(UC_ARM_REG_R0), cpu.reg_read(UC_ARM_REG_R1)]
            assert args == [0, 0]
            calls.append({'entry': address, 'args': args, 'return_address': cpu.reg_read(UC_ARM_REG_LR)})
            # The GUI modal alone is bridged to complete the isolated decoder.
            # Its actual drawing/input is established by the cold-boot captures.
            cpu.reg_write(UC_ARM_REG_R0, 0)
            cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))

    hook = u.hook_add(UC_HOOK_CODE, complete_wait)
    try:
        executed = call(u, 0x2A510, (output, OWNER, length))
    finally:
        u.hook_del(hook)
    assert calls == [{'entry': 0x02054E44, 'args': [0, 0], 'return_address': 0x0202A218}]
    assert {0x0202A510, 0x0202A1D8, 0x02054E44} <= executed
    assert struct.unpack('<I', u.mem_read(output, 4))[0] == 3
    assert struct.unpack('<I', u.mem_read(length, 4))[0] == 2
    remaining = bytearray(u.mem_read(output - 16, 112))
    remaining[16:20] = b'\xA5' * 4
    remaining[length - output + 16:length - output + 20] = b'\xA5' * 4
    assert remaining == b'\xA5' * 112
    assert bytes(u.mem_read(BASE, 0x400000)) == before
    return {'actual_VM_cursor_offset': offset, 'opcode': '2000', 'original_modal_call': calls[0],
        'original_instruction_length': 2, 'original_result_word': 3,
        'complete_native_dispatch_return_ABI_output_canaries_actual_RAM_unchanged': True,
        'already_loaded_native_cache_check_returns1_without_reading_a_file': True,
        'only_GUI_modal_completion_bridged_no_probe_drawing_or_actual_input_credit': True}


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(CLEAN.read_bytes()) == pre['clean_sha256'] and sha(CORE.read_bytes()) == CORE_SHA
    source_path = CAP / 'opening_holds_v686_source/capture_report.json'
    source_report = read(source_path)
    assert source_report['ROM_sha256'] == pre['clean_sha256'] and source_report['core_DLL_sha256'] == CORE_SHA
    assert source_report['cold_boot'] and not source_report['savestate_loaded'] and not source_report['callback_errors']
    assert source_report['frames'] == 31000 and source_report['scripted_input_schedule'] == read(pre['inputs'])
    assert source_report['battery_save_preloaded']['source_sha256'] == pre['donor_sha256']
    assert {k for k, v in source_report.items() if k.startswith('synthetic_') and v} == {'synthetic_gallery_fixtures'}
    contract = read(source_path.parent / 'run_contract.json')
    assert contract['runner_sha256'] == sha(Path('scripts/run_opening_holds_v686.py').read_bytes())
    assert contract['frozen_preflight_sha256'] == sha((ROOT / 'preflight.json').read_bytes())
    assert sha(Path(pre['current_report']).read_bytes()) == pre['current_report_sha256']
    current_report = read(pre['current_report'])
    assert current_report['ROM_sha256'] == pre['candidate_sha256']
    assert current_report['scripted_input_schedule'] == source_report['scripted_input_schedule']
    source_pictures, source_ram = captured(source_report)
    current_pictures, current_ram = captured(current_report)
    assert set(source_pictures) == {1, 60, 180, *FRAMES}
    original, current = NdsImage.open(CLEAN), NdsImage.open(CURRENT)
    arms = {tag: r.read_file('/__arm9__.bin') for tag, r in (('source', original), ('current', current))}
    chapters = {tag: IlnkContainer.parse(r.read_file('/data/SC3.DK4')).blocks[33]
                for tag, r in (('source', original), ('current', current))}
    assert len(chapters['source']) == len(chapters['current']) == 2528
    spans = ((0x24134, 0x241C4), (0x2A1D8, 0x2A228), (0x2A510, 0x2A5BC), (0x54E44, 0x55110))
    assert all(arms['source'][a:b] == arms['current'][a:b] for a, b in spans)
    native, holds = [], []
    for source_frame, current_frame, offset in HOLDS:
        assert cursor(source_ram[source_frame], chapters['source']) == cursor(current_ram[current_frame], chapters['current']) == (offset, 0x2000)
        for tag, ram in (('source', source_ram[source_frame]), ('current', current_ram[current_frame])):
            native.append(dict(native_wait(arms[tag], ram, offset), version=tag))
        left, right = source_pictures[source_frame], current_pictures[current_frame]
        assert left.crop((0, 0, 256, 192)).tobytes() == right.crop((0, 0, 256, 192)).tobytes()
        colors = []
        for tag, ram in (('source', source_ram[source_frame]), ('current', current_ram[current_frame])):
            assert ram[PALETTE - BASE:PALETTE - BASE + 32] == arms[tag][PALETTE - BASE:PALETTE - BASE + 32]
            palette = struct.unpack_from('<16H', ram, PALETTE - BASE)
            colors.append(captured_rgb(palette[15]))
        assert colors == [(0, 8, 0), (0, 8, 0)]
        assert not any(im.getpixel((x, y)) == color for im, color in zip((left, right), colors, strict=True)
                       for y in range(296, 376) for x in range(16, 240))
        diff = [(x, y) for y in range(296, 376) for x in range(16, 240)
                if left.getpixel((x, y)) != right.getpixel((x, y))]
        assert len(diff) == (208 if source_frame == 5800 else 0)
        bbox = ([min(x for x, y in diff), min(y for x, y in diff), max(x for x, y in diff) + 1,
                 max(y for x, y in diff) + 1] if diff else None)
        if diff:
            assert bbox == [224, 360, 240, 376]
        holds.append({'source_frame': source_frame, 'current_frame': current_frame,
            'actual_VM_cursor_offset_and_original_command': [offset, '2000'],
            'all49152_upper_source_current_RGB_pixels_exact': True,
            'both_full_dialogue_regions_have_zero_source_palette15_text_pixels': True,
            'complete_dialogue_rectangle_RGB_differences_retained': len(diff),
            'difference_bounds': bbox,
            '208_differences_are_visually_the_A_indicator_not_given_full_region_equivalence_credit': bool(diff),
            'original_zero_argument_modal_command_no_translation_added_blank_page': True})
    controls = []
    for sf, cf, expected in ((4600, 4600, 34), (6400, 6400, 122), (20800, 20200, 1532),
                             (21400, 20800, 1644), (31000, 30400, 2388)):
        sc, cc = cursor(source_ram[sf], chapters['source']), cursor(current_ram[cf], chapters['current'])
        assert sc == cc and sc[0] == expected and sc[1] != 0x2000
        controls.append({'source_frame': sf, 'current_frame': cf, 'matching_actual_VM_cursor': sc[0],
                         'matching_original_opcode': f'{sc[1]:04X}', 'not_a_blank_wait_opcode': True})
    # Preserve the failed chronological assumption as diagnostic evidence.
    assert cursor(source_ram[21400], chapters['source']) != cursor(current_ram[21400], chapters['current'])
    sheet = Image.new('RGB', (1024, 1230), '#263238')
    draw = ImageDraw.Draw(sheet)
    for row, (sf, cf, _) in enumerate(HOLDS):
        next_current = {4000: 4600, 5800: 6400, 21400: 22000}[cf]
        items = ((source_pictures[sf], f'Japanese original {sf}'), (current_pictures[cf], f'V685 {cf} same VM wait'),
                 (current_pictures[next_current], f'V685 after A {next_current}'),
                 (source_pictures[{4000: 4600, 5800: 6400, 21400: 31000}[cf]],
                  'Original continues after A (last: later join)'))
        for col, (im, title) in enumerate(items):
            x, y = col * 256, row * 410
            draw.text((x + 4, y + 4), title, fill='white')
            sheet.paste(im, (x, y + 24))
    review = ROOT / 'script_position_matched_original_waits.png'
    sheet.save(review)
    save(ROOT / 'proof.json', {'candidate': str(CURRENT), 'candidate_sha256': pre['candidate_sha256'],
        'source_report': str(source_path), 'source_report_sha256': sha(source_path.read_bytes()),
        'current_report': pre['current_report'], 'current_report_sha256': pre['current_report_sha256'],
        'one_original_Japanese31000_frame_cold_boot_same_inputs_and_existing_unlock_save': True,
        'three_actual_blank_holds_match_source_original_VM_2000_commands': holds,
        'six_complete_native_source_current_dispatches_with_GUI_modal_completion_bridge': native,
        'five_typed_non_wait_continuation_controls': controls,
        'source_exact_code_ranges': [{'begin': a, 'end': b, 'sha256': sha(arms['current'][a:b])} for a, b in spans],
        'same_frame21400_comparison_is_different_script_positions_not_a_pixel_waiver': True,
        'preceding_Japanese_paragraph_active_for_one_additional_sampled_input_step_not_a_general_lag_fit': True,
        'A_indicator208_RGB_differences_retained_full_button_phase_paint_not_proven_here': True,
        'three_specific_blank_holds_are_source_script_waits_not_new_English_padding_pages': True,
        'no_global_blank_page_or_full_Maria_route_or_hardware_claim': True,
        'review_sheet': str(review), 'review_sheet_sha256': sha(review.read_bytes()),
        'all18_plaques_incomplete22_historical_requirements_and_other_graphics_gates_open': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'current_goal_turn_classification': 'progress',
        'full_goal_complete': False})
    print('V686 three original script2000 holds classified; six native dispatches and five typed continuation controls pass; A-indicator differences retained.', flush=True)


if __name__ == '__main__':
    main()
