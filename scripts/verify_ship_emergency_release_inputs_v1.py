"""Verify the live emergency panels and exact-candidate startup."""

import argparse
from hashlib import sha256
from pathlib import Path
import struct
from types import FunctionType

from ndspy.code import MainCodeFile

from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_shared_notice_storage_v1 import checked_report, startup_proof
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
from scripts.run_mutiny_replay_v1 import FIELD as MUTINY_FIELD, ORIGINAL as MUTINY_ORIGINAL
from scripts.run_ship_emergency_replays_v1 import FIELD, ORIGINAL, set_condition
from scripts.run_ship_emergency_startup_v1 import PARENT, STARTUP
from scripts.stage_mutiny_review_v1 import render_portrait
from scripts.stage_ship_emergency_balanced_v2 import OUTPUT, PROOF, ROM, ROOT, first
from scripts.stage_ship_emergency_review_v1 import ARM, BASE
from scripts.verify_mutiny_release_inputs_v1 import portrait_ink


LIVE = ROOT / 'ship_emergency_gameplay_verification.json'
BOOT = STARTUP / 'own_startup_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = ROOT / 'repo_qa_ship_emergency.xml'


def captures(report):
    return {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('navigation.png')}


def verify_replay(mode, frame_count, picture_frames, fixture_modes, staged, image, raster):
    sha = staged['research_ROM_sha256']
    root = ROOT / mode
    terminal_path = root / 'terminal.json'
    terminal = load(terminal_path)
    assert terminal['mode'] == mode and terminal['candidate_sha256'] == sha and terminal['donor_unchanged']
    assert all(digest(terminal[key]) == terminal[key + '_sha256'] for key in ('report', 'commands', 'earlier_reference'))
    report, final = checked_report(terminal['report'], sha, frame_count)
    assert not any(report[k] for k in report if k.startswith('synthetic_') and k != 'synthetic_condition_fixtures')
    arm, kanji = image.read_file(ARM), image.read_file('/GRP/KANJI.FNT')
    screenshots = captures(report)
    snapshots = {row['frame']: row for row in report['read_only_pause_RAM_snapshots']}

    def snapshot(frame):
        row = snapshots[frame]
        assert row['read_only_export'] and digest(row['path']) == row['sha256']
        return Path(row['path']).read_bytes()

    expected = []
    for frame, fixture in zip((8327, 9627), fixture_modes, strict=True):
        _, row = set_condition(arm, snapshot(frame), {'mode': fixture})
        expected.append(row | {'frame': frame})
    assert report['synthetic_condition_fixtures'] == expected
    assert final[FIELD - BASE:FIELD - BASE + 4] == ORIGINAL
    assert final[MUTINY_FIELD - BASE:MUTINY_FIELD - BASE + 4] == MUTINY_ORIGINAL
    family = range(573, 580) if mode == 'leak' else range(601, 609)
    outputs = {bytes.fromhex(row['display_hex']): row for row in staged['native_cases']
               if row['message_ID'] in family}
    storage = {row['message_ID']: bytes.fromhex(row['staged_hex']) for row in staged['stored']}
    expand, out = (struct.unpack_from('<I', arm, offset)[0] - BASE for offset in (0x5444C, 0x54450))
    crop = (16, 296, 244, 360)
    observed = []
    for frame in picture_frames:
        raw = snapshot(frame)
        plain, display = (raw[at:at + 256].split(b'\0', 1)[0] for at in (expand, out))
        case = outputs[display]
        args = tuple(value.encode('cp932') for value in case['arguments'])
        payload = storage[case['message_ID']]
        assert plain == (payload % args if args else payload)
        pixels, glyphs = render_portrait(raster, arm, kanji, display)
        assert sha256(pixels).hexdigest() == case['native_ink_sha256']
        ink = bytes(value == 1 for value in pixels)
        assert ink == portrait_ink(screenshots[frame]['path'], crop)
        observed.append(dict(frame=frame, message_ID=case['message_ID'], arguments=case['arguments'],
            lines=case['visible_lines'], capture=screenshots[frame], RAM=snapshots[frame],
            complete_glyphs=len(glyphs), exact_native_foreground_and_margins=True))
    journal = root / 'capture/navigation_command_journal.json'
    commands = {row['frame']: row['command'] for row in load(journal)['commands_received'] if row['validation_passed']}
    assert all(commands[frame]['buttons'] == ['A'] for frame in picture_frames)
    evidence = {str(path): digest(path) for path in (terminal_path, journal, Path(terminal['report']))}
    if mode == 'leak':
        assert ink != portrait_ink(screenshots[9827]['path'], crop)
        scope = dict(warning_dismissed_with_A=True, returned_to_sailing=screenshots[9827])
    else:
        assert [row['arguments'] for row in observed] == [['Food'], ['Water']]
        earlier = captures(load(terminal['earlier_reference']))
        preceding = (9627, 9827, 10027, 10127, 10327, 10527, 10727, 10927)
        assert all(earlier[n]['framebuffer_sha256'] == screenshots[n]['framebuffer_sha256'] for n in preceding)
        scope = dict(original_supply_depletion_after_meal=True, no_supply_values_injected=True,
                     preceding_mutiny_and_return_frames_exact=len(preceding))
    return dict(mode=mode, fixture=expected, observed=observed, evidence=evidence, **scope)


def verify_live():
    assert not LIVE.exists()
    staged = load(PROOF)
    sha = digest(ROM)
    assert sha == staged['research_ROM_sha256']
    image = NdsImage.open(ROM)
    raster, _, _ = font_tools(image)
    leak = verify_replay('leak', 9827, (9627,), ('select-leak', 'restore-leak-selection'), staged, image, raster)
    supplies = verify_replay('supplies', 11727, (11127, 11327), ('select-mutiny', 'restore-mutiny-selection'), staged, image, raster)
    ids = sorted({row['message_ID'] for replay in (leak, supplies) for row in replay['observed']})
    save(LIVE, dict(candidate_sha256=sha, observed_notice_IDs=ids, actual_emulator_gameplay=True, hardware=False,
        flagship_leak=leak, supply_reports=supplies,
        evidence={str(path): digest(path) for path in (PROOF, OUTPUT, Path(__file__))}))
    print('The flagship leak and two supply warnings match the native font and original transitions.')


def verify_startup():
    assert not BOOT.exists() and not CHECKPOINT.exists()
    staged, ordinary, manuscript, live = map(load, (PROOF, first.PROOF, OUTPUT, LIVE))
    sha = digest(ROM)
    assert staged['research_ROM_sha256'] == live['candidate_sha256'] == sha
    dependencies = staged['evidence'] | live['evidence'] | live['flagship_leak']['evidence'] | live['supply_reports']['evidence']
    assert all(digest(path) == expected for path, expected in dependencies.items())
    assert len(staged['stored']) == 41 and len(staged['native_cases']) == 109
    assert manuscript['voice_cases'] == 1242 and staged['storage']['all_41_blocks_fit_8KiB']
    sheets = (*ordinary['contact_sheets'], *staged['contact_sheets'])
    assert all(digest(sheet['path']) == sheet['sha256'] for sheet in sheets)
    report_path = STARTUP / 'capture/capture_report.json'
    terminal = load(STARTUP / 'terminal.json')
    assert terminal['candidate_sha256'] == sha and terminal['report_sha256'] == digest(report_path)
    report, raw = checked_report(report_path, sha, 31000)
    parent_path = PARENT / 'capture/capture_report.json'
    predecessor = load(parent_path)
    assert predecessor['ROM_sha256'] == staged['registered_input']['candidate_sha256']
    assert predecessor['scripted_input_schedule'] == report['scripted_input_schedule']
    assert predecessor['core_options'] == report['core_options']
    old, new = ({s['frame']: s for s in run['frames_captured']} for run in (predecessor, report))
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
        live_messages=live['observed_notice_IDs'], stored_cases=41, native_expansions=109,
        fresh_viewed_pages=staged['rendered_unique_pages'], reused_exact_viewed_pages=staged['reused_exact_pages'],
        native_selector_cases=staged['selector_scope']['tested'], crew_voice_choices=1242,
        evidence={str(path): digest(path) for path in (PROOF, first.PROOF, OUTPUT, BOOT, LIVE, QA, Path(__file__))}))
    print('Exact startup, six parent frame matches, 24 protected getters and the two display paths pass.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=('live', 'startup'))
    {'live': verify_live, 'startup': verify_startup}[parser.parse_args().phase]()
