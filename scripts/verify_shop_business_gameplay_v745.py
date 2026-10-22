"""Ordinary shop replies, return transition and New Game regression captures."""

from pathlib import Path

from PIL import Image, ImageChops

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/shop_business_v745')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def captures(folder, frames):
    report_path = CAP / folder / 'capture_report.json'
    report = read(report_path)
    assert report['frames'] == frames and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors']
    assert report['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert sha(Path(report['ROM']).read_bytes()) == report['ROM_sha256']
    assert not any(k.startswith('synthetic_') and report[k] for k in report)
    rows = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        rows[row['frame']] = row
    if report.get('battery_save_preloaded'):
        donor = report['battery_save_preloaded']
        assert donor['source_sha256'] == 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
        assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
        assert donor['copied_byte_exact_before_cold_boot']
    return report, rows


def main():
    baseline, before = captures('shop_business_v745_baseline', 6500)
    report, after = captures('shop_business_v745_new', 6500)
    assert report['scripted_input_schedule'] == baseline['scripted_input_schedule']
    assert report['battery_save_preloaded']['source'] == baseline['battery_save_preloaded']['source']
    assert set(before) == set(after)
    rom = NdsImage.open(report['ROM'])
    font = GameAsciiFont.from_arm9(rom.read_file('/__arm9__.bin'))
    block = IlnkContainer.parse(rom.read_file('/COMMON/MESFILE.DK4')).blocks[8]
    layouts = {r['message_id']: r for r in read(ROOT / 'native_review.json')['native_macro_and_full_font_checks']}
    checks, equal = [], []
    selected = {5600: 657, 5900: 658}
    for frame in sorted(after):
        old = Image.open(before[frame]['path']).convert('RGB')
        new = Image.open(after[frame]['path']).convert('RGB')
        difference = ImageChops.difference(old, new)
        if frame not in selected:
            assert difference.getbbox() is None, frame
            equal.append(frame)
            continue
        i = selected[frame]
        expected = set()
        for nline, line in enumerate(layouts[i]['lines']):
            for n, char in enumerate(line):
                glyph = font.decode(char)
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x, y)):
                            expected.add((22 + n * 6 + x, 296 + nline * 16 + y))
        actual = {(x, y) for y in range(294, 366) for x in range(16, 240)
                  if new.getpixel((x, y)) == (0, 8, 0)}
        assert expected == actual, (frame, len(expected - actual), len(actual - expected))
        outside = difference.copy()
        outside.paste((0, 0, 0), (16, 294, 240, 366))
        assert outside.getbbox() is None
        snapshot = next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame'] == frame)
        ram = Path(snapshot['path']).read_bytes()
        assert len(ram) == 4194304 and sha(ram) == snapshot['sha256']
        position = ram.find(block)
        assert position >= 0 and ram.find(block, position + 1) == -1
        checks.append({'frame': frame, 'message_id': i, 'lines': layouts[i]['lines'],
                       'all_glyph_and_blank_paper_cells_exact': True, 'ink_pixels': len(actual),
                       'whole_resident_block8_exact': True, 'resident_address': 0x02000000 + position,
                       'all_pixels_outside_dialogue_body_equal_baseline': True,
                       'capture': after[frame]})
    assert len(equal) == 17 and {6050, 6150, 6250, 6400, 6500} <= set(equal)
    game, game_rows = captures('shop_business_v745_newgame', 4000)
    old_game = read(CAP / 'script_sources_v733_baseline/capture_report.json')
    assert game['scripted_input_schedule'] == [r for r in old_game['scripted_input_schedule'] if r['start'] <= 4000]
    assert not game.get('battery_save_preloaded')
    old_rows = {r['frame']: r for r in old_game['frames_captured']}
    same = sorted(old_rows.keys() & game_rows.keys())
    assert len(same) == 11
    for frame in same:
        old = old_rows[frame]
        assert sha(Path(old['path']).read_bytes()) == old['PNG_sha256']
        assert Image.open(old['path']).convert('RGB').tobytes() == Image.open(game_rows[frame]['path']).convert('RGB').tobytes()
    save(ROOT / 'gameplay_verification.json', {
        'candidate': report['ROM'], 'candidate_sha256': report['ROM_sha256'],
        'two_terminal6500_frame_shop_cold_boots': True,
        'ordinary_native_message_displays': checks,
        'whole_two_screen_equal_baseline_frames': equal,
        'ordinary_dialogue_exit_and_town_return_equal_baseline': True,
        'no_savestate_or_gameplay_fixture': True,
        'New_Game_terminal4000_frame_cold_boot': True,
        'New_Game11_whole_frame_pairs_exact': same,
        'other_five_changed_replies_complete_native_component_verified_not_ordinary_events': [682, 683, 684, 686, 687],
        'original_donor_save_unchanged': True,
        'reports': {str(CAP / name / 'capture_report.json'): sha((CAP / name / 'capture_report.json').read_bytes())
                    for name in ('shop_business_v745_baseline', 'shop_business_v745_new', 'shop_business_v745_newgame')},
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False,
    })
    print('V745 ordinary 657/658 complete; 17 shop and 11 New Game whole-frame pairs exact.', flush=True)


if __name__ == '__main__':
    main()
