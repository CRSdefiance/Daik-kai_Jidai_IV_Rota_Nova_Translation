"""Bypass dependency digests deliberately and challenge independent semantic gates before mutation."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B214_editorial_v1 as owned,lil_B214_atomic_support_v1 as support
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B214_atomic_v6731');POS=Path('work/analysis/lil_B214_atomic_v6730')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();positive=read(POS/'positive_receipt.json');config=Path(positive['config']);conf=read(config);parent=Path(positive['parent_ROM']);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');assert sha(config.read_bytes())==positive['config_sha256'] and sha(parent.read_bytes())==positive['parent_ROM_sha256']
    doc,mapfile,seal=[Path(conf[k]) for k in ['manuscript','reference_map','reference_approval']];d=read(doc);paths={k:Path(d[k]) for k in ['native_font_proof','native_stored_proof','native_policy_validation','native_approval','speaker_name_review','actual_English_proof','actual_English_view','relocated_control_proof']};tests=[]
    def add(label,path,edit):tests.append((label,Path(path),edit))
    def root(label,path,key,value):add(label,path,lambda v,k=key,x=value:v.update({k:x}))
    def row(label,key,value,index=0):add(label,doc,lambda v,k=key,x=value,i=index:v['records'][i].update({k:x}))
    for k in ['source_SC2_sha256','canonical_SC2_sha256','clean_SC2_sha256','clean_ROM_sha256','required_runtime_arm9_sha256','required_runtime_common_sha256','target_SC2_sha256','reference_ROM_sha256']:root('wrong-'+k,config,k,'0'*64)
    for k in owned.FLAGS:root('lost-map-'+k,mapfile,k,False)
    for k,x in [('translation_policy','literal'),('target_locale','en-GB'),('encoder','dialogue-fixed-v1'),('formatting_review_pending',True),('actual_objects',17),('actual_pages',17),('offline_only_objects',0),('all207_name_alias_review_and_full_four_storyline_editorial_objective_open',False)]:root('manuscript-'+k,doc,k,x)
    add('missing-record',doc,lambda v:v['records'].pop());add('duplicate-record',doc,lambda v:v['records'].__setitem__(1,deepcopy(v['records'][0])))
    for index,r in enumerate(d['records']):add('lost-formatting-'+r['id'],doc,lambda v,i=index:v['records'][i]['review'].update(formatting=False))
    for k in ['source','context','localization','naturalness']:add('lost-individual-'+k,doc,lambda v,k=k:v['records'][0]['review'].update({k:False}))
    for label,key,value,index in [('empty-speaker','speaker','',0),('invented-rank','speaker','Father Manuel Almeida',9),('lost-context','context','',0),('lost-meaning','source_meaning','',0),('lost-localization','localization_note','',0),('lost-whole-exchange','full_exchange_read_aloud_review',False,0),('wrong-static','source_selector',23,0),('wrong-dynamic','source_selector',151,10),('lost-preamble','source_complete_preamble_hex','0040ffff0002',0),('false-retention','editorial_decision','retain-wording',0),('lost-retention-reason','retention_reason','',1),('false-Manuel-actual','actual_record_observed',True,9),('false-offline-status','native_plane_verified_not_actual_English_gameplay',False,9),('taller-page','original_physical_native_rows_per_page',8,0),('extra-page','native_page_count',2,0),('changed-capacity','native_profile_maximum_total_rows',8,0),('blanket-wrap-waiver','qa_waivers',['weak-line-ending'],0),('lost-rowcount-reason','qa_waiver_reason','',0),('lost-boundaries','reviewed_ordinary_boundaries',[],0),('virtual-selector-stored','virtual_formatter_selector_not_stored_in_actor_style_body',False,10),('bad-compiled','compiled_hex','04',0),('wrong-index','current_record_index',35,0)]:row(label,key,value,index)
    for side in ['source','current']:add('wrong-'+side+'-reference',doc,lambda v,s=side:v['records'][0][s+'_reference'].update(offset=304))
    signature=next(i for i,r in enumerate(d['records']) if r['id']=='DK4_MES_B214_R0068');row('old-Pasha-signature','english',d['records'][signature]['english'].replace('Janus Pasar','Janus Pasha'),signature)
    for label,text in [('manual-LB',d['records'][0]['english']+'{LB}'),('positioned-LB',d['records'][0]['english']+'{LB@3}'),('new-macro',d['records'][0]['english']+'{MACRO:FI}'),('invented-location',d['records'][0]['english'].replace('a road leading to Rome','the Appian Way in Rome'))]:row(label,'english',text)
    add('typed-source-alias-lost',mapfile,lambda v:v['blocks'][0]['actor_style_commands'][0]['old_style_offsets'].__setitem__(7,0));add('typed-target-alias-lost',mapfile,lambda v:v['blocks'][0]['actor_style_commands'][0]['new_style_offsets'].__setitem__(7,0));add('nested-reference-disagrees',mapfile,lambda v:v['blocks'][0]['actor_style_commands'][0]['alternative_records'][0].update(target_hex='41'));add('source-relative-operand-lost',mapfile,lambda v:v['blocks'][0]['relative_skip_fixups'][0].update(span=8));add('lost-normal-tail',mapfile,lambda v:v['blocks'][0].update(target_tail_bytes=0));add('lost-end-map',mapfile,lambda v:v['blocks'][0]['complete_end_map'].update(target_offset=1300))
    for k,x in [('complete_native_pages',18),('logical_compiled_input_alignment_cases',135),('all_first_internal_final_visible_glyphs_in_order_unique_cells_and_bounds',False),('each_plane_exact_independent_current_font_and_all_canaries',False),('D0_fallback151_unchanged',False)]:root('font-'+k,paths['native_font_proof'],k,x)
    add('font-lost-final-glyph',paths['native_font_proof'],lambda v:v['records'][0].update(all_visible_first_internal_final_characters_in_order=False))
    for k,x in [('final_stored_alignment_cases',67),('fresh_parity_tail_records',0),('no_extra_blank_page_or_lost_leading_trailing_internal_glyph',False)]:root('stored-'+k,paths['native_stored_proof'],k,x)
    root('policy-rejection-count',paths['native_policy_validation'],'negative_count',79);add('policy-negative-accepted',paths['native_policy_validation'],lambda v:v['negative_cases'][0].update(rejected=False));add('policy-row-reason-lost',paths['native_policy_validation'],lambda v:v['row_count_reasons'].pop())
    root('approval-offline-erased',paths['native_approval'],'offline_only_objects',0);root('approval-name-alignments',paths['native_approval'],'name_alignments',40)
    for k in ['full_catalogue_UI_unvisited','Manuel_actual_header_unvisited','actor151_progressive_Sailor_catalogue_Retainer_not_newly_editorially_approved','all207_proper_name_role_alias_and_earlier_consumer_review_open']:root('names-'+k,paths['speaker_name_review'],k,False)
    a=paths['actual_English_proof']
    for k,x in [('actual_unique_objects',17),('complete_body_holds',28),('complete_name_holds',28),('source_exit_frame',5016),('actual_predicate_type2_Boolean_values',[1,0]),('normal_end_result',[0,1]),('no_full_RAM_future_sequence_broad_simulation_or_complete_causal_claim',False)]:root('actual-'+k,a,k,x)
    for key in ['command_result_differences','command_UI_word_differences','command_timing_differences','command_RNG_differences','command_duration_changes','later_same_frame_RGB_differences']:add('unreviewed-difference-'+key,a,lambda v,k=key:v[k].append(dict(unreviewed=True)))
    add('actual-body-hold-lost',a,lambda v:v['actual_panels'][0]['complete_body_holds'].pop());add('actual-mask-not-complete',a,lambda v:v['actual_panels'][0]['complete_body_holds'][0].update(complete_independent_native_body_black_gray_all_glyphs_equal=False));root('view-not-viewed',paths['actual_English_view'],'visual_review_pending',True)
    c=paths['relocated_control_proof'];root('typed-alias-not-preserved',c,'original_style2_7_alias_preserved',False);add('style-pointer-case-lost',c,lambda v:v['all207_target_style_getters']['cases'].pop());add('predicate-alignment-wrong',c,lambda v:v['relocated_predicates'][0].update(target_operand_alignment=2));add('predicate-owned-scratch-erased',c,lambda v:v['relocated_predicates'][1]['relocated'].update(original_unaligned_operand_read_scratch_writes=[]));add('normal-residual-normalized',c,lambda v:v['target_normal_end_cases'][1].update(native_result=[0,0,0,0,0,0]))
    root('loader-stubbed',Path(conf['loader']),'SDK_IO_bridges_only_no_loader_or_cache_success_stub',False);add('census-mapped-command-changed',Path(conf['census']),lambda v:v['blocks'][0]['mapped_commands'][0].update(new_native_extent=2));add('prerequisite87-erased',Path(conf['entry']),lambda v:v['selected_B214_source_events'][0].update(must_be_completed=[]))
    assert len(tests)==len({t[0] for t in tests}) and len(tests)>=90;ROOT.mkdir(parents=True);results=[];original_owned,original_support=owned.load,support.load
    for index,(label,path,edit) in enumerate(tests):
        original=read(path);altered=deepcopy(original);edit(altered);assert altered!=original,label
        def injected(p):
            key=Path(p).resolve()
            if key==config.resolve():
                value=deepcopy(altered if key==path.resolve() else conf);value['dependencies']={};return value
            if key==path.resolve():return deepcopy(altered)
            return original_owned(p)
        image=NdsImage.open(parent);before=image.read_file(owned.PATH);writes=[]
        def forbidden(*args,**kwargs):writes.append(args[0]);raise RuntimeError('Archive mutation attempted in negative '+label)
        image.replace_file=forbidden;owned.load=support.load=injected
        try:
            try:owned.apply_release(image,baseline,config)
            except (ValueError,AssertionError) as e:results.append(dict(case=label,target=str(path),rejected=True,error=str(e),archive_writes=0,dependency_digests_deliberately_bypassed=True))
            else:raise RuntimeError('Unsafe B214 alteration accepted:'+label)
        finally:owned.load=original_owned;support.load=original_support
        assert not writes and image.read_file(owned.PATH)==before,label
        if (index+1)%25==0:print(f'{index+1}/{len(tests)} independent rejections pass',flush=True)
    assert len(results)==len(tests) and sha(parent.read_bytes())==positive['parent_ROM_sha256'];cases=ROOT/'negative_cases.json';save(cases,results)
    save(ROOT/'atomic_validation_receipt.json',dict(config=str(config),config_sha256=sha(config.read_bytes()),positive_proof=positive['positive_proof'],positive_proof_sha256=positive['positive_proof_sha256'],parent_ROM=str(parent),parent_ROM_sha256=positive['parent_ROM_sha256'],positive_records=17,negative_cases=str(cases),negative_cases_sha256=sha(cases.read_bytes()),negative_count=len(results),all_negatives_reject_before_mutation=True,all17_objects_reconstructed_with_one_archive_write=True,source1316_full_inverse_and_all_other_components_exact=True,nine_actual_objects29_body29_names_eight_offline_objects_and_scope_bound=True,both_opposite_predicate_alignment_changes_original_owned_scratch_and_normal_residual_bound=True,full_goal_complete=False));print(dict(positive_records=17,negative_count=len(results),all_before_mutation=True,credit=0),flush=True)
