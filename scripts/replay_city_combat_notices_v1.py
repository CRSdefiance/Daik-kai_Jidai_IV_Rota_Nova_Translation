"""Cold-boot the new notices and order the existing regional fleet to attack."""

from json import dumps
from pathlib import Path
import sys
from types import FunctionType

from scripts import headless_desmume_v193 as harness
from scripts import replay_fleet_reports_v1 as prior
from scripts import run_diplomatic_outcome_startup_v2 as startup
from scripts import stage_city_combat_notices_v2 as stage


base = stage.first.review.prior
STARTUP = stage.ROOT / 'own_startup'
ROOT = stage.ROOT / 'regional_attack_replay'
SOURCE_REPLAY = Path('E:/Rota Nova translations/Generated/work/emulation_v193/regional_missions_v617_actual/capture_report.json')
PAUSE = 7000
ATTACK_MENU = (
    dict(until=7400, buttons=['DOWN'], duration=8),
    dict(until=7800, buttons=['DOWN'], duration=8),
    dict(until=8200, buttons=['DOWN'], duration=8),
    dict(until=8600, buttons=['A'], duration=8),
    dict(until=9000, buttons=['A'], duration=8),
)


def cold_boot():
    env = vars(startup) | dict(EVIDENCE=stage.PROOF, ROM=stage.ROM, STARTUP=STARTUP, PRIOR=prior.STARTUP)
    FunctionType(startup.main.__code__, env)()


def gameplay():
    proof = base.load(stage.PROOF)
    assert base.digest(stage.ROM) == proof['research_ROM_sha256']
    assert base.digest(prior.DONOR) == prior.DONOR_SHA
    old = base.load(SOURCE_REPLAY)
    assert old['frames'] == 42600 and old['cold_boot'] and not old['savestate_loaded'] and not old['callback_errors']
    assert old['battery_save_preloaded']['source_sha256'] == prior.DONOR_SHA
    schedule = [row for row in old['scripted_input_schedule'] if row['start'] < PAUSE]
    assert schedule[-1] == dict(start=6601, duration=8, buttons=['A'])
    ROOT.mkdir()
    commands, inputs = ROOT / 'commands.jsonl', ROOT / 'original_input_prefix.json'
    commands.write_text(''.join(dumps(row) + '\n' for row in ATTACK_MENU), encoding='utf-8')
    base.save(inputs, schedule)
    args = ['--rom', str(stage.ROM), '--out', str(ROOT / 'capture'), '--frames', '46000',
        '--inputs-json', str(inputs), '--battery-save', str(prior.DONOR), '--touchscreen',
        '--capture-every', '999999', '--pause-at', str(PAUSE), '--dump-pause-ram', '--dump-ram']
    previous = sys.stdin, sys.argv
    stream = prior.prior.prior.GrowingCommands(commands)
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
    assert base.digest(prior.DONOR) == prior.DONOR_SHA
    base.save(ROOT / 'terminal.json', dict(candidate_sha256=report['ROM_sha256'],
        report=str(report_path), report_sha256=base.digest(report_path), commands=str(commands),
        commands_sha256=base.digest(commands), unchanged_original_save=True))


if __name__ == '__main__':
    assert sys.argv[1:] in (['startup'], ['gameplay'])
    (cold_boot if sys.argv[1] == 'startup' else gameplay)()
