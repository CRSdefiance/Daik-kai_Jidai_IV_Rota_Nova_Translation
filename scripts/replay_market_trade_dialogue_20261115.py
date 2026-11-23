"""Replay ordinary contract refusal and investment navigation with a copied save."""

from argparse import ArgumentParser
from pathlib import Path
from subprocess import run
import sys
from types import FunctionType

from scripts import replay_kurushima_encounter_20261115 as startup_workflow
from scripts import stage_market_trade_dialogue_20261115 as stage


CAPTURES = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
DONOR_SHA = 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
FRAMES = (3200, 4000, 4400, 4600, 4800, 5000, 5200, 5400, 5600)


def schedule(mode):
    history = CAPTURES / f'market_contract_v758_{mode}_758' / 'capture_report.json'
    report = stage.base.load(history)
    donor = report['battery_save_preloaded']
    assert donor['source_sha256'] == stage.base.digest(donor['source']) == DONOR_SHA
    assert report['cold_boot'] and not report['savestate_loaded']
    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
    return report['scripted_input_schedule'], donor['source'], history


def replay(case):
    mode, side = case.split('_')
    staged = stage.base.load(stage.STORED)
    rom, key = (stage.parent.ROM, 'previous_sha256') if side == 'before' else (stage.ROM, 'candidate_sha256')
    assert stage.base.digest(rom) == staged[key]
    events, donor, history = schedule(mode)
    folder = stage.ROOT / case
    folder.mkdir()
    plan = folder / 'inputs.json'
    stage.base.save(plan, events)
    stage.base.save(folder / 'inputs_provenance.json', dict(historical_report=str(history),
        historical_report_sha256=stage.base.digest(history), donor=donor, donor_sha256=DONOR_SHA))
    run([sys.executable, '-B', '-m', 'scripts.headless_desmume_v193', '--rom', str(rom),
        '--out', str(folder / 'capture'), '--frames', '5601', '--inputs-json', str(plan), '--press-start', '-1',
        '--capture-every', '999999', '--capture-at', *map(str, FRAMES), '--touchscreen',
        '--battery-save', donor], check=True)
    assert stage.base.digest(donor) == DONOR_SHA


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('palace_before', 'palace_after', 'investment_before', 'investment_after', 'startup'))
    mode = parser.parse_args().mode
    if mode == 'startup':
        FunctionType(startup_workflow.startup.__code__, vars(startup_workflow) | {'stage': stage})()
    else:
        replay(mode)
