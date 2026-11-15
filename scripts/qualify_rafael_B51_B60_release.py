"""Exercise the new release wiring; reuse unchanged renderer/field negative proofs."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.rafael_B51_B60_release_v1 import plan_release as scene_plan
from dk4tool.patch.registered_Fernan_name_field_v1 import plan_release as field_plan
from dk4tool.patch.late_editorial_extensions_v1 import plan_extensions
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Rafael_B51_B60_release_qualification_20261104')
PREP = Path('work/analysis/Rafael_B51_B60_release_20261104/registered_preparation.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    prep = load(PREP)
    conf_path, field_path = Path(prep['config']), Path(prep['field_config'])
    conf, field = map(load,[conf_path,field_path])
    image = NdsImage.open(prep['canonical_parent'])
    baseline = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    before, base_before = bytes(image.rom.save()), bytes(baseline.rom.save())
    planned, proof = scene_plan(image,baseline,conf_path)
    assert len(proof['changed_records']) == 249 and sha(bytes(planned.save())) == conf['target_ROM_sha256']
    stack = load('translations/release_stack.json')
    spec = stack['profiles'][prep['profile']]['late_editorial_extensions'][-1]
    shared, shared_proof = plan_extensions(image,baseline,[spec])
    assert bytes(shared.save()) == bytes(planned.save())
    ROOT.mkdir()
    rejected = []
    cases = {'failed-fifth-gate':'manuscript','changed-selector00':'manuscript','encoded-body-tampering':'plan',
             'missing-actual-page':'focused_pixels','failed-name-review':'scoped_names',
             'changed-choice-index':'manuscript','failed-menu-controller':'menu_pixels','stale-scene-parent':None}
    for kind,key in cases.items():
        config = deepcopy(conf)
        if key is None:
            config['parent_ROM_sha256'] = '0'*64
        else:
            doc = load(config[key])
            if kind in ['failed-fifth-gate','failed-name-review']:
                doc['records'][0]['review']['formatting'] = False
            elif kind == 'changed-selector00':
                next(r for r in doc['records'] if r.get('source_selector') == 0)['source_complete_preamble_hex'] = '0040ffff0001'
            elif kind == 'encoded-body-tampering':
                row = doc['records'][0]
                raw = bytes.fromhex(row['encoded_hex'])
                row['encoded_hex'] = (raw[:1]+b'X'+raw[2:]).hex()
            elif kind == 'missing-actual-page':
                doc['body_pages'].pop()
            elif kind == 'changed-choice-index':
                next(r for r in doc['records'] if r['kind'] == 'typed-choice-label')['source_index'] = 1
            elif kind == 'failed-menu-controller':
                doc['A_acceptance_followed_by_original_next_fixture_speech_observed'] = False
            path = ROOT/(kind+'.json')
            save(path,doc)
            config[key] = str(path)
            config['dependencies'][str(path)] = sha(path.read_bytes())
        path = ROOT/(kind+'_config.json')
        save(path,config)
        try:
            scene_plan(image,baseline,path)
        except (ValueError,AssertionError,KeyError) as error:
            rejected.append(dict(case=kind,error_type=type(error).__name__,error=str(error)))
        else:
            raise AssertionError('Accepted invalid scene case:'+kind)
        assert bytes(image.rom.save()) == before and bytes(baseline.rom.save()) == base_before
    scene_path = Path(prep['stage_targets'][-1]['path'])
    scene = NdsImage.open(scene_path)
    scene_before = bytes(scene.rom.save())
    arm, field_proof = field_plan(scene,field_path)
    result = deepcopy(scene)
    result.replace_file('/__arm9__.bin',arm)
    assert sha(bytes(result.rom.save())) == prep['target_ROM_sha256']
    for kind,key in [('wrong-source-owner','proposal'),('failed-original-getter','native'),('failed-actual-header','actual_pixels'),('stale-field-parent',None)]:
        config = deepcopy(field)
        if key is None:
            config['parent_ROM_sha256'] = '0'*64
        else:
            doc = load(config[key])
            if kind == 'wrong-source-owner':
                doc['fields'][0]['actor'] = 40
            elif kind == 'failed-original-getter':
                doc['original_progressive_andfull_name_getters_pass'] = False
            else:
                doc['headers'] = [h for h in doc['headers'] if h['actor_ID'] != 35]
            path = ROOT/(kind+'.json')
            save(path,doc)
            config[key] = str(path)
            config['dependencies'][str(path)] = sha(path.read_bytes())
        path = ROOT/(kind+'_config.json')
        save(path,config)
        try:
            field_plan(scene,path)
        except (ValueError,AssertionError,KeyError) as error:
            rejected.append(dict(case=kind,error_type=type(error).__name__,error=str(error)))
        else:
            raise AssertionError('Accepted invalid field case:'+kind)
        assert bytes(scene.rom.save()) == scene_before
    assert len(rejected) == 12
    old = stack['profiles']['all-routes-rafael-tutorial-name-data-20261104']
    for i,(key,path) in enumerate(prep['preserved_stage_configs'].items()):
        prior, new = load(old[key]), load(path)
        allowed = {'parent_ROM_sha256','target_ROM_sha256'} | ({'parent_manifest','builder_dependencies'} if i == 0 else set())
        assert {k:v for k,v in prior.items() if k not in allowed} == {k:v for k,v in new.items() if k not in allowed}
        if i == 0:
            assert all(new['builder_dependencies'][k] == v for k,v in prior['builder_dependencies'].items())
    save(ROOT/'qualification.json',dict(positive_scene_plan=proof,positive_field_plan=field_proof,
        direct_andshared_scene_targets_equal=True,shared_extension_proof=shared_proof,semantic_rejections=rejected,
        unchanged_seven_final_stage_contracts_compared_exactly=True,
        earlier_native_compiler_andfield_negative_proofs_reused_without_reexecution=True,
        all_inputs_unowned_bytes_andcomplete_inverses_preserved=True,
        registered_build_patch_andown_startup_pending=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    print('249-record direct/shared plans andseparate Fernan field pass;12 invalid release inputs rejected;all seven earlier stage contracts preserved.',flush=True)
