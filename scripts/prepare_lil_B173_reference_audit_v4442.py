"""Prepare independent B173 reference checkpoint audit with complete history preserved."""
from pathlib import Path
import io,re,tokenize
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B173_reference_audit_tools_v4442')
SOURCE=Path('scripts/verify_editorial_handoff_v4401b.py')
TARGET=Path('scripts/verify_editorial_handoff_v4442.py')
if __name__=='__main__':
    assert not ROOT.exists() and not TARGET.exists()
    text=SOURCE.read_text(encoding='utf-8')
    a=text.index("    save(ROOT/'verified_handoff.json'")
    text=text[:a]
    changes={'B172':'B173','editorial_handoff_verification_v4401b':'editorial_handoff_verification_v4442',
        'checkpoint_v4400':'checkpoint_v4441','checkpoint_text_v4400':'checkpoint_text_v4441','V4400':'V4441',
        'reference_approval_v4399':'reference_approval_v4440',
        'Lil-B172-Julian-Mihwa-Silla-crown-conditional-date-independent-search27':'Lil-B173-Reika-crown-inquiry-uncertain-Julian-tomb-lead-competitive-search11',
        'unfinished_editorial_scope_v4400':'unfinished_editorial_scope_v4441','reference_reconciliation_v4400':'reference_reconciliation_v4441',
        "pending['new_emulator_runs']==4":"pending['new_emulator_runs']==2",
        "r['editorial_decision']=='revise' for r in doc['records'])==19":"r['editorial_decision']=='revise' for r in doc['records'])==8",
        'focused_repeat_proof':'postscene_native_state_proof',"'actual_new_cold_boot_runs':4":"'actual_new_cold_boot_runs':2",
        "for stage in ['display_run_v4390','repeat_run_v4395']:":"for stage in ['display_run_v4437']:",
    }
    for key in changes:assert key in text,key
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m[0]],text)
    numbers={'5789':'5800','5762':'5789','5792':'5803','3659':'3678','2103':'2111','27':'11'}
    tokens=[]
    for token in tokenize.generate_tokens(io.StringIO(text).readline):
        if token.type==tokenize.NUMBER and token.string in numbers:token=token._replace(string=numbers[token.string])
        tokens.append(token)
    text=tokenize.untokenize(tokens)
    # Tail is new current-state evidence;do not remap its verified scalar values.
    text+='''    candidate=ledger['current_integrated_candidate']
    assert candidate['profile']=='all-routes-unified-v4404'
    assert candidate['sha256']==doc['current_ROM_sha256']==sha(Path(candidate['path']).read_bytes())
    sample=read(doc['representative_proof']);stateproof=read(doc['postscene_native_state_proof'])
    assert sample['new_emulator_runs']==2 and sample['all11_progressive_panels_unforced_predicate_both_effects_single_end_and_normal_town_return_pass']
    assert sample['actual_VM_descriptor_last_result1_preserved_through_type3_and_end']
    assert len(stateproof['all2_actual_sheets_viewed'])==2 and len(stateproof['paired_full_screen_views'])==6
    assert len(stateproof['all115_sampled_nontext_region_checks'])==115 and stateproof['all115_sampled_nontext_regions_equal']
    assert stateproof['whole_RGB_town5530_and_final9001_equal'] and all(stateproof['postscene9001_native_component_equality'].values())
    assert stateproof['postscene9001_whole1A04_actor_models_and_captain2_equal']
    assert stateproof['source_relative_sites736740756_actual_744_offline_native_only']
    assert stateproof['PRNG_equality_or_future_world_equivalence_not_claimed']
    stored=read(doc['final_padding_proof']);mapping=read(doc['reference_map'])
    assert stored['current_final_stored_macro_alignment_cases']==44
    assert (stored['new_parity_macro_alignment_cases'],stored['exact_byte_identical_reused_macro_alignment_cases'])==(24,20)
    assert len(mapping['blocks'][0]['relative_skip_fixups'])==4 and len(mapping['blocks'][0]['target_native_skip_cases'])==20
    assert mapping['blocks'][0]['original_declared_end_word_maps']==[dict(source_offset=762,target_offset=794,extent=4,source_four_zero_bytes_exact=True)]
    save(ROOT/'verified_handoff.json',dict(checkpoint='V4441',ledger_sha256=sha(raw),fresh_reread=5800,
        integrated=5789,pending=11,source_prose=5803,revised=3678,retained=2111,new_source_prose_reviews=0,new_completed_records=0,
        all_prior_ledger_values_and_completed_records_preserved=True,all11_source_prose_native_reference_and_actual_display_approved=True,
        actual_panels=11,actual_sheets=2,viewed_source_English_full_screens=6,content_cold_boots=2,frames_each=9001,all_jobs_terminal=True,
        source_structural_commands=23,stored_fixture_commands=32,actual_selected_fixture_commands=31,
        four_relative_sites40_source_current_and20_target_native_cases=True,
        source_predicate1_both_A000s_single_end762_and_normal_return_actual=True,
        actual_VM_last_result1_preserved_through_type3_and_end=True,
        unvisited_source_jump744_has_explicit_offline_native_coverage=True,all115_nontext_regions_equal=True,
        current_candidate=candidate['path'],candidate_sha256=candidate['sha256'],promoted_main_V4353_unchanged=True,
        no_registry_builder_baseline_or_graphics_scope_change=True,one_space_complete_ledger_preserved=True,
        full_goal_active=True,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [DOC,APPROVAL,CHECK/'checkpoint_receipt.json',Path(__file__)]}))
    print('V4441 independently verified:11 reference-approved pending;all earlier records/counters,latestV4404,mainV4353 and wider scope preserved.')
'''
    assert 'utf-8' in text and 'utf-3' not in text
    compile(text,str(TARGET),'exec');TARGET.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'derivation.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),target=str(TARGET),
        target_sha256=sha(TARGET.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),no_new_review_or_completion_credit=True,full_goal_complete=False))
    print('Prepared independent V4441 checkpoint/reference audit;all prior history and two-boot scope retained.')
