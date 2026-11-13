"""Keep native test engines isolated; retain every file's result, including failures."""

import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path('work/patch_interaction_audit_20261027/isolated_tests')


if __name__ == '__main__':
    ROOT.mkdir(exist_ok=True)
    (ROOT / 'tmp').mkdir(exist_ok=True)
    retry = '--retry-setup' in sys.argv
    fixtures = '--retry-fixtures' in sys.argv
    assert not (retry and fixtures)
    files = ([Path(p) for p in json.loads((ROOT/'initial_failure_classes.json').read_text())['own_temporary_parent']]
             if retry else ([Path(r['file']) for r in json.loads((ROOT/'effective_results.json').read_text()) if r['exit_code']]
                            if fixtures else sorted(Path('tests').glob('test_*.py'))))
    results = []
    for index, path in enumerate(files):
        suffix = '_setup_retry' if retry else ('_fixture_retry' if fixtures else '')
        log_path = ROOT / (path.stem + suffix + '.log')
        started = time.monotonic()
        with log_path.open('w', encoding='utf-8') as output:
            try:
                proc = subprocess.run([sys.executable, '-m', 'pytest', str(path), '-q',
                    '--basetemp', str(ROOT / 'tmp' / (path.stem + suffix))], stdout=output, stderr=subprocess.STDOUT,
                    env=dict(os.environ, PYTHONUTF8='1'), timeout=90,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
                code = proc.returncode
            except subprocess.TimeoutExpired:
                code = 'timeout90s'
        result = dict(file=str(path), exit_code=code, seconds=round(time.monotonic()-started, 2), log=str(log_path))
        results.append(result)
        (ROOT / ('setup_retry_results.json' if retry else ('fixture_retry_results.json' if fixtures else 'results.json'))).write_text(json.dumps(results, indent=2)+'\n')
        if code or index % 20 == 0:
            print(index+1, path.name, 'exit', code, flush=True)
    print('Completed',len(results),'test files;',sum(r['exit_code'] == 0 for r in results),'passed files;',sum(r['exit_code'] != 0 for r in results),'need review.', flush=True)
