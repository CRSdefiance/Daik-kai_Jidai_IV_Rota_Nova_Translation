"""Prepare guarded B176 completion with quantity substitutions kept out of identifiers."""
import re
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B176_completion_tools_v4599')
assert not ROOT.exists()
source=Path('scripts/complete_lil_B175_v4545.py')
target=Path('scripts/complete_lil_B176_v4599.py')
assert not target.exists()
text=source.read_text(encoding='utf-8')
replacements={
    'Lil-B175-pirate-encirclement-pride-sea-challenge-unnamed-sword-and-banter32':
        'Lil-B176-banana-age-Owner-Cook-doubt-purchase-order-and-prospective-Seville-fashion10',
    'lil_B175_completion_v4545':'lil_B176_completion_v4599',
    'lil_B175_completion_text_v4545':'lil_B176_completion_text_v4599',
    'lil_B175_contextual_final_review':'lil_B176_contextual_final_review',
    'lil_B175_editorial_manuscript_v4':'lil_B176_editorial_manuscript_v4',
    'lil_B175_release_v4542':'lil_B176_release_v4596','lil_B175_startup_v4544':'lil_B176_startup_v4598',
    'lil_B175_actual_v4534/actual_all32_progressive_FE_controls_C200_and_first_end':
        'lil_B176_actual_v4588/actual_all10_progressive_FE_A000_C200_and_single_end',
    'lil_B175_actual_review_v4535/all6_actual_sheets_32_planes_scoped_transitions_return_and_final_state':
        'lil_B176_actual_review_v4589/all2_actual_sheets10_planes_fullscreens_return_and_final_state',
    'lil_B175_reference_checkpoint_v4537':'lil_B176_reference_checkpoint_v4591',
    'lil_B175_registration_v4540b':'lil_B176_registration_v4594',
    'all551_manifest_batches_and114_accepted_layers_present':'all552_manifest_batches_and114_accepted_layers_present',
    'all_current_requested_and_final_framebuffers_equal_V4496':'all_current_requested_and_final_framebuffers_equal_V4541',
    'all32_panels23_progressive9_FE_three_presentations_resource_C200_first_end_and_normal_town_return_pass':
        'all10_panels9_progressive1_impersonal_FE_source_A000_C200_single_end_and_normal_town_return_pass',
    "effective == body.replace(b'FI', b'Lil').replace(b'FA', b'Argot').replace(b'FO', b'Argot Co.')":
        "effective == body and not any(m in body for m in [b'FI',b'FA',b'FO'])",
    'source_prose_credit_already_recorded_in_V4519':'source_prose_credit_already_recorded_in_V4573',
    'all32_exact_source_predecessor_runtime_logical_and_integrated_references_bound':'all10_exact_source_predecessor_runtime_logical_and_integrated_references_bound',
    'actual_source_event175_selected':'actual_source_event176_selected',
    'actual_selected_B175_source_events':'actual_selected_B176_source_events',
    'lil_B175_v4519':'lil_B176_v4573','lil_B175_v4545':'lil_B176_v4599',
    'unfinished_editorial_scope_v4537':'unfinished_editorial_scope_v4591',
    'unfinished_editorial_scope_v4545':'unfinished_editorial_scope_v4599',
    'lil_B175_completed_v4545':'lil_B176_completed_v4599',
    'remaining_B176_B180':'remaining_B177_B180',
    'actual_FE_panels=9':'actual_FE_panels=1',
    'lil_B175_release_tools_v4541':'lil_B176_release_tools_v4595',
    "'promoted_main_build_v4512']":"'promoted_main_build_v4512', 'promoted_main_build_v4571']",
    "note='5865 fresh contextual rereads integrated;source/prose5868. Remaining58 physical B176-B180 speech leads,zero choice-command leads and every wider editorial family remain open.'":
        "note='5875 fresh contextual rereads integrated;source/prose5878. Remaining48 physical B177-B180 speech leads,zero choice-command leads and every wider editorial family remain open.'",
    '## V4545:32 Lil B175 reviews completed in V4541':'## V4599:10 Lil B176 reviews completed in V4595',
    'all32-source-native-reference-representative-release-checks-pass':'all10-source-native-reference-representative-release-checks-pass',
    'V4537':'V4591','V4545':'V4599','B175':'B176',
}
numbers={32:10,19:5,13:5,175:176,82:84,551:552,5833:5865,5865:5875,5868:5878,
         4012:4022,3728:3733,2137:2142,4266:4276,58:48}
replacements.update({str(k):str(v) for k,v in numbers.items()})
pattern='|'.join(re.escape(k) if not k.isdigit() else r'(?<![A-Za-z0-9_])'+k+r'(?![A-Za-z0-9_])' for k in sorted(replacements,key=len,reverse=True))
for k in replacements:
    assert k in text,k
text=re.sub(pattern,lambda m:replacements[m.group()],text)
compile(text,str(target),'exec')
target.write_text(text,encoding='utf-8',newline='\n')
tools=[dict(previous=str(source),previous_sha256=sha(source.read_bytes()),successor=str(target),successor_sha256=sha(target.read_bytes()))]
tools.append(derive('scripts/apply_lil_B175_completion_v4545.py','scripts/apply_lil_B176_completion_v4599.py',{
    'lil_B175_completion_v4545':'lil_B176_completion_v4599',
}))
tools.append(derive('scripts/seal_lil_B175_completion_v4545.py','scripts/seal_lil_B176_completion_v4599.py',{
    'lil_B175_completion_v4545':'lil_B176_completion_v4599',
    '(5865, 5865, 0)':'(5875, 5875, 0)','(5868, 5865, 3728, 2137)':'(5878, 5875, 3733, 2142)',
    'V4545 completion sealed:5865 integrated,32 B175 completions,source/prose5868':
        'V4599 completion sealed:5875 integrated,ten B176 completions,source/prose5878',
}))
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tools=tools,revised=5,retained=5,actual=10,FE=1,
    registered_release_startup_gates_required_before_execution=True,no_completion_credit_added=True,full_goal_complete=False))
