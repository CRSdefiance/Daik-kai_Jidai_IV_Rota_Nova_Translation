"""Prepare final integrated-reference/accounting audit without weakening actual limits."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B177_completion_audit_tools_v4660')
assert not ROOT.exists()
source=Path('scripts/verify_editorial_handoff_v4600.py');target=Path('scripts/verify_editorial_handoff_v4660.py')
assert not target.exists()
text=source.read_text(encoding='utf-8')
a=text.index("    assert transitions['nontext_equal_samples']");b=text.index('    scope=ledger[',a)
transitions="""    assert transitions['nontext_equal_samples']==115 and not transitions['nontext_difference_samples']
    assert transitions['source_A0008_C200480_single_end482_actually_executed']
    assert transitions['whole_RGB_town5290_through5950_and_final9001_equal'] and transitions['whole_RGB_final9001_equal']
    assert transitions['postscene9001_whole1A04_actor_models_and_captain2_equal'] and all(transitions['postscene9001_native_component_equality'].values())
    assert not transitions['PRNG_equality'] and transitions['postscene9001_PRNG_seeds']==[463267532,403514907]
    assert len(transitions['actual_timing_differences'])==11
    assert transitions['exact_timing_difference_counts']=={'total':11,'speech':9,'control_or_end':2}
    assert len(transitions['fourteen_following_A_button_indicator_animation_differences_retained_unmasked'])==14
    assert transitions['fourteen_following_indicator_differences_viewed_in_representative_full_screens_and_retained']
    assert transitions['no_new_PRNG_causal_trace'] and transitions['future_world_equivalence_and_full_RAM_equality_not_claimed']
    assert transitions['following_B120_offset606_in_progress_at_end_adds_no_editorial_credit']
"""
changes={
    text[a:b]:transitions,
    'all115_nontext_samples22_command_timings_and_sampled_whole_RGB5290_through9001_equal=True':
        'all115_upper_portrait_name_samples_equal_11_timing_and14_indicator_RGB_differences_retained=True',
    'final_state_actor_captain_PRNG_equal_with_full_RAM_future_world_and_hardware_limits=True':
        'final_state_actor_captain_town_final_RGB_equal_unequal_PRNG_with_full_RAM_future_world_and_hardware_limits=True',
    'lil_B176_completion_v4599':'lil_B177_completion_v4659',
    'editorial_handoff_verification_v4600':'editorial_handoff_verification_v4660',
    'editorial_handoff_verification_v4592':'editorial_handoff_verification_v4652',
    'source_prose_credit_already_recorded_in_V4573':'source_prose_credit_already_recorded_in_V4623',
    'lil_B176_v4573':'lil_B177_v4623','lil_B176_v4599':'lil_B177_v4659',
    'all552_manifest_batches_and114_accepted_layers_present':'all553_manifest_batches_and114_accepted_layers_present',
    'all_current_requested_and_final_framebuffers_equal_V4541':'all_current_requested_and_final_framebuffers_equal_V4595',
    'lil_B176_release_tools_v4595':'lil_B177_release_tools_v4655',
    'lil_B176_reference_v4580':'lil_B177_reference_v4630',
    "['profile']=='all-routes-unified-v4595'":"['profile']=='all-routes-unified-v4655'",
    "read('translations/promoted_build.json')['profile']=='all-routes-unified-v4541'":
        "read('translations/promoted_build.json')['profile']=='all-routes-unified-v4595'",
    '==[5256,5256]':'==[5255,5257]',
    'remaining_B177_B180_physical_speeches':'remaining_B178_B180_physical_speeches',
    'unfinished_editorial_scope_v4591':'unfinished_editorial_scope_v4641',
    'unfinished_editorial_scope_v4599':'unfinished_editorial_scope_v4659',
    'lil_B176_completed_v4599':'lil_B177_completed_v4659',
    'V4599':'V4659','B176':'B177','V4541':'V4595',
}
numbers={5875:5885,5878:5888,3733:3738,2142:2147,4022:4032,4276:4286,84:95,552:553,48:38,176:177}
changes.update({str(k):str(v) for k,v in numbers.items()})
for key in changes:assert key in text,key
pattern='|'.join(re.escape(k) if not k.isdigit() else r'(?<![A-Za-z0-9_])'+k+r'(?![A-Za-z0-9_])' for k in sorted(changes,key=len,reverse=True))
text=re.sub(pattern,lambda m:changes[m.group()],text)
compile(text,str(target),'exec');target.write_text(text,encoding='utf-8',newline='\n')
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(previous=str(source),previous_sha256=sha(source.read_bytes()),
    successor=str(target),successor_sha256=sha(target.read_bytes()),full_historical_accounting_preserved=True,
    exact_source_predecessor_integrated_references_and_five_retentions_required=True,
    measured11_timings14_indicator_differences_and_unequal_PRNG_preserved=True,
    no_completion_credit_added=True,full_goal_complete=False))
print('Prepared final B177 accounting/source-reference/history audit;no completion claim yet.')
