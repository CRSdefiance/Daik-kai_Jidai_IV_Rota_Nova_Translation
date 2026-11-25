"""Exercise the four-option Port menu after Narvik develops through ordinary input."""

from argparse import ArgumentParser
from hashlib import sha256
from io import StringIO
from json import dumps
from pathlib import Path
from struct import pack
import sys
from types import FunctionType

from scripts import headless_desmume_v193 as harness
from scripts import native_location_fixture_v519 as location
from scripts import native_village_location_v606 as center
from scripts import register_barmaid_town_labels_20261115 as base_release


base = base_release.base
ROOT = Path('work/crew_ui_visible_audit_20261115_v1')
HISTORY = Path('E:/Rota Nova translations/Generated/work/emulation_v193/'
               'village_development_v665_15_first/capture_report.json')
CAPTURES = (9880, 10680, 12580, 12980, 13200, 14100, 14400, 14800)
ACTIONS = ((13001, 'A'), (13801, 'A'), (14201, 'DOWN'), (14501, 'A'))
VILLAGE = 15


def replay(rom, folder, candidate_sha):
    assert base.digest(rom) == candidate_sha
    prior = base.load(HISTORY)
    assert prior['frames'] == 12980 and prior['cold_boot'] and not prior['savestate_loaded']
    old, = prior['synthetic_location_fixtures']
    assert old['village_id'] == VILLAGE and old['only_eight_ship_coordinate_bytes_owned']
    donor = prior['battery_save_preloaded']
    assert base.digest(donor['source']) == donor['source_sha256']
    events = prior['scripted_input_schedule'] + [
        dict(start=at, duration=8, buttons=[key]) for at, key in ACTIONS]
    folder.mkdir(parents=True)
    inputs = folder / 'inputs.json'
    base.save(inputs, events)

    image, original = map(base.NdsImage.open, (rom, base_release.stage.CLEAN))
    arm_path = base_release.stage.ARM
    source = original.read_file(arm_path)
    world = image.read_file('/data/WORLDMAP.DK4')
    assert world == original.read_file('/data/WORLDMAP.DK4')
    assert sha256(world).hexdigest() == old['terrain_proof']['WORLDMAP_sha256']
    assert image.rom.loadArm9Overlays()[0].data == original.rom.loadArm9Overlays()[0].data
    terrain_point = old['expected_selector_point_after_original_update']
    assert any(q['map_point'] == terrain_point and q['collision_free'] for q in old['terrain_proof']['queries'])

    def relocate(arm, raw, village):
        assert village == VILLAGE and arm == image.read_file(arm_path)
        assert all(arm[lo:hi] == source[lo:hi] for lo, hi in old['original_reference_code_spans_exact_current'])
        probe = FunctionType(center.relocate.__code__, vars(center) | {'ARM_SHA': sha256(arm).hexdigest()})
        _, proof = probe(arm, raw, village)
        assert proof['village_point'] == old['village_point']
        target = [n * 128 for n in terrain_point]
        offset = proof['active_ship'] - center.BASE + 16
        result = raw[:offset] + pack('<2i', *target) + raw[offset + 8:]
        return result, proof | dict(after_ship_fixed_point=target,
            expected_selector_point_after_original_update=terrain_point,
            changes=[dict(address=center.BASE + i, before=raw[i], after=result[i])
                     for i in range(offset, offset + 8) if raw[i] != result[i]],
            after_RAM_sha256=sha256(result).hexdigest(), previous_terrain_proof=str(HISTORY),
            previous_terrain_proof_sha256=base.digest(HISTORY))

    argv = [harness.__file__, '--rom', str(rom), '--out', str(folder / 'capture'),
        '--inputs-json', str(inputs), '--battery-save', donor['source'], '--touchscreen',
        '--press-start', '-1', '--frames', '14801', '--capture-every', '999999',
        '--capture-at', *map(str, CAPTURES), '--pause-at', '5200',
        '--dump-pause-ram', '--allow-location-fixtures']
    commands = ({'until': 5400, 'location_town': VILLAGE}, {'until': 12980}, {'until': 14100},
                {'until': 14400}, {'until': 14800}, {'stop': True})
    original_fixture, old_input, old_args = location.relocate, sys.stdin, sys.argv
    try:
        location.relocate, sys.stdin, sys.argv = relocate, StringIO(''.join(dumps(row) + '\n' for row in commands)), argv
        harness.main()
    finally:
        location.relocate, sys.stdin, sys.argv = original_fixture, old_input, old_args
    report_path = folder / 'capture/capture_report.json'
    report = base.load(report_path)
    assert report['ROM_sha256'] == candidate_sha and report['frames'] == 14800
    assert report['scripted_input_schedule'] == events and not report['callback_errors']
    assert len(report['synthetic_location_fixtures']) == 1
    assert base.digest(donor['source']) == donor['source_sha256']


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, default=base_release.ROM)
    parser.add_argument('--sha256', default=base.load(base_release.RELEASE)['candidate_sha256'])
    parser.add_argument('--out', type=Path, default=ROOT / 'narvik_original_v3')
    args = parser.parse_args()
    replay(args.rom, args.out, args.sha256)
