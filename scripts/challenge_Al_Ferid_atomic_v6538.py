"""Reject damaged name ownership, source, review and native evidence before one ARM9 write."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import Al_Ferid_name_release_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Al_Ferid_atomic_v6538');POS=Path('work/analysis/Al_Ferid_atomic_v6537')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();positive=read(POS/'positive_receipt.json');config=Path(positive['config']);conf=read(config);parent=Path(positive['parent_ROM']);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');assert sha(config.read_bytes())==positive['config_sha256'] and sha(parent.read_bytes())==positive['parent_ROM_sha256']
    doc,seal,proof,compat=[Path(conf[k]) for k in ['manuscript','approval','native_proof','B210_compatibility']];tests=[]
    def add(label,path,edit):tests.append((label,Path(path),edit))
    def root(label,path,key,value):add(label,path,lambda v,k=key,x=value:v.update({k:x}))
    def row(label,key,value):add(label,doc,lambda v,k=key,x=value:v['records'][0].update({k:x}))
    for k in ['canonical_ARM9_sha256','clean_ROM_sha256','clean_ARM9_sha256']:root('wrong-'+k,config,k,'0'*64)
    add('pre-B210-input',config,lambda v:v['source_files'].update({'/data/SC2.DK4':'0'*64}));add('different-runtime-component',config,lambda v:v['source_components'].update({'/__arm9__.bin':'0'*64}))
    for k,x in [('format','other'),('translation_policy','literal'),('target_locale','en-GB'),('all_five_individual_name_review_gates_true',False),('all621_name_table_pointers_and_cache_plan_unchanged',False),('full_catalogue_UI_unvisited',False),('all207_name_role_alias_and_earlier_consumer_review_open',False),('full_goal_complete',True),('exact_name_pointer_occurrences',[1183136])]:root('manuscript-'+k,doc,k,x)
    add('missing-name-record',doc,lambda v:v['records'].pop());add('duplicate-name-record',doc,lambda v:v['records'].append(deepcopy(v['records'][0])))
    for k in ['source','context','localization','naturalness','formatting']:add('lost-gate-'+k,doc,lambda v,k=k:v['records'][0]['review'].update({k:False}))
    for k,x in [('actor_ID',18),('field_column',0),('source_Japanese','シン'),('current_English','Ferid'),('english','Farid'),('editorial_decision','retain-wording'),('new_name_completion_credit',1),('new_dialogue_completion_credit',1),('context',''),('source_meaning',''),('localization_note',''),('formatting_reason','')]:row('row-'+k,k,x)
    add('wrong-clean-pointer',doc,lambda v:v['records'][0]['source_reference'].update(pointer=34978392));add('wrong-clean-terminated-bytes',doc,lambda v:v['records'][0]['source_reference'].update(terminated_hex='00'));add('wrong-current-pointer',doc,lambda v:v['records'][0]['current_reference'].update(runtime_pointer=37256525));add('wrong-staged-slot',doc,lambda v:v['records'][0]['current_reference'].update(staged_payload_offset=813));add('wrong-file-slot',doc,lambda v:v['records'][0]['current_reference'].update(file_offset=1518777))
    add('missing-source-name-field',doc,lambda v:v['records'][0]['all_three_source_current_name_fields'].pop());add('wrong-family-clean-field',doc,lambda v:v['records'][0]['all_three_source_current_name_fields'][1].update(pointer_field=1183144));add('invented-family-name',doc,lambda v:v['records'][0]['all_three_source_current_name_fields'][1].update(current_English='Shen'));add('wrong-additional-source-bytes',doc,lambda v:v['records'][0]['all_three_source_current_name_fields'][2].update(source_terminated_hex='00'))
    for k,x in [('one_additional_name_field_typography_approved_without_new_spelling',False),('all5_review_gates_true',False),('original_full_catalogue_getter_corrected_not_actual_full_catalogue_UI',False),('progressive_Al_Shin_and_all_other_fields_pointers_cache_code_fonts_unchanged',False),('no_global_name_normalization_or_207_queue_closure',False),('visual_review_pending',True),('new_review_credit',1),('exact_raw_pointer_hits',[1183144,1183136])]:root('seal-'+k,seal,k,x)
    for k,x in [('all9_whole_RGB_frames_match_V6488',False),('actual_target_staged123264_payload_and_each_executed_instruction_bound',False),('all_pointer_actor_rows_code_font_other_files_and_components_exact_except_five_name_data_bytes',False),('full_catalogue_getter_returns_corrected_Al_Ferid_Shin',False),('progressive_Al_Shin_and_both_Lil_Argot_consumers_unchanged',False),('only_ASCII_typography_correction_no_new_spelling_rank_relationship_or_biography',False),('full_catalogue_UI_unvisited_not_claimed_as_actual_full_name_display',False),('source_name_queue207_and_all_other_alias_consumers_open',False),('name_literal_alignment_cases',31),('target_ARM9_sha256','0'*64)]:root('native-'+k,proof,k,x)
    add('missing-startup-RGB-pair',proof,lambda v:v['actual_target_opening_framebuffer_pairs'].pop());add('missing-full-name-plane',proof,lambda v:v['target_native_name_planes'].pop());add('clipped-final-name-glyph',proof,lambda v:v['target_native_name_planes'][2].update(complete_leading_internal_final_ASCII_glyphs_in_bounds_one_row=False));add('wrong-full-name-getter',proof,lambda v:v['native_four_name_getters']['rows'][3].update(text='Al Shin'));add('lost-source-owned-getter-path',proof,lambda v:v['native_four_name_getters'].update(all_four_original_consumers_and_owned_or_readonly_memory_paths_exact=False))
    for k in ['all10_entire_dispatch_results_identical','all467_catalogue_rows_and_native_calls_bound','only_adapter_hash_guard_updated_no_address_or_instruction_change']:root('compatibility-'+k,compat,k,False)
    add('missing-post-name-dispatch',compat,lambda v:v['cases'].pop())
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
        results.append(dict(case=label,rejected=True,reason=reason,dependency_digests_bypassed_to_challenge_semantics=True,no_component_mutation=True))
        if number%20==0:print(f'{number}/{len(tests)} name semantic rejection cases pass.',flush=True)
    save(ROOT/'negative_cases.json',dict(cases=results,count=len(results),all_rejected_before_component_mutation=True,producer_sha256=sha(Path(__file__).read_bytes())))
    save(ROOT/'atomic_validation_receipt.json',dict(**{k:positive[k] for k in ['config','config_sha256','positive_proof','positive_proof_sha256','parent_ROM','parent_ROM_sha256','positive_records']},negative_cases=str(ROOT/'negative_cases.json'),negative_cases_sha256=sha((ROOT/'negative_cases.json').read_bytes()),negative_count=len(results),all_negatives_reject_before_mutation=True,one_name_reconstructed_with_one_component_write=True,five_owned_bytes_full_inverse_and_all_other_components_exact=True,full_goal_complete=False));print(f'Ferid name atomic validation passes:{len(results)} semantic negatives reject before component mutation.',flush=True)
