"""Actual paired Square introduction/cooking screens and New Game regression."""

from pathlib import Path

from PIL import Image, ImageChops

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_product_promotion_fixture_v747 import assign
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.probe_button_prompt_native import BASE, machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/product_pitches_v747')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def snapshot(report, frame):
    row = next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame'] == frame)
    raw = Path(row['path']).read_bytes()
    assert len(raw) == 4194304 and sha(raw) == row['sha256']
    return raw


def captures(folder, frames, fixture):
    report = read(CAP / folder / 'capture_report.json')
    assert report['frames'] == frames and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report['hardware_device_verification']
    assert report['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert sha(Path(report['ROM']).read_bytes()) == report['ROM_sha256']
    fixtures = report.get('synthetic_product_promotion_event_fixtures', [])
    assert len(fixtures) == int(fixture)
    assert not any(value for key, value in report.items()
                   if key.startswith('synthetic_') and key != 'synthetic_product_promotion_event_fixtures')
    if fixture:
        donor = report['battery_save_preloaded']
        assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256'] == 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
        assert donor['copied_byte_exact_before_cold_boot']
        arm = NdsImage.open(report['ROM']).read_file('/__arm9__.bin')
        raw = snapshot(report, 3200)
        after, receipt = assign(arm, raw, {'product': 14})
        assert fixtures[0]['frame'] == 3200
        assert receipt == {k: v for k, v in fixtures[0].items() if k != 'frame'}
        assert sum(a != b for a, b in zip(raw, after, strict=True)) == 3
        adapter = report['controlled_product_promotion_harness_adapter']
        assert adapter['original_harness_file_unchanged']
        assert adapter['unchanged_original_harness_sha256'] == sha(Path('scripts/headless_desmume_v193.py').read_bytes())
        assert adapter['adapter_sha256'] == sha(Path('scripts/run_product_pitches_capture_v747.py').read_bytes())
    else:
        assert not report.get('battery_save_preloaded')
    rows = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        rows[row['frame']] = row
    return report, rows


def main():
    baseline, before = captures('product_pitches_v747_baseline_final', 6501, True)
    report, after = captures('product_pitches_v747_new', 6501, True)
    assert report['scripted_input_schedule'] == baseline['scripted_input_schedule']
    assert report['core_options'] == baseline['core_options'] and set(before) == set(after)
    assert report['synthetic_product_promotion_event_fixtures'][0]['changes'] == baseline['synthetic_product_promotion_event_fixtures'][0]['changes']
    rom = NdsImage.open(report['ROM'])
    arm, common = rom.read_file('/__arm9__.bin'), rom.read_file('/COMMON/MESFILE.DK4')
    font = GameAsciiFont.from_arm9(arm)
    block = IlnkContainer.parse(common).blocks[8]
    document = read('translations/product_pitches_editorial_manuscript_v1.json')
    paragraphs = {r['message_id']: r['english'].removesuffix('{PAD}') for r in document['records']}
    cpu = machine(arm)
    from ndspy.code import MainCodeFile
    cpu.mem_write(0x02387A20, bytes(MainCodeFile(arm, BASE).sections[3].data[:-48]))
    layouts = {i: native_layout(cpu, b' ' + paragraphs[i].encode('ascii'), i, ('Olive Oil',) if i == 675 else ())[1]
               for i in (675, 676)}
    selected = {3800: 675, 4000: 675, 4200: 676, 4400: 676}
    checks, equal = [], []
    for frame in sorted(after):
        old = Image.open(before[frame]['path']).convert('RGB')
        new = Image.open(after[frame]['path']).convert('RGB')
        diff = ImageChops.difference(old, new)
        if frame not in selected:
            assert diff.getbbox() is None, frame
            equal.append(frame)
            continue
        i = selected[frame]
        expected = set()
        for row, line in enumerate(layouts[i]):
            for n, char in enumerate(line):
                glyph = font.decode(char)
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x, y)):
                            expected.add((22 + n * 6 + x, 296 + row * 16 + y))
        # Original228-pixel text plane: x16..243, including formerly overflowing old676.
        body = (16, 294, 244, 366)
        actual = {(x, y) for y in range(body[1], body[3]) for x in range(body[0], body[2])
                  if new.getpixel((x, y)) == (0, 8, 0)}
        assert expected == actual, (frame, len(expected - actual), len(actual - expected))
        outside = diff.copy()
        outside.paste((0, 0, 0), body)
        assert outside.getbbox() is None, (frame, outside.getbbox())
        ram = snapshot(report, frame)
        position = ram.find(block)
        assert position >= 0 and ram.find(block, position + 1) == -1
        checks.append({'frame': frame, 'message_id': i, 'lines': layouts[i], 'capture': after[frame],
                       'every_glyph_and_blank_paper_cell_exact': True, 'paper_bounds': body,
                       'all_pixels_outside_original_text_plane_equal_baseline': True,
                       'whole_resident_block8_unique_and_exact': True, 'resident_address': BASE + position})
    assert {3400, 3600, 4600, 4800, 5200, 6000, 6500, 6501} <= set(equal)
    game, game_rows = captures('product_pitches_v747_newgame', 4000, False)
    prior, prior_rows = captures('giveaway_v746_newgame', 4000, False)
    assert game['scripted_input_schedule'] == prior['scripted_input_schedule']
    same = sorted(game_rows.keys() & prior_rows.keys())
    assert same == [1, 60, 180, 1200, 2400, 3200, 4000]
    for frame in same:
        assert Image.open(game_rows[frame]['path']).convert('RGB').tobytes() == Image.open(prior_rows[frame]['path']).convert('RGB').tobytes()
    save(ROOT / 'gameplay_verification.json', {
        'candidate': report['ROM'], 'candidate_sha256': report['ROM_sha256'],
        'two_terminal6501_frame_paired_promotion_cold_boots': True,
        'disclosed_three_byte_product_event_and_stock_fixture': report['synthetic_product_promotion_event_fixtures'],
        'actual_original_introduction675_then_cooking676_complete': checks,
        'whole_two_screen_equal_baseline_frames': equal,
        'original_Square_menu_and_town_return_exact_baseline': True,
        'other_five_messages_source_native_full_font_and_exhaustive_substitution_evidence_not_ordinary_events': [677, 678, 679, 680, 681],
        'no_savestate_or_other_gameplay_fixture_and_original_donor_save_unchanged': True,
        'New_Game_terminal4000_frame_fixture_free_cold_boot_and7_whole_frame_pairs': same,
        'hardware_or_full_route_playthrough_not_claimed': True,
        'reports': {str(CAP / name / 'capture_report.json'): sha((CAP / name / 'capture_report.json').read_bytes())
                    for name in ('product_pitches_v747_baseline_final', 'product_pitches_v747_new', 'product_pitches_v747_newgame')},
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V747 original675/676 fixture sequence, unchanged return and ordinary New Game verified.', flush=True)


if __name__ == '__main__':
    main()
