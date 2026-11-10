"""Verify the completed cumulative Help build,all eight stages,23 exact articles andclean-input reconstruction."""
import argparse,os,sys
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.reviewed_help_pages_v1 import plan_articles
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from scripts.audit_story_glyph_consistency import load,save
from scripts.verify_release_baseline import main as verify_baseline
from scripts.verify_rafael_B51_B60_registered_release import KEYS,PIPELINES

PARENT_PROOF=Path('work/analysis/Rafael_B61_B80_release_verified_20261104/registered_release_verification.json')
QUAL=Path('work/analysis/Early_HELP23_release_qualification_20261104/qualification.json')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ['candidate','preparation','out']:parser.add_argument('--'+key,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    prep,parent_proof,qualification=map(load,[args.preparation,PARENT_PROOF,QUAL])
    registry_path=Path('translations/release_stack.json');registry=load(registry_path);profile=registry['profiles'][prep['profile']]
    manifest_path=args.candidate.with_suffix('.manifest.json');manifest=load(manifest_path)
    parent_path=Path(parent_proof['candidate']);parent_manifest=load(parent_path.with_suffix('.manifest.json'))
    assert sha(registry_path.read_bytes())==manifest['release_stack_sha256']==prep['registry_sha256']
    assert manifest['profile']==prep['profile'] and all(manifest['checks'].values()) and len(manifest['checks'])==26
    assert all(manifest['checks'][k]==v for k,v in parent_manifest['checks'].items())
    assert manifest['checks']['registered_Fernan_name_field_and_complete_parent_target_inverse']
    config_paths=[Path(profile[k]) for k in KEYS];configs=list(map(load,config_paths))
    assert config_paths==[Path(prep['preserved_stage_configs'][key]) for key in KEYS]
    old_profile=registry['profiles'][parent_proof['profile']]
    assert parent_manifest['batches'][-8:]==[str(Path(old_profile[k])) for k in KEYS]
    conf=load(prep['config']);final_path=Path(conf['manuscript']);doc=load(final_path)
    assert manifest['batches']==[*parent_manifest['batches'][:-8],str(final_path),*map(str,config_paths)]
    assert len(manifest['batches'])==671 and manifest['required_batches']==parent_manifest['required_batches']
    spec=profile['late_editorial_extensions'][-1];assert spec['config']==prep['config']
    assert sha(Path(spec['config']).read_bytes())==spec['config_sha256']
    module_path=Path(*spec['module'].split('.')).with_suffix('.py');assert sha(module_path.read_bytes())==spec['module_sha256']
    assert len(qualification['semantic_rejections'])==10 and qualification['direct_andshared_Help_targets_equal']
    assert qualification['unchanged_eight_final_stage_contracts_compared_exactly']
    for value in [conf,*configs]:
        for path,digest in value.get('dependencies',{}).items():assert sha(Path(path).read_bytes())==digest,path
    old_registry=load(args.preparation.parent/'release_stack_before.json')
    assert registry['accepted_layers']==old_registry['accepted_layers'] and len(registry['accepted_layers'])==114
    assert all(registry['profiles'][k]==v for k,v in old_registry['profiles'].items())
    present={str(Path(p).resolve()).casefold() for p in manifest['batches']}
    assert all(r.get('baked_into_baseline') is True or str(Path(r['batch']).resolve()).casefold() in present for r in registry['accepted_layers'])
    baseline=Path(registry['canonical_baseline']['path']);assert manifest['base_sha256']==sha(baseline.read_bytes())==registry['canonical_baseline']['sha256']
    assert sha(parent_path.read_bytes())==parent_proof['candidate_sha256']==parent_manifest['candidate_sha256']
    assert sha(args.candidate.read_bytes())==manifest['candidate_sha256']==prep['target_ROM_sha256']
    assert args.candidate.read_bytes()==Path(prep['final_ROM']).read_bytes()
    stages=[Path(manifest[a][b]) for a,b in PIPELINES]+[args.candidate]
    assert sha(stages[0].read_bytes())==conf['target_ROM_sha256']
    for i,(path,value) in enumerate(zip(config_paths,configs,strict=True)):
        assert sha(stages[i].read_bytes())==value['parent_ROM_sha256'] and sha(stages[i+1].read_bytes())==value['target_ROM_sha256']
        m=load(stages[i+1].with_suffix('.manifest.json'))
        assert m['release_stack_sha256']==prep['registry_sha256'] and m['candidate_sha256']==value['target_ROM_sha256'] and all(m['checks'].values())
        assert str(path) in m['batches']
    parent,candidate,base,clean=[NdsImage.open(p) for p in [parent_path,args.candidate,baseline,Path(conf['clean_ROM'])]]
    assert sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256']
    assert [p for _,p,v in parent.iter_files() if candidate.read_file(p)!=v]==['/COMMON/HELP.DK4']
    assert all(candidate.read_file(p)==v for p,v in parent.iter_components())
    assert sha(candidate.read_file('/__arm9__.bin'))==conf['final_runtime_ARM9_sha256']
    file=doc['file_path'];resource,compiled=plan_articles(doc,clean.read_file(file),base.read_file(file),parent.read_file(file))
    assert resource==candidate.read_file(file)==Path(conf['target_resource']).read_bytes()
    assert compiled['pages']==load(conf['plan'])['pages'] and len(compiled['pages'])==25
    blocks=IlnkContainer.parse(resource).blocks;assert len(blocks)==212
    actual=load(conf['actual']);visual=load(conf['actual_visual'])
    assert actual['all25_complete_actual_pages_andnative_child_targets_pass'] and visual['all25_complete_pages_approved']
    assert actual['research_ROM_sha256']==manifest['candidate_sha256'] and visual['actual_proof_sha256']==sha(Path(conf['actual']).read_bytes())
    assert len(doc['records'])==23 and (doc['proposed_revisions'],doc['justified_retentions'])==(16,7)
    bindings=[]
    for row in doc['records']:
        assert all(row['review'].values());pages=row['planned_stored_pages']
        assert len(pages)==len([p for p in compiled['pages'] if p['source_article_id']==row['topic_id']])
        for page in pages:
            raw=bytes.fromhex(page['exact_stored_hex']);at=page['archive_offset'];block=page['block']
            assert resource[at:at+len(raw)]==raw==blocks[block] and page['bytes']==len(raw) and page['target_archive_sha256']==sha(resource)
            case=next(r for r in actual['actual_HELP_cases'] if r['topic_id']==block)
            assert case['frame']==page['actual_frame'] and case['all_first_internal_final_glyphs_andblank_gaps_exact']
        bindings.append(dict(id=row['id'],file_path=file,topic_id=row['topic_id'],source_reference=row['source_reference'],source_hex=row['source_hex'],
            current_reference=row['current_reference'],current_hex=row['current_hex'],registered_pages=pages,
            decision=row['decision'],finding=row['finding'],retention_reason=row.get('retention_reason'),review=row['review']))
    inverse=deepcopy(candidate);inverse.replace_file(file,parent.read_file(file));assert bytes(inverse.rom.save())==parent_path.read_bytes()
    old_argv=sys.argv
    try:
        sys.argv=['verify_release_baseline',str(baseline),str(args.candidate)]
        for path in manifest['changed_paths']:sys.argv+=['--allow-path',path]
        verify_baseline()
    finally:sys.argv=old_argv
    patch=args.candidate.with_suffix('.xdelta');assert not patch.exists();args.out.mkdir(parents=True)
    reconstructed=args.out/'clean_input_reconstruction_RESEARCH_ONLY.nds'
    make_xdelta(Path(conf['clean_ROM']),args.candidate,patch);apply_xdelta(Path(conf['clean_ROM']),patch,reconstructed)
    assert reconstructed.read_bytes()==args.candidate.read_bytes()
    save(args.out/'exact_integrated_record_bindings.json',dict(candidate=str(args.candidate),candidate_sha256=manifest['candidate_sha256'],records=bindings,
        all23_exact_source_current_target_pages_andindividual_five_gates_bound=True,new_credit=0))
    field_proof=manifest['relocations']['/__arm9__.bin']['owned_Fernan_name_field']['proof']
    save(args.out/'registered_release_verification.json',dict(candidate=str(args.candidate),candidate_sha256=manifest['candidate_sha256'],
        manifest=str(manifest_path),manifest_sha256=sha(manifest_path.read_bytes()),profile=manifest['profile'],registry_sha256=prep['registry_sha256'],
        canonical_base=str(baseline),canonical_sha256=manifest['base_sha256'],parent=str(parent_path),parent_sha256=parent_proof['candidate_sha256'],
        changed_internal_files=[file],changed_components=[],target_HELP_sha256=sha(resource),actual_help_proof=conf['actual'],actual_help_proof_sha256=sha(Path(conf['actual']).read_bytes()),
        only_HELP_changed_all_other_files_components_graphics_names_andruntime_exact_to_parent=True,
        complete_stack_entries=671,accepted_layers=114,passing_release_checks=26,all_eight_registered_final_stages_preserved=True,
        Fernan_name_field_proof=field_proof,new_contextual_records=23,prose_revisions=16,justified_retentions=7,
        native_andactual_pages=25,actual_ordinary_Help_frames=32761,all23_exact_integrated_references_bound=True,
        byte_exact_to_reviewed_research_image=True,patch=str(patch),patch_sha256=sha(patch.read_bytes()),clean_input_sha256=conf['clean_ROM_sha256'],
        exact_clean_reconstruction=str(reconstructed),reconstructed_sha256=sha(reconstructed.read_bytes()),clean_input_patch_byte_exact=True,
        own_registered_startup_pending=True,experimental_not_promoted=True,full_goal_complete=False,new_credit=0,
        preparation=str(args.preparation),preparation_sha256=sha(args.preparation.read_bytes()),qualification=str(QUAL),qualification_sha256=sha(QUAL.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes())))
    pins_path=Path('translations/rom_retention_pins.json');before=pins_path.read_bytes();pins=load(pins_path);(args.out/'pins.before.json').write_bytes(before)
    for rom in [args.candidate,reconstructed,*Path('work/h23').rglob('*.nds')]:
        if not any(Path(r['path']).resolve()==rom.resolve() for r in pins):
            pins.append(dict(path=str(rom.resolve()),reason='Preserve registered Help23 build/reconstruction andall intermediates. SHA256 '+sha(rom.read_bytes())))
    temp=pins_path.with_name('rom_retention_pins.HELP23_verified.pending.json');assert not temp.exists();save(temp,pins)
    assert pins_path.read_bytes()==before;os.replace(temp,pins_path)
    print('671 entries/114 accepted layers/eight stages/23 exact articles andclean-input patch pass;own registered startup binding pending.')

if __name__=='__main__':main()
