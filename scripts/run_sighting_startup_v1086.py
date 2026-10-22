"""Cold-boot title/New Game controls using the unchanged real emulator harness."""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.finish_refit_display_v712 import load
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/sighting_release_v1085')
ROM = Path('out/all_routes_combined_v1086_candidate.nds')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
INPUT = Path('work/analysis/cliff_editorial_v829/ordinary_newgame_inputs.json')
FRAMES = [1, 60, 180, 1600, 2000, 3200, 4000]
HARNESS = 'd5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', choices=('newgame', 'title'))
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    digest = sha(ROM.read_bytes())
    assert digest == read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    assert sha(Path(harness.__file__).read_bytes()) == HARNESS
    if args.verify:
        target = ROOT/'ordinary_startup_verification.json'
        assert not target.exists()
        old_digest = sha(Path('out/all_routes_combined_v1034_candidate.nds').read_bytes())
        tests = [('newgame', 4000, 'reinforcement_sniping_v1034_newgame', FRAMES),
                 ('title', 1150, 'reinforcement_sniping_v1034_title', [1100])]
        pairs, receipts = [], []
        sheet = Image.new('RGB', (4*256, 2*410), '#263238')
        draw = ImageDraw.Draw(sheet)
        for mode, frame_count, old_folder, frames in tests:
            current, images, receipt = load(CAP/f'sighting_v1086_{mode}', digest, frame_count)
            previous, old, old_receipt = load(CAP/old_folder, old_digest, frame_count)
            assert not any(v for k, v in current.items() if k.startswith('synthetic_'))
            assert 'battery_save_preloaded' not in current
            assert current['scripted_input_schedule'] == previous['scripted_input_schedule']
            assert current['core_options'] == previous['core_options']
            for frame in frames:
                assert images[frame].tobytes() == old[frame].tobytes(), (mode, frame)
                i = len(pairs)
                pairs.append({'mode': mode, 'frame': frame, 'whole256x384_RGB_exact_to_V1034': True})
                x, y = i % 4*256, i // 4*410
                draw.text((x+4, y+4), f'{mode} frame{frame}', fill='white')
                sheet.paste(images[frame], (x, y+22))
            receipts.append({'mode': mode, 'current': receipt, 'V1034_reference': old_receipt})
        image = ROOT/'ordinary8_startup_and_title_controls.png'
        sheet.save(image)
        save(target, {'candidate': str(ROM), 'candidate_sha256': digest, 'pairs': pairs, 'receipts': receipts,
            'all8_complete_startup_title_NewGame_frames_exact': True,
            'no_battery_save_savestate_or_fixtures': True,
            'harness_file_sha256': HARNESS, 'producer_sha256': sha(Path(__file__).read_bytes()),
            'review_sheet': str(image), 'review_sheet_sha256': sha(image.read_bytes()),
            'visual_review_pending': True, 'new_sighting_attack_close_range_and_name_actual_UI_pending': True, 'full_goal_complete': False})
        print('V1086:all8 startup/title/New Game full-screen pairs match V1034;visual review and new scene checks pending.', flush=True)
        return
    assert args.run in ('newgame', 'title')
    folder = CAP/f'sighting_v1086_{args.run}'
    assert not folder.exists()
    frames, limit = (FRAMES, 4000) if args.run == 'newgame' else ([1100], 1150)
    plan = ROOT/f'{args.run}_run_plan.json'
    assert not plan.exists()
    save(plan, {'candidate': str(ROM), 'candidate_sha256': digest, 'folder': str(folder),
        'frames': limit, 'capture_at': frames, 'input': str(INPUT), 'input_sha256': sha(INPUT.read_bytes()),
        'no_save_savestate_or_fixtures': True, 'unchanged_harness_sha256': HARNESS})
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(folder), '--frames', str(limit),
                '--inputs-json', str(INPUT), '--touchscreen', '--capture-every', '999999',
                '--capture-at', *map(str, frames), '--dump-capture-ram', '--dump-ram']
    harness.main()


if __name__ == '__main__':
    main()
