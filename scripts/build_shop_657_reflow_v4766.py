"""Build through the sole registered cumulative release workflow."""
from pathlib import Path
import subprocess
import sys
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/shop657_build_v4766')
ROM=Path('out/all_routes_combined_v4766_candidate.nds')

if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists() and not ROM.with_suffix('.manifest.json').exists()
    receipt=read('work/analysis/shop657_registration_v4765/registration_receipt.json')
    assert sha(Path('translations/release_stack.json').read_bytes())==receipt['registry_after_sha256']
    assert sha(Path('scripts/build_integrated_release.py').read_bytes())==receipt['builder_after_sha256']
    ROOT.mkdir(parents=True)
    command=[sys.executable,'scripts/build_integrated_release.py','--profile',receipt['profile'],'--out',str(ROM)]
    save(ROOT/'build_plan.json',dict(command=command,registry_sha256=receipt['registry_after_sha256'],builder_sha256=receipt['builder_after_sha256'],all_existing_ROMs_preserved=True))
    log=ROOT/'registered_builder.log'
    with log.open('w',encoding='utf-8') as stream:
        result=subprocess.run(command,stdout=stream,stderr=subprocess.STDOUT,check=False)
    save(ROOT/'terminal.json',dict(terminal=True,returncode=result.returncode,log=str(log),log_sha256=sha(log.read_bytes()),candidate_exists=ROM.exists()))
    print(dict(terminal=True,returncode=result.returncode,candidate_exists=ROM.exists()),flush=True)
    raise SystemExit(result.returncode)
