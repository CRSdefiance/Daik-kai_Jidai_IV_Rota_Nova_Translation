"""Verify the assignment decisions, emulator pages, and exact candidate startup."""

import argparse
from hashlib import sha256
from pathlib import Path
from types import FunctionType

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1

from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_sailing_alert_review_v1 import word
from scripts.checkpoint_shared_notice_storage_v1 import checked_report, startup_proof
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
from scripts.run_sera_assignment_replay_v1 import CASES, PARENT, REFERENCE, SLOT, STARTUP, set_condition
from scripts.stage_mutiny_review_v1 import render_portrait
from scripts.stage_sera_assignment_review_v1 import ACTOR, ARM, BASE, OUTPUT, PROOF, ROM, ROOT
from scripts.verify_mutiny_release_inputs_v1 import portrait_ink
from scripts.verify_personal_gameplay_v841 import get_machine


LIVE = ROOT / 'sera_assignment_gameplay_verification.json'
BOOT = STARTUP / 'own_startup_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = ROOT / 'repo_qa_sera_assignment.xml'


def offline_decisions(arm, raw):
    decisions = []
    for mode, (_, _, expected) in CASES.items():
        before, fixture = set_condition(arm, raw, {'mode': mode})
        cpu, get = get_machine(arm, before)
        seen = []

        def intercept(u, pc, size, _):
            if pc == 0x02053FE4:
                assert u.reg_read(UC_ARM_REG_R0) == fixture['actor_object']
                seen.append(u.reg_read(UC_ARM_REG_R1))
            else:
                assert u.reg_read(UC_ARM_REG_R0) == fixture['selection_owner']
                seen.append('original repaint')
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

        for pc in (0x02053FE4, 0x02013724):
            cpu.hook_add(UC_HOOK_CODE, intercept, begin=pc, end=pc)
        get(0x13450, fixture['selection_owner'], SLOT)
        assert seen == [expected, 'original repaint']
        occupants = [get(0x82BC4, fixture['controller'], n) for n in range(31)]
        assigned = fixture['original_eligibility']
        assert (occupants[SLOT], occupants.count(ACTOR)) == ((ACTOR, 1) if assigned else (208, 0))
        decisions.append(dict(mode=mode, message_ID=expected, room_type=fixture['room_type'],
            language_bit=fixture['language_bit'], original_assignment=bool(assigned), original_repaint=True))
    return decisions


def check_replay(mode, arm, kanji, raster, staged):
    path = ROOT / mode
    terminal_path = path / 'terminal.json'
    terminal = load(terminal_path)
    sha = staged['research_ROM_sha256']
    assert terminal['mode'] == mode and terminal['candidate_sha256'] == sha
    assert all(digest(terminal[key]) == terminal[key + '_sha256'] for key in ('report', 'earlier_reference'))
    report, final = checked_report(terminal['report'], sha, 4800)
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot']
    assert digest(donor['source']) == donor['source_sha256'] == terminal['unchanged_donor_sha256']
    assert report['core_options'] == load(REFERENCE)['core_options']
    assert not any(report[k] for k in report if k.startswith('synthetic_') and k != 'synthetic_condition_fixtures')
    shots = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('_navigation.png')}
    ram = {row['frame']: row for row in report['read_only_pause_RAM_snapshots']}

    def snapshot(frame):
        row = ram[frame]
        assert row['read_only_export'] and digest(row['path']) == row['sha256']
        return Path(row['path']).read_bytes()

    raw = snapshot(4400)
    _, fixture = set_condition(arm, raw, {'mode': mode})
    assert report['synthetic_condition_fixtures'] == [fixture | {'frame': 4400}]
    assert all(any(e['start'] == frame and e['buttons'] == ['A'] for e in report['scripted_input_schedule'])
               for frame in (4401, 4601))
    shown = snapshot(4600)
    offsets = [word(arm, off) - BASE for off in (0x5444C, 0x54450)]
    plain, display = [shown[at:at + 256].split(b'\0', 1)[0] for at in offsets]
    number = fixture['expected_message_ID']
    stored = next(row for row in staged['stored'] if row['message_ID'] == number)
    expected = next(row for row in staged['native_cases'] if row['message_ID'] == number)
    assert plain.hex() == stored['staged_hex'] and display.hex() == expected['display_hex']
    pixels, glyphs = render_portrait(raster, arm, kanji, display)
    assert sha256(pixels).hexdigest() == expected['native_ink_sha256']
    crop = (16, 296, 244, 360)
    ink = bytes(value == 1 for value in pixels)
    assert ink == portrait_ink(shots[4600]['path'], crop)
    assert ink != portrait_ink(shots[4800]['path'], crop)
    _, get = get_machine(arm, final)
    occupant = get(0x82BC4, fixture['controller'], SLOT)
    assert occupant == (ACTOR if mode == 'galley' else 208)
    return dict(mode=mode, message_ID=number, original_branch_fixture=fixture,
        original_occupant_after_dismissal=occupant, dismissed_with_A=True, native_ink_exact=True,
        complete_glyphs=len(glyphs), lines=expected['visible_lines'], displayed=shots[4600], returned=shots[4800],
        source_RAM=ram[4400], visible_RAM=ram[4600],
        evidence={str(p): digest(p) for p in (terminal_path, Path(terminal['report']))}), raw


def verify_live():
    assert not LIVE.exists()
    staged = load(PROOF)
    sha = digest(ROM)
    assert sha == staged['research_ROM_sha256']
    image = NdsImage.open(ROM)
    arm, kanji = image.read_file(ARM), image.read_file('/GRP/KANJI.FNT')
    raster, _, _ = font_tools(image)
    galley, raw = check_replay('galley', arm, kanji, raster, staged)
    language, _ = check_replay('language', arm, kanji, raster, staged)
    decisions = offline_decisions(arm, raw)
    save(LIVE, dict(candidate_sha256=sha, actual_emulator_gameplay=True, hardware=False,
        observed_notice_IDs=[1357, 1360], galley=galley, language=language, all_four_native_decisions=decisions,
        cabin_and_other_refusal_offline_only=True,
        evidence={str(p): digest(p) for p in (PROOF, OUTPUT, Path(__file__))}))
    print('Both staged pages, original assignment or refusal, and A dismissal passed. Four native branches passed.')


def verify_startup():
    assert not BOOT.exists() and not CHECKPOINT.exists()
    staged, live = map(load, (PROOF, LIVE))
    sha = digest(ROM)
    assert staged['research_ROM_sha256'] == live['candidate_sha256'] == sha
    assert len(staged['stored']) == len(staged['native_cases']) == 4
    assert len(live['all_four_native_decisions']) == 4
    assert all(digest(p) == h for p, h in (staged['evidence'] | live['evidence']).items())
    assert all(digest(row['path']) == row['sha256'] for row in staged['contact_sheets'])
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
        live_messages=live['observed_notice_IDs'], stored_cases=4, viewed_pages=4,
        evidence={str(p): digest(p) for p in (PROOF, OUTPUT, BOOT, LIVE, QA, Path(__file__))}))
    print('Exact startup, six parent frame matches and 24 protected name getters passed.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=('live', 'startup'))
    (verify_live if parser.parse_args().phase == 'live' else verify_startup)()
