"""Check the native choice outcomes, village replay, and exact candidate startup."""

import argparse
from hashlib import sha256
from pathlib import Path
from types import FunctionType

from ndspy.code import MainCodeFile
from PIL import Image
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1
from unicorn.arm_const import UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R7, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_sailing_alert_review_v1 import word
from scripts.checkpoint_shared_notice_storage_v1 import checked_report, startup_proof
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
from scripts.probe_button_prompt_native import STACK, STOP
from scripts.record_navigation_v327 import dark_text
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.research_battle_declaration_context_v991c import ptr, text
from scripts.run_sea_approach_village_replay_v1 import PARENT, REFERENCE, STARTUP, relocate
from scripts.stage_mutiny_review_v1 import render_portrait
from scripts.stage_sea_approach_village_balanced_v2 import OUTPUT, PROOF, ROM, ROOT, first
from scripts.stage_sea_approach_village_review_v1 import ARM, BASE, COMMON, RELEASE
from scripts.verify_mutiny_release_inputs_v1 import portrait_ink


CHOICES = ROOT / 'sea_approach_offline_choice_verification.json'
LIVE = ROOT / 'village_gameplay_verification.json'
BOOT = STARTUP / 'own_startup_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = ROOT / 'repo_qa_sea_approach.xml'


def verify_choices():
    assert not CHOICES.exists()
    proof, review, release = map(load, (PROOF, OUTPUT, RELEASE))
    assert digest(ROM) == proof['research_ROM_sha256']
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    image = NdsImage.open(ROM)
    arm, common = image.read_file(ARM), image.read_file(COMMON)
    ctx = with_components(runtime, arm, common)
    group = next(row for row in review['exact_native_groups'] if row['first_ID'] == 1297)
    expected = {row['message_ID']: bytes.fromhex(row['staged_hex']) for row in proof['stored']}
    faction = review['original_arguments']['faction_label'][2]
    outputs = []
    for number in range(1297, 1305):
        actor = next(i for i, _, n in group['original_voice_choices'] if n == number)
        actor_pointer = ctx.actor_root + (0x19E4 if actor == 3 else 4 + 32 * actor)
        for entry, accepted, declined in ((0x02077690, 0x020776B8, 0x02077730),
                                           (0x02077978, 0x020779A0, 0x02077A18)):
            for ui_result in (0, 1):
                cpu, get, provider = ctx.machine(arm, common, ctx.raw, ctx.plan)
                faction_pointer = get(0xCB160) + 4 + faction['index'] * 76
                assert ptr(cpu, ptr(cpu, faction_pointer) + 8) == faction['getter']
                seen = []

                def on_step(u, pc, size, _):
                    if pc == 0x02053CDC:
                        u.reg_write(UC_ARM_REG_R0, actor)
                    elif pc == 0x02054058:
                        assert u.reg_read(UC_ARM_REG_R0) == 1
                        assert u.reg_read(UC_ARM_REG_R1) == actor_pointer
                        assert text(u, u.reg_read(UC_ARM_REG_R2)) == expected[number]
                        arg = ptr(u, u.reg_read(UC_ARM_REG_R3))
                        assert text(u, arg).hex() == faction['hex']
                        seen.append(pc)
                        u.reg_write(UC_ARM_REG_R0, ui_result)
                        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
                    else:
                        seen.append(pc)
                        u.emu_stop()

                for address in (0x02053CDC, 0x02054058, accepted, declined):
                    cpu.hook_add(UC_HOOK_CODE, on_step, begin=address, end=address)
                cpu.reg_write(UC_ARM_REG_R7, faction_pointer)
                cpu.reg_write(UC_ARM_REG_R4, 1)
                cpu.reg_write(UC_ARM_REG_SP, STACK)
                cpu.reg_write(UC_ARM_REG_LR, STOP)
                cpu.emu_start(entry, STOP, count=2000000)
                branch = declined if ui_result else accepted
                assert seen == [0x02054058, branch] and cpu.reg_read(UC_ARM_REG_SP) == STACK
                assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
                ctx.calls.clear()
                outputs.append(dict(message_ID=number, caller_fragment=entry, UI_result=ui_result,
                    original_branch=branch, source_faction=faction['label'], copied_argument_hex=faction['hex'],
                    source_first_mate_actor=actor, original_file_reads=provider.reads))
    assert len(outputs) == 32
    save(CHOICES, dict(candidate_sha256=proof['research_ROM_sha256'], original_caller_choice_cases=outputs,
        native_accept_and_decline_paths_preserved=True, actual_gameplay=False,
        evidence={str(path): digest(path) for path in (OUTPUT, PROOF, Path(__file__))}))
    print('Both original battle-assistance callers preserve accept and decline across all eight voices.')


def verify_live():
    assert not LIVE.exists()
    staged = load(PROOF)
    sha = staged['research_ROM_sha256']
    assert digest(ROM) == sha
    folder = ROOT / 'village_resupply'
    terminal_path = folder / 'terminal.json'
    terminal = load(terminal_path)
    assert terminal['candidate_sha256'] == sha and terminal['report_sha256'] == digest(terminal['report'])
    assert terminal['prior_capture'] == str(REFERENCE) and digest(REFERENCE) == terminal['prior_capture_sha256']
    report, _ = checked_report(terminal['report'], sha, 8000)
    donor = report['battery_save_preloaded']
    assert digest(donor['source']) == donor['source_sha256'] == terminal['unchanged_donor_sha256']
    assert report['scripted_input_schedule'] == load(folder / 'inputs.json')
    assert not any(report[k] for k in report if k.startswith('synthetic_') and k != 'synthetic_location_fixtures')
    shots = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('_navigation.png')}
    ram = {row['frame']: row for row in report['read_only_pause_RAM_snapshots']}

    def snapshot(frame):
        row = ram[frame]
        assert row['read_only_export'] and digest(row['path']) == row['sha256']
        return Path(row['path']).read_bytes()

    image = NdsImage.open(ROM)
    arm, kanji = image.read_file(ARM), image.read_file('/GRP/KANJI.FNT')
    _, fixture = relocate(arm, snapshot(5200), 0)
    assert report['synthetic_location_fixtures'] == [fixture | {'frame': 5200}]
    raster, _, _ = font_tools(image)
    out = word(arm, 0x54450) - BASE
    expand = word(arm, 0x5444C) - BASE
    stored = {row['message_ID']: row['staged_hex'] for row in staged['stored']}
    seen = []
    for frame, first_id, last_id in ((5400, 1313, 1320), (7600, 1321, 1328)):
        raw = snapshot(frame)
        plain, body = (raw[at:at + 256].split(b'\0', 1)[0] for at in (expand, out))
        case, = [row for row in staged['native_cases']
                 if first_id <= row['message_ID'] <= last_id and row['display_hex'] == body.hex()]
        assert plain.hex() == stored[case['message_ID']]
        pixels, glyphs = render_portrait(raster, arm, kanji, body)
        assert sha256(pixels).hexdigest() == case['native_ink_sha256']
        ink = bytes(value == 1 for value in pixels)
        assert ink == portrait_ink(shots[frame]['path'], (16, 296, 244, 360))
        seen.append(dict(message_ID=case['message_ID'], frame=frame, visible_lines=case['visible_lines'],
            complete_glyphs=len(glyphs), screenshot=shots[frame], RAM=ram[frame], exact_native_ink=True))
    font = GameAsciiFont.from_arm9(arm)
    transitions = []
    for frame, caption, box in ((5800, 'Discovered Inuvik.', (14, 290, 244, 320)),
            (6200, 'Dock at Inuvik?', (14, 290, 244, 325)),
            (7200, 'Resupply', (78, 223, 181, 251)), (8000, 'Resupply', (78, 223, 181, 251))):
        with Image.open(shots[frame]['path']) as screen:
            mask = dark_text(font, caption, screen.convert('RGB'), box)
        transitions.append(dict(frame=frame, screenshot=shots[frame], caption=mask))
    save(LIVE, dict(candidate_sha256=sha, actual_emulator_gameplay=True, hardware=False,
        fixture=fixture, observed_notice_IDs=[row['message_ID'] for row in seen], observed=seen,
        original_discovery_docking_resupply_and_menu_return=transitions,
        natural_travel=False, battle_choices_port_attacks_and_other_village_outcomes_offline=True,
        evidence={str(path): digest(path) for path in (PROOF, OUTPUT, terminal_path, Path(terminal['report']), Path(__file__))}))
    print('The original village discovery, docking, food and water report and menu return passed.')


def verify_startup():
    assert not BOOT.exists() and not CHECKPOINT.exists()
    staged, live, choices = map(load, (PROOF, LIVE, CHOICES))
    sha = digest(ROM)
    assert staged['research_ROM_sha256'] == live['candidate_sha256'] == choices['candidate_sha256'] == sha
    assert len(staged['stored']) == 67 and len(staged['all_substitution_layouts']) == 1024
    assert len(choices['original_caller_choice_cases']) == 32
    assert all(digest(path) == expected for path, expected in (staged['evidence'] | live['evidence'] | choices['evidence']).items())
    sheets = load(first.PROOF)['contact_sheets'] + staged['contact_sheets']
    assert all(digest(sheet['path']) == sheet['sha256'] for sheet in sheets)
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
        live_messages=live['observed_notice_IDs'], stored_cases=67, layout_cases=1024,
        fresh_viewed_pages=sum(len(sheet['messages']) for sheet in staged['contact_sheets']),
        reused_exact_viewed_pages=staged['reused_exact_viewed_pages'],
        native_selector_cases=staged['selector_scope']['tested'], crew_voice_choices=load(OUTPUT)['voice_cases'],
        evidence={str(path): digest(path) for path in (PROOF, first.PROOF, OUTPUT, BOOT, LIVE, CHOICES, QA, Path(__file__))}))
    print('Exact startup, six parent frame matches and 24 protected name getters passed.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=('choices', 'live', 'startup'))
    {'choices': verify_choices, 'live': verify_live, 'startup': verify_startup}[parser.parse_args().phase]()
