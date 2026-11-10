"""Preserve v1 research andrepair only registered adapter ownership/transaction metadata."""
import os,re
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

OLD=Path('work/analysis/Help97_Rafael330_release_20261105/registered_preparation.json')
ROOT=Path('work/analysis/Help97_Rafael330_release_v2_20261105')
PROFILE='all-routes-help97-rafael330-v2-20261105'
MODULES=['dk4tool.patch.deck_help31_release_v1','dk4tool.patch.remaining_help67_release_v1','dk4tool.patch.rafael_story_b81_b84_release_v2']
CONFIGS=[Path('translations')/name for name in ['deck30_Coerce33_editorial_release_v2.json',
    'remaining_help67_editorial_release_v2.json','rafael_B81_B84_editorial_release_v2.json']]
BOUNDS=Path('translations/ascii_bounds_Help97_Rafael330_release_v2.json')

if __name__=='__main__':
    assert not ROOT.exists() and not any(p.exists() for p in [*CONFIGS,BOUNDS])
    old=load(OLD);registry_path=Path('translations/release_stack.json');before=registry_path.read_bytes();registry=load(registry_path)
    assert sha(before)==old['registry_sha256']=='7fe38ca768724744e30ede97a9f2618977dd3fb6bd76b9a36c4597a161161b2a'
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114
    oldprofile=registry['profiles'][old['profile']];specs=oldprofile['late_editorial_extensions'][-3:]
    positive=load(OLD.parent/'positive_prepublication_plans.json')
    assert len({s['module'] for s in specs})==2 and any(not re.fullmatch('[a-z][a-z0-9_-]*',s['id']) for s in specs)
    assert all('one_complete_NDS_object_commit_after_all_gates' not in p for p in positive['layers'])
    ROOT.mkdir();(ROOT/'release_stack_before.json').write_bytes(before)
    save(ROOT/'v1_shared_contract_preflight_findings.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),
        frozen_shared_contract='dk4tool/patch/late_editorial_extensions_v1.py',
        findings=['A registered extension identity must be lowercase.','Every extension needs an exclusive module owner.',
            'Each pure planner must explicitly expose its guarded one-object commit contract.'],
        v1_direct_source_inverse_plans_andall11_research_ROMs_remain_valid=True,
        no_v1_shared_qualification_registered_build_playable_candidate_orcredit_claim=True,
        all_prior_modules_configs_profiles_andresearch_preserved=True,new_credit=0))
    for row in [*old['old_stage_states'],*old['ordered_canonical_targets'],*old['stage_targets']]:
        assert sha(Path(row['path']).read_bytes())==row['sha256']
    contract=deepcopy(load(OLD.parent/'expected_canonical_manifest_contract.json'))
    contract['new_extension_configs']=list(map(str,CONFIGS))
    contract_path=ROOT/'expected_canonical_manifest_contract.json';save(contract_path,contract)
    bounds=deepcopy(load(oldprofile['ascii_glyph_right_bounds']));bounds['parent_manifest']=str(contract_path)
    for module in MODULES:
        path=Path(*module.split('.')).with_suffix('.py');bounds['builder_dependencies'][str(path)]=sha(path.read_bytes())
    save(BOUNDS,bounds)
    new_specs=[]
    for i,(config_path,module) in enumerate(zip(CONFIGS,MODULES,strict=True)):
        conf=deepcopy(load(old['configs'][i]));conf['right_bound_configuration']=str(BOUNDS)
        module_path=Path(*module.split('.')).with_suffix('.py')
        for p in [module_path,Path(__file__),ROOT/'v1_shared_contract_preflight_findings.json']:
            conf['dependencies'][str(p)]=sha(p.read_bytes())
        save(config_path,conf)
        new_specs.append(dict(id=['deck30-coerce33-active','remaining-help67','rafael-b81-b84'][i],module=module,
            module_sha256=sha(module_path.read_bytes()),config=str(config_path),config_sha256=sha(config_path.read_bytes()),
            parent_ROM_sha256=conf['parent_ROM_sha256'],target_ROM_sha256=conf['target_ROM_sha256']))
    profile=deepcopy(oldprofile);profile['late_editorial_extensions'][-3:]=new_specs
    profile['ascii_glyph_right_bounds']=str(BOUNDS)
    registry['profiles'][PROFILE]=profile
    assert all(registry[k]==v for k,v in load(ROOT/'release_stack_before.json').items() if k!='profiles')
    assert all(registry['profiles'][k]==v for k,v in load(ROOT/'release_stack_before.json')['profiles'].items())
    staged=registry_path.with_name('release_stack.Help97_Rafael330_v2.pending.json');assert not staged.exists()
    save(staged,registry);assert registry_path.read_bytes()==before;os.replace(staged,registry_path)
    save(ROOT/'registered_preparation.json',{**old,'profile':PROFILE,'configs':list(map(str,CONFIGS)),
        'new_extension_specs':new_specs,'preserved_stage_configs':{**old['preserved_stage_configs'],'ascii_glyph_right_bounds':str(BOUNDS)},
        'registry_sha256':sha(registry_path.read_bytes()),'previous_preparation':str(OLD),'previous_preparation_sha256':sha(OLD.read_bytes()),
        'reused_all11_exact_research_ROMs_no_new_rendering_orROM_serialization':True,
        'shared_contract_adapter_repairs_only_no_text_orruntime_changes':True})
    print('Registered v2 exclusive adapters withguarded transaction contracts;all11 exact research ROMs reused. Shared qualification next.')
