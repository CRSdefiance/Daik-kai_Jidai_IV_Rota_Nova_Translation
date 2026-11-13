"""Qualify the new SC0 adapter without repeating unchanged native renderer research."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.rafael_early_tutorial_release_v1 import plan_release
from dk4tool.patch.registered_owned_static_text_v1 import plan_release as static_plan
from dk4tool.patch.late_editorial_extensions_v1 import plan_extensions
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save

ROOT=Path('work/analysis/Rafael_early_tutorial_B42_B43_release_qualification_20261104')
PREP=Path('work/analysis/Rafael_early_tutorial_B42_B43_release_20261104/registered_preparation.json')

if __name__=='__main__':
    assert not ROOT.exists()
    prepared=load(PREP)
    config_path=Path(prepared['config'])
    conf=load(config_path)
    image=NdsImage.open(prepared['canonical_parent'])
    baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    before,base_before=bytes(image.rom.save()),bytes(baseline.rom.save())
    target,proof=plan_release(image,baseline,config_path)
    assert sha(bytes(target.save()))==prepared['pre_runtime_ROM_sha256'] and len(proof['changed_records'])==40
    ROOT.mkdir()
    rejected=[]
    for kind in ['failed-fifth-gate','encoded-glyph-tampering','changed-selector00','lost-FI-substitution','stale-scene-parent','missing-actual-page','failed-name-review']:
        config=deepcopy(conf)
        if kind=='stale-scene-parent':
            config['parent_ROM_sha256']='0'*64
        else:
            field={'encoded-glyph-tampering':'plan','lost-FI-substitution':'plan','missing-actual-page':'focused_pixels','failed-name-review':'scoped_names'}.get(kind,'manuscript')
            doc=load(config[field])
            if kind in ['failed-fifth-gate','failed-name-review']:
                doc['records'][0]['review']['formatting']=False
            elif kind=='changed-selector00':
                next(r for r in doc['records'] if r['source_selector']==0)['source_complete_preamble_hex']='0040ffff0001'
            elif kind in ['encoded-glyph-tampering','lost-FI-substitution']:
                row=next(r for r in doc['records'] if r['id']=='DK4_MES_B43_R0017')
                raw=bytes.fromhex(row['encoded_hex'])
                assert raw[1:6]==b'First' and raw.count(b'FI')==1
                row['encoded_hex']=(raw[:1]+b'X'+raw[2:] if kind=='encoded-glyph-tampering' else raw.replace(b'FI',b'FA',1)).hex()
            else:
                doc['observed_record_pages'].remove(['DK4_MES_B43_R0017',1])
            path=ROOT/(kind+'.json')
            save(path,doc)
            config[field]=str(path)
            config['dependencies'][str(path)]=sha(path.read_bytes())
        path=ROOT/(kind+'_config.json')
        save(path,config)
        try:plan_release(image,baseline,path)
        except (ValueError,AssertionError,KeyError) as error:
            rejected.append(dict(case=kind,error_type=type(error).__name__,error=str(error)))
        else:raise AssertionError('Accepted invalid case: '+kind)
        assert bytes(image.rom.save())==before and bytes(baseline.rom.save())==base_before
    assert len(rejected)==7
    registry=load('translations/release_stack.json')
    spec=registry['profiles'][prepared['profile']]['late_editorial_extensions'][-1]
    shared,_=plan_extensions(image,baseline,[spec])
    assert bytes(shared.save())==bytes(target.save())
    old_profile=registry['profiles']['all-routes-hodram-b191-b210-static-text-20261104']
    for index,(key,path) in enumerate(prepared['preserved_stage_configs'].items()):
        old,new=load(old_profile[key]),load(path)
        allowed={'parent_ROM_sha256','target_ROM_sha256'}|({'parent_manifest','builder_dependencies'} if index==0 else set())
        assert {k:v for k,v in old.items() if k not in allowed}=={k:v for k,v in new.items() if k not in allowed}
        if index==0:assert all(new['builder_dependencies'][k]==v for k,v in old['builder_dependencies'].items())
    source=NdsImage.open(prepared['post_grouped_ROM'])
    original=bytes(source.rom.save())
    arm,static_proof=static_plan(source,prepared['static_config'])
    final=deepcopy(source)
    final.replace_file('/__arm9__.bin',arm)
    assert sha(bytes(final.rom.save()))==prepared['target_ROM_sha256'] and bytes(source.rom.save())==original
    prior_path=Path('work/analysis/Hodram_B191_B210_release_qualification_20261104/qualification.json')
    prior=load(prior_path)
    assert len(prior['semantic_rejections'])==6 and prior['all_six_prior_runtime_name_static_drivers_unchanged']
    save(ROOT/'qualification.json',dict(scene_config=str(config_path),positive_scene_plan=proof,
        direct_andshared_scene_targets_equal=True,positive_static_plan=static_proof,semantic_rejections=rejected,
        all_inputs_andunowned_bytes_preserved=True,unchanged_six_final_stage_contracts_compared_exactly=True,
        unchanged_final_stage_qualification_reused=dict(path=str(prior_path),sha256=sha(prior_path.read_bytes())),
        all_six_prior_runtime_name_static_drivers_unchanged=True,registered_build_patch_andown_startup_pending=True,
        new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    print('PASS40-record direct/shared production plans;seven invalid cases rejected;six final stage contracts preserved.')
