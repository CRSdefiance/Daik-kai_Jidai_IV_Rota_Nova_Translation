"""Verify the crew roles, native description pixels and original Lisbon menu return."""

import argparse
from pathlib import Path
from struct import unpack
from types import FunctionType, SimpleNamespace

from scripts import replay_crew_equipment_item_cards_v1 as replay
from scripts import stage_crew_equipment_item_cards_v1 as current
from scripts import verify_utility_weapon_item_cards_v1 as previous
from scripts.verify_captain_biographies_v1 import captured

stage = current.previous
ROOT, ROM, PROOF = current.ROOT, current.ROM, current.PROOF
PREDECESSOR = replay.parent.ROOT
LIVE = ROOT / 'crew_equipment_items_gameplay_verification.json'
BOOT = ROOT / 'own_startup_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = Path('work/crew_equipment_item_cards_repo_qa_20261111.xml')
OBSERVED = [replay.ITEM + 2815]
env = vars(previous) | globals()
env['stage'] = SimpleNamespace(**(vars(stage) | vars(current)))
verify_startup = FunctionType(previous.verify_startup.__code__, env)
approve = FunctionType(previous.approve.__code__, env)


def verify_roles(proof, rows):
    plan = stage.load(stage.prior.ITEM_PLAN)
    labels = {row['index']: row['compiled'] for row in plan['records'] if row.get('kind') == 'ROLE'}
    roles = {}
    for case in proof['item_cases']:
        number = case['message_ID']
        row = rows[number]
        role = row['native_role_index']
        draw, = [item for item in case['draws'] if item['x'] == plan['role_x'] and item['y'] == 12]
        assert draw['text'] == labels[role] and draw['text'].isascii()
        roles[role] = draw['text']
    assert len(proof['item_cases']) == 160
    assert set(roles) == set(range(16))
    return roles


def verify_live():
    proof = stage.load(PROOF)
    rows = current.active_rows(stage.load(current.OUTPUT))
    roles = verify_roles(proof, rows)
    assert stage.digest(ROM) == proof['research_ROM_sha256']
    report_path = replay.ITEMS / 'capture/capture_report.json'
    terminal_path = replay.ITEMS / 'terminal.json'
    inputs = replay.ITEMS / 'inputs.json'
    terminal, report = map(stage.load, (terminal_path, report_path))
    assert terminal['report_sha256'] == stage.digest(report_path)
    assert terminal['candidate_sha256'] == proof['research_ROM_sha256']
    assert stage.digest(inputs) == terminal['inputs_sha256'] and terminal['unchanged_original_save']
    assert stage.load(inputs) == report['scripted_input_schedule']
    assert report['ROM_sha256'] == proof['research_ROM_sha256'] and report['frames'] == 10801
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    donor = report['battery_save_preloaded']
    assert stage.digest(donor['source']) == donor['source_sha256'] == terminal['donor_sha256']
    assert donor['copied_byte_exact_before_cold_boot']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))

    image = stage.NdsImage.open(ROM)
    arm, common = image.read_file(stage.ARM), image.read_file(stage.COMMON)
    font = image.read_file('/GRP/KANJI.FNT')
    execute = stage.make_execute(proof['storage']['new_directory_sha256'], arm)
    native = execute(arm, 'fixture', item_page='main', item_case=(0, 4), surface_size=(240, 96),
                     kanji_font=font, mode=4, item_resource_index=replay.ITEM, item_common=common)
    case, = [row for row in proof['item_cases']
             if (row['item_ID'], row['page'], row['mode']) == (replay.ITEM, 'main', 4)]
    assert stage.sha256(native['pixels']).hexdigest() == case['native_ink_sha256']
    role = roles[rows[OBSERVED[0]]['native_role_index']]
    assert role == 'First Mate'
    parent_requests = proof['native_PARENT_crop_contract']['requests']
    composed, _ = stage.compose(native, parent_requests)
    pixels = unpack('<49152H', composed)
    projection, = [row for row in proof['ownership']['item_paragraphs'] if row['item_ID'] == replay.ITEM]
    assert projection['message_ID'] in OBSERVED and projection['storage'] == 'copied catalogue'
    fields = [row for row in parent_requests
              if row['source_origin'] in [[48, 0], [0, 12], [0, 36], [0, 48], [0, 60]]]
    assert len(fields) == 5
    shots = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('_cold_boot.png')}
    matches = []
    for frame in (10000, 10060):
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
    assert captured(shots[8400]).tobytes() == captured(shots[10800]).tobytes()
    assert captured(shots[10400]).tobytes() != captured(shots[10800]).tobytes()
    stage.save(LIVE, dict(candidate_sha256=proof['research_ROM_sha256'], observed_ids=OBSERVED,
        original_Items_screen=True, actual_title_role_effect_and_full_description_field_matches=matches,
        complete_description_foreground_and_blank_cells_exact=True, description_lines=case['lines'],
        selected_role=role, selected_projection=projection, returning_to_same_town_screen=True,
        role_index_to_rendered_label=roles, frame_references=[shots[n] for n in replay.HOLDS],
        original_battery_save_unchanged=True, inventory_fixture=False, hardware=False,
        evidence={str(p): stage.digest(p) for p in (PROOF, report_path, terminal_path, inputs, Path(__file__))}))
    print('Original Items menu displayed the complete Marco Polo card and First Mate label, then returned to Lisbon.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('live', 'startup', 'approve'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'approve':
        approve(args.viewed_sheets)
    else:
        (verify_live if args.action == 'live' else verify_startup)()
