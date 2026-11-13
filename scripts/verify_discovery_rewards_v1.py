"""Verify discovery and reward panels against the original gameplay and startup."""

import argparse
import inspect
from hashlib import sha256
from pathlib import Path
from types import FunctionType
import xml.etree.ElementTree as ET

from PIL import ImageChops

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.discovery_reward_wrap_v1 import PRIOR, SCOPE, previous as paragraph
from dk4tool.rom.nds import NdsImage
from scripts import stage_discovery_rewards_v1 as stage
from scripts import verify_setup_save_equipment_v1 as precedent
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_shared_notice_storage_v1 import checked_report
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.native_machine_scoped_v764 import machine
from scripts.record_navigation_v327 import dark_text
from scripts.replay_discovery_rewards_v1 import ROOT as BASELINE, SHIPYARD
from scripts.run_sea_approach_village_replay_v1 import REFERENCE, relocate
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_shared_crew_selector_v1 import ARGS, dispatch


ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
LIVE = ROOT / 'discovery_rewards_gameplay_verification.json'
BOOT = ROOT / 'own_startup_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = Path('work/discovery_rewards_repo_qa_20261111.xml')
PAPER = (16, 296, 244, 344)


def load_pair(case, proof):
    runs, evidence = [], []
    for root, expected in ((BASELINE, proof['registered_input']['candidate_sha256']),
                           (ROOT, proof['research_ROM_sha256'])):
        folder = root / case
        report_path = folder / 'capture/capture_report.json'
        terminal_path = folder / 'terminal.json'
        terminal = load(terminal_path)
        assert terminal['candidate_sha256'] == expected
        report, raw = checked_report(report_path, expected, 8000)
        donor = report['battery_save_preloaded']
        assert donor['copied_byte_exact_before_cold_boot']
        assert digest(donor['source']) == donor['source_sha256']
        runs.append((report, raw, terminal))
        evidence.extend((report_path, terminal_path))
    old, new = (entry[0] for entry in runs)
    assert old['scripted_input_schedule'] == new['scripted_input_schedule']
    assert old['core_options'] == new['core_options']
    assert old['battery_save_preloaded']['source_sha256'] == new['battery_save_preloaded']['source_sha256']
    return runs, evidence


def complete_notice(shot, proof, number, args):
    row, = [entry for entry in proof['rendered_variants']
            if entry['message_ID'] == number and entry['arguments'] == args]
    fg = bytes(pixel == (0, 8, 0) for pixel in captured(shot).crop(PAPER).get_flattened_data())
    assert sha256(fg).hexdigest() == row['native_ink_sha256'], (number, shot['frame'])
    return dict(message_ID=number, arguments=args, lines=row['lines'], capture=shot,
                complete_ink_and_blank_mask=True, ink_pixels=fg.count(1))


def verify_auto(proof, arm, font):
    pair, evidence = load_pair('auto', proof)
    for report, _, terminal in pair:
        assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
        assert all(digest(path) == expected for path, expected in terminal['evidence'].items())
    old, auto = (shots(entry[0]) for entry in pair)
    report, raw, trace = pair[1]
    assert trace['target_requests'] == pair[0][2]['target_requests']
    assert {(row['message_ID'], row['frame'], row['PC']) for row in trace['target_requests']} == {
        (298, 7301, 0x0205528C), (298, 7301, 0x020534F4)}
    assert report['scripted_input_schedule'][-2:] == [
        dict(start=7301, duration=8, buttons=['B']), dict(start=7361, duration=8, buttons=['A'])]
    assert all(old[frame]['framebuffer_sha256'] == auto[frame]['framebuffer_sha256']
               for frame in (6800, 7200, 7300, 7600, 8000))
    match = complete_notice(auto[7350], proof, 298, [])
    bounds = ImageChops.difference(captured(old[7350]), captured(auto[7350])).getbbox()
    assert bounds and PAPER[0] <= bounds[0] < bounds[2] <= PAPER[2]
    assert PAPER[1] <= bounds[1] < bounds[3] <= PAPER[3]
    match['changed_bounds'] = list(bounds)
    active_caption = find_mask(font, 'Stop Auto Move', captured(auto[7300]), (160, 365, 256, 384))
    manual = captured(auto[7600])
    manual_footer = [find_mask(font, name, manual, (0, 364, 256, 384))
                     for name in ('Rotate', 'Menu', 'Inspect', 'Sails')]
    cpu, get = get_machine(arm, raw)
    assert get(0x82C4C, get(0xCB1A8) + 0x2090, 1) == 0
    assert bytes(cpu.mem_read(stage.BASE, len(raw))) == raw
    return dict(stop_question=match, original_request_trace=trace['target_requests'],
                original_auto_move_footer=dict(capture=auto[7300], stop_caption=active_caption),
                confirmed_manual_footer=dict(capture=auto[7600], glyphs=manual_footer),
                native_automatic_flag_cleared=True, fixture_scope='Isolated ordinary Riga battery save and controller/stylus inputs',
                no_choice_branch_observed=False), evidence


def verify_village(proof, font):
    pair, evidence = load_pair('village_resupply', proof)
    frames = []
    registered_rom = Path(load(stage.RELEASE)['candidate'])
    for root, rom, (report, _, terminal) in zip((BASELINE, ROOT), (registered_rom, ROM), pair, strict=True):
        assert digest(terminal['report']) == terminal['report_sha256']
        assert terminal['prior_capture'] == str(REFERENCE) and digest(REFERENCE) == terminal['prior_capture_sha256']
        assert terminal['unchanged_donor_sha256'] == report['battery_save_preloaded']['source_sha256']
        assert report['scripted_input_schedule'] == load(root / 'village_resupply/inputs.json')
        assert not any(value for key, value in report.items()
                       if key.startswith('synthetic_') and key != 'synthetic_location_fixtures')
        snapshot, = [row for row in report['read_only_pause_RAM_snapshots'] if row['frame'] == 5200]
        assert snapshot['read_only_export'] and digest(snapshot['path']) == snapshot['sha256']
        replay_fixture = FunctionType(relocate.__code__, relocate.__globals__ | {'ROM': rom})
        arm = NdsImage.open(rom).read_file(stage.ARM)
        _, fixture = replay_fixture(arm, Path(snapshot['path']).read_bytes(), 0)
        assert report['synthetic_location_fixtures'] == [fixture | {'frame': 5200}]
        frames.append({row['frame']: row for row in report['frames_captured']
                       if row['path'].endswith('_navigation.png')})
    old, new = frames
    assert old.keys() == new.keys()
    assert all(old[n]['framebuffer_sha256'] == new[n]['framebuffer_sha256'] for n in new)
    discovery = complete_notice(new[5800], proof, 297, ['Inuvik'])
    transitions = []
    for frame, caption, box in (
        (6200, 'Dock at Inuvik?', (14, 290, 244, 325)),
        (7200, 'Resupply', (78, 223, 181, 251)),
        (7600, 'The villagers shared', (14, 291, 244, 313)),
        (8000, 'Stay', (78, 234, 181, 263)),
    ):
        transitions.append(dict(capture=new[frame], complete_caption=dark_text(font, caption, captured(new[frame]), box)))
    return dict(discovery=discovery, original_dock_resupply_and_menu_return=transitions,
                fixture=fixture, exact_matching_frames=sorted(new), natural_travel=False), evidence


def verify_selector(arm):
    u = machine(arm)
    cases = [(paragraph.NOTICE_PARENT, n, paragraph.EQUIPMENT_PARAGRAPH) for n in SCOPE]
    cases.extend((parent, n, PRIOR) for parent, n in (
        (0x0205473C, 292), (0x02054764, 288), (paragraph.NOTICE_PARENT, 287),
        (paragraph.NOTICE_PARENT, 297), (paragraph.NOTICE_PARENT, 302),
        (paragraph.NOTICE_PARENT, 329), (paragraph.NOTICE_PARENT, 341)))
    results = []
    for parent, n, expected in cases:
        target, regs = dispatch(u, paragraph.HOOK, {0xC4: parent, 0xD0: n},
                                (PRIOR, paragraph.EQUIPMENT_PARAGRAPH))
        assert target == expected and regs[:3] == ARGS[:3]
        results.append(dict(parent=parent, message_ID=n, verified_first_continuation=target))
    return results


def verify_live():
    proof = load(PROOF)
    assert digest(ROM) == proof['research_ROM_sha256']
    arm = NdsImage.open(ROM).read_file(stage.ARM)
    font = GameAsciiFont.from_arm9(arm)
    auto, auto_inputs = verify_auto(proof, arm, font)
    village, village_inputs = verify_village(proof, font)
    save(LIVE, dict(candidate_sha256=digest(ROM), observed_ids=[297, 298], original_auto_move=auto,
        original_village=village, selector_positive_and_negative_cases=verify_selector(arm), hardware=False,
        evidence={str(path): digest(path) for path in (PROOF, *auto_inputs, *village_inputs, Path(__file__))}))
    print('The original Auto Move question, manual return, and Inuvik discovery through resupply passed.')


def verify_startup():
    source = checked_text(inspect.getsource(precedent.verify_startup), {
        "parent_path = BIOGRAPHIES / 'own_startup/capture/capture_report.json'":
            "parent_path = SHIPYARD / 'own_startup/capture/capture_report.json'",
        "prior_proof = BIOGRAPHIES / 'own_startup_verification.json'":
            "prior_proof = SHIPYARD / 'own_startup_verification.json'",
    })
    env = {**vars(precedent), **globals()}
    exec(compile(source, __file__ + '::same-cold-boot-and-name-contract', 'exec'), env)
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
