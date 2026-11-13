"""Cold-boot Sound Setup and inspect the longest original track title."""

import sys

from scripts import headless_desmume_v193 as harness
from scripts import register_ancient_map_text_v2 as parent


base = parent.base
ROOT = parent.TEST.with_name('sound_bgm_title_display_20261111_v1')
START, STEP = 3300, 180
LONGEST, RAFAEL, CAMILLE = (START + index * STEP for index in (14, 24, 26))
FRAMES = (3200, START + 9 * STEP, START + 10 * STEP, LONGEST, RAFAEL, CAMILLE, CAMILLE + 180, CAMILLE + 360)


def inputs():
    # The first four inputs are the known ordinary title-to-Sound-Setup path.
    result = [dict(start=frame, duration=8, buttons=[button]) for frame, button in (
        (1601, 'START'), (2101, 'DOWN'), (2401, 'A'), (2801, 'A'),
    )]
    result.extend(dict(start=START + i * STEP + 1, duration=8, buttons=['DOWN']) for i in range(26))
    result.extend(dict(start=frame + 1, duration=8, buttons=['B']) for frame in (CAMILLE, CAMILLE + 180))
    return result


def main():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release['candidate_sha256']
    ROOT.mkdir()
    schedule = ROOT / 'inputs.json'
    base.save(schedule, inputs())
    sys.argv = [sys.argv[0], '--rom', str(parent.ROM), '--out', str(ROOT / 'capture'),
        '--frames', str(FRAMES[-1]), '--press-start', '-1', '--inputs-json', str(schedule),
        '--capture-every', '999999', '--capture-at', *map(str, FRAMES)]
    harness.main()
    path = ROOT / 'capture/capture_report.json'
    report = base.load(path)
    assert report['ROM_sha256'] == release['candidate_sha256'] and report['frames'] == FRAMES[-1]
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report.get('battery_save_preloaded')
    assert {row['frame'] for row in report['frames_captured']} >= set(FRAMES)
    base.save(ROOT / 'terminal.json', dict(candidate_sha256=report['ROM_sha256'],
        report_sha256=base.digest(path), inputs_sha256=base.digest(schedule), longest_track_frame=LONGEST,
        named_tracks_frames=[RAFAEL, CAMILLE], fixture=False))
    print('Sound Setup’s longest title, both named tracks and return frames were captured.')


if __name__ == '__main__':
    main()
