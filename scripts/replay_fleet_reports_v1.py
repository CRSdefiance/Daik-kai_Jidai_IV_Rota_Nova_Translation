"""Cold-boot the staged ROM with the verified existing regional fleet save."""

from pathlib import Path
import sys
from types import FunctionType

from scripts import headless_desmume_v193 as harness
from scripts import replay_crew_item_actions_v1 as prior
from scripts import stage_fleet_reports_v2 as stage


base = stage.first.review.prior
STARTUP = stage.ROOT / 'own_startup'
ROOT = stage.ROOT / 'regional_fleet_replay'
DONOR = Path('work/analysis/regional_fleet_v615/formed_Manuel_regional_copy.dsv')
DONOR_SHA = '2bec91a13ba69361c5c79ff52dcc3c8a3d5cf2ccbe2fc4b614bac8d12ab4cee1'
OLD_INPUTS = Path('work/analysis/regional_missions_v617/complete_V616_control_inputs.json')
PAUSE = 3400


def cold_boot():
    boot = prior.prior.precedent.startup
    env = vars(boot) | dict(EVIDENCE=stage.PROOF, ROM=stage.ROM, STARTUP=STARTUP, PRIOR=prior.STARTUP)
    FunctionType(boot.main.__code__, env)()


def gameplay():
    proof = base.load(stage.PROOF)
    assert base.digest(stage.ROM) == proof['research_ROM_sha256']
    assert base.digest(DONOR) == DONOR_SHA
    schedule = [row for row in base.load(OLD_INPUTS) if row['start'] < PAUSE]
    assert [row['buttons'] for row in schedule] == [['START'], ['A'], ['A'], ['A']]
    ROOT.mkdir()
    commands, inputs = ROOT / 'commands.jsonl', ROOT / 'original_input_prefix.json'
    commands.touch(exist_ok=False)
    base.save(inputs, schedule)
    args = ['--rom', str(stage.ROM), '--out', str(ROOT / 'capture'), '--frames', '33000',
        '--inputs-json', str(inputs), '--battery-save', str(DONOR), '--touchscreen', '--capture-every', '999999',
        '--pause-at', str(PAUSE), '--dump-pause-ram', '--dump-ram']
    previous = sys.stdin, sys.argv
    stream = prior.prior.GrowingCommands(commands)
    try:
        sys.stdin, sys.argv = stream, [str(Path(harness.__file__)), *args]
        harness.main()
    finally:
        sys.stdin, sys.argv = previous
        stream.close()
    report_path = ROOT / 'capture/capture_report.json'
    report = base.load(report_path)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['ROM_sha256'] == proof['research_ROM_sha256']
    assert base.digest(DONOR) == DONOR_SHA
    base.save(ROOT / 'terminal.json', dict(candidate_sha256=report['ROM_sha256'],
        report=str(report_path), report_sha256=base.digest(report_path), commands=str(commands),
        commands_sha256=base.digest(commands), unchanged_original_save=True))


if __name__ == '__main__':
    assert sys.argv[1:] in (['startup'], ['gameplay'])
    (cold_boot if sys.argv[1] == 'startup' else gameplay)()
