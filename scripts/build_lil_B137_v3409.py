"""Run the sole registered integrated builder with a durable terminal receipt."""
import os
import subprocess
import sys
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B137_build_v3409')
ROM=Path('out/all_routes_combined_v3409_candidate.nds')
REG=Path('work/analysis/lil_B137_registration_v3408b/registration_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists() and not ROM.with_suffix('.manifest.json').exists()
    registration=read(REG)
    assert registration['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert registration['builder_sha256']==sha(Path('scripts/build_integrated_release.py').read_bytes())
    ROOT.mkdir(parents=True)
    command=[sys.executable,'scripts/build_integrated_release.py','--profile','all-routes-unified-v3409','--out',str(ROM)]
    log=ROOT/'registered_builder.log'
    save(ROOT/'build_plan.json',dict(command=command,PID=os.getpid(),registration=str(REG),
        registration_sha256=sha(REG.read_bytes()),registry_sha256=registration['release_stack_sha256'],
        builder_sha256=registration['builder_sha256'],producer_sha256=sha(Path(__file__).read_bytes()),
        preserve_every_existing_ROM_translation_and_manifest=True,full_goal_complete=False))
    with log.open('w',encoding='utf-8') as stream:
        result=subprocess.run(command,stdout=stream,stderr=subprocess.STDOUT,check=False)
    save(ROOT/'build_terminal.json',dict(terminal=True,returncode=result.returncode,log=str(log),
        log_sha256=sha(log.read_bytes()),candidate=str(ROM),candidate_exists=ROM.exists(),
        manifest=str(ROM.with_suffix('.manifest.json')),full_goal_complete=False))
    if result.returncode:raise SystemExit(result.returncode)
    manifest=read(ROM.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256']==sha(ROM.read_bytes()) and manifest['profile']=='all-routes-unified-v3409'
    assert len(manifest['batches'])==523 and all(manifest['checks'].values())
    print('RegisteredV3409 cumulative build passes:523manifest batches;candidate andmanifest retained. Release reconstruction/currentstartup pending.',flush=True)
