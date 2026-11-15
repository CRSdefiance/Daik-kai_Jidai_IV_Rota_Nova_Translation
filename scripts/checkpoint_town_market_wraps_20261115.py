"""Verify staged dialogue against the rendered town and Market replay frames."""

from hashlib import sha256
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_town_market_wraps_20261115 as replay
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_market_gameplay_v753 import state as market_state
from scripts.verify_town_event_gameplay_v750 import state_fields as promoter_state


base, stage = replay.base, replay.stage
OUTPUT = stage.ROOT / 'gameplay_verification.json'
SHEET = stage.ROOT / 'gameplay_lower_screens.png'
HOLDS = {'promoter': {4600: 739, 4800: 739, 5000: 740},
         'specialty': {4200: 742, 4600: 742, 5000: 743, 5200: 743},
         'market': {5400: 748, 5600: 748}}
CONTROLS = {'promoter': (5400, 'Returned to the Square menu after accepting the ride.'),
            'specialty': (5800, 'Continued to the town news after agreeing to hand over Baby Shark.'),
            'market': (6200, 'Returned to Trade, Invest, and Market Info after dismissing the warning.')}


def mask(font, lines):
    return {(22 + 6 * column + x, 297 + 16 * row + y)
            for row, line in enumerate(lines) for column, char in enumerate(line)
            for glyph in (font.decode(char),) for x in range(6) for y in range(11) if glyph.getpixel((x, y))}


def item_availability(arm, raw):
    cpu = machine(arm)
    cpu.mem_write(BASE, raw)
    call(cpu, 0xCB190, ())
    item = cpu.reg_read(UC_ARM_REG_R0) + 4 + 4 * 20
    call(cpu, 0x4A224, (item,))
    return cpu.reg_read(UC_ARM_REG_R0)


def main():
    review, proof = map(base.load, (stage.MANUSCRIPT, stage.STORED))
    assert base.digest(stage.ROM) == review['candidate_sha256'] == proof['candidate_sha256']
    rom = base.NdsImage.open(stage.ROM)
    arm = rom.read_file(stage.ARM)
    font = GameAsciiFont.from_arm9(arm)
    lines = {row['message_ID']: row['visible_lines'] for row in review['records']}
    lines[742] = next(row['lines'] for row in review['specialty_title_arguments'] if row['values'] == ['Baby Shark', 'Caviar'])
    assert lines[742][0].endswith('Baby Shark?') and 'Caviar' in lines[742][1]
    evidence = {str(p): base.digest(p) for p in (stage.STORED, stage.MANUSCRIPT, SHEET, Path(__file__))}
    records, transitions = [], {}
    for case, chosen in HOLDS.items():
        root = stage.ROOT / case
        terminal_path = root / 'terminal.json'
        terminal = base.load(terminal_path)
        report_path = Path(terminal['report'])
        report = base.load(report_path)
        assert base.digest(report_path) == terminal['report_sha256']
        assert report['ROM_sha256'] == proof['candidate_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        reference, old, donor, expected_commands, _ = replay.history(case)
        assert base.digest(reference) == terminal['historical_sha256']
        assert base.digest(donor) == terminal['donor_sha256']
        assert report['scripted_input_schedule'] == old['scripted_input_schedule']
        journal = report_path.with_name('navigation_command_journal.json')
        commands = base.load(journal)['commands_received']
        assert [row['command'] for row in commands] == expected_commands
        assert all(row['validation_passed'] for row in commands)

        fixture = replay.CASES[case][5]
        assert not any(value for key, value in report.items() if key.startswith('synthetic_') and key != fixture)
        used, = report[fixture]
        ram = {}
        for row in report['read_only_pause_RAM_snapshots']:
            raw = Path(row['path']).read_bytes()
            assert row['read_only_export'] and len(raw) == 0x400000 and sha256(raw).hexdigest() == row['sha256']
            ram[row['frame']] = raw
            evidence[row['path']] = row['sha256']
        start, end = ram[3200], ram[report['frames']]
        request = expected_commands[0][next(key for key in expected_commands[0] if key.endswith('_fixture'))]
        modified, independent = replay.fixture_for(case, proof['target_ARM9_sha256'])(arm, start, request)
        assert used == independent | {'frame': 3200}
        if case == 'promoter':
            before, after = map(lambda raw: promoter_state(arm, raw), (start, end))
            assert (before['travel_flag'], after['travel_flag'], after['tracked_city']) == (0, 4, 22)
        elif case == 'specialty':
            before, after = map(lambda raw: item_availability(arm, raw), (modified, end))
            assert (before, after) == (4, 0)
        else:
            before, after = map(lambda raw: market_state(arm, raw), (modified, end))
            assert before == after and after['cash'] == after['share'] == 0
        frames = shots(report)
        for frame, n in chosen.items():
            shot = frames[frame]
            image = captured(shot)
            found = {(x, y) for x in range(16, 244) for y in range(294, 360) if image.getpixel((x, y)) == (0, 8, 0)}
            assert found == mask(font, lines[n]), (case, frame, n)
            records.append(dict(case=case, frame=frame, message_ID=n, visible_lines=lines[n], full_ink_pixels=len(found)))
            evidence[shot['path']] = shot['PNG_sha256']
        frame, observation = CONTROLS[case]
        control = frames[frame]
        captured(control)
        transitions[case] = dict(frame=frame, screen_observation=observation, original_state_before=before,
                                 original_state_after=after, setup_changed_RAM_bytes=len(used['changes']))
        evidence[control['path']] = control['PNG_sha256']
        evidence.update({str(p): base.digest(p) for p in (reference, report_path, terminal_path, journal)})

    data = dict(candidate_sha256=proof['candidate_sha256'], complete_holds=records, transitions=transitions,
        observed_changed_keys=[739, 743, 748], offline_only_changed_keys=[749],
        actual_emulator=True, earned_event_eligibility=False, hardware=False,
        visually_reviewed_sheet=str(SHEET), sheet_sha256=base.digest(SHEET), evidence=evidence)
    if OUTPUT.exists():
        assert base.load(OUTPUT) == data
    else:
        base.save(OUTPUT, data)
    print(f'{len(records)} complete visible glyph masks and all three original branch outcomes verified.')


if __name__ == '__main__':
    main()
