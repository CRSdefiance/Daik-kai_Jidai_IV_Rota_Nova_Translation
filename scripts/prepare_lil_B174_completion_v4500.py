"""Prepare hash-staged B174 completion without broad numeric substitutions."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B174_completion_tools_v4500')
OLD=Path('scripts/complete_lil_B173_v4449.py')
NEW=Path('scripts/complete_lil_B174_v4500.py')
if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    text=OLD.read_text(encoding='utf-8')
    note=next(line for line in text.splitlines() if "note='5800 fresh contextual rereads integrated" in line)
    changes={
        note:"        note='5833 fresh contextual rereads integrated;source/prose5836. Remaining90 physical B175-B180 speech leads,zero choice-command leads and every wider editorial family remain open.')",
        'lil_B173_completion_text_v4449':'lil_B174_completion_text_v4500','lil_B173_completion_v4449':'lil_B174_completion_v4500',
        'lil_B173_editorial_manuscript_v4':'lil_B174_editorial_manuscript_v6',
        'lil_B173_release_v4446':'lil_B174_release_v4497','lil_B173_startup_v4448':'lil_B174_startup_v4499',
        'lil_B173_actual_v4438b/actual_all11_unforced_predicate_paths_effects_and_end':
            'lil_B174_actual_v4489c/actual_all33_unforced_predicate_paths_effects_C200_and_end',
        'lil_B173_actual_review_v4439/all2_actual_sheets_unforced_suffix_paired_return_and_final_state':
            'lil_B174_actual_review_v4490b/all6_actual_sheets_optional_scope_join_notice_paired_return_and_final_state',
        'lil_B173_reference_checkpoint_v4441':'lil_B174_reference_checkpoint_v4492','lil_B173_registration_v4444':'lil_B174_registration_v4495',
        'Lil-B173-Reika-crown-inquiry-uncertain-Julian-tomb-lead-competitive-search11':
            'Lil-B174-Julian-Mihwa-crown-gratitude-grandfather-aspiration-conditional-date33',
        'OFFLINE = set()':"OFFLINE = {'DK4_MES_B174_R0069'}",
        'all549_manifest_batches':'all550_manifest_batches','all_current_requested_and_final_framebuffers_equal_V4404':'all_current_requested_and_final_framebuffers_equal_V4445',
        "actual['complete_matching_observations'] == 11":"actual['complete_matching_observations'] == 32",
        "reg['negative_count'] == 81":"reg['negative_count'] == 92",
        "len(rows) == 11":"len(rows) == 33","{'revise': 8, 'retain-wording': 3}":"{'revise': 23, 'retain-wording': 10}",
        "not sample['offline_only_display_IDs'] and sample['all11_progressive_panels_unforced_predicate_both_effects_single_end_and_normal_town_return_pass']":
            "sample['offline_only_display_IDs']==sorted(OFFLINE) and sample['all32_unconditional_panels_unforced_predicate_both_effects_C200_single_end_and_normal_town_return_pass']",
        'len(sampled) == 11':'len(sampled) == 32','blocks[173]':'blocks[174]','block=173':'block=174','blocks=[173]':'blocks=[174]',
        'len(old_keys) == 5789 and len(selected) == 11':'len(old_keys) == 5800 and len(selected) == 33',
        '(5800, 5789, 11)':'(5833, 5800, 33)',
        "['records_with_source_and_prose_pass'] == 5803":"['records_with_source_and_prose_pass'] == 5836",
        "['/data/SC2.DK4'] == 3947":"['/data/SC2.DK4'] == 3980",
        '# Current editorial handoff - V4441':'# Current editorial handoff - V4492',
        'lil_B173_release_tools_v4445':'lil_B174_release_tools_v4496',
        'records=rows, revised_count=8, retained_count=3, fresh_revisions=8, fresh_retentions=3':
            'records=rows, revised_count=23, retained_count=10, fresh_revisions=23, fresh_retentions=10',
        'records_editorially_completed=5800, records_revised_and_integrated=3686, retained_wordings_editorially_completed=2114':
            'records_editorially_completed=5833, records_revised_and_integrated=3709, retained_wordings_editorially_completed=2124',
        "['/data/SC2.DK4'] = 3947":"['/data/SC2.DK4'] = 3980",
        'fresh_pass_records_integrated=5800':'fresh_pass_records_integrated=5833',
        'records=11, final_review=str(FINAL), new_revisions=8, justified_retentions=3':
            'records=33, final_review=str(FINAL), new_revisions=23, justified_retentions=10',
        'new_completed_records=11':'new_completed_records=33','dict(revised=8, retained=3)':'dict(revised=23, retained=10)',
        'reviewed_route_records=4201, completed_route_records=4201':'reviewed_route_records=4234, completed_route_records=4234',
        'completion_credit_added=11':'completion_credit_added=33',
        'lil_B173_v4426':'lil_B174_v4475','lil_B173_v4449':'lil_B174_v4500',
        'unfinished_editorial_scope_v4441':'unfinished_editorial_scope_v4492','unfinished_editorial_scope_v4449':'unfinished_editorial_scope_v4500',
        'completed_targets=11':'completed_targets=33','actual_unique_speeches=11':'actual_unique_speeches=32',
        'remaining_B174_B180_physical_speeches=123':'remaining_B175_B180_physical_speeches=90',
        'len(keys) == 5800':'len(keys) == 5833',"['records_with_source_prose_drafts'] == 5803":"['records_with_source_prose_drafts'] == 5836",
        'revised=8, retained=3, fresh_reread=5800, fresh_integrated=5800':'revised=23, retained=10, fresh_reread=5833, fresh_integrated=5833',
        'source_prose=5803, completed=5800, historical_revised=3686, historical_retained=2114':
            'source_prose=5836, completed=5833, historical_revised=3709, historical_retained=2124',
        'manifest_batches=549':'manifest_batches=550','actual_unique_speech_panels=11':'actual_unique_speech_panels=32',
        'V4449:11 Lil B173 reviews completed in V4445':'V4500:33 Lil B174 reviews completed in V4496',
        'B173':'B174','v4449':'v4500','V4449':'V4500','all11-source':'all33-source',
    }
    for key in changes:assert key in text,key
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m[0]],text)
    compile(text,str(NEW),'exec');NEW.write_text(text,encoding='utf-8',newline='\n')
    tools=[dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),successor=str(NEW),successor_sha256=sha(NEW.read_bytes()))]
    tools.append(derive('scripts/apply_lil_B173_completion_v4449.py','scripts/apply_lil_B174_completion_v4500.py',{
        'lil_B173_completion_v4449':'lil_B174_completion_v4500',
    }))
    tools.append(derive('scripts/seal_lil_B173_completion_v4449.py','scripts/seal_lil_B174_completion_v4500.py',{
        'lil_B173_completion_v4449':'lil_B174_completion_v4500','(5800, 5800, 0)':'(5833, 5833, 0)',
        '(5803, 5800, 3686, 2114)':'(5836, 5833, 3709, 2124)',
        'V4449 completion sealed:5800 integrated,11 B173 completions,source/prose5803 unchanged.':
            'V4500 completion sealed:5833 integrated,33 B174 completions,source/prose5836 unchanged.',
    }))
    tools.append(derive('scripts/pin_lil_B173_v4449.py','scripts/pin_lil_B174_v4500.py',{
        'all_routes_combined_v4445':'all_routes_combined_v4496','lil_B173_reference_v4431':'lil_B174_reference_v4482',
        'lil_B173_display_v4436':'lil_B174_display_v4487','lil_B173_release_v4446':'lil_B174_release_v4497','B173 V4445':'B174 V4496',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tools=tools,
        completed_reviews_expected=5833,source_prose_expected=5836,decisions=dict(revised=3709,retained=2124),
        actual32_offline1_preserved=True,all_earlier_main_promotions_and_history_preserved=True,
        no_completion_credit_until_release_and_startup_gates=True,full_goal_complete=False))
    print('Prepared B174 completion gates:33 new completions once,23 revisions/10 retentions,32 actual/one offline; no execution or credit yet.')
