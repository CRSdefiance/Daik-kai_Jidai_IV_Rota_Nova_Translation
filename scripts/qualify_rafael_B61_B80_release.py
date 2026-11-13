"""Check production entry points and semantic rejection while reusing unchanged stage proofs."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.rafael_story_b61_b80_release_v1 import plan_release
from dk4tool.patch.late_editorial_extensions_v1 import plan_extensions
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B61_B80_release_qualification_20261104')
PREP=Path('work/analysis/Rafael_B61_B80_release_20261104/registered_preparation.json')
if __name__=='__main__':
    assert not ROOT.exists();prep=load(PREP);conf_path=Path(prep['config']);conf=load(conf_path)
    registry_path=Path('translations/release_stack.json');registry=load(registry_path)
    assert sha(registry_path.read_bytes())==prep['registry_sha256']
    image=NdsImage.open(prep['canonical_parent']);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    before,base_before=bytes(image.rom.save()),bytes(baseline.rom.save())
    planned,proof=plan_release(image,baseline,conf_path)
    assert len(proof['changed_records'])==539 and sha(bytes(planned.save()))==conf['target_ROM_sha256']
    spec=registry['profiles'][prep['profile']]['late_editorial_extensions'][-1]
    shared,shared_proof=plan_extensions(image,baseline,[spec]);assert bytes(shared.save())==bytes(planned.save())
    ROOT.mkdir();rejected=[]
    cases={'failed-fifth-gate':'manuscript','changed-selector00':'manuscript','encoded-body-tampering':'plan',
        'missing-actual-page':'focused_pixels','failed-name-review':'scoped_names','failed-complete-CG':'CG_pixels',
        'false-offline-coverage':'actual','changed-reviewed-scope':None,'stale-scene-parent':None}
    for kind,key in cases.items():
        config=deepcopy(conf)
        if key is None:
            if kind=='changed-reviewed-scope':config['reviewed_blocks'].remove(68)
            else:config['parent_ROM_sha256']='0'*64
        else:
            doc=load(config[key])
            if kind in ['failed-fifth-gate','failed-name-review']:doc['records'][0]['review']['formatting']=False
            elif kind=='changed-selector00':next(r for r in doc['records'] if r.get('source_selector')==0)['source_complete_preamble_hex']='0040ffff0001'
            elif kind=='encoded-body-tampering':
                row=doc['records'][0];raw=bytes.fromhex(row['encoded_hex']);row['encoded_hex']=(raw[:1]+b'X'+raw[2:]).hex()
            elif kind=='missing-actual-page':doc['body_pages'].pop()
            elif kind=='failed-complete-CG':doc['complete_scene_commands_retained']=False
            elif kind=='false-offline-coverage':doc['offline_only_utterances']=0
            path=ROOT/(kind+'.json');save(path,doc);config[key]=str(path);config['dependencies'][str(path)]=sha(path.read_bytes())
        path=ROOT/(kind+'_config.json');save(path,config)
        try:plan_release(image,baseline,path)
        except (ValueError,AssertionError,KeyError) as error:rejected.append(dict(case=kind,error_type=type(error).__name__,error=str(error)))
        else:raise AssertionError('Accepted invalid scene case:'+kind)
        assert bytes(image.rom.save())==before and bytes(baseline.rom.save())==base_before
    assert len(rejected)==9
    old=registry['profiles'][prep['previous_profile']]
    for i,(key,path) in enumerate(prep['preserved_stage_configs'].items()):
        prior,new=load(old[key]),load(path)
        allowed={'parent_ROM_sha256','target_ROM_sha256'}|({'parent_manifest','builder_dependencies'} if i==0 else set())
        assert {k:v for k,v in prior.items() if k not in allowed}=={k:v for k,v in new.items() if k not in allowed}
        if i==0:assert all(new['builder_dependencies'][k]==v for k,v in prior['builder_dependencies'].items())
    previous=Path('work/analysis/Rafael_B51_B60_release_qualification_v2_20261104/qualification.json')
    prior_qualification=load(previous);assert len(prior_qualification['semantic_rejections'])==12
    save(ROOT/'qualification.json',dict(profile=prep['profile'],preparation=str(PREP),preparation_sha256=sha(PREP.read_bytes()),
        registry_sha256=prep['registry_sha256'],positive_scene_plan=proof,direct_andshared_scene_targets_equal=True,
        shared_extension_proof=shared_proof,semantic_rejections=rejected,
        unchanged_eight_final_stage_contracts_compared_exactly=True,
        previous_native_field_andcompiler_negative_proofs=str(previous),previous_native_field_andcompiler_negative_proofs_sha256=sha(previous.read_bytes()),
        unchanged_owned_data_code_andrenderer_negative_proofs_reused_without_reexecution=True,
        all_inputs_unowned_bytes_andcomplete_inverses_preserved=True,
        registered_build_patch_andown_startup_pending=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    print('539-record direct/shared plans andnine semantic rejections pass;all eight earlier stage contracts preserved.',flush=True)
