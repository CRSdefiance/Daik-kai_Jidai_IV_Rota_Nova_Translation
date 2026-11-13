"""Verify the deployed bearing wrapper and the live Hamburg retreat sequence."""

import argparse
from hashlib import sha256
from inspect import getsource
from pathlib import Path
from struct import unpack_from
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree

from ndspy.code import MainCodeFile

from dk4tool.patch import pirate_report_bearings_v1 as bearings
from scripts import replay_pirate_and_retreat_reports_v1 as replay
from scripts import verify_city_combat_notices_live_v1 as city
from scripts import verify_item_production_advice_v1 as startup
from scripts.source_locked_derivation_v5118 import checked_text


stage, base = replay.stage, replay.base
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
BIOGRAPHIES = replay.prior.STARTUP.parent
BOOT, VISUAL = ROOT / 'own_startup_verification.json', ROOT / 'visual_layout_review.json'
LIVE = ROOT / 'pirate_and_retreat_reports_gameplay_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = Path('work/pirate_and_retreat_reports_repo_qa_20261111.xml')
review = stage.first.review
portrait = stage.first.first.portrait


def queued_portrait():
    source = getsource(portrait.with_arguments)
    anchor = "    env = {**portrait_case.__globals__, 'ARGUMENT_MEMORY': 0x02470000}"
    source = checked_text(source, {anchor: '''    source = checked_text(source, {
        'actor_id, arguments):': 'actor_id, arguments, original_bearing):',
        'pointers.extend([0] * (2 - len(pointers)))': 'pointers[0] = original_bearing',
        'cpu.emu_start(BASE + entry, STOP, count=3000000)': 'cpu.emu_start(BEARING_CALL, STOP, count=3000000)',
        'original_entry=BASE + entry': 'original_entry=BEARING_CALL',
    })
''' + anchor + "\n    env['BEARING_CALL'] = BEARING_CALL"})
    env = vars(portrait) | {'BEARING_CALL': bearings.CALL}
    exec(compile(source, __file__ + '::queued-pirate-call', 'exec'), env)
    return env['with_arguments']()


def focused_bearings(proof, draft):
    parent = base.load(review.parent.RELEASE)
    original = review.prior.RegisteredRuntime(review.parent.RELEASE, parent['own_registered_startup'], captain=3)
    assert original.receipt() == draft['registered_input']
    image = base.NdsImage.open(ROM)
    arm, common = image.read_file(review.ARM), image.read_file(review.COMMON)
    ctx = portrait.with_components(original, arm, common)
    at = bearings.CALL - review.BASE
    binding = proof['ownership']['bearing']
    assert ctx.raw[at:at + 4] == original.arm[at:at + 4] == bytes.fromhex(binding['original_call_hex'])
    assert arm[at:at + 4] == bytes.fromhex(binding['localized_call_hex'])
    ctx.raw = ctx.raw[:at] + arm[at:at + 4] + ctx.raw[at + 4:]
    queued = queued_portrait()
    rows = {row['message_ID']: row for row in draft['records']}
    groups = {group['first_ID']: group for group in draft['native_context']}
    checks = []
    for case in proof['records']:
        number = case['message_ID']
        row = rows[number]
        group = groups[row['native_group_first_ID']]
        if group['argument_kind'] != 'bearing_and_pirate':
            continue
        group = group | {'consumer': bearings.WRAPPER}
        actor = next(i for i, _, msg in group['original_voice_choices'] if msg == number)
        for display in case['displays']:
            sample = display['argument_sample']
            arguments = tuple(bytes.fromhex(value) for value in sample['arguments'])
            pointer = sample['bearing']['source_pointer']
            result = queued(ctx, row, group, bytes.fromhex(case['staged_hex']), actor, arguments, pointer)
            assert result.pop('display').hex() == display['display_hex']
            checks.append(dict(message_ID=number, original_bearing_pointer=pointer,
                original_call=bearings.CALL, pirate_name=arguments[1].decode('ascii'),
                display_hex=display['display_hex'], native=result))
    assert len(checks) == 20
    return checks


def approve_layout(viewed):
    assert not VISUAL.exists()
    proof, draft = map(base.load, (PROOF, stage.OUTPUT))
    assert base.digest(ROM) == proof['research_ROM_sha256'] and base.digest(stage.OUTPUT) == proof['manuscript_sha256']
    assert viewed == [row['sha256'] for row in proof['sheets']]
    assert all(base.digest(row['path']) == row['sha256'] for row in proof['sheets'])
    assert len(proof['records']) == 48 and proof['native_pages'] == proof['native_cases'] == 71
    assert sum(len(row['messages']) for row in proof['sheets']) == 71
    suites = list(ElementTree.parse(QA).iter('testsuite'))
    assert sum(int(row.get('tests', 0)) for row in suites) == 34
    assert all(int(row.get(key, 0)) == 0 for row in suites for key in ('errors', 'failures', 'skipped'))
    assert len(proof['ownership']['bearing_controls']) == 22
    base.save(VISUAL, dict(candidate_sha256=proof['research_ROM_sha256'], stored_cases=48, native_pages=71,
        all_pages_viewed=True, complete_glyphs_and_bounds=True, repository_tests=34, sheet_sha256=viewed,
        offline_original_queued_portraits=focused_bearings(proof, draft),
        offline_initialized_CPU_scope='Staged COMMON metadata and the four owned pirate call bytes applied to the parent startup snapshot.',
        complete_word_breaks_retained=dict(Peralonso=[2621, 2623, 2624, 2626, 2627, 2631, 2632], Jean=[2628]),
        evidence={str(path): base.digest(path) for path in (PROOF, stage.OUTPUT, QA, Path(__file__))},
        representative_gameplay_and_registration_pending=True, new_credit=0))
    print('Approved 71 viewed pages, 20 end-to-end queued portraits, 22 bearing controls and 34 tests.')


def verify_startup():
    loader = SimpleNamespace(load=base.load, RELEASE=review.parent.RELEASE, NdsImage=base.NdsImage, ARM=review.ARM)
    FunctionType(startup.verify_startup.__code__, vars(startup) | globals() | {'stage': loader, 'startup': startup.startup})()
    proof = base.load(PROOF)
    deployed = base.load(BOOT)
    raw = Path(deployed['read_only_snapshot']['path']).read_bytes()
    arm = base.NdsImage.open(ROM).read_file(review.ARM)
    bearing = proof['ownership']['bearing']
    tail = MainCodeFile(arm, review.BASE).sections[-1]
    at = bearing['extension'] - tail.ramAddress
    payload = bytes(tail.data[at:at + bearing['bytes']])
    assert len(payload) == bearing['bytes']
    at = bearings.CALL - review.BASE
    assert raw[at:at + 4].hex() == bearing['localized_call_hex']
    base.save(BOOT, deployed | dict(resident_main_RAM_pirate_call_exact=True,
        ROM_bearing_extension_sha256=sha256(payload).hexdigest(), startup_export_contains_only_main_RAM=True))


def verify_gameplay():
    assert not LIVE.exists() and not CHECKPOINT.exists()
    proof, layout, boot = map(base.load, (PROOF, VISUAL, BOOT))
    sha = base.digest(ROM)
    assert sha == proof['research_ROM_sha256'] == layout['candidate_sha256'] == boot['candidate_sha256']
    terminal_path = replay.ROOT / 'terminal.json'
    terminal = base.load(terminal_path)
    report_path, commands = Path(terminal['report']), Path(terminal['commands'])
    assert base.digest(report_path) == terminal['report_sha256'] and base.digest(commands) == terminal['commands_sha256']
    predecessor = base.load(replay.prior.ROOT / 'terminal.json')
    assert terminal['commands_sha256'] == predecessor['commands_sha256'] and terminal['unchanged_original_save']
    report = base.load(report_path)
    assert terminal['candidate_sha256'] == report['ROM_sha256'] == sha
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == replay.prior.prior.DONOR_SHA
    frames = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('_navigation.png')}
    snapshots = {row['frame']: row for row in report['read_only_pause_RAM_snapshots']}
    rom = base.NdsImage.open(ROM)
    arm = rom.read_file(review.ARM)
    raster, _, _ = portrait.font_tools(rom)
    kanji = rom.read_file('/GRP/KANJI.FNT')
    wrapped = unpack_from('<I', arm, 0x54450)[0] - review.BASE

    def snapshot(frame):
        row = snapshots[frame]
        assert row['read_only_export'] and base.digest(row['path']) == row['sha256']
        raw = Path(row['path']).read_bytes()
        assert len(raw) == 0x400000
        return raw

    def visible(raw):
        return raw[wrapped:wrapped + 256].split(b'\0', 1)[0]

    assert b'Hamburg' in visible(snapshot(24200))
    cases = {row['message_ID']: row for row in proof['records']}
    observations = []
    for frame, number in ((25100, 2651), (25500, 2657)):
        raw = snapshot(frame)
        text = visible(raw)
        display, = cases[number]['displays']
        assert text.hex() == display['display_hex'], (number, text)
        pixels, glyphs = portrait.render_portrait(raster, arm, kanji, text)
        live_ink = bytes(pixel == (0, 8, 0) for pixel in city.captured(frames[frame]).crop(city.PAPER).get_flattened_data())
        assert live_ink == bytes(bool(pixel) for pixel in pixels)
        assert len(glyphs) == display['complete_glyphs'] and sha256(pixels).hexdigest() == display['native_ink_sha256']
        observations.append(dict(message_ID=number, frame=frame, visible_hex=text.hex(), lines=display['visible_lines'],
            complete_glyphs=len(glyphs), state=city.get_state(arm, raw), capture=frames[frame], RAM=snapshots[frame]))
    assert observations[-1]['state']['order'] == [6, 0]
    end = report['frames']
    returned = city.get_state(arm, snapshot(end))
    assert end == 25900 and returned['clock'] > observations[-1]['state']['clock']
    assert frames[end]['framebuffer_sha256'] != observations[-1]['capture']['framebuffer_sha256']
    bindings = {str(path): base.digest(path) for path in (PROOF, VISUAL, BOOT, QA, Path(__file__),
        terminal_path, report_path, commands)}
    ids = [row['message_ID'] for row in observations]
    base.save(LIVE, dict(candidate_sha256=sha, observed_ids=ids, observations=observations,
        actual_emulator=True, hardware=False, original_attack_order_and_report=True,
        original_A_advance_and_return_to_sailing=True, returned=returned, returned_capture=frames[end],
        pirate_bearing_display_verified_offline=True, live_pirate_activation=False, evidence=bindings))
    base.save(CHECKPOINT, dict(candidate_sha256=sha, approved_for_registered_successor=True,
        live_messages=ids, stored_cases=48, viewed_pages=71, evidence=bindings | {str(LIVE): base.digest(LIVE)}))
    print('Verified the original Hamburg retreat, nearby-port order and return to sailing.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('layout', 'startup', 'gameplay'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'layout':
        approve_layout(args.viewed_sheets)
    else:
        {'startup': verify_startup, 'gameplay': verify_gameplay}[args.action]()
