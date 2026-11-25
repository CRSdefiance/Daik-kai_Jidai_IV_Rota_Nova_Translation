"""Correct the unbuilt extension's case to the registry's enforced lowercase grammar."""
import os
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_B36_B41_release_20261104')
if __name__=='__main__':
    prior_path=ROOT/'registered_preparation.json';target=ROOT/'registered_preparation_v2.json';assert not target.exists()
    prep=load(prior_path);path=Path('translations/release_stack.json');before=path.read_bytes();assert sha(before)==prep['registry_sha256']
    prior=load(path);registry=deepcopy(prior);profile=registry['profiles'][prep['profile']]
    spec=profile['late_editorial_extensions'][-1];assert spec['id']=='rafael-B36-B41';spec['id']='rafael-b36-b41'
    restored=deepcopy(registry);restored['profiles'][prep['profile']]['late_editorial_extensions'][-1]['id']='rafael-B36-B41'
    assert restored==prior
    backup=ROOT/'release_stack_before_lowercase_ID_correction.json';backup.write_bytes(before)
    temporary=path.with_name('release_stack.pending_Rafael_B36_B41_lowercase_ID.json');assert not temporary.exists()
    save(temporary,registry);assert path.read_bytes()==before;os.replace(temporary,path)
    save(target,dict(**{k:v for k,v in prep.items() if k!='registry_sha256'},registry_sha256=sha(path.read_bytes()),
        prior_preparation=str(prior_path),prior_preparation_sha256=sha(prior_path.read_bytes()),
        unbuilt_extension_ID_case_corrected_without_ROM_orconfig_orstage_changes=True,
        failed_initial_shared_framework_qualification_preserved='work/analysis/Rafael_B36_B41_release_qualification_20261104',
        correction_producer_sha256=sha(Path(__file__).read_bytes())))
    print('Corrected only unbuilt extension ID to rafael-b36-b41;all ROM/config/stage bytes unchanged;use preparation_v2.')
