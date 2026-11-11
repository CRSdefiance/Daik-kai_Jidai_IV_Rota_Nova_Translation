"""Approve final card layouts and verify original Items navigation and startup."""

import argparse
import inspect
from pathlib import Path
from struct import unpack
from xml.etree import ElementTree

from scripts import replay_utility_weapon_item_cards_v2 as replay
from scripts import stage_source_item_cards_and_coin_v2 as parent
from scripts import verify_setup_save_equipment_v1 as boot
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_captain_biographies_v1 import captured


stage = replay.stage
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
PREDECESSOR = parent.ROOT
LIVE = ROOT / 'utility_weapon_items_gameplay_verification.json'
BOOT = ROOT / 'own_startup_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = Path('work/utility_weapon_cards_repo_qa_20261111.xml')
OBSERVED = [stage.IDS[replay.earlier.ITEM - 20]]


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
    assert report['ROM_sha256'] == proof['research_ROM_sha256'] and report['frames'] == 10400
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    donor = report['battery_save_preloaded']
    assert stage.digest(donor['source']) == donor['source_sha256'] == terminal['donor_sha256']
    assert donor['copied_byte_exact_before_cold_boot']
    assert not any(value for key, value in report.items()
                   if key.startswith('synthetic_') and key != 'synthetic_inventory_fixtures')
    inventory, = report['synthetic_inventory_fixtures']
    item, = inventory['items']
    assert item['item_id'] == replay.earlier.ITEM and item['name'] == 'Black Rapier' and item['category'] == 2
    assert inventory['frame'] == 8400 and inventory['native_transfer_entry'] == 0x02049F30
    assert item['result_owner_kind'] == 0 and not inventory['normal_acquisition_verified']
    navigation = stage.load(journal)['commands_received']
    assert all(row['validation_passed'] for row in navigation)
    assert [row['command'] for row in navigation] == stage.load(commands)

    image = stage.NdsImage.open(ROM)
    arm, common = image.read_file(stage.ARM), image.read_file(stage.COMMON)
    font = image.read_file('/GRP/KANJI.FNT')
    execute = stage.make_execute(proof['storage']['new_directory_sha256'], arm)
    native = execute(arm, 'fixture', item_page='main', item_case=(0, 4), surface_size=(240, 96),
                     kanji_font=font, mode=4, item_resource_index=item['item_id'], item_common=common)
    case, = [row for row in proof['item_cases']
             if (row['item_ID'], row['page'], row['mode']) == (item['item_id'], 'main', 4)]
    assert stage.sha256(native['pixels']).hexdigest() == case['native_ink_sha256']
    parent_requests = proof['native_PARENT_crop_contract']['requests']
    composed, _ = stage.compose(native, parent_requests)
    pixels = unpack('<49152H', composed)
    projection, = [row for row in proof['ownership']['item_paragraphs'] if row['item_ID'] == item['item_id']]
    lo, hi = proof['ownership']['appended_resident_text_span']
    assert lo <= projection['new_pointer'] < hi and projection['message_ID'] in OBSERVED
    fields = [row for row in parent_requests if row['source_origin'] in [[48, 0], [0, 36], [0, 48], [0, 60]]]
    assert len(fields) == 4
    shots = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('_navigation.png')}
    matches = []
    for frame in replay.earlier.MENU_FRAMES:
        photo = captured(shots[frame])
        for field in fields:
            x, y = field['destination_origin']
            width, height = field['size']
            model = {(xx, yy) for yy in range(height) for xx in range(width)
                     if pixels[(y + yy) * 256 + x + xx] == 1}
            actual = {(xx, yy) for yy in range(height) for xx in range(width)
                      if photo.getpixel((x + xx, y + yy)) == (230, 230, 230)}
            assert model == actual, (frame, field, len(model ^ actual))
            matches.append(dict(frame=frame, native_source_origin=field['source_origin'],
                                destination=[x, y], size=[width, height], foreground_pixels=len(actual)))
    assert len(matches) == 8
    assert captured(shots[8400]).tobytes() == captured(shots[10400]).tobytes()
    assert captured(shots[10000]).tobytes() != captured(shots[10400]).tobytes()
    stage.save(LIVE, dict(
        candidate_sha256=proof['research_ROM_sha256'], observed_ids=OBSERVED, original_Items_screen=True,
        actual_title_and_full_description_field_matches=matches, complete_description_foreground_and_blank_cells_exact=True,
        description_lines=case['lines'], resident_projection=projection, returning_to_same_town_screen=True,
        frame_references=[shots[n] for n in (8400, *replay.earlier.MENU_FRAMES, 10000, 10400)],
        synthetic_inventory_fixture=inventory, original_battery_save_unchanged=True, hardware=False,
        evidence={str(p): stage.digest(p) for p in (PROOF, report_path, terminal_path, commands, journal, Path(__file__))},
    ))
    print('Native Items menu displayed the complete relocated Black Rapier card and returned to Lisbon.')


def verify_startup():
    before = stage.NdsImage.open(stage.load(stage.RELEASE)['candidate']).read_file(stage.ARM)
    after = stage.NdsImage.open(ROM).read_file(stage.ARM)
    assert stage.cache_plan(before) == stage.cache_plan(after)
    assert before[0x8E4:0x8E8] == after[0x8E4:0x8E8]
    assert before[0xE45DC:0xE45E0] == after[0xE45DC:0xE45E0]
    source = checked_text(inspect.getsource(boot.verify_startup), {'BIOGRAPHIES': 'PREDECESSOR'})
    env = vars(boot) | globals()
    exec(compile(source, __file__ + '::unchanged-main-allocation-and-own-startup', 'exec'), env)
    env['verify_startup']()


def approve(viewed):
    proof, live, startup = map(stage.load, (PROOF, LIVE, BOOT))
    assert viewed == [sheet['sha256'] for sheet in proof['sheets']]
    assert all(stage.digest(sheet['path']) == sheet['sha256'] for sheet in proof['sheets'])
    assert proof['research_ROM_sha256'] == live['candidate_sha256'] == startup['candidate_sha256'] == stage.digest(ROM)
    tests = list(ElementTree.parse(QA).iter('testsuite'))
    assert sum(int(row.get('tests', 0)) for row in tests) == 34
    assert not any(int(row.get(key, 0)) for row in tests for key in ('errors', 'failures', 'skipped'))
    stage.save(CHECKPOINT, dict(candidate_sha256=stage.digest(ROM), approved_for_registered_successor=True,
        observed_ids=live['observed_ids'], stored_records=len(proof['records']),
        viewed_pages=sum(len(sheet['messages']) for sheet in proof['sheets']),
        evidence={str(p): stage.digest(p) for p in (PROOF, LIVE, BOOT, QA, Path(__file__))}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('live', 'startup', 'approve'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'approve':
        approve(args.viewed_sheets)
    else:
        (verify_live if args.action == 'live' else verify_startup)()
