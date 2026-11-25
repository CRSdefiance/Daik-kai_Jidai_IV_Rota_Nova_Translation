"""Cold-boot the registered parent and staged successor through Lisbon Price Info."""

import argparse
from pathlib import Path
import subprocess
import sys

from scripts import replay_trade_good_descriptions_v1 as historical
from scripts import stage_price_info_wraps_20261115 as stage


base = stage.base
OLD_INPUTS = historical.ROOT / 'inputs.json'
DONOR_PLAN = historical.SOURCE / 'run_plan.json'


def main(case):
    staged = base.load(stage.STORED)
    target, key = (stage.ROM, 'candidate_sha256') if case == 'revised' else (stage.parent.ROM, 'previous_sha256')
    assert base.digest(target) == staged[key]
    folder = stage.ROOT / case
    assert not folder.exists()
    folder.mkdir()
    donor = base.load(DONOR_PLAN)['source_save']
    assert base.digest(donor['source']) == donor['source_sha256']
    inputs = base.load(OLD_INPUTS)
    if case == 'revised':
        # The revised Cheese description closes after one confirmation.
        inputs = [row for row in inputs if row['start'] != 15401]
    plan = folder / 'inputs.json'
    base.save(plan, inputs)
    subprocess.run([sys.executable, '-B', '-m', 'scripts.headless_desmume_v193', '--rom', str(target),
        '--out', str(folder / 'capture'), '--frames', str(historical.FRAMES[-1] + 1),
        '--inputs-json', str(plan), '--press-start', '-1', '--capture-every', '999999',
        '--capture-at', *map(str, historical.FRAMES), '--dump-capture-ram', '--touchscreen',
        '--battery-save', donor['source']], check=True)
    assert base.digest(donor['source']) == donor['source_sha256']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('parent', 'revised'))
    main(parser.parse_args().case)
