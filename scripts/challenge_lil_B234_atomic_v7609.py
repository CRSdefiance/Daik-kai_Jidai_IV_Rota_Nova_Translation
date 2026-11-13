"""Focused independent production challenges for B234's new controls, storage and palette risks."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B234_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B234_atomic_v7609');POS=Path('work/analysis/lil_B234_atomic_v7608')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    positive=read(POS/'positive_receipt.json');config=Path(positive['config']);conf=read(config);parent=Path(positive['parent_ROM']);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    assert sha(config.read_bytes())==positive['config_sha256'] and sha(parent.read_bytes())==positive['parent_ROM_sha256']
    doc,mapfile,seal=[Path(conf[k]) for k in ['manuscript','reference_map','reference_approval']];d=read(doc);approved=Path(d['native_approved_manuscript'])
    paths={k:Path(d[k]) for k in ['native_font_proof','native_stored_proof','native_policy_validation','native_approval','speaker_name_review','actual_English_proof','actual_English_view','relocated_control_proof','later_scope_proof','source_named_item_binding','native_name_proof','source_entry_proof','source_ellipsis_palette_proof']}
    tests=[]
    def add(label,path,trail,value):
        path=Path(path);original=read(path);target=original
        for key in trail[:-1]:target=target[key]
        assert target[trail[-1]]!=value,label
        def edit(v):
            target=v
            for key in trail[:-1]:target=target[key]
            target[trail[-1]]=deepcopy(value)
        tests.append((label,path,edit))
    def root(label,path,key,value):add(label,path,[key],value)
    def row(label,index,key,value):add(label,doc,['records',index,key],value)
    indices={r['source_record_index']:i for i,r in enumerate(d['records'])}
    for k in ['source_SC2_sha256','canonical_SC2_sha256','clean_SC2_sha256','clean_ROM_sha256','required_runtime_arm9_sha256','required_runtime_common_sha256','target_SC2_sha256','reference_ROM_sha256']:root('wrong-'+k,config,k,'0'*64)
    for flag in ['external_references_complete','complete1468_byte_predecessor_inverse_with_zero_source_tail','exact_R5_three_CP932_ellipses_actual_black_light_gray_masks_preserved']:root('lost-'+flag,mapfile,flag,False)
    for label,k,value in [('literal-policy','translation_policy','literal'),('wrong-locale','target_locale','en-GB'),('wrong-encoder','encoder','dialogue-fixed-v1'),('unreviewed-formatting','formatting_review_pending',True),('false-completion','full_goal_complete',True),('hidden-offline','offline_only_objects',1)]:root(label,doc,k,value)
    row('printable68-as-prose',indices[5],'source_selector',19)
    row('lost-complete-preamble',indices[5],'source_complete_preamble_hex','0040ffff0013')
    row('trader-wrong-voice',indices[5],'source_voice_class',7)
    row('Carlo-wrong-voice',indices[9],'source_voice_class',0)
    row('source-silence-as-greeting',indices[5],'english','{SPEAKER:68}Hello!')
    row('spoken-Filippo-as-family',indices[9],'english',d['records'][indices[9]]['english'].replace('Filippo','my brother'))
    row('merchant-ancestor-as-father',indices[26],'english',d['records'][indices[26]]['english'].replace('great-grandfather','father'))
    row('conditional-discovery-as-possession',indices[64],'english',d['records'][indices[64]]['english'].replace('If we found','Now that we own'))
    row('false-source-retention',indices[5],'retention_reason','')
    row('missing-context',indices[33],'context','')
    row('manual-line-break',indices[33],'english',d['records'][indices[33]]['english']+'{LB}')
    row('invented-macro',indices[57],'english',d['records'][indices[57]]['english']+'{MACRO:FI}')
    row('source-ellipsis-reencoded-as-ASCII',indices[5],'compiled_hex','682e2e2e')
    row('missing-individual-formatting',indices[33],'review',{**d['records'][indices[33]]['review'],'formatting':False})
    row('lost-native-glyph-proof',indices[16],'actual_record_observed',False)
    row('invented-native-page',indices[57],'native_page_count',2)
    row('expanded-physical-page',indices[57],'original_physical_native_rows_per_page',8)
    row('unscoped-warning-waiver',indices[9],'qa_waivers',['weak-line-ending'])
    row('R33-warning-line-changed',indices[33],'exact_reviewed_base_warnings',[dict(severity='warning',code='weak-line-ending',message="line 2 ends with weak wrap word 'the'")])
    row('R33-warning-reason-erased',indices[33],'qa_waiver_reason',None)
    for k in ['source_tail_bytes','source_logical_end','target_tail_bytes','target_logical_end']:add('wrong-'+k,mapfile,['blocks',0,k],read(mapfile)['blocks'][0][k]+2)
    add('A000-operand-changed',mapfile,['blocks',0,'original_A000_map',0,'source_hex'],'00a0ffff61000110')
    add('end-offset-changed',mapfile,['blocks',0,'complete_end_map',0,'target_offset'],1530)
    add('source-speaker-extent-changed',mapfile,['blocks',0,'command_map',0,'new_extent'],2)
    add('stored-reference-shifted',mapfile,['blocks',0,'text_records',0,'new_offset'],14)
    root('stored-source-tail-confused',paths['native_stored_proof'],'zero_ink_parity_tail_count',0)
    root('stored-reuse-falsely-fresh',paths['native_stored_proof'],'fresh_alignment_cases',72)
    root('font-first-final-glyph-proof-lost',paths['native_font_proof'],'all_first_internal_final_visible_glyphs_in_order_unique_cells_and_bounds',False)
    root('pair-phase-guard-proof-lost',paths['native_font_proof'],'original_pair_phase_and_guards_bound_without_new_substitutions',False)
    root('native-page-count-changed',paths['native_font_proof'],'complete_native_pages',19)
    root('unsafe-input-test-count-changed',paths['native_policy_validation'],'negative_count',0)
    add('unsafe-input-accepted',paths['native_policy_validation'],['negative_cases',0,'rejected'],False)
    root('warning-scope-lost',paths['native_policy_validation'],'all_base_QA_diagnostics_preserved_one_exact_R33_line1_article_classification',False)
    n=paths['speaker_name_review'];ni={r['actor_ID']:i for i,r in enumerate(read(n)['records'])}
    add('Trader-globally-renamed-Filippo',n,['records',ni[104],'english'],'Filippo')
    add('regional-field-as-surname',n,['records',ni[104],'catalogue_current'],'Trader European')
    add('source-oyaji-as-father',n,['records',ni[104],'english'],"Carlo's Father")
    add('Filippo-alias-misidentified',n,['spoken_alias','English'],'Philip')
    for actor in [19,104]:
        add('source-null-middle-lost-'+str(actor),n,['records',ni[actor],'source_fields',2,'source_null'],False)
        add('current-null-middle-lost-'+str(actor),n,['records',ni[actor],'source_fields',2,'current_null'],False)
    add('regional-name-offset-relative-instead-of-absolute',n,['records',ni[104],'source_fields',1,'current_storage_offset'],960)
    add('regional-name-pointer-retargeted',n,['records',ni[104],'source_fields',1,'current_pointer'],37255712)
    item=paths['source_named_item_binding'];reg=['actor104_regional_secondary_storage_contract']
    for label,key,value in [('regional-relative-as-absolute','current_deployed_payload_offset',1518924),('regional-absolute-as-relative','current_physical_ARM9_storage_offset',960),('regional-pool-misidentified','deployed_pool_base',0),('regional-role-pointer-wrong','pointer_field',1185920),('regional-returned-name-scope-lost','both_returned_name_strings_exclude_regional_literal',False)]:add(label,item,[*reg,key],value)
    for label,key,value in [('item106-wrong-ID','record_ID','DK4_ITEM_POINTER_097'),('item106-wrong-title','English',"Phidias' Chisel"),('item106-wrong-storage-class','current_storage_kind','verified-current-staged-payload'),('item106-relative-instead-of-static','current_storage_offset',132),('item106-wrong-pointer-field','pointer_field',1174312),('item106-other-consumers-falsely-approved','current_native_item_getter_card_bounds_mechanics_and_all_other_consumers_not_reviewed_here',False)]:add(label,item,['source_named_item',key],value)
    root('blessing-uncertainty-scope-lost',item,'reported_papal_association_blessing_andconditional_find_not_confirmed_mechanic',False)
    root('Filippo-metadata-as-other-route-approval',item,'legacy_Filippo_spelling_is_consistency_lead_not_other_route_fresh_approval',False)
    np=paths['native_name_proof']
    for label,key,value in [('name-fresh-count-erased','fresh_native_name_font_alignment_cases',0),('name-reuse-count-invented','exact_reused_native_name_font_alignment_cases',20),('name-literal-count-changed','complete_name_component_plane_count',6),('regional-literal-as-nationality','regional_European_literal_render_is_technical_only_not_returned_name_or_nationality',False)]:root(label,np,key,value)
    add('source-prerequisite-invented',paths['source_entry_proof'],['selected_B234_source_events',0,'must_be_completed'],[233])
    add('source-exclusion-invented',paths['source_entry_proof'],['selected_B234_source_events',0,'must_not_be_completed'],[233])
    add('source-action-misidentified',paths['source_entry_proof'],['selected_B234_source_events',0,'action_index'],234)
    a=paths['actual_English_proof'];actual=read(a)
    root('partial-actual-hold',a,'incomplete_sampled_body_holds',1)
    root('unreaped-capture',a,'all_jobs_terminal_and_reaped',False)
    add('R5-wrong-ASCII-shadow-color',a,['actual_panels',indices[5],'body_shadow_RGB'],[98,97,98])
    add('R5-wrong-held-shadow-color',a,['actual_panels',indices[5],'complete_body_holds',0,'body_shadow_RGB'],[98,97,98])
    add('ASCII-wrong-CP932-shadow-color',a,['actual_panels',indices[9],'body_shadow_RGB'],[197,198,197])
    for index in [indices[5],indices[9],indices[16],indices[57]]:
        add('incomplete-body-'+str(index),a,['actual_panels',index,'complete_body_holds',0,'complete_independent_native_body_black_gray_all_glyphs_equal'],False)
        add('incomplete-header-'+str(index),a,['actual_panels',index,'complete_name_holds',0,'complete_name_and_blank_guards_equal'],False)
    add('timing-row-erased',a,['command_comparison_differences'],actual['command_comparison_differences'][:-1])
    add('duration-erased',a,['command_duration_changes'],actual['command_duration_changes'][:-1])
    root('false-natural-activation',a,'initialized_B22_not_natural_event234_original_location_earned_progress_full_effects_route_orhardware',False)
    root('broad-simulation-claim',paths['later_scope_proof'],'no_full_RAM_future_sequence_broad_simulation_or_complete_causal_claim',False)
    root('invented-late-RGB-difference',paths['later_scope_proof'],'later_sampled_RGB_differences',[dict(frame=16001,whole_RGB_equal=False)])
    root('late-seed-changed',paths['later_scope_proof'],'final_PRNG_seeds',[1202927797,0])
    root('preview-dark-gray-as-actual-CP932-palette',paths['source_ellipsis_palette_proof'],'retained_CP932_shadow_RGB',[98,97,98])
    root('source-ellipsis-incomplete-glyph',paths['source_ellipsis_palette_proof'],'black_pixels',12)
    root('source-ellipsis-shadow-incomplete',paths['source_ellipsis_palette_proof'],'shadow_pixels',12)
    root('source-ellipsis-code-changed',paths['source_ellipsis_palette_proof'],'source_body_hex','8163')
    for key in ['original_normal_end1528_four_bytes_andtarget_zero_storage_tail_preserved','normal_state0_retains_existing_value_word_in_all25_cases','opaque_A000_effects_bridged_not_fully_explained']:root('control-'+key,paths['relocated_control_proof'],key,False)
    runplan=next(Path(p) for p in actual['evidence'] if Path(p).name=='run_plan.json')
    root('fixture-block-misidentified',runplan,'displayed_original_source_block',233)
    assert len(tests)==len({t[0] for t in tests}) and len(tests)>=70
    ROOT.mkdir(parents=True);results=[];original_load=owned.load
    protected=[parent,Path('translations/editorial_review_current_v1.json'),Path('translations/release_stack.json')];before_shared={str(p):sha(p.read_bytes()) for p in protected}
    save(ROOT/'challenge_plan.json',dict(negative_count=len(tests),cases=[dict(case=l,target=str(p)) for l,p,e in tests],dependency_digests_deliberately_bypassed=True,focused_new_B234_risks_existing83_policy_cases_not_replayed=True))
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
            except (ValueError,AssertionError) as e:results.append(dict(case=label,target=str(path),rejected=True,error=str(e),archive_writes=0,dependency_digests_deliberately_bypassed=True))
            else:raise RuntimeError('Unsafe alteration accepted:'+label)
        finally:owned.load=original_load
        assert not writes and image.read_file(owned.PATH)==before,label
        if (i+1)%20==0:save(ROOT/'partial_negative_cases.json',results);print(f'{i+1}/{len(tests)} independent rejections pass',flush=True)
    assert before_shared=={str(p):sha(p.read_bytes()) for p in protected}
    cases=ROOT/'negative_cases.json';save(cases,results)
    save(ROOT/'atomic_validation_receipt.json',dict(config=str(config),config_sha256=sha(config.read_bytes()),positive_proof=positive['positive_proof'],positive_proof_sha256=positive['positive_proof_sha256'],parent_ROM=str(parent),parent_ROM_sha256=positive['parent_ROM_sha256'],positive_records=18,negative_cases=str(cases),negative_cases_sha256=sha(cases.read_bytes()),negative_count=len(results),all_negatives_reject_before_mutation=True,all18_actual18_pages71_body71_headers_bound=True,original_A00025_ends_and_explicit_comparison_limits_bound=True,regional_absolute_vs_relative_andR5_CP932_palette_risks_checked=True,shared_ledger_registry_parent_ROM_unchanged=True,full_goal_complete=False))
    print(dict(positive_records=18,negative_count=len(results),all_before_mutation=True,credit=0),flush=True)
