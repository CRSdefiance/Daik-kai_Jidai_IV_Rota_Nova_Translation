"""Verify the actual town prompt, its two branches and the special-name source."""

import argparse
from hashlib import sha256
from json import loads
from pathlib import Path
from struct import unpack_from
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R5, UC_ARM_REG_SP

from scripts import replay_battle_commands_and_outcomes_v1 as replay
from scripts import verify_city_combat_notices_live_v1 as city
from scripts import verify_item_production_advice_v1 as startup
from scripts.probe_button_prompt_native import STACK, STOP
from scripts.verify_personal_gameplay_v841 import get_machine


stage, base = replay.stage, replay.base
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
BIOGRAPHIES = replay.prior.STARTUP.parent
BOOT, VISUAL = ROOT / 'own_startup_verification.json', ROOT / 'visual_layout_review.json'
LIVE, CHECKPOINT = ROOT / 'battle_commands_and_outcomes_gameplay_verification.json', ROOT / 'approved_checkpoint.json'
QA = Path('work/battle_commands_and_outcomes_repo_qa_20261111.xml')
review, portrait, names = stage.first.review, stage.first.first.portrait, stage.first.names
HISTORICAL_MONSTER = Path('work/analysis/inspection_status_actual_verified_v1583/both_original_status_paths_native_RGB_and_transitions.json')


def special_provider(arm, binding):
    old = base.load(HISTORICAL_MONSTER)
    inspection = next(row for row in old['paths'] if row['message_ID'] == 306)['audit']
    report_path = Path(inspection['terminal_report'])
    assert base.digest(report_path) == inspection['terminal_report_sha256']
    report = base.load(report_path)
    assert report['ROM_sha256'] == old['candidate_sha256']
    snapshot = next(row for row in report['read_only_pause_RAM_snapshots'] + report['read_only_capture_RAM_snapshots']
                    if row['frame'] == 5800)
    raw = Path(snapshot['path']).read_bytes()
    assert len(raw) == 0x400000 and sha256(raw).hexdigest() == snapshot['sha256']
    at = names.CALL - review.BASE
    source = base.NdsImage.open(review.CLEAN).read_file(review.ARM)
    assert raw[0x71D74:at + 4] == source[0x71D74:at + 4] and arm[0x71D74:at] == source[0x71D74:at]
    assert raw[at:at + 4].hex() == binding['original_call_hex'] and arm[at:at + 4].hex() == binding['localized_call_hex']
    cpu, get = get_machine(arm, raw[:at] + arm[at:at + 4] + raw[at + 4:])
    fleet = get(0xCB1A8) + 4 + 39 * 132
    mobile = get(0x36C70, fleet + 12)
    model = get(0x36C94, fleet + 12)
    assert mobile and model == get(0xCB148) + 4 + 149 * 140
    assert get(0xAB128, mobile) == 34
    seen = {}

    def observe(u, pc, size, unused):
        ptr = u.reg_read(UC_ARM_REG_R2)
        value = bytes(u.mem_read(ptr, 24)).split(b'\0', 1)[0]
        if pc == names.CALL:
            assert ptr == model + 8 and value == '化魚'.encode('cp932')
            seen.update(original_pointer=ptr, original_name_hex=value.hex())
        else:
            arguments = u.reg_read(UC_ARM_REG_R0), u.reg_read(UC_ARM_REG_R1)
            assert arguments == (1, names.TABLE), tuple(hex(n) for n in arguments)
            assert u.reg_read(UC_ARM_REG_LR) == names.CALL + 4 and value == b'Monster Fish'
            seen.update(localized_pointer=ptr, localized_name=value.decode('ascii'))
            u.emu_stop()

    for pc in (names.CALL, names.WRAPPER):
        cpu.hook_add(UC_HOOK_CODE, observe, begin=pc, end=pc)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_LR, STOP)
    cpu.reg_write(UC_ARM_REG_R5, 0)
    cpu.emu_start(review.BASE + 0x71D74, STOP, count=20000)
    assert cpu.reg_read(UC_ARM_REG_PC) == names.WRAPPER and len(seen) == 4
    assert bytes(cpu.mem_read(model, 140)) == raw[model - review.BASE:model - review.BASE + 140]
    return seen | dict(snapshot=snapshot, model_ID=149, supplied_original_handler_mode=0, exact_original_getter_executed=True,
        only_new_call_bytes_in_historical_CPU_copy=True, no_special_defeat_seen_in_gameplay=True)


def approve_layout(viewed):
    assert not VISUAL.exists()
    proof = base.load(PROOF)
    assert base.digest(ROM) == proof['research_ROM_sha256'] and base.digest(stage.OUTPUT) == proof['manuscript_sha256']
    assert viewed == [row['sha256'] for row in proof['sheets']]
    assert all(base.digest(row['path']) == row['sha256'] for row in proof['sheets'])
    assert len(proof['records']) == 29 and proof['native_pages'] == proof['native_cases'] == 65
    assert sum(len(row['messages']) for row in proof['sheets']) == 65
    modal = [case for case in proof['records'] if 2122 <= case['message_ID'] <= 2129]
    assert len(modal) == 8 and all(len(row['visible_lines']) == 1 and row['visible_lines'][0].endswith('?')
                                  for case in modal for row in case['displays'])
    suites = list(ElementTree.parse(QA).iter('testsuite'))
    assert sum(int(row.get('tests', 0)) for row in suites) == 34
    assert all(int(row.get(key, 0)) == 0 for row in suites for key in ('errors', 'failures', 'skipped'))
    assert len(proof['ownership']['target_name_controls']) == 10
    arm = base.NdsImage.open(ROM).read_file(review.ARM)
    original_provider = special_provider(arm, proof['ownership']['target_names'])
    base.save(VISUAL, dict(candidate_sha256=proof['research_ROM_sha256'], stored_cases=29, native_pages=65,
        all_pages_viewed=True, complete_glyphs_and_bounds=True, repository_tests=34,
        all_tested_town_names_and_questions_on_one_line=True,
        special_target_original_offline_provider=original_provider, sheet_sha256=viewed,
        evidence={str(path): base.digest(path) for path in (PROOF, stage.OUTPUT, QA, Path(__file__))},
        representative_gameplay_and_registration_pending=True, new_credit=0))
    print('Approved 65 viewed pages, 10 scoped name controls, the original Monster Fish provider, and 34 tests.')


def verify_startup():
    loader = SimpleNamespace(load=base.load, RELEASE=review.parent.RELEASE, NdsImage=base.NdsImage, ARM=review.ARM)
    FunctionType(startup.verify_startup.__code__, vars(startup) | globals() | {'stage': loader, 'startup': startup.startup})()
    proof, deployed = map(base.load, (PROOF, BOOT))
    raw = Path(deployed['read_only_snapshot']['path']).read_bytes()
    at = names.CALL - review.BASE
    assert raw[at:at + 4].hex() == proof['ownership']['target_names']['localized_call_hex']
    base.save(BOOT, deployed | {'resident_main_RAM_special_target_call_exact': True})


def verify_gameplay():
    assert not LIVE.exists() and not CHECKPOINT.exists()
    proof, layout, boot = map(base.load, (PROOF, VISUAL, BOOT))
    sha = base.digest(ROM)
    assert sha == proof['research_ROM_sha256'] == layout['candidate_sha256'] == boot['candidate_sha256']
    rom = base.NdsImage.open(ROM)
    arm = rom.read_file(review.ARM)
    raster, _, _ = portrait.font_tools(rom)
    kanji = rom.read_file('/GRP/KANJI.FNT')
    wrapped = unpack_from('<I', arm, 0x54450)[0] - review.BASE
    row = next(case for case in proof['records'] if case['message_ID'] == 2123)
    expected = next(case for case in row['displays'] if case['visible_lines'] == ['Attack Sao Tome?'])
    observations, inputs = [], [PROOF, VISUAL, BOOT, QA, Path(__file__)]
    for action in ('accept', 'cancel'):
        root = ROOT / f'town_attack_{action}'
        terminal_path = root / 'terminal.json'
        terminal = base.load(terminal_path)
        report_path, commands = Path(terminal['report']), Path(terminal['commands'])
        assert base.digest(report_path) == terminal['report_sha256'] and base.digest(commands) == terminal['commands_sha256']
        assert terminal['unchanged_original_save'] and base.digest(replay.DONOR) == replay.DONOR_SHA
        report = base.load(report_path)
        assert report['ROM_sha256'] == sha and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not any(value for key, value in report.items() if key.startswith('synthetic_')
                       and key != 'synthetic_battle_recovery_proximity_fixtures')
        donor = report['battery_save_preloaded']
        assert donor['copied_byte_exact_before_cold_boot'] and donor['source_sha256'] == replay.DONOR_SHA
        journal = report_path.with_name('navigation_command_journal.json')
        received = base.load(journal)['commands_received']
        assert all(row['validation_passed'] for row in received)
        assert [row['command'] for row in received] == [loads(line) for line in commands.read_text(encoding='utf-8').splitlines()]
        frames = {item['frame']: item for item in report['frames_captured'] if item['path'].endswith('_navigation.png')}
        snapshots = {item['frame']: item for item in report['read_only_pause_RAM_snapshots']}

        def snapshot(frame):
            item = snapshots[frame]
            assert item['read_only_export'] and base.digest(item['path']) == item['sha256']
            raw = Path(item['path']).read_bytes()
            assert len(raw) == 0x400000
            return raw

        before = snapshot(5000)
        _, receipt = replay.fixture_for_candidate()(arm, before, {'town_context': 'SaoTomeFirstMate'})
        assert report['synthetic_battle_recovery_proximity_fixtures'] == [receipt | {'frame': 5000}]
        assert receipt['First_Mate_existing_actor_ID'] == 16
        hold = snapshot(5810)
        text = hold[wrapped:wrapped + 256].split(b'\0', 1)[0]
        assert text.hex() == expected['display_hex']
        cpu, get = get_machine(arm, hold)
        assert get(0x82478, get(0xCB1A8) + 0x2090, 1) == 16
        assert get(0x53F4C, get(0xCB184) + 4 + 16 * 32, 0x02117D20) == 2123
        pixels, glyphs = portrait.render_portrait(raster, arm, kanji, text)
        modal = city.captured(frames[5810])
        ink = bytes(pixel == (0, 8, 0) for pixel in modal.crop(city.PAPER).get_flattened_data())
        assert ink == bytes(bool(pixel) for pixel in pixels) and len(glyphs) == expected['complete_glyphs']
        assert sha256(pixels).hexdigest() == expected['native_ink_sha256']
        after = snapshot(5910)
        cpu, get = get_machine(arm, after)
        world = get(0xCB19C)
        state = list(unpack_from('<3I', cpu.mem_read(get(0x3F0F8) + 8, 12)))
        town = unpack_from('<I', cpu.mem_read(world + 0x1360, 4))[0]
        assert (state, town) == (([0, 1, 64], 73) if action == 'accept' else ([0, 0, 0], 115)), (action, state, town)
        assert city.captured(frames[5910]).crop(city.PAPER).tobytes() != modal.crop(city.PAPER).tobytes()
        observations.append(dict(action=action, message_ID=2123, frame=5810, text='Attack Sao Tome?',
            selected_actor_ID=16, complete_glyphs=len(glyphs), modal_capture=frames[5810], after_capture=frames[5910],
            modal_RAM=snapshots[5810], after_RAM=snapshots[5910], state=state, town_ID=town, fixture=receipt))
        inputs.extend((terminal_path, report_path, commands, journal))
    assert observations[0]['modal_capture']['framebuffer_sha256'] == observations[1]['modal_capture']['framebuffer_sha256']
    bindings = {str(path): base.digest(path) for path in inputs}
    base.save(LIVE, dict(candidate_sha256=sha, observed_ids=[2123], observations=observations,
        actual_emulator=True, hardware=False, native_accept_and_cancel=True,
        ram_and_defeat_messages_offline=True, evidence=bindings))
    base.save(CHECKPOINT, dict(candidate_sha256=sha, approved_for_registered_successor=True,
        live_messages=[2123], stored_cases=29, viewed_pages=65, evidence=bindings | {str(LIVE): base.digest(LIVE)}))
    print('Both original Sao Tome confirmation transitions and the whole displayed text passed.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('layout', 'startup', 'gameplay'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'layout':
        approve_layout(args.viewed_sheets)
    else:
        {'startup': verify_startup, 'gameplay': verify_gameplay}[args.action]()
