"""Verify naturally triggered Lisbon sailing instructions against exact stored pages."""

from argparse import ArgumentParser
from pathlib import Path
from struct import unpack
from types import SimpleNamespace

from scripts import check_rafael_sailing_lisbon_eligibility_20261121 as entry
from scripts import verify_seville_square_gameplay_20261121 as town_checks


replay = entry.replay
base, active = replay.base, replay.active
native = active.native
town = town_checks.town
ROOT = replay.ROOT
PROOF = ROOT / 'verified_sailing_lesson.json'
PACKAGE = Path('releases/all_routes_editorial_20261119_rafael_sail_controls_candidate/verification')
REVIEW = PACKAGE / 'registered_review.json'
PRIOR_GAMEPLAY = PACKAGE / 'live_display.json'
STORED = PACKAGE / 'stored_proof.json'
SPEAKERS = {0: 'Rafael Castor', 4: 'Janus Pasar', 5: 'Claudio Manaus', 6: 'Julio Erneco'}


def text_planes(arm, current, clean):
    binding = base.load(replay.BINDING)
    group, = base.load(STORED)['groups']
    path, block = binding['scene_archive'], binding['block']
    assert group['file_path'] == path and group['block'] == block
    original, installed = [native.IlnkContainer.parse(rom.read_file(path)).blocks[block] for rom in (clean, current)]
    assert native.digest(original) == binding['clean_scene_block_sha256'] == group['source']
    assert native.digest(installed) == binding['installed_scene_block_sha256'] == group['after']
    rows = base.load(REVIEW)['records']
    assert len(rows) == 45
    context = SimpleNamespace(arm=arm, image=current)
    draw, fe = town.clipped_renderer(context), town.current_fe_painter(context)
    font = current.read_file('/GRP/KANJI.FNT')
    for row in rows:
        assert row['file_path'] == path and row['block'] == block and all(row['review'].values())
        source, output = row['source_reference'], row['registered_reference']
        refs = []
        for data, ref in ((original, source), (installed, output)):
            pos, start = ref['offset'], ref['command_offset']
            raw = bytes.fromhex(ref['exact_stored_hex'])
            assert pos == start + 5 and data[pos:pos + len(raw)] == raw
            refs.append(data[start:pos + 1])
        assert refs[0] == refs[1] == bytes.fromhex('0040ffff00') + bytes([row['source_selector']])
        selector = row['source_selector']
        raw = bytes.fromhex(output['exact_stored_hex'])[1:]
        assert not any(token in raw for token in (b'FA', b'FO'))
        expanded = raw.replace(b'FI', b'Rafael')
        if selector == 254:
            paint = fe(expanded)
            pixels, width = paint['physical'], 228
        else:
            paint = draw(arm, font, expanded)
            page, = paint['pages']
            assert page['native_independent_plane_equal']
            pixels, width = bytes.fromhex(page['native_plane_hex']), 216
        assert paint['complete_consumed_bytes'] == len(expanded)
        yield row, width, pixels


def state_at(frame, snapshots, arm, ev):
    shot = snapshots[frame]
    assert shot['read_only_export'] and base.digest(shot['path']) == shot['sha256']
    state = entry.getters(arm, ev, Path(shot['path']).read_bytes())
    return dict(snapshot=shot, **state)


def verify(plan):
    assert not PROOF.exists()
    files = (ROOT / 'capture/capture_report.json', ROOT / 'capture/navigation_command_journal.json',
             ROOT / 'arrival_source.json', active.RELEASE, replay.BINDING, entry.PROOF)
    report, journal, launch, release, binding, eligible = map(base.load, files)
    candidate = base.digest(active.ROM)
    assert candidate == release['candidate_sha256'] == launch['candidate_sha256'] == binding['candidate_sha256']
    assert candidate == report['ROM_sha256'] == journal['ROM_sha256'] == eligible['candidate_sha256']
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(replay.PRIOR) == launch['prior_report_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    assert all(command['validation_passed'] for command in journal['commands_received'])
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and donor['source'] == launch['donor']
    assert donor['source_sha256'] == launch['donor_sha256'] == base.digest(donor['source'])
    assert report['frames'] == plan['return_to_sea']

    clean, current = map(base.NdsImage.open, (native.CLEAN, active.ROM))
    arm = current.read_file(native.ARM)
    ev = current.read_file(binding['events_archive'])
    assert ev == clean.read_file(binding['events_archive']) and native.digest(ev) == binding['events_archive_sha256']
    states = {x['frame']: x for x in report['read_only_pause_RAM_snapshots']}
    before = state_at(plan['before_departure'], states, arm, ev)
    activated = state_at(plan['panels'][0], states, arm, ev)
    after = state_at(plan['return_to_sea'], states, arm, ev)
    assert before['town'] == entry.Lisbon and before['event_completion'] == {48: 0, 128: 0, 139: 1}
    assert activated['original_event_context'][:2] == [6, entry.Lisbon]
    assert after['town'] == after['fleet_location_state'] == 115
    assert after['event_completion'] == {48: 0, 128: 1, 139: 1}
    ram = Path(after['snapshot']['path']).read_bytes()
    cpu, get = entry.get_machine(arm, ram)
    captain = get(0xCB184) + 0x19E4
    # The original name getter is the source for the live FI substitution.
    vtable, = unpack('<I', cpu.mem_read(captain, 4))
    getter, = unpack('<I', cpu.mem_read(vtable + 8, 4))
    name_ptr = get(getter - entry.BASE, captain)
    assert bytes(cpu.mem_read(name_ptr, 14)).startswith(b'Rafael Castor\0')

    expected = list(text_planes(arm, current, clean))
    name_font = town_checks.GameAsciiFont.from_arm9(arm)
    captured = {x['frame']: x for x in report['frames_captured'] if x['path'].endswith('_navigation.png')}
    sequence = plan['panels']
    assert sequence == sorted(set(sequence)) and len(sequence) >= 40
    assert plan['before_departure'] < sequence[0] < sequence[-1] < plan['departure_notice'] < plan['return_to_sea']
    panels, previews, following = [], [], 0
    for frame in sequence:
        actual, image = town.read_frame(captured, frame)
        matches = []
        for index in range(following, len(expected)):
            row, width, mask = expected[index]
            if not town_checks.previous.mask_check(mask, width, image):
                continue
            speaker = SPEAKERS.get(row['source_selector'])
            if speaker:
                try:
                    town_checks.previous.complete_mask(name_font, speaker, image, 16, 277, town.INKS[1])
                except ValueError:
                    continue
            matches.append(index)
        assert matches, (frame, following)
        index = matches[0]
        row, width, mask = expected[index]
        following = index + 1
        panels.append(dict(id=row['id'], source_reference=row['source_reference'],
            registered_reference=row['registered_reference'], english=row['english'], decision=row['decision'],
            speaker=SPEAKERS.get(row['source_selector']), selector=row['source_selector'],
            complete_native_glyph_mask=native.digest(mask), observed=actual))
        previews.append((row['id'], image))
    assert panels[0]['id'] == 'DK4_MES_B128_R0012' and panels[-1]['id'] == 'DK4_MES_B128_R0210'
    returned, image = town.read_frame(captured, plan['return_to_sea'])
    notice, notice_image = town.read_frame(captured, plan['departure_notice'])
    previews.append(('Lisbon departure notice', notice_image))
    previews.append(('Return to Sea View', image))
    departure, _ = town.read_frame(captured, plan['before_departure'])
    observed = {p['id'] for p in panels}
    unseen = sorted(row['id'] for row, _, _ in expected if row['id'] not in observed)
    sheets = []
    for at in range(0, len(previews), 6):
        image = ROOT / f'lisbon_sailing_lesson_{at // 6 + 1}.png'
        town.sheet(previews[at:at + 6], image)
        sheets.append(dict(path=str(image), sha256=base.digest(image)))
    base.save(PROOF, dict(candidate_sha256=candidate, original_Lisbon_departure_activation=True,
        natural_activation=True, slot=0, before_departure=before, first_lesson_panel=activated,
        departure_return=after, ordinary_emulator_without_synthetic_state=True,
        hardware_verified=False, panels=panels, unobserved_records=unseen,
        previous_initialized_unvisited=base.load(PRIOR_GAMEPLAY)['unvisited'],
        departure_screen=departure, original_departure_notice=notice, final_screen=returned,
        new_editorial_credit=0, sheets=sheets,
        evidence={str(p): base.digest(p) for p in (*files, REVIEW, PRIOR_GAMEPLAY, STORED)}))
    print(f'Verified {len(panels)} naturally triggered Lisbon sailing panels and the original Sea View return.')


if __name__ == '__main__':
    arg = ArgumentParser(description=__doc__)
    arg.add_argument('--plan', type=Path, required=True)
    verify(base.load(arg.parse_args().plan))
