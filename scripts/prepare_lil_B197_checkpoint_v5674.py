"""Prepare a lossless six-file native-review checkpoint with unchanged counters."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B197_checkpoint_tools_v5674')
GATES='''def gates():
    packet,evidence=source_gates()
    prior=read(PRIOR);assert packet['current_ROM_sha256']==prior['candidate_sha256']==sha(Path(prior['candidate']).read_bytes())
    speech=read('translations/lil_B197_editorial_manuscript_v3.json');choice=read('translations/lil_B197_choice_manuscript_v2.json')
    approval=read('work/analysis/lil_B197_native_approval_v5670/all24_source_prose_current_native_speech_choice_approval.json')
    assert len(speech['records'])==21 and len(choice['records'])==3
    assert approval['revised']==16 and approval['retained']==8 and approval['all24_five_source_context_localization_naturalness_formatting_gates_true']
    assert approval['speech_processor_alignment_cases']==168 and approval['choice_selection_cancel_cases']==8
    assert len(approval['formatter_negatives'])==28 and len(approval['source_consumer_negative_controls'])==18
    assert len(approval['reviewed_sheets'])==3 and len(approval['reviewed_menu_sheets'])==1
    for sheet in approval['reviewed_sheets']+approval['reviewed_menu_sheets']:
        assert sheet['viewed_in_full_current_turn'] and sheet['original_detail'] and sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    context=read('work/analysis/lil_B197_context_v5662/clean_first_context_original_three_paths_gold_and_Charm.json')
    assert context['source_purchase_R53_answers_R49_romance_after_R45_acceptance_not_book_refusal']
    assert context['source_FE_R109_common_tail_observed_after_all_three_choices'] and context['source_delegated_gift_not_inferred_from_company_funds']
    assert context['actual_original_source_cold_boots']==3 and context['actual_source_frames']==39003
    plan=read('work/analysis/lil_B197_relocation_v5671/nested_source_relocation_research.json')
    block=plan['blocks'][0];assert block['source_bytes']==880 and block['research_bytes']==1004
    assert len(block['command_map'])==39 and len(block['relative_skip_fixups'])==6 and len(block['target_native_skip_cases'])==30
    assert block['inverse_plus_original_two_tailzeros_recovers_every_stored_source_byte']
    stored=read('work/analysis/lil_B197_stored_v5672/all21_final_stored_targets84_macro_cases_and_complete_planes.json')
    assert stored['current_final_stored_macro_alignment_cases']==84 and stored['new_parity_macro_alignment_cases']==28
    menus=read('work/analysis/lil_B197_stored_choices_v5673/one_final_typed_object_three_exact_references_and_both_even_alignments.json')
    assert menus['fresh_count_calls']==2 and menus['fresh_label_pointer_calls']==6 and len(menus['actual_target_record_references'])==3
    packet={**packet,'records':speech['records'],'typed_choice_records':choice['records']}
    proofs=[PRIOR,
        Path('work/analysis/lil_B197_source_fixture_v5658/complete_B197_source_B22_fixture.json'),
        Path('work/analysis/lil_B197_source_paths_v5661/three_actual_source_menu_paths_and_original_response_intervals.json'),
        Path('work/analysis/lil_B197_context_v5662/clean_first_context_original_three_paths_gold_and_Charm.json'),
        Path('work/analysis/lil_B197_comparison_v5663/all24_complete_clean_and_predecessor_exchange_with_three_choices.json'),
        Path('work/analysis/lil_B197_author_v5665/all24_clean_first_contextual_decisions_with_two_companions.json'),
        Path('work/analysis/lil_B197_native_approval_v5670/all24_source_prose_current_native_speech_choice_approval.json'),
        Path('work/analysis/lil_B197_relocation_v5671/nested_source_relocation_research.json'),
        Path('work/analysis/lil_B197_stored_v5672/all21_final_stored_targets84_macro_cases_and_complete_planes.json'),
        Path('work/analysis/lil_B197_stored_choices_v5673/one_final_typed_object_three_exact_references_and_both_even_alignments.json'),
        Path('work/analysis/lil_B197_layout_v5667/all21_paragraph_layout_QA.json'),
        Path('work/analysis/lil_B197_layout_review_v5667c/one_exact_R74_boundary_review_and_unchanged_planner.json'),
        Path('scripts/refine_lil_B197_layout_v5667b.py'),Path('scripts/lil_B197_checkpoint_text_v5674.py'),Path(__file__)]
    for p in proofs:
        evidence[str(p)]=sha(p.read_bytes())
        if p.suffix=='.json':
            data=read(p)
            for q,h in data.get('evidence',{}).items():assert sha(Path(q).read_bytes())==h;evidence[q]=h
            for key,h in data.items():
                if key.endswith('_sha256') and isinstance(data.get(key[:-7]),str) and Path(data[key[:-7]]).is_file():
                    q=Path(data[key[:-7]]);assert sha(q.read_bytes())==h;evidence[str(q)]=h
    return packet,evidence

'''
SCOPE='''        scope['historical_Lil_B197_source_bound_before_v5674']=scope.pop('next_Lil_B197_source_bound_uncredited_v5656')
        scope['next_Lil_B197_native_approved_uncredited_v5674']=dict(
            source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),objects=24,speeches=21,choice_labels=3,typed_three_option_menus=1,
            uncredited=True,revised=16,retained=8,native_approval='work/analysis/lil_B197_native_approval_v5670/all24_source_prose_current_native_speech_choice_approval.json',
            clean_source_actual_paths_and_contextual_correction_complete=True,all24_source_context_prose_native_gates_true=True,
            research_relocation_and_stored_speech_choice_checks_complete=True,
            whole_image_external_references_English_actual_compiler_registered_release_clean_patch_and_current_startup_pending=True)
'''
ENTRY='''        new[KEY]=dict(summary=SUMMARY,next=NEXT,source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),records=records,
            native_approved_uncredited_objects=24,speech_objects=21,typed_choice_labels=3,typed_choice_objects=1,revised=16,retained=8,
            source_prose_or_completion_credit_added=0,source_commands=39,progressive=20,FE=1,FI=0,FA=0,FO=0,
            source_actors=[21,169],source_voices={'21':1,'169':0},source_names={'21':'Ian Dukov','169':'Alluring Woman'},
            revised_labels=["Let's buy it",'Pass','You decide'],
            source_purchase_R53_romance_refusal_and_common_FE_correct_initial_gloss=True,
            native_speech_alignments=168,native_consumer_negatives=18,native_formatter_negatives=28,
            native_menu_selection_cancel_cases=8,native_label_style_planes=12,English_sheets_viewed=4,
            final_stored_speech_alignments=84,fresh_stored_alignments=28,reused_stored_alignments=56,
            research_source_target_bytes=[880,1004],relocation_spans=6,target_native_skip_cases=30,
            final_menu_count_calls=2,final_menu_pointer_calls=6,exact_stored_label_references=3,
            actual_Japanese_source_fixture_runs=3,actual_source_frames=39003,actual_source_distinct_speeches=21,actual_source_speech_observations=35,
            source_fixture_not_natural_event_activation_or_original_location=True,
            actual_revised_English_gameplay_observed=False,new_ROMs=1,new_revised_English_ROMs=0,new_emulator_runs=3,
            remaining_gates=['whole-image-load-and-external-entry-reference-map','relocated-dispatch-original-controls-and-end',
                'focused-English-three-choice-scene-and-transition-checks','atomic-compiler-registered-cumulative-release-exact-clean-patch-current-startup'],
            previous_goal_turn_classification='progress',current_goal_turn_classification='progress',evidence=evidence,full_goal_complete=False)
        new[SCOPE]=dict(path=str(inventory),sha256=sha(inventory.read_bytes()),Lil_B197_native_approved_uncredited_objects=24,
            broader_storylines_earlier_translations_town_shop_random_help_prose_and_retrospective_early_wrapping_open=True,
            graphics_and_later_older_record_technical_reaudit_separate=True,full_goal_complete=False)
'''
VERIFY='''        save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=prior['candidate'],candidate_sha256=prior['candidate_sha256'],
            patch=prior['patch'],patch_sha256=prior['patch_sha256'],all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,
            completed=6191,source_prose=6194,revised=3889,retained=2302,SC2=4306,SC3=96,reviewed_routes=4592,completed_routes=4592,
            native_approved_uncredited_Lil_B197_objects=24,B197_speeches=21,B197_choice_labels=3,B197_three_option_menus=1,
            B197_pending_revisions=16,B197_pending_retentions=8,source_original_paths_observed=3,source_actual_frames=39003,
            revised_English_native_speech_alignments=168,final_stored_speech_alignments=84,typed_choice_selection_cancel_cases=8,
            original_source_context_corrected_before_predecessor_comparison=True,English_actual_and_registered_release_pending=True,
            research_relocation_39_commands6_spans30_target_cases_and_inverse_complete=True,
            new_editorial_credit=0,new_ROMs=1,new_revised_English_ROMs=0,new_emulator_runs=3,main_V4701_preserved=True,
            full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
        print('V5674 verified;V5637 current/main V4701 unchanged.24 B197 contextual/native-approved objects uncredited.English actual,external references and release next.Full editorial goal active.')
'''
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/checkpoint_lil_B197_v5656.py');text=source.read_text(encoding='utf-8')
    a=text.index('def gates():');b=text.index('def audit(',a)
    c=text.index("        scope['historical_Lil_B197_clean_pending_before_v5656']");e=text.index('        inventory=ROOT/',c)
    f=text.index('        new[KEY]=');g=text.index('        new[PREVIOUS]=',f)
    h=text.index("        save(VERIFY/'verified_handoff.json'")
    tool=derive(source,'scripts/checkpoint_lil_B197_v5674.py',{
        text[a:b]:GATES,text[c:e]:SCOPE,text[f:g]:ENTRY,text[h:]:VERIFY,
        'from scripts.lil_B197_checkpoint_text_v5656 import NEXT,SUMMARY':'from scripts.lil_B197_checkpoint_text_v5674 import NEXT,SUMMARY\nfrom scripts.checkpoint_lil_B197_v5656 import gates as source_gates',
        "scopepath=Path(old['unfinished_editorial_scope_v5642']['path']);assert sha(scopepath.read_bytes())==old['unfinished_editorial_scope_v5642']['sha256']":
        "scopepath=Path(old['unfinished_editorial_scope_v5656']['path']);assert sha(scopepath.read_bytes())==old['unfinished_editorial_scope_v5656']['sha256']",
        'Lil_B197_source_review_v5656':'Lil_B197_native_review_v5674','v5656':'v5674','verification_v5657':'verification_v5675','verification_v5643':'verification_v5657','V5656':'V5674',
        'B197 clean exchange and native source contracts;24 uncredited objects':'B197 contextual English,native display and relocation;24 uncredited objects',
        'Save36 uncredited B197 source objects':'Save24 uncredited B197 native-reviewed objects',
        "'reviewed_ordinary_boundaries','native_layout_retention_reason'":"'reviewed_ordinary_boundaries','native_layout_retention_reason','qa_waivers','qa_waiver_reason','exact_reviewed_soft_wrap_rows','actual_source_paths'",
        'Six clean-source checkpoint targets staged;24 source objects remain uncredited.':'Six contextual/native checkpoint targets staged;24 reviewed objects remain uncredited.'})
    ROOT.mkdir(parents=True);save(ROOT/'lossless_checkpoint_tool_prepared.json',dict(tool=tool,
        all_old_root_and_nested_values_required_by_complete_inverse=True,all_coverage_counters_unchanged=True,
        exact_source_current_prose_decisions_justifications_and_native_evidence_in_ledger=True,full_goal_complete=False))
