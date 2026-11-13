"""Open the original Lisbon Price Info and replay one- and two-page descriptions."""

from pathlib import Path
import subprocess
import sys
from types import FunctionType, SimpleNamespace

from scripts import replay_item_production_advice_v1 as precedent
from scripts import stage_trade_good_descriptions_v4 as candidate


stage = SimpleNamespace(**candidate.stage_environment())
ROOT = stage.ROOT / 'price_info'
STARTUP = stage.ROOT / 'own_startup'
PRIOR = stage.parent.TEST.parent / 'proof_and_relic_advice_staged_20261111_v2' / 'own_startup'
SOURCE = Path('work/market_goods_info_terminator_release_v1/market_run_v3')
FRAMES = (12600, 13000, 13400, 13800, 14200, 14600, 15000, 15400, 15800,
          16200, 16600, 17000, 17400, 17800, 18200)
INPUTS = (
    (9601, 'DOWN'), (9901, 'DOWN'), (10201, 'A'), (10701, 'A'), (11101, 'RIGHT'),
    (11501, 'A'), (11901, (153, 44)), (12301, 'A'), (12601, 'A'), (13001, 'A'),
    (13401, 'A'), (13801, 'DOWN'), (14201, 'DOWN'), (14601, 'A'), (15001, 'A'),
    (15401, 'A'), (15801, 'UP'), (16201, 'RIGHT'), (16601, 'A'), (17001, 'A'),
    (17401, 'B'), (17801, 'B'),
)


def gameplay():
    assert not ROOT.exists()
    proof = stage.base.load(stage.PROOF)
    assert stage.base.digest(stage.ROM) == proof['research_ROM_sha256']
    donor = stage.base.load(SOURCE / 'run_plan.json')['source_save']
    assert stage.base.digest(donor['source']) == donor['source_sha256']
    inputs = [row for row in stage.base.load(SOURCE / 'unchanged_ordinary_inputs.json') if row['start'] <= 9600]
    inputs.extend(dict(start=frame, duration=8, buttons=[action]) if isinstance(action, str)
                  else dict(start=frame, duration=8, buttons=[], touch=list(action)) for frame, action in INPUTS)
    ROOT.mkdir()
    schedule, capture = ROOT / 'inputs.json', ROOT / 'capture'
    stage.base.save(schedule, inputs)
    subprocess.run([sys.executable, '-B', '-m', 'scripts.headless_desmume_v193', '--rom', str(stage.ROM),
        '--out', str(capture), '--frames', str(FRAMES[-1] + 1), '--inputs-json', str(schedule),
        '--press-start', '-1', '--capture-every', '999999', '--capture-at', *map(str, FRAMES),
        '--dump-capture-ram', '--touchscreen', '--battery-save', donor['source']], check=True)
    report_path = capture / 'capture_report.json'
    report = stage.base.load(report_path)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['ROM_sha256'] == proof['research_ROM_sha256'] and report['frames'] == FRAMES[-1] + 1
    assert report['scripted_input_schedule'] == inputs and stage.base.digest(donor['source']) == donor['source_sha256']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    stage.base.save(ROOT / 'terminal.json', dict(report=str(report_path), report_sha256=stage.base.digest(report_path),
        candidate_sha256=report['ROM_sha256'], unchanged_original_save=True, inputs_sha256=stage.base.digest(schedule)))


def cold_boot():
    env = vars(precedent.startup) | dict(EVIDENCE=stage.PROOF, ROM=stage.ROM, STARTUP=STARTUP, PRIOR=PRIOR)
    FunctionType(precedent.startup.main.__code__, env)()


if __name__ == '__main__':
    assert sys.argv[1:] in (['gameplay'], ['startup'])
    (gameplay if sys.argv[1] == 'gameplay' else cold_boot)()
