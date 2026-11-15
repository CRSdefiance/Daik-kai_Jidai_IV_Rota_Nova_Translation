"""Bind the reviewed sailing layouts and observed dolphin exchange to the candidate."""

import argparse
from hashlib import sha256
from json import loads
from pathlib import Path
from struct import unpack_from
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree

from scripts import replay_sailing_hazards_and_dolphins_v2 as replay
from scripts import verify_city_combat_notices_live_v1 as city
from scripts import verify_item_production_advice_v1 as startup


stage, base = replay.stage, replay.base
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
BIOGRAPHIES = replay.prior.previous.replay.STARTUP.parent
BOOT, VISUAL = ROOT / 'own_startup_verification.json', ROOT / 'visual_layout_review.json'
LIVE = ROOT / 'sailing_hazards_and_dolphins_gameplay_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = Path('work/sailing_hazards_and_dolphins_repo_qa_20261111_v2.xml')
review = replay.candidate.previous.review
portrait = replay.candidate.previous.prior.portrait
HOLDS = {8750: 2366, 8950: 2374, 10450: 2384}


def approve_layout(viewed):
    assert not VISUAL.exists()
    proof = base.load(PROOF)
    assert base.digest(ROM) == proof['research_ROM_sha256']
    assert base.digest(review.OUTPUT) == proof['manuscript_sha256']
    assert viewed == [row['sha256'] for row in proof['sheets']]
    assert all(base.digest(row['path']) == row['sha256'] for row in proof['sheets'])
    assert len(proof['records']) == proof['native_pages'] == proof['native_cases'] == 59
    assert sum(len(row['messages']) for row in proof['sheets']) == 59
    assert {row['message_ID'] for row in proof['records']} == set(range(2366, 2425))
    assert proof['allocation']['all_41_blocks_fit_8KiB'] and proof['parent_inverse_exact']
    assert proof['ownership']['selector_checks']['original_registers_and_stack_preserved']
    suites = list(ElementTree.parse(QA).iter('testsuite'))
    assert sum(int(row.get('tests', 0)) for row in suites) == 34
    assert all(int(row.get(key, 0)) == 0 for row in suites for key in ('errors', 'failures', 'skipped'))
    base.save(VISUAL, dict(candidate_sha256=proof['research_ROM_sha256'], stored_cases=59, native_pages=59,
        all_pages_viewed=True, complete_glyphs_and_bounds=True, repository_tests=34, sheet_sha256=viewed,
        dramatic_breaks={'2406': 'The startled cry stands on its own before the full warning.'},
        evidence={str(path): base.digest(path) for path in (PROOF, review.OUTPUT, QA, Path(__file__))},
        representative_gameplay_and_registration_pending=True, new_credit=0))
    print('Approved all 59 viewed pages and 34 targeted tests.')


def verify_startup():
    loader = SimpleNamespace(load=base.load, RELEASE=review.parent.RELEASE, NdsImage=base.NdsImage, ARM=review.ARM)
    FunctionType(startup.verify_startup.__code__, vars(startup) | globals() | {'stage': loader, 'startup': startup.startup})()


def verify_gameplay():
    assert not LIVE.exists() and not CHECKPOINT.exists()
    proof, layout, boot = map(base.load, (PROOF, VISUAL, BOOT))
    sha = base.digest(ROM)
    assert sha == proof['research_ROM_sha256'] == layout['candidate_sha256'] == boot['candidate_sha256']
    rom = base.NdsImage.open(ROM)
    arm = rom.read_file(review.ARM)
    raster, _, _ = portrait.font_tools(rom)
    kanji = rom.read_file('/GRP/KANJI.FNT')
    owner, wrapped = [unpack_from('<I', arm, offset)[0] - review.BASE for offset in (0x552A0, 0x54450)]
    rows = {case['message_ID']: case for case in proof['records']}

    terminal_path = replay.DOLPHINS / 'terminal.json'
    terminal = base.load(terminal_path)
    report_path, commands = Path(terminal['report']), Path(terminal['commands'])
    assert base.digest(report_path) == terminal['report_sha256'] and base.digest(commands) == terminal['commands_sha256']
    report = base.load(report_path)
    old = base.load(replay.prior.DOLPHINS / 'terminal.json')
    assert old['commands_sha256'] == terminal['commands_sha256']
    assert base.digest(old['report']) == old['report_sha256']
    assert terminal['unchanged_original_save'] and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and report['ROM_sha256'] == sha and report['frames'] == replay.prior.END
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    assert donor['source_sha256'] == base.load(old['report'])['battery_save_preloaded']['source_sha256']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_') and key != 'synthetic_condition_fixtures')
    journal = report_path.with_name('navigation_command_journal.json')
    received = base.load(journal)['commands_received']
    assert all(row['validation_passed'] for row in received)
    assert [row['command'] for row in received] == [loads(line) for line in commands.read_text(encoding='utf-8').splitlines()]
    frames = {item['frame']: item for item in report['frames_captured'] if item['path'].endswith('_navigation.png')}
    snapshots = {item['frame']: item for item in report['read_only_pause_RAM_snapshots']}

    def snapshot(frame):
        item = snapshots[frame]
        raw = Path(item['path']).read_bytes()
        assert item['read_only_export'] and len(raw) == 0x400000
        assert sha256(raw).hexdigest() == item['sha256']
        return raw

    def text(raw, pointer):
        return raw[pointer:pointer + 512].split(b'\0', 1)[0]

    _, condition = replay.set_condition(arm, snapshot(8327), {'event': 'dolphins'})
    assert report['synthetic_condition_fixtures'] == [condition | {'frame': 8327}]
    observations = []
    for frame, number in HOLDS.items():
        raw = snapshot(frame)
        staged = rows[number]
        assert text(raw, owner + 0x2030).hex() == staged['staged_hex'], number
        formatted = text(raw, wrapped)
        display, = staged['displays']
        assert formatted.hex() == display['display_hex'], number
        pixels, glyphs = portrait.render_portrait(raster, arm, kanji, formatted)
        image = city.captured(frames[frame])
        mask = bytes(pixel == (0, 8, 0) for pixel in image.crop(city.PAPER).get_flattened_data())
        assert mask == bytes(bool(pixel) for pixel in pixels) and sha256(pixels).hexdigest() == display['native_ink_sha256'], number
        assert len(glyphs) == display['complete_glyphs']
        observations.append(dict(message_ID=number, frame=frame, complete_glyphs=len(glyphs),
                                 lines=display['visible_lines'], capture=frames[frame], RAM=snapshots[frame]))
    next_frame = 12500
    assert text(snapshot(next_frame), owner + 0x2030) == b"Admiral, we've spotted a port!"
    old_frame, = [row for row in base.load(old['report'])['frames_captured']
                  if row['frame'] == next_frame and row['path'].endswith('_navigation.png')]
    assert city.captured(frames[next_frame]).tobytes() == city.captured(old_frame).tobytes()
    ids = list(HOLDS.values())
    inputs = (PROOF, VISUAL, BOOT, QA, terminal_path, report_path, commands, journal, Path(old['report']), Path(__file__))
    bindings = {str(path): base.digest(path) for path in inputs}
    base.save(LIVE, dict(candidate_sha256=sha, observed_ids=ids, observations=observations,
        actual_emulator=True, hardware=False, original_log_reply_farewell_and_next_sailing_report=True,
        next_port_report=frames[next_frame], fixture_scope='One original fleet condition set to Dolphins.',
        other_captains_and_hazards_offline=True, evidence=bindings))
    base.save(CHECKPOINT, dict(candidate_sha256=sha, approved_for_registered_successor=True,
        live_messages=ids, stored_cases=59, viewed_pages=59, evidence=bindings | {str(LIVE): base.digest(LIVE)}))
    print(f'Observed dolphin request, captain permission, farewell and next port report. IDs {ids}.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('layout', 'startup', 'gameplay'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'layout':
        approve_layout(args.viewed_sheets)
    else:
        {'startup': verify_startup, 'gameplay': verify_gameplay}[args.action]()
