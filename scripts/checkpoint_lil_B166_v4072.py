"""Preserve44 uncredited B166 decisions and concrete native-menu/phrase-flow risks without completion credit."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B166_checkpoint_v4072')
PRIOR=Path('work/analysis/editorial_handoff_verification_v4051/verified_handoff.json')
AUTHOR=Path('work/analysis/lil_B166_author_v4065/all44_clean_first_contextual_decisions.json')
FONT=Path('work/analysis/lil_B166_fonts_v4068/current_macro_QA_and_progressive_font_proof.json')
DIAGNOSTIC=Path('work/analysis/lil_B166_menu_pixels_v4071/width_cases_no_mismatch_approval.json')
DOCS=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
FINDINGS={
    'DK4_MES_B166_R0027':'Keep make her stronger together if possible within the four-row source-bound rules.',
    'DK4_MES_B166_R0037':'Keep used to together;the current sheet breaks after used.',
    'DK4_MES_B166_R0068':'Keep man like that together rather than leaving like that as the last fragment.',
    'DK4_MES_B166_R0112':'Keep since I together rather than ending the preceding row with since.',
    'DK4_MES_B166_R0123':'Keep take good care of her together andavoid splitting seem to.',
    'DK4_MES_B166_R0153':'Improve the ease the sailors discontent clause boundary while preserving Speech andboth room terms.',
    'DK4_MES_B166_R0157':'Keep food andwater together without inventing individual room-resource assignments.',
    'DK4_MES_B166_R0165':'Keep recover faster together if possible;retain both room names andthe condition.',
    'DK4_MES_B166_R0175':'Keep the rests on idiom together;retain the complete refit-care instruction.'
}
NEXT='Resolve B166 menu-painter storage ownership using original constructor/stride evidence andfocused actual selection coverage as needed;do not infer a gameplay defect fromthe synthetic plane. Refine the nine viewed phrase-flow boundaries without changing reviewed prose,source controls orwording waivers. Recheck changed native cases,approve the separate typed menu,then complete relocation/stored references,representative source/English display/choice/transitions,registered cumulative build/exact clean patch andfresh startup. Continue B167-B180 andevery wider editorial family. Preserve every ROM,translation,producer,proof andfailure.'
SUMMARY='''V4072 preserves the complete B166 contextual draft andits concrete next checks;B166 is not integrated orcredited. All42 clean Japanese speeches andtwo player labels were read as a full exchange andindividually glossed before exposing the predecessor English. The draft records24 proposed revisions and20 individually justified retentions. Preserve Manuel's absorbed ship improvements andapologies,Lil's mounting impatience,the crying-ship metaphor,Camille's enthusiastic persuasion,optional Fernando's dry complaint,Lil's technical ignorance,reluctant consent,Manuel's long-absence hesitation,grateful acceptance/full introduction andoptional flagship Workroom advice. Names are bound to original consumers:Manuel Almeida,Fernando Dias andCamille. No kinship,rank,numeric duration,formal retirement,source port or earned recruitment is invented.

Exact clean/current binding covers62 commands,42 progressive preambles,four actors2/9/20/23,FI3,eight relative sites/80 cases,one unforced Fernando20 predicate,11 exact nonrelative nonchoice leaves,two resource words/20 boundary cases,six presentation sites,one typed advice menu,one late A000 andone end. Event166/action167 getters are native/offline evidence,not current eligibility. Both menu paths rejoin at2938 before A000 at2940 andthe end at2948;spoken acceptance/introduction precede the menu. Declining advice does not decline employment. Six original progressive/full-name consumers restore owned scratch acrossall4MiB. Fernando's existing width forms remain untouched. The older0D audit remains open.

Nine room terms are bound to exact current reviewed Help pages:Workrooms,First Mate's Office,Chapel,Galley,Livestock Room,Infirmary,Private Cabin,Recreation Room andLumber Room. Use active Speech,Shipwright andSurgeon terms. Restore gun batteries,cannon type,affected officers/sailors,at-sea timing andshipyard refit/repair help where predecessor prose omitted ormisnamed them. Preserve source-specific treatment/recovery statements andthe grouped food/water effect without adding thresholds,instant/full cures orindividual room-resource mappings. Four initial editorial gates are true onall44 objects;formatting remains pending.

All42 native216x64 speech planes,336 logical/compiled alignment cases and17 source-consumer negatives pass complete glyph order,cells,row origins,bounds andsingle-page checks. Allsix speech sheets were viewed. Fifteen narrow row-count notes exempt no other issue. Nine phrase-flow refinements are queued without changing reviewed wording. The separate typed-menu proof stopped at complete-pixel equality andis preserved unapproved. The diagnostic shows the standalone painter dropping the initial P ofPlease do withstorage stride56 atlogical widths54/56;stride60 atwidths58/60 matches every expected pixel. The current padded menu haswidth60;the unpadded reviewed object haswidth54. The exact original menu constructor/bitmap ownership andactual behavior remain tobe reconciled. This is a synthetic probe finding,not a confirmed gameplay defect;no padding,widening,shortening,guard change,waiver ormenu approval has been applied.

Registered experimental V4046 remains the verified cumulative candidate:539 manuscript batches/114 accepted layers,canonical base3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe. ROM6b991313e0f31e72b2548b7fd024ca406b710f61d56ddc35c06e147a443e4913;clean-input patch56f13528927f23cd5c72f45fde79fbed58ab6d463d0ad2c916e149fc4b66c971. Exact reconstruction,63 compiler negatives,B165's23 actual/one offline panels,two registered startup/town boots,31 whole-frame pairs andfive actor/captain controls passed. OnlySC2 B165 changed fromV4002;ARM9/COMMON/fonts/graphics/other routes and123040 staged bytes remain exact. V1492 remains promoted.

Credited coverage stays5529 fresh rereads/integrated,0 credited route records pending;source/prose5532,including3676 SC2 and64 SC3;route3930/3930;historical3527 revised/2002 retained. The44 B166 draft objects are tracked separately withzero new source/prose orcompletion credit. Other348 physical B167-B180 speeches andone choice-command lead remain unreviewed/uncredited;the earlier390-speech/two-choice-command inventory is preserved as history. Neither count is the full Lil/project denominator. Every wider storyline,shared shop/town dialogue,random scene,help andremaining player-facing prose remains open. Preserve COMMON750-752,canonical Maria32 SC3B97,SourceItems/LocalProduct,five named-target leads,exact-record Proof consistency andSamwell's uncredited full-catalogue middle-field lead. Graphics/all18 plaques remain separate;retain the later older-record technical re-audit/queued0D gap. Preserve every ROM,translation,draft,executed/imported producer,proof,failure andclean/canonical input. Full goal active;all jobs terminal.'''
if __name__=='__main__':
    assert not ROOT.exists();lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger);prior,author,font,diagnostic=map(read,[PRIOR,AUTHOR,FONT,DIAGNOSTIC])
    assert sha(lp.read_bytes())==prior['ledger_sha256'] and prior['checkpoint']=='V4050'
    assert author['decision_counts']=={'revise':24,'retain-wording':20} and author['source_prose_orcompletion_credit_added']==0
    assert len(font['cases'])==42 and font['current_original_macro_alignment_calls']==336 and len(font['negative_controls'])==17 and len(font['review_sheets'])==6
    assert [(r['logical_width'],r['storage_stride'],r['independent_complete_native_pixels_match']) for r in diagnostic['cases']]==[(54,56,False),(56,56,False),(58,60,True),(60,60,True)]
    assert ledger['current_integrated_candidate']['sha256']==prior['candidate_sha256'] and ledger['current_integrated_candidate']['patch_sha256']==prior['patch_sha256']
    assert Path(DOCS[0]).read_text(encoding='utf-8').startswith('# Current editorial handoff - V4050')
    paths=[PRIOR,AUTHOR,FONT,DIAGNOSTIC,Path('work/analysis/lil_B166_menu_diagnostic_v4070/original_VM_widths_and_preserved_failed_probe.json'),Path('scripts/prove_lil_B166_choices_v4069.py'),Path(__file__)]
    for p,digest in author['evidence'].items():assert sha(Path(p).read_bytes())==digest;paths.append(Path(p))
    for p,digest in author['manuscripts'].items():assert sha(Path(p).read_bytes())==digest;paths.append(Path(p))
    viewed=[]
    for sheet in font['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256'];viewed.append({**sheet,'viewed':True,'review':'Complete native glyph planes viewed;phrase-flow findings remain explicitly pending.'});paths.append(Path(sheet['path']))
    assert sha(Path(diagnostic['sheet']).read_bytes())==diagnostic['sheet_sha256'];paths.append(Path(diagnostic['sheet']))
    ROOT.mkdir(parents=True)
    for p in [lp,*DOCS]:copy2(p,ROOT/(p.name+'.before'))
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    findings=ROOT/'viewed_native_sheets_phrase_flow_and_unapproved_menu.json'
    save(findings,dict(all_six_native_sheets_viewed=viewed,nine_phrase_flow_findings=FINDINGS,reviewed_words_meanings_controls_and_decisions_to_remain_unchanged=True,menu_diagnostic_sheet_viewed=True,menu_diagnostic=str(DIAGNOSTIC),menu_diagnostic_sha256=sha(DIAGNOSTIC.read_bytes()),standalone_painter_mismatch_not_confirmed_actual_gameplay_defect=True,no_menu_or_formatting_approval=True,no_new_ROM_or_source_prose_completion_credit=True,evidence=evidence,full_goal_complete=False))
    status=dict(status='44-uncredited-contextual-drafts;42-native-speech-planes-viewed;nine-phrase-flow-findings;typed-menu-painter-ownership-open',manuscripts=author['manuscripts'],proposed_revisions=24,justified_retentions=20,speech_objects=42,typed_choice_labels=2,source_prose_or_completion_credit_added=0,new_emulator_runs=0,findings=str(findings),findings_sha256=sha(findings.read_bytes()),evidence=evidence,next=NEXT,full_goal_complete=False)
    ledger['lil_B166_preintegration_review_v4072']=status
    ledger['formatting_watchlist']['lil_B166_v4072']=dict(status=status['status'],findings=str(findings),findings_sha256=status['findings_sha256'],native_speech_glyph_planes_pass=True,reviewed_objects_uncredited=44,typed_menu_approval_pending=True,actual_selected_B166_IDs=[],new_emulator_runs=0)
    for u in ledger['coverage_units']:
        if u['id']=='all-route-scenes':u['next']=NEXT
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v4050']['path']));inventory['next_focus']=NEXT;inventory['B166_uncredited_contextual_draft_and_native_findings_v4072']=status
    inventory['remaining_B167_B180_unreviewed_uncredited']=dict(physical_speeches=348,typed_choice_command_leads=1,not_full_Lil_or_project_denominator=True)
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v4072']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_credited_route_source_prose=0,uncredited_B166_draft_objects=44,remaining_B167_B180_physical_speeches=348,remaining_B167_B180_choice_command_leads=1,canonical_Maria32_pending_uncredited=True,Proof_terminology_consistency_open=True,later_untouched_storylines_shared_town_shop_random_help_prose_open=True,full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    for k in ['completed_editorial_families','contextual_story_natural_dialogue_pass_v1871','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','Proof_terminology_consistency_lead_v3286','lil_B157_provenance_amendment_v3784']:assert ledger[k]==before[k],k
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    section='## V4072:B166 contextual draft andunapproved native-menu finding\n\n'+SUMMARY+'\n\nDraft/native evidence: '+findings.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,p in enumerate(DOCS):
        first,rest=p.read_text(encoding='utf-8').split('\n',1);p.write_text(('# Current editorial handoff - V4072' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V4072',prior_verified_handoff=str(PRIOR),prior_verified_handoff_sha256=sha(PRIOR.read_bytes()),evidence=evidence,findings=str(findings),findings_sha256=sha(findings.read_bytes()),updated_files={str(p):sha(p.read_bytes()) for p in [lp,*DOCS]},new_source_prose_reviews=0,new_completed_records=0,uncredited_reviewed_objects=44,proposed_revisions=24,justified_retentions=20,fresh_reread=5529,fresh_integrated=5529,fresh_pending=0,source_prose=5532,historical_revised=3527,historical_retained=2002,candidate=prior['candidate'],candidate_sha256=prior['candidate_sha256'],patch=prior['patch'],patch_sha256=prior['patch_sha256'],manifest_batches=539,accepted_layers=114,native_speech_planes=42,native_macro_alignment_cases=336,source_consumer_negatives=17,phrase_flow_findings=9,typed_menu_approval_pending=True,all_jobs_terminal=True,full_goal_complete=False))
    print('V4072:verifiedV4046 preserved;44 B166 contextual drafts uncredited,42native planes viewed;9phrase-flow findings andtyped-menu painter ownership pending. Full goal active.')
