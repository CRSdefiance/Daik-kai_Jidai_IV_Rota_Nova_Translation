"""Prepare/requalify all eight ordered stages before publishing one experimental profile."""
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.rafael_B51_B60_release_v1 import plan_release as scene_plan
from dk4tool.patch.registered_reviewed_text_data_v3 import plan_release as data_plan
from dk4tool.patch.registered_Fernan_name_field_v1 import plan_release as field_plan
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Rafael_B51_B60_release_20261104')
CHECKED = Path('work/analysis/Rafael_B51_B60_checked_20261104')
INPUT = Path('work/analysis/Rafael_B51_B60_current_runtime_20261104')
OLD = 'all-routes-rafael-tutorial-name-data-20261104'
PROFILE = 'all-routes-rafael-b51-b60-Fernan-20261104'
CONFIG = Path('translations/rafael_B51_B60_editorial_release_v1.json')
FIELD_CONFIG = Path('translations/Fernan_name_field_rafael_B51_B60_release_v1.json')
MODULE = Path('dk4tool/patch/rafael_B51_B60_release_v1.py')
FIELD_MODULE = Path('dk4tool/patch/registered_Fernan_name_field_v1.py')
DRIVER = Path('scripts/build_integrated_release_with_Fernan_field.py')
KEYS = ['ascii_glyph_right_bounds','owned_name_glyph','owned_name_fields','owned_name_fields_next',
        'owned_name_fields_grouped','owned_static_text','owned_reviewed_text_data']
STAGE_CONFIGS = [Path('translations')/(name+'_rafael_B51_B60_release_v1.json') for name in
    ['ascii_bounds','emilio_name','fernando_samwell','follower_diogo','geronimo_vasquez_alonso','abkhaz_elysion','shared_tutorial_pedro_hayreddin']]

if __name__ == '__main__':
    assert not ROOT.exists() and not CONFIG.exists() and not FIELD_CONFIG.exists() and not any(p.exists() for p in STAGE_CONFIGS)
    registry_path = Path('translations/release_stack.json')
    before = registry_path.read_bytes()
    assert sha(before) == '40af555fb1e53625b5f8964b3beb35c53a6523a83f9b54eae8143e6fb1206f68'
    registry = load(registry_path)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers']) == 114
    profile = deepcopy(registry['profiles'][OLD])
    old_configs = [load(profile[k]) for k in KEYS]
    manifest_path = Path('out/all_routes_combined_rafael_tutorial_name_data_20261104_candidate.manifest.json')
    manifest = load(manifest_path)
    specs = [('production_pipeline','canonical_stage'),('owned_name_production_pipeline','post_bounds_stage'),
        ('owned_fields_production_pipeline','post_Emilio_stage'),('next_owned_fields_production_pipeline','post_prior_fields_stage'),
        ('grouped_owned_fields_production_pipeline','post_next_fields_stage'),('static_text_production_pipeline','post_grouped_fields_stage'),
        ('reviewed_text_data_production_pipeline','post_static_text_stage')]
    old_states = [Path(manifest[a][b]) for a,b in specs] + [Path(manifest['candidate_rom'])]
    rebuilt_path = Path('work/analysis/Rafael_B51_B60_rebuilt_20261104/reconstruction.json')
    rebuilt = load(rebuilt_path)
    final = Path('translations/rafael_B51_B60_contextual_final_review_v1.json')
    doc = load(final)
    assert len(doc['records']) == 249 and all(all(r['review'].values()) for r in doc['records'])
    assert sha(old_states[-1].read_bytes()) == manifest['candidate_sha256'] == rebuilt['parent_sha256']
    for i,conf in enumerate(old_configs):
        assert sha(old_states[i].read_bytes()) == conf['parent_ROM_sha256'] and sha(old_states[i+1].read_bytes()) == conf['target_ROM_sha256']
    archive = Path(rebuilt['target_archive']).read_bytes()
    assert sha(archive) == rebuilt['target_archive_sha256']
    ROOT.mkdir()
    (ROOT/'release_stack_before.json').write_bytes(before)
    targets = []
    for i,old in enumerate(old_states[:-1]):
        original, target = NdsImage.open(old), NdsImage.open(old)
        target.replace_file(doc['file_path'],archive)
        assert [p for _,p,v in original.iter_files() if target.read_file(p) != v] == [doc['file_path']]
        assert all(target.read_file(p) == v for p,v in original.iter_components())
        path = ROOT/f'stage_{i}_RESEARCH_REFERENCE.nds'
        target.save(path)
        inverse = NdsImage.open(path)
        inverse.replace_file(doc['file_path'],original.read_file(doc['file_path']))
        assert bytes(inverse.rom.save()) == old.read_bytes()
        targets.append(path)
    scene = Path(rebuilt['research_ROM'])
    assert sha(scene.read_bytes()) == rebuilt['research_ROM_sha256']
    expected = NdsImage.open(old_states[-1])
    expected.replace_file(doc['file_path'],archive)
    assert bytes(expected.rom.save()) == scene.read_bytes()
    targets.append(scene)
    composition = load('work/analysis/Rafael_B51_B60_focused_20261104/composition.json')
    combined = Path(composition['research_ROM'])
    assert sha(combined.read_bytes()) == composition['research_ROM_sha256']
    contract = deepcopy(load(old_configs[0]['parent_manifest']))
    contract['batches'].append(str(final))
    contract.update(expected_candidate_sha256=sha(targets[0].read_bytes()),predecessor_manifest=str(manifest_path),
        predecessor_manifest_sha256=sha(manifest_path.read_bytes()),new_extension_configs=[str(CONFIG)])
    contract_path = ROOT/'expected_canonical_manifest_contract.json'
    save(contract_path,contract)
    for i,(old,path) in enumerate(zip(old_configs,STAGE_CONFIGS,strict=True)):
        value = deepcopy(old)
        value.update(parent_ROM_sha256=sha(targets[i].read_bytes()),target_ROM_sha256=sha(targets[i+1].read_bytes()))
        if i == 0:
            value['parent_manifest'] = str(contract_path)
            for dep in [MODULE,Path('dk4tool/script/reviewed_scene_rebuild_v3.py')]:
                value['builder_dependencies'][str(dep)] = sha(dep.read_bytes())
        allowed = {'parent_ROM_sha256','target_ROM_sha256'} | ({'parent_manifest','builder_dependencies'} if i == 0 else set())
        assert {k:v for k,v in value.items() if k not in allowed} == {k:v for k,v in old.items() if k not in allowed}
        save(path,value)
    evidence = dict(manuscript=final,plan=CHECKED/'release_plans.json',reconstruction=rebuilt_path,
        stored_native=Path('work/analysis/Rafael_B51_B60_stored_native_20261104/stored_native_verification.json'),
        stored_lookup=Path('work/analysis/Rafael_B51_B60_stored_catalogue_20261104/all245_stored_effective_body_bindings.json'),
        loaders=Path('work/analysis/Rafael_B51_B60_loaders_20261104/verification.json'),actual=CHECKED/'actual_review.json',
        compiled_native=INPUT/'compatible_native_pages.json',visual_review=Path('work/analysis/Rafael_B51_B60_formatting_20261104/body_display_approval_v4.json'),
        typed_menu=INPUT/'compatible_menu_objects.json',native_styles=INPUT/'no_style_objects.json',
        scoped_names=Path('translations/rafael_B51_B60_scoped_names_actual_final_v2.json'),
        focused_pixels=Path('work/analysis/Rafael_B51_B60_focused_pixels_20261104/focused_actual_pixels.json'),
        menu_pixels=Path('work/analysis/Rafael_B60_menu_actual_pixels_20261104/menu_actual_pixels.json'))
    deps = set(evidence.values()) | {Path(p) for p in doc['formatting_evidence']} | {
        MODULE,Path('dk4tool/patch/reviewed_scene_batch_v5.py'),Path('dk4tool/script/reviewed_scene_rebuild.py'),
        Path('dk4tool/script/reviewed_scene_rebuild_v2.py'),Path('dk4tool/script/reviewed_scene_rebuild_v3.py'),
        Path('scripts/source_locked_derivation_v5118.py'),Path(__file__)}
    config = dict(format='dk4-rafael-B51-B60-release-v1',**{k:str(v) for k,v in evidence.items()},record_count=249,blocks=list(range(51,61)),
        canonical_ROM_sha256=sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()),clean_ROM='work/clean.nds',
        clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),parent_ROM_sha256=sha(old_states[0].read_bytes()),
        target_ROM_sha256=sha(targets[0].read_bytes()),pre_runtime_ARM9_sha256=sha(NdsImage.open(old_states[0]).read_file('/__arm9__.bin')),
        right_bound_configuration=str(STAGE_CONFIGS[0]),dependencies={str(p):sha(p.read_bytes()) for p in sorted(deps)})
    save(CONFIG,config)
    field_evidence = dict(manuscript=evidence['scoped_names'],proposal=INPUT/'Fernan_owned_fields_proposal.json',
        rebased_plan=INPUT/'Fernan_owned_fields_plan.json',native=Path('work/analysis/Rafael_Fernan_name_native_20261104/native_name_fields_verification.json'),
        dependency_qualification=INPUT/'dependency_qualification.json',actual_pixels=evidence['focused_pixels'],actual_visual=CHECKED/'actual_visual_approval.json',
        tested_ARM9=INPUT/'Fernan_proposed_ARM9_RESEARCH_ONLY.bin')
    field_deps = set(field_evidence.values()) | {FIELD_MODULE,DRIVER,Path('dk4tool/patch/owned_name_fields_v2.py'),Path(__file__)}
    field_config = dict(format='dk4-registered-Fernan-name-field-v1',**{k:str(v) for k,v in field_evidence.items()},
        clean_ROM=config['clean_ROM'],clean_ROM_sha256=config['clean_ROM_sha256'],parent_ROM_sha256=sha(scene.read_bytes()),
        target_ROM_sha256=sha(combined.read_bytes()),target_ARM9_sha256=sha(field_evidence['tested_ARM9'].read_bytes()),
        dependencies={str(p):sha(p.read_bytes()) for p in sorted(field_deps)})
    save(FIELD_CONFIG,field_config)
    planned,scene_proof = scene_plan(NdsImage.open(old_states[0]),NdsImage.open('out/raphael_natural_v2_accepted_base.nds'),CONFIG)
    assert sha(bytes(planned.save())) == config['target_ROM_sha256'] and len(scene_proof['changed_records']) == 249
    source = NdsImage.open(targets[6])
    arm,data_proof = data_plan(source,STAGE_CONFIGS[6])
    staged = deepcopy(source)
    staged.replace_file('/__arm9__.bin',arm)
    assert bytes(staged.rom.save()) == scene.read_bytes()
    arm,field_proof = field_plan(NdsImage.open(scene),FIELD_CONFIG)
    staged = NdsImage.open(scene)
    staged.replace_file('/__arm9__.bin',arm)
    assert bytes(staged.rom.save()) == combined.read_bytes()
    save(ROOT/'positive_prepublication_plans.json',dict(scene=scene_proof,data=data_proof,Fernan=field_proof,
        all_seven_prior_stage_configs_only_whole_ROM_identity_rebased=True,no_registry_mutation_yet=True))
    profile['late_editorial_extensions'].append(dict(id='rafael-b51-b60',module='dk4tool.patch.rafael_B51_B60_release_v1',
        module_sha256=sha(MODULE.read_bytes()),config=str(CONFIG),config_sha256=sha(CONFIG.read_bytes()),
        parent_ROM_sha256=config['parent_ROM_sha256'],target_ROM_sha256=config['target_ROM_sha256']))
    profile.update(dict(zip(KEYS,map(str,STAGE_CONFIGS))))
    profile['owned_Fernan_name_field'] = str(FIELD_CONFIG)
    profile['note'] = 'Experimental cumulative Rafael B51-B60:249 reviews/102 revisions/147 retentions,38 wraps/3 I glyphs;exclusive Fernan F field. Preserve114 accepted layers/all seven earlier stages;Fernan-field build driver required. No main promotion;full scope active;no guide photos.'
    registry['profiles'][PROFILE] = profile
    prior = load(ROOT/'release_stack_before.json')
    assert all(registry[k] == v for k,v in prior.items() if k != 'profiles')
    assert all(registry['profiles'][k] == v for k,v in prior['profiles'].items())
    assert registry_path.read_bytes() == before
    staged_path = registry_path.with_name('release_stack.Rafael_B51_B60.pending.json')
    assert not staged_path.exists()
    save(staged_path,registry)
    os.replace(staged_path,registry_path)
    save(ROOT/'registered_preparation.json',dict(profile=PROFILE,config=str(CONFIG),field_config=str(FIELD_CONFIG),
        canonical_parent=str(old_states[0]),canonical_parent_sha256=config['parent_ROM_sha256'],
        preserved_stage_configs=dict(zip(KEYS,map(str,STAGE_CONFIGS))),
        stage_targets=[dict(path=str(p),sha256=sha(p.read_bytes())) for p in targets],
        final_ROM=str(combined),target_ROM_sha256=sha(combined.read_bytes()),registry_sha256=sha(registry_path.read_bytes()),
        accepted_layers=114,previous_profiles_preserved=True,all_prior_drivers_anddata_qualification_dependencies_unchanged=True,
        new_credit=0,main_unchanged=True,semantic_qualification_andregistered_build_pending=True))
    pins_path = Path('translations/rom_retention_pins.json')
    pin_before = pins_path.read_bytes()
    pins = load(pins_path)
    (ROOT/'pins.before.json').write_bytes(pin_before)
    for path in targets[:-1]:
        assert not any(Path(p['path']).resolve() == path.resolve() for p in pins)
        pins.append(dict(path=str(path.resolve()),reason='Preserve exact registered Rafael B51-B60 stage reference; all ROMs retained. SHA256 '+sha(path.read_bytes())))
    temporary = pins_path.with_name('rom_retention_pins.Rafael_B51_B60_release.pending.json')
    assert not temporary.exists()
    save(temporary,pins)
    assert pins_path.read_bytes() == pin_before
    os.replace(temporary,pins_path)
    print('Registered249-review SC0 successor andseparate Fernan field;114 accepted layers/seven prior stages preserved. Semantic qualification/build next.',flush=True)
