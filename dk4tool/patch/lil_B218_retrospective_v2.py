"""Reconstruct one reviewed soft wrap, validate the complete block, then commit one files list."""
import json
from pathlib import Path
from collections import Counter
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.retrospective_SC2_reconstruction_v2 import reconstruct
from dk4tool.dialogue.lil_B218_retrospective_profile_v1 import contract,profile_for
from dk4tool.dialogue import lil_B218_retrospective_layout_v1 as codec
from scripts.retrospective_B218_final_paths_v7853 import proofs,FLAGS,measured_summary
CONFIG='translations/lil_B218_retrospective_release_v1.json'
PATHS=('/data/SC2.DK4',)
TARGET='DK4_MES_B218_R0027'
def load(path):return json.loads(Path(path).read_bytes())
def require(value,label):
    if not value:raise ValueError('B218 retrospective contract: '+label)
def check_dependencies(conf):
    for path,digest in conf['dependencies'].items():require(sha(Path(path).read_bytes())==digest,'dependency:'+path)
def commit_files(image,files):image.rom.files=files
def checked_plane(page):
    raw=Path(page['native_plane']).read_bytes()
    require(len(raw)==216*64 and sha(raw)==page['native_plane_sha256'],'complete native plane')
    return raw
def apply_release(image,baseline,config=CONFIG):
    conf=load(config);check_dependencies(conf)
    require(conf['format']=='dk4-B218-retrospective-release-v1' and len(conf['manuscripts'])==1 and conf['proofs']==proofs(),'sealed configuration')
    require(sha(baseline.source.read_bytes())==conf['canonical_ROM_sha256'],'canonical baseline')
    require(sha(Path(conf['parent_ROM']).read_bytes())==conf['parent_ROM_sha256'],'current parent')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'],'clean ROM')
    require({p:sha(v) for _,p,v in image.iter_files()}==conf['predecessor_file_hashes'] and
        {p:sha(v) for p,v in image.iter_components()}==conf['predecessor_component_hashes'],'complete predecessor files/components')
    arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    require(sha(arm)==conf['required_runtime_arm9_sha256'] and sha(common)==conf['required_runtime_common_sha256'],'exact runtime')
    clean=NdsImage.open(conf['clean_ROM']);mapping,seal=map(load,[conf['reference_map'],conf['reference_approval']])
    require(conf['required_map_flags']==FLAGS and mapping['format']=='dk4-B218-retrospective-source-relocation-map-v1'
        and all(mapping.get(k) is True for k in FLAGS),'sealed map flags')
    require(mapping['source_ROM']==conf['parent_ROM'] and mapping['source_ROM_sha256']==conf['parent_ROM_sha256']
        and mapping['clean_ROM_sha256']==conf['clean_ROM_sha256'] and mapping['file_path']==PATHS[0],'map identity')
    require(len(mapping['groups'])==1,'one original block')
    g=mapping['groups'][0]
    require(g['block']==218 and g['route']==2 and g['route_identity']=='Lil' and g['file_path']==PATHS[0]
        and g['original_entry_payload_offset']==8 and g['external_references_complete'],'original block entry')
    require((g['source_bytes'],g['source_logical_end'],g['source_tail_bytes'],g['target_bytes'],g['target_logical_end'],g['target_tail_bytes'])
        ==(1016,1016,0,1020,1018,2),'exact block extents')
    require(not g['relative_fixups'] and len(g['text_records'])==13 and len(g['all_target_commands'])==len(g['command_map'])==15,'all source objects andcommands')
    doc=load(conf['manuscripts'][0]);approved=load(doc['native_approved_manuscript'])
    require(seal['all13_individual_gates_andexact_references_sealed'] and seal['one_automatic_wrap_only_all13_words_retained']
        and seal['all15_commands_andboth_inverses_preserved'],'complete reference seal')
    require(seal['manuscript']==conf['manuscripts'][0] and seal['manuscript_sha256']==sha(Path(conf['manuscripts'][0]).read_bytes())
        and seal['reference_map_sha256']==doc['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()),'sealed document/map hashes')
    require(doc['records']==approved['records'] and doc['native_approved_manuscript_sha256']==g['approved_manuscript_sha256']==sha(Path(doc['native_approved_manuscript']).read_bytes()),'individually approved records')
    require(g['approved_manuscript']==doc['native_approved_manuscript'] and doc['file_path']==PATHS[0] and doc['block']==218,'approved identity')
    require(Path(doc['current_ROM']).resolve()==Path(conf['parent_ROM']).resolve() and doc['current_ROM_sha256']==conf['parent_ROM_sha256']
        and doc['current_ARM9_sha256']==sha(arm) and doc['current_COMMON_sha256']==sha(common),'document runtime identity')
    require(doc['source_ROM']==conf['clean_ROM'] and doc['source_ROM_sha256']==conf['clean_ROM_sha256'],'document clean source')
    require(doc['proof_paths']==conf['proofs'] and doc['proof_hashes']=={k:sha(Path(v).read_bytes()) for k,v in conf['proofs'].items()},'exact proof links')
    require(doc['encoder']=='dialogue-relocatable-v1' and doc['translation_policy']=='natural-dialogue-v2'
        and doc['target_locale']=='en-US' and not doc['formatting_review_pending'],'reviewed en-US policy')
    require(doc['all13_five_individual_gates_approved'] and doc['wording_retentions']==13 and doc['proposed_automatic_layout_revisions']==1
        and doc['unchanged_exact_compiled_plans']==12 and doc['new_credit']==doc['source_prose_andcompletion_credit_added']==0,'retrospective no duplicate credit')
    p={k:load(v) for k,v in conf['proofs'].items()}
    packet=p['source_context'];actual=p['actual'];view=p['actual_view'];policy=p['policy'];font=p['native_font'];stored=p['stored_controls']
    require(packet['candidate_sha256']==doc['current_ROM_sha256'] and packet['groups'][0]['command_map']==g['command_map']
        and packet['current_packet']==mapping['current_packet'],'complete source/current packet')
    require(packet['only_changed_record_ID']==TARGET and packet['other12_stored_speeches_exact'] and packet['all335_other_blocks_exact']
        and packet['complete_clean_andpredecessor_blocks_inverse_exact'] and packet['full_predecessor_archive_inverse_exact'],'whole source inverse scope')
    require(policy['positive_count']==len(policy['positive_records'])==13 and policy['negative_count']==len(policy['negative_cases'])==221
        and policy['all_negative_inputs_actually_changed_andrejected'] and all(c['actual_changed_input'] and c['error'] for c in policy['negative_cases']),'actual-changing policy checks')
    require(policy['all_protected_ROM_policy_ledger_andregistry_bytes_unchanged'] and policy['manuscript_sha256']==sha(Path(conf['proofs']['wording_review']).read_bytes()),'policy source binding')
    require(p['approval']['all13_individual_five_gates_approved'] and p['approval']['manuscript_sha256']==sha(Path(doc['native_approved_manuscript']).read_bytes()),'native approval receipt')
    require(font['current_original_processor_alignment_cases']==12 and len(font['pipelines'])==3 and len(font['native_planes'])==2
        and font['all_first_internal_andfinal_characters_complete_in_order'] and font['independent_current_font_planes_bounds_unique_cells_canaries_andcomplete_consumption'],'changed native display')
    require(font['original_static_selector']==font['actual_current_captain']==2 and font['zero_source_logical_compiled_macros'],'native selector andmacros')
    require(stored['fresh_changed_stored_alignments']==4 and stored['changed_parity_tail_zero_ink_complete_characters_bounds_andconsumption']
        and len(stored['other12_stored_bodies_exact'])==12 and len(stored['final_dispatch_cases'])==13,'final stored coverage')
    require(stored['all13_preambles_actor_voices_andzero_macro_bodies_bound'] and stored['both_sheets_directly_viewed'],'stored native views')
    require(len(stored['normal_terminal_seed_cases'])==25 and all(c['native_result'][0]==0 and c['native_result'][1]==c['initial_value_word']
        for c in stored['normal_terminal_seed_cases']) and stored['two_zero_storage_tail_bytes_separate_from_complete_four_byte_terminal'],'normal end andtail')
    require(stored['original_A000']['source_command_hex']=='00a0ffff2e000110' and stored['relocated_A000']['error'] is None,'original A000 boundary')
    require(p['loader']['whole_SC2_loads_andcache_hits']==336 and p['loader']['original_parent_modes']==672
        and p['loader']['all336_native_loads_cache_hits_and672_modes_pass'] and p['loader']['original_parent_both_modes_start_at_loaded_payload_plus8'],'original archive loader')
    caller=p['caller']
    require(caller['only_original24070_interpreter_call_andno_literal_alias'] and caller['original_VM_entry_offset']==8
        and len(caller['all15_clean_current_target_commands_bound'])==15,'bounded original caller')
    require([c['mapping'] for c in caller['all15_clean_current_target_commands_bound']]==g['command_map']
        and [c['current'] for c in caller['all15_clean_current_target_commands_bound']]==mapping['current_packet']['all_current_commands']
        and [c['target'] for c in caller['all15_clean_current_target_commands_bound']]==g['all_target_commands'],'all mapped source commands')
    require(actual['both_jobs_terminal_andreaped'] and actual['actual_frames']==32002 and actual['total_actual_pages']==26
        and actual['total_actual_complete_body_andheader_holds']==102 and actual['total_incomplete_sampled_holds']==0,'complete actual English scope')
    require(actual['previous_andproposed_English_only_no_new_Japanese_capture']
        and actual['initialized_Amsterdam_original_B22_prelude_not_natural_B218_activation_original_location_fullmechanics_routes_orhardware'],'honest actual scope')
    require(view['actual_proof_sha256']==sha(Path(conf['proofs']['actual']).read_bytes()) and view['all_eight_sheets_directly_viewed']
        and len(view['viewed_images'])==8 and len(view['all26_overview_panes_exact'])==26,'actual visual binding')
    require(all(sha(Path(v['path']).read_bytes())==v['sha256'] for v in view['viewed_images']),'viewed sheet bytes')
    summary=measured_summary(actual)
    require(summary==mapping['observed_comparison_contract']==seal['measured_comparison_contract'],'complete measured comparison contract')
    require(summary['exits']==[5975,5975] and summary['command_difference_rows']==8 and summary['duration_difference_rows']==0
        and summary['later_RGB_differences']==0 and summary['later_samples']==167,'measured late andtiming scope')
    require(actual['all24_original_command_results_andUI_equal'] and actual['all13_paired_upper_scene_portrait_andnameplate_RGB_equal']
        and len(actual['semantic_upper_portrait_nameplate_pairs'])==13 and all(all(v[k] for k in ['upper_scene','portrait','nameplate'])
            for v in actual['semantic_upper_portrait_nameplate_pairs']),'paired results scenes andheaders')
    require(len(actual['command_comparisons'])==24 and all(set(c['differing_fields'])<=set(['fixture_offset','decoded_length'])
        for c in actual['command_comparisons']),'all measured offset differences')
    require(len(actual['later_sampled_whole_frame_comparisons'])==167 and all(r['whole_RGB_equal'] for r in actual['later_sampled_whole_frame_comparisons']),'later sampled RGB')
    finals=actual['final_native_values'];require(len(finals)==2,'two final snapshots')
    require(actual['five_native_component_equality']=={k:finals[0]['components'][k]==finals[1]['components'][k] for k in finals[0]['components']}
        and all(actual['five_native_component_equality'].values()),'measured component equality')
    require(actual['final_whole_actor_equal']==(finals[0]['whole_actor_sha256']==finals[1]['whole_actor_sha256']) is True
        and actual['final_PRNG_seeds']==[v['seed'] for v in finals]==[3000421369,3000421369],'measured actors andRNG')
    rows=doc['records'];ids={r['id'] for r in rows};bindings=contract()['record_bindings']
    require(len(rows)==len(ids)==13 and ids==set(bindings) and Counter(r['source_selector'] for r in rows)=={2:6,21:7},'thirteen original speeches')
    oldrows={r['id']:r for r in p['original_final']['records']};words={r['id']:r for r in p['wording_review']['records']}
    sources={r['id']:r for r in packet['records']};glosses={r['id']:r for r in p['source_gloss']['records']}
    require(ids==set(oldrows)==set(words)==set(sources)==set(glosses),'whole exchange source set')
    groups={g['case']:g for g in actual['groups']}
    require(set(groups)=={'previous_English','proposed_English'} and len(actual['groups'])==2,'two English versions')
    fixtures={f['case']:f for f in p['fixtures']['fixtures']}
    require(set(fixtures)==set(groups),'fixture cases')
    for case,group in groups.items():
        require(group['actual_unique_speeches']==group['actual_complete_pages']==len(group['panels'])==13
            and {r['id'] for r in group['panels']}==ids and group['actual_complete_body_andheader_holds']==51
            and group['incomplete_sampled_holds']==0 and not group['unreturned_at_capture_end'],'all complete actual speeches')
        require(group['exit_frame']==5975 and group['normal_terminal_result']==[0,0] and len(group['command_pairs'])==24,'complete actual return')
        require(sha(Path(group['capture_report']).read_bytes())==group['capture_report_sha256']
            and sha(Path(group['observer_report']).read_bytes())==group['observer_report_sha256'],'actual report bytes')
        report=load(group['capture_report']);trace=load(group['observer_report'])
        require(report['ROM_sha256']==group['research_ROM_sha256']==fixtures[case]['research_ROM_sha256'] and report['frames']==16001
            and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and not report.get('battery_save_preloaded'),'actual cold boot')
        require(not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact'],'read-only original observation')
        require(sha(Path(fixtures[case]['research_ROM']).read_bytes())==group['research_ROM_sha256'],'actual fixture bytes')
        fixture_image=NdsImage.open(fixtures[case]['research_ROM'])
        fixture_blocks=IlnkContainer.parse(fixture_image.read_file(PATHS[0])).blocks
        fixture_hashes={n:sha(v) for n,v in enumerate(fixture_blocks)}
        trace_pairs=[]
        for tr in trace['rows']:
            location=tr['source']
            require(tr['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'] and location['classification']=='original_SC_cache'
                and location['route']==2 and location['whole_resident_payload_exact_ROM']
                and location['actual_sha256']==fixture_hashes[location['block']],'original resident trace source')
            if tr['kind']!='after_command' or location['block']!=22:continue
            entry=trace['rows'][tr['entry_row']]
            trace_pairs.append(dict(fixture_offset=entry['source']['instruction_offset'],word=entry['source']['first_word'],
                start=entry['frame'],returned=tr['frame'],duration=tr['frame']-entry['frame'],
                native_result=tr['result_words'],decoded_length=tr['decoded_length'],
                before_RNG=entry['original_RNG_seed'],after_RNG=tr['original_RNG_seed'],UI_after=tr['native_UI_request_words']))
        require(trace_pairs==group['command_pairs'],'actual measurements equal original trace')
        for measured,command in zip(group['command_pairs'],fixtures[case]['all24_stored_fixture_commands'],strict=True):
            require(measured['word']==command['word'] and measured['fixture_offset']==command['offset']
                and measured['decoded_length']==command['native_extent'],'all actual original command extents')
        text_refs={r['id']:r for r in fixtures[case]['original_text_records']}
        captures={r['frame']:r for r in report['frames_captured']}
        historical_planes={r['id']:r['complete_pages']['pages'][0] for r in p['original_stored']['records']}
        for panel in group['panels']:
            ident=panel['id'];fixture_text=text_refs[ident]
            interval=next(r for r in group['command_pairs'] if r['fixture_offset']==fixture_text['fixture_command_offset'])
            require(panel['interval']==interval and panel['source_selector']==fixture_text['source_selector'],'actual interval/source association')
            expected_plane=stored['changed_stored_pages']['pages'][0] if case=='proposed_English' and ident==TARGET else historical_planes[ident]
            require(panel['native_stored_plane']==expected_plane['native_plane']
                and panel['native_stored_plane_sha256']==expected_plane['native_plane_sha256']
                and checked_plane(expected_plane)==Path(panel['native_stored_plane']).read_bytes(),'actual final stored plane association')
            holds=panel['complete_body_andheader_holds']
            require(all(interval['start']+20<h['frame']<interval['returned']-4
                and h['capture']==captures[h['frame']]['path'] and h['sha256']==captures[h['frame']]['PNG_sha256'] for h in holds),'actual complete hold/report association')
            require(panel['source_selector'] in [2,21] and panel['speaker_name']=={2:'Lil Argot',21:'Ian Dukov'}[panel['source_selector']]
                and panel['native_pages']==1 and holds and not panel['incomplete_sampled_body_holds'],'actual source speaker andpage')
            require(all(h['complete_native_body_black_gray_andnameplate_masks_equal'] and sha(Path(h['capture']).read_bytes())==h['sha256'] for h in holds),'complete actual native masks')
            require(sha(Path(panel['native_stored_plane']).read_bytes())==panel['native_stored_plane_sha256'],'actual expected native plane')
    for c,previous,proposed in zip(actual['command_comparisons'],groups['previous_English']['command_pairs'],groups['proposed_English']['command_pairs'],strict=True):
        require(c['previous']==previous and c['proposed']==proposed
            and c['differing_fields']==[k for k in previous if previous[k]!=proposed[k]],'complete command comparison association')
    require(sum(c['previous']['duration']!=c['proposed']['duration'] for c in actual['command_comparisons'])==actual['duration_difference_rows']
        and sum(bool(c['differing_fields']) for c in actual['command_comparisons'])==actual['command_difference_rows'],'computed timing/offset counts')
    require(all(c['previous']['native_result']==c['proposed']['native_result'] and c['previous']['UI_after']==c['proposed']['UI_after']
        for c in actual['command_comparisons']),'measured original result/UI equality')
    panels={r['id']:r for r in groups['proposed_English']['panels']}
    source=image.read_file(PATHS[0]);japanese=clean.read_file(PATHS[0]);archive=conf['archives'][0]
    require(len(conf['archives'])==1 and archive['file_path']==PATHS[0] and sha(source)==mapping['source_archive_sha256']==archive['source_sha256']
        and sha(japanese)==archive['clean_sha256'] and sha(baseline.read_file(PATHS[0]))==archive['canonical_sha256'],'source clean canonical archives')
    require(image.read_file('/data/EV2.DK4')==clean.read_file('/data/EV2.DK4'),'unchanged source EV2 actions')
    blocks=IlnkContainer.parse(source).blocks;cleanblocks=IlnkContainer.parse(japanese).blocks
    require(len(blocks)==len(cleanblocks)==336 and blocks[218][:8].hex()==g['source_header_hex'],'source block/header')
    for row in rows:
        ident=row['id'];b=bindings[ident];s=sources[ident];old=oldrows[ident];w=words[ident]
        require(row['file_path']==PATHS[0] and row['block']==218 and row['source_selector']==b['source_selector'],'record identity:'+ident)
        require(row['source_hex']==s['source_hex']==b['compiler_source_hex']==glosses[ident]['source_hex']
            and row['current_hex']==s['current_hex'] and row['source_reference']==s['source_reference']==b['source_reference']
            and row['current_reference']==s['current_reference']==b['current_reference'],'exact source/current:'+ident)
        require(row['source_Japanese']==old['source_Japanese'] and row['source_meaning']==old['source_meaning']
            and row['context']==old['context'] and row['localization_note']==old['localization_note'],'whole original meaning/context:'+ident)
        require(row['fresh_retrospective_source_context']==w['fresh_retrospective_source_context']
            and row['retrospective_wording_reason']==w['retrospective_wording_reason'] and row['retrospective_wording_reason'].strip()
            and row['retrospective_wording_decision']=='retain-wording','individual wording retention:'+ident)
        require(row['english']==old['english']==w['english']==b['planning_record']['english']
            and row['review']=={k:True for k in ['source','context','localization','naturalness','formatting']},'reviewed unchanged wording:'+ident)
        require(row['retrospective_layout_decision']==('revise-automatic-soft-wrap' if ident==TARGET else 'retain-exact-compiled-plan'),'one layout revision:'+ident)
        prof=profile_for(arm,blocks[218],ident);encoded=codec.encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],prof)
        qa=codec.audit_relocatable_dialogue_record(bytes.fromhex(row['source_hex']),row['english'],prof)
        require(encoded.encoded.hex()==row['compiled_hex']==b['compiled_hex'] and qa==row['base_QA_report'],'exact compiled/QA:'+ident)
        require(row['qa_waivers']==[] and row['qa_waiver_reason'] is None and row['row_count_reason']==b['row_count_reason']
            and row['native_page_count']==1 and row['actual_record_observed']
            and row['actual_complete_body_andheader_holds']==len(panels[ident]['complete_body_andheader_holds']),'individual native/actual reasons:'+ident)
    targetref=next(r for r in g['text_records'] if r['id']==TARGET)
    require(targetref==stored['changed_stored_target'] and targetref['parity_space_added'],'exact changed stored target')
    body=bytes.fromhex(targetref['target_hex'])[1:];compiled=bytes.fromhex(targetref['compiled_hex'])[1:]
    require(body==compiled+b' ' and len(stored['changed_stored_pipeline']['cases'])==4
        and all(c['output_hex']==body.hex() for c in stored['changed_stored_pipeline']['cases']),'zero-ink stored input')
    proposed=next(v for v in font['native_planes'] if v['version']=='proposed-compiled')
    require(len(proposed['pages'])==len(stored['changed_stored_pages']['pages'])==1
        and checked_plane(proposed['pages'][0])==checked_plane(stored['changed_stored_pages']['pages'][0]),'changed complete ink')
    unchanged={r['id']:r for r in stored['other12_stored_bodies_exact']};historical={r['id']:r for r in p['original_stored']['records']}
    for ref in g['text_records']:
        if ref['id']==TARGET:continue
        require(ref['old_hex']==ref['target_hex']==unchanged[ref['id']]['exact_previous_andcurrent_stored_hex']
            ==historical[ref['id']]['final_target_hex'],'unchanged stored body:'+ref['id'])
    target=reconstruct(blocks[218],cleanblocks[218],g,mapping['current_packet'],rows,[])
    targetblocks=list(blocks);targetblocks[218]=target;payload=IlnkContainer(targetblocks).to_bytes()
    require(sha(payload)==mapping['target_archive_sha256']==archive['target_sha256'],'complete target archive')
    require(sha(Path(conf['reference_ROM']).read_bytes())==conf['reference_ROM_sha256']==doc['reference_research_ROM_sha256'],'reference ROM identity')
    reference=NdsImage.open(conf['reference_ROM'])
    require(payload==reference.read_file(PATHS[0]) and [i for i,(a,b) in enumerate(zip(blocks,targetblocks,strict=True)) if a!=b]==[218],'only B218 changes')
    require(all(reference.read_file(p)==v for _,p,v in image.iter_files() if p not in PATHS)
        and all(reference.read_file(p)==v for p,v in image.iter_components()),'all unowned files/components exact')
    changes=[dict(id=TARGET,file_path=PATHS[0],block=218,old_offset=targetref['old_offset'],new_offset=targetref['new_offset'])]
    files=list(image.rom.files);index=image.path_map()[PATHS[0]];files[index]=payload
    require([i for i,(a,b) in enumerate(zip(image.rom.files,files,strict=True)) if a!=b]==[index],'one archive file slot')
    commit_files(image,files)
    return dict(manuscripts=conf['manuscripts'],reference_map=conf['reference_map'],changed_records=changes,
        files=[dict(file_path=PATHS[0],source_sha256=sha(source),target_sha256=sha(payload),changed_records=changes)],
        reviewed_records=13,wording_retentions=13,automatic_wrap_revisions=1,unchanged_stored_records=12,
        one_files_list_commit_after_all_gates=True,all15_original_commands13_preambles_zero_macros_andboth_inverses_preserved=True,
        all335_other_blocks_files_components_andmeasured_actual_limits_preserved=True,
        no_duplicate_editorial_credit=True,full_goal_complete=False)
