"""Register539 reviewed speeches while preserving all eight final-stage contracts."""
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.rafael_story_b61_b80_release_v1 import plan_release
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B61_B80_release_20261104')
CHECKED=Path('work/analysis/Rafael_B61_B80_checked_20261104')
FORMAT=Path('work/analysis/Rafael_B61_B80_formatting_20261104')
OLD='all-routes-rafael-b51-b60-Fernan-20261104'
PROFILE='all-routes-rafael-b61-b80-20261104'
CONFIG=Path('translations/rafael_B61_B80_editorial_release_v1.json')
MODULE=Path('dk4tool/patch/rafael_story_b61_b80_release_v1.py')
KEYS=['ascii_glyph_right_bounds','owned_name_glyph','owned_name_fields','owned_name_fields_next',
    'owned_name_fields_grouped','owned_static_text','owned_reviewed_text_data','owned_Fernan_name_field']
STAGE_CONFIGS=[Path('translations')/(name+'_rafael_B61_B80_release_v1.json') for name in
    ['ascii_bounds','emilio_name','fernando_samwell','follower_diogo','geronimo_vasquez_alonso','abkhaz_elysion','shared_tutorial_pedro_hayreddin','Fernan_name_field']]

if __name__=='__main__':
    registry_path=Path('translations/release_stack.json');before=registry_path.read_bytes()
    assert sha(before)=='1c8212e74a7c786de5895e59492850596e115c945a6a5f2f6d16312d4d525893'
    assert not ROOT.exists() and not CONFIG.exists() and not any(p.exists() for p in STAGE_CONFIGS)
    registry=load(registry_path);assert len(registry['accepted_layers'])==114 and PROFILE not in registry['profiles']
    profile=deepcopy(registry['profiles'][OLD]);old_configs=[load(profile[k]) for k in KEYS]
    manifest_path=Path('out/all_routes_combined_rafael_b51_b60_Fernan_20261104_candidate.manifest.json')
    manifest=load(manifest_path)
    specs=[('production_pipeline','canonical_stage'),('owned_name_production_pipeline','post_bounds_stage'),
        ('owned_fields_production_pipeline','post_Emilio_stage'),('next_owned_fields_production_pipeline','post_prior_fields_stage'),
        ('grouped_owned_fields_production_pipeline','post_next_fields_stage'),('static_text_production_pipeline','post_grouped_fields_stage'),
        ('reviewed_text_data_production_pipeline','post_static_text_stage'),('Fernan_field_production_pipeline','post_reviewed_text_stage')]
    old_states=[Path(manifest[a][b]) for a,b in specs]+[Path(manifest['candidate_rom'])]
    rebuilt_path=Path('work/analysis/Rafael_B61_B80_rebuilt_v12_20261104/reconstruction.json');rebuilt=load(rebuilt_path)
    final=Path('translations/rafael_B61_B80_contextual_final_review_v1.json');doc=load(final)
    assert len(doc['records'])==539 and all(all(r['review'].values()) for r in doc['records'])
    assert sha(old_states[-1].read_bytes())==manifest['candidate_sha256']==rebuilt['parent_sha256']
    for i,conf in enumerate(old_configs):
        assert sha(old_states[i].read_bytes())==conf['parent_ROM_sha256']
        assert sha(old_states[i+1].read_bytes())==conf['target_ROM_sha256']
    archive=Path(rebuilt['target_archive']).read_bytes();assert sha(archive)==rebuilt['target_archive_sha256']
    ROOT.mkdir();(ROOT/'release_stack_before.json').write_bytes(before)
    targets=[]
    for i,old in enumerate(old_states[:-1]):
        original,target=NdsImage.open(old),NdsImage.open(old)
        target.replace_file(doc['file_path'],archive)
        assert [p for _,p,v in original.iter_files() if target.read_file(p)!=v]==[doc['file_path']]
        assert all(target.read_file(p)==v for p,v in original.iter_components())
        path=ROOT/f'stage_{i}_RESEARCH_REFERENCE.nds';target.save(path)
        inverse=NdsImage.open(path);inverse.replace_file(doc['file_path'],original.read_file(doc['file_path']))
        assert bytes(inverse.rom.save())==old.read_bytes();targets.append(path)
    scene=Path(rebuilt['research_ROM']);assert sha(scene.read_bytes())==rebuilt['research_ROM_sha256']
    expected=NdsImage.open(old_states[-1]);expected.replace_file(doc['file_path'],archive)
    assert bytes(expected.rom.save())==scene.read_bytes();targets.append(scene)
    contract=deepcopy(load(old_configs[0]['parent_manifest']))
    contract['batches'].append(str(final))
    contract.update(expected_candidate_sha256=sha(targets[0].read_bytes()),predecessor_manifest=str(manifest_path),
        predecessor_manifest_sha256=sha(manifest_path.read_bytes()),new_extension_configs=[str(CONFIG)])
    contract_path=ROOT/'expected_canonical_manifest_contract.json';save(contract_path,contract)
    for i,(old,path) in enumerate(zip(old_configs,STAGE_CONFIGS,strict=True)):
        value=deepcopy(old);value.update(parent_ROM_sha256=sha(targets[i].read_bytes()),target_ROM_sha256=sha(targets[i+1].read_bytes()))
        if i==0:
            value['parent_manifest']=str(contract_path)
            for dep in [MODULE,Path('dk4tool/script/reviewed_scene_rebuild_v3.py')]:value['builder_dependencies'][str(dep)]=sha(dep.read_bytes())
        allowed={'parent_ROM_sha256','target_ROM_sha256'}|({'parent_manifest','builder_dependencies'} if i==0 else set())
        assert {k:v for k,v in value.items() if k not in allowed}=={k:v for k,v in old.items() if k not in allowed}
        assert all(NdsImage.open(targets[i+n]).read_file('/__arm9__.bin')==NdsImage.open(old_states[i+n]).read_file('/__arm9__.bin') for n in [0,1])
        save(path,value)
    evidence=dict(manuscript=final,plan=CHECKED/'release_plans.json',reconstruction=rebuilt_path,
        stored_native=Path('work/analysis/Rafael_B61_B80_stored_native_v12_20261104/stored_native_verification.json'),
        stored_lookup=Path('work/analysis/Rafael_B61_B80_stored_catalogue_v12_20261104/all539_stored_effective_body_bindings.json'),
        loaders=Path('work/analysis/Rafael_B61_B80_loaders_v12_20261104/verification.json'),actual=CHECKED/'actual_review.json',
        compiled_native=FORMAT/'combined_native_v12.json',visual_review=FORMAT/'body_display_approval_v12.json',
        typed_menu=FORMAT/'no_menu_objects_v12.json',native_styles=FORMAT/'no_style_objects_v12.json',
        scoped_names=Path('translations/rafael_B61_B80_scoped_names_actual_final_v1.json'),
        focused_pixels=Path('work/analysis/Rafael_B61_B80_names_pagination_pixels_v12_20261104/focused_actual_pixels.json'),
        CG_pixels=Path('work/analysis/Rafael_B69_complete_scene_pixels_v12_20261104/focused_actual_pixels.json'))
    deps=set(evidence.values())|{Path(p) for p in doc['formatting_evidence']}|{
        MODULE,Path('dk4tool/patch/rafael_B51_B60_release_v1.py'),Path('dk4tool/patch/reviewed_scene_batch_v5.py'),
        Path('dk4tool/script/reviewed_scene_rebuild.py'),Path('dk4tool/script/reviewed_scene_rebuild_v2.py'),
        Path('dk4tool/script/reviewed_scene_rebuild_v3.py'),Path('scripts/source_locked_derivation_v5118.py'),Path(__file__)}
    config=dict(format='dk4-rafael-B61-B80-release-v1',**{k:str(v) for k,v in evidence.items()},record_count=539,
        blocks=rebuilt['changed_blocks'],reviewed_blocks=doc['blocks'],
        canonical_ROM_sha256=sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()),clean_ROM='work/clean.nds',
        clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),parent_ROM_sha256=sha(old_states[0].read_bytes()),
        target_ROM_sha256=sha(targets[0].read_bytes()),pre_runtime_ARM9_sha256=sha(NdsImage.open(old_states[0]).read_file('/__arm9__.bin')),
        right_bound_configuration=str(STAGE_CONFIGS[0]),dependencies={str(p):sha(p.read_bytes()) for p in sorted(deps)})
    save(CONFIG,config)
    planned,proof=plan_release(NdsImage.open(old_states[0]),NdsImage.open('out/raphael_natural_v2_accepted_base.nds'),CONFIG)
    assert sha(bytes(planned.save()))==config['target_ROM_sha256'] and len(proof['changed_records'])==539
    save(ROOT/'positive_prepublication_plan.json',dict(scene=proof,all_eight_ARM9_transitions_identical_to_verified_predecessor=True,
        no_registry_mutation_yet=True))
    profile['late_editorial_extensions'].append(dict(id='rafael-b61-b80',module='dk4tool.patch.rafael_story_b61_b80_release_v1',
        module_sha256=sha(MODULE.read_bytes()),config=str(CONFIG),config_sha256=sha(CONFIG.read_bytes()),
        parent_ROM_sha256=config['parent_ROM_sha256'],target_ROM_sha256=config['target_ROM_sha256']))
    profile.update(dict(zip(KEYS,map(str,STAGE_CONFIGS))))
    profile['note']='Experimental cumulative Rafael539:210 revisions/329 retentions;545 pages,22 names,14 layout refinements/16 I/14 ellipsis fixes.95 utterances observed/444 offline-only. Preserve114 accepted layers/all eight stages including Fernan F. No main promotion;full scope active;no guide photos.'
    registry['profiles'][PROFILE]=profile;prior=load(ROOT/'release_stack_before.json')
    assert all(registry[k]==v for k,v in prior.items() if k!='profiles')
    assert all(registry['profiles'][k]==v for k,v in prior['profiles'].items()) and registry_path.read_bytes()==before
    staged=registry_path.with_name('release_stack.Rafael_B61_B80.pending.json');assert not staged.exists()
    save(staged,registry);os.replace(staged,registry_path)
    save(ROOT/'registered_preparation.json',dict(profile=PROFILE,previous_profile=OLD,config=str(CONFIG),
        canonical_parent=str(old_states[0]),canonical_parent_sha256=config['parent_ROM_sha256'],
        preserved_stage_configs=dict(zip(KEYS,map(str,STAGE_CONFIGS))),
        old_stage_states=[dict(path=str(p),sha256=sha(p.read_bytes())) for p in old_states],
        stage_targets=[dict(path=str(p),sha256=sha(p.read_bytes())) for p in targets],
        final_ROM=str(scene),target_ROM_sha256=sha(scene.read_bytes()),registry_sha256=sha(registry_path.read_bytes()),
        accepted_layers=114,previous_profiles_preserved=True,new_credit=0,main_unchanged=True,
        semantic_qualification_andregistered_build_pending=True))
    pins_path=Path('translations/rom_retention_pins.json');pin_before=pins_path.read_bytes();pins=load(pins_path)
    (ROOT/'pins.before.json').write_bytes(pin_before)
    for path in targets[:-1]:
        assert not any(Path(p['path']).resolve()==path.resolve() for p in pins)
        pins.append(dict(path=str(path.resolve()),reason='Preserve registered Rafael539 stage reference;all prior ROMs retained. SHA256 '+sha(path.read_bytes())))
    temporary=pins_path.with_name('rom_retention_pins.Rafael_B61_B80_release.pending.json');assert not temporary.exists()
    save(temporary,pins);assert pins_path.read_bytes()==pin_before;os.replace(temporary,pins_path)
    print('Registered539-review experimental successor;114 accepted layers/all eight final-stage contracts preserved. Qualification/build next.',flush=True)
