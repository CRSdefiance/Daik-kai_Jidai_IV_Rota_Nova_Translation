"""Current combined-ROM integration check of five category-maximum hints.

Only the helper's process-local exact-ARM allowlist is extended, after original
transfer/getter/history code identity checks. Shared harness/helper/core files
are unchanged. The helper applies bounded inventory data; UI controls equip it.
"""

import io
import json
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts import native_inventory_fixture_v481 as inventory
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/long_hints_v730')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/long_hints_v730')
ROM = Path('out/all_routes_combined_v712_candidate.nds')
OLD = Path('E:/Rota Nova translations/Generated/work/emulation_v193/equipment_long_names_v536')
ITEMS = [40, 71, 92, 98, 126]
FRAMES = [3000, 6200, 7000, 12000, 14800, 15000, 15200, 15400, 15600]
CURRENT_ARM = 'af4ce98637f6febb4e3e0dab7ce63f5984050deb267713b1c741f5005eb98e41'


def support():
    current = NdsImage.open(ROM).read_file('/__arm9__.bin')
    prior = NdsImage.open('out/all_routes_combined_v534_candidate.nds').read_file('/__arm9__.bin')
    ranges = [(0x49D00, 0x4B000), (0xCB190, 0xCB1C0), (0xCDA80, 0xCDB40)]
    assert sha(current) == CURRENT_ARM and sha(prior) in inventory.SUPPORTED_ARM_SHA
    assert all(current[lo:hi] == prior[lo:hi] for lo, hi in ranges)
    if CURRENT_ARM not in inventory.SUPPORTED_ARM_SHA:
        inventory.SUPPORTED_ARM_SHA += (CURRENT_ARM,)
    return {'current_ARM9_sha256': sha(current), 'prior_V534_ARM9_sha256': sha(prior),
        'source_exact_transfer_getter_history_ranges': [list(r) for r in ranges],
        'process_local_allowlist_extension_only': True,
        'shared_helper_source_sha256': sha(Path('scripts/native_inventory_fixture_v481.py').read_bytes())}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'preflight.json').exists() and not (CAP / 'capture_report.json').exists()
    original = read('work/analysis/equipment_long_names_v536/save_copy_manifest.json')
    donor = Path(original['original'])
    assert sha(donor.read_bytes()) == original['original_sha256']
    test_copy = ROOT / 'maria_current_long_hints_TEST_ONLY.dsv'
    copy(donor, test_copy)
    old_report = read(OLD / 'capture_report.json')
    assert old_report['ROM_sha256'] == 'cac800924a1dfb3e2bc6352ef3f47f8f82986229377de20bc5e194046b5a6f45'
    save(ROOT / 'inputs.json', old_report['scripted_input_schedule'])
    compatibility = support()
    release = {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'),
        ROM.with_suffix('.xdelta'), Path('translations/release_stack.json'),
        Path('out/raphael_natural_v2_accepted_base.nds'))}
    assert release[str(ROM)] == '6534e5619673ea6bdffa3a2342622b99ef393bef52ef58cac131ee94ae0f4030'
    commands = [{'until': 15600, 'inventory_items': ITEMS}, {'stop': True}]
    save(ROOT / 'interactive_commands.json', commands)
    pre = {'candidate': str(ROM), 'candidate_sha256': release[str(ROM)],
        'release_hashes': release, 'compatibility': compatibility,
        'original_donor': str(donor), 'original_donor_sha256': sha(donor.read_bytes()),
        'test_copy': str(test_copy), 'test_copy_sha256': sha(test_copy.read_bytes()),
        'old_report': str(OLD / 'capture_report.json'),
        'old_report_sha256': sha((OLD / 'capture_report.json').read_bytes()),
        'inputs': str(ROOT / 'inputs.json'), 'inputs_sha256': sha((ROOT / 'inputs.json').read_bytes()),
        'runner_sha256': sha(Path(__file__).read_bytes()),
        'shared_harness_sha256': sha(Path('scripts/headless_desmume_v193.py').read_bytes()),
        'core_sha256': sha(harness.CORE.read_bytes()), 'capture_frames': FRAMES,
        'synthetic_inventory_not_normal_acquisition': True, 'full_goal_complete': False}
    save(ROOT / 'preflight.json', pre)
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(CAP),
        '--frames', '15600', '--inputs-json', str(ROOT / 'inputs.json'),
        '--battery-save', str(test_copy), '--touchscreen', '--pause-at', '3000',
        '--allow-inventory-fixtures', '--dump-pause-ram', '--dump-capture-ram',
        '--capture-every', '999999', '--capture-at', *map(str, FRAMES), '--dump-ram']
    previous_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(''.join(json.dumps(c) + '\n' for c in commands))
        harness.main()
    finally:
        sys.stdin = previous_stdin
    for key in ('original_donor', 'test_copy'):
        assert sha(Path(pre[key]).read_bytes()) == pre[key + '_sha256']
    for path, digest in release.items():
        assert sha(Path(path).read_bytes()) == digest
    print('V730 terminal current long-hint integration capture; original saves and release files unchanged.', flush=True)


if __name__ == '__main__':
    main()
