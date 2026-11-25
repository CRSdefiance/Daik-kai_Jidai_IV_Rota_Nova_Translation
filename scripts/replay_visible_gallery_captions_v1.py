"""Replay the Gallery caption candidate and its exact parent through all four carousels."""

import argparse
from pathlib import Path
import sys
from types import FunctionType

from PIL import Image, ImageChops

from scripts import headless_desmume_v193 as harness
from scripts import run_diplomatic_outcome_startup_v2 as startup_replay
from scripts import stage_visible_gallery_captions_v1 as stage
from scripts import verify_setup_save_equipment_v1 as startup_check
from scripts.verify_gallery_hodram_v521 import compact_caption


base, review = stage.base, stage.review
ROOT, ROM = stage.ROOT, stage.ROM
PROOF = ROOT / 'startup_input.json'
BOOT = ROOT / 'own_startup_verification.json'
BIOGRAPHIES = stage.parent.replay.ROOT
LIVE = ROOT / 'gallery_caption_gameplay_verification.json'
OLD_REPORT = Path('work/emulation_v193/gallery_all_v523/capture_report.json')


def startup():
    proof = base.load(stage.PROOF)
    assert base.digest(ROM) == proof['candidate_sha256']
    base.save(PROOF, dict(research_ROM_sha256=proof['candidate_sha256'],
                         registered_input=dict(candidate_sha256=proof['parent_sha256'])))
    FunctionType(startup_replay.main.__code__, vars(startup_replay) | dict(EVIDENCE=PROOF, ROM=ROM,
        STARTUP=ROOT / 'own_startup', PRIOR=BIOGRAPHIES / 'own_startup'))()
    FunctionType(startup_check.verify_startup.__code__, vars(startup_check) | globals())()


def schedule():
    old = base.load(OLD_REPORT)
    events = list(old['scripted_input_schedule'][:7])
    seen, frames = {}, [2400, 2800]
    frame = 3200
    tracks = [
        (['LEFT'], {0, 45}),
        (['RIGHT'] * 7, {0, 2, 7}),
        (['RIGHT'] * 11, {0, 11}),
        (['LEFT'] * 5, {0, 37, 33}),
    ]
    for route, (buttons, observed) in enumerate(tracks):
        if route:
            touch = {1: [170, 50], 2: [84, 130], 3: [170, 130]}[route]
            events.extend([dict(start=frame+1, duration=8, buttons=[], touch=touch),
                           dict(start=frame+201, duration=8, buttons=['A'])])
            frame += 400
        position = 0
        seen[frame] = (route, position)
        for button in buttons:
            events.append(dict(start=frame+1, duration=8, buttons=[button]))
            frame += 200
            delta = 1 if button == 'RIGHT' else -1
            position = (position + delta) % len(review.NOTES[route])
            if position in observed:
                seen[frame] = (route, position)
        events.append(dict(start=frame+1, duration=8, buttons=['B']))
        frame += 400
        frames.append(frame)
    for _ in range(2):
        events.append(dict(start=frame+1, duration=8, buttons=['B']))
        frame += 300
        frames.append(frame)
    return events, sorted([*frames, *seen]), frame, seen, old['battery_save_preloaded']


def capture(side):
    assert side in ('parent', 'revised')
    proof = base.load(stage.PROOF)
    path = stage.parent.ROM if side == 'parent' else ROM
    digest = proof['parent_sha256' if side == 'parent' else 'candidate_sha256']
    assert base.digest(path) == digest
    events, frames, end, _, donor = schedule()
    assert base.digest(donor['source']) == donor['source_sha256']
    folder = ROOT / f'gallery_{side}'
    folder.mkdir()
    input_path = folder / 'inputs.json'
    base.save(input_path, events)
    old_argv = sys.argv
    try:
        sys.argv = [sys.argv[0], '--rom', str(path), '--out', str(folder / 'capture'), '--frames', str(end),
            '--inputs-json', str(input_path), '--press-start', '-1', '--capture-every', '999999',
            '--capture-at', *map(str, frames), '--touchscreen', '--battery-save', donor['source']]
        harness.main()
    finally:
        sys.argv = old_argv
    report_path = folder / 'capture/capture_report.json'
    report = base.load(report_path)
    assert report['ROM_sha256'] == digest and report['frames'] == end
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['battery_save_preloaded']['source_sha256'] == base.digest(donor['source'])
    base.save(folder / 'terminal.json', dict(candidate_sha256=digest, report_sha256=base.digest(report_path),
        schedule_sha256=base.digest(input_path), original_donor_sha256=donor['source_sha256']))


def compare():
    proof = base.load(stage.PROOF)
    assert base.digest(ROM) == proof['candidate_sha256']
    schedule_rows, frames, end, seen, _ = schedule()
    runs, receipts = [], []
    for side, sha in (('parent', proof['parent_sha256']), ('revised', proof['candidate_sha256'])):
        folder = ROOT / f'gallery_{side}'
        terminal = folder / 'terminal.json'
        report = folder / 'capture/capture_report.json'
        receipt = base.load(terminal)
        body = base.load(report)
        assert receipt['report_sha256'] == base.digest(report)
        assert receipt['schedule_sha256'] == base.digest(folder / 'inputs.json')
        assert receipt['candidate_sha256'] == body['ROM_sha256'] == sha and body['frames'] == end
        assert body['scripted_input_schedule'] == schedule_rows
        runs.append({r['frame']: r for r in body['frames_captured'] if r['frame'] in frames
                     and r['path'].endswith('_cold_boot.png')})
        receipts.extend((terminal, report))
    assert runs[0].keys() == runs[1].keys() == set(frames)
    draft = base.load(review.OUTPUT)
    rows = {(r['route'], r['position']): r for r in draft['records']}
    font = stage.GameAsciiFont.from_arm9(base.NdsImage.open(ROM).read_file(stage.ARM))
    selected, revised, exact = [], [], []
    for frame in frames:
        before, after = [run[frame] for run in runs]
        assert all(base.digest(row['path']) == row['PNG_sha256'] for row in (before, after))
        a, b = [Image.open(row['path']).convert('RGB') for row in (before, after)]
        delta = ImageChops.difference(a, b).getbbox()
        if frame in seen:
            row = rows[seen[frame]]
            old = compact_caption(font, row['current_English'], a)
            new = compact_caption(font, row['english'], b)
            selected.append(dict(id=row['id'], frame=frame, original_image=row['original_scene_image'],
                                 before=old, after=new, changed_rectangle=delta))
            if row['decision'] == 'revision':
                assert delta and 32 <= delta[0] < delta[2] <= 224 and 262 <= delta[1] < delta[3] <= 273
                revised.append(row['id'])
                continue
        assert not delta and before['framebuffer_sha256'] == after['framebuffer_sha256']
        exact.append(frame)
    assert len(selected) == 10 and len(revised) == 7
    base.save(LIVE, dict(candidate_sha256=proof['candidate_sha256'], parent_sha256=proof['parent_sha256'],
        actual_emulator=True, selected_captions=selected, observed_revision_ids=revised,
        original_arrows_and_navigation_preserved=True, exact_frame_matches=exact,
        all_image_and_noncaption_pixels_exact=True, isolated_Gallery_unlock_battery=True,
        earned_Gallery_unlock=False, hardware=False,
        evidence={str(path): base.digest(path) for path in (*receipts, stage.PROOF, Path(__file__))}))
    print('Ten original Gallery positions and seven revised captions matched; arrows and return screens are exact.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('startup', 'parent', 'revised', 'compare'))
    action = parser.parse_args().action
    if action == 'startup':
        startup()
    elif action == 'compare':
        compare()
    else:
        capture(action)
