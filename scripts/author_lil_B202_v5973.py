"""Author19 complete-exchange v2 decisions;leave native formatting gates pending."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.lil_B202_prose_v5972 import REVISIONS,RETAIN_NOTES
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B202_prose_v5973')
OUT=Path('translations/lil_B202_editorial_manuscript_v1.json')
COMPARISON=Path('work/analysis/lil_B202_comparison_v5971/all19_complete_clean_source_and_predecessor_exchange.json')
SOURCE=Path('work/analysis/lil_B202_source_v5959/all19_clean_current_complete_context.json')
PROOFS={
 'actor_voice_contract':'work/analysis/lil_B202_voices_v5960/current207_catalog_eight_voices_and_four_source_selectors.json',
 'control_contract':'work/analysis/lil_B202_dispatches_v5963/all19_source_current_dispatches_no_macros_and7_control_leaves.json',
 'branch_proof':'work/analysis/lil_B202_branches_v5965/original_relative_skip_operand_proof.json',
 'source_entry_proof':'work/analysis/lil_B202_entry_v5964/source_EV2_B202_action_dependency_and_native_getter_binding.json',
 'source_effect_and_predicate_contract':'work/analysis/lil_B202_controls_v5966/seven_exact_leaves632A_picture47xx_two_A000_pairs_and_guarded_end.json',
 'source_nameplate_consumer_proof':'work/analysis/lil_B202_names_v5961/eight_original_progressive_and_catalogue_name_consumers.json',
 'actor_terminology_reconciliation':'work/analysis/lil_B202_source_names_v5962/four_exact_source_name_fields_voices_and_original_Sailor_alias.json',
 'contextual_reconciliation':'work/analysis/lil_B202_source_reconciliation_v5970/viewed_complete_source_exchange_names_title_and_return_scope.json',
 'actual_original_response_paths':'work/analysis/lil_B202_source_paths_v5969/one_actual_source_path_and_complete_command_intervals.json'}
CONTEXT='A Sailor abruptly gives Lil an unspecified object with permission to use it. Lil is surprised. The Guildmaster spots the Sailor and shouts for him to stop;the Sailor gives a casual farewell and the Guildmaster repeats the command. Lil is left bewildered. Charles asks what is happening;Lil says something was forced on her. Charles asks what it is,and Lil tentatively identifies a book. Charles examines it and reads Glassmaking Guide. He advises keeping something freely given;Lil hesitates,but he restates his pragmatic view. Charles then asks to see the book later,and Lil recognizes his self-interest. No theft,police rank,kinship,romance,confirmed legitimate ownership,payment,guaranteed trade effect or source FE notice is established.'
if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists();comp,packet=map(read,[COMPARISON,SOURCE]);rows=[]
    assert set(REVISIONS).isdisjoint(RETAIN_NOTES) and set(REVISIONS)|set(RETAIN_NOTES)=={r['source_record_index'] for r in comp['records']}
    assert read(PROOFS['contextual_reconciliation'])['all19_source_speeches_observed']
    names={2:'Lil',18:'Charles',147:'Guildmaster',157:'Sailor'}
    for original in comp['records']:
        r=deepcopy(original);index=r['source_record_index'];rev=index in REVISIONS;body,note=REVISIONS[index] if rev else (r['previous_paragraph'],RETAIN_NOTES[index])
        assert '\n' not in body and '{' not in body and '\x00' not in body and body==body.strip() and '  ' not in body
        assert (body!=r['previous_paragraph'])==rev
        r.update(english='{SPEAKER:'+format(r['source_selector'],'02X')+'}'+body,speaker=names[r['source_selector']],source_meaning=r['fresh_source_gloss'],context=CONTEXT,localization_note=note,editorial_decision='revise' if rev else 'retain-wording',effective_predecessor_paragraph=r['previous_paragraph'],full_clean_context_precedes_comparison=True,editorial_predecessor_English_comparison_pending=False,current_native_voice_macro_entry_and_context_pending=False,current_macro_dispatch_bound=True,current_complete_native_display_pending=True,current_native_UI_body_explicit_unexecuted_boundary=True,review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),status='source-prose-approved-native-format-references-and-release-pending',prose_author_module='scripts/lil_B202_prose_v5972.py')
        if not rev:r['fresh_retained_wording_justification']=note
        rows.append(r)
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':6,'retain-wording':13}
    doc=dict(format='dk4-editorial-manuscript-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',review_gates=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),file_path='/data/SC2.DK4',current_ROM=packet['current_ROM'],current_ROM_sha256=packet['current_ROM_sha256'],source_ROM_sha256=packet['source_ROM_sha256'],required_runtime_ARM9_sha256=packet['current_ARM9_sha256'],source_prose_or_completion_credit_added=0,formatting_review_pending=True,status='source-prose-approved-native-format-references-and-release-pending',whole_exchange_context=CONTEXT,
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),whole_exchange_context_notes=packet['whole_exchange_context_notes'],whole_exchange_context_notes_sha256=packet['whole_exchange_context_notes_sha256'],effective_current_comparison=str(COMPARISON),effective_current_comparison_sha256=sha(COMPARISON.read_bytes()),records=rows,revised=6,retained=13,
        no_authored_line_break_alignment_spaces_or_fit_driven_prose_shortening=True,all19_source_speeches_observed_no_offline_only_source_lines=True,
        source_defined_Sailor_alias_distinct_from_Retainer_catalogue_no_name_bytes_changed=True,spoken_Glassmaking_Guide_bound_to_exact_clean_item14_and_actual_card=True,
        incomplete_following_B43_source_item_term_is_a_separate_uncredited_lead=True,
        no_crime_police_kinship_rank_romance_ownership_provenance_or_item_effect_invented=True,
        source_four_actors26_commands_seven_leaves_zero_FE_choices_and_FI_FA_FO_preserved=True,full_goal_complete=False)
    for k,p in PROOFS.items():doc[k],doc[k+'_sha256']=p,sha(Path(p).read_bytes())
    save(OUT,doc);ROOT.mkdir(parents=True);save(ROOT/'nineteen_uncredited_contextual_prose_decisions.json',dict(manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),revised=6,retained=13,four_prose_gates_per_record=True,native_formatting_all_gates_false=True,all19_uncredited=True,no_ROM_or_registered_release_change=True,source_gameplay_fixture_runs=1,source_gameplay_fixture_frames=13001,evidence={str(p):sha(Path(p).read_bytes()) for p in [COMPARISON,SOURCE,*PROOFS.values(),Path(__file__),Path('scripts/lil_B202_prose_v5972.py')]},full_goal_complete=False))
    print('B20219 uncredited decisions:six revisions/13 individual retentions. Four prose gates pass;native formatting/reference/release pending. Names/voices/title/source paths bound.')
