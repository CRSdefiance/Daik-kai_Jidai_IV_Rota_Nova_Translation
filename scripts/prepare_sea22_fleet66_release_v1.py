"""Register two ordered reviewed Help layers with the complete accepted stack and eight final stages."""
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.sea_help22_release_v1 import plan_release as sea_plan
from dk4tool.patch.fleet_help66_amendment_release_v1 import plan_release as fleet_plan
from scripts.audit_story_glyph_consistency import load,save
from scripts.prepare_rafael_B61_B80_release import KEYS

ROOT=Path('work/analysis/Sea22_Fleet66_release_20261104')
RELEASE=Path('work/analysis/Shipyard_HELP37_release_verified_20261104/registered_release_verification.json')
OLD='all-routes-shipyard-help37-20261104'
PROFILE='all-routes-sea22-fleet66-20261104'
SEA=Path('work/analysis/Shared_HELP_T81_T102_formatting_20261104')
FLEET=Path('work/analysis/HELP66_Command_amendment_20261104')
CONFIGS=[Path('translations/sea_help22_editorial_release_v1.json'),Path('translations/fleet_help66_amendment_release_v1.json')]
MODULES=[Path('dk4tool/patch/sea_help22_release_v1.py'),Path('dk4tool/patch/fleet_help66_amendment_release_v1.py')]
FINALS=[Path('translations/help_sea22_contextual_final_review_v1.json'),Path('translations/help_fleet66_Command_contextual_amendment_v2.json')]
STAGE_CONFIGS=[Path('translations')/(name+'_sea22_fleet66_release_v1.json')for name in
    ['ascii_bounds','emilio_name','fernando_samwell','follower_diogo','geronimo_vasquez_alonso','abkhaz_elysion','shared_tutorial_pedro_hayreddin','Fernan_name_field']]

if __name__=='__main__':
    registry_path=Path('translations/release_stack.json');before=registry_path.read_bytes()
    assert sha(before)=='9d4a352f95f67c847a9ae29f7dd7f93a1a209c79720d070d253d5fe202299c35'
    assert not ROOT.exists() and not any(p.exists()for p in [*CONFIGS,*STAGE_CONFIGS])
    registry=load(registry_path);release=load(RELEASE);assert len(registry['accepted_layers'])==114 and PROFILE not in registry['profiles']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    profile=deepcopy(registry['profiles'][OLD]);old_configs=[load(profile[k])for k in KEYS]
    manifest_path=Path(release['manifest']);manifest=load(manifest_path)
    assert sha(manifest_path.read_bytes())==release['manifest_sha256'] and len(manifest['batches'])==673
    specs=[('production_pipeline','canonical_stage'),('owned_name_production_pipeline','post_bounds_stage'),
        ('owned_fields_production_pipeline','post_Emilio_stage'),('next_owned_fields_production_pipeline','post_prior_fields_stage'),
        ('grouped_owned_fields_production_pipeline','post_next_fields_stage'),('static_text_production_pipeline','post_grouped_fields_stage'),
        ('reviewed_text_data_production_pipeline','post_static_text_stage'),('Fernan_field_production_pipeline','post_reviewed_text_stage')]
    old_states=[Path(manifest[a][b])for a,b in specs]+[Path(release['candidate'])]
    assert sha(old_states[-1].read_bytes())==release['candidate_sha256']
    for i,c in enumerate(old_configs):
        assert sha(old_states[i].read_bytes())==c['parent_ROM_sha256'] and sha(old_states[i+1].read_bytes())==c['target_ROM_sha256']
    plans=[load(SEA/'production_plan_v1.json'),load(FLEET/'after_sea22_v2/production_plan_v2.json')]
    docs=list(map(load,FINALS));resources=[Path(p['research_resource']).read_bytes()for p in plans]
    scenes=[Path(load(SEA/'preview_qualification_v1/qualification.json')['research_ROM']),
        Path(load(FLEET/'after_sea22_v2/metadata_rebinding_receipt_v2.json')['research_ROM'])]
    assert len(docs[0]['records'])==22 and len(docs[1]['records'])==1
    assert docs[0]['current_ROM_sha256']==release['candidate_sha256'] and docs[1]['current_ROM_sha256']==sha(scenes[0].read_bytes())
    assert all(all(r['review'].values())for d in docs for r in d['records'])
    ROOT.mkdir();(ROOT/'release_stack_before.json').write_bytes(before)
    targets=[]
    for layer,(doc,resource,scene)in enumerate(zip(docs,resources,scenes,strict=True)):
        parents=old_states if layer==0 else targets[0]
        states=[]
        for i,parent in enumerate(parents):
            image=NdsImage.open(parent);raw=image.read_file(doc['file_path'])
            assert sha(raw)==doc['source_current_HELP_sha256']
            target=deepcopy(image);target.replace_file(doc['file_path'],resource)
            assert [p for _,p,b in image.iter_files()if target.read_file(p)!=b]==[doc['file_path']]
            assert all(target.read_file(p)==b for p,b in image.iter_components())
            if i==8:
                assert bytes(target.rom.save())==scene.read_bytes();path=scene
            else:
                path=ROOT/f'layer{layer}_stage{i}_RESEARCH_REFERENCE.nds';target.save(path)
            inverse=NdsImage.open(path);inverse.replace_file(doc['file_path'],raw);assert bytes(inverse.rom.save())==parent.read_bytes()
            states.append(path)
        targets.append(states)
    contract=deepcopy(load(old_configs[0]['parent_manifest']));contract['batches'].extend(map(str,FINALS))
    contract.update(expected_candidate_sha256=sha(targets[-1][0].read_bytes()),predecessor_manifest=str(manifest_path),
        predecessor_manifest_sha256=sha(manifest_path.read_bytes()),new_extension_configs=list(map(str,CONFIGS)))
    contract_path=ROOT/'expected_canonical_manifest_contract.json';save(contract_path,contract)
    for i,(old,path)in enumerate(zip(old_configs,STAGE_CONFIGS,strict=True)):
        value=deepcopy(old);value.update(parent_ROM_sha256=sha(targets[-1][i].read_bytes()),target_ROM_sha256=sha(targets[-1][i+1].read_bytes()))
        if i==0:
            value['parent_manifest']=str(contract_path)
            for dep in MODULES+[Path('dk4tool/dialogue/reviewed_help_pages_v7.py'),Path('dk4tool/dialogue/reviewed_help_fleet66_amendment_v1.py')]:
                value['builder_dependencies'][str(dep)]=sha(dep.read_bytes())
        allowed={'parent_ROM_sha256','target_ROM_sha256'}|({'parent_manifest','builder_dependencies'}if i==0 else set())
        assert {k:v for k,v in value.items()if k not in allowed}=={k:v for k,v in old.items()if k not in allowed}
        for n in [0,1]:
            assert NdsImage.open(targets[-1][i+n]).read_file('/__arm9__.bin')==NdsImage.open(old_states[i+n]).read_file('/__arm9__.bin')
        save(path,value)
    proof_rows=[];new_specs=[]
    for index,(doc,plan,config_path,module,final,planner)in enumerate(zip(docs,plans,CONFIGS,MODULES,FINALS,[sea_plan,fleet_plan],strict=True)):
        parent=old_states[0]if index==0 else targets[0][0]
        evidence=(dict(manuscript=final,plan=SEA/'production_plan_v1.json',native=SEA/'native_pages_v1/native_help_pages.json',
            visual=SEA/'preview_qualification_v1/direct_visual_approval.json',actual=SEA/'focused_navigation_checked_v1/ordinary_gameplay_verification.json',
            actual_visual=SEA/'focused_navigation_checked_v1/direct_actual_visual_approval.json',target_resource=Path(plan['research_resource']))if index==0 else
            dict(manuscript=final,plan=FLEET/'after_sea22_v2/production_plan_v2.json',native=Path(doc['native_proof']),visual=Path(doc['native_visual_approval']),
            actual=Path(doc['actual_proof']),actual_visual=Path(doc['actual_visual_approval']),target_resource=Path(plan['research_resource'])))
        deps=set(evidence.values())|{Path(p)for p in doc['evidence']}|set(MODULES)|{Path(__file__),
            Path('dk4tool/patch/early_help23_release_v1.py'),Path('dk4tool/patch/town_help23_release_v1.py'),
            Path('dk4tool/dialogue/help_source_links.py'),Path('scripts/source_locked_derivation_v5118.py'),
            Path('scripts/verify_help_parser_v281.py'),Path('scripts/prepare_help_pages_v281.py'),
            Path('dk4tool/dialogue/reviewed_help_fleet66_amendment_v1.py')}
        deps.update(Path('dk4tool/dialogue')/f'reviewed_help_pages_v{i}.py'for i in range(1,8))
        config=dict(format=['dk4-sea-help22-release-v1','dk4-fleet-help66-amendment-release-v1'][index],
            **{k:str(v)for k,v in evidence.items()},record_count=[22,1][index],
            canonical_ROM_sha256=sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()),clean_ROM='work/clean.nds',
            clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),parent_ROM_sha256=sha(parent.read_bytes()),
            target_ROM_sha256=sha(targets[index][0].read_bytes()),pre_runtime_ARM9_sha256=sha(NdsImage.open(parent).read_file('/__arm9__.bin')),
            final_runtime_ARM9_sha256=sha(NdsImage.open(old_states[-1]).read_file('/__arm9__.bin')),target_HELP_sha256=sha(resources[index]),
            right_bound_configuration=str(STAGE_CONFIGS[0]),dependencies={str(p):sha(p.read_bytes())for p in sorted(deps)})
        save(config_path,config)
        planned,proof=planner(NdsImage.open(parent),NdsImage.open('out/raphael_natural_v2_accepted_base.nds'),config_path)
        assert sha(bytes(planned.save()))==config['target_ROM_sha256'] and len(proof['changed_records'])==[22,1][index]
        proof_rows.append(proof)
        new_specs.append(dict(id=['sea-help22','fleet-help66-command'][index],module=['dk4tool.patch.sea_help22_release_v1','dk4tool.patch.fleet_help66_amendment_release_v1'][index],
            module_sha256=sha(module.read_bytes()),config=str(config_path),config_sha256=sha(config_path.read_bytes()),
            parent_ROM_sha256=config['parent_ROM_sha256'],target_ROM_sha256=config['target_ROM_sha256']))
    save(ROOT/'positive_prepublication_plans.json',dict(layers=proof_rows,all_eight_ARM9_transitions_identical_to_verified37=True,no_registry_mutation_yet=True))
    profile['late_editorial_extensions'].extend(new_specs);profile.update(dict(zip(KEYS,map(str,STAGE_CONFIGS))))
    profile['note']='Experimental cumulative sea Help22 and Fleet66 Command amendment:22+2 exact native/observed pages,all individual gates,all114 accepted layers/eight final stages. Supersede the old Leadership wording before any37 completion credit. Preserve all earlier work;no promotion or duplicate review credit.'
    registry['profiles'][PROFILE]=profile;prior=load(ROOT/'release_stack_before.json')
    assert all(registry[k]==v for k,v in prior.items()if k!='profiles')and all(registry['profiles'][k]==v for k,v in prior['profiles'].items())
    assert registry_path.read_bytes()==before
    temporary=registry_path.with_name('release_stack.sea22_fleet66.pending.json');assert not temporary.exists();save(temporary,registry);os.replace(temporary,registry_path)
    save(ROOT/'registered_preparation.json',dict(profile=PROFILE,previous_profile=OLD,configs=list(map(str,CONFIGS)),new_extension_specs=new_specs,
        canonical_parent=str(old_states[0]),canonical_parent_sha256=sha(old_states[0].read_bytes()),
        intermediate_canonical_parent=str(targets[0][0]),final_canonical_target=str(targets[1][0]),
        preserved_stage_configs=dict(zip(KEYS,map(str,STAGE_CONFIGS))),old_stage_states=[dict(path=str(p),sha256=sha(p.read_bytes()))for p in old_states],
        layer_stage_targets=[[dict(path=str(p),sha256=sha(p.read_bytes()))for p in states]for states in targets],
        final_ROM=str(scenes[-1]),target_ROM_sha256=sha(scenes[-1].read_bytes()),registry_sha256=sha(registry_path.read_bytes()),
        expected_manifest_entries=675,accepted_layers=114,previous_profiles_preserved=True,new_credit=0,main_unchanged=True,
        semantic_qualification_andregistered_build_pending=True))
    pins_path=Path('translations/rom_retention_pins.json');pin_before=pins_path.read_bytes();pins=load(pins_path);(ROOT/'pins.before.json').write_bytes(pin_before)
    for states in targets:
        for path in states:
            if not any(Path(p['path']).resolve()==path.resolve()for p in pins):
                pins.append(dict(path=str(path.resolve()),reason='Preserve reviewed sea22/Fleet66 cumulative research reference;all earlier ROMs retained. SHA256 '+sha(path.read_bytes())))
    temporary=pins_path.with_name('rom_retention_pins.sea22_fleet66.pending.json');assert not temporary.exists();save(temporary,pins)
    assert pins_path.read_bytes()==pin_before;os.replace(temporary,pins_path)
    print('Registered two-layer Help successor:675 entries/114 accepted layers/all eight unchanged final-stage contracts. Qualification/build next.')
