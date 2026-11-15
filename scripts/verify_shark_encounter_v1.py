"""Verify the complete focused shark decision and both original outcomes."""

import argparse
import inspect
from hashlib import sha256
from pathlib import Path
import struct
import xml.etree.ElementTree as ET

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.rom.nds import NdsImage
from scripts import stage_shark_encounter_v1 as stage
from scripts import verify_setup_save_equipment_v1 as precedent
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_shared_notice_storage_v1 import checked_report
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.record_navigation_v327 import dark_text
from scripts.replay_shark_encounter_v1 import ARM, BASE, COMMON_HOLDS, FINAL
from scripts.replay_shark_encounter_v1 import MENU, MENU_CONFIRM, PAUSE, PRIOR as EPILOGUE, commands
from scripts.replay_shark_encounter_v2 import CONTINUE, ENTRY, OUT as KILL_RUN, fixture_controller
from scripts.replay_shark_encounter_v3 import OUT as CARD_REFERENCE
from scripts.replay_shark_encounter_v4 import OUT as RAISE_RUN, FINAL as RAISE_FINAL
from scripts.replay_shark_encounter_v4 import RESTORE as RAISE_RESTORE, commands as raise_commands
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_captain_biographies_v1 import captured
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_mutiny_release_inputs_v1 import portrait_ink
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_plaque_release_v247 import find_mask


ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
LIVE = ROOT / 'shark_encounter_gameplay_verification.json'
BOOT = ROOT / 'own_startup_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = Path('work/shark_encounter_repo_qa_20261111.xml')
PAPER = (16, 296, 244, 360)
COMMON_IDS = (2425, 313, 2427, 313, 2430, 2432, 2435, 2443, 2445, 2448, 2449, 2450, 2451)
OUTCOMES = {'raise': (2452, 2436, 2438, 2441, 314), 'kill': (2442, 2453)}
SYSTEM = {313: 'Splish, splash!', 314: 'You got a baby shark!'}
NAMEPLATES = {'Al Ferid Shin': 'Al Shin', 'Samwell da Khan': 'Samwell Khan', 'Hodram': 'Hodram Bergstrom'}


def menu_mask(proof, frame, selected):
    menu = proof['native_menu']
    x0, y0, x1, _ = menu['research']['modal_rectangle']
    width = menu['research']['minimum_width_units'] * 6
    x = (x0 + x1 - width) // 2
    assert digest(menu['sheet']['path']) == menu['sheet']['sha256']
    with Image.open(menu['sheet']['path']) as source:
        sheet = source.convert('RGB')
    screen = captured(frame)
    masks = []
    for index in (0, 1):
        style = 15 if index == selected else 1
        order = 2 * index + (style == 15)
        native = menu['captions'][order]
        assert native['option'] == index and native['style'] == style
        y_sheet = 55 * order + 17
        pixels = sheet.crop((5, y_sheet, 5 + 3 * width, y_sheet + 36))
        ink = bytes(color == (0, 8, 0) for color in
                    pixels.resize((width, 12), Image.Resampling.NEAREST).get_flattened_data())
        y = 192 + y0 + 16 + 20 * index
        colors = screen.crop((x, y, x + width, y + 12)).get_flattened_data()
        assert bytes(color == (8, 8, 8) for color in colors) == ink, (frame['frame'], index, style, x, y)
        assert ((0, 165, 172) in colors) == (style == 15), (frame['frame'], index, style)
        masks.append(dict(frame=frame['frame'], index=index, caption=native['text'],
                          style=style, original_complete_caption_and_centering=True))
    return masks


def check_replay(choice, proof, manuscript, arm, font):
    out = (RAISE_RUN if choice == 'raise' else KILL_RUN) / 'raise'
    terminal = load(out / 'terminal.json')
    path = Path(terminal['report'])
    assert terminal['candidate_sha256'] == proof['research_ROM_sha256']
    assert terminal['donor_unchanged'] and digest(path) == terminal['report_sha256']
    assert digest(out / 'commands.json') == terminal['commands_sha256']
    ending_frame = RAISE_FINAL if choice == 'raise' else FINAL
    report, final = checked_report(path, proof['research_ROM_sha256'], ending_frame)
    donor = report['battery_save_preloaded']
    assert digest(donor['source']) == donor['source_sha256'] == terminal['donor_sha256']
    assert donor['copied_byte_exact_before_cold_boot']
    schedule = raise_commands() if choice == 'raise' else commands('raise')
    prefix = load(out / 'inputs.json')
    start = PAUSE
    expected = list(prefix)
    for command in schedule[:-1]:
        if command.get('buttons'):
            expected.append(dict(start=start + 1, duration=command['duration'], buttons=command['buttons']))
        start = command['until']
    assert report['scripted_input_schedule'] == expected
    assert not any(value for key, value in report.items()
                   if key.startswith('synthetic_') and key != 'synthetic_condition_fixtures')
    frames = {entry['frame']: entry for entry in report['frames_captured'] if entry['path'].endswith('navigation.png')}
    snapshots = {entry['frame']: entry for entry in report['read_only_pause_RAM_snapshots']}

    def snapshot(frame):
        entry = snapshots[frame]
        assert entry['read_only_export'] and digest(entry['path']) == entry['sha256']
        return Path(entry['path']).read_bytes()

    replay_fixture = fixture_controller(ROM)
    fixtures = []
    for frame, mode in ((PAUSE, 'initialize'), (COMMON_HOLDS[0], 'restore-entry'),
                        (RAISE_RESTORE if choice == 'raise' else 13627, 'restore-return-and-roster')):
        _, receipt = replay_fixture(arm, snapshot(frame), {'mode': mode})
        fixtures.append(receipt | {'frame': frame})
    # JSON converts the two actor-ID keys to strings.
    for receipt in fixtures:
        receipt['actor_membership_fields'] = {str(k): v for k, v in receipt['actor_membership_fields'].items()}
    assert report['synthetic_condition_fixtures'] == fixtures
    assert final[ENTRY:CONTINUE + 4] == arm[ENTRY:CONTINUE + 4]
    for address in fixtures[0]['actor_membership_fields'].values():
        assert final[address - BASE] == snapshot(PAUSE)[address - BASE]

    bodies = {row['message_ID']: row for row in proof['native_portrait_cases']}
    storage = {row['message_ID']: row for row in proof['stored']}
    source = {row['message_ID']: row for row in manuscript['records']}
    expand, output = (struct.unpack_from('<I', arm, offset)[0] - BASE for offset in (0x5444C, 0x54450))
    timeline = list(zip(COMMON_IDS, COMMON_HOLDS, strict=True))
    timeline.extend(zip(OUTCOMES[choice], range(12627, 12627 + 200 * len(OUTCOMES[choice]), 200), strict=True))
    observed = []
    for n, frame in timeline:
        shot = frames[frame]
        if n in SYSTEM:
            text = dark_text(font, SYSTEM[n], captured(shot), (14, 291, 244, 320))
            observed.append(dict(message_ID=n, capture=shot, original_system_caption=text))
            continue
        raw = snapshot(frame)
        plain, display = (raw[at:at + 256].split(b'\0', 1)[0] for at in (expand, output))
        assert plain.hex() == storage[n]['staged_hex'] and display.hex() == bodies[n]['display_hex'], (n, frame)
        assert sha256(portrait_ink(shot['path'], PAPER)).hexdigest() == bodies[n]['native_ink_sha256'], (n, frame)
        speaker = source[n]['speaker']
        label = NAMEPLATES[speaker]
        count, bounds = complete_mask(font, label, captured(shot), 16, 277, (98, 97, 98))
        nameplate = dict(label=label, ink_pixels=count, bounds=bounds, complete_mask=True)
        observed.append(dict(message_ID=n, capture=shot, RAM=snapshots[frame],
            lines=bodies[n]['visible_lines'], speaker=speaker, exact_nameplate=nameplate,
            exact_native_glyphs_and_blank_margins=True))

    for frame in (MENU, MENU_CONFIRM):
        for row in proof['menu_allocation']['changes']:
            assert struct.unpack_from('<I', snapshot(frame), row['field'])[0] == row['target_pointer']
    menu = menu_mask(proof, frames[MENU], None)
    menu += menu_mask(proof, frames[MENU_CONFIRM], 0 if choice == 'raise' else 1)
    command_path = out / 'capture/navigation_command_journal.json'
    journal = load(command_path)['commands_received']
    assert all(row['validation_passed'] for row in journal)
    assert [row['command'] for row in journal] == schedule
    cpu, get = get_machine(arm, final)
    item = get(0xCB190) + 4 + 4 * 20
    found = get(0x4A368, item)
    available = get(0x4A224, item)
    assert found == (2 if choice == 'raise' else 0)
    assert available == (4 if choice == 'raise' else 0)
    assert bytes(cpu.mem_read(BASE, len(final))) == final
    item_card = None
    card_evidence = ()
    if choice == 'raise':
        item_frame = frames[13627]
        reference = CARD_REFERENCE / 'raise/capture/capture_report.json'
        old, = [row for row in load(reference)['frames_captured'] if row['frame'] == 13627]
        assert captured(item_frame).tobytes() == captured(old).tobytes()
        item_card = dict(capture=item_frame, visual_title='Baby Shark', unchanged_card_capture=old,
                         exact_frame_repeat=True, original_B_dismissal=True)
        card_evidence = (reference,)
    returned = frames[RAISE_RESTORE if choice == 'raise' else 13027]
    footer = [find_mask(font, label, captured(returned), (0, 365, 256, 384))
              for label in ('Rotate', 'Menu', 'Inspect', 'Sails')]
    return dict(choice=choice, original_dialogue=observed, original_menu_planes=menu, fixture=fixtures,
        original_item_4_received=available == 4, original_item_4_found_bit=found,
        original_item_4_inventory_bit=available, original_item_card=item_card,
        return_to_sea=returned, native_manual_sailing_footer=footer,
        ROM_sha256=terminal['candidate_sha256'], natural_encounter=False), (
            path, out / 'terminal.json', command_path, *card_evidence)


def verify_live():
    proof, manuscript = map(load, (PROOF, stage.OUTPUT))
    assert digest(ROM) == proof['research_ROM_sha256']
    arm = NdsImage.open(ROM).read_file(ARM)
    font = GameAsciiFont.from_arm9(arm)
    runs, paths = [], []
    for choice in ('raise', 'kill'):
        run, evidence = check_replay(choice, proof, manuscript, arm, font)
        runs.append(run)
        paths.extend(evidence)
    observed = sorted({row['message_ID'] for run in runs for row in run['original_dialogue']
                       if row['message_ID'] not in SYSTEM})
    assert len(observed) == 17
    save(LIVE, dict(candidate_sha256=digest(ROM), observed_ids=observed, original_choice_results=runs,
        hardware=False, evidence={str(path): digest(path) for path in (PROOF, *paths, Path(__file__))}))
    print('The original shark decision and both dialogue and item outcomes passed.')


def verify_startup():
    source = checked_text(inspect.getsource(precedent.verify_startup), {
        "parent_path = BIOGRAPHIES / 'own_startup/capture/capture_report.json'":
            "parent_path = EPILOGUE / 'own_startup/capture/capture_report.json'",
        "prior_proof = BIOGRAPHIES / 'own_startup_verification.json'":
            "prior_proof = EPILOGUE / 'own_startup_verification.json'",
    })
    env = {**vars(precedent), **globals()}
    exec(compile(source, __file__ + '::same-cold-boot-and-name-contract', 'exec'), env)
    env['verify_startup']()


def approve(viewed):
    assert not CHECKPOINT.exists()
    proof, live, startup = map(load, (PROOF, LIVE, BOOT))
    sheets = [*proof['contact_sheets'], proof['native_menu']['sheet']]
    assert viewed == [sheet['sha256'] for sheet in sheets]
    assert all(digest(sheet['path']) == sheet['sha256'] for sheet in sheets)
    assert proof['research_ROM_sha256'] == live['candidate_sha256'] == startup['candidate_sha256'] == digest(ROM)
    suites = list(ET.parse(QA).getroot().iter('testsuite'))
    assert sum(int(row.get('tests', 0)) for row in suites) == 30
    assert all(int(row.get(key, 0)) == 0 for row in suites for key in ('errors', 'failures', 'skipped'))
    save(CHECKPOINT, dict(candidate_sha256=digest(ROM), approved_for_registered_successor=True,
        observed_ids=live['observed_ids'], stored_records=len(proof['stored']),
        viewed_portrait_pages=sum(len(sheet['messages']) for sheet in sheets[:-1]),
        viewed_choice_styles=len(proof['native_menu']['captions']),
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
