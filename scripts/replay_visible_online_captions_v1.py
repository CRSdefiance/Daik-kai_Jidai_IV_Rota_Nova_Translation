"""Replay and verify the revised native Online captions against their observed parent."""

import argparse
from pathlib import Path
import sys
from types import FunctionType

from PIL import Image, ImageChops

from scripts import headless_desmume_v193 as harness
from scripts import run_diplomatic_outcome_startup_v2 as startup_replay
from scripts import run_ancient_map_hint_label_startup_v1 as parent_startup
from scripts import stage_visible_online_captions_v1 as stage
from scripts import verify_setup_save_equipment_v1 as startup_check


base, review = stage.base, stage.review
ROOT, ROM = stage.ROOT, stage.ROM
PROOF = ROOT / 'startup_input.json'
BOOT = ROOT / 'own_startup_verification.json'
BIOGRAPHIES = parent_startup.ROOT
LIVE = ROOT / 'online_caption_gameplay_verification.json'


def startup():
    proof = base.load(stage.PROOF)
    assert base.digest(ROM) == proof['candidate_sha256']
    base.save(PROOF, dict(research_ROM_sha256=proof['candidate_sha256'],
                         registered_input=dict(candidate_sha256=proof['parent_sha256'])))
    FunctionType(startup_replay.main.__code__, vars(startup_replay) | dict(EVIDENCE=PROOF, ROM=ROM,
        STARTUP=ROOT / 'own_startup', PRIOR=BIOGRAPHIES / 'own_startup'))()
    FunctionType(startup_check.verify_startup.__code__, vars(startup_check) | globals())()


def gameplay():
    proof = base.load(stage.PROOF)
    assert base.digest(ROM) == proof['candidate_sha256']
    observer = base.load(review.CONSUMERS)
    old_path = review.observed.ROOT / 'online/capture/capture_report.json'
    old = base.load(old_path)
    assert old['ROM_sha256'] == observer['observer_ROM_sha256']
    input_path = review.observed.ROOT / 'online/inputs.json'
    inputs, frames, end, _, donor = review.observed.get_schedule('online')
    assert not donor and base.load(input_path) == inputs and old['frames'] == end
    original = sys.argv
    try:
        sys.argv = [sys.argv[0], '--rom', str(ROM), '--out', str(ROOT / 'online'),
            '--frames', str(end), '--inputs-json', str(input_path), '--press-start', '-1',
            '--capture-every', '999999', '--capture-at', *map(str, frames)]
        harness.main()
    finally:
        sys.argv = original
    report_path = ROOT / 'online/capture_report.json'
    result = base.load(report_path)
    assert result['ROM_sha256'] == proof['candidate_sha256'] and result['frames'] == end
    assert result['cold_boot'] and not result['savestate_loaded'] and not result['callback_errors']
    assert not result.get('battery_save_preloaded')
    assert old['scripted_input_schedule'] == result['scripted_input_schedule']
    left, right = [{row['frame']: row for row in item['frames_captured'] if row['path'].endswith('_cold_boot.png')}
                   for item in (old, result)]
    assert left.keys() == right.keys()
    draft = base.load(review.OUTPUT)
    font = review.GameAsciiFont.from_arm9(base.NdsImage.open(ROM).read_file(stage.ARM))
    observations, revised = [], set()
    for row, hold in zip(draft['records'], observer['observed_online_caption_masks'], strict=True):
        n = hold['screenshot']['frame']
        assert hold['id'] == row['id']
        for image in (left[n], right[n]):
            assert base.digest(image['path']) == image['PNG_sha256']
        a, b = [Image.open(side[n]['path']).convert('RGB') for side in (left, right)]
        x, y = row['output_origin']
        ink, bounds = review.complete_mask(font, row['english'], b, x, y, review.COLOR)
        delta = ImageChops.difference(a, b).getbbox()
        if row['decision'] == 'revision':
            assert delta and 28 <= delta[0] and delta[2] <= 228 and 205 <= delta[1] and delta[3] <= 216
            revised.add(n)
        else:
            assert not delta
        observations.append(dict(id=row['id'], frame=n, complete_ink=ink, bounds=bounds, changed_rectangle=delta))
    assert len(revised) == 4 and len(observations) == 13
    assert all(left[n]['framebuffer_sha256'] == right[n]['framebuffer_sha256'] for n in left.keys() - revised)
    evidence = (report_path, old_path, input_path, stage.PROOF, review.CONSUMERS, Path(__file__))
    base.save(LIVE, dict(candidate_sha256=proof['candidate_sha256'], parent_sha256=proof['parent_sha256'],
        actual_emulator=True, all_observed_caption_masks=observations, original_navigation_and_return_frames_exact=True,
        changed_caption_frames=sorted(revised), other_whole_frame_matches=sorted(left.keys() - revised),
        graphic_artwork_unchanged=True, hardware=False, evidence={str(path): base.digest(path) for path in evidence}))
    print('All 13 original Online caption masks, the revised caption bounds and menu returns passed.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('startup', 'gameplay'))
    (startup if parser.parse_args().action == 'startup' else gameplay)()
