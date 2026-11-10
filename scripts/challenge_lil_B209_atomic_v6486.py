"""Challenge independent semantic guards with digests deliberately bypassed; reject before writes."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B209_editorial_v3 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B209_atomic_v6486');POS=Path('work/analysis/lil_B209_atomic_v6485c')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();positive=read(POS/'positive_receipt.json');config=Path(positive['config']);conf=read(config);parent=Path(positive['parent_ROM']);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');assert sha(config.read_bytes())==positive['config_sha256'] and sha(parent.read_bytes())==positive['parent_ROM_sha256']
    doc,mapfile,seal=[Path(conf[k]) for k in ['manuscript','reference_map','reference_approval']];d=read(doc);font,stored,policy,approval,names,actual,view=[Path(d[k]) for k in ['native_font_proof','native_stored_proof','native_policy_validation','native_approval','speaker_names_review','actual_English_proof','actual_English_view']]
    tests=[]
    def add(label,path,edit):tests.append((label,Path(path),edit))
    def setroot(label,path,key,value):add(label,path,lambda v,k=key,x=value:v.update({k:x}))
    def setrow(label,key,value,index=0):add(label,doc,lambda v,k=key,x=value,i=index:v['records'][i].update({k:x}))
    for k in ['source_SC2_sha256','canonical_SC2_sha256','clean_SC2_sha256','clean_ROM_sha256','required_runtime_arm9_sha256','required_runtime_common_sha256','target_SC2_sha256','reference_ROM_sha256']:setroot('wrong-'+k,config,k,'0'*64)
    for k in owned.FLAGS:setroot('lost-map-'+k,mapfile,k,False)
    for k,x in [('translation_policy','literal'),('target_locale','en-GB'),('encoder','dialogue-fixed-v1'),('formatting_review_pending',True),('actual_objects',20),('actual_pages',22),('offline_only_objects',0),('all207_name_alias_review_and_full_four_storyline_editorial_objective_open',False)]:setroot('manuscript-'+k,doc,k,x)
    add('missing-record',doc,lambda v:v['records'].pop());add('duplicate-record',doc,lambda v:v['records'].__setitem__(1,deepcopy(v['records'][0])))
    for k in ['source','context','localization','naturalness','formatting']:add('lost-individual-'+k,doc,lambda v,k=k:v['records'][0]['review'].update({k:False}))
    for label,key,value,i in [('empty-speaker','speaker','',0),('invented-speaker-name','speaker','Lord Yukihisa',0),('invented-Jacques-middle-name','speaker','Jam Jacques Ludwyan',3),('unmapped-D0-label','speaker','First Mate',5),('missing-context','context','',0),('missing-source-meaning','source_meaning','',0),('lost-localization-note','localization_note','',0),('lost-whole-exchange-review','full_exchange_read_aloud_review',False,0),('wrong-static-selector','source_selector',13,0),('wrong-D0-selector','source_selector',151,5),('lost-full-preamble','source_complete_preamble_hex','0040ffff000d',0),('false-retention-decision','editorial_decision','retain-wording',0),('lost-retention-justification','retention_reason','',5),('false-actual-credit','actual_record_observed',True,5),('all-native-labelled-actual','native_plane_verified_not_actual_English_gameplay',False,5),('taller-physical-viewport','original_physical_native_rows_per_page',8,0),('lost-continuation','native_page_count',1,0),('altered-capacity','native_profile_maximum_total_rows',4,0),('blanket-weak-wrap-waiver','qa_waivers',['weak-line-ending'],0),('lost-rowcount-reason','qa_waiver_reason','',0),('lost-ordinary-boundaries','reviewed_ordinary_boundaries',[],0),('serialize-virtual-D0','virtual_formatter_selector_not_stored_in_actor_style_body',False,5),('bad-compiled-byte','compiled_hex','d0',0),('wrong-current-index','current_record_index',28,0)]:setrow(label,key,value,i)
    for side in ['source','current']:add('wrong-'+side+'-reference',doc,lambda v,s=side:v['records'][0][s+'_reference'].update(offset=334))
    original=d['records'][0]['english']
    for label,text in [('authored-LB',original+'{LB}'),('authored-ALIGN',original+'{ALIGN@2}'),('authored-PAD',original+'{PAD}'),('raw-newline',original+'\n'),('lost-hearsay',original.replace('are said to be','are')),('invented-Tokugawa-intent',original.replace('efforts are afoot','Tokugawa has ordered efforts')),('invented-macro',original+'{MACRO:FI}')]:setrow(label,'english',text)
    setrow('lost-tentative-interest','english','{SPEAKER:02}We will find it.',4)
    for k,x in [('complete_native_pages',21),('logical_compiled_input_alignment_cases',159),('all_first_internal_final_visible_glyphs_in_order_unique_cells_and_bounds',False),('each216x64_plane_exact_independent_current_font_and_all_canaries',False),('continuation_first_row_retains_original6px_guard_indent',False),('D0_fallback151_unchanged',False)]:setroot('font-'+k,font,k,x)
    add('font-lost-page',font,lambda v:v['records'][0]['pages'].pop());add('lost-final-glyph',font,lambda v:v['records'][0].update(all_visible_first_internal_final_characters_in_order=False))
    for k,x in [('final_stored_alignment_cases',79),('fresh_parity_tail_records',0),('no_extra_blank_page_or_lost_leading_trailing_internal_glyph',False),('all15_style_bodies_exclude_virtual_D0_and_have_independent_terminators',False)]:setroot('stored-'+k,stored,k,x)
    add('stored-tail-ink',stored,lambda v:v['records'][0].update(unchanged_words_glyphs_page_count_and_zero_ink_tail=False));add('wrong-stored-body',stored,lambda v:v['records'][0].update(final_target_hex='0c'))
    for k,x in [('negative_count',53),('no_unwaived_warning_or_error',False),('source_bound_ordinary_boundary_rules_not_global_waivers',False)]:setroot('policy-'+k,policy,k,x)
    add('lost-rowcount-reason-set',policy,lambda v:v['row_count_reasons'].pop());add('negative-case-accepted',policy,lambda v:v['negative_cases'][0].update(rejected=False))
    for k,x in [('original_viewport',[216,128]),('name_literal_alignments',111),('actual_unique_objects',20),('offline_only_objects',0),('original_event209_dependency85_not_naturally_selected',False)]:setroot('approval-'+k,approval,k,x)
    for k,x in [('full_source_signature','白樹行尚'),('retained_current_full_signature','Yukihisa Shiraki'),('fallback151_progressive_Sailor_full_catalogue_Retainer_not_global_editorial_approval',False),('Jam_actual_header_unvisited_native_plane_complete',False),('no_new_user_approval_or_original_Latin_artwork_claim',False),('all207_names_aliases_earlier_consumers_and_full_editorial_goal_open',False)]:setroot('names-'+k,names,k,x)
    add('alter-retained-Jack-field',names,lambda v:v['proper_name_retentions'][1].update(catalogue='Jam Jacques Ludwyan'));add('global-fallback-substitution',names,lambda v:v['fallback151_consumer_specific_open_lead'].update(progressive='Retainer'))
    for k in ['command_timing_differences','command_RNG_differences','command_duration_changes','later_same_frame_RGB_differences']:add('erase-measured-'+k,actual,lambda v,k=k:v[k].pop())
    for k,x in [('actual_unique_objects',20),('explicit_Jam_R65_and13_other_stored_style_bodies_unvisited',False),('source_exit_frame',4774),('ordinary_original_A_schedule_identical_to_source',False),('whole_RAM_final_PRNG_and_future_simulation_equivalence_unproven',False)]:setroot('actual-'+k,actual,k,x)
    for k,x in [('visual_review_pending',True),('no_same_frame_or_whole_RGB_equivalence_claim_from_semantic_pairs',False),('later_older_record_technical_reaudit_retains_all_measured_differences',False),('no_broad_final_RAM_future_simulation_or_complete_causal_equivalence_claim',False),('final_PRNG_seeds',[1095690386,1095690386]),('final_calendar_ticks',[2401,2401])]:setroot('view-'+k,view,k,x)
    add('lost-semantic-region-pair',view,lambda v:v['upper_scene_and_portrait_semantic_pairs'].pop())
    add('wrong-target-extent',mapfile,lambda v:v['blocks'][0].update(target_bytes=1334));add('wrong-target-logical-end',mapfile,lambda v:v['blocks'][0].update(target_logical_end=1336));add('wrong-target-tail',mapfile,lambda v:v['blocks'][0].update(target_tail_bytes=0));add('invented-menu',mapfile,lambda v:v['blocks'][0]['choice_commands'].append({}))
    add('lost-typed-object',mapfile,lambda v:v['blocks'][0]['actor_style_commands'].pop());add('wrong-style-table-slot',mapfile,lambda v:v['blocks'][0]['actor_style_commands'][0]['new_style_offsets'].__setitem__(7,0));add('wrong-typed-header',mapfile,lambda v:v['blocks'][0]['actor_style_commands'][0].update(target_hex='0041'))
    add('lost-source-alias',doc,lambda v:v['records'][7].update(style_indices=[2]));add('wrong-native-command-extent',mapfile,lambda v:v['blocks'][0]['mapped_native_commands'][0].update(new_native_extent=316))
    add('lost-relative-site',mapfile,lambda v:v['blocks'][0]['relative_skip_fixups'].pop());add('wrong-relative-span',mapfile,lambda v:v['blocks'][0]['relative_skip_fixups'][1].update(new_span=396));add('wrong-complete-end',mapfile,lambda v:v['blocks'][0]['complete_end_map'].update(target_offset=1332));add('lost-native-branch-value',mapfile,lambda v:v['blocks'][0]['target_native_skip_cases'].pop());add('wrong-original-branch-extent',mapfile,lambda v:v['blocks'][0]['target_native_skip_cases'][0].update(extent=4))
    add('wrong-event-dependency',conf['entry'],lambda v:v['selected_B209_source_events'][0].update(must_be_completed=[]));setroot('forced-D0-fallback',conf['controls'],'predicate_type2_Boolean0_preserved',False)
    ROOT.mkdir(parents=True);results=[];original_load=owned.load
    for number,(label,path,edit) in enumerate(tests,1):
        value=deepcopy(read(path));before=deepcopy(value);edit(value);assert value!=before,label;image=NdsImage.open(parent);initial=image.read_file(owned.PATH);calls=[];replace=image.replace_file
        def tracked(*args,**kwargs):calls.append(args[0]);return replace(*args,**kwargs)
        def injected(p):
            v=deepcopy(value) if Path(p)==path else original_load(p)
            if Path(p)==config:v['dependencies']={}
            return v
        image.replace_file=tracked;owned.load=injected
        try:
            try:owned.apply_release(image,baseline,config)
            except (ValueError,AssertionError) as exc:reason=str(exc) or type(exc).__name__
            else:raise RuntimeError('Negative unexpectedly accepted:'+label)
        finally:owned.load=original_load
        assert not calls and image.read_file(owned.PATH)==initial,label
        results.append(dict(case=label,rejected=True,reason=reason,dependency_digests_bypassed_to_challenge_semantics=True,no_archive_mutation=True))
        if number%25==0:print(f'{number}/{len(tests)} semantic rejection cases pass.',flush=True)
    save(ROOT/'negative_cases.json',dict(cases=results,count=len(results),all_rejected_before_archive_mutation=True,producer_sha256=sha(Path(__file__).read_bytes())))
    save(ROOT/'atomic_validation_receipt.json',dict(**{k:positive[k] for k in ['config','config_sha256','positive_proof','positive_proof_sha256','parent_ROM','parent_ROM_sha256','positive_records']},negative_cases=str(ROOT/'negative_cases.json'),negative_cases_sha256=sha((ROOT/'negative_cases.json').read_bytes()),negative_count=len(results),all_negatives_reject_before_mutation=True,all20_records_reconstructed_with_one_archive_write=True,source1148_full_inverse_and_all_other_components_exact=True,full_goal_complete=False));print(f'B20920-object atomic validation passed:{len(results)} independent semantic negatives reject before the sole archive write. Registration next.',flush=True)
