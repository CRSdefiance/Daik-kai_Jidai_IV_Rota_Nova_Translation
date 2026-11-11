"""Verify the figurehead, instrument, and gift screens in the original Items menu."""

import argparse
from pathlib import Path
from struct import unpack
from types import FunctionType

from scripts import replay_figurehead_navigation_gift_cards_v1 as replay
from scripts import verify_utility_weapon_item_cards_v1 as previous
from scripts.verify_captain_biographies_v1 import captured

stage = replay.stage
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
PREDECESSOR = replay.parent.ROOT
LIVE = ROOT / 'figurehead_navigation_gift_gameplay_verification.json'
BOOT = ROOT / 'own_startup_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = Path('work/figurehead_navigation_gift_cards_repo_qa_20261111.xml')
OBSERVED = [2929, 2940, 2942]
env = vars(previous) | globals()
verify_startup = FunctionType(previous.verify_startup.__code__, env)
approve = FunctionType(previous.approve.__code__, env)


def matches(photo, pixels, field):
    x, y = field['destination_origin']
    width, height = field['size']
    model = {(xx, yy) for yy in range(height) for xx in range(width)
             if pixels[(y + yy) * 256 + x + xx] == 1}
    actual = {(xx, yy) for yy in range(height) for xx in range(width)
              if photo.getpixel((x + xx, y + yy)) == (230, 230, 230)}
    return model == actual, len(actual)


def verify_live():
    proof = stage.load(PROOF)
    assert stage.digest(ROM) == proof['research_ROM_sha256']
    report_path = replay.ITEMS / 'capture/capture_report.json'
    commands = replay.ITEMS / 'commands.json'
    journal = replay.ITEMS / 'capture/navigation_command_journal.json'
    terminal_path = replay.ITEMS / 'terminal.json'
    terminal = stage.load(terminal_path)
    assert terminal['report_sha256'] == stage.digest(report_path)
    assert terminal['candidate_sha256'] == proof['research_ROM_sha256']
    assert stage.digest(commands) == terminal['commands_sha256'] and terminal['unchanged_original_save']
    report = stage.load(report_path)
    assert report['ROM_sha256'] == proof['research_ROM_sha256'] and report['frames'] == 11600
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    donor = report['battery_save_preloaded']
    assert stage.digest(donor['source']) == donor['source_sha256'] == terminal['donor_sha256']
    assert donor['copied_byte_exact_before_cold_boot']
    assert not any(value for key, value in report.items()
                   if key.startswith('synthetic_') and key != 'synthetic_inventory_fixtures')
    inventory, = report['synthetic_inventory_fixtures']
    assert [(row['item_id'], row['category'], row['name']) for row in inventory['items']] == [
        (114, 5, 'Eagle Figurehead'), (127, 7, 'Frozen Rose')]
    assert inventory['frame'] == 8400 and inventory['native_transfer_entry'] == 0x02049F30
    assert all(row['result_owner_kind'] == 0 for row in inventory['items'])
    assert not inventory['normal_acquisition_verified']
    navigation = stage.load(journal)['commands_received']
    assert all(row['validation_passed'] for row in navigation)
    assert [row['command'] for row in navigation] == stage.load(commands)

    image = stage.NdsImage.open(ROM)
    arm, common = image.read_file(stage.ARM), image.read_file(stage.COMMON)
    font = image.read_file('/GRP/KANJI.FNT')
    execute = stage.make_execute(proof['storage']['new_directory_sha256'], arm)
    requests = proof['native_PARENT_crop_contract']['requests']
    fields = [row for row in requests
              if row['source_origin'] in [[48, 0], [0, 12], [0, 36], [0, 48], [0, 60]]]
    title, *body = fields
    assert title['source_origin'] == [48, 0] and len(body) == 4
    shots = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('_navigation.png')}
    frames = {frame: captured(shots[frame]) for frame in replay.HOLDS}
    observed = {}
    for number in OBSERVED:
        ident = number - 2815
        native = execute(arm, 'fixture', item_page='main', item_case=(0, 4), surface_size=(240, 96),
                         kanji_font=font, mode=4, item_resource_index=ident, item_common=common)
        case, = [row for row in proof['item_cases']
                 if (row['message_ID'], row['page'], row['mode']) == (number, 'main', 4)]
        assert stage.sha256(native['pixels']).hexdigest() == case['native_ink_sha256']
        composed, _ = stage.compose(native, requests)
        pixels = unpack('<49152H', composed)
        title_matches = [(n, photo) for n, photo in frames.items() if matches(photo, pixels, title)[0]]
        assert title_matches, (number, 'native title did not appear')
        receipts = []
        for frame, photo in title_matches:
            for field in fields:
                exact, foreground = matches(photo, pixels, field)
                assert exact, (number, frame, field)
                receipts.append(dict(frame=frame, native_source_origin=field['source_origin'],
                                     destination=field['destination_origin'], size=field['size'],
                                     foreground_pixels=foreground))
        observed[number] = dict(title_role_effect_and_description_fields=receipts,
                                capture_frames=[shots[n] for n, _ in title_matches], lines=case['lines'])
    assert captured(shots[8400]).tobytes() == captured(shots[11600]).tobytes()
    assert captured(shots[11200]).tobytes() != captured(shots[11600]).tobytes()
    stage.save(LIVE, dict(candidate_sha256=proof['research_ROM_sha256'], observed_ids=OBSERVED,
        original_Items_screen=True, complete_description_foreground_and_blank_cells_exact=True,
        returning_to_same_town_screen=True, observed=observed,
        navigation_fixture=inventory, original_sextant_already_held=True,
        original_battery_save_unchanged=True, hardware=False,
        town_return=shots[11600], evidence={
            str(p): stage.digest(p) for p in (PROOF, report_path, terminal_path, commands, journal, Path(__file__))
        }))
    print('Original Items menu displayed the complete Eagle Figurehead, Sextant and Frozen Rose cards and returned to Lisbon.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('live', 'startup', 'approve'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'approve':
        approve(args.viewed_sheets)
    else:
        (verify_live if args.action == 'live' else verify_startup)()
