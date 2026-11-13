"""Register the checked211-record successor while preserving all sealed prior stages."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.owned_name_glyph_v1 import plan_arm9_name_glyph
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Hodram_B91_B110_release_20261101')
CONFIG=Path('translations/hodram_B91_B110_editorial_release_v1.json')
RUNTIME=Path('translations/ascii_glyph_right_bounds_hodram_B91_B110_v1.json')
EMILIO=Path('translations/emilio_name_glyph_hodram_B91_B110_release_v1.json')
NAMES=Path('translations/fernando_samwell_owned_fields_release_v1.json')
PROFILE='all-routes-hodram-b91-b110-names-20261101'
MODULE=Path('dk4tool/patch/reviewed_scene_batch_v4.py')

if __name__=='__main__':
    assert not ROOT.exists() and not any(p.exists() for p in [CONFIG,RUNTIME,EMILIO,NAMES])
    registry_path=Path('translations/release_stack.json');before=registry_path.read_bytes();registry=load(registry_path)
    assert PROFILE not in registry['profiles'];profile=deepcopy(registry['profiles']['all-routes-hodram-b81-b89-emilio-20261101'])
    old_runtime=load(profile['ascii_glyph_right_bounds']);old_name=load(profile['owned_name_glyph'])
    manifest_path=Path('out/all_routes_combined_hodram_b81_b89_emilio_20261101_candidate.manifest.json');manifest=load(manifest_path)
    canonical_path=Path(manifest['production_pipeline']['canonical_stage']);canonical=NdsImage.open(canonical_path)
    assert sha(canonical_path.read_bytes())==manifest['production_pipeline']['canonical_stage_sha256']==old_runtime['parent_ROM_sha256']
    bound_parent=NdsImage.open(manifest['owned_name_production_pipeline']['post_bounds_stage'])
    rebuilt_path=Path('work/analysis/Hodram_B91_B110_rebuilt_20261101/reconstruction.json');rebuilt=load(rebuilt_path)
    name_ref_path=Path('work/analysis/Hodram_B91_B110_name_research_20261101/research_reference.json');name_ref=load(name_ref_path)
    parent=NdsImage.open(rebuilt['parent']);story=NdsImage.open(rebuilt['research_ROM'])
    assert sha(Path(rebuilt['parent']).read_bytes())==manifest['candidate_sha256']
    assert sha(Path(rebuilt['research_ROM']).read_bytes())==rebuilt['research_ROM_sha256']
    assert parent.read_file('/__arm9__.bin')==story.read_file('/__arm9__.bin')
    inverse=deepcopy(parent);inverse.replace_file('/__arm9__.bin',canonical.read_file('/__arm9__.bin'));assert bytes(inverse.rom.save())==canonical_path.read_bytes()
    pre=deepcopy(story);pre.replace_file('/__arm9__.bin',canonical.read_file('/__arm9__.bin'))
    assert [p for _,p,v in canonical.iter_files() if pre.read_file(p)!=v]==['/data/SC1.DK4']
    assert all(pre.read_file(p)==v for p,v in canonical.iter_components())
    bounds=deepcopy(story);bounds.replace_file('/__arm9__.bin',bound_parent.read_file('/__arm9__.bin'))
    emilio_arm,proof=plan_arm9_name_glyph(bounds.read_file('/__arm9__.bin'),load(old_name['proposal']))
    assert emilio_arm==story.read_file('/__arm9__.bin')
    restored=deepcopy(bounds);restored.replace_file('/__arm9__.bin',emilio_arm);assert bytes(restored.rom.save())==Path(rebuilt['research_ROM']).read_bytes()
    ROOT.mkdir(parents=True);(ROOT/'release_stack_before.json').write_bytes(before)
    prepath=ROOT/'canonical_target_RESEARCH_ONLY.nds';prepath.write_bytes(bytes(pre.rom.save()))
    boundpath=ROOT/'post_bounds_target_RESEARCH_ONLY.nds';boundpath.write_bytes(bytes(bounds.rom.save()))
    final=Path('translations/hodram_B91_B110_contextual_final_review_v1.json');doc=load(final)
    plan=Path(rebuilt['plan']);stored=Path('work/analysis/Hodram_B91_B110_stored_20261101/stored_native_verification.json')
    loaders=Path('work/analysis/Hodram_B91_B110_loaders_20261101/verification.json')
    actual=Path('work/analysis/Hodram_B91_B110_editorial_20261101/actual_review.json')
    visual=Path('work/analysis/Hodram_B91_B110_visual_20261101/visual_review.json')
    menu=Path('work/analysis/Hodram_B91_B110_menu_20261101/menu_provider_and_planes_reviewed.json')
    pixels=Path('work/analysis/Hodram_B91_B110_actual_pixels_20261101d/focused_actual_pixels.json')
    native_name=Path('work/analysis/Hodram_B91_B110_name_native_20261101/native_name_fields_verification_reviewed.json')
    name_doc=Path('translations/fernando_samwell_owned_name_review_v1.json')
    conf=deepcopy(load('translations/hodram_B81_B89_editorial_release_v1.json'))
    conf.update(format='dk4-reviewed-scene-release-v4',manuscript=str(final),plan=str(plan),reconstruction=str(rebuilt_path),stored_native=str(stored),loaders=str(loaders),actual=str(actual),visual_review=str(visual),typed_menu=str(menu),focused_pixels=str(pixels),
        record_count=211,speech_count=209,typed_choice_count=2,blocks=doc['blocks'],native_pages=215,relative_cases=40,actual_frames=28003,actual_runs=3,actual_sheets=13,
        focused_pixel_counts=dict(menu_samples=3,name_headers=6,body_pages=6),observed_FE_ids=['DK4_MES_B91_R0084','DK4_MES_B91_R0087','DK4_MES_B91_R0103','DK4_MES_B91_R0106'],
        observed_macro_FE_ids=['DK4_MES_B91_R0084','DK4_MES_B91_R0103'],parent_ROM_sha256=sha(canonical_path.read_bytes()),target_ROM_sha256=sha(prepath.read_bytes()),pre_runtime_reference_ROM=str(prepath),pre_runtime_ARM9_sha256=sha(canonical.read_file('/__arm9__.bin')),
        final_runtime_ROM_sha256=sha(boundpath.read_bytes()),right_bound_configuration=str(RUNTIME))
    paths=[final,plan,rebuilt_path,stored,loaders,actual,visual,menu,pixels,native_name,name_doc,name_ref_path,MODULE,Path(__file__),Path(rebuilt['packet']),Path(rebuilt['native'])]
    paths += [Path('scripts')/p for p in ['finalize_hodram_B91_B110_review.py','rebuild_reviewed_editorial_batch_v3.py','rebuild_reviewed_editorial_batch_v2.py','check_editorial_stored_batch_v2.py','check_editorial_two_choice_display.py','create_reviewed_hodram_fixtures.py','plan_editorial_scene_prose_v9.py','plan_editorial_scene_prose_v8.py','plan_editorial_scene_prose_v6.py','plan_editorial_scene_prose_v5.py','plan_editorial_scene_prose.py','refresh_editorial_compiled_pages_v2.py','check_editorial_compiled_pages_v3.py','resume_editorial_native_blocks_v2.py','check_hodram_B91_B110_actual_pixels_v4.py','check_hodram_B91_B110_actual_pixels.py','check_reviewed_scene_loaders.py']]
    paths += [Path('dk4tool/patch/reviewed_scene_batch_v2.py'),Path('dk4tool/patch/reviewed_scene_batch_v3.py')]
    conf['dependencies'].update({str(p):sha(p.read_bytes()) for p in paths});save(CONFIG,conf)
    profile['late_editorial_extensions'].append(dict(id='hodram-b91-b110',module='dk4tool.patch.reviewed_scene_batch_v4',module_sha256=sha(MODULE.read_bytes()),config=str(CONFIG),config_sha256=sha(CONFIG.read_bytes()),parent_ROM_sha256=conf['parent_ROM_sha256'],target_ROM_sha256=conf['target_ROM_sha256']))
    contract=deepcopy(load(old_runtime['parent_manifest']));contract['batches'].append(str(final));contract.update(expected_candidate_sha256=conf['target_ROM_sha256'],predecessor_manifest=str(manifest_path),predecessor_manifest_sha256=sha(manifest_path.read_bytes()),new_extension_configs=[str(CONFIG)])
    contract_path=ROOT/'expected_canonical_manifest_contract.json';save(contract_path,contract)
    runtime=deepcopy(old_runtime);runtime.update(parent_ROM_sha256=conf['target_ROM_sha256'],target_ROM_sha256=sha(boundpath.read_bytes()),parent_manifest=str(contract_path));runtime['builder_dependencies'][str(MODULE)]=sha(MODULE.read_bytes());save(RUNTIME,runtime)
    emilio=deepcopy(old_name);emilio.update(parent_ROM_sha256=sha(boundpath.read_bytes()),target_ROM_sha256=rebuilt['research_ROM_sha256']);save(EMILIO,emilio)
    native=load(native_name);proposal=Path(native['proposal'])
    name_paths=[name_doc,proposal,native_name,pixels,actual,Path('dk4tool/patch/owned_name_fields_v2.py'),Path('dk4tool/patch/registered_owned_name_fields_v2.py'),Path('scripts/build_integrated_release_with_owned_fields.py'),Path('scripts/check_owned_name_fields.py'),Path('scripts/build_integrated_release_with_owned_names.py')]
    name_conf=dict(format='dk4-registered-owned-name-fields-v2',manuscript=str(name_doc),proposal=str(proposal),native=str(native_name),actual=str(pixels),clean_ROM=conf['clean_ROM'],clean_ROM_sha256=conf['clean_ROM_sha256'],parent_ROM_sha256=rebuilt['research_ROM_sha256'],target_ROM_sha256=name_ref['research_ROM_sha256'],target_ARM9_sha256=native['name_data_plan']['target_ARM9_sha256'],dependencies={str(p):sha(p.read_bytes()) for p in name_paths},
        actual_policy=[dict(actor=20,kind='changed-progressive-name',full_name='Fernando Dias',complete_header_key='normal_F_andall_name_glyphs_andblank_guards_exact',minimum_headers=6),dict(actor=22,kind='unchanged-progressive-middle-component',full_name='Samwell da Khan')])
    save(NAMES,name_conf)
    profile.update(ascii_glyph_right_bounds=str(RUNTIME),owned_name_glyph=str(EMILIO),owned_name_fields=str(NAMES),note='Cumulative experimental successor:211 five-gate reviews,129 revisions/82 retentions,215 pages,five page fixes,two additional fixed-slot name fields,three focused initialized coldboots/28003frames. Preserve all accepted andprevious experimental layers,right-bound correction andEmilio metadata stage. Use build_integrated_release_with_owned_fields.py. Main promotion requires user hardware acceptance;full scope remains;no guide photos.')
    registry['profiles'][PROFILE]=profile;assert registry_path.read_bytes()==before;save(registry_path,registry)
    save(ROOT/'registered_preparation.json',dict(profile=PROFILE,config=str(CONFIG),config_sha256=sha(CONFIG.read_bytes()),runtime_config=str(RUNTIME),runtime_config_sha256=sha(RUNTIME.read_bytes()),emilio_config=str(EMILIO),emilio_config_sha256=sha(EMILIO.read_bytes()),name_config=str(NAMES),name_config_sha256=sha(NAMES.read_bytes()),pre_runtime_ROM=str(prepath),pre_runtime_ROM_sha256=conf['target_ROM_sha256'],post_bounds_ROM=str(boundpath),post_bounds_ROM_sha256=sha(boundpath.read_bytes()),post_Emilio_ROM_sha256=rebuilt['research_ROM_sha256'],target_ROM_sha256=name_ref['research_ROM_sha256'],accepted_layers=len(registry['accepted_layers']),previous_profiles_preserved=True,all_prior_drivers_unchanged=True,new_credit=0,main_unchanged=True))
    pins=Path('translations/rom_retention_pins.json');values=load(pins)
    for p in [prepath,boundpath]:values.append(dict(path=str(p.resolve()),reason='Preserve exact B91-B110 cumulative stage reference for registered reconstruction;all ROMs retained.'))
    save(pins,values)
    print(dict(profile=PROFILE,pre_runtime=conf['target_ROM_sha256'],post_bounds=sha(boundpath.read_bytes()),post_Emilio=rebuilt['research_ROM_sha256'],final=name_ref['research_ROM_sha256'],accepted_layers=len(registry['accepted_layers'])))
