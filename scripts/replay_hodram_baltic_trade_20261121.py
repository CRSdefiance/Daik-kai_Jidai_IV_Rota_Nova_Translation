"""Replay the ordinary Hamburg docking and verify the cumulative ROM inputs."""

from argparse import ArgumentParser
from types import FunctionType, SimpleNamespace
import sys

from scripts import replay_hodram_alexandria_tutorial_20261121 as precedent
from scripts import stage_hodram_baltic_trade_20261121 as stage


base, native = stage.base, stage.native
ROOT = stage.ROOT / 'voyage'
REPORT = ROOT / 'capture/capture_report.json'
BASELINE = stage.preview.dialogue.FOLDER / 'capture/capture_report.json'
PLAN = stage.preview.dialogue.FOLDER / 'verification_trade.json'
STARTUP_CAPTURE = stage.ROOT / 'startup/capture/capture_report.json'
STARTUP_PLAN = stage.ROOT / 'startup/identical_inputs.json'


def voyage():
    release, stored, before, plan, observed = map(base.load, (
        stage.parent.RELEASE, stage.PROOF, BASELINE, PLAN, stage.preview.dialogue.REVIEW))
    assert release['candidate_sha256'] == before['ROM_sha256'] == stored['predecessor_sha256']
    assert observed['evidence'][str(BASELINE)] == base.digest(BASELINE)
    assert observed['evidence'][str(PLAN)] == base.digest(PLAN)
    assert base.digest(stage.ROM) == stored['candidate_sha256']
    assert before['cold_boot'] and not before['savestate_loaded'] and not before['callback_errors']
    assert not any(v for key, v in before.items() if key.startswith('synthetic_'))
    donor = before['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    inputs = [row for row in before['scripted_input_schedule'] if row['start'] <= plan['port_return']]
    frames = [3760, 19965, 24965, plan['dock_prompt'], *plan['panels'], plan['port_return']]
    assert frames == sorted(set(frames)) and len(plan['panels']) == 9
    ROOT.mkdir()
    schedule = ROOT / 'inputs.json'
    base.save(schedule, inputs)
    base.save(ROOT / 'replay_scope.json', dict(candidate_sha256=stored['candidate_sha256'],
        original_report_sha256=base.digest(BASELINE), original_plan_sha256=base.digest(PLAN),
        donor_sha256=donor['source_sha256'], schedule_sha256=base.digest(schedule),
        exact_ordinary_prefix_through_port_return=True, frames=frames))
    harness = precedent.template.template.games.harness
    sys.argv = [harness.__file__, '--rom', str(stage.ROM), '--out', str(REPORT.parent),
                '--frames', str(plan['port_return']), '--inputs-json', str(schedule), '--battery-save', donor['source'],
                '--press-start', '-1', '--touchscreen', '--dump-ram', '--capture-every', '999999',
                '--capture-at', *map(str, frames)]
    harness.main()
    assert base.digest(donor['source']) == donor['source_sha256']


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('voyage', 'startup', 'patch'))
    case = parser.parse_args().case
    if case == 'voyage':
        voyage()
        return
    common = precedent.template.template
    action = common.common.startup if case == 'startup' else common.common.reconstruct
    runtime = SimpleNamespace(active=stage.parent, PROOF=stage.PROOF, ROOT=stage.ROOT,
                              ROM=stage.ROM, native=native, play=common.games)
    FunctionType(action.__code__, action.__globals__ |
                 {'stage': runtime, 'STARTUP_CAPTURE': STARTUP_CAPTURE, 'PLAN': STARTUP_PLAN})()


if __name__ == '__main__':
    main()
