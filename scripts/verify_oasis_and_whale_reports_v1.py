"""Bind the rendered pages and original whale sequence to the staged ROM."""

import argparse
from hashlib import sha256
from json import loads
from pathlib import Path
from struct import unpack_from
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree

from scripts import replay_oasis_and_whale_reports_v1 as replay
from scripts import verify_city_combat_notices_live_v1 as city
from scripts import verify_item_production_advice_v1 as startup
from scripts.navigate_hot_spring_crew_v1652 import visible_paper


stage, base = replay.stage, replay.base
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
BIOGRAPHIES = replay.prior.STARTUP.parent
BOOT, VISUAL = ROOT / 'own_startup_verification.json', ROOT / 'visual_layout_review.json'
LIVE, CHECKPOINT = ROOT / 'oasis_and_whale_reports_gameplay_verification.json', ROOT / 'approved_checkpoint.json'
QA = Path('work/oasis_and_whale_reports_repo_qa_20261111.xml')
review, portrait = replay.candidate.review, replay.candidate.first.portrait


def approve_layout(viewed):
    assert not VISUAL.exists()
    proof = base.load(PROOF)
    assert base.digest(ROM) == proof['research_ROM_sha256']
    assert base.digest(replay.candidate.OUTPUT) == proof['manuscript_sha256']
    assert viewed == [row['sha256'] for row in proof['sheets']]
    assert all(base.digest(row['path']) == row['sha256'] for row in proof['sheets'])
    assert len(proof['records']) == 71 and proof['native_pages'] == proof['native_cases'] == 125
    assert sum(len(row['messages']) for row in proof['sheets']) == 125
    suites = list(ElementTree.parse(QA).iter('testsuite'))
    assert sum(int(row.get('tests', 0)) for row in suites) == 34
    assert all(int(row.get(key, 0)) == 0 for row in suites for key in ('errors', 'failures', 'skipped'))
    assert len(proof['ownership']['native_proof_argument_prefixes']) == 7
    assert len([d for row in proof['records'] if 2323 <= row['message_ID'] <= 2330 for d in row['displays']]) == 56
    base.save(VISUAL, dict(candidate_sha256=proof['research_ROM_sha256'], stored_cases=71, native_pages=125,
        all_pages_viewed=True, complete_glyphs_and_bounds=True, repository_tests=34, sheet_sha256=viewed,
        proof_region_and_item_combinations=56, native_proof_prefixes=7,
        scoped_break_guard_controls=proof['ownership']['selector_checks'],
        evidence={str(path): base.digest(path) for path in (PROOF, replay.candidate.OUTPUT, QA, Path(__file__))},
        representative_gameplay_and_registration_pending=True, new_credit=0))
    print('Approved 125 viewed pages, all seven native Proof name pairs and 34 tests.')


def verify_startup():
    loader = SimpleNamespace(load=base.load, RELEASE=review.parent.RELEASE, NdsImage=base.NdsImage, ARM=review.ARM)
    FunctionType(startup.verify_startup.__code__, vars(startup) | globals() | {'stage': loader, 'startup': startup.startup})()
    proof, deployed = map(base.load, (PROOF, BOOT))
    raw = Path(deployed['read_only_snapshot']['path']).read_bytes()
    at = replay.candidate.REGION_CALL - review.BASE
    assert raw[at:at + 4].hex() == proof['ownership']['region_provider']['localized_call_hex']
    base.save(BOOT, deployed | {'resident_main_RAM_proof_region_call_exact': True})


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
    holds = {'warning': (11400, 2351), 'escape': (11200, 2352)}
    observations, transitions, inputs = [], {}, [PROOF, VISUAL, BOOT, QA, Path(__file__)]

    def text(raw, pointer):
        return raw[pointer:pointer + 512].split(b'\0', 1)[0]

    for scenario, (frame, number) in holds.items():
        root = ROOT / f'whale_{scenario}'
        terminal_path = root / 'terminal.json'
        terminal = base.load(terminal_path)
        report_path, commands = Path(terminal['report']), Path(terminal['commands'])
        assert base.digest(report_path) == terminal['report_sha256'] and base.digest(commands) == terminal['commands_sha256']
        assert terminal['unchanged_original_save']
        report = base.load(report_path)
        old_root, end = replay.RUNS[scenario]
        old_terminal = base.load(old_root / 'terminal.json')
        assert base.digest(old_terminal['report']) == old_terminal['report_sha256']
        old_report = base.load(old_terminal['report'])
        assert report['ROM_sha256'] == sha and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['frames'] == end and report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
        donor = report['battery_save_preloaded']
        assert base.digest(donor['source']) == donor['source_sha256'] == old_report['battery_save_preloaded']['source_sha256']
        assert not any(value for key, value in report.items() if key.startswith('synthetic_') and key != 'synthetic_condition_fixtures')
        journal = report_path.with_name('navigation_command_journal.json')
        received = base.load(journal)['commands_received']
        assert all(row['validation_passed'] for row in received)
        assert [row['command'] for row in received] == [loads(line) for line in commands.read_text(encoding='utf-8').splitlines()]
        frames = {item['frame']: item for item in report['frames_captured'] if item['path'].endswith('_navigation.png')}
        snapshots = {item['frame']: item for item in report['read_only_pause_RAM_snapshots']}
        old_snapshots = {item['frame']: item for item in old_report['read_only_pause_RAM_snapshots']}

        def snapshot(frame, source=snapshots):
            item = source[frame]
            assert item['read_only_export'] and base.digest(item['path']) == item['sha256']
            raw = Path(item['path']).read_bytes()
            assert len(raw) == 0x400000
            return raw

        fixture = replay.set_condition if scenario == 'warning' else replay.set_aged_condition
        actual_fixture = []
        for initial, name in ((8327, 'wind'), (9900, 'whale')):
            _, receipt = fixture(arm, snapshot(initial), {'event': name})
            actual_fixture.append(receipt | {'frame': initial})
        assert report['synthetic_condition_fixtures'] == actual_fixture
        raw = snapshot(frame)
        staged = rows[number]
        assert text(raw, owner + 0x2030).hex() == staged['staged_hex']
        formatted = text(raw, wrapped)
        display, = staged['displays']
        assert formatted.hex() == display['display_hex']
        pixels, glyphs = portrait.render_portrait(raster, arm, kanji, formatted)
        image = city.captured(frames[frame])
        mask = bytes(pixel == (0, 8, 0) for pixel in image.crop(city.PAPER).get_flattened_data())
        assert mask == bytes(bool(pixel) for pixel in pixels) and sha256(pixels).hexdigest() == display['native_ink_sha256']
        assert len(glyphs) == display['complete_glyphs']
        observations.append(dict(scenario=scenario, message_ID=number, frame=frame,
            complete_glyphs=len(glyphs), lines=display['visible_lines'], capture=frames[frame], RAM=snapshots[frame]))
        if scenario == 'escape':
            for linked in (11400, 11600, 11800):
                raw, old = snapshot(linked), snapshot(linked, old_snapshots)
                assert text(raw, owner + 0x2030) == text(old, owner + 0x2030)
                if linked != 11400:
                    assert text(raw, wrapped) == text(old, wrapped)
            assert not visible_paper(frames[end]['path'])
            transitions = dict(item_presentation=frames[11400], sympathy=[frames[n] for n in (11600, 11800)],
                               original_return=frames[end])
        inputs.extend((terminal_path, report_path, commands, journal, Path(old_terminal['report'])))

    bindings = {str(path): base.digest(path) for path in inputs}
    ids = [row['message_ID'] for row in observations]
    base.save(LIVE, dict(candidate_sha256=sha, observed_ids=ids, observations=observations, transitions=transitions,
        actual_emulator=True, hardware=False, original_item_follow_up_and_return=True,
        fixture_scope='Original whale condition and one near-expiry timestamp for the escape sequence.',
        oasis_proof_shark_and_other_whale_alternatives_offline=True, evidence=bindings))
    base.save(CHECKPOINT, dict(candidate_sha256=sha, approved_for_registered_successor=True,
        live_messages=ids, stored_cases=71, viewed_pages=125, evidence=bindings | {str(LIVE): base.digest(LIVE)}))
    print(f'Observed white-whale messages {ids}, original item and sympathy follow-ups and return.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('layout', 'startup', 'gameplay'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'layout':
        approve_layout(args.viewed_sheets)
    else:
        {'startup': verify_startup, 'gameplay': verify_gameplay}[args.action]()
