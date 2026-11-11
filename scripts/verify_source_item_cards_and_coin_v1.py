"""Verify both representative actual displays and the fixed-allocation startup."""

import argparse
import inspect
from pathlib import Path
from xml.etree import ElementTree

from scripts import replay_source_item_cards_and_coin_v2 as replay
from scripts import verify_rumor_and_cooperation_v1 as prior
from scripts import verify_setup_save_equipment_v1 as boot
from scripts.register_faction_aftermath_portraits_v1 import RELEASE as PARENT
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_plaque_release_v247 import find_mask


stage = replay.stage
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
PREDECESSOR = replay.predecessor.ROOT
LIVE = ROOT / 'source_item_cards_and_coin_gameplay_verification.json'
BOOT = ROOT / 'own_startup_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = Path('work/source_item_cards_and_coin_repo_qa_20261111.xml')
OBSERVED = [2814, 2819]


def png_frames(report, suffix):
    return {row['frame']: row for row in report['frames_captured'] if row['path'].endswith(suffix)}


def verify_coin(proof, arm, kanji, raster, font):
    folder = replay.COIN_DIR / 'capture_finish'
    path = folder / 'capture_report.json'
    receipt = replay.COIN_DIR / 'fixture.json'
    fixture = prior.load(receipt)
    assert fixture['staged_ROM_sha256'] == proof['research_ROM_sha256']
    assert prior.digest(replay.COIN_ROM) == fixture['research_ROM_sha256']
    report, _ = prior.checked_report(path, fixture['research_ROM_sha256'], 6600)
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    commands = replay.COIN_DIR / 'inputs_finish.json'
    assert prior.load(commands) == report['scripted_input_schedule']
    frames = png_frames(report, '_cold_boot.png')
    snaps = {row['frame']: row for row in report['read_only_capture_RAM_snapshots']}

    def raw(frame):
        row = snaps[frame]
        assert row['read_only_export'] and prior.digest(row['path']) == row['sha256']
        return Path(row['path']).read_bytes()

    source = checked_text(inspect.getsource(prior.portrait_match), {
        "'Trader', captured(frames[frame])": "'Fernando Dias', captured(frames[frame])",
        "text='Trader'": "text='Fernando Dias'",
    })
    env = vars(prior).copy()
    exec(compile(source, __file__ + '::exact-coin-portrait-and-unchanged-nameplate', 'exec'), env)
    observed = env['portrait_match'](5450, 2814, frames, raw, snaps, arm, kanji, raster, font, proof)
    assert not observed['original_arguments']
    board = prior.captured(frames[5700])
    footer = [find_mask(font, label, board, (0, 365, 256, 384)) for label in ('Finish', 'Select')]
    assert frames[5700]['PNG_sha256'] != frames[5450]['PNG_sha256']
    return dict(response=observed, board_return=frames[5700], original_coin_buttons=footer,
                fixture=fixture, zero_selection_finished_with_X=True, natural_recruitment=False), (receipt, path, commands)


def verify_shark(proof, image, font):
    folder = replay.SHARK_DIR
    term_path = folder / 'terminal.json'
    term = prior.load(term_path)
    path = Path(term['report'])
    assert prior.digest(path) == term['report_sha256'] and term['candidate_sha256'] == proof['research_ROM_sha256']
    report, final = prior.checked_report(path, proof['research_ROM_sha256'], 14027)
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and prior.digest(donor['source']) == term['donor_sha256']
    fixtures = report['synthetic_condition_fixtures']
    assert [row['mode'] for row in fixtures] == ['initialize', 'restore-entry', 'restore-return-and-roster']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_') and key != 'synthetic_condition_fixtures')
    frames = png_frames(report, '_navigation.png')
    journal = folder / 'capture/navigation_command_journal.json'
    commands = folder / 'commands.json'
    assert prior.digest(commands) == term['commands_sha256']
    inputs = prior.load(journal)['commands_received']
    assert all(row['validation_passed'] for row in inputs)
    assert [row['command'] for row in inputs] == prior.load(commands)
    arm, common = image.read_file(stage.ARM), image.read_file(stage.COMMON)
    raw_before = next(row for row in report['read_only_pause_RAM_snapshots'] if row['frame'] == 8327)
    assert prior.digest(raw_before['path']) == raw_before['sha256']
    before = Path(raw_before['path']).read_bytes()
    for fixture in fixtures:
        for change in fixture['changes']:
            i = change['address'] - stage.BASE
            assert final[i] == before[i]
    cpu, get = prior.get_machine(arm, final)
    item = get(0xCB190) + 4 + 4 * 20
    assert get(0x4A368, item) == 2 and get(0x4A224, item) == 4
    assert bytes(cpu.mem_read(stage.BASE, len(final))) == final

    kanji = image.read_file('/GRP/KANJI.FNT')
    native = stage.make_execute(proof['storage']['new_directory_sha256'], arm)(
        arm, 'fixture', item_page='standalone', item_case=(0, 1), surface_size=(240, 96),
        kanji_font=kanji, mode=4, item_resource_index=4, item_common=common)
    target = next(row for row in proof['item_cases'] if (row['item_ID'], row['page'], row['mode']) == (4, 'standalone', 4))
    assert stage.sha256(native['pixels']).hexdigest() == target['native_ink_sha256']
    values = tuple(pixel for value in native['pixels'] for pixel in (value & 15, value >> 4))
    model = {(x, y) for y in range(36) for x in range(240) if values[(y + 24) * 256 + x] == 1}
    card = frames[13627]
    photo = prior.captured(card)
    x0, y0 = 8, 276
    actual = {(x, y) for y in range(36) for x in range(240) if photo.getpixel((x0 + x, y0 + y)) == (230, 230, 230)}
    assert actual == model, ('item card pixels', len(model), len(actual), len(model ^ actual))
    returned = frames[13827]
    footer = [find_mask(font, label, prior.captured(returned), (0, 365, 256, 384))
              for label in ('Rotate', 'Menu', 'Inspect', 'Sails')]
    return dict(message_ID=2819, original_item_card=card, description_lines=target['lines'],
        complete_description_foreground_and_blank_cells_exact=True, ink_pixels=len(model),
        original_ownership_award_and_sailing_return=True, returned=returned, sailing_footer=footer,
        standalone_origin=[x0, y0], initialized_original_shark_encounter=True, natural_encounter=False), (
            term_path, path, journal, commands)


def verify_live():
    proof = prior.load(PROOF)
    assert prior.digest(ROM) == proof['research_ROM_sha256']
    image = stage.NdsImage.open(ROM)
    arm = image.read_file(stage.ARM)
    raster, _, _ = prior.font_tools(image)
    font = prior.GameAsciiFont.from_arm9(arm)
    coin, coin_evidence = verify_coin(proof, arm, image.read_file('/GRP/KANJI.FNT'), raster, font)
    item, item_evidence = verify_shark(proof, image, font)
    prior.save(LIVE, dict(candidate_sha256=proof['research_ROM_sha256'], observed_ids=OBSERVED,
        coin_game=coin, item_card=item, hardware=False,
        evidence={str(p): prior.digest(p) for p in (PROOF, *coin_evidence, *item_evidence, Path(__file__))}))
    print('Verified Fernando’s empty-selection portrait and the full Baby Shark description in their original screens.')


def verify_startup():
    before = stage.NdsImage.open(prior.load(PARENT)['candidate']).read_file(stage.ARM)
    after = stage.NdsImage.open(ROM).read_file(stage.ARM)
    assert stage.cache_plan(before) == stage.cache_plan(after)
    assert before[0x8E4:0x8E8] == after[0x8E4:0x8E8]
    assert before[0xE45DC:0xE45E0] == after[0xE45DC:0xE45E0]
    source = checked_text(inspect.getsource(boot.verify_startup), {'BIOGRAPHIES': 'PREDECESSOR'})
    env = vars(boot) | globals()
    exec(compile(source, __file__ + '::original-fixed-allocation-startup-and-protected-getters', 'exec'), env)
    env['verify_startup']()


def approve(viewed):
    proof, live, startup = map(prior.load, (PROOF, LIVE, BOOT))
    assert viewed == [sheet['sha256'] for sheet in proof['sheets']]
    assert all(prior.digest(sheet['path']) == sheet['sha256'] for sheet in proof['sheets'])
    assert proof['research_ROM_sha256'] == live['candidate_sha256'] == startup['candidate_sha256'] == prior.digest(ROM)
    tests = list(ElementTree.parse(QA).iter('testsuite'))
    assert sum(int(row.get('tests', 0)) for row in tests) == 34
    assert not any(int(row.get(key, 0)) for row in tests for key in ('errors', 'failures', 'skipped'))
    prior.save(CHECKPOINT, dict(candidate_sha256=prior.digest(ROM), approved_for_registered_successor=True,
        observed_ids=live['observed_ids'], stored_records=len(proof['records']),
        viewed_pages=sum(len(sheet['messages']) for sheet in proof['sheets']),
        evidence={str(p): prior.digest(p) for p in (PROOF, LIVE, BOOT, QA, Path(__file__))}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('live', 'startup', 'approve'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'approve':
        approve(args.viewed_sheets)
    else:
        (verify_live if args.action == 'live' else verify_startup)()

