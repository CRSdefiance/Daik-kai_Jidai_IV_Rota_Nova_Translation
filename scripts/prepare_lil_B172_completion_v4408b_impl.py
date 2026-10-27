"""Prepare one-time B172 completion behind exact release and fresh startup gates."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B172_completion_tools_v4408b')
OLD=Path('scripts/complete_lil_B171_v4357.py')
NEW=Path('scripts/complete_lil_B172_v4408.py')
if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    text=OLD.read_text(encoding='utf-8')
    changes={
        'B171':'B172','completion_v4357':'completion_v4408','completion_text_v4357':'completion_text_v4408',
        'editorial_manuscript_v5':'editorial_manuscript_v4','release_v4354':'release_v4405','startup_v4356':'startup_v4407',
        'actual_v4342/actual_all37_dream_morning_presentations_resource_C200_and_first_end':'actual_v4394/actual_all27_presentations_resources_C200_A000_and_end',
        'transition_review_v4345/all7_sheets_dream_morning_C200_and_paired_return_review':'transition_review_v4398/all5_sheets_departure_C200_A000_and_paired_return_review',
        'work/analysis/lil_B171_timing_count_amendment_v4349/amendment_receipt.json':'work/analysis/lil_B172_reference_checkpoint_v4400/checkpoint_receipt.json',
        'registration_v4352':'registration_v4403',
        'Lil-B171-Sanghyeon-dream-visit-expulsion-siblinglike-bond-training-work37':'Lil-B172-Julian-Mihwa-Silla-crown-conditional-date-independent-search27',
        'all547_manifest_batches_and114_accepted_layers_present':'all548_manifest_batches_and114_accepted_layers_present',
        'all_current_requested_and_final_framebuffers_equal_V4303':'all_current_requested_and_final_framebuffers_equal_V4353',
        'actual37_progressive_panels_dream_morning_resource_C200_first_end_and_normal_town_return_pass':'actual27_progressive_panels_departure_resources_C200_A000_single_end_and_normal_town_return_pass',
        ' and not actual[\'paired_region_differences\']':" and len(actual['paired_region_differences'])==1",
        "reg['negative_count'] == 63":"reg['negative_count'] == 69",
        '[171]':'[172]','block=171':'block=172','actual_source_event171_selected':'actual_source_event172_selected',
        'source_prose_credit_already_recorded_in_V4329':'source_prose_credit_already_recorded_in_V4379',
        '# Current editorial handoff - V4349':'# Current editorial handoff - V4400',
        'B172-B180':'B173-B180','remaining_B172_B180':'remaining_B173_B180',
        "['lil_B171_v4329']":"['lil_B172_v4379']","['lil_B171_v4357']":"['lil_B172_v4408']",
        'unfinished_editorial_scope_v4347':'unfinished_editorial_scope_v4400','unfinished_editorial_scope_v4357':'unfinished_editorial_scope_v4408',
        'lil_B171_completed_v4357':'lil_B172_completed_v4408',
        'release_tools_v4353':'release_tools_v4404','V4357':'V4408','V4353':'V4404',
        'manifest_batches=547':'manifest_batches=548',
        "'lil_B171_command_timing_count_amendment_v4349'":"'lil_B171_command_timing_count_amendment_v4349', 'promoted_main_build_v4392'",
        "planned.write_bytes((json.dumps(ledger, ensure_ascii=False, indent=2) + '\\n').replace('\\n', '\\r\\n').encode('utf-8'))":"planned.write_bytes(encode_ledger(ledger))",
        'import json':'import json\nfrom scripts.editorial_ledger_storage_v1 import encode_ledger',
    }
    for key in changes:assert key in text,key
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m[0]],text)
    numbers={'5725':'5762','5762':'5789','5765':'5792','3659':'3678','2103':'2111','3909':'3936','4163':'4190','37':'27','24':'19','13':'8','161':'134'}
    text=re.sub(r'(?<!\d)(?:'+'|'.join(numbers)+r')(?!\d)',lambda m:numbers[m[0]],text)
    assert not re.search(r'\[171\]|== 171|block=171|all37|indent=2',text)
    compile(text,str(NEW),'exec');NEW.write_text(text,encoding='utf-8',newline='\n')
    tools=[dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),successor=str(NEW),successor_sha256=sha(NEW.read_bytes()))]
    tools.append(derive('scripts/apply_lil_B171_completion_v4357.py','scripts/apply_lil_B172_completion_v4408.py',{'lil_B171_completion_v4357':'lil_B172_completion_v4408'}))
    tools.append(derive('scripts/seal_lil_B171_completion_v4357.py','scripts/seal_lil_B172_completion_v4408.py',{
        'B171':'B172','lil_B171_completion_v4357':'lil_B172_completion_v4408',
        '(5762, 5762, 0)':'(5789, 5789, 0)','(5765, 5762, 3659, 2103)':'(5792, 5789, 3678, 2111)',
        'V4357 completion sealed:5762 integrated,37 B171 completions,source/prose5765 unchanged.':'V4408 completion sealed:5789 integrated,27 B172 completions,source/prose5792 unchanged.',
    }))
    tools.append(derive('scripts/pin_lil_B171_v4357.py','scripts/pin_lil_B172_v4408.py',{
        'all_routes_combined_v4353':'all_routes_combined_v4404','lil_B171_reference_v4335':'lil_B172_reference_v4384',
        'lil_B171_display_v4340':'lil_B172_display_v4389','lil_B171_release_v4354':'lil_B172_release_v4405','B171 V4353':'B172 V4404',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,expected_completed=5789,expected_pending=0,source_prose_unchanged=5792,
        revised=19,retained=8,new_completed_records=27,atomic_negatives=69,registered_startup_pairs=31,
        emulator_runs_in_family=6,completion_execution_pending_release_and_startup=True,promoted_V4353_unchanged=True,full_goal_complete=False))
    print('Prepared B172 completion producers;27 completion credits remain gated on registered release,exact patch and fresh startup.')
