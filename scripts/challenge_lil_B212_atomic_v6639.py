"""Challenge semantic release seams with dependency hashes bypassed; every rejection precedes writes."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B212_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B212_atomic_v6639');POS=Path('work/analysis/lil_B212_atomic_v6638b')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();positive=read(POS/'positive_receipt.json');config=Path(positive['config']);conf=read(config);parent=Path(positive['parent_ROM']);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');doc,mapfile,seal=[Path(conf[k]) for k in ['manuscript','reference_map','reference_approval']];d=read(doc);tests=[]
    def add(label,path,edit):tests.append((label,Path(path),edit))
    def root(label,path,key,value):add(label,path,lambda v,k=key,x=value:v.update({k:x}))
    def row(label,key,value,index=0):add(label,doc,lambda v,k=key,x=value,i=index:v['records'][i].update({k:x}))
    for k in ['source_SC2_sha256','canonical_SC2_sha256','clean_SC2_sha256','clean_ROM_sha256','required_runtime_arm9_sha256','required_runtime_common_sha256','target_SC2_sha256','reference_ROM_sha256']:root('wrong-'+k,config,k,'0'*64)
    for k in owned.FLAGS:root('lost-map-'+k,mapfile,k,False)
    for k,x in [('translation_policy','literal'),('target_locale','en-GB'),('encoder','dialogue-fixed-v1'),('formatting_review_pending',True),('actual_unique_speech_objects',9),('actual_unique_choice_labels',4),('offline_only_speech_IDs',[]),('no_uncle_kinship_named_peninsula_named_spear_guarantee_or_item_effect_invented',False),('game_Changban_Bridge_reference_not_silently_corrected',False),('approved_names_Rafael_Hodram_Joakim_Maria_Camille_preserved',False)]:root('manuscript-'+k,doc,k,x)
    for index,r in enumerate(d['records']):
        add('lost-individual-formatting-'+r['id'],doc,lambda v,i=index:v['records'][i]['review'].update(formatting=False))
    for k,x in [('english','Hello! Uncle knows best.'),('source_hex','00'),('current_hex','00'),('source_voice_class',3),('source_selector',148),('source_complete_preamble_hex','0040ffff0094'),('kind','system-FE'),('actual_record_observed',False),('compiled_hex','954869'),('source_meaning','Unrelated source'),('retention_reason','invented')]:row('record-'+k,k,x)
    row('shortened-Zhuge-choice','english','Zhuge',13);row('invented-choice-index','option_index',7,13);add('missing-record',doc,lambda v:v['records'].pop());add('duplicate-record',doc,lambda v:v['records'].__setitem__(1,deepcopy(v['records'][0])))
    for key,x in [('complete_body_holds',22),('complete_name_holds',24),('source_flagged_end1_value0_preserved_in_actual_English',False),('source_exit_frame',4774),('complete_label_holds',19),('source_and_English_runs_terminal_reaped',False)]:root('actual-'+key,d['actual_English_proof'],key,x)
    add('lost-body-hold',d['actual_English_proof'],lambda v:v['actual_panels'][0]['complete_body_holds'].pop());add('lost-name-hold',d['actual_English_proof'],lambda v:v['actual_panels'][0]['complete_name_holds'].pop());add('lost-timing-limit',d['actual_English_proof'],lambda v:v['command_timing_differences'].pop())
    for key in ['ordinary_00000000_terminator_actual_result_state0_residual1_preserved','all_source_English_first_menu_returns_index1','following_B120_command_pending_at6001_not_full_following_scene_completion']:root('No-'+key,d['actual_No_proof'],key,False)
    for key,x in [('actual_shared_physical_backing',[66,36]),('two_option_views',[48,11]),('three_option_views',[60,12]),('raw_2376_owned_three_caption_pixels_equal_independent_current_font',False),('unowned_physical_differences',0),('no_blank_or_equal_unowned_backing_claim',False)]:root('backing-'+key,d['actual_menu_backing_proof'],key,x)
    add('wrong-highlight',d['actual_menu_backing_proof'],lambda v:v['three_actual_highlight_states'][1].update(selected_option_index=0));root('lost-seeded-end',d['seeded_end_proof'],'case_count',149);root('zero-normalized-end',d['seeded_end_proof'],'normal_state0_leaves_existing_value_word_unchanged',False);root('unviewed',d['actual_English_view'],'visual_review_pending',True);root('false-all-actual-view',d['actual_English_view'],'offline_only_speech_IDs',[]);root('false-catalogue-visit',d['speaker_name_review'],'full_catalogue_UI_unvisited',False);root('lost-role-review',d['speaker_name_review'],'one_contextual_role_retention_approved_no_asset_change',False);root('lost-layout-negative',d['native_policy_validation'],'negative_count',64);root('waived-warning',d['native_policy_validation'],'no_base_QA_warning_error_removed_or_waived',False);root('loader-stub',conf['loader'],'SDK_IO_bridges_only_no_loader_or_cache_success_stub',False);root('alias-census',conf['census'],'only_original24070_interpreter_call_no_literal_alias',False);add('invented-event-prerequisite',conf['entry'],lambda v:v['selected_B212_source_events'][0].update(must_be_completed=[85]));root('false-seal',seal,'all14_five_gates_and_exact_references_approved',False)
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
        assert not calls and image.read_file(owned.PATH)==initial,label;results.append(dict(case=label,rejected=True,reason=reason,dependency_hashes_bypassed_for_semantic_challenge=True,no_archive_mutation=True))
        if number%25==0:print(f'{number}/{len(tests)} semantic rejection cases pass.',flush=True)
    save(ROOT/'negative_cases.json',dict(cases=results,count=len(results),all_rejected_before_archive_mutation=True,producer_sha256=sha(Path(__file__).read_bytes())));save(ROOT/'atomic_validation_receipt.json',dict(**{k:positive[k] for k in ['config','config_sha256','positive_proof','positive_proof_sha256','parent_ROM','parent_ROM_sha256','positive_records']},negative_cases=str(ROOT/'negative_cases.json'),negative_cases_sha256=sha((ROOT/'negative_cases.json').read_bytes()),negative_count=len(results),all_negatives_reject_before_mutation=True,all14_objects_reconstructed_with_one_archive_write=True,source884_full_inverse_and_all_other_components_exact=True,seven_actual_speeches_five_labels_two_offline_alternatives_bound=True,full_goal_complete=False));print(f'B212 atomic validation passed:{len(results)} independent semantic negatives reject before archive mutation.',flush=True)
