"""Register the completed scene batch and a separate final owned-name stage."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Hodram_B81_B89_release_20261101')
CONFIG=Path('translations/hodram_B81_B89_editorial_release_v1.json')
RUNTIME=Path('translations/ascii_glyph_right_bounds_hodram_B81_B89_v1.json')
NAME_CONFIG=Path('translations/emilio_name_glyph_release_v1.json')
PROFILE='all-routes-hodram-b81-b89-emilio-20261101'
MODULE=Path('dk4tool/patch/reviewed_scene_batch_v3.py')

if __name__=='__main__':
    assert not ROOT.exists() and not any(p.exists() for p in [CONFIG,RUNTIME,NAME_CONFIG])
    ROOT.mkdir(parents=True);registry_path=Path('translations/release_stack.json');before=registry_path.read_bytes();registry=load(registry_path)
    (ROOT/'release_stack_before.json').write_bytes(before);assert PROFILE not in registry['profiles']
    profile=deepcopy(registry['profiles']['all-routes-hodram-b71-b80-20261101'])
    old_runtime=load(profile['ascii_glyph_right_bounds'])
    rebuilt_path=Path('work/analysis/Hodram_B81_B89_rebuild_20261101/reconstruction.json');rebuilt=load(rebuilt_path)
    name_ref_path=Path('work/analysis/Hodram_B81_B89_name_research_20261101/research_reference.json');name_ref=load(name_ref_path)
    previous_manifest=Path('out/all_routes_combined_hodram_b71_b80_20261101_candidate.manifest.json');manifest=load(previous_manifest)
    canonical_path=Path(manifest['production_pipeline']['canonical_stage']);canonical=NdsImage.open(canonical_path)
    assert sha(canonical_path.read_bytes())==manifest['production_pipeline']['canonical_stage_sha256']==old_runtime['parent_ROM_sha256']
    parent=NdsImage.open(rebuilt['parent']);target=NdsImage.open(rebuilt['research_ROM'])
    assert sha(Path(rebuilt['parent']).read_bytes())==manifest['candidate_sha256']==old_runtime['target_ROM_sha256']
    assert sha(Path(rebuilt['research_ROM']).read_bytes())==rebuilt['research_ROM_sha256']
    inverse=deepcopy(parent);inverse.replace_file('/__arm9__.bin',canonical.read_file('/__arm9__.bin'))
    assert bytes(inverse.rom.save())==canonical_path.read_bytes()
    pre=deepcopy(target);pre.replace_file('/__arm9__.bin',canonical.read_file('/__arm9__.bin'))
    assert parent.read_file('/__arm9__.bin')==target.read_file('/__arm9__.bin')
    prepath=ROOT/'canonical_target_RESEARCH_ONLY.nds';prepath.write_bytes(bytes(pre.rom.save()))
    assert [p for _,p,v in canonical.iter_files() if pre.read_file(p)!=v]==['/data/SC1.DK4']
    assert all(pre.read_file(p)==v for p,v in canonical.iter_components())
    final=Path('translations/hodram_B81_B89_contextual_final_review_v1.json');plan=Path(rebuilt['plan'])
    stored=Path('work/analysis/Hodram_B81_B89_stored_20261101/stored_native_verification.json')
    loaders=Path('work/analysis/Hodram_B81_B89_loaders_20261101/verification.json')
    actual=Path('work/analysis/Hodram_B81_B89_editorial_20261101/actual_review.json')
    visual=Path('work/analysis/Hodram_B81_B89_editorial_20261101/visual_review.json')
    menu=Path('work/analysis/Hodram_B87_menu_20261101/menu_provider_and_planes_reviewed.json')
    pixels=Path('work/analysis/Hodram_B81_B89_actual_pixels_20261101d/focused_actual_pixels.json')
    name=Path('work/analysis/Emilio_name_glyph_native_20261101/native_name_glyph_verification_reviewed.json')
    name_doc=Path('translations/emilio_name_glyph_review_v1.json')
    conf=deepcopy(load('translations/hodram_B71_B80_editorial_release_v1.json'))
    conf.update(format='dk4-reviewed-scene-release-v3',manuscript=str(final),plan=str(plan),reconstruction=str(rebuilt_path),
        stored_native=str(stored),loaders=str(loaders),actual=str(actual),visual_review=str(visual),typed_menu=str(menu),focused_pixels=str(pixels),
        record_count=306,speech_count=304,typed_choice_count=2,blocks=list(range(81,90)),native_pages=306,relative_cases=140,
        actual_frames=41004,actual_runs=4,actual_sheets=20,parent_ROM_sha256=sha(canonical_path.read_bytes()),
        target_ROM_sha256=sha(prepath.read_bytes()),pre_runtime_reference_ROM=str(prepath),
        pre_runtime_ARM9_sha256=sha(canonical.read_file('/__arm9__.bin')),final_runtime_ROM_sha256=rebuilt['research_ROM_sha256'],right_bound_configuration=str(RUNTIME))
    paths=[final,plan,rebuilt_path,stored,loaders,actual,visual,menu,pixels,name,name_doc,name_ref_path,MODULE,Path(__file__),
        Path('translations/hodram_B81_B89_editorial_manuscript_v2.json'),Path(rebuilt['packet']),Path(rebuilt['native']),
        Path('dk4tool/script/reviewed_scene_rebuild_v2.py'),Path('dk4tool/dialogue/reviewed_two_choice_object_v1.py'),
        Path('scripts/rebuild_reviewed_editorial_batch_v2.py'),Path('scripts/check_editorial_stored_batch_v2.py'),
        Path('scripts/check_editorial_two_choice_display.py'),Path('scripts/create_hodram_B81_B89_fixtures.py'),
        Path('scripts/finalize_hodram_B81_B89_format_review.py'),Path('scripts/check_hodram_B81_B89_loaders.py'),
        Path('scripts/plan_editorial_scene_prose_v5.py'),Path('scripts/plan_editorial_scene_prose.py'),
        Path('scripts/refresh_editorial_compiled_pages_v2.py'),Path('scripts/check_editorial_compiled_pages_v2.py'),
        Path('scripts/check_hodram_focused_actual_pixels_v4.py'),Path('scripts/check_hodram_focused_actual_pixels.py'),
        Path('scripts/make_editorial_capture_sheets_v2.py'),Path('scripts/source_locked_derivation_v5118.py')]
    conf['dependencies'].update({str(p):sha(p.read_bytes()) for p in paths});save(CONFIG,conf)
    profile['late_editorial_extensions'].append(dict(id='hodram-b81-b89',module='dk4tool.patch.reviewed_scene_batch_v3',
        module_sha256=sha(MODULE.read_bytes()),config=str(CONFIG),config_sha256=sha(CONFIG.read_bytes()),
        parent_ROM_sha256=conf['parent_ROM_sha256'],target_ROM_sha256=conf['target_ROM_sha256']))
    contract=deepcopy(load(old_runtime['parent_manifest']));contract['batches'].append(str(final))
    contract.update(expected_candidate_sha256=conf['target_ROM_sha256'],predecessor_manifest=str(previous_manifest),
        predecessor_manifest_sha256=sha(previous_manifest.read_bytes()),new_extension_configs=[str(CONFIG)])
    contract_path=ROOT/'expected_canonical_manifest_contract.json';save(contract_path,contract)
    runtime=deepcopy(old_runtime);runtime.update(parent_ROM_sha256=conf['target_ROM_sha256'],target_ROM_sha256=rebuilt['research_ROM_sha256'],parent_manifest=str(contract_path))
    runtime['builder_dependencies'][str(MODULE)]=sha(MODULE.read_bytes());save(RUNTIME,runtime)
    name_native=load(name);proposal=Path(name_native['proposal'])
    name_paths=[name_doc,proposal,name,pixels,actual,Path('dk4tool/patch/owned_name_glyph_v1.py'),
        Path('dk4tool/patch/registered_owned_name_glyph_v1.py'),Path('scripts/build_integrated_release_with_owned_names.py'),
        Path('scripts/build_integrated_release_with_runtime_bounds.py'),Path('scripts/check_emilio_name_glyph.py')]
    name_conf=dict(format='dk4-registered-owned-name-glyph-v1',manuscript=str(name_doc),proposal=str(proposal),native=str(name),actual=str(pixels),
        parent_ROM_sha256=rebuilt['research_ROM_sha256'],target_ROM_sha256=name_ref['research_ROM_sha256'],
        target_ARM9_sha256=name_native['name_data_plan']['target_ARM9_sha256'],dependencies={str(p):sha(p.read_bytes()) for p in name_paths})
    save(NAME_CONFIG,name_conf)
    profile.update(ascii_glyph_right_bounds=str(RUNTIME),owned_name_glyph=str(NAME_CONFIG),
        note='Cumulative experimental successor:306 five-gate contextual reviews,216 wording/name revisions,6 punctuation glyph revisions,84 retentions;Emilio name-metadata F corrected separately.306 stored speech pages,140 native relative cases,325 loads,four initialized QA runs/41004frames pass. Preserve all prior accepted/experimental layers andthe registered right-bound repair. Use build_integrated_release_with_owned_names.py. Main promotion requires user acceptance;full editorial goal remains active;no guide photos.')
    registry['profiles'][PROFILE]=profile;assert registry_path.read_bytes()==before;save(registry_path,registry)
    save(ROOT/'registered_preparation.json',dict(profile=PROFILE,config=str(CONFIG),config_sha256=sha(CONFIG.read_bytes()),
        runtime_config=str(RUNTIME),runtime_config_sha256=sha(RUNTIME.read_bytes()),name_config=str(NAME_CONFIG),name_config_sha256=sha(NAME_CONFIG.read_bytes()),
        pre_runtime_ROM=str(prepath),pre_runtime_ROM_sha256=conf['target_ROM_sha256'],post_bounds_ROM_sha256=rebuilt['research_ROM_sha256'],
        target_ROM_sha256=name_ref['research_ROM_sha256'],accepted_layers=len(registry['accepted_layers']),previous_profiles_preserved=True,
        canonical_andruntime_bounds_builders_unchanged=True,new_credit=0,main_unchanged=True))
    pins=Path('translations/rom_retention_pins.json');values=load(pins);values.append(dict(path=str(prepath.resolve()),reason='Preserve exact B81-B89 pre-runtime cumulative reconstruction target;all ROMs retained.'));save(pins,values)
    print(dict(profile=PROFILE,pre_runtime=conf['target_ROM_sha256'],post_bounds=rebuilt['research_ROM_sha256'],final=name_ref['research_ROM_sha256'],accepted_layers=len(registry['accepted_layers'])))
