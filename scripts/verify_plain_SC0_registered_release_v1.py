"""Verify the original cumulative stack,owned SC0 references andexact clean-input patch."""
import argparse
import os
import sys
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.verify_release_baseline import main as verify_baseline
from scripts.verify_rafael_B51_B60_registered_release import KEYS,PIPELINES


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ['candidate','preparation','qualification','parent-release','build-terminal','build-work','out']:
        parser.add_argument('--'+key,type=Path,required=True)
    args=parser.parse_args()
    patch=args.candidate.with_suffix('.xdelta')
    assert not args.out.exists() and not patch.exists()
    prep,q,parentproof,terminal=map(load,[args.preparation,args.qualification,args.parent_release,args.build_terminal])
    assert terminal['terminal'] and terminal['driver_completed_without_exception'] and terminal['all_original_driver_andregistry_bytes_unchanged']
    assert not terminal['garbage_collection']['errors']
    assert terminal['original_locked_ROM_core_sha256']==sha(Path('dk4tool/rom/nds.py').read_bytes())
    for path,digest in terminal['driver_andcanonical_bytes'].items():assert sha(Path(path).read_bytes())==digest
    registry_path=Path('translations/release_stack.json');registry=load(registry_path)
    manifest_path=args.candidate.with_suffix('.manifest.json');m=load(manifest_path)
    parentpath=Path(parentproof['candidate']);pm=load(parentpath.with_suffix('.manifest.json'))
    assert sha(registry_path.read_bytes())==prep['registry_sha256']==q['registry_sha256']==m['release_stack_sha256']==terminal['registry_sha256']
    assert m['profile']==terminal['profile']==prep['profile']==q['profile']
    assert len(m['checks'])==26 and all(m['checks'].values()) and all(m['checks'][k]==v for k,v in pm['checks'].items())
    assert m['checks']['registered_Fernan_name_field_and_complete_parent_target_inverse']
    assert q['preparation_sha256']==sha(args.preparation.read_bytes()) and q['direct_prepublication_andshared_targets_equal']
    assert len(q['changed_scope_andordering_rejections'])==8 and q['unchanged_eight_final_stage_contracts_compared_exactly']
    profile=registry['profiles'][prep['profile']]
    paths=[Path(profile[k]) for k in KEYS];configs=list(map(load,paths))
    assert paths==[Path(prep['preserved_stage_configs'][k]) for k in KEYS]
    assert len(prep['configs'])==len(prep['new_extension_specs'])==1
    sceneconf=load(prep['configs'][0]);finalpath=Path(sceneconf['manuscript']);doc=load(finalpath)
    assert m['batches']==[*pm['batches'][:-8],str(finalpath),*map(str,paths)] and len(m['batches'])==prep['expected_manifest_entries']
    assert m['required_batches']==pm['required_batches'] and profile['late_editorial_extensions'][-1]==prep['new_extension_specs'][0]
    spec=prep['new_extension_specs'][0]
    assert sha(Path(spec['config']).read_bytes())==spec['config_sha256']
    assert sha(Path(*spec['module'].split('.')).with_suffix('.py').read_bytes())==spec['module_sha256']
    for conf in [sceneconf,*configs]:
        for path,digest in conf.get('dependencies',{}).items():assert sha(Path(path).read_bytes())==digest,path
    before=load(args.preparation.parent/'release_stack_before.json')
    assert registry['accepted_layers']==before['accepted_layers'] and len(registry['accepted_layers'])==114
    assert all(registry['profiles'][k]==v for k,v in before['profiles'].items())
    present={str(Path(p).resolve()).casefold() for p in m['batches']}
    assert all(r.get('baked_into_baseline') is True or str(Path(r['batch']).resolve()).casefold() in present for r in registry['accepted_layers'])
    baseline=Path(registry['canonical_baseline']['path'])
    assert sha(baseline.read_bytes())==registry['canonical_baseline']['sha256']==m['base_sha256']
    assert sha(parentpath.read_bytes())==parentproof['candidate_sha256']==pm['candidate_sha256']
    assert sha(args.candidate.read_bytes())==m['candidate_sha256']==prep['target_ROM_sha256']
    assert args.candidate.read_bytes()==Path(prep['final_ROM']).read_bytes()
    stages=[Path(m[a][b]) for a,b in PIPELINES]+[args.candidate]
    assert sha(stages[0].read_bytes())==sceneconf['target_ROM_sha256']
    for i,(path,conf) in enumerate(zip(paths,configs,strict=True)):
        assert sha(stages[i].read_bytes())==conf['parent_ROM_sha256'] and sha(stages[i+1].read_bytes())==conf['target_ROM_sha256']
        sm=load(stages[i+1].with_suffix('.manifest.json'))
        assert sm['candidate_sha256']==conf['target_ROM_sha256'] and sm['release_stack_sha256']==prep['registry_sha256'] and all(sm['checks'].values())
        assert str(path) in sm['batches']
    parent,candidate=map(NdsImage.open,[parentpath,args.candidate]);file='/data/SC0.DK4'
    assert [p for _,p,v in parent.iter_files() if candidate.read_file(p)!=v]==[file]
    assert all(candidate.read_file(p)==v for p,v in parent.iter_components())
    resource=candidate.read_file(file);rebuilt=load(sceneconf['reconstruction'])
    assert sha(parent.read_file(file))==rebuilt['source_archive_sha256'] and sha(resource)==rebuilt['target_archive_sha256']
    assert resource==Path(rebuilt['target_archive']).read_bytes()
    oldblocks,blocks=[IlnkContainer.parse(x).blocks for x in [parent.read_file(file),resource]]
    assert len(oldblocks)==len(blocks)==343
    assert [i for i,(a,b) in enumerate(zip(oldblocks,blocks,strict=True)) if a!=b]==sceneconf['blocks']==rebuilt['changed_blocks']
    assert blocks[44]==oldblocks[44] and all(blocks[i]==oldblocks[i] for i in [81,82,83,84])
    for group in rebuilt['groups']:assert sha(blocks[group['block']])==group['target_sha256']
    bindings=[]
    for row in doc['records']:
        assert all(row['review'].values())
        ref=row['planned_integrated_reference'];raw=bytes.fromhex(ref['exact_stored_hex']);at=ref['offset'];block=blocks[row['block']]
        assert block[at:at+len(raw)+1]==raw+b'\0' and ref['target_archive_sha256']==sha(resource)
        if row['kind']!='typed-choice-label':assert block[ref['header_offset']:at+1].hex()==row['source_complete_preamble_hex']
        bindings.append(dict(id=row['id'],file_path=file,block=row['block'],source_reference=row['source_reference'],source_hex=row['source_hex'],
            current_reference=row['current_reference'],current_hex=row['current_hex'],registered_reference=ref,decision=row['decision'],
            finding=row['finding'],retention_reason=row.get('retention_reason'),review=row['review']))
    revisions=sum(r['decision']=='revision' for r in bindings);retentions=sum(r['decision']=='retention' for r in bindings)
    assert len(bindings)==sceneconf['record_count']==revisions+retentions
    inverse=deepcopy(candidate);inverse.replace_file(file,parent.read_file(file))
    assert bytes(inverse.rom.save())==parentpath.read_bytes()
    oldargv=sys.argv
    try:
        sys.argv=['verify_release_baseline',str(baseline),str(args.candidate)]
        for path in m['changed_paths']:sys.argv+=['--allow-path',path]
        verify_baseline()
    finally:sys.argv=oldargv
    args.out.mkdir(parents=True)
    clean=Path(sceneconf['clean_ROM']);assert sha(clean.read_bytes())==sceneconf['clean_ROM_sha256']
    reconstruction=args.out/'clean_input_reconstruction_RESEARCH_ONLY.nds'
    make_xdelta(clean,args.candidate,patch);apply_xdelta(clean,patch,reconstruction)
    assert reconstruction.read_bytes()==args.candidate.read_bytes()
    bound=args.out/'exact_integrated_record_bindings.json'
    save(bound,dict(candidate=str(args.candidate),candidate_sha256=m['candidate_sha256'],records=bindings,all_individual_five_gates_andexact_source_current_final_refs_bound=True,new_credit=0))
    actual=load(sceneconf['actual'])
    save(args.out/'registered_release_verification.json',dict(candidate=str(args.candidate),candidate_sha256=m['candidate_sha256'],manifest=str(manifest_path),manifest_sha256=sha(manifest_path.read_bytes()),
        profile=m['profile'],registry_sha256=prep['registry_sha256'],canonical_base=str(baseline),canonical_sha256=m['base_sha256'],parent=str(parentpath),parent_sha256=parentproof['candidate_sha256'],
        changed_internal_files=[file],changed_components=[],target_SC0_sha256=sha(resource),
        all_other_files_components_graphics_names_andruntime_exact_to_parent=True,only_owned_SC0_blocks_changed=sceneconf['blocks'],
        complete_stack_entries=len(m['batches']),accepted_layers=114,passing_release_checks=26,all_eight_registered_final_stages_preserved=True,
        Fernan_name_field_proof=m['relocations']['/__arm9__.bin']['owned_Fernan_name_field']['proof'],
        new_contextual_records=len(bindings),prose_revisions=revisions,justified_retentions=retentions,exact_record_bindings=str(bound),exact_record_bindings_sha256=sha(bound.read_bytes()),
        exact_all_integrated_references_bound=True,native_andviewed_body_pages=sceneconf['native_pages'],typed_choice_labels=sceneconf['typed_choice_count'],
        observed_actual_source_speeches=actual['source_speeches_observed'],observed_actual_body_pages=actual['native_body_pages_observed'],observed_actual_choices=actual['actual_choice_labels'],
        offline_only_source_speeches=actual['offline_only_source_speeches'],actual_review=sceneconf['actual'],actual_review_sha256=sha(Path(sceneconf['actual']).read_bytes()),
        byte_exact_to_reviewed_research_image=True,patch=str(patch),patch_sha256=sha(patch.read_bytes()),clean_input_sha256=sceneconf['clean_ROM_sha256'],
        exact_clean_reconstruction=str(reconstruction),reconstructed_sha256=sha(reconstruction.read_bytes()),clean_input_patch_byte_exact=True,own_registered_startup_pending=True,
        experimental_not_promoted=True,full_goal_complete=False,new_credit=0,preparation=str(args.preparation),preparation_sha256=sha(args.preparation.read_bytes()),
        qualification=str(args.qualification),qualification_sha256=sha(args.qualification.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes())))
    pins_path=Path('translations/rom_retention_pins.json');pin_before=pins_path.read_bytes();pins=load(pins_path)
    (args.out/'pins.before.json').write_bytes(pin_before)
    for rom in [args.candidate,reconstruction,*args.build_work.rglob('*.nds')]:
        if not any(Path(r['path']).resolve()==rom.resolve() for r in pins):pins.append(dict(path=str(rom.resolve()),reason='Preserve registered plain SC0 cumulative/intermediate/clean reconstruction. SHA256 '+sha(rom.read_bytes())))
    pending=pins_path.with_name('rom_retention_pins.'+args.out.name+'.pending.json');assert not pending.exists();save(pending,pins)
    assert pins_path.read_bytes()==pin_before;os.replace(pending,pins_path)
    print(dict(entries=len(m['batches']),new_source_objects=len(bindings),revisions=revisions,retentions=retentions,exact_clean_patch=True,own_startup_pending=True),flush=True)


if __name__=='__main__':main()
