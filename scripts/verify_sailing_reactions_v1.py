"""Seal the visual review and verify the two original sailing event transitions."""

import argparse
from hashlib import sha256
from pathlib import Path
from struct import unpack_from
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree

from scripts import replay_sailing_reactions_v1 as replay
from scripts import verify_item_production_advice_v1 as precedent
from scripts.verify_captain_biographies_v1 import captured


stage = replay.stage
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
BIOGRAPHIES = replay.PRIOR.parent
BOOT, VISUAL = ROOT / 'own_startup_verification.json', ROOT / 'visual_layout_approval.json'
LIVE = ROOT / 'sailing_reactions_gameplay_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = Path('work/sailing_reactions_repo_qa_20261111.xml')
PAPER = (16, 296, 244, 360)
NAMEPLATE = (4, 273, 103, 289)


def verify_startup():
    loader = SimpleNamespace(load=stage.base.load, RELEASE=stage.parent.RELEASE, NdsImage=stage.NdsImage, ARM=stage.ARM)
    FunctionType(precedent.verify_startup.__code__, vars(precedent) | globals() | {'stage': loader})()


def approve_layout(viewed):
    base = stage.base
    assert not VISUAL.exists()
    proof = base.load(PROOF)
    assert base.digest(ROM) == proof['research_ROM_sha256']
    assert base.digest(stage.OUTPUT) == proof['manuscript_sha256']
    assert viewed == [row['sha256'] for row in proof['sheets']]
    assert all(base.digest(row['path']) == row['sha256'] for row in proof['sheets'])
    assert sum(len(row['messages']) for row in proof['sheets']) == proof['native_pages'] == len(proof['records']) == 53
    tests = list(ElementTree.parse(QA).iter('testsuite'))
    assert sum(int(row.get('tests', 0)) for row in tests) == 34
    assert all(int(row.get(key, 0)) == 0 for row in tests for key in ('errors', 'failures', 'skipped'))
    base.save(VISUAL, dict(candidate_sha256=proof['research_ROM_sha256'], native_records=53,
        native_pages=53, sheet_sha256=viewed, repository_tests=34,
        all_pages_viewed=True, complete_glyphs_and_bounds=True,
        evidence={str(p): base.digest(p) for p in (PROOF, stage.OUTPUT, QA, Path(__file__))},
        representative_gameplay_and_registration_pending=True, new_credit=0))
    print('Approved all 53 final portrait pages and 34 targeted tests.')


def verify_live():
    base = stage.base
    proof, visual, boot = map(base.load, (PROOF, VISUAL, BOOT))
    sha = base.digest(ROM)
    assert sha == proof['research_ROM_sha256'] == visual['candidate_sha256'] == boot['candidate_sha256']
    terminal_path = replay.ROOT / 'terminal.json'
    terminal = base.load(terminal_path)
    report_path, commands = Path(terminal['report']), Path(terminal['commands'])
    assert base.digest(report_path) == terminal['report_sha256']
    assert base.digest(commands) == terminal['commands_sha256']
    report = base.load(report_path)
    assert terminal['candidate_sha256'] == report['ROM_sha256'] == sha and report['frames'] == replay.END
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not any(value for key, value in report.items()
                   if key.startswith('synthetic_') and key != 'synthetic_condition_fixtures')
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    assert terminal['unchanged_original_save']
    frames = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('_navigation.png')}
    snapshots = {row['frame']: row for row in report['read_only_pause_RAM_snapshots']}
    assert set(frames) <= snapshots.keys()
    arm = stage.NdsImage.open(ROM).read_file(stage.ARM)
    addresses = [unpack_from('<I', arm, offset)[0] - stage.BASE for offset in (0x5444C, 0x54450)]

    def snapshot(frame):
        row = snapshots[frame]
        assert row['read_only_export'] and base.digest(row['path']) == row['sha256']
        raw = Path(row['path']).read_bytes()
        assert len(raw) == 0x400000
        return raw

    applied = []
    for frame, event in ((replay.PAUSE, 'wind'), (9900, 'whale')):
        _, fixture = replay.set_condition(arm, snapshot(frame), {'event': event})
        applied.append(fixture | {'frame': frame})
    assert report['synthetic_condition_fixtures'] == applied
    journal_path = report_path.with_name('navigation_command_journal.json')
    journal = base.load(journal_path)['commands_received']
    assert all(row['validation_passed'] for row in journal)
    assert [row['command'] for row in journal] == list(replay.COMMANDS)
    by_display = {row['display_hex']: row for row in proof['records']}
    observed = []
    for frame in sorted(frames):
        ram = snapshot(frame)
        template, display = [ram[at:at + 256].split(b'\0', 1)[0].hex() for at in addresses]
        if display not in by_display:
            continue
        row = by_display[display]
        screen = captured(frames[frame])
        ink = bytes(color == (0, 8, 0) for color in screen.crop(PAPER).get_flattened_data())
        if sha256(ink).hexdigest() != row['native_ink_sha256']:
            continue
        assert template == row['staged_hex']
        observed.append(dict(message_ID=row['message_ID'], frame=frame, visible_lines=row['visible_lines'],
            complete_glyphs=row['complete_glyphs'], native_ink_matches_live_foreground_and_blank_cells=True,
            captured_RAM=snapshots[frame], capture=frames[frame],
            nameplate_sha256=sha256(screen.crop(NAMEPLATE).tobytes()).hexdigest()))
    wind, first, second = observed
    assert 2454 <= wind['message_ID'] <= 2461 and wind['frame'] == 9700
    assert 2359 <= first['message_ID'] <= 2365 and 2462 <= second['message_ID'] <= 2468
    assert first['message_ID'] - 2359 == second['message_ID'] - 2462
    assert first['nameplate_sha256'] == second['nameplate_sha256']
    assert first['frame'] < second['frame'] < replay.END
    assert frames[replay.END]['framebuffer_sha256'] != second['capture']['framebuffer_sha256']
    assert frames[9900]['framebuffer_sha256'] != wind['capture']['framebuffer_sha256']
    fleet_offset = applied[0]['fleet'] - stage.BASE
    assert snapshot(9900)[fleet_offset + 0x2C] == snapshot(replay.END)[fleet_offset + 0x2C] == 27
    evidence = (PROOF, VISUAL, BOOT, terminal_path, report_path, commands, journal_path, QA, Path(__file__))
    ids = [row['message_ID'] for row in observed]
    base.save(LIVE, dict(candidate_sha256=sha, observed_ids=ids, observed=observed,
        actual_emulator=True, hardware=False, focused_condition_inputs=applied, natural_event_selection=False,
        original_wind_return=True, complete_white_whale_exchange=True, same_lookout_nameplate=True,
        original_A_advancement_and_return=True, return_to_sailing_capture=frames[replay.END],
        evidence={str(p): base.digest(p) for p in evidence}))
    base.save(CHECKPOINT, dict(candidate_sha256=sha, approved_for_registered_successor=True,
        live_messages=ids, stored_cases=53, viewed_pages=53,
        evidence={str(p): base.digest(p) for p in (*evidence, LIVE)}))
    print(f'Verified live reactions {ids}, complete whale exchange and original sailing return.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('startup', 'layout', 'live'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'layout':
        approve_layout(args.viewed_sheets)
    else:
        (verify_startup if args.action == 'startup' else verify_live)()
