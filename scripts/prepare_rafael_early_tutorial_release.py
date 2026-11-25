"""Register one cumulative SC0 successor while preserving all six final stages."""
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.rafael_early_tutorial_release_v1 import plan_release

ROOT=Path('work/analysis/Rafael_early_tutorial_B42_B43_release_20261104')
PROFILE='all-routes-rafael-early-tutorial-static-text-20261104'
OLD='all-routes-hodram-b191-b210-static-text-20261104'
CONFIG=Path('translations/rafael_B42_B43_editorial_release_v1.json')
MODULE=Path('dk4tool/patch/rafael_early_tutorial_release_v1.py')
CHECKED=Path('work/analysis/Rafael_early_tutorial_B42_B43_checked_20261104')
FINAL=Path('translations/rafael_B42_B43_contextual_final_review_v1.json')
REBUILT=Path('work/analysis/Rafael_early_tutorial_B42_B43_storage_20261104/reconstruction_v2/reconstruction.json')
FORMAT=Path('work/analysis/Rafael_early_tutorial_B42_B43_formatting_20261104/speech_display_approved_v2')

if __name__=='__main__':
    assert not ROOT.exists() and not CONFIG.exists()
    registry_path=Path('translations/release_stack.json')
    before=registry_path.read_bytes()
    assert sha(before)=='fcc6e85f43b101ad459de1ff035be49640c04925c4a728bc9febfd37b5b69f96'
    registry=load(registry_path)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114
    profile=deepcopy(registry['profiles'][OLD])
    keys=['ascii_glyph_right_bounds','owned_name_glyph','owned_name_fields','owned_name_fields_next','owned_name_fields_grouped','owned_static_text']
    old_configs=[load(profile[k]) for k in keys]
    manifest_path=Path('out/all_routes_combined_hodram_b191_b210_static_text_20261104_candidate.manifest.json')
    manifest=load(manifest_path)
    specs=[('production_pipeline','canonical_stage'),('owned_name_production_pipeline','post_bounds_stage'),
        ('owned_fields_production_pipeline','post_Emilio_stage'),('next_owned_fields_production_pipeline','post_prior_fields_stage'),
        ('grouped_owned_fields_production_pipeline','post_next_fields_stage'),('static_text_production_pipeline','post_grouped_fields_stage')]
    stages=[Path(manifest[a][b]) for a,b in specs]
    rebuilt,doc,native=map(load,[REBUILT,FINAL,FORMAT/'all40_native_pages.json'])
    assert all(all(r['review'].values()) for r in doc['records']) and len(doc['records'])==40
    parent=Path(rebuilt['parent'])
    assert sha(parent.read_bytes())==manifest['candidate_sha256']=='88e9984f767a0fa14bde5e9ce07392d1fbcf44fb41a6815e4ca466740fb82a15'
    old_states=stages+[parent]
    for i,conf in enumerate(old_configs):
        assert sha(old_states[i].read_bytes())==conf['parent_ROM_sha256']
        assert sha(old_states[i+1].read_bytes())==conf['target_ROM_sha256']
    archive=Path(rebuilt['target_archive']).read_bytes()
    assert sha(archive)==rebuilt['target_archive_sha256']
    ROOT.mkdir()
    (ROOT/'release_stack_before.json').write_bytes(before)
    targets=[]
    for index,old in enumerate(stages):
        original,target=NdsImage.open(old),NdsImage.open(old)
        target.replace_file(doc['file_path'],archive)
        assert [p for _,p,v in original.iter_files() if target.read_file(p)!=v]==[doc['file_path']]
        assert all(target.read_file(p)==v for p,v in original.iter_components())
        path=ROOT/f'stage_{index}_RESEARCH_REFERENCE.nds'
        target.save(path)
        restored=NdsImage.open(path)
        restored.replace_file(doc['file_path'],original.read_file(doc['file_path']))
        assert bytes(restored.rom.save())==old.read_bytes()
        targets.append(path)
    final=Path(rebuilt['research_ROM'])
    assert sha(final.read_bytes())==rebuilt['research_ROM_sha256']
    expected=NdsImage.open(parent)
    expected.replace_file(doc['file_path'],archive)
    assert bytes(expected.rom.save())==final.read_bytes()
    targets.append(final)
    FE_path=ROOT/'FE_final_layout_check.json'
    FE=[r for r in native['records'] if r['kind']=='system-FE']
    assert len(FE)==1 and FE[0]['complete_native_English_display']['planned_native_row_comparison']['complete_glyph_row_membership_exact']
    save(FE_path,dict(FE_records=1,findings=[],unexpected_blank_rows_orwraps_absent=True,strict_native_rows=True,
        native=str(FORMAT/'all40_native_pages.json'),native_sha256=sha((FORMAT/'all40_native_pages.json').read_bytes()),no_new_rendering_run=True))
    evidence=dict(manuscript=FINAL,plan=CHECKED/'release_plans.json',reconstruction=REBUILT,
        stored_native=Path('work/analysis/Rafael_early_tutorial_B42_B43_storage_20261104/stored_native_v1/stored_native_verification.json'),
        loaders=Path('work/analysis/Rafael_early_tutorial_B42_B43_loaders_20261104/verification.json'),actual=CHECKED/'actual_visual_approval.json',
        compiled_native=FORMAT/'all40_native_pages.json',visual_review=FORMAT/'visual_approval.json',
        scoped_names=Path('translations/rafael_B42_B43_scoped_names_final_v1.json'),name_visual=CHECKED/'scoped_name_visual_approval.json',
        focused_pixels=Path('work/analysis/Rafael_early_tutorial_B42_B43_actual_pixels_20261104/focused_actual_pixels.json'),FE_layout=FE_path)
    dependencies=[*evidence.values(),CHECKED/'current_rebuilder_exact_replay.json',CHECKED/'formatting_checkpoint.json',
        Path(rebuilt['packet']),Path(rebuilt['native']),MODULE,Path('dk4tool/patch/reviewed_scene_batch_v1.py'),
        Path('dk4tool/script/rafael_early_tutorial_rebuild_v1.py'),Path('dk4tool/script/reviewed_scene_rebuild.py'),
        Path('scripts/source_locked_derivation_v5118.py'),Path('scripts/finalize_rafael_early_tutorial_review.py'),
        Path('scripts/check_rafael_early_tutorial_stored.py'),Path('scripts/analyze_rafael_early_tutorial_actual.py'),
        Path('scripts/check_rafael_early_tutorial_loaders.py'),Path(__file__)]
    runtime_path=Path('translations/ascii_glyph_right_bounds_rafael_B42_B43_v1.json')
    conf=dict(format='dk4-rafael-early-tutorial-release-v1',**{k:str(v) for k,v in evidence.items()},
        record_count=40,blocks=[42,43],native_pages=42,relative_cases=0,FE_count=1,
        canonical_ROM_sha256=sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()),
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        parent_ROM_sha256=sha(stages[0].read_bytes()),target_ROM_sha256=sha(targets[0].read_bytes()),
        pre_runtime_reference_ROM=str(targets[0]),pre_runtime_ARM9_sha256=sha(NdsImage.open(stages[0]).read_file('/__arm9__.bin')),
        right_bound_configuration=str(runtime_path),dependencies={str(p):sha(p.read_bytes()) for p in dependencies})
    save(CONFIG,conf)
    # Test the direct pure plan before publishing a registry entry.
    planned,proof=plan_release(NdsImage.open(stages[0]),NdsImage.open('out/raphael_natural_v2_accepted_base.nds'),CONFIG)
    assert sha(bytes(planned.save()))==conf['target_ROM_sha256'] and len(proof['changed_records'])==40
    profile['late_editorial_extensions'].append(dict(id='rafael-early-tutorial',module='dk4tool.patch.rafael_early_tutorial_release_v1',
        module_sha256=sha(MODULE.read_bytes()),config=str(CONFIG),config_sha256=sha(CONFIG.read_bytes()),
        parent_ROM_sha256=conf['parent_ROM_sha256'],target_ROM_sha256=conf['target_ROM_sha256']))
    contract=deepcopy(load(old_configs[0]['parent_manifest']))
    contract['batches'].append(str(FINAL))
    contract.update(expected_candidate_sha256=conf['target_ROM_sha256'],predecessor_manifest=str(manifest_path),
        predecessor_manifest_sha256=sha(manifest_path.read_bytes()),new_extension_configs=[str(CONFIG)])
    contract_path=ROOT/'expected_canonical_manifest_contract.json'
    save(contract_path,contract)
    paths=[runtime_path,Path('translations/emilio_name_glyph_rafael_B42_B43_release_v1.json'),
        Path('translations/fernando_samwell_rafael_B42_B43_release_v1.json'),Path('translations/follower_diogo_rafael_B42_B43_release_v1.json'),
        Path('translations/geronimo_vasquez_alonso_rafael_B42_B43_release_v1.json'),Path('translations/abkhaz_elysion_rafael_B42_B43_release_v1.json')]
    assert not any(p.exists() for p in paths)
    for i,(old,path) in enumerate(zip(old_configs,paths,strict=True)):
        value=deepcopy(old)
        value.update(parent_ROM_sha256=sha(targets[i].read_bytes()),target_ROM_sha256=sha(targets[i+1].read_bytes()))
        if i==0:
            value['parent_manifest']=str(contract_path)
            value['builder_dependencies'][str(MODULE)]=sha(MODULE.read_bytes())
            value['builder_dependencies']['dk4tool/script/rafael_early_tutorial_rebuild_v1.py']=sha(Path('dk4tool/script/rafael_early_tutorial_rebuild_v1.py').read_bytes())
        save(path,value)
    profile.update(dict(zip(keys,map(str,paths))))
    profile['note']='Experimental cumulative Rafael early-tutorial successor:40 reviews,19 revisions/21 retentions,42 pages/two page fixes. Preserve114 accepted layers/all prior profiles/six final stages. Static-text build pipeline required;main acceptance required. Full scope active;no guide photos.'
    registry['profiles'][PROFILE]=profile
    prior=load(ROOT/'release_stack_before.json')
    assert all(registry[k]==v for k,v in prior.items() if k!='profiles')
    assert all(registry['profiles'][k]==v for k,v in prior['profiles'].items())
    assert registry_path.read_bytes()==before
    staged=registry_path.with_name('release_stack.pending_Rafael_B42_B43.json')
    assert not staged.exists()
    save(staged,registry)
    os.replace(staged,registry_path)
    save(ROOT/'registered_preparation.json',dict(profile=PROFILE,config=str(CONFIG),preserved_stage_configs=dict(zip(keys,map(str,paths))),
        canonical_parent=str(stages[0]),canonical_parent_sha256=conf['parent_ROM_sha256'],stage_targets=[dict(path=str(p),sha256=sha(p.read_bytes())) for p in targets],
        pre_runtime_ROM=str(targets[0]),pre_runtime_ROM_sha256=conf['target_ROM_sha256'],post_grouped_ROM=str(targets[5]),
        static_config=str(paths[5]),final_ROM=str(final),target_ROM_sha256=sha(final.read_bytes()),registry_sha256=sha(registry_path.read_bytes()),
        accepted_layers=114,previous_profiles_preserved=True,all_prior_drivers_anddata_qualification_dependencies_unchanged=True,
        positive_direct_plan=proof,new_credit=0,main_unchanged=True))
    pins_path=Path('translations/rom_retention_pins.json')
    pins_before=pins_path.read_bytes()
    pins=load(pins_path)
    (ROOT/'pins.before.json').write_bytes(pins_before)
    pins += [dict(path=str(p.resolve()),reason='Preserve exact registered Rafael tutorial stage reference;no pruning.') for p in targets[:-1]]
    staged=pins_path.with_name('rom_retention_pins.Rafael_B42_B43_release.pending.json')
    assert not staged.exists()
    save(staged,pins)
    assert pins_path.read_bytes()==pins_before
    os.replace(staged,pins_path)
    print('Registered 40-review Rafael tutorial profile;114 accepted layers and six final stages preserved;qualification/build next.')
