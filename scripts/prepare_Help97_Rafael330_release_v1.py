"""Register three ordered reviewed extensions andone set ofeight preserved final-stage contracts."""
import gc,os
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.reviewed_remaining_help_release_v1 import plan_release as help_plan
from dk4tool.patch.rafael_story_b81_b84_release_v1 import plan_release as story_plan
from scripts.audit_story_glyph_consistency import load,save
from scripts.prepare_rafael_B61_B80_release import KEYS

ROOT=Path('work/analysis/Help97_Rafael330_release_20261105')
OLD='all-routes-sea22-fleet66-20261104'
PROFILE='all-routes-help97-rafael330-20261105'
RELEASE=Path('work/analysis/Sea22_Fleet66_release_verified_20261105/registered_release_verification.json')
FINALS=list(map(Path,['translations/help_deck30_Coerce33_active_terms_final_review_v1.json',
    'translations/help_remaining67_contextual_final_review_v1.json','translations/rafael_B81_B84_contextual_final_review_v1.json']))
MODULES=list(map(Path,['dk4tool/patch/reviewed_remaining_help_release_v1.py','dk4tool/patch/reviewed_remaining_help_release_v1.py',
    'dk4tool/patch/rafael_story_b81_b84_release_v1.py']))
CONFIGS=[Path('translations')/name for name in ['deck30_Coerce33_editorial_release_v1.json',
    'remaining_help67_editorial_release_v1.json','rafael_B81_B84_editorial_release_v1.json']]
STAGE_CONFIGS=[Path('translations')/(name+'_Help97_Rafael330_release_v1.json') for name in
    ['ascii_bounds','emilio_name','fernando_samwell','follower_diogo','geronimo_vasquez_alonso','abkhaz_elysion','shared_tutorial_pedro_hayreddin','Fernan_name_field']]

def identity(path):return dict(path=str(path),sha256=sha(Path(path).read_bytes()))

def main():
    registry_path=Path('translations/release_stack.json');before=registry_path.read_bytes()
    assert sha(before)=='82a17be4f7610abef225fa39c2059cd4180511af5683f519aec8171de3df5f4e'
    assert sha(Path('dk4tool/rom/nds.py').read_bytes())=='27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963'
    assert not ROOT.exists() and not any(p.exists() for p in [*CONFIGS,*STAGE_CONFIGS])
    registry,release=load(registry_path),load(RELEASE)
    assert len(registry['accepted_layers'])==114 and PROFILE not in registry['profiles']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    manifest_path=Path(release['manifest']);manifest=load(manifest_path)
    assert sha(manifest_path.read_bytes())==release['manifest_sha256'] and len(manifest['batches'])==675
    profile=deepcopy(registry['profiles'][OLD]);old_configs=[load(profile[k]) for k in KEYS]
    specs=[('production_pipeline','canonical_stage'),('owned_name_production_pipeline','post_bounds_stage'),
        ('owned_fields_production_pipeline','post_Emilio_stage'),('next_owned_fields_production_pipeline','post_prior_fields_stage'),
        ('grouped_owned_fields_production_pipeline','post_next_fields_stage'),('static_text_production_pipeline','post_grouped_fields_stage'),
        ('reviewed_text_data_production_pipeline','post_static_text_stage'),('Fernan_field_production_pipeline','post_reviewed_text_stage')]
    old_states=[Path(manifest[a][b]) for a,b in specs]+[Path(release['candidate'])]
    old_identities=[identity(p) for p in old_states]
    assert old_identities[-1]['sha256']==release['candidate_sha256']=='81511dde6bc4cd81dee799e8ce893ba06f1fa44d96bbd541ac86ca67ae2d9635'
    for i,c in enumerate(old_configs):
        assert old_identities[i]['sha256']==c['parent_ROM_sha256'] and old_identities[i+1]['sha256']==c['target_ROM_sha256']
    plans_paths=[Path('work/analysis/HELP31_active_terms_20261105/production_plan_v1.json'),
        Path('work/analysis/Remaining_HELP67_formatting_20261105/production_plan_v1.json'),
        Path('work/analysis/Rafael330_checked_20261105/release_plans.json')]
    plans=list(map(load,plans_paths));docs=list(map(load,FINALS))
    rebuilt_path=Path('work/analysis/Rafael_B81_B84_rebuilt_v3_20261105/reconstruction.json');rebuilt=load(rebuilt_path)
    resources=[Path(plans[i]['research_resource']).read_bytes() for i in [0,1]]+[Path(rebuilt['target_archive']).read_bytes()]
    assert [len(d['records']) for d in docs]==[31,67,330] and all(all(all(r['review'].values()) for r in d['records']) for d in docs)
    assert docs[0]['current_ROM_sha256']==release['candidate_sha256']
    assert plans[0]['target_HELP_sha256']==plans[1]['source_HELP_sha256']
    assert plans[0]['source_HELP_sha256']==release['target_HELP_sha256']
    final_arm9_sha256=sha(NdsImage.open(old_states[-1]).read_file('/__arm9__.bin'))
    ROOT.mkdir();(ROOT/'release_stack_before.json').write_bytes(before)
    # Only two intermediate canonical parents are needed; all eight final stage
    # targets receive the complete composite. Avoid writing27 full stage ROMs.
    states=[];previous=old_states[0]
    for i in range(3):
        image=NdsImage.open(previous);target=deepcopy(image);file=docs[i]['file_path'];old_resource=image.read_file(file)
        expected=plans[i]['source_HELP_sha256'] if i<2 else rebuilt['source_archive_sha256']
        assert sha(old_resource)==expected
        target.replace_file(file,resources[i]);rom=ROOT/f'canonical_layer{i+1}_RESEARCH_REFERENCE.nds';target.save(rom)
        assert [(p,q) for (_,p,a),(_,q,b) in zip(image.iter_files(),target.iter_files(),strict=True) if p!=q or a!=b]==[(file,file)]
        assert all(target.read_file(p)==v for p,v in image.iter_components())
        inverse=deepcopy(target);inverse.replace_file(file,old_resource);assert bytes(inverse.rom.save())==previous.read_bytes()
        states.append(rom);previous=rom;del image,target,inverse;gc.collect()
        print('Prepared canonical extension',i+1,flush=True)
    targets=[states[-1]]
    for i,parent in enumerate(old_states[1:],1):
        image=NdsImage.open(parent);target=deepcopy(image)
        originals={file:image.read_file(file) for file in ['/COMMON/HELP.DK4','/data/SC0.DK4']}
        target.replace_file('/COMMON/HELP.DK4',resources[1]);target.replace_file('/data/SC0.DK4',resources[2])
        assert {p for (_,p,a),(_,q,b) in zip(image.iter_files(),target.iter_files(),strict=True) if p!=q or a!=b}==set(originals)
        assert all(target.read_file(p)==v for p,v in image.iter_components())
        rom=ROOT/f'complete_stage{i}_RESEARCH_REFERENCE.nds';target.save(rom)
        inverse=deepcopy(target)
        for file,raw in originals.items():inverse.replace_file(file,raw)
        assert bytes(inverse.rom.save())==parent.read_bytes()
        targets.append(rom);del image,target,inverse;gc.collect()
        print('Prepared preserved final-stage target',i,flush=True)
    target_identities=[identity(p) for p in targets]
    contract=deepcopy(load(old_configs[0]['parent_manifest']));contract['batches'].extend(map(str,FINALS))
    contract.update(expected_candidate_sha256=target_identities[0]['sha256'],predecessor_manifest=str(manifest_path),
        predecessor_manifest_sha256=sha(manifest_path.read_bytes()),new_extension_configs=list(map(str,CONFIGS)))
    contract_path=ROOT/'expected_canonical_manifest_contract.json';save(contract_path,contract)
    for i,(old,path) in enumerate(zip(old_configs,STAGE_CONFIGS,strict=True)):
        value=deepcopy(old);value.update(parent_ROM_sha256=target_identities[i]['sha256'],target_ROM_sha256=target_identities[i+1]['sha256'])
        if i==0:
            value['parent_manifest']=str(contract_path)
            for dep in set(MODULES)|{Path('dk4tool/script/reviewed_FE_pagination_v1.py')}:
                value['builder_dependencies'][str(dep)]=sha(dep.read_bytes())
        allowed={'parent_ROM_sha256','target_ROM_sha256'}|({'parent_manifest','builder_dependencies'} if i==0 else set())
        assert {k:v for k,v in value.items() if k not in allowed}=={k:v for k,v in old.items() if k not in allowed}
        save(path,value)
    choices=Path('work/analysis/Rafael_B84_choices_20261105')
    b84=rebuilt['groups'][-1];menus=[]
    for obj,subpath in zip(b84['first_page_reconstruction']['native_objects'],['two_choice_native_v1','three_choice_native_v1'],strict=True):
        proof=choices/subpath/'menu_provider_and_planes.json'
        menus.append(dict(block=84,source_command_offset=obj['old_offset'],target_object_hex=obj['compiled_hex'],
            source_native_receipt=str(proof),source_native_receipt_sha256=sha(proof.read_bytes())))
    menu_path=ROOT/'typed_menu_qualification.json';save(menu_path,dict(menus=menus,typed_labels=5,offline_visual_approved=True,
        native_visual_approval=str(choices/'complete_native_visual_approval_v1.json'),actual_controller_proofs=[
            'work/analysis/Rafael330_menu_actual_pixels_v2_20261105/menu_actual_pixels.json',
            'work/analysis/Rafael330_menu_cursor_actual_pixels_v2_20261105/menu_actual_pixels.json'],new_credit=0))
    evidence=[
        dict(manuscript=FINALS[0],plan=plans_paths[0],native=Path('work/analysis/HELP31_active_terms_20261105/native_pages_v1/native_help_pages.json'),
            visual=Path('work/analysis/HELP31_active_terms_20261105/preview_qualification_v1/direct_visual_approval.json'),
            actual=Path('work/analysis/HELP31_active_terms_20261105/focused_navigation_checked_v1/ordinary_gameplay_verification.json'),
            actual_visual=Path('work/analysis/HELP31_active_terms_20261105/focused_navigation_checked_v1/direct_actual_visual_approval.json'),target_resource=Path(plans[0]['research_resource'])),
        dict(manuscript=FINALS[1],plan=plans_paths[1],native=Path('work/analysis/Remaining_HELP67_formatting_20261105/native_pages_v3/native_help_pages.json'),
            visual=Path('work/analysis/Remaining_HELP67_formatting_20261105/preview_qualification_v3/direct_visual_approval.json'),
            actual=Path('work/analysis/Remaining_HELP67_formatting_20261105/focused_navigation_checked_v1/ordinary_gameplay_verification.json'),
            actual_visual=Path('work/analysis/Remaining_HELP67_formatting_20261105/focused_navigation_checked_v1/direct_actual_visual_approval.json'),target_resource=Path(plans[1]['research_resource'])),
        dict(manuscript=FINALS[2],plan=plans_paths[2],reconstruction=rebuilt_path,
            compiled_native=Path('work/analysis/Rafael330_stored_consumer_inputs_v3_20261105/native_consumer_planes.json'),
            consumer_reconstruction=Path('work/analysis/Rafael330_stored_consumer_inputs_v3_20261105/native_consumer_reconstruction.json'),
            stored_native=Path('work/analysis/Rafael330_stored_native_v3_20261105/stored_native_verification.json'),
            stored_lookup=Path('work/analysis/Rafael330_stored_catalogue_v3_20261105/all327_stored_effective_body_bindings.json'),
            loaders=Path('work/analysis/Rafael330_loaders_v3_20261105/verification.json'),
            visual_review=Path('work/analysis/Rafael330_checked_20261105/complete_visual_approval.json'),
            actual=Path('work/analysis/Rafael330_checked_20261105/actual_review.json'),
            scoped_names=Path('translations/rafael_B81_B84_scoped_names_actual_final_v1.json'),typed_menu=menu_path)]
    common_deps=set(MODULES)|{Path(__file__),Path('dk4tool/script/reviewed_FE_pagination_v1.py'),
        Path('dk4tool/script/reviewed_scene_rebuild.py'),Path('dk4tool/script/reviewed_scene_rebuild_v2.py'),
        Path('dk4tool/script/reviewed_scene_rebuild_v3.py'),Path('dk4tool/patch/reviewed_scene_batch_v5.py'),
        Path('dk4tool/dialogue/reviewed_choice_object_v2.py'),Path('dk4tool/dialogue/help_source_links.py'),
        Path('scripts/source_locked_derivation_v5118.py'),Path('scripts/prepare_help_pages_v281.py')}
    common_deps.update(Path('dk4tool/dialogue')/f'reviewed_help_pages_v{i}.py' for i in range(1,17))
    proofs=[];new_specs=[]
    for i,(e,config_path,planner) in enumerate(zip(evidence,CONFIGS,[help_plan,help_plan,story_plan],strict=True)):
        parent=old_states[0] if i==0 else states[i-1]
        dependencies=common_deps|set(e.values())|{Path(p) for p in docs[i].get('formatting_evidence',docs[i].get('evidence',{}))}
        config=dict(format='dk4-reviewed-remaining-help-release-v1' if i<2 else 'dk4-rafael-B81-B84-release-v1',
            **{k:str(v) for k,v in e.items()},record_count=[31,67,330][i],
            canonical_ROM_sha256=sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()),
            clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
            parent_ROM_sha256=sha(parent.read_bytes()),target_ROM_sha256=sha(states[i].read_bytes()),
            pre_runtime_ARM9_sha256=sha(NdsImage.open(parent).read_file('/__arm9__.bin')),
            final_runtime_ARM9_sha256=final_arm9_sha256,right_bound_configuration=str(STAGE_CONFIGS[0]),
            dependencies={str(p):sha(p.read_bytes()) for p in sorted(dependencies)})
        if i<2:config.update(kind=['deck31','remaining67'][i],target_HELP_sha256=sha(resources[i]),
            final_dependency_ROM=release['candidate'],final_dependency_ROM_sha256=release['candidate_sha256'])
        else:config['blocks']=[81,82,83,84]
        save(config_path,config)
        planned,proof=planner(NdsImage.open(parent),NdsImage.open('out/raphael_natural_v2_accepted_base.nds'),config_path)
        assert sha(bytes(planned.save()))==config['target_ROM_sha256'] and len(proof['changed_records'])==[31,67,330][i]
        proofs.append(proof)
        new_specs.append(dict(id=['deck30-Coerce33-active','remaining-help67','rafael-b81-b84'][i],
            module=['dk4tool.patch.reviewed_remaining_help_release_v1','dk4tool.patch.reviewed_remaining_help_release_v1','dk4tool.patch.rafael_story_b81_b84_release_v1'][i],
            module_sha256=sha(MODULES[i].read_bytes()),config=str(config_path),config_sha256=sha(config_path.read_bytes()),
            parent_ROM_sha256=config['parent_ROM_sha256'],target_ROM_sha256=config['target_ROM_sha256']))
        del planned;gc.collect();print('Pure source-bound extension plan passes:',i+1,flush=True)
    save(ROOT/'positive_prepublication_plans.json',dict(layers=proofs,all_eight_final_stage_component_transitions_preserved=True,
        new_source_articles_anddialogue_objects=427,one_previously_credited_amendment=33,no_registry_mutation_yet=True))
    profile['late_editorial_extensions'].extend(new_specs);profile.update(dict(zip(KEYS,map(str,STAGE_CONFIGS))))
    profile['note']='Experimental cumulative Help97 plusRafael330:427 new editorial decisions,Coerce33 amendment zero duplicate credit;all114 accepted layers/eight final stages preserved. All336 Rafael bodypages/five captions and103 Help pages checked;honest representative actual/offline provenance. No main promotion;full scope active;no guide photos.'
    registry['profiles'][PROFILE]=profile;prior=load(ROOT/'release_stack_before.json')
    assert all(registry[k]==v for k,v in prior.items() if k!='profiles') and all(registry['profiles'][k]==v for k,v in prior['profiles'].items())
    assert registry_path.read_bytes()==before
    temporary=registry_path.with_name('release_stack.Help97_Rafael330.pending.json');assert not temporary.exists();save(temporary,registry);os.replace(temporary,registry_path)
    save(ROOT/'registered_preparation.json',dict(profile=PROFILE,previous_profile=OLD,configs=list(map(str,CONFIGS)),new_extension_specs=new_specs,
        canonical_parent=str(old_states[0]),canonical_parent_sha256=old_identities[0]['sha256'],
        ordered_canonical_targets=[identity(p) for p in states],stage_targets=target_identities,old_stage_states=old_identities,
        preserved_stage_configs=dict(zip(KEYS,map(str,STAGE_CONFIGS))),final_ROM=str(targets[-1]),target_ROM_sha256=target_identities[-1]['sha256'],
        registry_sha256=sha(registry_path.read_bytes()),expected_manifest_entries=678,accepted_layers=114,previous_profiles_preserved=True,
        new_source_editorial_objects=427,previously_credited_amendments=[33],new_credit=0,main_unchanged=True,
        semantic_qualification_andregistered_build_pending=True))
    pins_path=Path('translations/rom_retention_pins.json');pin_before=pins_path.read_bytes();pins=load(pins_path);(ROOT/'pins.before.json').write_bytes(pin_before)
    for path in [*states,*targets[1:]]:
        assert not any(Path(p['path']).resolve()==path.resolve() for p in pins)
        pins.append(dict(path=str(path.resolve()),reason='Preserve ordered Help97/Rafael330 registered research reference. SHA256 '+sha(path.read_bytes())))
    temporary=pins_path.with_name('rom_retention_pins.Help97_Rafael330.pending.json');assert not temporary.exists();save(temporary,pins)
    assert pins_path.read_bytes()==pin_before;os.replace(temporary,pins_path)
    print('Registered678-entry successor:427 new source objects pluszero-credit amendment,114 accepted layers/eight final stages. Qualification/build pending.')

if __name__=='__main__':main()
