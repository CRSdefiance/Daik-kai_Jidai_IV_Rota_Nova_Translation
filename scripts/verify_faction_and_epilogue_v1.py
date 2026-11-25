"""Verify all four original epilogue panels and the Game Over transition."""

import argparse
import inspect
from pathlib import Path
import struct
import xml.etree.ElementTree as ET

from PIL import ImageChops

from dk4tool.patch.faction_and_epilogue_wrap_v1 import PRIOR, SCOPE
from dk4tool.patch.equipment_removal_wrap_v1 import EQUIPMENT_PARAGRAPH, HOOK, NOTICE_PARENT
from dk4tool.rom.nds import NdsImage
from scripts import stage_faction_and_epilogue_v2 as stage
from scripts import verify_setup_save_equipment_v1 as precedent
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_shared_notice_storage_v1 import checked_report
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.native_machine_scoped_v764 import machine
from scripts.register_discovery_rewards_v1 import RELEASE
from scripts.replay_faction_and_epilogue_v1 import ARM, BASELINE, FINAL, HOLDS, INPUT, PAUSE, PRESSES, PRIOR as DISCOVERY
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_discovery_rewards_v1 import complete_notice, PAPER
from scripts.verify_shared_crew_selector_v1 import ARGS, dispatch


ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
LIVE = ROOT / 'faction_and_epilogue_gameplay_verification.json'
BOOT = ROOT / 'own_startup_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = Path('work/faction_and_epilogue_repo_qa_20261111.xml')


def replay_report(root, expected):
    folder = root / 'epilogue'
    path, terminal_path = folder / 'capture/capture_report.json', folder / 'terminal.json'
    terminal = load(terminal_path)
    assert terminal['candidate_sha256'] == expected and terminal['report_sha256'] == digest(path)
    assert terminal['prior_capture_sha256'] == digest(INPUT) and not terminal['earned_ending']
    report, _ = checked_report(path, expected, FINAL)
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot']
    assert digest(donor['source']) == donor['source_sha256'] == terminal['unchanged_donor_sha256']
    assert report['scripted_input_schedule'] == load(folder / 'inputs.json')
    fixture, = report['synthetic_ending_fixtures']
    assert fixture['frame'] == PAUSE and fixture['only_two_state_bytes_changed']
    assert (fixture['requested_state'], fixture['requested_substate'], fixture['actual_captain']) == (3, 1, 1)
    assert fixture['original_epilogue_entry'] == 0x0203E208
    assert fixture['changes'] == [
        dict(address=0x022796BC, before=1, after=3), dict(address=0x022796C4, before=0, after=1)]
    assert not any(value for key, value in report.items()
                   if key.startswith('synthetic_') and key != 'synthetic_ending_fixtures')
    return report, (path, terminal_path)


def native_cases(arm):
    cpu = machine(arm)
    cases = [(NOTICE_PARENT, n, EQUIPMENT_PARAGRAPH) for n in SCOPE]
    cases.extend((parent, n, PRIOR) for parent, n in (
        (0x0205473C, 342), (0x02054764, 334), (NOTICE_PARENT, 335),
        (NOTICE_PARENT, 337), (NOTICE_PARENT, 341), (NOTICE_PARENT, 346), (NOTICE_PARENT, 288)))
    proof = []
    for parent, n, expected in cases:
        target, regs = dispatch(cpu, HOOK, {0xC4: parent, 0xD0: n}, (PRIOR, EQUIPMENT_PARAGRAPH))
        assert target == expected and regs[:3] == ARGS[:3]
        proof.append(dict(parent=parent, message_ID=n, continuation=target))
    return proof


def verify_live():
    proof, parent = map(load, (PROOF, RELEASE))
    assert digest(ROM) == proof['research_ROM_sha256']
    baseline, old_evidence = replay_report(BASELINE, parent['candidate_sha256'])
    report, new_evidence = replay_report(ROOT, proof['research_ROM_sha256'])
    for key in ('scripted_input_schedule', 'core_options', 'synthetic_ending_fixtures'):
        assert baseline[key] == report[key]
    assert report['scripted_input_schedule'][-4:] == [dict(start=n, duration=8, buttons=['A']) for n in PRESSES]
    old, new = shots(baseline), shots(report)
    assert old[PAUSE]['framebuffer_sha256'] == new[PAUSE]['framebuffer_sha256']
    assert all(old[n]['framebuffer_sha256'] == new[n]['framebuffer_sha256'] for n in HOLDS[4:])
    arm = NdsImage.open(ROM).read_file(ARM)
    expanded_at, display_at = (value - 0x02000000 for value in struct.unpack_from('<2I', arm, 0x54890))
    snapshots = {row['frame']: row for row in report['read_only_capture_RAM_snapshots']}
    observed = []
    for n, frame in zip(range(342, 346), HOLDS[:4], strict=True):
        args = ['Bergstrom Fleet', 'Hodram Joakim Bergstrom'] if n == 342 else []
        match = complete_notice(new[frame], proof, n, args)
        variant, = [row for row in proof['rendered_variants'] if row['message_ID'] == n and row['arguments'] == args]
        snap = snapshots[frame]
        assert snap['read_only_export'] and digest(snap['path']) == snap['sha256']
        raw = Path(snap['path']).read_bytes()
        for addr, field in ((expanded_at, 'expanded_hex'), (display_at, 'native_wrapper_output_hex')):
            assert raw[addr:addr + 256].split(b'\0', 1)[0] == bytes.fromhex(variant[field]), (n, field)
        bounds = ImageChops.difference(captured(old[frame]), captured(new[frame])).getbbox()
        assert bounds and PAPER[0] <= bounds[0] < bounds[2] <= PAPER[2]
        assert PAPER[1] <= bounds[1] < bounds[3] <= PAPER[3]
        observed.append(match | dict(snapshot=snap, exact_original_format_buffers=True,
            previous_capture=old[frame], changed_bounds=list(bounds)))
    save(LIVE, dict(candidate_sha256=digest(ROM), observed_ids=[342, 343, 344, 345],
        original_panel_holds=observed, original_A_dismissals=list(PRESSES),
        original_game_over_return=[new[n] for n in HOLDS[4:]],
        original_pre_fixture_frame=new[PAUSE], fixture=report['synthetic_ending_fixtures'][0],
        selector_positive_and_negative_cases=native_cases(arm), hardware=False,
        evidence={str(path): digest(path) for path in (PROOF, *old_evidence, *new_evidence, Path(__file__))}))
    print('All four original epilogue pages and the Game Over transition passed.')


def verify_startup():
    code = checked_text(inspect.getsource(precedent.verify_startup), {
        "parent_path = BIOGRAPHIES / 'own_startup/capture/capture_report.json'":
            "parent_path = DISCOVERY / 'own_startup/capture/capture_report.json'",
        "prior_proof = BIOGRAPHIES / 'own_startup_verification.json'":
            "prior_proof = DISCOVERY / 'own_startup_verification.json'",
    })
    env = {**vars(precedent), **globals()}
    exec(compile(code, __file__ + '::same-cold-boot-and-name-contract', 'exec'), env)
    env['verify_startup']()


def approve(viewed):
    assert not CHECKPOINT.exists()
    proof, live, startup = map(load, (PROOF, LIVE, BOOT))
    assert viewed == [sheet['sha256'] for sheet in proof['sheets']]
    assert all(digest(sheet['path']) == sheet['sha256'] for sheet in proof['sheets'])
    assert proof['research_ROM_sha256'] == live['candidate_sha256'] == startup['candidate_sha256'] == digest(ROM)
    suites = list(ET.parse(QA).getroot().iter('testsuite'))
    assert sum(int(row.get('tests', 0)) for row in suites) == 30
    assert all(int(row.get(key, 0)) == 0 for row in suites for key in ('errors', 'failures', 'skipped'))
    save(CHECKPOINT, dict(candidate_sha256=digest(ROM), approved_for_registered_successor=True,
        observed_ids=live['observed_ids'], stored_records=len(proof['records']),
        viewed_pages=sum(sheet['pages'] for sheet in proof['sheets']),
        evidence={str(path): digest(path) for path in (PROOF, LIVE, BOOT, QA, Path(__file__))}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('live', 'startup', 'approve'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'approve':
        approve(args.viewed_sheets)
    elif args.action == 'live':
        verify_live()
    else:
        verify_startup()
