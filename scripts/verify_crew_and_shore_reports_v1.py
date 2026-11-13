"""Verify shore reports, original event transitions and all final portrait pages."""

import argparse
from hashlib import sha256
from json import loads
from pathlib import Path
from struct import unpack_from
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree

from scripts import replay_crew_and_shore_reports_v1 as replay
from scripts import verify_city_combat_notices_live_v1 as city
from scripts import verify_item_production_advice_v1 as startup
from scripts.navigate_hot_spring_crew_v1652 import visible_paper
from scripts.verify_personal_gameplay_v841 import get_machine


stage, base = replay.stage, replay.base
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
BIOGRAPHIES = replay.prior.STARTUP.parent
BOOT, VISUAL = ROOT / 'own_startup_verification.json', ROOT / 'visual_layout_review.json'
LIVE, CHECKPOINT = ROOT / 'crew_and_shore_reports_gameplay_verification.json', ROOT / 'approved_checkpoint.json'
QA = Path('work/crew_and_shore_reports_repo_qa_20261111.xml')
review, portrait = stage.first.review, stage.first.first.portrait


def approve_layout(viewed):
    assert not VISUAL.exists()
    proof = base.load(PROOF)
    assert base.digest(ROM) == proof['research_ROM_sha256'] and base.digest(stage.OUTPUT) == proof['manuscript_sha256']
    assert viewed == [row['sha256'] for row in proof['sheets']]
    assert all(base.digest(row['path']) == row['sha256'] for row in proof['sheets'])
    assert len(proof['records']) == proof['native_pages'] == proof['native_cases'] == 56
    assert sum(len(row['messages']) for row in proof['sheets']) == 56
    suites = list(ElementTree.parse(QA).iter('testsuite'))
    assert sum(int(row.get('tests', 0)) for row in suites) == 34
    assert all(int(row.get(key, 0)) == 0 for row in suites for key in ('errors', 'failures', 'skipped'))
    records = {case['message_ID']: case['displays'][0] for case in proof['records']}
    assert max(len(case['visible_lines']) for case in records.values()) == 4
    assert all(any(phrase in line for line in records[number]['visible_lines'])
               for number, phrases in stage.PHRASES.items() for phrase in phrases)
    base.save(VISUAL, dict(candidate_sha256=proof['research_ROM_sha256'], stored_cases=56, native_pages=56,
        all_pages_viewed=True, complete_glyphs_and_bounds=True, repository_tests=34, sheet_sha256=viewed,
        complete_question_and_phrase_controls=stage.PHRASES,
        deliberate_comic_pause=dict(message_ID=2200, note='The sarcastic last sentence is the captain’s second beat.'),
        evidence={str(path): base.digest(path) for path in (PROOF, stage.OUTPUT, QA, Path(__file__))},
        representative_gameplay_and_registration_pending=True, new_credit=0))
    print('Approved 56 viewed pages, complete glyphs, the scoped phrases and 34 tests.')


def verify_startup():
    loader = SimpleNamespace(load=base.load, RELEASE=review.parent.RELEASE, NdsImage=base.NdsImage, ARM=review.ARM)
    FunctionType(startup.verify_startup.__code__, vars(startup) | globals() | {'stage': loader, 'startup': startup.startup})()


def fleet_state(arm, raw):
    cpu, get = get_machine(arm, raw)
    fleet = get(0xCB1A8) + 4 + 132 * get(0x2E58C)
    assert get(0x2E58C) == get(0x7F244) == 1
    mobiles = [get(0x36C70, fleet + 12 + slot * 8) for slot in range(5)]
    assert all(mobiles)
    scratch = 0x02450000
    get(0x34EB0, fleet, scratch)
    resources = list(unpack_from('<2I', cpu.mem_read(scratch, 8)))
    return dict(water_and_food=resources, crew=[get(0x55444, obj) for obj in mobiles],
        original_mode=list(unpack_from('<3I', cpu.mem_read(get(0x3F0F8) + 8, 12))))


def verify_gameplay():
    assert not LIVE.exists() and not CHECKPOINT.exists()
    proof, layout, boot = map(base.load, (PROOF, VISUAL, BOOT))
    sha = base.digest(ROM)
    assert sha == proof['research_ROM_sha256'] == layout['candidate_sha256'] == boot['candidate_sha256']
    rom = base.NdsImage.open(ROM)
    arm = rom.read_file(review.ARM)
    raster, _, _ = portrait.font_tools(rom)
    kanji = rom.read_file('/GRP/KANJI.FNT')
    owner, wrapped, modal = [unpack_from('<I', arm, offset)[0] - review.BASE for offset in (0x552A0, 0x54450, 0x54894)]
    groups = {row['first_ID']: row for row in base.load(stage.OUTPUT)['native_context']}
    rows = {case['message_ID']: case for case in proof['records']}
    cases = {'attack': ((20322, 2243),), 'welcome': ((45956, 2234), (46396, 2239))}
    observations, transitions, inputs = [], {}, [PROOF, VISUAL, BOOT, QA, Path(__file__)]

    def text(raw, pointer):
        return raw[pointer:pointer + 512].split(b'\0', 1)[0]

    for name, expected in cases.items():
        root = ROOT / f'shore_{name}'
        terminal_path = root / 'terminal.json'
        terminal = base.load(terminal_path)
        report_path, commands = Path(terminal['report']), Path(terminal['commands'])
        assert base.digest(report_path) == terminal['report_sha256'] and base.digest(commands) == terminal['commands_sha256']
        assert terminal['unchanged_original_save']
        old_plan, old_path, old_report, donor, _, historical_commands, end = replay.history(name)
        assert str(old_path) == terminal['historical_report'] and base.digest(old_path) == terminal['historical_report_sha256']
        assert base.digest(donor) == old_plan['source_donor_sha256']
        report = base.load(report_path)
        assert report['ROM_sha256'] == sha and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['frames'] == end and report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
        assert not any(value for key, value in report.items() if key.startswith('synthetic_')
                       and key != 'synthetic_battle_recovery_proximity_fixtures')
        journal = report_path.with_name('navigation_command_journal.json')
        received = base.load(journal)['commands_received']
        assert all(row['validation_passed'] for row in received)
        assert [row['command'] for row in received] == [loads(line) for line in commands.read_text(encoding='utf-8').splitlines()]
        assert [row['command'] for row in received] == historical_commands
        frames = {item['frame']: item for item in report['frames_captured'] if item['path'].endswith('_navigation.png')}
        snapshots = {item['frame']: item for item in report['read_only_pause_RAM_snapshots']}
        old_snapshots = {item['frame']: item for item in old_report['read_only_pause_RAM_snapshots']}

        def snapshot(frame, source=snapshots):
            item = source[frame]
            assert item['read_only_export'] and base.digest(item['path']) == item['sha256']
            raw = Path(item['path']).read_bytes()
            assert len(raw) == 0x400000
            return raw

        requests = {row['frame']: row['command']['battle_fixture'] for row in received if 'battle_fixture' in row['command']}
        recorded = report['synthetic_battle_recovery_proximity_fixtures']
        assert len(recorded) == len(requests)
        fixture = replay.fixtures(proof['research_ARM9_sha256'])
        for case in recorded:
            frame = case['frame']
            _, verified = fixture(arm, snapshot(frame), requests[frame])
            assert case == verified | {'frame': frame}

        for frame, group_start in expected:
            raw = snapshot(frame)
            group = groups[group_start]
            cpu, get = get_machine(arm, raw)
            identity = get(0x82478, get(0xCB1A8) + 0x2090, group['original_role_argument'])
            actor = get(0xCB184) + (0x19E4 if identity == get(0x7F244) else 4 + 32 * identity)
            number = get(0x53F4C, actor, group['table'])
            assert group['first_ID'] <= number <= group['last_ID']
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
            observations.append(dict(scenario=name, message_ID=number, frame=frame, native_table=group['table'],
                actor_ID=identity, complete_glyphs=len(glyphs), lines=display['visible_lines'], capture=frames[frame], RAM=snapshots[frame]))

        follow = 20542 if name == 'attack' else 46176
        old_hold, new_hold = snapshot(follow, old_snapshots), snapshot(follow)
        assert text(old_hold, modal) == text(new_hold, modal)
        expected_template = b'Sailors lost: %s.' if name == 'attack' else b'Fatigue decreased by %s.'
        assert text(new_hold, owner + 0x2030) == expected_template
        before = fleet_state(arm, snapshot(expected[0][0]))
        after = fleet_state(arm, snapshot(end))
        assert before == fleet_state(arm, snapshot(expected[0][0], old_snapshots))
        assert after == fleet_state(arm, snapshot(end, old_snapshots))
        if name == 'attack':
            assert sum(before['crew']) - sum(after['crew']) == 10
        else:
            assert before['crew'] == after['crew']
        assert after['original_mode'] == [0, 0, 0] and not visible_paper(city.captured(frames[end]))
        transitions[name] = dict(original_follow_up_template=expected_template.decode('ascii'), follow_up_frame=follow,
            formatted_status_hex=text(new_hold, modal).hex(), before=before, after=after,
            return_frame=end, return_capture=frames[end], fixture_count=len(recorded))
        inputs.extend((terminal_path, report_path, commands, journal, old_path))

    bindings = {str(path): base.digest(path) for path in inputs}
    ids = sorted({row['message_ID'] for row in observations})
    base.save(LIVE, dict(candidate_sha256=sha, observed_ids=ids, observations=observations, transitions=transitions,
        actual_emulator=True, hardware=False, both_sequences_return_to_sailing=True,
        representative_scope='Original Search choices, original RNG, copied saves and disclosed setup fixtures.',
        captain_reprimand_and_other_shore_events_offline=True, evidence=bindings))
    base.save(CHECKPOINT, dict(candidate_sha256=sha, approved_for_registered_successor=True,
        live_messages=ids, stored_cases=56, viewed_pages=56, evidence=bindings | {str(LIVE): base.digest(LIVE)}))
    print(f'Observed shore messages {ids}, original status follow-ups and both returns to sailing.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('layout', 'startup', 'gameplay'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'layout':
        approve_layout(args.viewed_sheets)
    else:
        {'startup': verify_startup, 'gameplay': verify_gameplay}[args.action]()
