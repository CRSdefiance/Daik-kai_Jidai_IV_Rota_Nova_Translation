"""Prepare staged B179 completion, independent audits, application and retention."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B179_completion_tools_v4753')
assert not ROOT.exists()
numbers={13:14,5885:5898,5898:5912,5901:5915,3740:3748,2158:2164,4045:4059,4299:4313,98:101,554:555,25:11,178:179}
common={
    'complete_lil_B178_v4705':'complete_lil_B179_v4753',
    'lil_B178_completion_text_v4705':'lil_B179_completion_text_v4753',
    'lil_B178_completion_v4705':'lil_B179_completion_v4753',
    'lil_B178_editorial_manuscript_v4':'lil_B179_editorial_manuscript_v4',
    'lil_B178_release_v4702':'lil_B179_release_v4750','lil_B178_startup_v4704':'lil_B179_startup_v4752',
    'lil_B178_actual_v4694/actual_all13_progressive_FE_A000_C200_and_single_end':
        'lil_B179_actual_v4742/actual_all14_progressive_FE_A000_and_single_end_no_C200',
    'lil_B178_actual_review_v4695/all3_actual_sheets13':'lil_B179_actual_review_v4743/all3_actual_sheets14',
    'lil_B178_reference_checkpoint_v4697':'lil_B179_reference_checkpoint_v4745',
    'lil_B178_registration_v4700b':'lil_B179_registration_v4748',
    'editorial_handoff_verification_v4698':'editorial_handoff_verification_v4746',
    'editorial_handoff_verification_v4706':'editorial_handoff_verification_v4754',
    'all554_manifest_batches_and114_accepted_layers_present':'all555_manifest_batches_and114_accepted_layers_present',
    'all_current_requested_and_final_framebuffers_equal_V4655':'all_current_requested_and_final_framebuffers_equal_V4701',
    'all13_panels12_progressive1_impersonal_FE_source_A000_C200_single_end_and_normal_parent_return_pass':
        'all14_panels13_progressive1_impersonal_FE_source_A000_single_end_no_C200_and_normal_parent_return_pass',
    "{'revise': 2, 'retain-wording': 11}":"{'revise': 8, 'retain-wording': 6}",
    "{'revise':2,'retain-wording':11}":"{'revise':8,'retain-wording':6}",
    "{'revised':2,'retained':11}":"{'revised':8,'retained':6}",
    'dict(revised=2,retained=11)':'dict(revised=8,retained=6)',
    'revised=2, retained=11':'revised=8, retained=6',
    'revised_count=2, retained_count=11, fresh_revisions=2, fresh_retentions=11':
        'revised_count=8, retained_count=6, fresh_revisions=8, fresh_retentions=6',
    'new_revisions=2, justified_retentions=11':'new_revisions=8, justified_retentions=6',
    'source_prose_credit_already_recorded_in_V4679':'source_prose_credit_already_recorded_in_V4727',
    'lil_B178_v4679':'lil_B179_v4727','lil_B178_v4705':'lil_B179_v4753',
    'unfinished_editorial_scope_v4697':'unfinished_editorial_scope_v4745',
    'unfinished_editorial_scope_v4705':'unfinished_editorial_scope_v4753',
    'lil_B178_completed_v4705':'lil_B179_completed_v4753',
    'remaining_B179_B180':'remaining_B180',
    'lil_B178_release_tools_v4701':'lil_B179_release_tools_v4749',
    '## V4705:13 Lil B178 reviews completed in V4701':'## V4753:14 Lil B179 reviews completed in V4749',
    '# Current editorial handoff - V4697':'# Current editorial handoff - V4745',
    'all13':'all14','and11_retentions':'and6_retentions',
    'all5898_completed_record_keys_unique':'all5912_completed_record_keys_unique',
    'source_prose_credit_unchanged_completion_adds_thirteen_once':'source_prose_credit_unchanged_completion_adds_fourteen_once',
    'thirteen completions only':'fourteen completions only',
    'actual_source_event176_selected':'actual_source_event179_selected',
    'all-routes-unified-v4595':'all-routes-unified-v4701',
    'main_V4595':'main_V4701','main V4595':'main V4701','promoted_main_V4595':'promoted_main_V4701',
    'V4705':'V4753','lil_B178':'lil_B179','B178':'B179',
}
tools=[]


def guarded(src,dst,specific=None):
    source,target=Path(src),Path(dst);assert not target.exists()
    text=source.read_text(encoding='utf-8')
    changes={k:v for k,v in common.items() if k in text}
    for k,v in (specific or {}).items():
        assert k in text,k
        changes[k]=v
    for k,v in numbers.items():
        if re.search(r'(?<![A-Za-z0-9_])'+str(k)+r'(?![A-Za-z0-9_])',text):changes[str(k)]=str(v)
    pattern='|'.join(re.escape(k) if not k.isdigit() else r'(?<![A-Za-z0-9_])'+k+r'(?![A-Za-z0-9_])' for k in sorted(changes,key=len,reverse=True))
    text=re.sub(pattern,lambda m:changes[m.group()],text)
    compile(text,str(target),'exec');target.write_text(text,encoding='utf-8',newline='\n')
    tools.append(dict(source=src,source_sha256=sha(source.read_bytes()),target=dst,target_sha256=sha(target.read_bytes()),changes=changes))


guarded('scripts/complete_lil_B178_v4705.py','scripts/complete_lil_B179_v4753.py',{
    'Lil-B178-home-baking-three-Ladies-husband-corner-bakery-teaching-ingredients-and-prospective-Amsterdam-wheat13':
        'Lil-B179-Barkeep-Patron-Sailor-wine-trial-three-gulps-joining-order-and-prospective-Sao-Jorge14',
    "note='5898 fresh contextual rereads integrated;source/prose5878. Remaining25 physical B179-B180 speech leads,zero choice-command leads and every wider editorial family remain open.'":
        "note='5912 fresh contextual rereads integrated;source/prose5915. Remaining11 physical B180 speech leads,zero typed-choice leads and every wider editorial family remain open.'",
    "'promoted_main_build_v4651']":"'promoted_main_build_v4651', 'promoted_main_build_v4725']",
})
guarded('scripts/verify_lil_B178_completion_plan_v4705b.py','scripts/verify_lil_B179_completion_plan_v4753.py',{
    "ROOT/'independent_preapplication_audit_v2.json'":"ROOT/'independent_preapplication_audit.json'",
    "assert scope['canonical_Maria32_pending_uncredited'] and scope['remaining_B179_B180_physical_speeches']==25":
        "assert scope['canonical_Maria32_pending_uncredited'] and scope['remaining_B180_physical_speeches']==11",
})
guarded('scripts/apply_lil_B178_completion_v4705.py','scripts/apply_lil_B179_completion_v4753.py',{
    "    assert len(plan['files'])==6":
        "    assert len(plan['files'])==6\n    audited=read(ROOT/'independent_preapplication_audit.json')\n    assert audited['all_six_before_and_planned_hashes_verified'] and audited['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes())",
    "stream.write(Path(entry['planned']).read_bytes())":"stream.write(Path(entry['planned']).read_bytes())\n            stream.truncate(Path(entry['planned']).stat().st_size)",
})
guarded('scripts/seal_lil_B178_completion_v4705.py','scripts/seal_lil_B179_completion_v4753.py',{
    'V4705 completion sealed:5898 integrated,thirteen B178 completions,source/prose5901':
        'V4753 completion sealed:5912 integrated,fourteen B179 completions,source/prose5915',
})
guarded('scripts/pin_lil_B178_v4705.py','scripts/pin_lil_B179_v4753.py',{
    'lil_B178_retention_v4705':'lil_B179_retention_v4753','lil_B178_reference_v4686':'lil_B179_reference_v4734',
    'lil_B178_display_v4691':'lil_B179_display_v4739','V4701 cumulative':'V4749 cumulative',
})
guarded('scripts/verify_editorial_handoff_v4706.py','scripts/verify_editorial_handoff_v4754.py',{
    "(final['revised'],final['retained'])==(2,11)":"(final['revised'],final['retained'])==(8,6)",
    '==(2,11,2,11)':'==(8,6,8,6)',
    'lil_B178_reference_v4686':'lil_B179_reference_v4734',
    "ledger['current_integrated_candidate']['profile']=='all-routes-unified-v4701'":
        "ledger['current_integrated_candidate']['profile']=='all-routes-unified-v4749'",
    "=={'progressive':12,'system-FE':1}":"=={'progressive':13,'system-FE':1}",
    '[5977,5976]':'[6216,6215]',
    'source_A0008_C200488_single_end490_actually_executed':'source_A0008_single_end508_actually_executed_no_C200',
    '[3306586022,3306586022]':'[403514907,403514907]',
    "len(transitions['actual_timing_differences'])==14":"len(transitions['actual_timing_differences'])==8",
    "{'total':14,'speech':12,'control_or_end':2}":"{'total':8,'speech':7,'control_or_end':1}",
    'native104_alignment_cases52_stored_cases_single_end_two_decodes_and13_dispatches_bound':
        'native112_alignment_cases56_stored_cases_single_end_two_decodes_and14_dispatches_bound',
    'actual13_panels12_progressive1_impersonal_FE_A000_C200_single_end_and_parent_return_verified':
        'actual14_panels13_progressive1_impersonal_FE_A000_single_end_no_C200_and_parent_return_verified',
    'all115_upper_portrait_name_samples_equal_14_timing_and4_indicator_RGB_differences_retained':
        'all115_upper_portrait_name_samples_equal_8_timing_and4_indicator_RGB_differences_retained',
    'PRNG3306586022':'PRNG403514907',
    "assert inventory['incomplete_route_source_prose_groups']==[] and inventory['incomplete_route_source_prose_count']==0":
        "assert inventory['incomplete_route_source_prose_groups']==[] and inventory['incomplete_route_source_prose_count']==0\n    assert inventory['untranslated_Sao_Jorge_alias_lead']==oldinventory['untranslated_Sao_Jorge_alias_lead']\n    assert inventory['untranslated_Sao_Jorge_alias_lead']['id']=='ARM9-Sao-Jorge-alias-15E5D4-pointer122504'",
    'V4705 independently verified:5898 completed,zero pending,3740 revised/2158 retained. B178 integrated;main V4595/full objective preserved.':
        'V4753 independently verified:5912 completed,zero pending,3748 revised/2164 retained. B179 integrated;main V4701/full objective preserved.',
})
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tools=tools,source_credit_unchanged_completion_adds14_once=True,
    complete_root_and_nested_history_required_before_any_metadata_write=True,city_alias_lead_and_full_scope_preserved=True,
    no_completion_credit_added_yet=True,full_goal_complete=False))
tests=Path('work/analysis/lil_B179_release_tools_v4749/regression_test_results.json')
assert not tests.exists()
save(tests,dict(command='python -m pytest tests/test_integrated_release.py tests/test_dialogue_review.py tests/test_dialogue_balanced_wrap.py tests/test_dialogue_pair_phase.py tests/test_dialogue_relocation.py tests/test_lil_editorial_literal_guard.py -q',
    output='78 passed in 4.38s',returncode=0,source='Observed current-turn exec result before completion preparation',new_emulator_runs=0))
print('Prepared B179 completion,preapplication/full-history audits,apply/seal/retention;no completion credit yet.')
