"""Derive final B176 accounting, integrated references and complete-history verification."""
import re
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B176_completion_audit_tools_v4600')
assert not ROOT.exists()
source=Path('scripts/verify_editorial_handoff_v4546.py')
target=Path('scripts/verify_editorial_handoff_v4600.py')
assert not target.exists()
text=source.read_text(encoding='utf-8')
start=text.index("    assert transitions['nontext_equal_samples']")
end=text.index('    scope=ledger[',start)
old_transitions=text[start:end]
new_transitions="""    assert transitions['nontext_equal_samples']==115 and not transitions['nontext_difference_samples']
    assert transitions['source_A0008_C200384_single_end386_actually_executed']
    assert transitions['all_sampled_whole_RGB_from5290_through9001_equal'] and transitions['whole_RGB_final9001_equal']
    assert transitions['postscene9001_whole1A04_actor_models_and_captain2_equal'] and all(transitions['postscene9001_native_component_equality'].values())
    assert transitions['PRNG_equality'] and transitions['postscene9001_PRNG_seeds']==[403514907,403514907]
    assert not transitions['actual_timing_differences'] and transitions['future_world_equivalence_and_full_RAM_equality_not_claimed']
    assert transitions['following_B120_offset606_in_progress_at_end_adds_no_editorial_credit']
"""
start=text.index("    save(ROOT/'verified_handoff.json'")
old_tail=text[start:]
new_tail="""    save(ROOT/'verified_handoff.json',dict(checkpoint='V4599',ledger_sha256=sha(lp.read_bytes()),fresh_reread=5875,integrated=5875,pending=0,
        source_prose=5878,revised=3733,retained=2142,candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest_batches=552,accepted_layers=114,
        all10_source_predecessor_integrated_references_and5_retentions_verified=True,
        all_earlier_ledger_records_completions_and_full_objective_preserved=True,
        native80_alignment_cases40_stored_cases_single_end_two_decodes_and10_dispatches_bound=True,
        actual10_panels9_progressive1_impersonal_FE_A000_C200_single_end_and_town_return_verified=True,
        all115_nontext_samples22_command_timings_and_sampled_whole_RGB5290_through9001_equal=True,
        final_state_actor_captain_PRNG_equal_with_full_RAM_future_world_and_hardware_limits=True,
        current_startup31_whole_frames_and5_models_verified=True,candidate_whole_ROM_equal_reviewed_research_reference=True,
        atomic_compiler_negatives=84,regression_tests_passed=78,main_V4541_unchanged=True,
        remaining_B177_B180_physical_speeches=48,new_source_prose_reviews=0,new_completed_records=10,
        all_jobs_terminal=True,full_goal_active=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('V4599 independently verified:5875 completed,zero pending,3733 revised/2142 retained. B176 integrated;main V4541/full objective preserved.')
"""
replacements={
    old_transitions:new_transitions,old_tail:new_tail,
    'complete_lil_B175_v4545':'complete_lil_B176_v4599',
    'editorial_handoff_verification_v4546':'editorial_handoff_verification_v4600',
    'editorial_handoff_verification_v4538':'editorial_handoff_verification_v4592',
    'unfinished_editorial_scope_v4545':'unfinished_editorial_scope_v4599',
    'lil_B175_completion_v4545':'lil_B176_completion_v4599',
    'source_prose_credit_already_recorded_in_V4519':'source_prose_credit_already_recorded_in_V4573',
    'lil_B175_v4519':'lil_B176_v4573','lil_B175_v4545':'lil_B176_v4599',
    'all551_manifest_batches_and114_accepted_layers_present':'all552_manifest_batches_and114_accepted_layers_present',
    'all_current_requested_and_final_framebuffers_equal_V4496':'all_current_requested_and_final_framebuffers_equal_V4541',
    'lil_B175_release_tools_v4541':'lil_B176_release_tools_v4595',
    'lil_B175_reference_v4526':'lil_B176_reference_v4580',
    "['profile']=='all-routes-unified-v4541'":"['profile']=='all-routes-unified-v4595'",
    "read('translations/promoted_build.json')['profile']=='all-routes-unified-v4496'":
        "read('translations/promoted_build.json')['profile']=='all-routes-unified-v4541'",
    'actual_source_event175_selected':'actual_source_event176_selected',
    "=={'progressive':23,'system-FE':9}":"=={'progressive':9,'system-FE':1}",
    '==[10534,10535]':'==[5256,5256]',
    'remaining_B176_B180_physical_speeches':'remaining_B177_B180_physical_speeches',
    'unfinished_editorial_scope_v4537':'unfinished_editorial_scope_v4591',
    'lil_B175_completed_v4545':'lil_B176_completed_v4599',
    "inventory['lil_B175_completed_v4545']['actual_FE_panels']==9":"inventory['lil_B176_completed_v4599']['actual_FE_panels']==1",
    '# Current editorial handoff - V4545':'# Current editorial handoff - V4599',
    'B175':'B176',
}
numbers={32:10,19:5,13:5,175:176,82:84,5865:5875,5868:5878,4012:4022,3728:3733,2137:2142,4266:4276,58:48}
replacements.update({str(k):str(v) for k,v in numbers.items()})
for key in replacements:assert key in text,key
pattern='|'.join(re.escape(k) if not k.isdigit() else r'(?<![A-Za-z0-9_])'+k+r'(?![A-Za-z0-9_])' for k in sorted(replacements,key=len,reverse=True))
text=re.sub(pattern,lambda m:replacements[m.group()],text)
compile(text,str(target),'exec');target.write_text(text,encoding='utf-8',newline='\n')
tools=[dict(previous=str(source),previous_sha256=sha(source.read_bytes()),successor=str(target),successor_sha256=sha(target.read_bytes()))]
tools.append(derive('scripts/pin_lil_B175_v4545.py','scripts/pin_lil_B176_v4599.py',{
    'B175':'B176','lil_B175_retention_v4545':'lil_B176_retention_v4599',
    'lil_B175_release_v4542':'lil_B176_release_v4596','lil_B175_reference_v4526':'lil_B176_reference_v4580',
    'lil_B175_display_v4531':'lil_B176_display_v4585','V4541 cumulative':'V4595 cumulative',
}))
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tools=tools,full_historical_accounting_and_original_scope_required=True,
    no_completion_credit_added_yet=True,full_goal_complete=False))
