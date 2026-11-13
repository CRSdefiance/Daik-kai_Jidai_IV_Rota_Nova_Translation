"""Register reviewed Help23 while preserving all eight current final-stage contracts."""
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.early_help23_release_v1 import plan_release
from scripts.audit_story_glyph_consistency import load,save
from scripts.prepare_rafael_B61_B80_release import KEYS

ROOT=Path('work/analysis/Early_HELP23_release_20261104')
FORMAT=Path('work/analysis/Shared_HELP_early23_formatting_20261104')
RELEASE=Path('work/analysis/Rafael_B61_B80_release_verified_20261104/registered_release_verification.json')
OLD='all-routes-rafael-b61-b80-20261104'
PROFILE='all-routes-early-help23-20261104'
CONFIG=Path('translations/early_help23_editorial_release_v1.json')
MODULE=Path('dk4tool/patch/early_help23_release_v1.py')
STAGE_CONFIGS=[Path('translations')/(name+'_early_HELP23_release_v1.json') for name in
    ['ascii_bounds','emilio_name','fernando_samwell','follower_diogo','geronimo_vasquez_alonso','abkhaz_elysion','shared_tutorial_pedro_hayreddin','Fernan_name_field']]

if __name__=='__main__':
    registry_path=Path('translations/release_stack.json');before=registry_path.read_bytes()
    assert sha(before)=='e0447b467e8b6fe9f428edf2aa2c6b9f3b6b6202abe7133aaa913aab140d74fe'
    assert not ROOT.exists() and not CONFIG.exists() and not any(p.exists() for p in STAGE_CONFIGS)
    registry=load(registry_path);release=load(RELEASE)
    assert len(registry['accepted_layers'])==114 and PROFILE not in registry['profiles']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    profile=deepcopy(registry['profiles'][OLD]);old_configs=[load(profile[k]) for k in KEYS]
    manifest_path=Path(release['manifest']);manifest=load(manifest_path)
    specs=[('production_pipeline','canonical_stage'),('owned_name_production_pipeline','post_bounds_stage'),
        ('owned_fields_production_pipeline','post_Emilio_stage'),('next_owned_fields_production_pipeline','post_prior_fields_stage'),
        ('grouped_owned_fields_production_pipeline','post_next_fields_stage'),('static_text_production_pipeline','post_grouped_fields_stage'),
        ('reviewed_text_data_production_pipeline','post_static_text_stage'),('Fernan_field_production_pipeline','post_reviewed_text_stage')]
    old_states=[Path(manifest[a][b]) for a,b in specs]+[Path(release['candidate'])]
    final=Path('translations/help_early23_contextual_final_review_v1.json');doc=load(final)
    plan=load(FORMAT/'production_plan_v1.json');resource=Path(plan['research_resource']).read_bytes()
    qualification=load(FORMAT/'preview_qualification_v1/qualification.json')
    assert len(doc['records'])==23 and all(all(r['review'].values()) for r in doc['records'])
    assert sha(old_states[-1].read_bytes())==manifest['candidate_sha256']==release['candidate_sha256']==doc['current_ROM_sha256']
    for i,conf in enumerate(old_configs):
        assert sha(old_states[i].read_bytes())==conf['parent_ROM_sha256']
        assert sha(old_states[i+1].read_bytes())==conf['target_ROM_sha256']
    ROOT.mkdir();(ROOT/'release_stack_before.json').write_bytes(before);targets=[]
    for i,old in enumerate(old_states[:-1]):
        original,target=NdsImage.open(old),NdsImage.open(old)
        assert sha(original.read_file(doc['file_path']))==doc['source_current_HELP_sha256']
        target.replace_file(doc['file_path'],resource)
        assert [p for _,p,v in original.iter_files() if target.read_file(p)!=v]==[doc['file_path']]
        assert all(target.read_file(p)==v for p,v in original.iter_components())
        path=ROOT/f'stage_{i}_RESEARCH_REFERENCE.nds';target.save(path)
        inverse=NdsImage.open(path);inverse.replace_file(doc['file_path'],original.read_file(doc['file_path']))
        assert bytes(inverse.rom.save())==old.read_bytes();targets.append(path)
    scene=Path(qualification['research_ROM']);assert sha(scene.read_bytes())==qualification['research_ROM_sha256']
    expected=NdsImage.open(old_states[-1]);expected.replace_file(doc['file_path'],resource)
    assert bytes(expected.rom.save())==scene.read_bytes();targets.append(scene)
    contract=deepcopy(load(old_configs[0]['parent_manifest']));contract['batches'].append(str(final))
    contract.update(expected_candidate_sha256=sha(targets[0].read_bytes()),predecessor_manifest=str(manifest_path),
        predecessor_manifest_sha256=sha(manifest_path.read_bytes()),new_extension_configs=[str(CONFIG)])
    contract_path=ROOT/'expected_canonical_manifest_contract.json';save(contract_path,contract)
    for i,(old,path) in enumerate(zip(old_configs,STAGE_CONFIGS,strict=True)):
        value=deepcopy(old);value.update(parent_ROM_sha256=sha(targets[i].read_bytes()),target_ROM_sha256=sha(targets[i+1].read_bytes()))
        if i==0:
            value['parent_manifest']=str(contract_path)
            for dep in [MODULE,Path('dk4tool/dialogue/reviewed_help_pages_v1.py')]:value['builder_dependencies'][str(dep)]=sha(dep.read_bytes())
        allowed={'parent_ROM_sha256','target_ROM_sha256'}|({'parent_manifest','builder_dependencies'} if i==0 else set())
        assert {k:v for k,v in value.items() if k not in allowed}=={k:v for k,v in old.items() if k not in allowed}
        assert all(NdsImage.open(targets[i+n]).read_file('/__arm9__.bin')==NdsImage.open(old_states[i+n]).read_file('/__arm9__.bin') for n in [0,1])
        save(path,value)
    evidence=dict(manuscript=final,plan=FORMAT/'production_plan_v1.json',native=FORMAT/'native_pages_v2/native_help_pages.json',
        visual=FORMAT/'preview_qualification_v1/direct_visual_approval.json',actual=FORMAT/'ordinary_navigation_checked_v2/ordinary_gameplay_verification.json',
        actual_visual=FORMAT/'ordinary_navigation_checked_v2/direct_actual_visual_approval.json',target_resource=Path(plan['research_resource']))
    deps=set(evidence.values())|{Path(p) for p in doc['evidence']}|{MODULE,Path(__file__),Path('dk4tool/dialogue/reviewed_help_pages_v1.py'),
        Path('dk4tool/dialogue/help_source_links.py'),Path('scripts/verify_help_parser_v281.py'),Path('scripts/prepare_help_pages_v281.py'),
        Path('scripts/check_early_HELP23_native_pages.py'),Path('scripts/verify_early_HELP23_ordinary_navigation.py'),
        Path('scripts/verify_early_HELP23_ordinary_navigation_v2.py'),Path('scripts/plan_early_HELP23_ordinary_navigation_v2.py')}
    config=dict(format='dk4-early-help23-release-v1',**{k:str(v) for k,v in evidence.items()},record_count=23,
        canonical_ROM_sha256=sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()),clean_ROM='work/clean.nds',
        clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),parent_ROM_sha256=sha(old_states[0].read_bytes()),
        target_ROM_sha256=sha(targets[0].read_bytes()),pre_runtime_ARM9_sha256=sha(NdsImage.open(old_states[0]).read_file('/__arm9__.bin')),
        final_runtime_ARM9_sha256=sha(NdsImage.open(old_states[-1]).read_file('/__arm9__.bin')),target_HELP_sha256=sha(resource),
        right_bound_configuration=str(STAGE_CONFIGS[0]),dependencies={str(p):sha(p.read_bytes()) for p in sorted(deps)})
    save(CONFIG,config)
    planned,proof=plan_release(NdsImage.open(old_states[0]),NdsImage.open('out/raphael_natural_v2_accepted_base.nds'),CONFIG)
    assert sha(bytes(planned.save()))==config['target_ROM_sha256'] and len(proof['changed_records'])==23
    save(ROOT/'positive_prepublication_plan.json',dict(help=proof,all_eight_ARM9_transitions_identical_to_verified_predecessor=True,no_registry_mutation_yet=True))
    profile['late_editorial_extensions'].append(dict(id='early-help23',module='dk4tool.patch.early_help23_release_v1',
        module_sha256=sha(MODULE.read_bytes()),config=str(CONFIG),config_sha256=sha(CONFIG.read_bytes()),
        parent_ROM_sha256=config['parent_ROM_sha256'],target_ROM_sha256=config['target_ROM_sha256']))
    profile.update(dict(zip(KEYS,map(str,STAGE_CONFIGS))))
    profile['note']='Experimental cumulative early Help23:16 revisions/7 retentions;25 full native andordinary UI pages,original links andboth continuation/history returns checked. Preserve Rafael539/all114 accepted layers/all eight final stages. No main promotion;full scope active;no guide photos.'
    registry['profiles'][PROFILE]=profile;prior=load(ROOT/'release_stack_before.json')
    assert all(registry[k]==v for k,v in prior.items() if k!='profiles') and all(registry['profiles'][k]==v for k,v in prior['profiles'].items())
    assert registry_path.read_bytes()==before
    staged=registry_path.with_name('release_stack.early_HELP23.pending.json');assert not staged.exists();save(staged,registry);os.replace(staged,registry_path)
    save(ROOT/'registered_preparation.json',dict(profile=PROFILE,previous_profile=OLD,config=str(CONFIG),canonical_parent=str(old_states[0]),
        canonical_parent_sha256=config['parent_ROM_sha256'],preserved_stage_configs=dict(zip(KEYS,map(str,STAGE_CONFIGS))),
        old_stage_states=[dict(path=str(p),sha256=sha(p.read_bytes())) for p in old_states],stage_targets=[dict(path=str(p),sha256=sha(p.read_bytes())) for p in targets],
        final_ROM=str(scene),target_ROM_sha256=sha(scene.read_bytes()),registry_sha256=sha(registry_path.read_bytes()),
        accepted_layers=114,previous_profiles_preserved=True,new_credit=0,main_unchanged=True,semantic_qualification_andregistered_build_pending=True))
    pins_path=Path('translations/rom_retention_pins.json');pin_before=pins_path.read_bytes();pins=load(pins_path);(ROOT/'pins.before.json').write_bytes(pin_before)
    for path in targets:
        if not any(Path(p['path']).resolve()==path.resolve() for p in pins):
            pins.append(dict(path=str(path.resolve()),reason='Preserve reviewed Help23 research/stage reference;all prior ROMs retained. SHA256 '+sha(path.read_bytes())))
    temporary=pins_path.with_name('rom_retention_pins.early_HELP23.pending.json');assert not temporary.exists();save(temporary,pins)
    assert pins_path.read_bytes()==pin_before;os.replace(temporary,pins_path)
    print('Registered Help23 experimental successor;114 accepted layers/all eight stage contracts preserved. Qualification/build next.',flush=True)
