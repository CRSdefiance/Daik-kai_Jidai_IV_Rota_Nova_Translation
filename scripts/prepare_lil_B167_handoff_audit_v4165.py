"""Derive an independent final audit of source, predecessor, integrated bytes and coverage."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B167_handoff_audit_tools_v4165')
TARGET=Path('scripts/verify_editorial_handoff_v4165.py')
if __name__=='__main__':
    assert not ROOT.exists() and not TARGET.exists();source=Path('scripts/verify_editorial_handoff_v4115.py');text=source.read_text(encoding='utf-8')
    changes={
        'editorial_handoff_verification_v4115':'editorial_handoff_verification_v4165','lil_B166_completion_v4114':'lil_B167_completion_v4164',
        'Lil-B166-Manuel-ship-care-recruitment-optional-Workroom-advice44':'Lil-B167-Shipwright-complete-sail-lesson-accept-refuse29',
        'lil_B166_release_v4111':'lil_B167_release_v4161','all_routes_combined_v4046':'all_routes_combined_v4110',
        'all-routes-unified-v4110':'all-routes-unified-v4160','lil_B166_editorial_release_v1':'lil_B167_editorial_release_v1',
        "(2952,2972)":"(2176,2052)","['Please do','Decline']":"['Okay','No thanks']",
        'actual_advice_choice_result_observed':'actual_menu_choice_result_observed','[2,9,20,23]':'[2,4,13,23,109]',
        "row['id']!='DK4_MES_B166_R0087'":"row['id'] not in {'DK4_MES_B167_R0045','DK4_MES_B167_R0131'}",
        "row['id']=='DK4_MES_B166_R0087'":"row['id'] in {'DK4_MES_B167_R0045','DK4_MES_B167_R0131'}",
        "['DK4_MES_B166_R0087']":"['DK4_MES_B167_R0045','DK4_MES_B167_R0131']",
        "stored['current_final_stored_macro_alignment_cases'] == 168":"stored['current_final_stored_macro_alignment_cases'] == 108",
        "len(controls['relocated_dispatch_cases']) == 42 and len(controls['relocated_predicate_pairs']) == 1":"len(controls['relocated_dispatch_cases']) == 27 and len(controls['relocated_predicate_pairs']) == 2",
        "len(controls['all11_source_current_target_nonrelative_nonspeech_nonchoice_leaves']) == 11":"len(controls['all6_source_current_target_nonrelative_nonspeech_nonchoice_leaves']) == 6",
        "len(block['command_map']) == 62 and len(block['relative_skip_fixups']) == 8 and len(block['target_native_skip_cases']) == 40":"len(block['command_map']) == 46 and len(block['relative_skip_fixups']) == 12 and len(block['target_native_skip_cases']) == 60",
        "== [2948]":"== [430,2172]",
        'lil_B166_actual_v4104/actual_both_choices_conditional_panels_and_single_return':'lil_B167_actual_v4151/actual_both_choices_conditional_panels_and_distinct_returns',
        'lil_B166_transition_review_v4105/both_choices_all7_sheets_Manuel_names_figures_and_paired_returns_review':'lil_B167_transition_review_v4152/both_choices_all5_sheets_static_names_and_distinct_returns_review',
        'all7_actual_sheets_viewed':'all5_actual_sheets_viewed',"== 7 and len(transition['English_full_screen_views']) == 11":"== 5 and len(transition['English_full_screen_views']) == 8",
        'lil_B166_startup_v4113':'lil_B167_startup_v4163','all_current_requested_and_final_framebuffers_equal_V4046':'all_current_requested_and_final_framebuffers_equal_V4110',
        'lil_B166_registration_v4109':'lil_B167_registration_v4159b','unfinished_editorial_scope_v4114':'unfinished_editorial_scope_v4164',
        "scope['remaining_choice_command_leads'] == 1":"scope['remaining_choice_command_leads'] == 0",
        'all44':'all29','all62_commands8_spans40_skips168_stored_cases_predicate_resources_single_end_and_names_bound':'all46_commands12_spans60_skips108_stored_cases_two_queries_resources_two_ends_and_names_bound',
        'actual_four_B22_fixtures41_unique73_observations_both_choices_and_returns_verified':'actual_four_B22_fixtures25_unique28_observations_both_choices_and_distinct_returns_verified',
        'conditional_Fernando_remark_explicitly_offline_only':'two_conditional_Cesare_remarks_explicitly_offline_only',
        'remaining_B167_B180':'remaining_B168_B180','remaining_choice_command_leads=1':'remaining_choice_command_leads=0',
        'V4114':'V4164','B166':'B167','event166':'event167','manifest_batches=541':'manifest_batches=543','541/114':'543/114'
    }
    for old in changes:assert old in text,old
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group(0)],text)
    nums={5573:5602,5576:5605,3551:3567,2022:2035,3720:3749,3974:4003,44:29,24:16,20:13,42:27,541:543,41:25,73:28,72:78,348:321,166:167}
    text=re.sub(r'\b('+ '|'.join(map(str,nums))+r')\b',lambda m:str(nums[int(m.group(0))]),text)
    assert 'B166' not in text and 'Fernando' not in text
    compile(text,str(TARGET),'exec');TARGET.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(previous=str(source),previous_sha256=sha(source.read_bytes()),successor=str(TARGET),successor_sha256=sha(TARGET.read_bytes()),all_source_predecessor_integrated_macro_native_actual_registry_patch_startup_scope_and_count_requirements_retained=True,no_audit_or_completion_claim_yet=True))
