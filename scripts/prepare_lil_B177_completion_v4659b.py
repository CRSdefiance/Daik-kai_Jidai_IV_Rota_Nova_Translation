"""Prepare source-credit-preserving B177 completion after the main promotion."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B177_completion_tools_v4659')
assert not ROOT.exists()
source=Path('scripts/complete_lil_B176_v4599.py');target=Path('scripts/complete_lil_B177_v4659.py')
assert target.exists()
text=source.read_text(encoding='utf-8')
changes={
    'Lil-B176-banana-age-Owner-Cook-doubt-purchase-order-and-prospective-Seville-fashion10':
        'Lil-B177-tomato-red-passion-youthful-love-dry-Cook-cook-sell-and-prospective-Genoa-fashion10',
    'lil_B176_completion_v4599':'lil_B177_completion_v4659',
    'lil_B176_completion_text_v4599':'lil_B177_completion_text_v4659',
    'lil_B176_editorial_manuscript_v4':'lil_B177_editorial_manuscript_v6',
    'lil_B176_release_v4596':'lil_B177_release_v4656','lil_B176_startup_v4598':'lil_B177_startup_v4658',
    'lil_B176_actual_v4588':'lil_B177_actual_v4638','lil_B176_actual_review_v4589':'lil_B177_actual_review_v4639',
    'lil_B176_reference_checkpoint_v4591':'promotion_v4651b',
    'checkpoint_receipt.json':'promotion_receipt.json',
    'lil_B176_registration_v4594':'lil_B177_registration_v4654',
    'all552_manifest_batches_and114_accepted_layers_present':'all553_manifest_batches_and114_accepted_layers_present',
    'all_current_requested_and_final_framebuffers_equal_V4541':'all_current_requested_and_final_framebuffers_equal_V4595',
    'source_prose_credit_already_recorded_in_V4573':'source_prose_credit_already_recorded_in_V4623',
    'lil_B176_v4573':'lil_B177_v4623','lil_B176_v4599':'lil_B177_v4659',
    'unfinished_editorial_scope_v4591':'unfinished_editorial_scope_v4641',
    'unfinished_editorial_scope_v4599':'unfinished_editorial_scope_v4659',
    'lil_B176_completed_v4599':'lil_B177_completed_v4659',
    'remaining_B177_B180':'remaining_B178_B180',
    'lil_B176_release_tools_v4595':'lil_B177_release_tools_v4655',
    "'promoted_main_build_v4571']":"'promoted_main_build_v4571', 'promoted_main_build_v4651']",
    '## V4599:10 Lil B176 reviews completed in V4595':'## V4659:10 Lil B177 reviews completed in V4655',
    '# Current editorial handoff - V4591':'# Current editorial handoff - V4651',
    '# Current editorial handoff - V4599':'# Current editorial handoff - V4659',
    "prior['updated_files'][str(path)]":"prior['updated_files'][path.as_posix()]",
    'V4599':'V4659','lil_B176':'lil_B177','B176':'B177',
    'Remaining48 physical B177-B180':'Remaining38 physical B178-B180',
}
numbers={5865:5875,5875:5885,5878:5888,3733:3738,2142:2147,4022:4032,4276:4286,48:38,84:95,552:553,176:177}
changes.update({str(k):str(v) for k,v in numbers.items()})
for key in changes:assert key in text,key
pattern='|'.join(re.escape(k) if not k.isdigit() else r'(?<![A-Za-z0-9_])'+k+r'(?![A-Za-z0-9_])' for k in sorted(changes,key=len,reverse=True))
text=re.sub(pattern,lambda m:changes[m.group()],text)
compile(text,str(target),'exec');assert target.read_text(encoding='utf-8')==text
tools=[dict(previous=str(source),previous_sha256=sha(source.read_bytes()),successor=str(target),successor_sha256=sha(target.read_bytes()))]
tools.append(derive('scripts/verify_lil_B176_completion_plan_v4599.py','scripts/verify_lil_B177_completion_plan_v4659.py',{
    'lil_B176_completion_v4599':'lil_B177_completion_v4659','B176':'B177',
    'lil_B176':'lil_B177',
    '(5875,5878,3733,2142)':'(5885,5888,3738,2147)',
    '==5875':'==5885','all5875_completed_record_keys_unique':'all5885_completed_record_keys_unique',
    '==4276':'==4286','lil_B176_v4573':'lil_B177_v4623',
    'remaining_B177_B180_physical_speeches':'remaining_B178_B180_physical_speeches','==48':'==38',
    'unfinished_editorial_scope_v4591':'unfinished_editorial_scope_v4641',
    "==84":"==95",'lil_B176_release_tools_v4595':'lil_B177_release_tools_v4655',
    'all-routes-unified-v4541':'all-routes-unified-v4595','promoted_main_V4541':'promoted_main_V4595',
}))
tools.append(derive('scripts/apply_lil_B176_completion_v4599.py','scripts/apply_lil_B177_completion_v4659.py',{
    'lil_B176_completion_v4599':'lil_B177_completion_v4659',
}))
tools.append(derive('scripts/seal_lil_B176_completion_v4599.py','scripts/seal_lil_B177_completion_v4659.py',{
    'lil_B176_completion_v4599':'lil_B177_completion_v4659',
    '(5875, 5875, 0)':'(5885, 5885, 0)','(5878, 5875, 3733, 2142)':'(5888, 5885, 3738, 2147)',
    'V4599 completion sealed:5875 integrated,ten B176 completions,source/prose5878':
        'V4659 completion sealed:5885 integrated,ten B177 completions,source/prose5888',
}))
tools.append(derive('scripts/pin_lil_B176_v4599.py','scripts/pin_lil_B177_v4659.py',{
    'B176':'B177','lil_B176_retention_v4599':'lil_B177_retention_v4659',
    'lil_B176_release_v4596':'lil_B177_release_v4656','lil_B176_reference_v4580':'lil_B177_reference_v4630',
    'lil_B176_display_v4585':'lil_B177_display_v4635','V4595 cumulative':'V4655 cumulative',
}))
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tools=tools,full_promotion_and_history_preserved=True,
    completion_adds_ten_once_no_new_source_credit=True,registered_release_and_startup_gates_required=True,
    no_completion_credit_added_yet=True,full_goal_complete=False))
print('Prepared B177 completion staging/deep preapplication audit/seal/retention;current metadata unchanged.')
