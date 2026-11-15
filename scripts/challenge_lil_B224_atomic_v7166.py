"""Actual-changing B224 challenges bypass dependency digests to reach individual gates."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B224_editorial_v3 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B224_atomic_v7166');POS=Path('work/analysis/lil_B224_atomic_v7165b')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();positive=read(POS/'positive_receipt.json');config=Path(positive['config']);conf=read(config);parent=Path(positive['parent_ROM'])
    assert sha(config.read_bytes())==positive['config_sha256'] and sha(parent.read_bytes())==positive['parent_ROM_sha256']
    baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');doc,mapfile,seal=[Path(conf[k]) for k in ['manuscript','reference_map','reference_approval']];d=read(doc);approved=Path(d['native_approved_manuscript']);paths={k:Path(d[k]) for k in ['native_font_proof','native_stored_proof','native_policy_validation','native_approval','speaker_name_review','actual_English_proof','actual_English_view','relocated_control_proof','later_scope_proof','ellipsis_palette_proof']};tests=[]
    def add(label,path,edit):tests.append((label,Path(path),edit))
    def root(label,path,key,value):add(label,path,lambda v,k=key,x=value:v.update({k:x}))
    def row(label,key,value,index=0):add(label,doc,lambda v,k=key,x=value,i=index:v['records'][i].update({k:x}))
    for k in ['source_SC2_sha256','canonical_SC2_sha256','clean_SC2_sha256','clean_ROM_sha256','required_runtime_arm9_sha256','required_runtime_common_sha256','target_SC2_sha256','reference_ROM_sha256']:root('wrong-'+k,config,k,'0'*64)
    for k in owned.FLAGS:root('lost-map-'+k,mapfile,k,False)
    for k,x in [('translation_policy','literal'),('target_locale','en-GB'),('encoder','dialogue-fixed-v1'),('formatting_review_pending',True),('actual_objects',14),('actual_pages',14),('offline_only_objects',1),('all207_name_alias_and_full_four_storyline_editorial_objective_open',False)]:root('manuscript-'+k,doc,k,x)
    add('missing-record',doc,lambda v:v['records'].pop());add('duplicate-record',doc,lambda v:v['records'].__setitem__(1,deepcopy(v['records'][0])))
    for i,r in enumerate(d['records']):add('lost-formatting-'+r['id'],doc,lambda v,i=i:v['records'][i]['review'].update(formatting=False))
    for k in ['source','context','localization','naturalness']:add('lost-individual-'+k,doc,lambda v,k=k:v['records'][0]['review'].update({k:False}))
    for label,k,x,i in [('empty-speaker','speaker','',0),('invented-rank','speaker','Commander Julian Lopes',0),('lost-context','context','',0),('lost-meaning','source_meaning','',0),('lost-localization','localization_note','',0),('lost-whole-exchange','full_exchange_read_aloud_review',False,0),('wrong-actor','source_selector',2,0),('lost-preamble','source_complete_preamble_hex','0040ffff0002',0),('false-retention','editorial_decision','retain-wording',0),('lost-retention-reason','retention_reason','',2),('false-actual','actual_record_observed',False,0),('false-offline-status','native_plane_verified_not_actual_English_gameplay',True,0),('taller-physical-page','original_physical_native_rows_per_page',8,0),('extra-page','native_page_count',2,0),('changed-capacity','native_profile_maximum_total_rows',8,0),('blanket-wrap-waiver','qa_waivers',['weak-line-ending','encoding'],0),('missing-exact-waiver','qa_waivers',[],0),('lost-rowcount-reason','row_count_reason',None,1),('lost-boundaries','reviewed_ordinary_boundaries',[],0),('bad-compiled','compiled_hex','1a41',0),('wrong-index','current_record_index',35,0)]:row(label,k,x,i)
    add('delete-original-base-warning',doc,lambda v:v['records'][0]['base_QA_report']['base_QA_issues'].clear())
    for side in ['source','current']:add('wrong-'+side+'-reference',doc,lambda v,s=side:v['records'][0][s+'_reference'].update(offset=14))
    for label,text in [('manual-LB',d['records'][0]['english']+'{LB}'),('positioned-LB',d['records'][0]['english']+'{LB@3}'),('new-macro',d['records'][0]['english']+'{MACRO:FI}'),('invented-marriage',d['records'][0]['english'].replace('Hi, Safia.','Hello, my wife.'))]:row(label,'english',text)
    row('ellipsis-normalized-to-ASCII','english','{SPEAKER:1A}...',2);row('ellipsis-compiled-changed','compiled_hex','1a2e2e2e',2)
    for key in ['source_tail_bytes','source_logical_end','target_tail_bytes','target_logical_end']:add('wrong-'+key,mapfile,lambda v,k=key:v['blocks'][0].update({k:v['blocks'][0][k]+2}))
    for key in ['complete_end_map','original_A000_map','original_C200_map']:add('lost-'+key,mapfile,lambda v,k=key:v['blocks'][0][k].clear())
    add('A000-invented-item-operand',mapfile,lambda v:v['blocks'][0]['original_A000_map'][0].update(source_hex='00a0ffff47000110'))
    add('C200-wrong-target',mapfile,lambda v:v['blocks'][0]['original_C200_map'][0].update(target_offset=1036))
    add('end-wrong-target',mapfile,lambda v:v['blocks'][0]['complete_end_map'][0].update(target_offset=1038))
    add('stored-reference-wrong',mapfile,lambda v:v['blocks'][0]['text_records'][0].update(new_offset=14))
    add('command-extent-wrong',mapfile,lambda v:v['blocks'][0]['command_map'][0].update(new_extent=2))
    for k,x in [('complete_native_pages',14),('logical_compiled_input_alignment_cases',119),('all_first_internal_final_visible_glyphs_in_order_unique_cells_and_bounds',False),('each216x64_plane_exact_independent_current_font_and_all_canaries',False),('original_source_current_R11_ellipsis_CP932_glyph_retained_without_punctuation_revision',False)]:root('font-'+k,paths['native_font_proof'],k,x)
    for k,x in [('stored_alignment_cases',59),('fresh_alignment_cases',35),('exact_reused_alignment_cases',23),('zero_ink_parity_tail_count',8),('all_bounds_canaries_pair_phase_and_zero_macros_pass',False)]:root('stored-'+k,paths['native_stored_proof'],k,x)
    root('policy-rejection-count',paths['native_policy_validation'],'negative_count',61);add('policy-negative-accepted',paths['native_policy_validation'],lambda v:v['negative_cases'][0].update(rejected=False))
    root('approval-name-alignments',paths['native_approval'],'name_alignments',19)
    for k in ['secondary_Basra_preserved_not_appended_as_surname','both_actual_English_names_complete','full_catalogue_UI_unvisited','all207_names_roles_aliases_and_earlier_consumers_remain_open']:root('names-'+k,paths['speaker_name_review'],k,False)
    add('Basra-invented-surname',paths['speaker_name_review'],lambda v:v['records'][1].update(english='Safia Basra'))
    a=paths['actual_English_proof']
    for k,x in [('actual_unique_speeches',14),('actual_complete_body_holds',58),('actual_complete_name_holds',58),('incomplete_sampled_body_holds',1),('source_exit_frame',6456),('normal_terminal_result',[0,1]),('no_full_RAM_every_intermediate_frame_future_sequence_broad_simulation_or_causal_claim',False),('all_following_resident_payloads_verified_against_actual_SC0_to_SC3_bank',False)]:root('actual-'+k,a,k,x)
    add('actual-unreviewed-command-difference',a,lambda v:v['command_comparison_differences'].append(dict(unreviewed=True)))
    add('later-RGB-sample-differs',a,lambda v:v['later_sampled_whole_frame_comparisons'][0].update(whole_RGB_equal=False))
    for i,r in enumerate(d['records']):
        add('actual-incomplete-body-'+r['id'],a,lambda v,i=i:v['actual_panels'][i]['complete_body_holds'][0].update(complete_independent_native_body_black_gray_all_glyphs_equal=False))
        add('actual-incomplete-name-'+r['id'],a,lambda v,i=i:v['actual_panels'][i]['complete_name_holds'][0].update(complete_name_and_blank_guards_equal=False))
    root('view-pending',paths['actual_English_view'],'visual_review_pending',True)
    p=paths['ellipsis_palette_proof']
    for k,x in [('complete_source_current_compiled_hex','1a2e2e2e'),('retained_CP932_shadow_RGB',[98,97,98]),('shadow_pixels',5),('sole_existing_ellipsis_palette_scope_not_global_Japanese_renderer_approval',False)]:root('palette-'+k,p,k,x)
    add('ellipsis-full-RGB-not-source',a,lambda v:v['actual_panels'][2]['complete_body_holds'][0].update(retained_R11_full_body_RGB_equals_original=False))
    add('ASCII-gray-weakened',a,lambda v:v['actual_panels'][0].update(body_shadow_RGB=[197,198,197]))
    add('C200-request-changed',paths['relocated_control_proof'],lambda v:v['relocated_C200']['source_owned_UI_request_words'].__setitem__(1,3))
    add('C200-unowned-mutation',paths['relocated_control_proof'],lambda v:v['relocated_C200'].update(all_other4MiB_actor_roster_event_RNG_and_models_exact=False))
    root('later-captain-changed',paths['later_scope_proof'],'captain_IDs',[0,2]);root('later-seed-changed',paths['later_scope_proof'],'final_PRNG_seeds',[0,3169181745])
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
    assert len(results)==len(tests) and sha(parent.read_bytes())==positive['parent_ROM_sha256'];cases=ROOT/'negative_cases.json';save(cases,results)
    save(ROOT/'atomic_validation_receipt.json',dict(config=str(config),config_sha256=sha(config.read_bytes()),positive_proof=positive['positive_proof'],positive_proof_sha256=positive['positive_proof_sha256'],parent_ROM=str(parent),parent_ROM_sha256=positive['parent_ROM_sha256'],positive_records=15,negative_cases=str(cases),negative_cases_sha256=sha(cases.read_bytes()),negative_count=len(results),all_negatives_reject_before_mutation=True,all15_objects_reconstructed_with_one_archive_write=True,source960_full_inverse_including_tail2_and_all_other_components_exact=True,all15_actual_pages59_body59_headers_and_four_ellipsis_full_RGB_holds_bound=True,original_A000_C20025_ends_and_explicit_comparison_limits_bound=True,full_goal_complete=False));print(dict(positive_records=15,negative_count=len(results),all_before_mutation=True,credit=0),flush=True)
