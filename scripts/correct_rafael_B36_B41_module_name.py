"""Supply the byte-identical adapter under the framework's required lowercase module name."""
import os,re
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_B36_B41_release_20261104')
if __name__=='__main__':
    prep_path=ROOT/'registered_preparation_v2.json';target=ROOT/'registered_preparation_v3.json';assert not target.exists()
    prep=load(prep_path);path=Path('translations/release_stack.json');before=path.read_bytes();assert sha(before)==prep['registry_sha256']
    prior=load(path);registry=deepcopy(prior);profile=registry['profiles'][prep['profile']];spec=profile['late_editorial_extensions'][-1]
    assert spec['id']=='rafael-b36-b41' and spec['module']=='dk4tool.patch.rafael_B36_B41_release_v1'
    old=Path('dk4tool/patch/rafael_B36_B41_release_v1.py');new=Path('dk4tool/patch/rafael_story_b36_b41_release_v1.py');assert not new.exists()
    raw=old.read_bytes();assert sha(raw)==spec['module_sha256'];new.write_bytes(raw);assert new.read_bytes()==raw
    spec['module']='dk4tool.patch.rafael_story_b36_b41_release_v1'
    assert re.fullmatch(r'[a-z][a-z0-9_-]*',spec['id']) and re.fullmatch(r'dk4tool\.patch\.[a-z][a-z0-9_]*',spec['module'])
    assert len({r['id'] for r in profile['late_editorial_extensions']})==len({r['module'] for r in profile['late_editorial_extensions']})==len(profile['late_editorial_extensions'])
    restored=deepcopy(registry);restored['profiles'][prep['profile']]['late_editorial_extensions'][-1]['module']='dk4tool.patch.rafael_B36_B41_release_v1';assert restored==prior
    (ROOT/'release_stack_before_lowercase_module_correction.json').write_bytes(before)
    temporary=path.with_name('release_stack.pending_Rafael_B36_B41_lowercase_module.json');assert not temporary.exists();save(temporary,registry)
    assert path.read_bytes()==before;os.replace(temporary,path)
    save(target,dict(**{k:v for k,v in prep.items() if k!='registry_sha256'},registry_sha256=sha(path.read_bytes()),
        prior_module_preparation=str(prep_path),prior_module_preparation_sha256=sha(prep_path.read_bytes()),
        lowercase_module=str(new),lowercase_module_sha256=sha(raw),original_identical_module_preserved=str(old),
        all_ROM_config_native_constants_andstage_bytes_unchanged=True,correction_producer_sha256=sha(Path(__file__).read_bytes())))
    print('Registered byte-identical lowercase adapter;both framework identifier grammars anduniqueness pass;use preparation_v3.')
