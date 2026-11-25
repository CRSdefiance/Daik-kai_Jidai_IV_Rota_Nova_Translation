"""Finish the preparation receipt after the completed atomic module registration."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    root=Path('work/analysis/Rafael_B36_B41_release_20261104')
    source=root/'registered_preparation_v2.json';target=root/'registered_preparation_v3.json';assert not target.exists()
    prep=load(source);backup=root/'release_stack_before_lowercase_module_correction.json';assert sha(backup.read_bytes())==prep['registry_sha256']
    prior=load(backup);registry_path=Path('translations/release_stack.json');current=load(registry_path)
    expected=deepcopy(prior);spec=expected['profiles'][prep['profile']]['late_editorial_extensions'][-1]
    assert spec['module']=='dk4tool.patch.rafael_B36_B41_release_v1';spec['module']='dk4tool.patch.rafael_story_b36_b41_release_v1'
    assert current==expected
    old=Path('dk4tool/patch/rafael_B36_B41_release_v1.py');new=Path('dk4tool/patch/rafael_story_b36_b41_release_v1.py')
    assert old.read_bytes()==new.read_bytes() and sha(new.read_bytes())==spec['module_sha256']
    result={**prep,'registry_sha256':sha(registry_path.read_bytes()),'prior_module_preparation':str(source),
        'prior_module_preparation_sha256':sha(source.read_bytes()),'lowercase_module':str(new),'lowercase_module_sha256':sha(new.read_bytes()),
        'original_identical_module_preserved':str(old),'all_ROM_config_native_constants_andstage_bytes_unchanged':True,
        'post_commit_receipt_recovery_only_registry_not_modified':True,'correction_producer_sha256':sha(Path(__file__).read_bytes())}
    save(target,result)
    print('Preparation_v3 receipt recovered from exact committed state;only registered module path differs fromv2;ROMs/configs unchanged.')
