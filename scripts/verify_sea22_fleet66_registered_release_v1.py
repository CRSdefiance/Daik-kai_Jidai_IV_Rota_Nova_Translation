"""Verify675 cumulative entries and59 new Help articles using three honest page-proof groups."""
import argparse,os,sys
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.dialogue.reviewed_help_pages_v7 import plan_articles as sea_plan
from dk4tool.dialogue.reviewed_help_fleet66_amendment_v1 import plan_articles as fleet_plan
from scripts.audit_story_glyph_consistency import load,save
from scripts.verify_release_baseline import main as verify_baseline
from scripts.verify_rafael_B51_B60_registered_release import KEYS,PIPELINES

PARENT=Path('work/analysis/Shipyard_HELP37_release_verified_20261104/registered_release_verification.json')
QUAL=Path('work/analysis/Sea22_Fleet66_release_qualification_20261105/qualification.json')
SHIP=Path('translations/shipyard_help37_editorial_release_v2.json')
FILE='/COMMON/HELP.DK4'

def proof_group(config_path,candidate):
    c=load(config_path);doc,native,visual,actual,av=[load(Path(c[k])) for k in ['manuscript','native','visual','actual','actual_visual']]
    assert native['all_complete_glyph_codes_font_pixels_link_requests_row_coordinates_input_header_andpixel_guards_pass']
    assert native['all_executed_current_instruction_bytes_exact']
    assert native['current_ARM9_sha256']==sha(candidate.read_file('/__arm9__.bin'))
    assert visual['native_proof_sha256']==sha(Path(c['native']).read_bytes())
    assert actual['all_selected_complete_actual_pages_andnative_child_targets_pass']
    assert actual['actual_ordinary_controls_no_state_injection'] and actual['archive_load_andnative_widgets_observed']
    assert av.get('actual_proof_sha256',av.get('actual_verification_sha256'))==sha(Path(c['actual']).read_bytes())
    if len(doc['records'])==37:
        assert visual['all38_complete_pages_approved'] and visual['all_ten_sheets_directly_viewed']
        assert av['all17_observed_pages_approved'] and (actual['actual_pages'],actual['actual_articles'],actual['offline_only_pages'])==(17,16,21)
    elif len(doc['records'])==22:
        assert visual['all22_complete_pages_approved'] and visual['all_six_sheets_directly_viewed']
        assert av['all22_observed_pages_approved'] and (actual['actual_pages'],actual['actual_articles'],actual['offline_only_pages'])==(22,22,0)
    else:
        assert len(doc['records'])==1 and doc['records'][0]['topic_id']==66
        assert visual['all_two_complete_pages_directly_viewed'] and av['all_two_observed_complete_pages_andone_actual_sheet_directly_viewed']
        assert (actual['actual_pages'],actual['actual_articles'],actual['offline_only_pages'])==(2,1,0)
    research=Path(actual['research_ROM']);assert sha(research.read_bytes())==actual['research_ROM_sha256']
    image=NdsImage.open(research)
    for f in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']:
        assert candidate.read_file(f)==image.read_file(f),(config_path,f)
    blocks=IlnkContainer.parse(image.read_file(FILE)).blocks
    for row in doc['records']:
        assert all(row['review'].values())
        for p in row['planned_stored_pages']:
            b=p['block'];raw=bytes.fromhex(p['exact_stored_hex'])
            assert raw==blocks[b]
            case=next(r for r in native['records'] if r['topic_id']==b)
            assert case['encoded_hex']==raw.hex() and case['all_visible_lines_coordinates_complete_pixels_and_first_final_glyphs_exact']
            assert case['input_header_pixel_guards_pass'] and case['all_executed_current_instruction_bytes_exact']
            assert sha(Path(p['native_preview']).read_bytes())==p['native_preview_sha256']
            observed=[r for r in actual['actual_HELP_cases'] if r['topic_id']==b]
            if 'actual_frame' in p:
                assert len(observed)==1 and observed[0]['frame']==p['actual_frame']
                assert observed[0]['capture_sha256']==p['actual_capture_sha256']==sha(Path(p['actual_capture']).read_bytes())
                assert observed[0]['all_first_internal_final_glyphs_andblank_gaps_exact']
                assert observed[0]['full252x164_actual_text_mask_equals_current_independent_font_model']
                ram=observed[0]['RAM'];assert sha(Path(ram['path']).read_bytes())==ram['sha256']
            else:assert not observed and row['offline_only'] and row['topic_id'] in actual['offline_only_article_IDs']
    return c,doc,actual

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ['candidate','preparation','out']:parser.add_argument('--'+key,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    prep,parentproof,qualification=map(load,[args.preparation,PARENT,QUAL])
    registry_path=Path('translations/release_stack.json');registry=load(registry_path);profile=registry['profiles'][prep['profile']]
    manifest_path=args.candidate.with_suffix('.manifest.json');m=load(manifest_path)
    parentpath=Path(parentproof['candidate']);pm=load(parentpath.with_suffix('.manifest.json'))
    assert sha(registry_path.read_bytes())==prep['registry_sha256']==m['release_stack_sha256']
    assert m['profile']==prep['profile'] and len(m['checks'])==26 and all(m['checks'].values())
    assert all(m['checks'][k]==v for k,v in pm['checks'].items())
    assert m['checks']['registered_Fernan_name_field_and_complete_parent_target_inverse']
    paths=[Path(profile[k]) for k in KEYS];configs=list(map(load,paths))
    assert paths==[Path(prep['preserved_stage_configs'][k]) for k in KEYS]
    extensionpaths=list(map(Path,prep['configs']));extensionconfigs=list(map(load,extensionpaths))
    manuscripts=[str(Path(c['manuscript'])) for c in extensionconfigs]
    assert m['batches']==[*pm['batches'][:-8],*manuscripts,*map(str,paths)] and len(m['batches'])==675
    assert m['required_batches']==pm['required_batches']
    assert profile['late_editorial_extensions'][-2:]==prep['new_extension_specs']
    for spec in prep['new_extension_specs']:
        assert sha(Path(spec['config']).read_bytes())==spec['config_sha256']
        assert sha(Path(*spec['module'].split('.')).with_suffix('.py').read_bytes())==spec['module_sha256']
    assert qualification['direct_prepublication_andshared_targets_equal'] and len(qualification['changed_scope_andordering_rejections'])==5
    assert qualification['unchanged_eight_final_stage_contracts_compared_exactly']
    assert qualification['all_inputs_unowned_files_components_andcomplete_inverses_preserved']
    for c in [*extensionconfigs,*configs]:
        for path,digest in c.get('dependencies',{}).items():assert sha(Path(path).read_bytes())==digest,path
    before=load(args.preparation.parent/'release_stack_before.json')
    assert registry['accepted_layers']==before['accepted_layers'] and len(registry['accepted_layers'])==114
    assert all(registry['profiles'][k]==v for k,v in before['profiles'].items())
    present={str(Path(p).resolve()).casefold() for p in m['batches']}
    assert all(r.get('baked_into_baseline') is True or str(Path(r['batch']).resolve()).casefold() in present for r in registry['accepted_layers'])
    baseline=Path(registry['canonical_baseline']['path'])
    assert m['base_sha256']==sha(baseline.read_bytes())==registry['canonical_baseline']['sha256']
    assert sha(parentpath.read_bytes())==parentproof['candidate_sha256']==pm['candidate_sha256']
    assert sha(args.candidate.read_bytes())==m['candidate_sha256']==prep['target_ROM_sha256']
    assert args.candidate.read_bytes()==Path(prep['final_ROM']).read_bytes()
    stages=[Path(m[a][b]) for a,b in PIPELINES]+[args.candidate]
    assert sha(stages[0].read_bytes())==extensionconfigs[-1]['target_ROM_sha256']
    for i,(p,c) in enumerate(zip(paths,configs,strict=True)):
        assert sha(stages[i].read_bytes())==c['parent_ROM_sha256'] and sha(stages[i+1].read_bytes())==c['target_ROM_sha256']
        sm=load(stages[i+1].with_suffix('.manifest.json'))
        assert sm['release_stack_sha256']==prep['registry_sha256'] and sm['candidate_sha256']==c['target_ROM_sha256'] and all(sm['checks'].values())
        assert str(p) in sm['batches']
    parent,candidate,base,clean=[NdsImage.open(p) for p in [parentpath,args.candidate,baseline,Path(extensionconfigs[0]['clean_ROM'])]]
    assert sha(Path(extensionconfigs[0]['clean_ROM']).read_bytes())==extensionconfigs[0]['clean_ROM_sha256']
    assert [p for _,p,v in parent.iter_files() if candidate.read_file(p)!=v]==[FILE]
    assert all(candidate.read_file(p)==v for p,v in parent.iter_components())
    resource=parent.read_file(FILE)
    for c,compiler in zip(extensionconfigs,[sea_plan,fleet_plan],strict=True):
        resource,compiled=compiler(load(Path(c['manuscript'])),clean.read_file(FILE),base.read_file(FILE),resource)
        assert resource==Path(c['target_resource']).read_bytes() and sha(resource)==c['target_HELP_sha256']
        assert compiled['pages']==load(Path(c['plan']))['pages']
    assert resource==candidate.read_file(FILE)
    blocks=IlnkContainer.parse(resource).blocks;assert len(blocks)==217
    # Use the archive's actual table;never assume archive offsets remain stable after earlier articles grow.
    import struct
    offsets=[struct.unpack_from('<I',resource,8+4*i)[0] for i in range(len(blocks))]
    groups=[proof_group(p,candidate) for p in [SHIP,*extensionpaths]]
    records={r['topic_id']:(r,c,a) for c,d,a in groups for r in d['records']}
    assert len(records)==59 and set(records)==set(range(44,103))
    assert (sum(r['decision']=='revision' for r,_,_ in records.values()),sum(r['decision']=='retention' for r,_,_ in records.values()))==(44,15)
    bindings=[];observed=0;offline=0;observedarticles=0
    for topic,(row,c,actual) in sorted(records.items()):
        pages=[];hasactual=False
        for p in row['planned_stored_pages']:
            raw=bytes.fromhex(p['exact_stored_hex']);b=p['block'];assert blocks[b]==raw
            off=offsets[b];assert resource[off:off+len(raw)]==raw
            final={**deepcopy(p),'archive_offset':off,'bytes':len(raw),'offset_table_slot':8+4*b,'target_archive_sha256':sha(resource),
                'source_page_proof':c['actual'],'source_page_proof_sha256':sha(Path(c['actual']).read_bytes())}
            if 'actual_frame' in p:observed+=1;hasactual=True
            else:offline+=1
            pages.append(final)
        observedarticles+=int(hasactual)
        bindings.append(dict(id=row['id'],file_path=FILE,topic_id=topic,source_reference=row['source_reference'],source_hex=row['source_hex'],
            current_reference=row['current_reference'],current_hex=row['current_hex'],registered_pages=pages,
            decision=row['decision'],finding=row['finding'],retention_reason=row.get('retention_reason'),review=row['review']))
    assert (sum(len(r['registered_pages']) for r in bindings),observed,observedarticles,offline)==(60,39,38,21)
    inverse=deepcopy(candidate);inverse.replace_file(FILE,parent.read_file(FILE));assert bytes(inverse.rom.save())==parentpath.read_bytes()
    oldargv=sys.argv
    try:
        sys.argv=['verify_release_baseline',str(baseline),str(args.candidate)]
        for p in m['changed_paths']:sys.argv+=['--allow-path',p]
        verify_baseline()
    finally:sys.argv=oldargv
    patch=args.candidate.with_suffix('.xdelta');assert not patch.exists();args.out.mkdir(parents=True)
    reconstruction=args.out/'clean_input_reconstruction_RESEARCH_ONLY.nds'
    make_xdelta(Path(extensionconfigs[0]['clean_ROM']),args.candidate,patch)
    apply_xdelta(Path(extensionconfigs[0]['clean_ROM']),patch,reconstruction)
    assert reconstruction.read_bytes()==args.candidate.read_bytes()
    bound=args.out/'exact_integrated_record_bindings.json'
    save(bound,dict(candidate=str(args.candidate),candidate_sha256=m['candidate_sha256'],records=bindings,
        all59_exact_source_current_target_pages_andindividual_five_gates_bound=True,new_credit=0))
    composite=args.out/'composite_page_coverage.json'
    save(composite,dict(candidate=str(args.candidate),candidate_sha256=m['candidate_sha256'],
        proof_groups=[dict(manuscript=c['manuscript'],actual=c['actual'],actual_sha256=sha(Path(c['actual']).read_bytes()),
            research_ROM=a['research_ROM'],research_ROM_sha256=a['research_ROM_sha256']) for c,d,a in groups],
        every_selected_page_byte_andARM9_COMMON_font_dependency_exact_to_its_own_observed_research_image=True,
        final_archive_offsets_rebound_without_relabeling_older_RAM_orcaptures=True,
        native_andvisually_reviewed_pages=60,observed_pages=39,observed_articles=38,offline_only_pages=21,
        duplicate_old66_and216_observations_superseded_by_amendment_not_double_counted=True,
        all60_observed_on_one_final_ROM=False,actual_full_story_playthrough=False,hardware=False,new_credit=0))
    save(args.out/'registered_release_verification.json',dict(candidate=str(args.candidate),candidate_sha256=m['candidate_sha256'],manifest=str(manifest_path),manifest_sha256=sha(manifest_path.read_bytes()),
        profile=m['profile'],registry_sha256=prep['registry_sha256'],canonical_base=str(baseline),canonical_sha256=m['base_sha256'],parent=str(parentpath),parent_sha256=parentproof['candidate_sha256'],
        changed_internal_files=[FILE],changed_components=[],target_HELP_sha256=sha(resource),composite_page_coverage=str(composite),composite_page_coverage_sha256=sha(composite.read_bytes()),
        only_HELP_changed_all_other_files_components_graphics_names_andruntime_exact_to_parent=True,
        complete_stack_entries=675,accepted_layers=114,passing_release_checks=26,all_eight_registered_final_stages_preserved=True,
        Fernan_name_field_proof=m['relocations']['/__arm9__.bin']['owned_Fernan_name_field']['proof'],
        new_contextual_records=59,prose_revisions=44,justified_retentions=15,native_andvisually_reviewed_pages=60,observed_actual_pages=39,observed_actual_articles=38,offline_only_pages=21,offline_only_articles=21,
        all59_exact_integrated_references_bound=True,exact_record_bindings=str(bound),exact_record_bindings_sha256=sha(bound.read_bytes()),
        byte_exact_to_reviewed_research_image=True,patch=str(patch),patch_sha256=sha(patch.read_bytes()),clean_input_sha256=extensionconfigs[0]['clean_ROM_sha256'],
        exact_clean_reconstruction=str(reconstruction),reconstructed_sha256=sha(reconstruction.read_bytes()),clean_input_patch_byte_exact=True,own_registered_startup_pending=True,
        experimental_not_promoted=True,full_goal_complete=False,new_credit=0,preparation=str(args.preparation),preparation_sha256=sha(args.preparation.read_bytes()),qualification=str(QUAL),qualification_sha256=sha(QUAL.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes())))
    pins_path=Path('translations/rom_retention_pins.json');beforebytes=pins_path.read_bytes();pins=load(pins_path);(args.out/'pins.before.json').write_bytes(beforebytes)
    for rom in [args.candidate,reconstruction,*Path('work/s22f66m').rglob('*.nds')]:
        if not any(Path(r['path']).resolve()==rom.resolve() for r in pins):pins.append(dict(path=str(rom.resolve()),reason='Preserve675 cumulative build/intermediate/clean reconstruction. SHA256 '+sha(rom.read_bytes())))
    pending=pins_path.with_name('rom_retention_pins.Sea22_Fleet66_verified.pending.json');assert not pending.exists();save(pending,pins)
    assert pins_path.read_bytes()==beforebytes;os.replace(pending,pins_path)
    print('675 entries/114 accepted layers/eight stages/59 exact articles/clean patch pass;60 native,39 observed across three proof groups,21 offline-only pages;own startup pending.')

if __name__=='__main__':main()
