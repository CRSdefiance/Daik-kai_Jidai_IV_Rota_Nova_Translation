"""Try only still-buildable historical profiles with exact original ancestry."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/patch_interaction_audit_20261027')


def main():
    rows = json.loads((ROOT/'remaining_historical_profile_checks.json').read_text())
    folder = ROOT/'historical_registered_reconstruction'
    folder.mkdir(exist_ok=False)
    results = []
    registry = Path('translations/release_stack.json').read_bytes()
    for row in rows:
        if row['status'] != 'registered_profile' or not row['exact_historical_batch_list']:
            continue
        target = Path(row['ROM'])
        assert not target.exists()
        original_manifest = next(p for p in [target.with_suffix('.manifest.json'),
            target.with_name(target.stem.replace('_candidate','')+'_manifest.json')] if p.exists())
        expected = json.loads(original_manifest.read_text(encoding='utf-8'))['candidate_sha256']
        research = folder/target.name
        log = folder/(target.stem+'.log')
        with log.open('w',encoding='utf-8') as output:
            result = subprocess.run([sys.executable,'-m','scripts.build_integrated_release',
                '--profile',row['profile'],'--out',str(research)],stdout=output,stderr=subprocess.STDOUT,
                env=dict(os.environ,PYTHONUTF8='1'),timeout=240)
        proof = dict(ROM=str(target),profile=row['profile'],log=str(log),exit_code=result.returncode,
            original_manifest=str(original_manifest),expected_sha256=expected,restored=False)
        if result.returncode == 0:
            proof['actual_sha256'] = sha(research.read_bytes())
            if proof['actual_sha256'] == expected:
                assert not target.exists() and target.resolve().parent == Path('out').resolve()
                shutil.copyfile(research,target)
                assert sha(target.read_bytes()) == expected
                proof['restored'] = True
        results.append(proof)
        (ROOT/'historical_registered_reconstruction_results.json').write_text(json.dumps(results,indent=2)+'\n')
        assert Path('translations/release_stack.json').read_bytes() == registry
        print(target,'restored',proof['restored'],'exit',result.returncode,flush=True)


if __name__ == '__main__':
    main()
