"""Verify the BGM candidate’s ordinary startup, menu transitions and four revised titles."""

import argparse
from hashlib import sha256
from pathlib import Path
from types import FunctionType
from xml.etree import ElementTree

from PIL import Image, ImageChops

from scripts import replay_sound_bgm_titles_v1 as baseline
from scripts import run_diplomatic_outcome_startup_v2 as replay
from scripts import stage_sound_bgm_titles_v1 as stage
from scripts import verify_setup_save_equipment_v1 as startup


base = stage.base
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.ROOT / 'startup_input.json'
REGISTRATION = ROOT / 'registered_inputs.json'
BOOT = ROOT / 'own_startup_verification.json'
LIVE = ROOT / 'sound_setup_gameplay_verification.json'
VISUAL = ROOT / 'sound_setup_visual_review.json'
CHECKPOINT = ROOT / 'ready_to_register.json'
BIOGRAPHIES = stage.parent.stage.ROOT
QA = Path('work/sound_bgm_titles_repo_qa_20261111.xml')
OBSERVED = {baseline.FRAMES[1]: 3260, baseline.FRAMES[2]: 3261, baseline.LONGEST: 3265,
            baseline.RAFAEL: 3275, baseline.CAMILLE: 3277}
TITLE_BOX = (4, 258, 124, 271)


def cold_boot():
    proof = base.load(stage.PROOF)
    assert base.digest(ROM) == proof['candidate_sha256']
    base.save(PROOF, dict(research_ROM_sha256=proof['candidate_sha256'],
        registered_input=dict(candidate_sha256=proof['parent_sha256'])))
    FunctionType(replay.main.__code__, vars(replay) | dict(EVIDENCE=PROOF, ROM=ROM,
        STARTUP=ROOT / 'own_startup', PRIOR=BIOGRAPHIES / 'own_startup'))()


def capture(folder, sha):
    terminal = folder / 'terminal.json'
    path = folder / 'capture/capture_report.json'
    receipt = base.load(terminal)
    report = base.load(path)
    assert base.digest(path) == receipt['report_sha256']
    assert report['ROM_sha256'] == receipt['candidate_sha256'] == sha
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames'] == baseline.FRAMES[-1] and not report.get('battery_save_preloaded')
    assert report['scripted_input_schedule'] == baseline.inputs()
    frames = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('_cold_boot.png')}
    assert set(baseline.FRAMES) <= frames.keys()
    assert all(base.digest(row['path']) == row['PNG_sha256'] for row in frames.values())
    return frames, (terminal, path)


def gameplay():
    proof = base.load(stage.PROOF)
    before, old_evidence = capture(baseline.ROOT, proof['parent_sha256'])
    after, new_evidence = capture(ROOT / 'sound_setup', proof['candidate_sha256'])
    assert before.keys() == after.keys()
    font = stage.GameAsciiFont.from_arm9(base.NdsImage.open(ROM).read_file(stage.ARM))
    rows = {row['message_ID']: row for row in proof['records']}
    changed = {n for n, row in OBSERVED.items() if row in stage.review.REVISIONS}
    assert all(before[n]['framebuffer_sha256'] == after[n]['framebuffer_sha256'] for n in before.keys() - changed)
    details = []
    for frame, n in OBSERVED.items():
        a, b = [Image.open(run[frame]['path']).convert('RGB') for run in (before, after)]
        diff = ImageChops.difference(a, b).getbbox()
        if frame in changed:
            assert diff and diff[0] >= TITLE_BOX[0] and diff[1] >= TITLE_BOX[1]
            assert diff[2] <= TITLE_BOX[2] and diff[3] <= TITLE_BOX[3]
        row = rows[n]
        x0, _ = row['original_center']
        expected = {(x0 + i * 5 + gx, 259 + gy) for i, char in enumerate(row['complete_text'])
                    for gx in range(6) for gy in range(11) if font.decode(char).getpixel((gx, gy))}
        actual = {(x, y) for x in range(128) for y in range(258, 271) if b.getpixel((x, y)) == (230, 230, 230)}
        assert expected == actual, (n, len(expected), len(actual), sorted(expected ^ actual)[:10])
        details.append(dict(message_ID=n, exact_ink=len(actual), changed_bounds=diff, before=before[frame], after=after[frame]))
    evidence = (*old_evidence, *new_evidence, stage.PROOF, Path(__file__))
    base.save(LIVE, dict(candidate_sha256=base.digest(ROM), actual_emulator=True, hardware=False,
        observed_ids=list(OBSERVED.values()), observations=details, original_return_frames_exact=True,
        gameplay_fixture=False, scope='Ordinary Options and Sound Setup inputs. Audio output was not assessed.',
        evidence={str(path): base.digest(path) for path in evidence}))
    print('All four revised titles and the longest retained title match the actual glyphs. Both returns are exact.')


def approve(viewed):
    proof, live, boot = map(base.load, (stage.PROOF, LIVE, BOOT))
    assert proof['candidate_sha256'] == live['candidate_sha256'] == boot['candidate_sha256'] == base.digest(ROM)
    assert len(boot['original_protected_name_getters']) == 24
    assert len(proof['records']) == 38 and len(live['observations']) == 5
    assert viewed == [row['sha256'] for row in proof['sheets']]
    assert all(base.digest(row['path']) == row['sha256'] for row in proof['sheets'])
    tests = list(ElementTree.parse(QA).iter('testsuite'))
    assert sum(int(t.get('tests', 0)) for t in tests) == 34
    assert not any(int(t.get(k, 0)) for t in tests for k in ('errors', 'failures', 'skipped'))
    image = base.NdsImage.open(ROM)
    base.save(REGISTRATION, proof | dict(research_ROM_sha256=proof['candidate_sha256'],
        registered_input=dict(candidate_sha256=proof['parent_sha256']),
        research_ARM9_sha256=sha256(image.read_file(stage.ARM)).hexdigest(),
        research_COMMON_sha256=sha256(image.read_file(stage.COMMON)).hexdigest()))
    base.save(VISUAL, dict(viewed_sheets=proof['sheets'], reviewed_track_titles=38, candidate_sha256=base.digest(ROM)))
    base.save(CHECKPOINT, dict(candidate_sha256=base.digest(ROM), approved_for_registered_successor=True,
        live_messages=live['observed_ids'], stored_cases=38, viewed_pages=38,
        evidence={str(path): base.digest(path) for path in (stage.PROOF, REGISTRATION, LIVE, BOOT, QA, VISUAL, Path(__file__))}))
    print('All 38 BGM titles are ready for registered integration.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only', choices=('cold-boot', 'startup', 'gameplay'))
    parser.add_argument('--approve', nargs=2)
    args = parser.parse_args()
    if args.approve:
        approve(args.approve)
    elif args.only == 'cold-boot':
        cold_boot()
    elif args.only == 'startup':
        FunctionType(startup.verify_startup.__code__, vars(startup) | globals())()
    elif args.only == 'gameplay':
        gameplay()
    else:
        parser.error('Select an action')
