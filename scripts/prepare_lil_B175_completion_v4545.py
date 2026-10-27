"""Prepare source-bound B175 completion/apply/seal producers without granting credit."""
import re
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B175_completion_tools_v4545')
if __name__=='__main__':
    target=Path('scripts/complete_lil_B175_v4545.py');assert not ROOT.exists() and not target.exists()
    source=Path('scripts/complete_lil_B174_v4500b.py');text=source.read_text(encoding='utf-8')
    replacements={
        'Lil-B174-Julian-Mihwa-crown-gratitude-grandfather-aspiration-conditional-date33':
            'Lil-B175-pirate-encirclement-pride-sea-challenge-unnamed-sword-and-banter32',
        'lil_B174_completion_v4500':'lil_B175_completion_v4545','lil_B174_completion_text_v4500':'lil_B175_completion_text_v4545',
        'lil_B174_contextual_final_review':'lil_B175_contextual_final_review','lil_B174_editorial_manuscript_v6':'lil_B175_editorial_manuscript_v4',
        'lil_B174_release_v4497':'lil_B175_release_v4542','lil_B174_startup_v4499':'lil_B175_startup_v4544',
        'lil_B174_actual_v4489c/actual_all33_unforced_predicate_paths_effects_C200_and_end':
            'lil_B175_actual_v4534/actual_all32_progressive_FE_controls_C200_and_first_end',
        'lil_B174_actual_review_v4490b/all6_actual_sheets_optional_scope_join_notice_paired_return_and_final_state':
            'lil_B175_actual_review_v4535/all6_actual_sheets_32_planes_scoped_transitions_return_and_final_state',
        'lil_B174_reference_checkpoint_v4492':'lil_B175_reference_checkpoint_v4537',
        'lil_B174_registration_v4495':'lil_B175_registration_v4540b',
        "OFFLINE = {'DK4_MES_B174_R0069'}":"OFFLINE = set()",
        'all_current_requested_and_final_framebuffers_equal_V4445':'all_current_requested_and_final_framebuffers_equal_V4496',
        'all32_unconditional_panels_unforced_predicate_both_effects_C200_single_end_and_normal_town_return_pass':
            'all32_panels23_progressive9_FE_three_presentations_resource_C200_first_end_and_normal_town_return_pass',
        'all11_exact_source_predecessor_runtime_logical_and_integrated_references_bound':'all32_exact_source_predecessor_runtime_logical_and_integrated_references_bound',
        'source_prose_credit_already_recorded_in_V4475':'source_prose_credit_already_recorded_in_V4519',
        'actual_source_event174_selected':'actual_source_event175_selected',
        'lil_B174_v4475':'lil_B175_v4519','lil_B174_v4500':'lil_B175_v4545',
        'unfinished_editorial_scope_v4492':'unfinished_editorial_scope_v4537',
        'remaining_B175_B180':'remaining_B176_B180','B175-B180':'B176-B180',
        'actual_FE_panels=0':'actual_FE_panels=9',
        'lil_B174_release_tools_v4496':'lil_B175_release_tools_v4541',
        "'promoted_main_build_v4452']":"'promoted_main_build_v4452', 'promoted_main_build_v4512']",
        'V4492':'V4537','V4500':'V4545','v4500':'v4545','V4496':'V4541','B174':'B175',
    }
    # Do not remap inserted B176 scope strings or old promotion history keys.
    numbers={33:32,23:19,10:13,174:175,92:82,550:551,5800:5833,5833:5865,5836:5868,3980:4012,
        3709:3728,2124:2137,4234:4266,90:58}
    replacements.update({str(k):str(v) for k,v in numbers.items()})
    pattern='|'.join(re.escape(k) if not k.isdigit() else r'(?<!\d)'+k+r'(?!\d)' for k in sorted(replacements,key=len,reverse=True))
    text=re.sub(pattern,lambda m:replacements[m.group()],text)
    compile(text,str(target),'exec');target.write_text(text,encoding='utf-8',newline='\n')
    tools=[dict(previous=str(source),previous_sha256=sha(source.read_bytes()),successor=str(target),successor_sha256=sha(target.read_bytes()))]
    tools.append(derive('scripts/apply_lil_B174_completion_v4500.py','scripts/apply_lil_B175_completion_v4545.py',{
        'lil_B174_completion_v4500':'lil_B175_completion_v4545',
    }))
    tools.append(derive('scripts/seal_lil_B174_completion_v4500.py','scripts/seal_lil_B175_completion_v4545.py',{
        'lil_B174_completion_v4500':'lil_B175_completion_v4545','(5833, 5833, 0)':'(5865, 5865, 0)',
        '(5836, 5833, 3709, 2124)':'(5868, 5865, 3728, 2137)',
        'V4500 completion sealed:5833 integrated,33 B174 completions,source/prose5836':'V4545 completion sealed:5865 integrated,32 B175 completions,source/prose5868',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tools=tools,revised=19,retained=13,actual=32,FE=9,
        registered_release_startup_gates_required_before_execution=True,no_completion_credit_added=True,full_goal_complete=False))
    print('Prepared B175 completion/apply/seal gates:32 complete/19 revisions/13 retentions;no execution or credit yet.')
