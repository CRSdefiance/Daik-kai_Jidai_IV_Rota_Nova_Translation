"""Prepare B171 completion; preserve full scope and gate every credit on release/startup."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B171_completion_tools_v4357')
OLD=Path('scripts/complete_lil_B170_v4307b.py')
NEW=Path('scripts/complete_lil_B171_v4357.py')
if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    text=OLD.read_text(encoding='utf-8')
    changes={
        'B170':'B171','lil_B170':'lil_B171','completion_v4307':'completion_v4357','completion_text_v4307':'completion_text_v4357',
        'editorial_manuscript_v6':'editorial_manuscript_v5','release_v4304':'release_v4354','startup_v4306':'startup_v4356',
        'actual_v4293/actual_all33_pause_resources_A000_C200_and_first_end':'actual_v4342/actual_all37_dream_morning_presentations_resource_C200_and_first_end',
        'transition_review_v4297/all6_sheets_figure_pause_effect_C200_and_paired_return_review':'transition_review_v4345/all7_sheets_dream_morning_C200_and_paired_return_review',
        'work/analysis/lil_B170_reference_checkpoint_v4299/checkpoint_receipt.json':'work/analysis/lil_B171_timing_count_amendment_v4349/amendment_receipt.json',
        'registration_v4302b':'registration_v4352',
        'Lil-B170-Yifa-collision-apology-Taoist-training-resolve-joining33':'Lil-B171-Sanghyeon-dream-visit-expulsion-siblinglike-bond-training-work37',
        'all546_manifest_batches_and114_accepted_layers_present':'all547_manifest_batches_and114_accepted_layers_present',
        'all_current_requested_and_final_framebuffers_equal_V4251':'all_current_requested_and_final_framebuffers_equal_V4303',
        'actual33_progressive_panels_figure_pause_resources_A000_C200_first_end_and_normal_town_return_pass':'actual37_progressive_panels_dream_morning_resource_C200_first_end_and_normal_town_return_pass',
        '[170]':'[171]','block=170':'block=171','actual_source_event170_selected':'actual_source_event171_selected',
        'source_prose_credit_already_recorded_in_V4279':'source_prose_credit_already_recorded_in_V4329',
        '# Current editorial handoff - V4299':'# Current editorial handoff - V4349',
        'B171-B180':'B172-B180','remaining_B171_B180':'remaining_B172_B180',
        "['lil_B170_v4279']":"['lil_B171_v4329']","['lil_B170_v4307']":"['lil_B171_v4357']",
        'unfinished_editorial_scope_v4299':'unfinished_editorial_scope_v4347','unfinished_editorial_scope_v4307':'unfinished_editorial_scope_v4357',
        'lil_B170_completed_v4307':'lil_B171_completed_v4357',
        'release_tools_v4303':'release_tools_v4353','V4307':'V4357','V4303':'V4353',
        'manifest_batches=546':'manifest_batches=547',
        "'promoted_main_build_v4289']":"'promoted_main_build_v4289', 'promoted_main_build_v4331', 'lil_B171_command_timing_count_amendment_v4349']",
    }
    for key in changes:assert key in text,key
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group()],text)
    counts={'5692':'5725','5725':'5762','5728':'5765','3635':'3659','2090':'2103','3872':'3909','4126':'4163','33':'37','21':'24','12':'13','198':'161'}
    text=re.sub(r'(?<!\d)(?:'+'|'.join(re.escape(k) for k in sorted(counts,key=len,reverse=True))+r')(?!\d)',lambda m:counts[m.group()],text)
    assert 'B170' not in text and 'lil_B170' not in text and '[170]' not in text
    compile(text,str(NEW),'exec');NEW.write_text(text,encoding='utf-8',newline='\n')
    tools=[dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),successor=str(NEW),successor_sha256=sha(NEW.read_bytes()))]
    tools.append(derive('scripts/apply_lil_B170_completion_v4307.py','scripts/apply_lil_B171_completion_v4357.py',{
        'lil_B170_completion_v4307':'lil_B171_completion_v4357',
    }))
    tools.append(derive('scripts/seal_lil_B170_completion_v4307.py','scripts/seal_lil_B171_completion_v4357.py',{
        'B170':'B171','lil_B170_completion_v4307':'lil_B171_completion_v4357',
        '(5725, 5725, 0)':'(5762, 5762, 0)','(5728, 5725, 3635, 2090)':'(5765, 5762, 3659, 2103)',
        'V4307 completion sealed:5725 integrated,33 B170 completions,source/prose5728 unchanged.':'V4357 completion sealed:5762 integrated,37 B171 completions,source/prose5765 unchanged.',
    }))
    tools.append(derive('scripts/pin_lil_B170_v4307.py','scripts/pin_lil_B171_v4357.py',{
        'all_routes_combined_v4303':'all_routes_combined_v4353',
        'lil_B170_reference_v4284':'lil_B171_reference_v4335','lil_B170_display_v4291':'lil_B171_display_v4340',
        'lil_B170_release_v4304':'lil_B171_release_v4354','B170 V4303':'B171 V4353',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,expected_completed=5762,expected_pending=0,expected_source_prose_unchanged=5765,
        revised=24,retained=13,new_completed_records=37,required_atomic_negative_count=63,required_registered_startup_pairs=31,
        expected_emulator_runs_in_family=6,completion_execution_pending_release_and_startup=True,promoted_V4303_unchanged=True,full_goal_complete=False))
    print('Prepared B171 completion producers;37 completion credits remain gated on registered release,exact patch and fresh startup.')
