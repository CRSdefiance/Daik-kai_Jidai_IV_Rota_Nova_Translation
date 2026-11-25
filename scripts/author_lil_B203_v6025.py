"""Author22 complete-exchange v2 decisions;keep native and integration gates pending."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.lil_B203_prose_v6024 import REVISIONS,RETAIN_NOTES
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B203_prose_v6025')
OUT=Path('translations/lil_B203_editorial_manuscript_v1.json')
COMPARISON=Path('work/analysis/lil_B203_comparison_v6023/all22_complete_clean_source_and_predecessor_exchange.json')
SOURCE=Path('work/analysis/lil_B203_source_v6010/all22_clean_current_complete_context.json')
PROOFS={
 'actor_voice_contract':'work/analysis/lil_B203_voices_v6011/current207_catalog_eight_voices_and_three_source_selectors.json',
 'control_contract':'work/analysis/lil_B203_dispatches_v6014/all22_source_current_dispatches_FI_and9_control_leaves.json',
 'branch_proof':'work/analysis/lil_B203_branches_v6016/original_relative_skip_operand_proof.json',
 'source_entry_proof':'work/analysis/lil_B203_entry_v6015/source_EV2_B203_action_dependency_and_native_getter_binding.json',
 'source_effect_and_predicate_contract':'work/analysis/lil_B203_controls_v6017/nine_exact_leaves_resource632E_6003_picture47xx_four_A000_pairs_and_end.json',
 'source_nameplate_consumer_proof':'work/analysis/lil_B203_names_v6012/six_original_progressive_and_catalogue_name_consumers.json',
 'actor_terminology_reconciliation':'work/analysis/lil_B203_source_names_v6013/three_exact_source_name_fields_voices_and_distinct_name_consumers.json',
 'contextual_reconciliation':'work/analysis/lil_B203_source_reconciliation_v6022/viewed_complete_source_exchange_names_item18_and_return_scope.json',
 'actual_original_response_paths':'work/analysis/lil_B203_source_paths_v6020/one_actual_source_path_and_complete_command_intervals.json'}
CONTEXT='Mikhail reacts to an unidentified specimen;Lil asks what is wrong. They notice a bug with something like grass growing on it. A Mysterious Old Man identifies caterpillar fungus and explains that it is prized as medicine in China. Lil is surprised and Mikhail becomes interested. The older man offers an object and explains that it is a book about medicinal ingredients. Lil hesitates over its apparent value;he says he no longer needs it. After Lil unfinished objection,he teases that her companion seems to want it. Mikhail sheepishly admits wanting to read the book. Lil proposes paying1,000 gold rather than taking it free;the old man laughs and accepts100. A separate FE/FI notice reports Lil Charm+1. The original source effects later display an existing item-acquired notice. No explicit spoken book title,medical profession,kinship,rank,nationality,biography,guaranteed efficacy or complete payment/item-effect semantics is established.'
if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists();comp,packet=map(read,[COMPARISON,SOURCE]);rows=[]
    assert set(REVISIONS).isdisjoint(RETAIN_NOTES) and set(REVISIONS)|set(RETAIN_NOTES)=={r['source_record_index'] for r in comp['records']}
    recon=read(PROOFS['contextual_reconciliation']);assert recon['all22_source_objects_observed'] and not recon['visual_review_pending']
    names={2:'Lil',76:'Mikhail',170:'Mysterious Old Man',254:'System'}
    for original in comp['records']:
        r=deepcopy(original);index=r['source_record_index'];rev=index in REVISIONS;body,note=REVISIONS[index] if rev else (r['previous_paragraph'],RETAIN_NOTES[index])
        assert '\n' not in body and '{' not in body and '\0' not in body and body==body.strip() and '  ' not in body
        assert (body!=r['previous_paragraph'])==rev
        marked=body
        for macro in ['FI','FA','FO']:marked=marked.replace(macro,'{MACRO:'+macro+'}')
        r.update(english='{SPEAKER:'+format(r['source_selector'],'02X')+'}'+marked,speaker=names[r['source_selector']],source_meaning=r['fresh_source_gloss'],context=CONTEXT,localization_note=note,editorial_decision='revise' if rev else 'retain-wording',effective_predecessor_paragraph=r['previous_paragraph'],full_clean_context_precedes_comparison=True,editorial_predecessor_English_comparison_pending=False,current_native_voice_macro_entry_and_context_pending=False,current_macro_dispatch_bound=True,current_complete_native_display_pending=True,current_native_UI_body_explicit_unexecuted_boundary=True,review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),status='source-prose-approved-native-format-references-and-release-pending',prose_author_module='scripts/lil_B203_prose_v6024.py',record_index=r['current_record_index'])
        if not rev:r['fresh_retained_wording_justification']=note
        rows.append(r)
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':9,'retain-wording':13}
    doc=dict(format='dk4-editorial-manuscript-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC2.DK4',current_ROM=packet['current_ROM'],current_ROM_sha256=packet['current_ROM_sha256'],source_ROM_sha256=packet['source_ROM_sha256'],required_runtime_ARM9_sha256=packet['current_ARM9_sha256'],source_prose_or_completion_credit_added=0,formatting_review_pending=True,status='source-prose-approved-native-format-references-and-release-pending',whole_exchange_context=CONTEXT,
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),whole_exchange_context_notes=packet['whole_exchange_context_notes'],whole_exchange_context_notes_sha256=packet['whole_exchange_context_notes_sha256'],effective_current_comparison=str(COMPARISON),effective_current_comparison_sha256=sha(COMPARISON.read_bytes()),records=rows,revised=9,retained=13,
        no_authored_line_break_alignment_spaces_or_fit_driven_prose_shortening=True,all22_source_objects_observed_no_offline_only_source_lines=True,
        source_name_fields_and_progressive_catalogue_distinction_no_name_bytes_changed=True,names_review_decisions=recon['contextual_name_decisions'],source_item18_observed_without_inserting_unspoken_title=True,
        incomplete_following_B43_source_item_and_Local_Product_terms_are_separate_uncredited_leads=True,generated_item_acquired_notice_observed_not_an_extra_stored_speech_or_new_credit=True,
        no_medical_profession_kinship_rank_nationality_ownership_provenance_or_guaranteed_item_effect_invented=True,
        source_three_actors31_commands9_leaves_one_FE_FI_no_choices_FA_FO_or_relative_sites_preserved=True,full_goal_complete=False)
    for k,p in PROOFS.items():doc[k],doc[k+'_sha256']=p,sha(Path(p).read_bytes())
    save(OUT,doc);ROOT.mkdir(parents=True)
    save(ROOT/'twenty_two_uncredited_contextual_prose_decisions.json',dict(manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),revised=9,retained=13,four_prose_gates_per_record=True,native_formatting_all_gates_false=True,all22_uncredited=True,no_ROM_or_registered_release_change=True,source_gameplay_fixture_runs=1,source_gameplay_fixture_frames=13001,evidence={str(p):sha(Path(p).read_bytes()) for p in [COMPARISON,SOURCE,*PROOFS.values(),Path(__file__),Path('scripts/lil_B203_prose_v6024.py')]},full_goal_complete=False))
    print('B20322 uncredited decisions:nine revisions/13 individual retentions. Four prose gates pass;native/reference/release checks pending.')
