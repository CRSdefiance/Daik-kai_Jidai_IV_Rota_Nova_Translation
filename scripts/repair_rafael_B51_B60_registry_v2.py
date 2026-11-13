"""Preserve the rejected uppercase binding; qualify its lowercase entry point before publication."""
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.late_editorial_extensions_v1 import plan_extensions
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B51_B60_release_registry_v2_20261104')
PRIOR=Path('work/analysis/Rafael_B51_B60_release_20261104/registered_preparation.json')
CONFIG=Path('translations/rafael_B51_B60_editorial_release_v2.json')
BOUNDS=Path('translations/ascii_bounds_rafael_B51_B60_release_v2.json')
MODULE=Path('dk4tool/patch/rafael_story_b51_b60_release_v1.py')

if __name__=='__main__':
    assert not ROOT.exists() and not CONFIG.exists() and not BOUNDS.exists()
    prep=load(PRIOR);registry_path=Path('translations/release_stack.json');before=registry_path.read_bytes()
    assert sha(before)==prep['registry_sha256']
    registry=load(registry_path);profile=deepcopy(registry['profiles'][prep['profile']])
    assert profile['late_editorial_extensions'][-1]['module']=='dk4tool.patch.rafael_B51_B60_release_v1'
    original=load(prep['config']);conf=deepcopy(original)
    conf['right_bound_configuration']=str(BOUNDS)
    conf['dependencies'][str(MODULE)]=sha(MODULE.read_bytes())
    conf['dependencies'][str(Path(__file__))]=sha(Path(__file__).read_bytes())
    save(CONFIG,conf)
    ROOT.mkdir();(ROOT/'release_stack_before.json').write_bytes(before)
    old_bounds=load(profile['ascii_glyph_right_bounds']);bounds=deepcopy(old_bounds)
    contract=deepcopy(load(bounds['parent_manifest']))
    contract['new_extension_configs']=[str(CONFIG)]
    contract_path=ROOT/'expected_canonical_manifest_contract.json';save(contract_path,contract)
    bounds['parent_manifest']=str(contract_path)
    bounds['builder_dependencies'][str(MODULE)]=sha(MODULE.read_bytes())
    save(BOUNDS,bounds)
    spec=deepcopy(profile['late_editorial_extensions'][-1])
    spec.update(module='dk4tool.patch.rafael_story_b51_b60_release_v1',module_sha256=sha(MODULE.read_bytes()),
        config=str(CONFIG),config_sha256=sha(CONFIG.read_bytes()))
    image=NdsImage.open(prep['canonical_parent']);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    parent=bytes(image.rom.save());base=bytes(baseline.rom.save())
    planned,proof=plan_extensions(image,baseline,[spec])
    assert sha(bytes(planned.save()))==conf['target_ROM_sha256']
    assert bytes(image.rom.save())==parent and bytes(baseline.rom.save())==base
    profile['late_editorial_extensions'][-1]=spec;profile['ascii_glyph_right_bounds']=str(BOUNDS)
    registry['profiles'][prep['profile']]=profile
    prior=load(ROOT/'release_stack_before.json')
    assert all(registry[k]==v for k,v in prior.items() if k!='profiles')
    assert all(registry['profiles'][k]==v for k,v in prior['profiles'].items() if k!=prep['profile'])
    assert all(profile[k]==v for k,v in prior['profiles'][prep['profile']].items() if k not in ['late_editorial_extensions','ascii_glyph_right_bounds'])
    assert profile['late_editorial_extensions'][:-1]==prior['profiles'][prep['profile']]['late_editorial_extensions'][:-1]
    assert registry_path.read_bytes()==before
    temporary=registry_path.with_name('release_stack.Rafael_B51_B60_v2.pending.json');assert not temporary.exists()
    save(temporary,registry);os.replace(temporary,registry_path)
    updated=deepcopy(prep);updated['config']=str(CONFIG);updated['preserved_stage_configs']['ascii_glyph_right_bounds']=str(BOUNDS)
    updated.update(registry_sha256=sha(registry_path.read_bytes()),uppercase_binding_rejected_before_build=True,
        prior_preparation=str(PRIOR),prior_preparation_sha256=sha(PRIOR.read_bytes()),lowercase_direct_shared_plan=proof,
        prior_reference_ROMs_andall_other_configs_reused_exactly=True)
    save(ROOT/'registered_preparation.json',updated)
    print('Lowercase adapter passes shared atomic extension before publication;only new profile/config binding repaired;all prior stage ROMs reused.',flush=True)
