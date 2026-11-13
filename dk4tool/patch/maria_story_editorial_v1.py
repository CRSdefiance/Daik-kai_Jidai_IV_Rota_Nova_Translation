"""Validate the complete Maria67 batch, reconstruct three blocks, then commit one archive."""
import json
from collections import Counter
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.maria_story_profile_v1 import contract,profile_for
from dk4tool.dialogue import maria_story_layout_v1 as codec
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.maria_story_reconstruction_v1 import reconstruct
from scripts.Maria_story_final_paths_v7771 import proofs
from scripts.seal_Maria_story_references_v7772 import FLAGS
CONFIG='translations/maria_story_editorial_release_v1.json'
PATHS=('/data/SC3.DK4',)
def load(path):return json.loads(Path(path).read_bytes())
def require(value,label):
    if not value:raise ValueError('Maria67 editorial contract: '+label)
def check_dependencies(conf):
    for path,digest in conf['dependencies'].items():require(sha(Path(path).read_bytes())==digest,'dependency:'+path)
def commit_files(image,files):image.rom.files=files
def late_summary(group):
    return dict(block=group['block'],exits=group['source_English_exits'],command_differences=len(group['command_comparison_differences']),
        duration_differences=len(group['duration_differences']),late_RGB_differences=len(group['later_RGB_differences']),
        late_samples=group['later_sample_count'],component_equality=group['five_native_component_equality'],
        actors_equal=group['whole_actors_equal'],final_seeds=group['final_PRNG_seeds'])
def apply_release(image,baseline,config=CONFIG):
    conf=load(config);check_dependencies(conf)
    require(conf['format']=='dk4-Maria67-editorial-release-v1' and len(conf['manuscripts'])==1 and conf['proofs']==proofs(),'single sealed manuscript/proof configuration')
    require(sha(baseline.source.read_bytes())==conf['canonical_ROM_sha256'],'canonical baseline')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'],'clean ROM')
    require(sha(Path(conf['parent_ROM']).read_bytes())==conf['parent_ROM_sha256'],'current parent ROM')
    arm=image.read_file('/__arm9__.bin')
    require(sha(arm)==conf['required_runtime_arm9_sha256'] and sha(image.read_file('/COMMON/MESFILE.DK4'))==conf['required_runtime_common_sha256'],'exact own runtime')
    require({path:sha(value) for _,path,value in image.iter_files()}==conf['predecessor_file_hashes'] and {path:sha(value) for path,value in image.iter_components()}==conf['predecessor_component_hashes'],'complete predecessor files/components')
    clean=NdsImage.open(conf['clean_ROM']);mapping,seal=[load(conf[key]) for key in ['reference_map','reference_approval']]
    require(conf['required_map_flags']==FLAGS and mapping['format']=='dk4-Maria67-source-relocation-map-v1' and all(mapping[key] is True for key in FLAGS),'all sealed map flags')
    require(mapping['source_ROM']==conf['parent_ROM'] and mapping['source_ROM_sha256']==conf['parent_ROM_sha256'] and mapping['clean_ROM_sha256']==conf['clean_ROM_sha256'],'source/current map identity')
    require([g['block'] for g in mapping['groups']]==[34,108,35] and all(g['route']==3 and g['file_path']==PATHS[0] and g['external_references_complete'] for g in mapping['groups']),'three original Maria entries')
    require(seal['all67_five_gates_andexact_references_approved'] and seal['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'reference approval seal')
    p=conf['proofs'];packet,font,stored,actual,later,view,policy,names,branches,loader,census=[load(p[key]) for key in [
        'source_context','native_font_proof','native_stored_proof','actual_proof','later_scope_proof','actual_view','native_policy_validation',
        'speaker_name_review','source_branch_proof','native_loader_proof','native_caller_proof']]
    require(font['all67_single_native_four_row_pages_complete_glyph_bounds_andconsumption'] and font['final_complete_pages']==67 and font['fresh_compiled_alignment_cases']+font['exact_own_current_compiled_alignment_cases_reused']==268,'complete native paragraph coverage')
    require(stored['stored_alignment_coverage']==268 and stored['zero_ink_parity_tails']==33 and stored['final_complete_native_pages']==67 and stored['all67_final_stored_targets_equal_reviewed_complete_native_ink'],'stored native coverage andtails')
    require(policy['positive_count']==len(policy['positive_cases'])==67 and policy['negative_count']==len(policy['negative_cases'])==200 and all(r['rejected'] and r['expected_guard'] in r['error'] for r in policy['negative_cases']),'actual-changing policy guards')
    require(view['all130_final_actual_panes_viewed_with_exact_reuse'] and view['complete_body_andheader_holds']==528 and view['shared155_Sailor_Retainer_review_open_no_global_name_asset_change'],'visual andshared-name scope')
    require(actual['total_actual_speech_occurrences']==actual['complete_actual_page_panels']==130 and not actual['unresolved'] and actual['existing_system_only_unlock_fixture'] and actual['earned_unlock_verified'] is False,'complete disclosed actual scope')
    require(len(actual['groups'])==6 and sum(g['complete_body_andheader_holds'] for g in actual['groups'])==528,'six actual groups/holds')
    for group in actual['groups']:
        number,version=group['block'],group['version'];fixture=group['fixture']
        require(fixture['route']==3 and number in [34,108,35] and version in ['clean_Japanese','English'],'actual route/version')
        require(group['actual_unique_speeches']==len(group['speech_observations'])=={34:8,108:29,35:28}[number] and not group['incomplete_sampled_holds'] and not group['unidentified_trace_rows'],'actual complete/unpartial speeches')
        require(group['native_terminal_result'][0]==0 and group['native_terminal_result'][1]==group['command_pairs'][-2]['native_result'][1] and len(group['command_pairs'])=={34:30,108:49,35:47}[number],'original commands andnormal type0 carry')
        require(sha(Path(group['capture_report']).read_bytes())==group['capture_report_sha256'] and sha(Path(group['observer_report']).read_bytes())==group['observer_report_sha256'],'actual report/trace binding')
    require(len(later['groups'])==3 and [g['block'] for g in later['groups']]==[34,108,35],'three measured comparison groups')
    require([late_summary(g) for g in later['groups']]==view['final_late_limits']==mapping['observed_comparison_contract'],'full measured comparison contract')
    expected=[(34,[6295,6295],7,0,0,163),(108,[11336,11335],37,13,60,79),(35,[11335,11334],35,8,60,79)]
    for group,(number,exits,commands,durations,rgb,samples) in zip(later['groups'],expected,strict=True):
        require(group['block']==number and group['source_English_exits']==exits and len(group['command_comparison_differences'])==commands and len(group['duration_differences'])==durations and len(group['later_RGB_differences'])==rgb and group['later_sample_count']==len(group['later_full_RGB_comparisons'])==samples,'measured timings/late RGB preserved')
        require(not group['actual_initializer_andexchange_result_differences'] and not group['actual_UI_request_differences'] and all(r['whole_upper_scene_portrait_header_RGB_equal'] for r in group['scene_portrait_header_pairs']),'paired scene/results/UI')
    require(names['seven_actual_distinct_speaker_headers_seen_Julian26_offline_only'] and names['all207_name_role_alias_review_active'] and names['shared155_label_semantic_review_still_unresolved_no_asset_edit'],'speaker review limitations')
    require(loader['fresh_native_whole_loads_andcache_hits']==303 and loader['fresh_initial_parent_modes']==606 and census['only_original24070_interpreter_call_no_literal_alias'],'original native loader/caller binding')
    require(len(branches['operands_requiring_adjustment_when_resizing'])==20,'all original branch operands')
    source=image.read_file(PATHS[0]);japanese=clean.read_file(PATHS[0])
    require(sha(source)==mapping['source_archive_sha256']==conf['archives'][0]['source_sha256'] and sha(japanese)==conf['archives'][0]['clean_sha256'] and sha(baseline.read_file(PATHS[0]))==conf['archives'][0]['canonical_sha256'],'current/clean/canonical archives')
    path=conf['manuscripts'][0];doc=load(path);approved=load(doc['native_approved_manuscript'])
    require(doc['file_path']==PATHS[0] and doc['route']==3 and doc['route_identity']=='Maria','document file/route identity')
    require(Path(doc['current_ROM']).resolve()==Path(conf['parent_ROM']).resolve() and doc['current_ROM_sha256']==packet['current_ROM_sha256']==conf['parent_ROM_sha256'],'document current ROM identity')
    require(doc['current_ARM9_sha256']==packet['current_ARM9_sha256']==conf['required_runtime_arm9_sha256'] and doc['current_COMMON_sha256']==packet['current_COMMON_sha256']==conf['required_runtime_common_sha256'],'document runtime identity')
    require(Path(doc['source_ROM']).resolve()==Path(conf['clean_ROM']).resolve() and doc['source_ROM_sha256']==conf['clean_ROM_sha256'],'document clean source identity')
    require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and doc['encoder']=='dialogue-relocatable-v1' and doc['formatting_review_pending'] is False,'reviewed natural-dialogue-v2 manuscript')
    validate_natural_dialogue_batch(doc)
    require(doc['records']==approved['records'] and sha(Path(doc['native_approved_manuscript']).read_bytes())==doc['native_approved_manuscript_sha256'],'individually approved decisions')
    require(seal['manuscript']==path and seal['manuscript_sha256']==sha(Path(path).read_bytes()) and doc['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()) and doc['reference_research_ROM_sha256']==conf['reference_ROM_sha256'],'sealed manuscript/map/reference')
    for key,value in p.items():require(doc[key]==value and doc[key+'_sha256']==sha(Path(value).read_bytes()),'exact proof link:'+key)
    bindings=contract()['record_bindings'];rows=doc['records']
    require(len(rows)==len({r['id'] for r in rows})==67 and Counter(r['editorial_decision'] for r in rows)=={'revise':48,'retain-wording':19},'67 unique decisions')
    sources={r['id']:r for r in packet['records']};fonts={r['id']:r for r in font['records']};stores={r['id']:r for r in stored['records']}
    panels={s['id']:s for g in actual['groups'] if g['version']=='English' for s in g['speech_observations']}
    require(set(sources)==set(fonts)==set(stores)==set(bindings)=={r['id'] for r in rows} and set(bindings)-set(panels)=={'DK4_MES_B108_R0020','DK4_MES_B108_R0125'},'all native sets andtwo unplayed conditionals')
    blocks=IlnkContainer.parse(source).blocks;cleanblocks=IlnkContainer.parse(japanese).blocks;targetblocks=list(blocks);changes=[]
    for row in rows:
        ident=row['id'];b=bindings[ident];before=sources[ident];f=fonts[ident];s=stores[ident]
        require(row['route']==3 and row['route_identity']=='Maria' and row['file_path']==PATHS[0] and row['block']==b['block'] and row['source_selector']==b['source_selector'],'individual source identity:'+ident)
        require(row['source_hex']==before['source_hex']==b['compiler_source_hex'] and row['current_hex']==before['current_hex'] and row['source_reference']==before['source_reference'] and row['current_reference']==before['current_reference'],'individual exact source/current:'+ident)
        require(row['source_meaning']==before['source_gloss'] and row['context']==before['full_clean_exchange_context'] and row['source_Japanese']==before['source_Japanese'],'individual source gloss/context:'+ident)
        require(row['review']=={k:True for k in ['source','context','localization','naturalness','formatting']} and row['whole_English_exchange_cadence_andemotional_progression_reviewed'] and row['editorial_finding'] and row['localization_note'] and (row['editorial_decision']!='retain-wording' or row['retention_reason']),'individual review andretention reason:'+ident)
        require(row['english']==b['planning_record']['english'] and row['logical_English']==b['logical_English'],'exact reviewed prose:'+ident)
        prof=profile_for(arm,blocks[row['block']],ident,PATHS[0]);encoded=codec.encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],prof);qa=codec.audit_relocatable_dialogue_record(bytes.fromhex(row['source_hex']),row['english'],prof)
        require(encoded.encoded.hex()==row['compiled_hex']==b['compiled_hex']==f['compiled_hex'] and qa==row['base_QA_report'],'compiled text/QA:'+ident)
        require(row['qa_waivers']==[] and row['qa_waiver_reason'] is None and row['row_count_reason']==b['row_count_reason'] and row['native_page_count']==1,'scoped display reasons:'+ident)
        value=encoded.encoded;pad=len(value)%2!=len(bytes.fromhex(row['current_hex']))%2
        if pad:value+=b' '
        expanded=bytes.fromhex(f['expanded_native_hex'])+(b' ' if pad else b'')
        require(value.hex()==s['final_target_hex'] and expanded.hex()==s['final_expanded_hex'] and s['parity_space_added']==pad and len(s['native_pipeline']['cases'])==4 and all(c['output_hex']==expanded.hex() for c in s['native_pipeline']['cases']),'final stored alignment/substitution:'+ident)
        require(len(f['pages'])==len(s['complete_pages']['pages'])==1 and all(Path(a['native_plane']).read_bytes()==Path(z['native_plane']).read_bytes() and sha(Path(z['native_plane']).read_bytes())==z['native_plane_sha256']==a['native_plane_sha256'] for a,z in zip(f['pages'],s['complete_pages']['pages'],strict=True)),'complete native ink:'+ident)
        panel=panels.get(ident)
        require(row['actual_record_observed']==(panel is not None),'actual/offline scope:'+ident)
        if panel is not None:
            require(panel['source_selector']==row['source_selector'] and panel['actual_name']==row['speaker'] and panel['native_page_count']==1,'actual speaker/page:'+ident)
            holds=[h for pg in panel['pages'] for h in pg['complete_body_andname_holds']]
            require(len(holds)==row['actual_complete_body_andheader_holds'] and holds and all(h['complete_black_body_mask_equal'] and h['ASCII_gray_equal'] and h['CP932_gray_equal'] and h['complete_name_mask_equal'] and sha(Path(h['capture']).read_bytes())==h['sha256'] for h in holds),'actual complete body/header/palette:'+ident)
        else:require(row['offline_only_reason'] and row['actual_complete_body_andheader_holds']==0,'explicit offline conditional:'+ident)
    for group in mapping['groups']:
        number=group['block'];packetgroup=next(g for g in packet['groups'] if g['block']==number)
        selected=[r for r in rows if r['block']==number]
        targetblocks[number]=reconstruct(blocks[number],cleanblocks[number],group,packetgroup,selected,branches['operands_requiring_adjustment_when_resizing'])
        changes.extend(dict(id=r['id'],file_path=PATHS[0],block=number,old_offset=r['current_reference']['offset'],new_offset=next(t['new_offset'] for t in group['text_records'] if t['id']==r['id'])) for r in selected)
    payload=IlnkContainer(targetblocks).to_bytes()
    require(sha(payload)==mapping['target_archive_sha256']==conf['archives'][0]['target_sha256'],'complete reconstructed archive')
    require(sha(Path(conf['reference_ROM']).read_bytes())==conf['reference_ROM_sha256'],'research ROM identity')
    reference=NdsImage.open(conf['reference_ROM']);require(payload==reference.read_file(PATHS[0]),'pinned approved reference archive')
    require([i for i,(a,b) in enumerate(zip(blocks,targetblocks,strict=True)) if a!=b]==[34,35,108],'only three owned blocks')
    require(all(reference.read_file(path)==value for _,path,value in image.iter_files() if path not in PATHS) and all(reference.read_file(path)==value for path,value in image.iter_components()),'all other files/components unchanged')
    files=list(image.rom.files);index=image.path_map()[PATHS[0]];files[index]=payload
    require([i for i,(a,b) in enumerate(zip(image.rom.files,files,strict=True)) if a!=b]==[index],'one SC3 file slot')
    commit_files(image,files)
    return dict(manuscripts=conf['manuscripts'],reference_map=conf['reference_map'],changed_records=changes,
        files=[dict(file_path=PATHS[0],source_sha256=sha(source),target_sha256=sha(payload),changed_records=changes)],
        one_files_list_commit_after_all_gates=True,three_clean_predecessor_blocks_andarchive_inverse_exact=True,
        all67_original_preambles_macros_controls_andsingle_native_pages_preserved=True,
        actual65_eachlanguage_two_offline_Julian_conditions_andshared_name_scope_preserved=True,
        all_measured_late_andnatural_activation_limits_preserved=True,full_goal_complete=False)
