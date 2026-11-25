"""Prepare positive and atomic rejection tests before registering cumulative B174."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B174_registration_tools_v4495')
SOURCE=Path('scripts/register_lil_B173_v4444.py')
TARGET=Path('scripts/register_lil_B174_v4495.py')
if __name__=='__main__':
    assert not ROOT.exists() and not TARGET.exists()
    text=SOURCE.read_text(encoding='utf-8')
    a=text.index('    profile.update(status=');b=text.index("    registry['profiles'][PROFILE]",a)
    text=text[:a]+'''    profile.update(status='experimental',lil_B174_editorial=owned.CONFIG,
        description='Full V4445 cumulative stack plus33 B174 crown/grandfather-aspiration/conditional-date reviews:23 revisions/10 retentions,45 commands,eight numeric leaves,four relative sites/20 target cases,one predicate,two A000s and C200. Two16001-frame unforced content boots observe32 unconditional panels,result0,both effects,C200,single end andnormal town return;232 nontext regions match. Optional Emilio R69 retains offline native coverage. Actual source/target skip extents52/62 and VM last-result0 are explicit. Exported postscene state is compared without PRNG/future-world equality or natural eligibility claims.',
        note='B174 source/native/reference/representative approved;registered build,exact patch andfresh startup pending.')
''' + text[b:]
    # Replace known literal fault injections with faults in the new source scope.
    changes={
        'all-routes-unified-v4445':'all-routes-unified-v4496','all_routes_combined_v4404':'all_routes_combined_v4445',
        'all-routes-unified-v4404':'all-routes-unified-v4445','all-routes-unified-v4353':'all-routes-unified-v4445',
        'registration_v4444':'registration_v4495','build_integrated_release_v4444.tmp':'build_integrated_release_v4495.tmp',
        'editorial_manuscript_v4':'editorial_manuscript_v6','lil_B173_layout_v1':'lil_B174_layout_v2',
        'reference_checkpoint_v4441':'reference_checkpoint_v4492','reference_approval_v4440':'reference_approval_v4491',
        'loader_v4432':'loader_v4483','editorial_handoff_verification_v4442b':'editorial_handoff_verification_v4493',
        'actual_review_v4439/all2_actual_sheets_unforced_suffix_paired_return_and_final_state':
            'actual_review_v4490b/all6_actual_sheets_optional_scope_join_notice_paired_return_and_final_state',
        "len(proof['changed_records']) == 11":"len(proof['changed_records']) == 33",
        "english='{SPEAKER:CA}Hello.'":"english='{SPEAKER:02}Hello.'",
        'Reika_selector_as_text':'Mihwa_selector_as_text',"english='Reika says hello.'":"english='Mihwa says hello.'",
        'source_resource20_boundary_cases_reused_only_by_exact_words_and_runtime':'source_resource10_boundary_cases_reused_only_by_exact_words_and_runtime',
        'native_four_consumer_cases':'native_eight_consumer_cases',"r['actor_ID']==202":"r['actor_ID']==201",'invented_Reika':'invented_Mihwa',
        'single_end762_actual':'single_end2086_actual',
        'source_relative_sites736740756_actual_744_offline_native_only':'source_relative_sites882890_actual_886894938_offline_native_only',
        'actual_VM_descriptor_last_result1_preserved_through_type3_and_end':'actual_VM_descriptor_last_result0_preserved_through_type3_C200_and_end',
        'postscene9001_whole1A04_actor_models_and_captain2_equal':'postscene16001_whole1A04_actor_models_and_captain2_equal',
        'postscene9001_native_component_equality':'postscene16001_native_component_equality',
        'actual_all11_unforced_predicate_paths_effects_and_end':'actual_all33_unforced_predicate_paths_effects_C200_and_end',
        "version['single_source_end_offset']=766":"version['single_source_end_offset']=2090",
        "version['actual_predicate']['result_words']=[2,0]":"version['actual_predicate']['result_words']=[2,1]",
        "version['source_A000_hex_by_offset']['748']":"version['source_A000_hex_by_offset']['2076']",
        "version['actual_source_A000s'][1]['result_words']=[3,0]":"version['actual_source_A000s'][1]['result_words']=[3,1]",
        "version['selected_B22_command_pairs'][-1]['result_words']=[0,0]":"version['selected_B22_command_pairs'][-1]['result_words']=[0,1]",
        "version['actual_source_relative_commands'][0]['result_words']=[3,0]":"version['actual_source_relative_commands'][0]['result_words']=[3,1]",
        'reset_actual_effect_last_result':'invent_actual_effect_last_result','reset_actual_end_last_result':'invent_actual_end_last_result',
        'reset_actual_relative_last_result':'invent_actual_relative_last_result',
        'after_full_V4404':'after_full_V4445','V4404 stack':'V4445 stack',
        'expected_manifest_batches=549':'expected_manifest_batches=550','expected_batches=549':'expected_batches=550','positive_records=11':'positive_records=33',
        'B173':'B174',
    }
    for key in changes:assert key in text,key
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m[0]],text)
    # Source-native predicate result1 and actual fixture result0 are intentionally distinct.
    marker="    for macro in ['FI','FA','FO']:"
    assert text.count(marker)==1
    text=text.replace(marker,'''    mutations.extend([
        ('invented_actual_Emilio','manuscript',lambda v:next(r for r in v['records'] if r['source_record_index']==69).update(actual_B22_display_fixture_observed=True)),
        ('lost_Emilio_UI_boundary','manuscript',lambda v:next(r for r in v['records'] if r['source_record_index']==69).update(current_native_UI_body_explicit_unexecuted_boundary=False)),
        ('missing_C200_pair','relocated_control_proof',lambda v:v['relocated_C200_pairs'].pop()),
        ('wrong_C200_request','relocated_control_proof',lambda v:v['relocated_C200_pairs'][0]['cases'][1].update(source_owned_UI_request_words=[1,0,14,0,0,0,1])),
        ('wrong_C200_ownership','relocated_control_proof',lambda v:v['relocated_C200_pairs'][0]['cases'][1].update(all_other4MiB_actor_roster_event_RNG_and_models_exact=False)),
        ('lost_join_notice_first_J','postscene_native_state_proof',lambda v:v.update(join_notice_leading_J_full_Julian_Lopes_and_trailing_exclamation_viewed=False)),
        ('wrong_join_indicator_scope','postscene_native_state_proof',lambda v:v.update(join_notice_full_RGB_difference_is_original_A_button_indicator=[0,0,256,384])),
        ('lost_native_exact_reuse_scope','native_font_proof',lambda v:v.update(reused_original_macro_alignment_calls=0)),
    ])
''' + marker)
    old="        elif label=='wrong_actual_resource':version['actual_resources'][0]['word']=0x6326"
    assert old in text
    text=text.replace(old,old+'''
        elif label=='wrong_actual_C200':version['actual_source_C200'][0]['result_words']=[3,1]
        elif label=='wrong_actual_skip_extent':version['actual_source_relative_commands'][1]['extent']+=2
        elif label=='missing_actual_offline_scope':actual['offline_only_display_IDs']=[]''')
    old="'invent_actual_effect_last_result','invent_actual_end_last_result','invent_actual_relative_last_result','missing_actual_version'])"
    assert old in text
    text=text.replace(old,"'invent_actual_effect_last_result','invent_actual_end_last_result','invent_actual_relative_last_result','missing_actual_version', 'wrong_actual_C200','wrong_actual_skip_extent','missing_actual_offline_scope'])")
    compile(text,str(TARGET),'exec');TARGET.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'derivation.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),target=str(TARGET),
        target_sha256=sha(TARGET.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),
        optional_actual_scope_C200_owned_writes_relocated_extents_and_join_notice_negatives=True,
        positive_and_all_negatives_precede_registry_builder_writes=True,expected_batches=550,full_goal_complete=False))
    print('Prepared B174 atomic registration and distinct conditional/C200/notice rejection controls; expected550 batches, main V4445 preserved.')
