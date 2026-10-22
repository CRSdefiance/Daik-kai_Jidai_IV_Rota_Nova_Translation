"""Paired native distribution captures with the disclosed three-byte role fixture."""

from pathlib import Path

from PIL import Image, ImageChops
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_missionary_fixture_v746 import assign
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_tavern_queued_native_v626 import queued_wrap
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/giveaway_editorial_v746')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def captures(folder, frames, fixture):
    report = read(CAP / folder / 'capture_report.json')
    assert report['frames'] == frames and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors']
    assert not report['hardware_device_verification']
    assert report['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert sha(Path(report['ROM']).read_bytes()) == report['ROM_sha256']
    fixtures = report.get('synthetic_missionary_Chapel_assignment_fixtures', [])
    assert len(fixtures) == int(fixture)
    assert not any(value for key, value in report.items()
                   if key.startswith('synthetic_') and key != 'synthetic_missionary_Chapel_assignment_fixtures')
    rows = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        rows[row['frame']] = row
    for row in report.get('read_only_capture_RAM_snapshots', []):
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
    if fixture:
        donor = report['battery_save_preloaded']
        assert donor['source_sha256'] == 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
        assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
        assert donor['copied_byte_exact_before_cold_boot']
        arm = NdsImage.open(report['ROM']).read_file('/__arm9__.bin')
        raw = snapshot(report, 3200)
        after, receipt = assign(arm, raw, True)
        recorded = {k: v for k, v in fixtures[0].items() if k != 'frame'}
        assert fixtures[0]['frame'] == 3200 and receipt == recorded
        changed = [BASE + i for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b]
        assert changed == sorted(r['address'] for r in receipt['changes'])
        assert cargo(arm, raw) == 2 and cargo(arm, after) == 2
        final = report['read_only_RAM_snapshot']
        final_bytes = Path(final['path']).read_bytes()
        assert sha(final_bytes) == final['sha256'] and cargo(arm, final_bytes) == 0
    else:
        assert not report.get('battery_save_preloaded')
    return report, rows


def snapshot(report, frame):
    row = next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame'] == frame)
    raw = Path(row['path']).read_bytes()
    assert len(raw) == 4194304 and sha(raw) == row['sha256']
    return raw


def cargo(arm, raw):
    cpu = machine(arm)
    cpu.mem_write(BASE, raw)
    call(cpu, 0xCB1A8, ())
    root = cpu.reg_read(UC_ARM_REG_R0)
    call(cpu, 0x36180, (root + 4 + 0x84, 0x02440000))
    return cpu.reg_read(UC_ARM_REG_R0)


def main():
    baseline, before = captures('giveaway_v746_baseline', 8001, True)
    report, after = captures('giveaway_v746_new', 8001, True)
    assert report['scripted_input_schedule'] == baseline['scripted_input_schedule']
    assert report['core_options'] == baseline['core_options']
    assert report['battery_save_preloaded']['source'] == baseline['battery_save_preloaded']['source']
    assert set(before) == set(after)
    fixtures = report['synthetic_missionary_Chapel_assignment_fixtures']
    assert fixtures[0]['changes'] == baseline['synthetic_missionary_Chapel_assignment_fixtures'][0]['changes']
    rom = NdsImage.open(report['ROM'])
    arm, common = rom.read_file('/__arm9__.bin'), rom.read_file('/COMMON/MESFILE.DK4')
    font = GameAsciiFont.from_arm9(arm)
    block = IlnkContainer.parse(common).blocks[8]
    entries = common_message_entries(common, arm, clean=False)
    # The inherited queued portrait wrapper normalizes stored LF/guards and wraps
    # again after expansion. Verify that actual consumer, not just stored breaks.
    layouts, runtime_checks = {}, []
    for i in range(659, 675):
        if i == 674:
            continue  # Customer674 uses its separate direct portrait path.
        parent, table = (0x02053D24, 0x021184C0) if i < 666 else (0x02053DB8, 0x021184A0)
        text = entries[i].text.rstrip(b' ')
        formatted = queued_wrap(arm, text, parent, table)
        assert b' '.join(formatted.split()) == b' '.join(text.split())
        lines = [line.strip().decode('ascii') for line in formatted.split(b'\n')]
        assert len(lines) <= 4 and all(len(line) <= 35 for line in lines)
        plane = raster(arm, formatted, 0x01FFCE40 - BASE, size=(228, 64), instruction_limit=1000000)
        expected = bytearray(228 * 64)
        for row, line in enumerate(lines):
            for n, char in enumerate(line):
                glyph = font.decode(char)
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x, y)):
                            expected[(16 * row + y) * 228 + 6 + n * 6 + x] = 1
        assert plane == bytes(expected), i
        preview = ROOT / f'native_runtime_message_{i}.png'
        Image.frombytes('L', (228, 64), bytes(0 if p else 255 for p in plane)).save(preview)
        layouts[i] = lines
        runtime_checks.append({'message_id': i, 'parent': parent, 'table': table,
                               'formatted_hex': formatted.hex(), 'lines': lines,
                               'complete_post_wrapper228x64_font_plane_exact': True,
                               'all_words_and_letters_preserved': True, 'preview': str(preview)})
    layouts[674] = [line.strip().decode('ascii') for line in entries[674].text.rstrip(b' ').split(b'\n')]
    selected = {4800: 665, 5200: 665, 6800: 673, 7200: 674}
    checks, equal = [], []
    for frame in sorted(after):
        old = Image.open(before[frame]['path']).convert('RGB')
        new = Image.open(after[frame]['path']).convert('RGB')
        difference = ImageChops.difference(old, new)
        if frame not in (4800, 5200):
            assert difference.getbbox() is None, frame
            equal.append(frame)
        if frame not in selected:
            continue
        i = selected[frame]
        expected = set()
        for nline, line in enumerate(layouts[i]):
            for n, char in enumerate(line):
                glyph = font.decode(char)
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x, y)):
                            expected.add((22 + n * 6 + x, 296 + nline * 16 + y))
        # Two complete rows and surrounding blank paper; choice buttons begin below this area.
        body = (16, 294, 240, 344)
        actual = {(x, y) for y in range(body[1], body[3]) for x in range(body[0], body[2])
                  if new.getpixel((x, y)) == (0, 8, 0)}
        assert actual == expected, (frame, len(expected - actual), len(actual - expected))
        outside = difference.copy()
        outside.paste((0, 0, 0), body)
        assert outside.getbbox() is None
        ram = snapshot(report, frame)
        position = ram.find(block)
        assert position >= 0 and ram.find(block, position + 1) == -1
        cpu = machine(arm)
        cpu.mem_write(BASE, ram)
        call(cpu, 0x7E988, (fixtures[0]['actor'],))
        assert cpu.reg_read(UC_ARM_REG_R0) == 7
        checks.append({'frame': frame, 'message_id': i, 'lines': layouts[i],
                       'all_glyph_and_blank_paper_cells_exact': True, 'ink_pixels': len(actual),
                       'paper_bounds': body, 'choice_buttons_and_all_other_pixels_equal_baseline': True,
                       'whole_resident_block8_exact': True, 'resident_address': BASE + position,
                       'native_actor_style': 7, 'capture': after[frame]})
    assert len(equal) == 15 and {5600, 6000, 6400, 7200, 7600, 8000, 8001} <= set(equal)
    game, game_rows = captures('giveaway_v746_newgame', 4000, False)
    old_game, old_rows = captures('shop_business_v745_newgame', 4000, False)
    assert game['scripted_input_schedule'] == old_game['scripted_input_schedule']
    same = sorted(old_rows.keys() & game_rows.keys())
    assert same == [1, 60, 180, 1200, 2400, 3200, 4000]
    for frame in same:
        assert Image.open(old_rows[frame]['path']).convert('RGB').tobytes() == Image.open(game_rows[frame]['path']).convert('RGB').tobytes()
    save(ROOT / 'gameplay_verification.json', {
        'candidate': report['ROM'], 'candidate_sha256': report['ROM_sha256'],
        'two_terminal8001_frame_distribution_cold_boots': True,
        'fixture_native_message_displays': checks, 'whole_two_screen_equal_baseline_frames': equal,
        'all15_unique_confirm_and_announcement_entries_post_runtime_wrapper_native_planes': runtime_checks,
        'stored_LF_reflowed_by_inherited_queued_portrait_wrapper_not_rendered_verbatim': True,
        'disclosed_three_byte_Chapel_and_Manuel_assignment_only_at3200': fixtures,
        'fixture_reproduced_from_original_RAM_and_exact_receipt': True,
        'actual_native_actor_style7_binds_confirm665_and_announcement673': True,
        'following_direct_customer_reaction674_complete': True,
        'original_native_cargo_count2_before_and0_after_distribution': True,
        'distribution_choice_buttons_and_final_Square_return_exact_baseline': True,
        'no_savestate_or_other_gameplay_fixture': True, 'original_donor_save_unchanged': True,
        'earned_qualifications_refit_assignment_or_goods_acquisition_verified': False,
        'all_other_voice_slots_verified_by_original_native_selector_and_complete_font_component_only': True,
        'New_Game_terminal4000_frame_cold_boot_without_fixture_or_save': True,
        'New_Game7_whole_frame_pairs_exact': same,
        'reports': {str(CAP / name / 'capture_report.json'): sha((CAP / name / 'capture_report.json').read_bytes())
                    for name in ('giveaway_v746_baseline', 'giveaway_v746_new', 'giveaway_v746_newgame')},
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False,
    })
    print('V746 complete fixture 665/673; 15 unchanged distribution and 7 New Game whole-frame pairs.', flush=True)


if __name__ == '__main__':
    main()
