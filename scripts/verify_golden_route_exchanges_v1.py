"""Approve the Golden Route layouts and bind the captured sale and guild transitions."""

import argparse
from hashlib import sha256
from pathlib import Path
from struct import unpack_from
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree

from scripts import replay_golden_route_exchanges_v1 as replay
from scripts import verify_city_combat_notices_live_v1 as city
from scripts import verify_golden_route_payout_v1 as payout
from scripts import verify_item_production_advice_v1 as startup


stage, base = replay.stage, replay.base
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
BIOGRAPHIES = replay.PREVIOUS.parent
BOOT, VISUAL = ROOT / 'own_startup_verification.json', ROOT / 'visual_layout_review.json'
LIVE, CHECKPOINT = ROOT / 'golden_route_gameplay_verification.json', ROOT / 'approved_checkpoint.json'
QA = Path('work/golden_route_exchanges_repo_qa_20261111.xml')
HOLDS = {23200: 3324, 23500: 3328, 23800: 3336, 24100: 3344, 24400: 3348, 24700: 3356,
         25000: 3360, 33100: 3380, 33700: 3381, 34000: 3385}


def approve_layout(viewed):
    assert not VISUAL.exists()
    proof = base.load(PROOF)
    assert base.digest(ROM) == proof['research_ROM_sha256']
    assert base.digest(stage.OUTPUT) == proof['manuscript_sha256']
    assert viewed == [row['sha256'] for row in proof['sheets']]
    assert all(base.digest(row['path']) == row['sha256'] for row in proof['sheets'])
    assert proof['native_pages'] == proof['native_cases'] == 117 and len(proof['records']) == 73
    assert sum(len(row['messages']) for row in proof['sheets']) == 117
    assert proof['parent_inverse_exact'] and proof['allocation']['all_41_blocks_fit_8KiB']
    assert proof['ownership']['selector_checks']['original_registers_and_stack_preserved']
    amount = base.load(payout.OUTPUT)
    assert len(amount['observations']) == 6 and amount['candidate_sha256'] == proof['research_ROM_sha256']
    assert amount['original_month_counter_and_season_gate_preserved'] and amount['offline_only']
    suites = list(ElementTree.parse(QA).iter('testsuite'))
    assert sum(int(row.get('tests', 0)) for row in suites) == 34
    assert all(int(row.get(key, 0)) == 0 for row in suites for key in ('errors', 'failures', 'skipped'))
    base.save(VISUAL, dict(candidate_sha256=proof['research_ROM_sha256'], stored_cases=73,
        native_pages=117, all_pages_viewed=True, complete_glyphs_and_bounds=True, repository_tests=34,
        sheet_sha256=viewed, payout_amount_last_row='The separate amount row holds the full native ten-digit value.',
        evidence={str(path): base.digest(path) for path in (PROOF, stage.OUTPUT, QA, payout.OUTPUT, Path(__file__))},
        representative_gameplay_and_registration_pending=True, new_credit=0))
    print('Approved 117 viewed layouts, six original payout cases and 34 repository tests.')


def verify_startup():
    review = stage.review
    loader = SimpleNamespace(load=base.load, RELEASE=review.parent.RELEASE, NdsImage=base.NdsImage, ARM=review.ARM)
    FunctionType(startup.verify_startup.__code__, vars(startup) | globals() | {'stage': loader, 'startup': startup.startup})()


def verify_gameplay():
    assert not LIVE.exists() and not CHECKPOINT.exists()
    proof, layout, boot = map(base.load, (PROOF, VISUAL, BOOT))
    sha = base.digest(ROM)
    assert sha == proof['research_ROM_sha256'] == layout['candidate_sha256'] == boot['candidate_sha256']
    terminal_path = replay.SALE / 'terminal.json'
    terminal = base.load(terminal_path)
    report_path = Path(terminal['report'])
    assert base.digest(report_path) == terminal['report_sha256']
    assert base.digest(terminal['source_capture']) == terminal['source_capture_sha256']
    assert base.digest(terminal['commands']) == terminal['commands_sha256']
    assert base.digest(replay.SALE / 'inputs.json') == terminal['inputs_sha256']
    report = base.load(report_path)
    assert report['ROM_sha256'] == sha and report['cold_boot'] and not report['savestate_loaded']
    assert report['frames'] == replay.END and not report['callback_errors']
    assert not report['earned_golden_route_discovery_reporting_or_payment_verified']
    snapshots = {row['frame']: row for row in report['read_only_capture_RAM_snapshots']}
    frames = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('.png')}
    rom = base.NdsImage.open(ROM)
    arm = rom.read_file(stage.ARM)
    portrait = stage.fleet.portrait
    raster, _, _ = portrait.font_tools(rom)
    kanji = rom.read_file('/GRP/KANJI.FNT')
    owner, wrapped = [unpack_from('<I', arm, offset)[0] - stage.BASE for offset in (0x552A0, 0x54450)]
    records = {row['message_ID']: row for row in proof['records']}

    def snapshot(item):
        raw = Path(item['path']).read_bytes()
        assert item['read_only_export'] and len(raw) == 0x400000 and sha256(raw).hexdigest() == item['sha256']
        return raw

    def text(raw, address):
        return raw[address:address + 512].split(b'\0', 1)[0]

    paused, = [row for row in report['read_only_pause_RAM_snapshots'] if row['frame'] == replay.PAUSE]
    _, fixture = replay.discount_salt_purchase(arm, snapshot(paused), 1)
    assert report['synthetic_golden_route_display_fixtures'] == [fixture | {'frame': replay.PAUSE}]
    table = payout.TABLE - stage.BASE
    assert [snapshot(snapshots[frame])[table] for frame in (22600, 23200, 30400, 33100, 34000)] == [0, 1, 2, 3, 3]
    observed = []
    for frame, number in HOLDS.items():
        raw = snapshot(snapshots[frame])
        record = records[number]
        stored = text(raw, owner + 0x2030)
        formatted = text(raw, wrapped)
        assert stored.hex() == record['staged_hex'], (frame, number, stored)
        pixels, glyphs = portrait.render_portrait(raster, arm, kanji, formatted)
        image = city.captured(frames[frame])
        mask = bytes(pixel == (0, 8, 0) for pixel in image.crop(city.PAPER).get_flattened_data())
        assert mask == bytes(bool(pixel) for pixel in pixels), (frame, number, formatted)
        if number != 3385:
            display, = [case for case in record['displays'] if case['display_hex'] == formatted.hex()]
            assert len(glyphs) == display['complete_glyphs']
        else:
            purchase, sale = unpack_from('<II', raw, table + 4)
            assert purchase == 1 and sale > purchase
            assert b' '.join(formatted.split()) == stored % (b'Salt', str(sale - purchase).encode('ascii'))
        observed.append(dict(message_ID=number, frame=frame, native_glyphs=len(glyphs),
            stored_hex=stored.hex(), expanded_visible=formatted.decode('cp932'), capture=frames[frame]))
    bindings = {str(path): base.digest(path) for path in
                (PROOF, VISUAL, BOOT, QA, payout.OUTPUT, terminal_path, report_path, Path(__file__))}
    ids = list(HOLDS.values())
    base.save(LIVE, dict(candidate_sha256=sha, observed_ids=ids, observations=observed,
        actual_emulator=True, hardware=False, original_sale_guild_report_and_reward_terms=True,
        discovery_view=frames[33400], guild_menu_return=frames[replay.END],
        fixture_scope='One temporary Salt purchase-cost word on the original Trade screen.',
        repeat_discovery_plural_report_and_payout_offline=True, evidence=bindings))
    base.save(CHECKPOINT, dict(candidate_sha256=sha, approved_for_registered_successor=True, live_messages=ids,
        stored_cases=73, viewed_pages=117, evidence=bindings | {str(LIVE): base.digest(LIVE)}))
    print(f'Observed original sale, discovery dialogue, guild report and reward terms: {ids}.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('layout', 'startup', 'gameplay'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'layout':
        approve_layout(args.viewed_sheets)
    else:
        {'startup': verify_startup, 'gameplay': verify_gameplay}[args.action]()
