"""Reject incomplete and expanded actor0 allowlists before any layout output."""
import os
import subprocess
import sys
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_B286_B302_clean_20261110')


def main():
    out = ROOT/'actor0_scope_negatives_v1'
    assert not out.exists()
    out.mkdir()
    source = ROOT/'formatting_v1/formatting_input.json'
    before = digest(source)
    rows = load(source)['records']
    actual = {r['id'] for r in rows if r.get('source_selector') == 0}
    assert actual == {'DK4_MES_B286_R0029', 'DK4_MES_B286_R0042'}
    results = []
    cases = [('missing_real_zero', ['DK4_MES_B286_R0029']),
        ('extra_nonzero', ['DK4_MES_B286_R0029', 'DK4_MES_B286_R0042', 'DK4_MES_B286_R0005'])]
    for name, ids in cases:
        target = out/name
        command = [sys.executable, '-m', 'scripts.plan_scoped_clean_editorial_v4', '--root', str(ROOT),
            '--actor0-source-ids', *ids, '--manuscript', str(source),
            '--preferences', str(ROOT/'formatting_v1/viewed_phrase_preferences_v2.json'), '--out', str(target)]
        run = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', env={**os.environ, 'PYTHONUTF8': '1'})
        log = out/(name+'.txt')
        log.write_text(run.stdout+run.stderr, encoding='utf-8')
        assert run.returncode == 1 and 'AssertionError' in run.stderr and not target.exists()
        assert digest(source) == before
        results.append(dict(case=name, actor0_allowlist=ids, exit_code=run.returncode,
            rejected_before_output=True, manuscript_unchanged=True, log=str(log), log_sha256=digest(log)))
    save(out/'qualification.json', dict(cases=results, exact_two_source0_records_only=True,
        positive_final_plan=str(ROOT/'plan_v5/automatic_plans.json'),
        positive_final_plan_sha256=digest(ROOT/'plan_v5/automatic_plans.json'),
        new_credit=0, evidence={str(p): digest(p) for p in [source, Path('scripts/plan_scoped_clean_editorial_v4.py'), Path(__file__)]}))
    print('PASS two source0 scope negatives rejected before output;exact manuscript preserved.')


if __name__ == '__main__':
    main()
