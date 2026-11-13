"""Record the next clean-source context without awarding a prose review or completion."""
from pathlib import Path
from copy import deepcopy
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_Recruits_Julian_source_checkpoint_v3077')
PRIOR=Path('work/analysis/editorial_handoff_verification_v3071/verified_handoff.json')
SOURCE=Path('work/analysis/lil_Recruits_Julian_source_v3072/complete199_clean_current_native_context.json')
BRANCH=Path('work/analysis/lil_Recruits_Julian_branches_v3073/original_relative_skip_operand_proof.json')
CONTROL=Path('work/analysis/lil_Recruits_Julian_controls_v3074/source_bound197_preambles_FE_and_original_conditional_predicates.json')
CONTEXT=Path('work/analysis/lil_Recruits_Julian_context_v3075/complete_clean_exchange_context_notes.json')
TERMS=Path('work/analysis/lil_Recruits_Julian_terms_v3076/clean_current_crown_Mihwa_alias_and_shipyard_UI_terms.json')
SUMMARY=('V3077 preserves the independently verified V3070 release checkpoint and records the next uncredited clean-source scope: '
    '197 speeches and two typed player choices across Lil SC2 B75-B79. The five complete exchanges cover Janus hiring and ship delivery, '
    'Charles recruitment, Yukihisa intervention and recruitment, and Julian crown and family-history conversations. '
    'All clean Japanese has been read in complete exchanges. Exact clean/current references,372 commands,68 relative sites/680 clean-current cases, '
    '394 historical dispatcher cases and16 current predicates pass;there are no event queries. The typed menu and every new English paragraph still require review. '
    'The one FE ship-renaming guide remains an unlabeled modal panel. The current visible shipyard menu says Dock/Remodel;Refit is a separate header. '
    'Clean/current item137 proves Silla Gold Crown;catalog201 proves Mihwa;the existing Chinese alias spelling is Luo Yuli. '
    'Actor109 is Shipwright in the native catalog,so the provisional Townsman annotation must be corrected in new manuscript metadata. '
    'The nontext B80 neighbor has14 commands and earns no editorial credit. No new manuscript,English comparison pass,native target font approval,ROM or registry change is claimed. '
    'Coverage stays3791 reread/integrated/completed,2642 historically revised and1149 retained;source/prose stays3794,including1964 SC2. '
    'All2192 reviewed route records are integrated. COMMON750-752 callers and every wider untouched storyline,shared shop/town,random scene and remaining player-facing prose stay open. '
    'Keep graphics/all18 plaques separate and retain the later older-record technical re-audit,including the queued0D validation-gap lead. '
    'Experimental V3066 remains508 manifest batches/114 accepted layers,with exact clean-input reconstruction and31 current opening/town framebuffer matches toV3029. '
    'V1492 remains promoted. Preserve every ROM,earlier translation and executed proof. Full goal active;all jobs terminal.')
if __name__=='__main__':
    assert not ROOT.exists();lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    assert sha(lp.read_bytes())==read(PRIOR)['ledger_sha256']
    source,branch,control,context,terms=map(read,[SOURCE,BRANCH,CONTROL,CONTEXT,TERMS])
    assert source['current_ROM_sha256']==ledger['current_integrated_candidate']['sha256']
    assert (source['speech_objects'],source['typed_choice_labels'],source['total_editorial_objects'])==(197,2,199)
    assert [b['block'] for b in source['blocks']]==[75,76,77,78,79] and sum(len(b['all_clean_native_commands']) for b in source['blocks'])==372
    assert len(branch['operands_requiring_adjustment_when_resizing'])==68 and len(branch['cases'])==680
    assert control['all197_complete_preambles_and394_historical_dispatch_contexts_pass'] and len(control['current_original_predicate_cases'])==16 and control['original_event_queries']==[]
    assert context['all197_complete_clean_Japanese_speeches_and2_typed_choices_read_before_old_English_comparison']
    assert terms['approved_item_name']=='Silla Gold Crown'
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(3791,3791,0)
    assert ledger['records_with_source_and_prose_pass']==3794 and ledger['records_editorially_completed']==3791
    known={(r['file_path'],r['id']) for r in fresh['record_keys']};assert not known&{(r['file_path'],r['id']) for r in source['records']+source['typed_choice_records']}
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf8').startswith('# Current editorial handoff - V3070')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,SOURCE,BRANCH,CONTROL,CONTEXT,TERMS,Path(__file__)]}
    nextwork=dict(status='clean-source-context-mapped;uncredited-prose-and-native-targets-pending',file_path='/data/SC2.DK4',blocks=[75,76,77,78,79],speech_objects=197,typed_choice_labels=2,total_editorial_objects=199,
        source_context=str(SOURCE),branch_proof=str(BRANCH),control_contract=str(CONTROL),whole_exchange_context_notes=str(CONTEXT),terminology_reconciliation=str(TERMS),evidence=evidence,
        next='Compare all older English only after using the complete clean context. Author197 individual gloss/English/notes andtwo typed labels. Reconcile Shipwright109 annotation. Keep Silla Gold Crown,Mihwa,Luo Yuli andDock/Remodel terms. Prove196 ordinary planes/one FE guide andallsource macros;separate original two-choice VM/geometry/eight style planes. Apply exact source-prefix guards for29/6D/9E. Then review all native sheets,checkpoint,relocate372commands/68spans/340cases/16predicates/noqueries andone typedmenu,prove all336 loaders/entries/final padding,representative rules,register a cumulative successor afterfullV3066,create exactcleanpatch andfreshcurrentstartup. Do not credit B80 nontext orbegin later older-record re-audit.',
        full_older_English_comparison_still_required=True,only_existing_menu_labels_and_name_alias_inspected_for_term_reconciliation=True,
        new_source_prose_reviews=0,new_completed_records=0,new_emulator_runs=0,full_goal_complete=False)
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v3070']['path']));inventory['next_clean_only_uncredited_recruits_Julian_scope_v3077']=nextwork
    inventory['next_focus']='Review and integrate all199 B75-B79 objects,then continue every untouched storyline/shared shop-town/random/help/player prose family. Preserve all inherited unfinished leads,graphics separation andlater technical re-audit.'
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v3077']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=0,next_uncredited_clean_source_objects=199,full_goal_complete=False)
    ledger['lil_Recruits_Julian_clean_source_lead_v3077']=nextwork;ledger['latest_checkpoint']=SUMMARY
    for key in ['completed_editorial_families','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file','current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','reviewed_but_incomplete_route_record_IDs','active_source_prose_drafts','contextual_story_natural_dialogue_pass_v1871','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c']:
        assert ledger[key]==before[key],key
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    section='## V3077:next199 clean-source objects mapped;V3066 remains verified\n\n'+SUMMARY+'\n\nNext context: '+CONTEXT.as_posix()+'. Exact source/current packet: '+SOURCE.as_posix()+'. Terms: '+TERMS.as_posix()+'. The verified release and hashes remain in the V3070 section below.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf8').split('\n',1);p.write_text(('# Current editorial handoff - V3077' if i==0 else first)+'\n\n'+section+rest,encoding='utf8',newline='\n')
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V3077',summary=SUMMARY,evidence=evidence,updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},next_work=nextwork,
        prior_verified_handoff=str(PRIOR),new_source_prose_reviews=0,new_completed_records=0,source_prose=3794,completed=3791,fresh_reread=3791,fresh_integrated=3791,fresh_pending=0,historical_revised=2642,historical_retained=1149,
        candidate=ledger['current_integrated_candidate'],new_emulator_runs=0,all_jobs_terminal=True,full_goal_complete=False))
    print('V3077:199next-source objects mapped withoutcredit;3791completed/3794source-prose unchanged. V3066 preserved;fullgoalactive.')
