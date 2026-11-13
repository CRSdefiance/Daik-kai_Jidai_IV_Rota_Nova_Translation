"""Verify native Auto Move returns and cold startup on the exact staged ROM."""

import argparse
from hashlib import sha256
from pathlib import Path
from types import FunctionType

from ndspy.code import MainCodeFile
from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_navigation_prerequisite_review_v1 import ARM, BASE, OUTPUT, word
from scripts.checkpoint_shared_notice_storage_v1 import checked_report, startup_proof
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
from scripts.record_navigation_v327 import dark_text
from scripts.run_navigation_prerequisite_replays_v1 import FIELD, ORIGINAL, set_condition
from scripts.run_navigation_prerequisite_startup_v1 import PARENT
from scripts.run_navigation_prerequisite_startup_v2 import STARTUP
from scripts.stage_mutiny_review_v1 import render_portrait
from scripts.stage_navigation_prerequisite_balanced_v2 import PROOF, ROM, ROOT, first
from scripts.verify_mutiny_release_inputs_v1 import portrait_ink


LIVE = ROOT / 'navigation_gameplay_verification.json'
BOOT = STARTUP / 'own_startup_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = ROOT / 'repo_qa_navigation_30.xml'


def verify_replay(mode, frames, confirm, warning, restored, message_id, staged, image, raster):
    root = ROOT / mode
    terminal_path = root / 'terminal.json'
    terminal = load(terminal_path)
    sha = staged['research_ROM_sha256']
    assert terminal['mode'] == mode and terminal['candidate_sha256'] == sha
    assert all(digest(terminal[key]) == terminal[key + '_sha256'] for key in ('report', 'earlier_reference'))
    report, final = checked_report(terminal['report'], sha, frames)
    prior = load(terminal['earlier_reference'])
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot']
    assert digest(donor['source']) == donor['source_sha256'] == terminal['donor_sha256']
    assert donor['source_sha256'] == prior['battery_save_preloaded']['source_sha256']
    assert report['core_options'] == prior['core_options']
    assert digest(root / 'inputs.json') == terminal['initial_inputs_sha256']
    initial = load(root / 'inputs.json')
    assert initial == [row for row in prior['scripted_input_schedule'] if row['start'] <= (confirm if mode == 'cabin' else frames)]
    assert not any(report[k] for k in report if k.startswith('synthetic_') and k != 'synthetic_condition_fixtures')
    arm, kanji = image.read_file(ARM), image.read_file('/GRP/KANJI.FNT')
    shots = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('_cold_boot.png')}
    snapshots = {row['frame']: row for row in report['read_only_capture_RAM_snapshots']}

    def snapshot(frame):
        row = snapshots[frame]
        assert row['read_only_export'] and digest(row['path']) == row['sha256']
        return Path(row['path']).read_bytes()

    expected_fixtures = []
    if mode == 'cabin':
        for frame, fixture in ((confirm, 'require-cabin'), (warning, 'restore-cabin')):
            _, row = set_condition(arm, snapshot(frame), {'mode': fixture})
            expected_fixtures.append(row | {'frame': frame})
    assert report.get('synthetic_condition_fixtures', []) == expected_fixtures
    assert final[FIELD - BASE:FIELD - BASE + 4] == ORIGINAL
    assert all(any(event['start'] == frame + 1 and event['buttons'] == ['A']
                   for event in report['scripted_input_schedule']) for frame in (confirm, warning))

    raw = snapshot(warning)
    expand, output = (word(arm, offset) - BASE for offset in (0x5444C, 0x54450))
    plain, display = (raw[at:at + 256].split(b'\0', 1)[0] for at in (expand, output))
    stored = next(row for row in staged['stored'] if row['message_ID'] == message_id)
    case = next(row for row in staged['native_cases'] if row['message_ID'] == message_id)
    assert plain.hex() == stored['staged_hex'] and display.hex() == case['display_hex']
    pixels, glyphs = render_portrait(raster, arm, kanji, display)
    assert sha256(pixels).hexdigest() == case['native_ink_sha256']
    ink = bytes(value == 1 for value in pixels)
    crop = (16, 296, 244, 360)
    assert ink == portrait_ink(shots[warning]['path'], crop)
    assert ink != portrait_ink(shots[restored]['path'], crop)
    font = GameAsciiFont.from_arm9(arm)
    captions = []
    for frame in (confirm, restored):
        with Image.open(shots[frame]['path']) as screen:
            captions.append(dark_text(font, 'Auto Move', screen.convert('RGB'), (88, 270, 170, 308)))
    with Image.open(shots[confirm]['path']) as before, Image.open(shots[restored]['path']) as after:
        assert before.crop((0, 0, 256, 192)).tobytes() == after.crop((0, 0, 256, 192)).tobytes()
        if mode == 'ceuta':
            assert before.tobytes() == after.tobytes()
    return dict(mode=mode, natural_condition=mode == 'ceuta', fixture=expected_fixtures,
        message_ID=message_id, lines=case['visible_lines'], complete_glyphs=len(glyphs),
        displayed=shots[warning], RAM=snapshots[warning], exact_native_foreground_and_margins=True,
        original_confirmation=shots[confirm], returned_confirmation=shots[restored],
        confirmation_caption_masks=captions, dismissed_with_A=True,
        evidence={str(path): digest(path) for path in (terminal_path, Path(terminal['report']))})


def verify_live():
    assert not LIVE.exists()
    staged = load(PROOF)
    sha = digest(ROM)
    assert sha == staged['research_ROM_sha256']
    image = NdsImage.open(ROM)
    raster, _, _ = font_tools(image)
    ceuta = verify_replay('ceuta', 7200, 6000, 6400, 6800, 633, staged, image, raster)
    cabin = verify_replay('cabin', 7800, 7200, 7500, 7800, 646, staged, image, raster)
    save(LIVE, dict(candidate_sha256=sha, observed_notice_IDs=[633, 646], actual_emulator_gameplay=True,
        hardware=False, natural_ceuta=ceuta, focused_cabin=cabin, route_failure_offline_only=True,
        evidence={str(path): digest(path) for path in (PROOF, OUTPUT, Path(__file__))}))
    print('Both warnings match complete native glyphs and return to the original Auto Move confirmation.')


def verify_startup():
    assert not BOOT.exists() and not CHECKPOINT.exists()
    staged, manuscript, live = map(load, (PROOF, OUTPUT, LIVE))
    sha = digest(ROM)
    assert staged['research_ROM_sha256'] == live['candidate_sha256'] == sha
    dependencies = staged['evidence'] | live['evidence'] | live['natural_ceuta']['evidence'] | live['focused_cabin']['evidence']
    assert all(digest(path) == expected for path, expected in dependencies.items())
    assert len(staged['stored']) == len(staged['native_cases']) == 24
    assert manuscript['voice_cases'] == 621 and staged['storage']['all_41_blocks_fit_8KiB']
    sheets = staged['contact_sheets']
    assert all(digest(sheet['path']) == sheet['sha256'] for sheet in sheets)
    assert [n for sheet in sheets for n in sheet['messages']] == list(range(629, 653))
    report_path = STARTUP / 'capture/capture_report.json'
    terminal = load(STARTUP / 'terminal.json')
    assert terminal['candidate_sha256'] == sha and terminal['report_sha256'] == digest(report_path)
    report, raw = checked_report(report_path, sha, 31000)
    parent_path = PARENT / 'capture/capture_report.json'
    parent = load(parent_path)
    assert parent['ROM_sha256'] == staged['registered_input']['candidate_sha256']
    assert parent['scripted_input_schedule'] == report['scripted_input_schedule']
    assert parent['core_options'] == report['core_options']
    old, new = ({shot['frame']: shot for shot in run['frames_captured']} for run in (parent, report))
    frames = (1600, 2200, 3340, 4000, 16000, 31000)
    assert all(old[n]['framebuffer_sha256'] == new[n]['framebuffer_sha256'] for n in frames)
    arm = NdsImage.open(ROM).read_file(ARM)
    check_names = FunctionType(startup_proof.__code__, {**startup_proof.__globals__, 'STARTUP': report_path})
    startup = check_names(arm, sha)
    payload = bytes(MainCodeFile(arm, BASE).sections[3].data[:-48])
    assert len(payload) == 123264 and raw[POOL - BASE:POOL - BASE + len(payload)] == payload
    startup.update(candidate_sha256=sha, cold_boot=True, savestate=False, actual_captain_getter=3,
        read_only_snapshot=report['read_only_RAM_snapshot'], complete_deployed_payload_exact=True,
        exact_predecessor_capture_sha256=digest(parent_path))
    save(BOOT, startup)
    save(CHECKPOINT, dict(candidate_sha256=sha, approved_for_registered_successor=True,
        live_messages=live['observed_notice_IDs'], stored_cases=24, native_pages=24,
        viewed_sheets=sheets, native_selector_cases=staged['selector_scope']['tested'],
        crew_voice_choices=621, route_predicate_cases=32,
        evidence={str(path): digest(path) for path in (PROOF, first.PROOF, OUTPUT, BOOT, LIVE, QA, Path(__file__))}))
    print('Exact startup, six parent frame matches and 24 protected name getters pass.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=('live', 'startup'))
    {'live': verify_live, 'startup': verify_startup}[parser.parse_args().phase]()
