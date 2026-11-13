"""Cold-boot the seven changed village contexts; reuse original input algorithms."""

import argparse
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.village_port_consistency import transform
from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts import native_location_fixture_v519 as location
from scripts.native_village_visits_v664 import relocate as historical_relocate
from scripts.run_village_development_v665 import PREVIOUS, Controller
from scripts.run_village_return_v665 import ReturnController
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/village_consistency_v666')
ROM = Path('out/all_routes_combined_v666_candidate.nds')
INDICES = (4, 6, 12, 16, 21, 22, 23)


def relocate(arm, raw, village):
    original = NdsImage.open('out/all_routes_combined_v653_candidate.nds').read_file('/__arm9__.bin')
    target, _ = transform(original)
    assert target == arm and len(raw) == 0x400000 and type(village) is int and 0 <= village < 24
    after, receipt = historical_relocate(original, raw, village)
    assert len(after) == len(raw) and sum(a != b for a, b in zip(raw, after, strict=True)) <= 8
    receipt.update(actual_candidate_ARM9_sha256=sha(arm), fixture_current_guard='V666-exact-transform-of-V653',
        reference_V653_ARM9_sha256=sha(original),
        original_coordinate_and_terrain_code_unchanged_by_seven_data_repairs=True)
    return after, receipt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('village', type=int, choices=INDICES)
    args = parser.parse_args()
    proof = read(ROOT / 'static_release_proof.json')
    assert sha(ROM.read_bytes()) == proof['candidate_sha256']
    donor = read('work/analysis/village_development_v665/preflight.json')
    assert sha(Path(donor['donor']).read_bytes()) == donor['donor_sha256']
    answer = next(r['english'] for r in read('translations/village_promised_words_manuscript_v1.json')['records']
                  if r['kind'] == 'ANSWER' and r['index'] == args.village)
    folder = CAP / f'village_consistency_v666_{args.village:02d}'
    assert not folder.exists(), 'Retain all prior attempts; never overwrite a run'
    folder.mkdir()
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    cls = ReturnController if args.village in (22, 23) else Controller
    controller = cls(args.village, folder, arm, answer)
    save(folder / 'run_contract.json', {'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'],
        'runner': str(Path(__file__)), 'runner_sha256': sha(Path(__file__).read_bytes()),
        'reused_controller_source': 'scripts/run_village_development_v665.py',
        'reused_controller_sha256': sha(Path('scripts/run_village_development_v665.py').read_bytes()),
        'isolated_saved_setup_cold_boot_no_savestate': True,
        'coordinate_only_approach_no_development_story_or_password_flags': True})
    old, stdin = location.relocate, sys.stdin
    location.relocate, sys.stdin = relocate, controller
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(folder),
        '--frames', '30000', '--inputs-json', str(PREVIOUS / f'inputs_chief_{args.village:02d}.json'),
        '--battery-save', donor['donor'], '--pause-at', '5200', '--allow-location-fixtures',
        '--touchscreen', '--capture-every', '999999', '--dump-pause-ram', '--dump-ram', '--dump-native-state']
    try:
        harness.main()
    finally:
        location.relocate, sys.stdin = old, stdin
    if controller.error:
        raise RuntimeError('Retained controller failure: ' + controller.error)
    print(f'V666 village {args.village}: terminal at {controller.frame}.', flush=True)


if __name__ == '__main__':
    main()
