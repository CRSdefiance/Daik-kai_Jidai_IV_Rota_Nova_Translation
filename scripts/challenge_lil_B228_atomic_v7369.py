"""Challenge B228 independent semantics with file digests deliberately bypassed."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B228_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B228_atomic_v7369');POS=Path('work/analysis/lil_B228_atomic_v7368')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    positive=read(POS/'positive_receipt.json');config=Path(positive['config']);conf=read(config);parent=Path(positive['parent_ROM'])
    assert sha(config.read_bytes())==positive['config_sha256'] and sha(parent.read_bytes())==positive['parent_ROM_sha256']
    baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');doc,mapfile,seal=[Path(conf[k]) for k in ['manuscript','reference_map','reference_approval']];d=read(doc);approved=Path(d['native_approved_manuscript']);paths={k:Path(d[k]) for k in ['native_font_proof','native_stored_proof','native_policy_validation','native_approval','speaker_name_review','actual_English_proof','actual_English_view','relocated_control_proof','later_scope_proof']};tests=[]
    def add(label,path,edit):tests.append((label,Path(path),edit))
    def root(label,path,key,value):add(label,path,lambda v,k=key,x=value:v.update({k:x}))
    def row(label,key,value,index=0):add(label,doc,lambda v,k=key,x=value,i=index:v['records'][i].update({k:x}))
    for k in ['source_SC2_sha256','canonical_SC2_sha256','clean_SC2_sha256','clean_ROM_sha256','required_runtime_arm9_sha256','required_runtime_common_sha256','target_SC2_sha256','reference_ROM_sha256']:root('wrong-'+k,config,k,'0'*64)
    for k in owned.FLAGS:root('lost-map-'+k,mapfile,k,False)
    for k,x in [('translation_policy','literal'),('target_locale','en-GB'),('encoder','dialogue-fixed-v1'),('formatting_review_pending',True),('actual_objects',12),('actual_pages',12),('actual_complete_body_holds',50),('actual_complete_name_holds',50),('offline_only_objects',1),('full207_name_role_alias_andearlier_review_open',False),('source_middle_field_not_invented_surname_rank_or_nationality',False),('full_goal_complete',True)]:root('manuscript-'+k,doc,k,x)
    add('missing-record',doc,lambda v:v['records'].pop());add('duplicate-record',doc,lambda v:v['records'].__setitem__(1,deepcopy(v['records'][0])))
    for i,r in enumerate(d['records']):add('lost-formatting-'+r['id'],doc,lambda v,i=i:v['records'][i]['review'].update(formatting=False))
    for k in ['source','context','localization','naturalness']:add('lost-individual-'+k,doc,lambda v,k=k:v['records'][0]['review'].update({k:False}))
    retain=next(i for i,r in enumerate(d['records']) if r['editorial_decision']=='retain-wording')
    for label,k,x,i in [('empty-speaker','speaker','',0),('invented-rank','speaker','King Samwell',0),('lost-context','context','',0),('lost-meaning','source_meaning','',0),('lost-localization','localization_note','',0),('lost-finding','editorial_finding','',0),('lost-whole-exchange','full_exchange_read_aloud_review',False,0),('wrong-actor','source_selector',2,0),('lost-preamble','source_complete_preamble_hex','0040ffff0002',0),('false-revision','editorial_decision','revise',0),('lost-retention-reason','retention_reason','',retain),('false-actual','actual_record_observed',False,0),('false-offline-status','native_plane_verified_not_actual_English_gameplay',True,0),('taller-physical-page','original_physical_native_rows_per_page',8,0),('extra-page','native_page_count',2,0),('changed-capacity','native_profile_maximum_total_rows',8,0),('blanket-wrap-waiver','qa_waivers',['encoding'],0),('lost-boundaries','reviewed_ordinary_boundaries',[],2),('bad-compiled','compiled_hex','a241',0),('wrong-index','current_record_index',35,0),('authored-layout','no_manual_line_break_padding_or_alignment_authored',False,0)]:row(label,k,x,i)
    for side in ['source','current']:add('wrong-'+side+'-reference',doc,lambda v,s=side:v['records'][0][s+'_reference'].update(offset=14))
    for label,text in [('manual-LB',d['records'][0]['english']+'{LB}'),('new-macro',d['records'][0]['english']+'{MACRO:FI}'),('invented-relationship',d['records'][0]['english']+' My uncle!')]:row(label,'english',text)
    for key in ['source_tail_bytes','source_logical_end','target_tail_bytes','target_logical_end']:add('wrong-'+key,mapfile,lambda v,k=key:v['blocks'][0].update({k:v['blocks'][0][k]+2}))
    for key in ['complete_end_map','original_A000_map']:add('lost-'+key,mapfile,lambda v,k=key:v['blocks'][0][k].clear())
    for key in ['original_C200_map','original_630B_map']:add('invented-'+key,mapfile,lambda v,k=key:v['blocks'][0][k].append(dict(source_offset=80)))
    add('A000-wrong-operand',mapfile,lambda v:v['blocks'][0]['original_A000_map'][0].update(source_hex='00a0ffff47000110'))
    add('end-wrong-target',mapfile,lambda v:v['blocks'][0]['complete_end_map'][0].update(target_offset=742))
    add('stored-reference-wrong',mapfile,lambda v:v['blocks'][0]['text_records'][0].update(new_offset=14))
    add('command-extent-wrong',mapfile,lambda v:v['blocks'][0]['command_map'][0].update(new_extent=2))
    for k in ['complete_native_pages','logical_compiled_input_alignment_cases']:root('font-'+k,paths['native_font_proof'],k,0)
    for k in ['all13_single_original_four_row_pages','all13_complete_prose_paragraphs','all_first_internal_final_visible_glyphs_in_order_unique_cells_and_bounds','each216x64_plane_exact_independent_current_font_and_all_canaries','all_original_current_font_renderer_instructions_verified','original_pair_phase_and_guards_bound_without_new_substitutions','zero_source_and_compiled_FI_FA_FO_no_substitutions_added','only_original_static_selectors2_22']:root('font-'+k,paths['native_font_proof'],k,False)
    for k in ['stored_alignment_cases','zero_ink_parity_tail_count','complete_native_pages','exact_reused_alignment_cases']:root('stored-'+k,paths['native_stored_proof'],k,0)
    root('stored-false-fresh',paths['native_stored_proof'],'fresh_alignment_cases',4)
    for k in ['all_final_stored_targets_equal_reviewed_complete_native_ink','all_bounds_canaries_pair_phase_and_zero_macros_pass']:root('stored-'+k,paths['native_stored_proof'],k,False)
    root('policy-rejection-count',paths['native_policy_validation'],'negative_count',61);add('policy-negative-accepted',paths['native_policy_validation'],lambda v:v['negative_cases'][0].update(rejected=False))
    root('policy-QA-weakened',paths['native_policy_validation'],'all_base_QA_diagnostics_preserved_zero_warning_waivers',False)
    add('policy-lost-row-reason',paths['native_policy_validation'],lambda v:v['row_count_reasons'].pop(next(iter(v['row_count_reasons']))))
    for k in ['revision_count','retention_count','native_pages','logical_compiled_alignments','stored_alignments','zero_ink_parity_tails','name_alignments','layout_rejections','actual_objects','complete_body_holds','complete_name_holds']:root('approval-'+k,paths['native_approval'],k,0)
    for k in ['both_actual_final_English_personal_names_complete','two_contextual_progressive_names_retained_no_assets_or_duplicate_credit','source_middle_field_not_invented_surname_rank_or_nationality','full207_name_role_alias_andearlier_name_review_open','no_new_name_or_dialogue_credit','full_catalogue_UI_unvisited']:root('names-'+k,paths['speaker_name_review'],k,False)
    for i in range(2):add('name-invented-identity-'+str(i),paths['speaker_name_review'],lambda v,i=i:v['records'][i].update(english='King Samwell'))
    a=paths['actual_English_proof']
    for k in ['actual_unique_speeches','actual_native_pages','actual_complete_body_holds','actual_complete_name_holds','source_exit_frame','normal_port_sample_frame']:root('actual-'+k,a,k,0)
    root('actual-terminal',a,'normal_terminal_result',[0,1]);root('actual-partial',a,'incomplete_sampled_body_holds',1)
    for k in ['all13_single_original_native_pages_verified','initialized_B22_not_natural_event228_original_location_earned_progress_full_effects_route_orhardware','no_roles_roster_funds_conditions_RNG_results_RAM_code_battery_or_savestate_forced','no_full_RAM_every_intermediate_frame_future_sequence_broad_simulation_orcausal_claim','full207_name_role_alias_andearlier_editorial_scope_open','both_source_personal_names_preserved','all_following_resident_payloads_verified_against_actual_SC0_to_SC3_bank']:root('actual-'+k,a,k,False)
    add('actual-lost-command-difference',a,lambda v:v['command_comparison_differences'].append(dict(invented_difference=True)));add('actual-lost-duration',a,lambda v:v['command_duration_changes'].append(dict(invented_difference=True)))
    for i,r in enumerate(d['records']):
        add('actual-incomplete-body-'+r['id'],a,lambda v,i=i:v['actual_panels'][i]['complete_body_holds'][0].update(complete_independent_native_body_black_gray_all_glyphs_equal=False))
        add('actual-incomplete-name-'+r['id'],a,lambda v,i=i:v['actual_panels'][i]['complete_name_holds'][0].update(complete_name_and_blank_guards_equal=False))
    root('view-pending',paths['actual_English_view'],'visual_review_pending',True)
    for k in ['all13_complete_preambles_voices_andzero_macro_bodies_bound','zero_original_orinvented_FI_FA_FO','normal_state0_retains_existing_value_word_in_all25_cases','original_normal_end740_four_bytes_andtarget_no_tail_preserved','all15_commands_no_predicate_relative_typed_style_orpicture_assumptions','opaque_A000_effects_bridged_not_fully_explained']:root('control-'+k,paths['relocated_control_proof'],k,False)
    root('later-captain-changed',paths['later_scope_proof'],'captain_IDs',[0,2]);root('later-seed-changed',paths['later_scope_proof'],'final_PRNG_seeds',[0,2548610151]);add('later-RGB-difference-erased',paths['later_scope_proof'],lambda v:v['later_sampled_RGB_differences'].append(dict(frame=6070,whole_RGB_equal=False)));root('later-broad-claim',paths['later_scope_proof'],'no_full_RAM_future_sequence_broad_simulation_or_complete_causal_claim',False)
    row('wrong-source-voice','source_voice_class',7,0)
    ap=read(a);runplan=next(Path(p) for p in ap['evidence'] if Path(p).name=='run_plan.json');fixture=Path(ap['fixture'])
    root('B228-explicit-entry-scope-lost',runplan,'source_event228_not_naturally_selected',False)
    root('B228-displayed-block-misidentified',runplan,'displayed_original_source_block',227)
    add('B228-fixture-block-misidentified',fixture,lambda v:v['fixtures'][0].update(source_block=227))
    root('B228-fixture-scope-lost',fixture,'initialized_Amsterdam_B22_not_natural_event228_location_or_earned_progress',False)
    root('Samwell-catalogue-global-approval-invented',paths['speaker_name_review'],'progressive_headers_only_not_full_catalogue_wording_approval',False)
    add('Samwell-catalogue-middle-approved',paths['speaker_name_review'],lambda v:v['records'][1].update(catalogue_wording_editorially_approved=True))
    add('Samwell-catalogue-middle-romanized-without-review',paths['speaker_name_review'],lambda v:v['records'][1].update(catalogue_current='Samwell da Khan'))
    add('Samwell-source-middle-invented',paths['speaker_name_review'],lambda v:v['records'][1]['source_fields'][2].update(Japanese='カーン'))
    add('Samwell-current-middle-bytes-changed',paths['speaker_name_review'],lambda v:v['records'][1]['source_fields'][2].update(current_terminated_hex='646100'))
    getters=Path(d['current_consumer_proof']);add('Samwell-full-getter-invented',getters,lambda v:v['native_four_distinct_name_consumers']['rows'][3].update(text='Samwell da Khan'))
    item=Path(d['source_named_item_binding'])
    for k in ['Samwell_mixed_Japanese_full_catalogue_wording_not_editorially_approved','candidate_spelling_not_shipped_or_globally_approved','source_named_shield_not_runtime_FI_substitution','current_Armadillo_Hide_asset_andharder_than_iron_source_meaning_bound','no_item_or_actor_asset_change_or_duplicate_credit','no_inventory_card_orcomplete_item_mechanic_approval','full207_name_role_alias_andSamwell_middle_consumer_review_remains_open']:root('item-scope-'+k,item,k,False)
    for k,x in [('record_ID','DK4_ITEM_POINTER_051'),('Japanese','アルマジロの皮'),('English','Armadillo Steel Hide'),('source_terminated_hex','834100'),('current_terminated_hex','41726d6f7200'),('pointer_field',0),('current_storage_offset',0),('source_storage_offset',0)]:add('item-field-'+k,item,lambda v,k=k,x=x:v['source_named_item'].update({k:x}))
    add('middle-binding-romaji-invented',item,lambda v:v['Samwell_middle_field'].update(current_English='da'))
    add('effect-consumer-native-rows-lost',paths['relocated_control_proof'],lambda v:v['relocated_A000']['rows'].clear())
    add('effect-consumer-opaque-bridge-lost',paths['relocated_control_proof'],lambda v:v['relocated_A000']['opaque_effect_bridges'].clear())
    assert len(tests)==len({t[0] for t in tests}) and len(tests)>=100;ROOT.mkdir(parents=True);results=[];original_load=owned.load
    save(ROOT/'challenge_plan.json',dict(negative_count=len(tests),cases=[dict(case=l,target=str(p)) for l,p,e in tests],dependency_digests_deliberately_bypassed=True,positive_receipt_sha256=sha((POS/'positive_receipt.json').read_bytes())))
    for i,(label,path,edit) in enumerate(tests):
        original=read(path);altered=deepcopy(original);edit(altered);assert altered!=original,label
        def injected(p):
            key=Path(p).resolve()
            if key==config.resolve():
                value=deepcopy(altered if key==path.resolve() else conf);value['dependencies']={};return value
            if key==path.resolve():return deepcopy(altered)
            if path.resolve()==doc.resolve() and key==approved.resolve():
                value=original_load(p);value['records']=deepcopy(altered['records']);return value
            return original_load(p)
        image=NdsImage.open(parent);before=image.read_file(owned.PATH);writes=[]
        def forbidden(*args,**kwargs):writes.append(args[0]);raise RuntimeError('Archive write attempted in '+label)
        image.replace_file=forbidden;owned.load=injected
        try:
            try:owned.apply_release(image,baseline,config)
            except (ValueError,AssertionError) as e:results.append(dict(case=label,target=str(path),rejected=True,error=str(e),archive_writes=0,dependency_digests_deliberately_bypassed=True,approved_record_mirror_for_deeper_semantics=path.resolve()==doc.resolve()))
            else:raise RuntimeError('Unsafe alteration accepted:'+label)
        finally:owned.load=original_load
        assert not writes and image.read_file(owned.PATH)==before,label
        if (i+1)%25==0:save(ROOT/'partial_negative_cases.json',results);print(f'{i+1}/{len(tests)} independent rejections pass',flush=True)
    cases=ROOT/'negative_cases.json';save(cases,results)
    save(ROOT/'atomic_validation_receipt.json',dict(config=str(config),config_sha256=sha(config.read_bytes()),positive_proof=positive['positive_proof'],positive_proof_sha256=positive['positive_proof_sha256'],parent_ROM=str(parent),parent_ROM_sha256=positive['parent_ROM_sha256'],positive_records=13,negative_cases=str(cases),negative_cases_sha256=sha(cases.read_bytes()),negative_count=len(results),all_negatives_reject_before_mutation=True,all13_actual13_pages51_body51_headers_bound=True,original_A00025_ends_and_explicit_comparison_limits_bound=True,full_goal_complete=False));print(dict(positive_records=13,negative_count=len(results),all_before_mutation=True,credit=0),flush=True)
