"""Verify complete visible Square dialogue and the original replay outcomes."""

from hashlib import sha256
from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_square_samples_wraps_20261115 as replay
from scripts.checkpoint_town_market_wraps_20261115 import mask
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_giveaway_gameplay_v746 import cargo


base, stage = replay.base, replay.stage
OUTPUT = stage.ROOT / 'gameplay_verification.json'
SHEET = stage.ROOT / 'gameplay_lower_screens.png'
VIEWED_SHEET = 'eb7b6da30b5aa3ff76222c9eb34f25fe43636cf5aacc5b8fe7b8d503928fed26'
SHOP = stage.MANUSCRIPT.with_name('istanbul_shop_observed_consumers_20261114_v1.json')
HOLDS = {'samples': {4800: 665, 5200: 665, 6800: 673, 7200: 674},
         'epidemic': {5600: 657, 5900: 683}}
TRANSITIONS = {'samples': {8000: 'Returned to the shop list after the customer tried the sample.'},
               'epidemic': {6050: 'Returned to the shop list.', 6150: 'Selected the Trends prompt.',
                            6250: 'Returned to town at the Square.', 6400: 'Moved the town cursor to Port.'}}


def main():
    review, proof = map(base.load, (stage.MANUSCRIPT, stage.STORED))
    assert base.digest(stage.ROM) == review['candidate_sha256'] == proof['candidate_sha256']
    arm = base.NdsImage.open(stage.ROM).read_file(stage.ARM)
    assert sha256(arm).hexdigest() == proof['target_ARM9_sha256']
    font = GameAsciiFont.from_arm9(arm)
    lines = {row['message_ID']: row['visible_lines'] for row in review['records']}
    normal = next(row for row in base.load(SHOP)['observed_shop_dialogue'] if row['id'] == 'COMMON_MESSAGE_657')
    lines[657] = [line.strip() for line in normal['English'].splitlines()]
    evidence = {str(p): base.digest(p) for p in (stage.STORED, stage.MANUSCRIPT, SHOP, SHEET, Path(__file__))}
    assert evidence[str(SHEET)] == VIEWED_SHEET
    complete, transitions, outcomes = [], [], {}
    for case, selected in HOLDS.items():
        reference, prior, donor, expected_frames = replay.history(case)
        _, command_key, fixture_key, _ = replay.CASES[case]
        root = stage.ROOT / case
        terminal_path = root / 'terminal.json'
        terminal = base.load(terminal_path)
        report_path = Path(terminal['report'])
        report = base.load(report_path)
        assert terminal['report_sha256'] == base.digest(report_path)
        assert terminal['historical_sha256'] == base.digest(reference)
        assert terminal['source_save_sha256'] == base.digest(donor) and terminal['original_save_unchanged']
        save = report['battery_save_preloaded']
        assert save['copied_byte_exact_before_cold_boot'] and save['source_sha256'] == base.digest(donor)
        assert report['ROM_sha256'] == proof['candidate_sha256'] and report['frames'] == prior['frames']
        assert report['scripted_input_schedule'] == prior['scripted_input_schedule']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not any(v for k, v in report.items() if k.startswith('synthetic_') and k != fixture_key)
        used, = report[fixture_key]
        journal = report_path.with_name('navigation_command_journal.json')
        received = base.load(journal)['commands_received']
        request = True if case == 'samples' else {'town': 22, 'condition': 1, 'days': 30}
        assert [row['command'] for row in received] == [
            {'until': report['frames'], command_key: request}, {'stop': True}]
        assert all(row['validation_passed'] for row in received)
        ram = {}
        for row in report['read_only_pause_RAM_snapshots']:
            data = Path(row['path']).read_bytes()
            assert row['read_only_export'] and len(data) == 0x400000
            assert sha256(data).hexdigest() == row['sha256']
            ram[row['frame']] = data
            evidence[row['path']] = row['sha256']
        fixture = replay.sample_fixture() if case == 'samples' else replay.epidemic
        modified, verified = fixture(arm, ram[3200], request)
        assert used == verified | {'frame': 3200}
        if case == 'samples':
            counts = [cargo(arm, raw) for raw in (ram[3200], modified, ram[report['frames']])]
            assert counts == [2, 2, 0] and len(used['changes']) == 3
            outcomes[case] = {'cargo_before_fixture_after_fixture_after_giveaway': counts, 'setup_changed_RAM_bytes': 3}
        else:
            assert used['original_shop_selection'] == 683 and len(used['changes']) == 2
            outcomes[case] = {'original_shop_selection': 683, 'setup_changed_RAM_bytes': 2}

        frames = shots(report)
        assert set(expected_frames) == set(selected) | set(TRANSITIONS[case])
        for frame, n in selected.items():
            shot = frames[frame]
            img = captured(shot)
            ink = {(x, y) for x in range(16, 244) for y in range(294, 360)
                   if img.getpixel((x, y)) == (0, 8, 0)}
            assert ink == mask(font, lines[n]), (case, frame, n)
            complete.append(dict(case=case, frame=frame, message_ID=n, visible_lines=lines[n], full_ink_pixels=len(ink)))
            evidence[shot['path']] = shot['PNG_sha256']
        for frame, observation in TRANSITIONS[case].items():
            shot = frames[frame]
            captured(shot)
            transitions.append(dict(case=case, frame=frame, observation=observation))
            evidence[shot['path']] = shot['PNG_sha256']
        evidence.update({str(p): base.digest(p) for p in (reference, report_path, terminal_path, journal)})
    data = dict(candidate_sha256=proof['candidate_sha256'], complete_holds=complete, transitions=transitions,
        original_outcomes=outcomes, observed_changed_keys=[665, 673, 683], offline_only_changed_keys=[659, 661, 667, 672, 684, 687],
        actual_emulator=True, earned_Chapel_assignment_or_epidemic=False, hardware=False,
        visually_reviewed_sheet=str(SHEET), sheet_sha256=VIEWED_SHEET, evidence=evidence)
    if OUTPUT.exists():
        assert base.load(OUTPUT) == data
    else:
        base.save(OUTPUT, data)
    print(f'{len(complete)} complete dialogue masks, {len(transitions)} transitions, and both original outcomes verified.')


if __name__ == '__main__':
    main()
