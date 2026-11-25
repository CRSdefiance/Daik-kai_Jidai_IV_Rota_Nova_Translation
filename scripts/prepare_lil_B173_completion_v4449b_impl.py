"""Prepare one-time B173 completion;numeric tokens never rewrite UTF-8 literals."""
from pathlib import Path
import io,re,tokenize
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B173_completion_tools_v4449b')
OLD=Path('scripts/complete_lil_B172_v4408.py')
NEW=Path('scripts/complete_lil_B173_v4449.py')
if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    text=OLD.read_text(encoding='utf-8')
    changes={
        'B172':'B173','completion_v4408':'completion_v4449','completion_text_v4408':'completion_text_v4449',
        'release_v4405':'release_v4446','startup_v4407':'startup_v4448',
        'actual_v4394/actual_all27_presentations_resources_C200_A000_and_end':'actual_v4438b/actual_all11_unforced_predicate_paths_effects_and_end',
        'transition_review_v4398/all5_sheets_departure_C200_A000_and_paired_return_review':'actual_review_v4439/all2_actual_sheets_unforced_suffix_paired_return_and_final_state',
        'reference_checkpoint_v4400':'reference_checkpoint_v4441','registration_v4403':'registration_v4444',
        'Lil-B172-Julian-Mihwa-Silla-crown-conditional-date-independent-search27':'Lil-B173-Reika-crown-inquiry-uncertain-Julian-tomb-lead-competitive-search11',
        'all548_manifest_batches_and114_accepted_layers_present':'all549_manifest_batches_and114_accepted_layers_present',
        'all_current_requested_and_final_framebuffers_equal_V4353':'all_current_requested_and_final_framebuffers_equal_V4404',
        "len(actual['paired_region_differences'])==1":"not actual['paired_region_differences']",
        "reg['negative_count'] == 69":"reg['negative_count'] == 81",
        "{'revise': 19, 'retain-wording': 8}":"{'revise': 8, 'retain-wording': 3}",
        'actual27_progressive_panels_departure_resources_C200_A000_single_end_and_normal_town_return_pass':'all11_progressive_panels_unforced_predicate_both_effects_single_end_and_normal_town_return_pass',
        'source_prose_credit_already_recorded_in_V4379':'source_prose_credit_already_recorded_in_V4426',
        '# Current editorial handoff - V4400':'# Current editorial handoff - V4441',
        'B173-B180':'B174-B180','remaining_B173_B180':'remaining_B174_B180',
        "['lil_B172_v4379']":"['lil_B173_v4426']","['lil_B172_v4408']":"['lil_B173_v4449']",
        'unfinished_editorial_scope_v4400':'unfinished_editorial_scope_v4441','unfinished_editorial_scope_v4408':'unfinished_editorial_scope_v4449',
        'lil_B172_completed_v4408':'lil_B173_completed_v4449','focused_repeat_proof':'postscene_native_state_proof',
        'release_tools_v4404':'release_tools_v4445','V4408':'V4449','V4404':'V4445',
        'manifest_batches=548':'manifest_batches=549','new_focused_repeat_runs=2':'new_focused_repeat_runs=0',
        'new_emulator_runs=6':'new_emulator_runs=4','new_actual_emulator_runs=6':'new_actual_emulator_runs=4',
        'actual_source_event172_selected':'actual_source_event173_selected',
    }
    for key in changes:assert key in text,key
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m[0]],text)
    # Change decision fields explicitly;other eight-valued source/layout data stays intact.
    for a,b in [('revised=19, retained=8','revised=8, retained=3'),('revised_count=19, retained_count=8','revised_count=8, retained_count=3'),
        ('fresh_revisions=19, fresh_retentions=8','fresh_revisions=8, fresh_retentions=3'),('new_revisions=19, justified_retentions=8','new_revisions=8, justified_retentions=3'),
]:
        assert a in text,a;text=text.replace(a,b)
    numbers={'5762':'5789','5789':'5800','5792':'5803','3678':'3686','2111':'2114','3936':'3947','4190':'4201','27':'11','134':'123','172':'173'}
    tokens=[]
    for token in tokenize.generate_tokens(io.StringIO(text).readline):
        if token.type==tokenize.NUMBER and token.string in numbers:token=token._replace(string=numbers[token.string])
        tokens.append(token)
    text=tokenize.untokenize(tokens).replace('all27','all11')
    text=text.replace('5789 fresh contextual rereads integrated;source/prose5792. Remaining134 physical B174-B180',
        '5800 fresh contextual rereads integrated;source/prose5803. Remaining123 physical B174-B180')
    text=text.replace('V4449:27 Lil B173 reviews','V4449:11 Lil B173 reviews')
    assert 'encode_ledger(ledger)' in text and 'utf-8' in text and 'utf-3' not in text
    assert not re.search(r'\[172\]|== 172|block=172|all27|focused_repeat_proof',text)
    compile(text,str(NEW),'exec');NEW.write_text(text,encoding='utf-8',newline='\n')
    tools=[dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),successor=str(NEW),successor_sha256=sha(NEW.read_bytes()))]
    tools.append(derive('scripts/apply_lil_B172_completion_v4408.py','scripts/apply_lil_B173_completion_v4449.py',{'lil_B172_completion_v4408':'lil_B173_completion_v4449'}))
    tools.append(derive('scripts/seal_lil_B172_completion_v4408.py','scripts/seal_lil_B173_completion_v4449.py',{
        'B172':'B173','lil_B172_completion_v4408':'lil_B173_completion_v4449',
        '(5789, 5789, 0)':'(5800, 5800, 0)','(5792, 5789, 3678, 2111)':'(5803, 5800, 3686, 2114)',
        'V4408 completion sealed:5789 integrated,27 B172 completions,source/prose5792 unchanged.':'V4449 completion sealed:5800 integrated,11 B173 completions,source/prose5803 unchanged.',
    }))
    tools.append(derive('scripts/pin_lil_B172_v4408.py','scripts/pin_lil_B173_v4449.py',{
        'all_routes_combined_v4404':'all_routes_combined_v4445','lil_B172_reference_v4384':'lil_B173_reference_v4431',
        'lil_B172_display_v4389':'lil_B173_display_v4436','lil_B172_release_v4405':'lil_B173_release_v4446','B172 V4404':'B173 V4445',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,expected_completed=5800,expected_pending=0,source_prose_unchanged=5803,
        revised=8,retained=3,new_completed_records=11,atomic_negatives=81,registered_startup_pairs=31,
        emulator_runs_in_family=4,completion_execution_pending_release_and_startup=True,promoted_V4353_unchanged=True,full_goal_complete=False))
    print('Prepared B173 completion producers;11 completion credits gated on registered release,exact patch and fresh startup.')
