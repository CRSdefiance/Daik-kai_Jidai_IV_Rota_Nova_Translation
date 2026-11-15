"""Register the checked mixed-scene batch after every sealed predecessor stage."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Hodram_B111_B130_release_20261102')
PROFILE='all-routes-hodram-b111-b130-names-20261102'
CONFIG=Path('translations/hodram_B111_B130_editorial_release_v1.json')
RUNTIME=Path('translations/ascii_glyph_right_bounds_hodram_B111_B130_v1.json')
EMILIO=Path('translations/emilio_name_glyph_hodram_B111_B130_release_v1.json')
PRIOR=Path('translations/fernando_samwell_hodram_B111_B130_release_v1.json')
NEXT=Path('translations/follower_diogo_owned_fields_release_v1.json')
MODULE=Path('dk4tool/patch/reviewed_scene_batch_v5.py')

def main():
    assert not ROOT.exists() and not any(p.exists() for p in [CONFIG,RUNTIME,EMILIO,PRIOR,NEXT])
    registry_path=Path('translations/release_stack.json');before=registry_path.read_bytes();registry=load(registry_path)
    assert sha(before)=='b73049bf6391478aba731672b187cead93865cc59f232758d98f6b1733336e5b'
    profile=deepcopy(registry['profiles']['all-routes-hodram-b91-b110-names-20261101']);assert PROFILE not in registry['profiles']
    old_runtime,old_emilio,old_fields=[load(profile[k]) for k in ['ascii_glyph_right_bounds','owned_name_glyph','owned_name_fields']]
    manifest_path=Path('out/all_routes_combined_hodram_b91_b110_names_20261101_candidate.manifest.json');manifest=load(manifest_path)
    canonical_path=Path(manifest['production_pipeline']['canonical_stage']);canonical=NdsImage.open(canonical_path)
    bounds_parent=NdsImage.open(manifest['owned_name_production_pipeline']['post_bounds_stage'])
    emilio_parent=NdsImage.open(manifest['owned_fields_production_pipeline']['post_Emilio_stage'])
    assert sha(canonical_path.read_bytes())==old_runtime['parent_ROM_sha256']==manifest['production_pipeline']['canonical_stage_sha256']
    rebuilt_path=Path('work/analysis/Hodram_B111_B130_rebuilt_20261102b/reconstruction.json');rebuilt=load(rebuilt_path)
    reference_path=Path('work/analysis/Hodram_B111_B130_name_research_20261102/research_reference.json');reference=load(reference_path)
    parent=NdsImage.open(rebuilt['parent']);story=NdsImage.open(rebuilt['research_ROM']);final=NdsImage.open(reference['research_ROM'])
    assert sha(Path(rebuilt['parent']).read_bytes())==manifest['candidate_sha256']
    assert sha(Path(rebuilt['research_ROM']).read_bytes())==rebuilt['research_ROM_sha256']
    assert sha(Path(reference['research_ROM']).read_bytes())==reference['research_ROM_sha256']=='f2f0bf2fd904ead5d539b25d516d53fa70a0175af145be27751e8d9f6f2ccde2'
    inverse=deepcopy(parent);inverse.replace_file('/__arm9__.bin',canonical.read_file('/__arm9__.bin'));assert bytes(inverse.rom.save())==canonical_path.read_bytes()
    pre=deepcopy(story);pre.replace_file('/__arm9__.bin',canonical.read_file('/__arm9__.bin'))
    assert [p for _,p,v in canonical.iter_files() if pre.read_file(p)!=v]==['/data/SC1.DK4'] and all(pre.read_file(p)==v for p,v in canonical.iter_components())
    bound=deepcopy(story);bound.replace_file('/__arm9__.bin',bounds_parent.read_file('/__arm9__.bin'))
    emilio=deepcopy(story);emilio.replace_file('/__arm9__.bin',emilio_parent.read_file('/__arm9__.bin'))
    ROOT.mkdir(parents=True);(ROOT/'release_stack_before.json').write_bytes(before)
    prepath=ROOT/'canonical_target_RESEARCH_ONLY.nds';prepath.write_bytes(bytes(pre.rom.save()))
    boundpath=ROOT/'post_bounds_target_RESEARCH_ONLY.nds';boundpath.write_bytes(bytes(bound.rom.save()))
    emiliopath=ROOT/'post_Emilio_target_RESEARCH_ONLY.nds';emiliopath.write_bytes(bytes(emilio.rom.save()))
    doc_path=Path('translations/hodram_B111_B130_contextual_final_review_v1.json');doc=load(doc_path)
    stored=Path('work/analysis/Hodram_B111_B130_stored_20261102/stored_native_verification.json')
    loaders=Path('work/analysis/Hodram_B111_B130_loaders_20261102/verification.json')
    actual=Path('work/analysis/Hodram_B111_B130_checked_20261102b/actual_review.json')
    visual=Path('work/analysis/Hodram_B111_B130_editorial_20261101/visual_review.json')
    menu=Path('work/analysis/Hodram_B111_B130_editorial_20261101/menu_v1/menu_provider_and_planes_reviewed.json')
    styles=Path('work/analysis/Hodram_B111_B130_editorial_20261101/styles_v1/compiled_style_objects.json')
    FE=Path('work/analysis/Hodram_B111_B130_editorial_20261101/FE_final_layout_check.json')
    pixels=Path('work/analysis/Hodram_B111_B130_actual_pixels_20261102/focused_actual_pixels.json')
    names=Path('work/analysis/Hodram_B111_B130_name_native_20261101/native_name_fields_verification_reviewed.json')
    namedoc=Path('translations/follower_diogo_owned_name_review_v1.json')
    deps=[doc_path,Path(rebuilt['plan']),rebuilt_path,stored,loaders,actual,visual,menu,styles,FE,pixels,names,namedoc,reference_path,
        Path(rebuilt['packet']),Path(rebuilt['native']),MODULE,Path(__file__),Path('scripts/qualify_hodram_B111_B130_release.py')]
    deps += [Path(p) for p in ['dk4tool/script/reviewed_scene_rebuild.py','dk4tool/script/reviewed_scene_rebuild_v2.py','dk4tool/script/reviewed_scene_rebuild_v3.py',
        'dk4tool/dialogue/reviewed_choice_object_v2.py','dk4tool/dialogue/reviewed_actor_style_object_v1.py','scripts/rebuild_reviewed_editorial_batch_v4.py',
        'scripts/check_editorial_stored_batch_v3.py','scripts/finalize_hodram_B111_B130_review.py','scripts/check_hodram_B111_B130_actual_pixels.py']]
    conf=dict(format='dk4-reviewed-scene-release-v5',manuscript=str(doc_path),plan=rebuilt['plan'],reconstruction=str(rebuilt_path),stored_native=str(stored),loaders=str(loaders),
        actual=str(actual),visual_review=str(visual),typed_menu=str(menu),native_styles=str(styles),FE_layout=str(FE),focused_pixels=str(pixels),
        record_count=323,speech_count=308,ordinary_count=260,style_count=48,typed_choice_count=15,reviewed_blocks=doc['blocks'],blocks=rebuilt['changed_blocks'],
        native_pages=315,relative_cases=430,FE_count=35,menu_alignments=30,menu_returns=120,menu_planes=60,style_slots=64,
        actual_frames=51005,actual_runs=5,actual_sheets=25,focused_pixel_counts=dict(menu_samples=3,name_headers=5,body_pages=21),
        canonical_ROM_sha256=sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()),clean_ROM='work/clean.nds',
        clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),parent_ROM_sha256=sha(canonical_path.read_bytes()),target_ROM_sha256=sha(prepath.read_bytes()),
        pre_runtime_reference_ROM=str(prepath),pre_runtime_ARM9_sha256=sha(canonical.read_file('/__arm9__.bin')),
        right_bound_configuration=str(RUNTIME),dependencies={str(p):sha(p.read_bytes()) for p in deps})
    save(CONFIG,conf)
    profile['late_editorial_extensions'].append(dict(id='hodram-b111-b130',module='dk4tool.patch.reviewed_scene_batch_v5',module_sha256=sha(MODULE.read_bytes()),config=str(CONFIG),
        config_sha256=sha(CONFIG.read_bytes()),parent_ROM_sha256=conf['parent_ROM_sha256'],target_ROM_sha256=conf['target_ROM_sha256']))
    contract=deepcopy(load(old_runtime['parent_manifest']));contract['batches'].append(str(doc_path))
    contract.update(expected_candidate_sha256=conf['target_ROM_sha256'],predecessor_manifest=str(manifest_path),predecessor_manifest_sha256=sha(manifest_path.read_bytes()),new_extension_configs=[str(CONFIG)])
    contract_path=ROOT/'expected_canonical_manifest_contract.json';save(contract_path,contract)
    runtime=deepcopy(old_runtime);runtime.update(parent_ROM_sha256=conf['target_ROM_sha256'],target_ROM_sha256=sha(boundpath.read_bytes()),parent_manifest=str(contract_path))
    runtime['builder_dependencies'][str(MODULE)]=sha(MODULE.read_bytes());save(RUNTIME,runtime)
    next_emilio=deepcopy(old_emilio);next_emilio.update(parent_ROM_sha256=sha(boundpath.read_bytes()),target_ROM_sha256=sha(emiliopath.read_bytes()));save(EMILIO,next_emilio)
    prior_fields=deepcopy(old_fields);prior_fields.update(parent_ROM_sha256=sha(emiliopath.read_bytes()),target_ROM_sha256=rebuilt['research_ROM_sha256']);save(PRIOR,prior_fields)
    native=load(names);proposal=Path(native['proposal'])
    name_paths=[namedoc,proposal,names,pixels,actual,Path('dk4tool/patch/registered_owned_name_fields_v3.py'),Path('dk4tool/patch/registered_owned_name_fields_v2.py'),
        Path('dk4tool/patch/owned_name_fields_v2.py'),Path('scripts/build_integrated_release_with_next_owned_fields.py'),Path('scripts/build_integrated_release_with_owned_fields.py')]
    new_fields=dict(format='dk4-registered-owned-name-fields-v3',manuscript=str(namedoc),proposal=str(proposal),native=str(names),actual=str(pixels),
        clean_ROM=conf['clean_ROM'],clean_ROM_sha256=conf['clean_ROM_sha256'],parent_ROM_sha256=rebuilt['research_ROM_sha256'],target_ROM_sha256=reference['research_ROM_sha256'],
        target_ARM9_sha256=native['name_data_plan']['target_ARM9_sha256'],dependencies={str(p):sha(p.read_bytes()) for p in name_paths},
        actual_policy=[dict(actor=178,kind='changed-progressive-name',full_name='Follower',complete_header_key='normal_F_andall_name_glyphs_andblank_guards_exact',minimum_headers=5),
            dict(actor=43,kind='unchanged-progressive-middle-component',full_name='Diogo de Escante',unvisited_key='Diogo_full_catalogue_UI_unvisited')])
    save(NEXT,new_fields)
    profile.update(ascii_glyph_right_bounds=str(RUNTIME),owned_name_glyph=str(EMILIO),owned_name_fields=str(PRIOR),owned_name_fields_next=str(NEXT),
        note='Cumulative experimental successor:323 five-gate reviews,315 pages,239 revisions/84 retentions,mixed native styles/menus,two next name fields after preserved Fernando/Samwell. Use build_integrated_release_with_next_owned_fields.py. All114 accepted layers andold profiles preserved. Main needs explicit user acceptance;full scope andlater audit remain;no guide photos.')
    registry['profiles'][PROFILE]=profile;assert registry_path.read_bytes()==before;save(registry_path,registry)
    save(ROOT/'registered_preparation.json',dict(profile=PROFILE,config=str(CONFIG),runtime_config=str(RUNTIME),emilio_config=str(EMILIO),prior_fields_config=str(PRIOR),next_fields_config=str(NEXT),
        canonical_parent=str(canonical_path),canonical_parent_sha256=conf['parent_ROM_sha256'],pre_runtime_ROM=str(prepath),pre_runtime_ROM_sha256=conf['target_ROM_sha256'],
        post_bounds_ROM=str(boundpath),post_bounds_ROM_sha256=sha(boundpath.read_bytes()),post_Emilio_ROM=str(emiliopath),post_Emilio_ROM_sha256=sha(emiliopath.read_bytes()),
        post_prior_fields_ROM=rebuilt['research_ROM'],post_prior_fields_ROM_sha256=rebuilt['research_ROM_sha256'],final_ROM=reference['research_ROM'],target_ROM_sha256=reference['research_ROM_sha256'],
        accepted_layers=len(registry['accepted_layers']),previous_profiles_preserved=True,all_prior_drivers_unchanged=True,new_credit=0,main_unchanged=True))
    pins_path=Path('translations/rom_retention_pins.json');pins=load(pins_path)
    for p in [prepath,boundpath,emiliopath]:pins.append(dict(path=str(p.resolve()),reason='Preserve B111-B130 exact registered stage reference;no pruning.'))
    save(pins_path,pins)
    print(dict(profile=PROFILE,pre_runtime=conf['target_ROM_sha256'],post_bounds=sha(boundpath.read_bytes()),post_Emilio=sha(emiliopath.read_bytes()),post_prior_fields=rebuilt['research_ROM_sha256'],final=reference['research_ROM_sha256'],accepted_layers=114))

if __name__=='__main__':main()
