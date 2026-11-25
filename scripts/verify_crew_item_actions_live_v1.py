"""Verify refusal, expanded remedy text and normal transitions in the original Items menu."""

from hashlib import sha256
from json import loads
from pathlib import Path
from struct import unpack_from

from scripts import replay_crew_item_actions_v1 as refusal
from scripts import replay_crew_item_actions_v2 as success
from scripts import verify_crew_item_actions_v1 as checked
from scripts.verify_captain_biographies_v1 import captured


stage, base = refusal.stage, refusal.base
LIVE = stage.ROOT / 'crew_item_actions_gameplay_verification.json'
CHECKPOINT = stage.ROOT / 'approved_checkpoint.json'
PAPER = (16, 296, 244, 360)


def checked_replay(root, sha, stop_frame):
    terminal_path = root / 'terminal.json'
    terminal = base.load(terminal_path)
    report_path, commands = Path(terminal['report']), Path(terminal['commands'])
    assert base.digest(report_path) == terminal['report_sha256']
    assert base.digest(commands) == terminal['commands_sha256']
    report = base.load(report_path)
    assert terminal['candidate_sha256'] == report['ROM_sha256'] == sha
    assert report['frames'] == stop_frame and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and terminal['unchanged_original_save']
    assert {key for key, value in report.items() if key.startswith('synthetic_') and value} == {
        'synthetic_inventory_fixtures', 'synthetic_condition_fixtures'}
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    inventory, = report['synthetic_inventory_fixtures']
    item, = inventory['items']
    assert inventory['frame'] == 8327 and item['item_id'] == 23 and item['name'] == "Hua Tuo's Tonic"
    assert not inventory['normal_acquisition_verified']
    frames = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('_navigation.png')}
    snapshots = {row['frame']: row for row in report['read_only_pause_RAM_snapshots']}
    assert set(frames) <= snapshots.keys()
    journal_path = report_path.with_name('navigation_command_journal.json')
    journal = base.load(journal_path)['commands_received']
    assert all(row['validation_passed'] for row in journal)
    assert [row['command'] for row in journal] == [loads(line) for line in commands.read_text(encoding='utf-8').splitlines()]
    return report, frames, snapshots, (terminal_path, report_path, commands, journal_path)


def read_ram(snapshots, frame):
    row = snapshots[frame]
    assert row['read_only_export'] and base.digest(row['path']) == row['sha256']
    raw = Path(row['path']).read_bytes()
    assert len(raw) == 0x400000
    return raw


def main():
    proof, layout, boot = map(base.load, (stage.PROOF, checked.VISUAL, checked.BOOT))
    sha = base.digest(stage.ROM)
    assert sha == proof['research_ROM_sha256'] == layout['candidate_sha256'] == boot['candidate_sha256']
    arm = base.NdsImage.open(stage.ROM).read_file(stage.first.ARM)
    addresses = [unpack_from('<I', arm, offset)[0] - stage.first.BASE for offset in (0x5444C, 0x54450)]
    cases = [(row, display) for row in proof['records'] for display in row['displays']]
    observed, paths, fixtures = [], [], []
    for root, end, test_frame, set_fixture, selections, return_frame in (
        (refusal.ROOT, 11100, 9900, refusal.set_condition, ((9600, range(2505, 2509)), (10200, range(2512, 2516))), 10500),
        (success.ROOT, 10700, 9300, success.set_condition, ((9800, range(2509, 2512)),), 10100),
    ):
        report, frames, snapshots, run_paths = checked_replay(root, sha, end)
        paths.extend(run_paths)
        _, condition = set_fixture(arm, read_ram(snapshots, test_frame), {'event': 'remedy-condition'})
        assert report['synthetic_condition_fixtures'] == [condition | {'frame': test_frame}]
        fixtures.append(condition)
        assert frames[return_frame]['framebuffer_sha256'] != frames[selections[-1][0]]['framebuffer_sha256']
        assert frames[end]['framebuffer_sha256'] != frames[return_frame]['framebuffer_sha256']
        for frame, scope in selections:
            raw = read_ram(snapshots, frame)
            template, display_hex = (raw[at:at + 256].split(b'\0', 1)[0].hex() for at in addresses)
            image = captured(frames[frame])
            ink = sha256(bytes(pixel == (0, 8, 0) for pixel in image.crop(PAPER).get_flattened_data())).hexdigest()
            eligible = [(row, display) for row, display in cases if row['message_ID'] in scope
                        and display['display_hex'] == display_hex and display['native_ink_sha256'] == ink]
            assert eligible, (frame, bytes.fromhex(template), bytes.fromhex(display_hex))
            row, display = eligible[0]
            assert all(other['message_ID'] == row['message_ID'] for other, _ in eligible)
            expected_input = display['native'].get('input_hex', row['staged_hex'])
            assert template == expected_input, (frame, bytes.fromhex(template), bytes.fromhex(expected_input))
            observed.append(dict(message_ID=row['message_ID'], frame=frame, lines=display['visible_lines'],
                item_name=display['item_name'], native_ink_and_blank_cells_match=True,
                capture=frames[frame], RAM=snapshots[frame]))
        if root == success.ROOT:
            offset = condition['fleet'] - stage.first.BASE + 0x2C
            assert read_ram(snapshots, 9800)[offset] == 27
            assert "Hua Tuo's Tonic" in ' '.join(observed[-1]['lines'])
    evidence = {str(path): base.digest(path) for path in (
        stage.PROOF, checked.VISUAL, checked.BOOT, checked.QA, Path(__file__), *paths)}
    ids = [row['message_ID'] for row in observed]
    base.save(LIVE, dict(candidate_sha256=sha, observed_ids=ids, observed=observed,
        actual_emulator=True, hardware=False, fixture_inventory=[23], condition_inputs=fixtures,
        original_item_use_and_return=True, no_need_and_unavailable_replies=True,
        successful_long_name_substitution=True, evidence=evidence))
    base.save(CHECKPOINT, dict(candidate_sha256=sha, approved_for_registered_successor=True,
        live_messages=ids, stored_cases=33, viewed_pages=40, evidence=evidence | {str(LIVE): base.digest(LIVE)}))
    print(f'Original item use and returns verified for {ids}.')


if __name__ == '__main__':
    main()
