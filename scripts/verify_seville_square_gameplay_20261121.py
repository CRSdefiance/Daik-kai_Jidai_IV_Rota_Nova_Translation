"""Read navigation snapshots and verify naturally triggered Square exchanges."""

from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from struct import unpack
from types import SimpleNamespace

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_seville_square_20261121 as runs
from scripts import verify_lisbon_seoul_trend_gameplay_20261121 as previous


town, base, native = previous.town, runs.base, previous.native
@dataclass(frozen=True)
class Exchange:
    route: int
    town_number: int
    block: int
    count: int
    review: Path
    speakers: dict[int, str]

    @property
    def scene(self):
        return f'/data/SC{self.route}.DK4'


EXCHANGES = {
    'seville': Exchange(0, 13, 188, 10,
        Path('releases/all_routes_editorial_20261121_seville_stockholm_trends_candidate/verification/registered_review.json'),
        {174: 'Owner', 175: 'Cook'}),
    'hamburg': Exchange(1, 5, 193, 17,
        Path('releases/all_routes_editorial_20261120_hamburg_ceramics_candidate/verification/registered_review.json'),
        {147: 'Guildmaster', 82: 'Shopkeeper', 104: 'Trader', 113: 'Port Worker'}),
}


def navigation_state(arm, raw, exchange):
    cpu, get = town.get_machine(arm, raw)
    captain = get(0x7F244)
    assert captain == get(0x2E58C) == exchange.route
    fleet = get(0xCB1A8) + 4 + 132 * captain
    status = get(0x34674, fleet)
    ship_point = displacement = None
    port = get(0xCD6B8, exchange.town_number)
    port_point = tuple(component * 128 for component in unpack('<2i', cpu.mem_read(port + 12, 8)))
    if status == 0x73:
        ship = get(0x36C70, fleet + 12)
        ship_point = unpack('<2i', cpu.mem_read(ship + 16, 8))
        displacement = [b - a for a, b in zip(ship_point, port_point)]
    actor = get(0xCB184) + 0x19E4
    get(0xCC9A8, town.SCRATCH, get(0xCB1B4))
    _, year, month, day, _ = unpack('<5I', cpu.mem_read(town.SCRATCH, 20))
    birthday = [get(0x82F88, actor) + 1, get(0x82F80, actor) + 1]
    active_town = get(0xB65E4)
    assert bytes(cpu.mem_read(town.B, 0x400000)) == raw
    return dict(captain=captain, town=active_town, fleet_status=status, ship_point=ship_point,
                port_point=port_point, displacement_to_port=displacement,
                calendar=[year, month + 1, day + 1], birthday=birthday)


def source_rows(clean, current, event, exchange):
    path, block = exchange.scene, exchange.block
    banks = [native.IlnkContainer.parse(rom.read_file(path)).blocks for rom in (clean, current)]
    original, installed = (bank[block] for bank in banks)
    assert native.digest(original) == event['prior_review']['clean_block_sha256']
    assert native.digest(installed) == event['prior_review']['current_block_sha256']
    rows = [r for r in base.load(exchange.review)['records'] if r['file_path'] == path and r['block'] == block]
    assert len(rows) == event['prior_review']['records'] == exchange.count
    for row in rows:
        refs = [row['source_reference'], row['registered_reference']]
        headers = []
        for payload, ref in zip((original, installed), refs, strict=True):
            assert ref['file_path'] == path and ref['block'] == block
            at, start = ref['offset'], ref['command_offset']
            expected = bytes.fromhex(ref['exact_stored_hex'])
            assert payload[at:at + len(expected)] == expected
            headers.append(payload[start:at + 1])
        assert headers[0] == headers[1] and all(row['review'].values())
    return rows


def observe(current, rows, captures, frame_numbers, speakers):
    arm, font = (current.read_file(name) for name in (native.ARM, '/GRP/KANJI.FNT'))
    context = SimpleNamespace(image=current, arm=arm)
    draw, draw_fe = town.clipped_renderer(context), town.current_fe_painter(context)
    name_font = GameAsciiFont.from_arm9(arm)
    panels, previews = [], []
    for row, number in zip(rows, frame_numbers, strict=True):
        source, stored = row['source_reference'], row['registered_reference']
        selector = row['source_selector']
        body = bytes.fromhex(stored['exact_stored_hex'])[1:]
        if selector == 254:
            result = draw_fe(body)
            plane, width = result['physical'], 228
        else:
            result = draw(arm, font, body)
            page, = result['pages']
            assert page['native_independent_plane_equal']
            plane, width = bytes.fromhex(page['native_plane_hex']), 216
        assert result['complete_consumed_bytes'] == len(body)
        actual, image = town.read_frame(captures, number)
        assert previous.mask_check(plane, width, image), (row['id'], number)
        name = None
        if selector != 254:
            speaker = speakers[selector]
            ink, bounds = previous.complete_mask(name_font, speaker, image, 16, 277, town.INKS[1])
            name = dict(text=speaker, ink_pixels=ink, bounds=bounds)
        panels.append(dict(id=row['id'], japanese=row['Japanese'], english=row['english'],
            source_reference=source, registered_reference=stored, editorial_decision=row['decision'],
            editorial_reason=row['localization_note'], five_gates=row['review'], observed=actual,
            complete_native_body_mask_sha256=native.digest(plane), nameplate=name))
        previews.append((row['id'], image))
    return panels, previews


def verify(folder, plan, current, arm, city, exchange):
    release = base.load(runs.active.RELEASE)
    log = folder / 'capture/capture_report.json'
    journal = folder / 'capture/navigation_command_journal.json'
    contract = folder / 'discovery_source.json'
    report, controls, launch = map(base.load, (log, journal, contract))
    assert report['ROM_sha256'] == launch['candidate_sha256'] == release['candidate_sha256'] == base.digest(runs.active.ROM)
    assert release['registry_sha256'] == base.digest(base.REGISTRY)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
    assert all(row['validation_passed'] for row in controls['commands_received'])
    battery = report['battery_save_preloaded']
    assert battery['copied_byte_exact_before_cold_boot'] and battery['source'] == launch['donor']
    assert battery['source_sha256'] == launch['donor_sha256'] == base.digest(battery['source'])
    clean = base.NdsImage.open(native.CLEAN)
    assert base.digest(native.CLEAN) == release['clean_input_sha256']
    event_index = base.load(town.events.OUTPUT)
    clean_arm = clean.read_file(native.ARM)
    for ref in event_index['clean_identical_native_dependencies']:
        first, end = ref['address'] - town.B, ref['end_exclusive'] - town.B
        assert arm[first:end] == clean_arm[first:end] and native.digest(arm[first:end]) == ref['sha256']
    route = event_index['routes'][exchange.route]
    loaded_events = current.read_file(route['event_archive'])
    assert loaded_events == clean.read_file(route['event_archive'])
    assert native.digest(loaded_events) == route['archive_sha256']
    event, = [r for r in route['entries'] if r['script_block'] == exchange.block]
    assert event['town'] == exchange.town_number and event['facility'] == 0 and event['event_ID'] == exchange.block
    assert event['date_comparison'] == 1 and route['scene_archive'] == exchange.scene
    rows = source_rows(clean, current, event, exchange)
    captures = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('_navigation.png')}
    shots = plan['panels']
    assert plan['docked'] < plan['entry'] < min(shots) and shots == sorted(set(shots)) and max(shots) < plan['returned']
    assert report['frames'] == plan['returned']
    panels, previews = observe(current, rows, captures, shots, exchange.speakers)
    states = {row['frame']: row for row in report['read_only_pause_RAM_snapshots']}
    retained_states = {}
    for key in ('docked', 'entry', 'returned'):
        state = states[plan[key]]
        assert state['read_only_export'] and base.digest(state['path']) == state['sha256']
        assert navigation_state(arm, Path(state['path']).read_bytes(), exchange)['town'] == exchange.town_number
        retained_states[key] = state
    waiting = Path(retained_states['entry']['path']).read_bytes()
    at = waiting.index(loaded_events[:96])
    assert waiting.find(loaded_events[:96], at + 1) == -1
    cpu, get = town.get_machine(arm, waiting)
    assert get(0x23840, town.B + at - 0x30, event['event_ID']) == 0
    assert bytes(cpu.mem_read(town.B, 0x400000)) == waiting
    final = report['read_only_RAM_snapshot']
    state = navigation_state(arm, Path(final['path']).read_bytes(), exchange)
    completion = previous.event_completion(arm, report, loaded_events, event, dict(route=exchange.route,
        final_calendar=state['calendar'][1:], birthday=state['birthday']))
    transitions = {key: town.read_frame(captures, number)[0] for key, number in plan.items() if key != 'panels'}
    _, close = town.read_frame(captures, plan['returned'])
    previews.append((f'Returned to {city.title()} Square', close))
    sheets = []
    for at in range(0, len(previews), 6):
        image = folder / f'{city}_exchange_{at // 6 + 1}.png'
        town.sheet(previews[at:at + 6], image)
        sheets.append(dict(path=str(image), sha256=base.digest(image)))
    path = folder / f'verified_{city}_square.json'
    assert not path.exists()
    base.save(path, dict(candidate_sha256=release['candidate_sha256'], original_ordinary_Square_activation=True,
        route=exchange.route, file_path=exchange.scene, block=exchange.block,
        panels=panels, observations=transitions, completion=completion,
        retained_read_only_snapshots=retained_states, original_completion_flag_before_entry=0,
        hardware_verified=False, existing_editorial_credit_retained=True, new_editorial_credit=0,
        screenshots=sheets, evidence={str(p): base.digest(p) for p in
            (log, journal, contract, town.events.OUTPUT, exchange.review)}))
    print(f'Verified {len(panels)} {city.title()} panels, speaker labels, the matching date and the event-completion flag.')


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--town', choices=EXCHANGES, default='seville')
    parser.add_argument('--folder', type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--inspect', type=Path, help='Inspect a read-only ARM9 snapshot.')
    mode.add_argument('--plan', type=Path, help='Verify a completed replay using its observed frame map.')
    args = parser.parse_args()
    current = base.NdsImage.open(runs.active.ROM)
    arm = current.read_file(native.ARM)
    exchange = EXCHANGES[args.town]
    if args.inspect:
        print(navigation_state(arm, args.inspect.read_bytes(), exchange))
    else:
        verify(args.folder or runs.VOYAGES[args.town][0], base.load(args.plan), current, arm, args.town, exchange)


if __name__ == '__main__':
    main()
