"""Verify all accepted layers/eight stages,exact249 references andclean-input reconstruction."""
import argparse
import sys
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.registered_Fernan_name_field_v1 import plan_release as field_plan
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.verify_release_baseline import main as verify_baseline

KEYS=['ascii_glyph_right_bounds','owned_name_glyph','owned_name_fields','owned_name_fields_next',
      'owned_name_fields_grouped','owned_static_text','owned_reviewed_text_data','owned_Fernan_name_field']
PIPELINES=[('production_pipeline','canonical_stage'),('owned_name_production_pipeline','post_bounds_stage'),
    ('owned_fields_production_pipeline','post_Emilio_stage'),('next_owned_fields_production_pipeline','post_prior_fields_stage'),
    ('grouped_owned_fields_production_pipeline','post_next_fields_stage'),('static_text_production_pipeline','post_grouped_fields_stage'),
    ('reviewed_text_data_production_pipeline','post_static_text_stage'),('Fernan_field_production_pipeline','post_reviewed_text_stage')]
PARENT_PROOF=Path('work/analysis/Shared_tutorial_name_data_release_verified_20261104/registered_release_verification.json')
QUALIFICATION=Path('work/analysis/Rafael_B51_B60_release_qualification_v2_20261104/qualification.json')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ['candidate','preparation','out']:parser.add_argument('--'+key,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    prepared,parent_proof,qualification=map(load,[args.preparation,PARENT_PROOF,QUALIFICATION])
    registry_path=Path('translations/release_stack.json');registry=load(registry_path);profile=registry['profiles'][prepared['profile']]
    manifest_path=args.candidate.with_suffix('.manifest.json');manifest=load(manifest_path)
    parent_path=Path(parent_proof['candidate']);parent_manifest=load(parent_path.with_suffix('.manifest.json'))
    assert sha(registry_path.read_bytes())==manifest['release_stack_sha256']==prepared['registry_sha256']
    assert manifest['profile']==prepared['profile'] and all(manifest['checks'].values())
    assert manifest['checks']['registered_Fernan_name_field_and_complete_parent_target_inverse']
    assert all(manifest['checks'][k]==v for k,v in parent_manifest['checks'].items())
    config_paths=[Path(profile[k]) for k in KEYS];configs=list(map(load,config_paths))
    assert config_paths[-1]==Path(prepared['field_config'])
    old_profile=registry['profiles'][parent_proof['profile']]
    old_stage_paths=[str(Path(old_profile[k])) for k in KEYS[:-1]]
    assert parent_manifest['batches'][-7:]==old_stage_paths
    scene_conf=load(prepared['config']);final_path=Path(scene_conf['manuscript']);final=load(final_path)
    expected_batches=[*parent_manifest['batches'][:-7],str(final_path),*map(str,config_paths)]
    assert manifest['batches']==expected_batches and len(expected_batches)==669
    assert manifest['required_batches']==parent_manifest['required_batches']
    spec=profile['late_editorial_extensions'][-1]
    assert spec['config']==prepared['config'] and sha(Path(spec['config']).read_bytes())==spec['config_sha256']
    module_path=Path(*spec['module'].split('.')).with_suffix('.py')
    assert sha(module_path.read_bytes())==spec['module_sha256']
    assert len(qualification['semantic_rejections'])==12 and qualification['direct_andshared_scene_targets_equal']
    for conf in [scene_conf,*configs]:
        for path,digest in conf.get('dependencies',{}).items():assert sha(Path(path).read_bytes())==digest,path
    original_preparation=Path(prepared['prior_preparation'])
    old_registry=load(original_preparation.parent/'release_stack_before.json')
    assert registry['accepted_layers']==old_registry['accepted_layers'] and len(registry['accepted_layers'])==114
    assert all(registry['profiles'][k]==v for k,v in old_registry['profiles'].items())
    present={str(Path(p).resolve()).casefold() for p in manifest['batches']}
    assert all(r.get('baked_into_baseline') is True or str(Path(r['batch']).resolve()).casefold() in present for r in registry['accepted_layers'])
    baseline=Path(registry['canonical_baseline']['path'])
    assert manifest['base_sha256']==registry['canonical_baseline']['sha256']==sha(baseline.read_bytes())
    assert sha(parent_path.read_bytes())==parent_manifest['candidate_sha256']==parent_proof['candidate_sha256']
    assert sha(args.candidate.read_bytes())==manifest['candidate_sha256']==prepared['target_ROM_sha256']
    assert args.candidate.read_bytes()==Path(prepared['final_ROM']).read_bytes()
    # Every original driver must have produced its exact ordered parent/target.
    stage_paths=[Path(manifest[a][b]) for a,b in PIPELINES]+[args.candidate]
    assert sha(stage_paths[0].read_bytes())==scene_conf['target_ROM_sha256']
    for i,(config_path,conf) in enumerate(zip(config_paths,configs,strict=True)):
        assert sha(stage_paths[i].read_bytes())==conf['parent_ROM_sha256']
        assert sha(stage_paths[i+1].read_bytes())==conf['target_ROM_sha256']
        stage_manifest=load(stage_paths[i+1].with_suffix('.manifest.json'))
        assert stage_manifest['candidate_sha256']==conf['target_ROM_sha256']
        assert stage_manifest['release_stack_sha256']==prepared['registry_sha256'] and all(stage_manifest['checks'].values())
        assert str(config_path) in stage_manifest['batches']
    pipeline=manifest['Fernan_field_production_pipeline']
    assert pipeline['all_prior_drivers_unchanged'] and pipeline['only_final_exclusive_Fernan_name_field_changed']
    parent,candidate,scene=NdsImage.open(parent_path),NdsImage.open(args.candidate),NdsImage.open(stage_paths[-2])
    arm,field_proof=field_plan(scene,config_paths[-1])
    assert field_proof==qualification['positive_field_plan'] and candidate.read_file('/__arm9__.bin')==arm
    stored=manifest['relocations']['/__arm9__.bin']['owned_Fernan_name_field']
    assert stored['proof']==field_proof and stored['release_config_sha256']==sha(config_paths[-1].read_bytes())
    assert [p for _,p,v in parent.iter_files() if candidate.read_file(p)!=v]==['/data/SC0.DK4']
    assert [p for p,v in parent.iter_components() if candidate.read_file(p)!=v]==['/__arm9__.bin']
    # The only ARM9 difference from the verified predecessor is the tested field.
    inverse_arm=bytearray(arm)
    for f in field_proof['fields']:
        at,n=f['physical_offset'],f['owned_bytes'];assert inverse_arm[at:at+n].hex()==f['new_hex']
        inverse_arm[at:at+n]=bytes.fromhex(f['old_hex'])
    assert bytes(inverse_arm)==parent.read_file('/__arm9__.bin')
    rebuild=load(scene_conf['reconstruction']);old_archive=parent.read_file('/data/SC0.DK4');archive=candidate.read_file('/data/SC0.DK4')
    assert sha(old_archive)==rebuild['source_archive_sha256'] and sha(archive)==rebuild['target_archive_sha256']
    before,after=[IlnkContainer.parse(a).blocks for a in [old_archive,archive]]
    assert len(before)==len(after)==343 and [i for i,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b]==list(range(51,61))
    assert len(final['records'])==249 and (final['proposed_revisions'],final['wording_retentions'])==(102,147)
    bindings=[]
    for row in final['records']:
        assert all(row['review'].values())
        ref=row['planned_integrated_reference'];raw=bytes.fromhex(ref['exact_stored_hex']);block=after[row['block']];at=ref['offset']
        assert block[at:at+len(raw)+1]==raw+b'\0' and ref['target_archive_sha256']==sha(archive)
        if row['kind']!='typed-choice-label':
            assert block[ref['header_offset']:at+1].hex()==row['source_complete_preamble_hex']
        bindings.append(dict(id=row['id'],file_path='/data/SC0.DK4',block=row['block'],reference=ref,decision=row['decision']))
    for group in rebuild['groups']:assert sha(after[group['block']])==group['target_sha256']
    restored=deepcopy(candidate);restored.replace_file('/__arm9__.bin',bytes(inverse_arm));restored.replace_file('/data/SC0.DK4',old_archive)
    assert bytes(restored.rom.save())==parent_path.read_bytes()
    old_argv=sys.argv
    try:
        sys.argv=['verify_release_baseline',str(baseline),str(args.candidate)]
        for path in manifest['changed_paths']:sys.argv+=['--allow-path',path]
        verify_baseline()
    finally:sys.argv=old_argv
    clean=Path(configs[-1]['clean_ROM']);assert sha(clean.read_bytes())==configs[-1]['clean_ROM_sha256']
    patch=args.candidate.with_suffix('.xdelta');assert not patch.exists()
    args.out.mkdir(parents=True);reconstructed=args.out/'clean_input_reconstruction_RESEARCH_ONLY.nds'
    make_xdelta(clean,args.candidate,patch);apply_xdelta(clean,patch,reconstructed)
    assert reconstructed.read_bytes()==args.candidate.read_bytes()
    save(args.out/'exact_integrated_record_bindings.json',dict(candidate=str(args.candidate),candidate_sha256=manifest['candidate_sha256'],
        records=bindings,all249_final_bytes_controls_source_current_andindividual_gates_bound=True,new_credit=0))
    save(args.out/'registered_release_verification.json',dict(candidate=str(args.candidate),candidate_sha256=manifest['candidate_sha256'],
        manifest=str(manifest_path),manifest_sha256=sha(manifest_path.read_bytes()),profile=manifest['profile'],
        registry_sha256=manifest['release_stack_sha256'],canonical_base=str(baseline),canonical_sha256=manifest['base_sha256'],
        parent=str(parent_path),parent_sha256=parent_proof['candidate_sha256'],changed_internal_files=['/data/SC0.DK4'],changed_components=['/__arm9__.bin'],
        Fernan_name_field_proof=field_proof,all_unowned_files_components_graphics_names_fonts_andruntime_code_exact_to_parent=True,
        only_reviewed_SC0_ten_blocks_andone_owned_name_field_changed=True,all_eight_registered_final_stages_preserved=True,
        complete_stack_entries=669,accepted_layers=114,passing_release_checks=len(manifest['checks']),
        new_contextual_records=249,dialogue_revisions=102,justified_retentions=147,wrap_fixes=38,ASCII_I_corrections=3,separate_name_field_corrections=1,
        actual_research_utterances=32,offline_only_utterances=213,actual_choice_captions=4,full_catalogue_UI_unvisited=True,
        all249_exact_integrated_references_bound=True,byte_exact_to_checked_research_image=True,
        patch=str(patch),patch_sha256=sha(patch.read_bytes()),clean_input_sha256=sha(clean.read_bytes()),
        exact_clean_reconstruction=str(reconstructed),reconstructed_sha256=sha(reconstructed.read_bytes()),clean_input_patch_byte_exact=True,
        own_registered_startup_pending=True,experimental_not_promoted=True,full_goal_complete=False,
        preparation=str(args.preparation),preparation_sha256=sha(args.preparation.read_bytes()),qualification=str(QUALIFICATION),qualification_sha256=sha(QUALIFICATION.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes())))
    pins_path=Path('translations/rom_retention_pins.json');pins_before=pins_path.read_bytes();pins=load(pins_path)
    (args.out/'pins.before.json').write_bytes(pins_before)
    for rom in [args.candidate,reconstructed,*Path('work/f8').rglob('*.nds')]:
        if not any(Path(r['path']).resolve()==rom.resolve() for r in pins):
            pins.append(dict(path=str(rom.resolve()),reason='Preserve registered Rafael249 eight-stage build/reconstruction andall intermediates. SHA256 '+sha(rom.read_bytes())))
    save(pins_path,pins)
    print('669 entries/114 accepted layers/eight stages/249 exact references andclean-input patch pass;own startup binding pending.',flush=True)

if __name__=='__main__':main()
