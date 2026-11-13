"""Replay real Golden Route views with explicit isolated display/cost fixtures."""

import argparse
import builtins
import json
import sys
from pathlib import Path

from dk4tool.patch.golden_route_plaques import FILES
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/golden_route_plaques_v613')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
SOURCE = ROOT / 'original_art_CONTROL_ONLY.nds'
DONOR = Path('work/analysis/weapon_voyage_v476/syracuse_test_copy.dsv')


def prepare_source():
    parent = NdsImage.open('out/all_routes_combined_v612_candidate.nds')
    before = {p: data for _, p, data in parent.iter_files()} | dict(parent.iter_components())
    clean = NdsImage.open('work/clean.nds')
    for path in FILES:
        parent.replace_file(path, clean.read_file(path))
    parent.save(SOURCE)
    saved = NdsImage.open(SOURCE)
    after = {p: data for _, p, data in saved.iter_files()} | dict(saved.iter_components())
    assert before.keys() == after.keys()
    assert {p for p in before if before[p] != after[p]} == set(FILES)
    proof = {'research_original_art_control_only': True, 'ROM': str(SOURCE), 'ROM_sha256': sha(SOURCE.read_bytes()),
             'parent': 'out/all_routes_combined_v612_candidate.nds',
             'parent_sha256': sha(Path('out/all_routes_combined_v612_candidate.nds').read_bytes()),
             'only_three_original_Japanese_atlases_changed': list(FILES),
             'all_code_dialogue_input_and_other_art_exact_V612': True, 'playable_release_or_handoff': False}
    save(ROOT / 'source_art_control.json', proof)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('variant', choices=('current', 'original'))
    parser.add_argument('context', choices=('records', 'sale', 'market'))
    args = parser.parse_args()
    if args.variant == 'original' and not SOURCE.exists():
        prepare_source()
    rom = Path('out/all_routes_combined_v613_candidate.nds') if args.variant == 'current' else SOURCE
    if args.variant == 'original':
        assert sha(rom.read_bytes()) == read(ROOT / 'source_art_control.json')['ROM_sha256']
    if args.context == 'market':
        assert args.variant == 'current'
        baseline = read(CAP / 'save_load_plaques_v612_market/capture_report.json')
        pause = None
    else:
        baseline = read(CAP / ('golden_route_plaques_v613_control' if args.context == 'records'
                               else 'golden_route_plaques_v613_sale_control') / 'capture_report.json')
        pause = 4600 if args.context == 'records' else 22000
    plan = ROOT / ('complete_' + args.context + '_inputs.json')
    save(plan, baseline['scripted_input_schedule'])
    frames = sorted({r['frame'] for r in baseline['frames_captured']})
    output = CAP / ('golden_route_plaques_v613_' + args.context + '_' + args.variant)
    argv = ['headless_desmume_v193.py', '--rom', str(rom), '--out', str(output),
            '--frames', str(baseline['frames']), '--inputs-json', str(plan), '--touchscreen',
            '--capture-every', '999999', '--capture-at', *map(str, frames)]
    if args.context == 'records':
        argv += ['--battery-save', str(DONOR)]
    commands = []
    if pause is not None:
        argv += ['--pause-at', str(pause), '--dump-pause-ram', '--dump-capture-ram', '--allow-golden-route-fixtures']
        fixture = {'golden_route_records': read(ROOT / 'fixture_rows.json')} if args.context == 'records' else {'golden_route_purchase_cost': 1}
        commands = [json.dumps({**fixture, 'until': baseline['frames']}), '{"stop":true}']
    original_input, original_argv = builtins.input, sys.argv
    iterator = iter(commands)
    builtins.input = lambda *a: next(iterator)
    sys.argv = argv
    try:
        harness.main()
    finally:
        builtins.input, sys.argv = original_input, original_argv


if __name__ == '__main__':
    main()
