"""Prepare guarded thirteen-record completion without duplicate source/prose credit."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B178_completion_tools_v4705');assert not ROOT.exists()


def guarded(source,target,changes,numbers):
    source,target=Path(source),Path(target);assert not target.exists()
    text=source.read_text(encoding='utf-8')
    for k in changes:assert k in text,k
    for k,v in numbers.items():
        if re.search(r'(?<![A-Za-z0-9_])'+str(k)+r'(?![A-Za-z0-9_])',text):changes[str(k)]=str(v)
    pattern='|'.join(re.escape(k) if not k.isdigit() else r'(?<![A-Za-z0-9_])'+k+r'(?![A-Za-z0-9_])' for k in sorted(changes,key=len,reverse=True))
    text=re.sub(pattern,lambda m:changes[m.group()],text)
    compile(text,str(target),'exec');target.write_text(text,encoding='utf-8',newline='\n')
    return dict(previous=str(source),previous_sha256=sha(source.read_bytes()),successor=str(target),successor_sha256=sha(target.read_bytes()))


tools=[guarded('scripts/complete_lil_B177_v4659.py','scripts/complete_lil_B178_v4705.py',{
    'Lil-B177-tomato-red-passion-youthful-love-dry-Cook-cook-sell-and-prospective-Genoa-fashion10':
        'Lil-B178-home-baking-three-Ladies-husband-corner-bakery-teaching-ingredients-and-prospective-Amsterdam-wheat13',
    'lil_B177_completion_v4659':'lil_B178_completion_v4705','lil_B177_completion_text_v4659':'lil_B178_completion_text_v4705',
    'lil_B177_editorial_manuscript_v6':'lil_B178_editorial_manuscript_v4',
    'lil_B177_release_v4656':'lil_B178_release_v4702','lil_B177_startup_v4658':'lil_B178_startup_v4704',
    'lil_B177_actual_v4638/actual_all10':'lil_B178_actual_v4694/actual_all13',
    'lil_B177_actual_review_v4639/all2_actual_sheets10':'lil_B178_actual_review_v4695/all3_actual_sheets13',
    'promotion_v4651b/promotion_receipt.json':'lil_B178_reference_checkpoint_v4697/checkpoint_receipt.json',
    'lil_B177_registration_v4654':'lil_B178_registration_v4700b',
    "prior['updated_files'][path.as_posix()]":"prior['updated_files'][str(path)]",
    'all553_manifest_batches_and114_accepted_layers_present':'all554_manifest_batches_and114_accepted_layers_present',
    'all_current_requested_and_final_framebuffers_equal_V4595':'all_current_requested_and_final_framebuffers_equal_V4655',
    'all10_panels9_progressive1_impersonal_FE_source_A000_C200_single_end_and_normal_town_return_pass':
        'all13_panels12_progressive1_impersonal_FE_source_A000_C200_single_end_and_normal_parent_return_pass',
    "{'revise': 5, 'retain-wording': 5}":"{'revise': 2, 'retain-wording': 11}",
    'source_prose_credit_already_recorded_in_V4623':'source_prose_credit_already_recorded_in_V4679',
    'all10_exact_source_predecessor_runtime_logical_and_integrated_references_bound':'all13_exact_source_predecessor_runtime_logical_and_integrated_references_bound',
    'revised=5, retained=5':'revised=2, retained=11',
    'revised_count=5, retained_count=5, fresh_revisions=5, fresh_retentions=5':'revised_count=2, retained_count=11, fresh_revisions=2, fresh_retentions=11',
    'new_revisions=5, justified_retentions=5':'new_revisions=2, justified_retentions=11',
    'lil_B177_v4623':'lil_B178_v4679','lil_B177_v4659':'lil_B178_v4705',
    'unfinished_editorial_scope_v4641':'unfinished_editorial_scope_v4697','unfinished_editorial_scope_v4659':'unfinished_editorial_scope_v4705',
    'lil_B177_completed_v4659':'lil_B178_completed_v4705','remaining_B178_B180':'remaining_B179_B180',
    'lil_B177_release_tools_v4655':'lil_B178_release_tools_v4701',
    '## V4659:10 Lil B177 reviews completed in V4655':'## V4705:13 Lil B178 reviews completed in V4701',
    '# Current editorial handoff - V4651':'# Current editorial handoff - V4697',
    'all10-source-native-reference-representative-release-checks-pass':'all13-source-native-reference-representative-release-checks-pass',
    'Remaining38 physical B178-B180':'Remaining25 physical B179-B180',
    'V4659':'V4705','lil_B177':'lil_B178','B177':'B178',
},{10:13,5875:5885,5885:5898,5888:5901,3738:3740,2147:2158,4032:4045,4286:4299,95:98,553:554,38:25,177:178})]

tools.append(guarded('scripts/verify_lil_B177_completion_plan_v4659b.py','scripts/verify_lil_B178_completion_plan_v4705.py',{
    'complete_lil_B177_v4659':'complete_lil_B178_v4705','lil_B177_completion_v4659':'lil_B178_completion_v4705',
    'unfinished_editorial_scope_v4659':'unfinished_editorial_scope_v4705','unfinished_editorial_scope_v4641':'unfinished_editorial_scope_v4697',
    'lil_B177_completed_v4659':'lil_B178_completed_v4705','lil_B177_v4623':'lil_B178_v4679','lil_B177_v4659':'lil_B178_v4705',
    "{'revise':5,'retain-wording':5}":"{'revise':2,'retain-wording':11}",
    "{'revised':5,'retained':5}":"{'revised':2,'retained':11}",
    'dict(revised=5,retained=5)':'dict(revised=2,retained=11)',
    'remaining_B178_B180':'remaining_B179_B180',
    'all5885_completed_record_keys_unique':'all5898_completed_record_keys_unique',
    'lil_B177_release_tools_v4655':'lil_B178_release_tools_v4701','lil_B177':'lil_B178','B177':'B178',
},{10:13,5885:5898,5888:5901,3738:3740,2147:2158,4286:4299,95:98,38:25} ))
tools.append(derive('scripts/apply_lil_B177_completion_v4659.py','scripts/apply_lil_B178_completion_v4705.py',{
    'lil_B177_completion_v4659':'lil_B178_completion_v4705',
}))
tools.append(derive('scripts/seal_lil_B177_completion_v4659.py','scripts/seal_lil_B178_completion_v4705.py',{
    'lil_B177_completion_v4659':'lil_B178_completion_v4705',
    '(5885, 5885, 0)':'(5898, 5898, 0)','(5888, 5885, 3738, 2147)':'(5901, 5898, 3740, 2158)',
    'V4659 completion sealed:5885 integrated,ten B177 completions,source/prose5888':
        'V4705 completion sealed:5898 integrated,thirteen B178 completions,source/prose5901',
}))
tools.append(derive('scripts/pin_lil_B177_v4659.py','scripts/pin_lil_B178_v4705.py',{
    'B177':'B178','lil_B177_retention_v4659':'lil_B178_retention_v4705',
    'lil_B177_release_v4656':'lil_B178_release_v4702','lil_B177_reference_v4630':'lil_B178_reference_v4686',
    'lil_B177_display_v4635':'lil_B178_display_v4691','V4655 cumulative':'V4701 cumulative',
}))
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tools=tools,revised=2,retained=11,actual=13,FE=1,
    full_root_and_nested_history_required_before_any_metadata_write=True,source_credit_unchanged_completion_adds13_once=True,
    registered_release_and_current_startup_gates_required=True,no_completion_credit_added_yet=True,full_goal_complete=False))
print('Prepared B178 completion/staged deep audit/apply/seal/retention;no completion credit yet.')
