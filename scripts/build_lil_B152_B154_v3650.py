"""Run the sole registered cumulative builder and retain its terminal receipt."""
import os,subprocess,sys
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B152_B154_build_v3650')
ROM=Path('out/all_routes_combined_v3650_candidate.nds')
REG=Path('work/analysis/lil_B152_B154_registration_v3649/registration_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists() and not ROM.with_suffix('.manifest.json').exists();r=read(REG);assert r['registry_after_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and r['builder_after_sha256']==sha(Path('scripts/build_integrated_release.py').read_bytes());ROOT.mkdir(parents=True);command=[sys.executable,'scripts/build_integrated_release.py','--profile','all-routes-unified-v3650','--out',str(ROM)];log=ROOT/'registered_builder.log';save(ROOT/'build_plan.json',dict(command=command,PID=os.getpid(),registration=str(REG),registration_sha256=sha(REG.read_bytes()),registry_sha256=r['registry_after_sha256'],builder_sha256=r['builder_after_sha256'],preserve_every_existing_ROM_translation_and_manifest=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    with log.open('w',encoding='utf-8') as stream:result=subprocess.run(command,stdout=stream,stderr=subprocess.STDOUT,check=False)
    save(ROOT/'build_terminal.json',dict(terminal=True,returncode=result.returncode,log=str(log),log_sha256=sha(log.read_bytes()),candidate=str(ROM),candidate_exists=ROM.exists(),manifest=str(ROM.with_suffix('.manifest.json')),full_goal_complete=False));print(dict(terminal=True,returncode=result.returncode,candidate_exists=ROM.exists()),flush=True);raise SystemExit(result.returncode)
