"""Summarize isolated tests without losing initial failures or fixture provenance."""

from collections import Counter
import json
from pathlib import Path
import re
import shutil

ROOT = Path('work/patch_interaction_audit_20261027/isolated_tests')


def main():
    for name in ['effective_results.json','summary.json','missing_input_classification.json']:
        before = ROOT/(Path(name).stem+'_pre_fixture_recovery.json')
        if not before.exists():
            shutil.copyfile(ROOT/name,before)
    selected = {}
    for name in ['results.json','setup_retry_results.json','fixture_retry_results.json']:
        for row in json.loads((ROOT/name).read_text()):
            selected[row['file']] = row
    rows = list(selected.values())
    assert len(rows) == 492
    full, partial, errors = Counter(), Counter(), Counter()
    blocked = []
    diagnostics = 0
    for row in rows:
        text = Path(row['log']).read_text(encoding='utf-8',errors='replace')
        diagnostics += 'Windows fatal exception' in text
        lines = [s for s in text.splitlines() if re.search(r'\d+ (passed|failed|skipped|error)',s) and re.search(r' in \d',s)]
        assert lines, row
        counts = Counter({key:int(count) for count,key in re.findall(r'(\d+) (passed|failed|skipped|errors?)',lines[-1])})
        (partial if row['exit_code'] else full).update(counts)
        if row['exit_code']:
            types = Counter(re.findall(r'^E\s+(\w+(?:Error|Exception)):',text,re.M))
            assert set(types) == {'FileNotFoundError'}
            assert sum(types.values()) == counts['failed']+counts['errors']+counts['error']
            errors.update(types)
            blocked.append(dict(file=row['file'],log=row['log'],terminal_exception_types=dict(types)))
    def save(name,value):
        (ROOT/name).write_text(json.dumps(value,indent=2)+'\n')
    save('effective_results.json',rows)
    save('summary.json',dict(file_count=len(rows),passed_files=sum(r['exit_code']==0 for r in rows),
        blocked_missing_input_files=len(blocked),fully_passing_file_outcomes=dict(full),
        partially_blocked_file_outcomes=dict(partial),files_with_native_diagnostics=diagnostics,
        restored_historical_ROM_inputs=40,newly_passing_files_after_fixture_recovery=65))
    save('missing_input_classification.json',dict(terminal_exception_counts=dict(errors),files=blocked))
    print((ROOT/'summary.json').read_text())


if __name__ == '__main__':
    main()
