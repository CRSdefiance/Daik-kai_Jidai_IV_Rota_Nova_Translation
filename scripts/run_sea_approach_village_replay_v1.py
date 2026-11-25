"""Cold-boot the exact staged ROM and replay the original village interaction."""

import argparse
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path
import struct
import sys
from types import FunctionType

from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts import native_location_fixture_v519 as location
from scripts import native_village_location_v606 as center
from scripts import run_diplomatic_outcome_startup_v2 as startup
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_sea_approach_village_review_v1 import ARM, BASE, CLEAN
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.run_navigation_prerequisite_startup_v2 import STARTUP as PARENT
from scripts.stage_sea_approach_village_balanced_v2 import PROOF, ROM, ROOT


REFERENCE = Path('E:/Rota Nova translations/Generated/work/emulation_v193/village_visits_v664_00/capture_report.json')
STARTUP = ROOT / 'own_startup'


def relocate(arm, raw, village):
    assert village == 0 and len(raw) == 0x400000
    image, clean = map(NdsImage.open, (ROM, CLEAN))
    source = clean.read_file(ARM)
    assert arm == image.read_file(ARM)
    earlier = load(REFERENCE)['synthetic_location_fixtures']
    old, = earlier
    assert old['village_id'] == village and old['only_eight_ship_coordinate_bytes_owned']
    spans = old['original_reference_code_spans_exact_current']
    assert all(arm[lo:hi] == source[lo:hi] for lo, hi in spans)
    assert image.rom.loadArm9Overlays()[0].data == clean.rom.loadArm9Overlays()[0].data
    worldmap = image.read_file('/data/WORLDMAP.DK4')
    assert worldmap == clean.read_file('/data/WORLDMAP.DK4')
    assert sha256(worldmap).hexdigest() == old['terrain_proof']['WORLDMAP_sha256']
    original = FunctionType(center.relocate.__code__, {**center.relocate.__globals__,
        'ARM_SHA': sha256(arm).hexdigest()})
    _, proof = original(arm, raw, village)
    assert proof['village_point'] == old['village_point']
    safe = old['expected_selector_point_after_original_update']
    assert any(q['map_point'] == safe and q['collision_free'] for q in old['terrain_proof']['queries'])
    offset = proof['active_ship'] - BASE + 16
    target = [n * 128 for n in safe]
    after = raw[:offset] + struct.pack('<2i', *target) + raw[offset + 8:]
    changes = [dict(address=BASE + n, before=raw[n], after=after[n])
               for n in range(offset, offset + 8) if raw[n] != after[n]]
    return after, proof | dict(expected_selector_point_after_original_update=safe,
        after_ship_fixed_point=target, changes=changes, after_RAM_sha256=sha256(after).hexdigest(),
        previous_terrain_proof=str(REFERENCE), previous_terrain_proof_sha256=digest(REFERENCE))


def village_replay():
    assert digest(ROM) == load(PROOF)['research_ROM_sha256']
    prior = load(REFERENCE)
    donor = Path(prior['battery_save_preloaded']['source'])
    assert digest(donor) == prior['battery_save_preloaded']['source_sha256']
    out = ROOT / 'village_resupply'
    out.mkdir()
    inputs = out / 'inputs.json'
    save(inputs, prior['scripted_input_schedule'] + [
        {'start': 7201, 'duration': 8, 'buttons': ['A']},
        {'start': 7601, 'duration': 8, 'buttons': ['A']},
    ])
    commands = [
        {'until': 5400, 'location_town': 0}, {'until': 5800}, {'until': 6200},
        {'until': 6600}, {'until': 7200}, {'until': 7600}, {'until': 8000}, {'stop': True},
    ]
    args = ['--rom', str(ROM), '--out', str(out / 'capture'), '--frames', '8001',
            '--inputs-json', str(inputs), '--battery-save', str(donor), '--touchscreen',
            '--capture-every', '999999', '--pause-at', '5200', '--allow-location-fixtures',
            '--dump-pause-ram', '--dump-ram']
    original, old_input, old_args = location.relocate, sys.stdin, sys.argv
    with StringIO(''.join(json.dumps(row) + '\n' for row in commands)) as stream:
        try:
            location.relocate, sys.stdin, sys.argv = relocate, stream, [sys.argv[0], *args]
            harness.main()
        finally:
            location.relocate, sys.stdin, sys.argv = original, old_input, old_args
    report = out / 'capture/capture_report.json'
    assert load(report)['core_options'] == prior['core_options']
    assert digest(donor) == prior['battery_save_preloaded']['source_sha256']
    save(out / 'terminal.json', dict(report=str(report), report_sha256=digest(report),
        candidate_sha256=digest(ROM), unchanged_donor_sha256=digest(donor),
        prior_capture=str(REFERENCE), prior_capture_sha256=digest(REFERENCE), commands=commands))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=('village', 'startup'))
    if parser.parse_args().phase == 'village':
        village_replay()
    else:
        run = FunctionType(startup.main.__code__, {
            **startup.main.__globals__, 'EVIDENCE': PROOF, 'ROM': ROM,
            'STARTUP': STARTUP, 'PRIOR': PARENT,
        })
        run()


if __name__ == '__main__':
    main()
