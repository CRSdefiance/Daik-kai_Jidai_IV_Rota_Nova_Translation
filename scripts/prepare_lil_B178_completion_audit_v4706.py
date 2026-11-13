"""Prepare final B178 accounting, exact integrated references and complete-history audit."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B178_completion_audit_tools_v4706');assert not ROOT.exists()
source=Path('scripts/verify_editorial_handoff_v4660.py');target=Path('scripts/verify_editorial_handoff_v4706.py')
assert not target.exists();text=source.read_text(encoding='utf-8')
a=text.index("    assert transitions['nontext_equal_samples']");b=text.index('    scope=ledger[',a)
transitions="""    assert transitions['nontext_equal_samples']==115 and not transitions['nontext_difference_samples']
    assert transitions['source_A0008_C200488_single_end490_actually_executed']
    assert transitions['sampled_postscene_whole_RGB_equal_except_four_original_A_indicator_frames'] and transitions['whole_RGB_final9001_equal']
    assert transitions['postscene9001_whole1A04_actor_models_and_captain2_equal'] and all(transitions['postscene9001_native_component_equality'].values())
    assert transitions['PRNG_equality'] and transitions['postscene9001_PRNG_seeds']==[3306586022,3306586022]
    assert len(transitions['actual_timing_differences'])==14 and transitions['exact_timing_difference_counts']=={'total':14,'speech':12,'control_or_end':2}
    assert [(r['frame'],r['whole_frame_difference_bbox']) for r in transitions['sampled_postscene_whole_RGB_differences_unmasked']]==[
        (6970,[224,360,240,371]),(7150,[224,360,240,371]),(7930,[224,360,240,376]),(8110,[224,360,240,376])]
    assert transitions['all_four_following_indicator_differences_viewed_in_full_and_retained']
    assert transitions['no_new_PRNG_causal_trace'] and transitions['future_world_equivalence_and_full_RAM_equality_not_claimed']
    assert transitions['following_scene_adds_no_editorial_credit']
    assert [(r['pending'][0]['block'],r['pending'][0]['offset'],r['pending'][0]['start'])
        for r in transitions['following_observed_blocks_and_unreturned_commands']]==[(120,352,8376),(120,352,8375)]
"""
changes={
    text[a:b]:transitions,
    'complete_lil_B177_v4659':'complete_lil_B178_v4705','lil_B177_completion_v4659':'lil_B178_completion_v4705',
    'editorial_handoff_verification_v4660':'editorial_handoff_verification_v4706','editorial_handoff_verification_v4652':'editorial_handoff_verification_v4698',
    'source_prose_credit_already_recorded_in_V4623':'source_prose_credit_already_recorded_in_V4679',
    'lil_B177_v4623':'lil_B178_v4679','lil_B177_v4659':'lil_B178_v4705',
    'unfinished_editorial_scope_v4659':'unfinished_editorial_scope_v4705','unfinished_editorial_scope_v4641':'unfinished_editorial_scope_v4697',
    'lil_B177_completed_v4659':'lil_B178_completed_v4705',
    "(final['revised'],final['retained'])==(5,5)":"(final['revised'],final['retained'])==(2,11)",
    '==(5,5,5,5)':'==(2,11,2,11)',"{'revise':5,'retain-wording':5}":"{'revise':2,'retain-wording':11}",
    'dict(revised=5,retained=5)':'dict(revised=2,retained=11)',
    'all553_manifest_batches_and114_accepted_layers_present':'all554_manifest_batches_and114_accepted_layers_present',
    'all_current_requested_and_final_framebuffers_equal_V4595':'all_current_requested_and_final_framebuffers_equal_V4655',
    'lil_B177_release_tools_v4655':'lil_B178_release_tools_v4701','lil_B177_reference_v4630':'lil_B178_reference_v4686',
    "ledger['current_integrated_candidate']['profile']=='all-routes-unified-v4655'":"ledger['current_integrated_candidate']['profile']=='all-routes-unified-v4701'",
    "=={'progressive':9,'system-FE':1}":"=={'progressive':12,'system-FE':1}",
    '==[5255,5257]':'==[5977,5976]',
    'remaining_B178_B180_physical_speeches':'remaining_B179_B180_physical_speeches',
    'native80_alignment_cases40_stored_cases_single_end_two_decodes_and10_dispatches_bound':
        'native104_alignment_cases52_stored_cases_single_end_two_decodes_and13_dispatches_bound',
    'all10_source_predecessor_integrated_references_and5_retentions_verified':'all13_source_predecessor_integrated_references_and11_retentions_verified',
    'actual10_panels9_progressive1_impersonal_FE_A000_C200_single_end_and_town_return_verified':
        'actual13_panels12_progressive1_impersonal_FE_A000_C200_single_end_and_parent_return_verified',
    'all115_upper_portrait_name_samples_equal_11_timing_and14_indicator_RGB_differences_retained':
        'all115_upper_portrait_name_samples_equal_14_timing_and4_indicator_RGB_differences_retained',
    'final_state_actor_captain_town_final_RGB_equal_unequal_PRNG_with_full_RAM_future_world_and_hardware_limits':
        'final_state_actor_captain_PRNG3306586022_and_final_RGB_equal_with_four_indicator_differences_full_RAM_future_world_and_hardware_limits',
    'V4659':'V4705','B177':'B178',
}
for k in changes:assert k in text,k
numbers={10:13,5885:5898,5888:5901,3738:3740,2147:2158,4032:4045,4286:4299,95:98,553:554,38:25,177:178}
for k,v in numbers.items():
    if re.search(r'(?<![A-Za-z0-9_])'+str(k)+r'(?![A-Za-z0-9_])',text):changes[str(k)]=str(v)
pattern='|'.join(re.escape(k) if not k.isdigit() else r'(?<![A-Za-z0-9_])'+k+r'(?![A-Za-z0-9_])' for k in sorted(changes,key=len,reverse=True))
text=re.sub(pattern,lambda m:changes[m.group()],text)
compile(text,str(target),'exec');target.write_text(text,encoding='utf-8',newline='\n')
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(previous=str(source),previous_sha256=sha(source.read_bytes()),successor=str(target),successor_sha256=sha(target.read_bytes()),
    source_predecessor_integrated_references_and11_retentions_required=True,all_root_nested_history_and_objective_preserved=True,
    actual14_timings4_indicator_differences_and_equal_PRNG_bound=True,no_completion_credit_added=True,full_goal_complete=False))
print('Prepared final B178 accounting,all13 integrated references/11 retentions and complete-history audit.')
