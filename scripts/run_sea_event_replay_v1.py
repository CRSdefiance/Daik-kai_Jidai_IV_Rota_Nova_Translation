"""Replay two ordinary voyages with the staged sea-event text and isolated saves."""

import argparse
from pathlib import Path
import sys

from scripts import headless_desmume_v193 as harness
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.stage_sea_event_review_v1 import EVIDENCE, ROM, ROOT


REPLAYS = {
    'bubbles': ('sea_foam_family_v514_final_actual', 9476,
                (3200, 6000, 8327, 8476, 8676, 8876, 9076, 9276, 9476)),
    'scurvy': ('alignment_sort_v378', 9600, (3200, 7200, 8400, 9000, 9200, 9600)),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay', required=True, choices=tuple(REPLAYS))
    args = parser.parse_args()
    name, frames, samples = REPLAYS[args.replay]
    old_path = Path('work/emulation_v193') / name / 'capture_report.json'
    old = load(old_path)
    assert old['cold_boot'] and not old['savestate_loaded'] and not old['callback_errors']
    donor = Path(old['battery_save_preloaded']['source'])
    donor_sha = old['battery_save_preloaded']['source_sha256']
    assert digest(donor) == donor_sha
    release = load(EVIDENCE)
    assert digest(ROM) == release['research_ROM_sha256']
    target = ROOT / ('ordinary_' + args.replay)
    target.mkdir()
    inputs = target / 'inputs.json'
    schedule = [command for command in old['scripted_input_schedule'] if command['start'] <= frames]
    save(inputs, schedule)
    command = ['--rom', str(ROM), '--out', str(target / 'capture'), '--frames', str(frames),
               '--inputs-json', str(inputs), '--battery-save', str(donor), '--touchscreen',
               '--capture-every', '999999', '--capture-at', *map(str, samples), '--dump-capture-ram', '--dump-ram']
    previous = sys.argv
    try:
        sys.argv = [sys.argv[0], *command]
        harness.main()
    finally:
        sys.argv = previous
    report_path = target / 'capture/capture_report.json'
    report = load(report_path)
    assert report['scripted_input_schedule'] == schedule and report['core_options'] == old['core_options']
    assert digest(donor) == donor_sha
    save(target / 'terminal.json', dict(candidate_sha256=digest(ROM), report=str(report_path),
        report_sha256=digest(report_path), inputs=str(inputs), inputs_sha256=digest(inputs),
        historic_report=str(old_path), historic_report_sha256=digest(old_path), donor_unchanged=True,
        no_gameplay_state_or_savestate_injection=True))


if __name__ == '__main__':
    main()
