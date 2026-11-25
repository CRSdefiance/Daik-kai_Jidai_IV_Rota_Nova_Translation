"""Run the repaired historical regressions with isolated test-engine processes."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path('work/blocked_test_resolution_20261027')


def main(mode):
    rows = json.loads(Path('work/patch_interaction_audit_20261027/isolated_tests/missing_input_classification.json').read_text())['files']
    files = [Path(r['file']) for r in rows]
    if mode=='components':
        files = [p for p in files if p.name not in ('test_hodram_route_completion.py','test_raphael_route_completion.py')]
    elif mode=='routes':
        files = [p for p in files if p.name in ('test_hodram_route_completion.py','test_raphael_route_completion.py')]
    if mode in ('components','all'):
        files += [Path('tests')/name for name in ('test_historical_fixture_support.py','test_integrated_release.py','test_combined_percentage_safety.py')]
    destination = ROOT/mode
    destination.mkdir(exist_ok=False)
    (destination/'tmp').mkdir()
    results = []
    for path in files:
        log = destination/(path.stem+'.log')
        started = time.monotonic()
        with log.open('w',encoding='utf-8') as output:
            process = subprocess.run([sys.executable,'-m','pytest',str(path),'-q',
                '--basetemp',str(destination/'tmp'/path.stem)],stdout=output,stderr=subprocess.STDOUT,
                env=dict(os.environ,PYTHONUTF8='1'),timeout=180,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        results.append(dict(file=str(path),exit_code=process.returncode,
            seconds=round(time.monotonic()-started,2),log=str(log)))
        (destination/'results.json').write_text(json.dumps(results,indent=2)+'\n')
        print(path.name,process.returncode,flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--mode',choices=['components','routes','all'],required=True)
    main(parser.parse_args().mode)
