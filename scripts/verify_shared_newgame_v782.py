"""Seven exact cold-boot/New Game framebuffer comparisons, not a route playthrough."""

from pathlib import Path

from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/shared_integration_v782')
REPORT = Path('E:/Rota Nova translations/Generated/work/emulation_v193/shared_v782_newgame/capture_report.json')
OLD = Path('E:/Rota Nova translations/Generated/work/emulation_v193/barmaid_v780_newgame/capture_report.json')


def main():
    reports = [read(p) for p in (OLD, REPORT)]
    for p in reports:
        assert p['cold_boot'] and not p['savestate_loaded'] and not p['callback_errors']
        assert p['frames'] == 4000 and p['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
        assert sha(Path(p['ROM']).read_bytes()) == p['ROM_sha256']
        assert not any(p.get(k) for k in ('battery_save', 'battery_save_copy', 'isolated_location_fixtures', 'isolated_inventory_fixtures'))
    assert reports[0]['scripted_input_schedule'] == reports[1]['scripted_input_schedule']
    assert reports[0]['core_options'] == reports[1]['core_options']
    frames = [{r['frame']: r for r in p['frames_captured']} for p in reports]
    pairs = []
    for frame in (1, 60, 180, 1600, 2000, 3200, 4000):
        rows = [p[frame] for p in frames]
        pixels = []
        for row in rows:
            path = Path(row['path'])
            assert sha(path.read_bytes()) == row['PNG_sha256']
            with Image.open(path) as image:
                pixels.append(image.convert('RGB').tobytes())
        assert pixels[0] == pixels[1]
        pairs.append({'frame': frame, 'captures': rows, 'all_pixels_exact': True})
    save(ROOT/'newgame_regression.json', {
        'candidate_sha256': reports[1]['ROM_sha256'], 'reference_ROM_sha256': reports[0]['ROM_sha256'],
        'capture_reports': [str(OLD), str(REPORT)], 'whole_screen_frame_pairs': pairs, 'all_pixels_exact': True,
        'no_savestate_or_test_fixture': True,
        'scope': 'Seven targeted automated-emulator cold-boot/New Game frames;not new shared-dialogue gameplay,route completion or hardware verification.',
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Seven cold-boot/New Game whole-frame pairs match V780 exactly.', flush=True)


if __name__ == '__main__':
    main()
