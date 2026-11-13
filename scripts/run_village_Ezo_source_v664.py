"""Original Japanese Ezo control, with source-equal eight-byte approach helpers."""

import io
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts import native_location_fixture_v519 as location
from scripts.native_village_visits_v664 import SPANS, relocate
from scripts.run_village_visits_v664 import CAP, ROOT
from scripts.verify_village_wrap_v608 import read

CLEAN = 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'


def source_approach(arm, raw, village):
    original = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm == original
    assert sha(Path('work/clean.nds').read_bytes()) == CLEAN
    current = NdsImage.open('out/all_routes_combined_v653_candidate.nds').read_file('/__arm9__.bin')
    assert all(arm[a:b] == current[a:b] for a, b in SPANS)
    # Those unmodified functions read this run's original Japanese live models.
    after, receipt = relocate(current, raw, village)
    receipt.update(actual_emulated_ROM='work/clean.nds', actual_emulated_ROM_sha256=CLEAN,
                   actual_emulated_ARM9_sha256=sha(arm),
                   current_helper_function_spans_exact_original_Japanese=True)
    return after, receipt


def main():
    pre = read(ROOT / 'preflight.json')
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    commands = (ROOT / 'commands_Ezo_chief.jsonl').read_text(encoding='utf-8')
    old, stdin = location.relocate, sys.stdin
    location.relocate, sys.stdin = source_approach, io.StringIO(commands)
    sys.argv = ['headless_desmume_v193.py', '--rom', 'work/clean.nds',
        '--out', str(CAP / 'village_visits_v664_Ezo_Japanese_control'), '--frames', '12201',
        '--inputs-json', str(ROOT / 'inputs_Ezo_chief.json'), '--battery-save', pre['donor'],
        '--pause-at', '5200', '--allow-location-fixtures', '--touchscreen', '--capture-every', '999999',
        '--dump-pause-ram', '--dump-ram', '--dump-native-state']
    try:
        harness.main()
    finally:
        location.relocate, sys.stdin = old, stdin
    print('V664 original Japanese Ezo control terminal.', flush=True)


if __name__ == '__main__':
    main()
