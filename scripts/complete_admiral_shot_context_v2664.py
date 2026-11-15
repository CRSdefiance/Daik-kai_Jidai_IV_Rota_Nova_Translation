"""Complete seven prior source/prose drafts under current representative scope."""
from pathlib import Path
from copy import deepcopy
from shutil import copy2
from collections import Counter
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/admiral_shot_completion_v2664')
OLD=Path('translations/admiral_shot_contextual_editorial_manuscript_v2.json')
DOC=Path('translations/admiral_shot_contextual_editorial_manuscript_v3.json')
FINAL=Path('translations/admiral_shot_contextual_final_review_v1.json')
SAMPLING=Path('work/analysis/admiral_shot_sampling_v2663/representative_family_and_transition_reconciliation.json')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V2284 Lookout shot7 native and representative context verified')
IDS=list(range(1924,1931));FAMILY='Lookout-admiral-shot7-contextual-completed'
SUMMARY=(
    'V2664 completes the seven previously unfinished COMMON Lookout reports1924-1930. '
    'Their fresh clean-Japanese contextual reread retains all seven current paragraphs with individual glosses and reasons. '
    'Successful targeted shots and collective victory remain explicit;no death,execution,weapon class,reward,kinship or new rank is invented. '
    'Seven current complete native228x64 font planes,eight original role7 voice pipelines,fourteen cold/warm copies and fourteen compiler negatives pass. '
    'All seven native previews were viewed. Complete first/final/interior glyphs,blank paper,guard cells,x6 margin,35-cell/four-row bounds and16px stride pass. '
    'The unassigned physical Lookout returns metric0;logical fallback Gerhard16 does not establish chance eligibility. '
    'Three original exclusions,three threshold exclusions and twenty post-RNG arithmetic unit inputs stop before all shot effects. '
    'New copied-state execution of original73BAC performs its mobile-flag clear,ship-state invalidation and original6609C(2,250,0) experience dispatch,then reaches72368(mode0). '
    'The existing ship-state was already minus1 and no eligible experience recipient changed in this copied snapshot;the only main4MiB delta is the original mobile flag4to0. '
    'Two isolated scratch-header tests verify regular72368 and special-B5 71D54 dispatch without executing or replacing either outcome. '
    'The first2662 probe refused a raw-versus-current-overlay comparison;preserved successor2662b compares the bounded current context correctly. '
    'Original role7 selection,portrait construction,dismissal/return,post-report dispatch and outcome callees are byte-identical across clean,current,and the two preserved representative builds. '
    'Actual historical role7 Search2229 holds/normal dismissal and actual capture2011/rewards/cargo/sailing provide shared presentation/regular-callee coverage. '
    'Prior complete pixel,input,fixture and donor audits remain hash-bound without replay. The new sheet showing those four representative states was viewed. '
    'The pre-report1096F8 call is unchanged and does not introduce a new text consumer. '
    'Under the user representative-sampling policy,the source-bound common controls,current exhaustive native checks and focused distinct cleanup/dispatch tests resolve this translation-specific transition finding. '
    'No individual shot variant or special-B5 gameplay outcome is claimed activated. No new emulator run,current startup,earned qualification,original chance draw,full-route or hardware proof is claimed. '
    'The seven paragraphs reconcile through the existing registered reinforcement_sniping_editorial/manuscriptv2 owner;no current English or metadata changes and no new ROM build are required. '
    'This adds seven completed records,not seven new source/prose records. Original registered editorial decisions were six revisions and one retention;the fresh pass retains all seven deployed paragraphs. '
    'Fresh coverage is2150 reread /2150 integrated-reconciled /zero pending. Historical completion is now2150(1504revised,646retained);source/prose2259 and incompleteCOMMON109 reconcile exactly. '
    'All original2143 historical completions remain freshly reconciled. '
    'The special outcome exposes COMMON2187-2191 named-target defeat reports as five separate context-only leads,with exact clean/current references and no source/prose or completion credit here. '
    'Registered experimental cumulativeV2284 remains493batches/114accepted layers with its exactly reconstructable clean-input patch. '
    'ROM,runtime,geometry,registry,profile,manifest and patch are unchanged;V1492 remains promoted and all ROMs and earlier translations are preserved. '
    'All remaining source/prose drafts,every never-reviewed storyline,shared shop/town dialogue,random scene and player-facing prose remain in scope. '
    'Separate graphics/all18 plaques,raw rejected-record coverage,SC3B109 classification and later older-record technical re-audit remain open. Full goal active;all jobs terminal.'
)

if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,DOC,FINAL,GUIDE])
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp)
    prior_audit_path=Path('work/analysis/editorial_handoff_verification_v2661/verified_handoff.json');audit=read(prior_audit_path)
    assert sha(lp.read_bytes())==audit['ledger_sha256']
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2150,2143,7)
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==116 and set(IDS)<=set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    sample=read(SAMPLING);assert sample['no_open_translation_specific_display_or_transition_finding']
    sheet=Path(sample['review_sheet']);assert sha(sheet.read_bytes())==sample['review_sheet_sha256']
    for p,digest in sample['evidence'].items():assert sha(Path(p).read_bytes())==digest,p
    doc=deepcopy(read(OLD));owner=doc['registered_prose_owner_bindings'][0]
    registered=read(owner['manuscript']);prior={r['message_id']:r for r in registered['records']}
    assert Counter(prior[n]['editorial_decision'] for n in IDS)=={'revise':6,'retain':1}
    rows=[]
    for row in doc['records']:
        n=row['message_id'];assert all(row['review'].values()) and row['english']==prior[n]['english']
        row.update(status='contextually-reviewed-current-native-and-representative-scope-reconciled',
            historical_editorial_decision=prior[n]['editorial_decision'],
            decision='revised-and-integrated' if prior[n]['editorial_decision']=='revise' else 'retained-and-editorially-reviewed',
            integrated_hex=row['current_hex'],integrated_reference=row['current_reference'],
            completed_candidate_reference=doc['current_ROM'],representative_reconciliation=str(SAMPLING),
            actual_holds=[],individual_actual_activation_not_claimed=True,
            all_source_native_copy_font_and_representative_scope_gates_pass=True)
        rows.append(row)
    doc.update(records=rows,status='complete-contextual-current-native-and-registered-retention',
        distinct_post_shot_transition_pending=False,current_native_and_representative_transition_reconciliation_pending=False,
        representative_reconciliation=str(SAMPLING),representative_reconciliation_sha256=sha(SAMPLING.read_bytes()),
        historical_representative_sheet_viewed=True,actual_shot_IDs=[],new_emulator_runs=0,
        completion_credit_added=7,source_prose_credit_added=0,all_source_native_and_representative_scope_gates_pass=True)
    validate_natural_dialogue_batch(doc)
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text().startswith('# Current editorial handoff - V2660')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    save(DOC,doc)
    evidence_paths=[OLD,DOC,SAMPLING,Path(doc['source_context_packet']),Path(doc['native_context_proof']),
        Path(doc['fresh_ordinary_supplement']),Path(doc['current_native_font_proof']),Path(doc['focused_original_gate_proof']),
        Path('work/analysis/admiral_shot_return_v2662b/original_post_report_cleanup_and_dispatch.json'),
        Path('work/analysis/refit_spritsail_release_v2285b/registered_release_verification.json'),
        Path(owner['config']),Path(owner['manuscript']),Path(__file__),prior_audit_path,sheet]
    evidence={str(p):sha(p.read_bytes()) for p in evidence_paths}
    release=read('work/analysis/refit_spritsail_release_v2285b/registered_release_verification.json')
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==release['candidate_sha256']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256'] and release['whole_ROM_reconstruction_byte_exact']
    save(FINAL,dict(format='dk4-editorial-final-review-v1',family=FAMILY,file_path='/COMMON/MESFILE.DK4',native_message_IDs=IDS,
        revised_count=0,retained_count=7,new_completed_records=7,historical_decisions_newly_completed=dict(revised=6,retained=1),
        records=rows,summary=SUMMARY,evidence=evidence,registered_stage_binding=owner,
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],profile='all-routes-unified-v2284',
        patch=release['patch'],patch_sha256=release['patch_sha256'],whole_clean_input_reconstruction_exact=True,
        no_ROM_profile_registry_manifest_or_patch_change=True,current_native_font_executions=7,current_native_speech_pipelines=8,
        current_native_copies=14,actual_shot_IDs=[],representative_actual_IDs=[2229,2011],new_emulator_runs=0,
        special_B5_branch_offline_only=True,context_only_companion_IDs=list(range(2187,2192)),companion_credit=0,
        all_review_sheets_viewed=True,full_goal_complete=False))
    existing={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    selected={('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}') for n in IDS}
    assert not selected&existing
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/COMMON/MESFILE.DK4',native_message_IDs=IDS,
        record_IDs=[f'COMMON_MESSAGE_{n}' for n in IDS],final_review=str(FINAL),revised_count=6,retained_count=1,
        fresh_contextual_retentions=7,new_current_prose_revisions=0,
        actual_verification_scope='Representative existing role7/portrait and regular capture/result;focused copied-state cleanup and both dispatches. No individual shot or special-B5 activation.',records=rows))
    ledger['records_editorially_completed']=2150;ledger['records_revised_and_integrated']=1504
    ledger['retained_wordings_editorially_completed']=646
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']=1493
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in IDS]
    active=ledger['active_source_prose_drafts'];active['native_message_IDs']=[n for n in active['native_message_IDs'] if n not in IDS]
    for key,ns in active['manuscript_record_subsets_pending'].items():active['manuscript_record_subsets_pending'][key]=[n for n in ns if n not in IDS]
    fresh.update(fresh_pass_records_integrated=2150,fresh_pass_records_pending_native_actual_release=0,
        integrated_record_keys=deepcopy(fresh['record_keys']),pending_record_keys=[],pending_contextual_families=[],
        latest_pending_contextual_family=None,latest_contextual_manuscript=str(DOC),latest_completed_family=FAMILY,
        latest_contextual_retention_review=str(FINAL),latest_final_review=str(FINAL),
        coverage_note='2150fresh contextual rereads and reconciliations;original2143historical set plus7newly completed Lookout reports. Source/prose2259 and109incompleteCOMMON;five additional named-target reports are context-only uncredited leads. Full broader objective remains active.')
    fresh['reconciled_families'].append(dict(id=FAMILY,records=7,final_review=str(FINAL),new_revisions=0,justified_retentions=7,
        speaker_metadata_corrections=0,historical_reconciliation_only=False,new_completed_records=7,
        historical_decisions_newly_completed=dict(revised=6,retained=1),actual_shot_IDs=[],new_emulator_runs=0,
        current_native_font_executions=7,current_original_speech_pipelines=8,representative_sampling_policy_reconciled=True))
    active['note']=fresh['coverage_note'];ledger['latest_checkpoint']=SUMMARY
    ledger['admiral_shot_contextual_v2664']=dict(summary=SUMMARY,final_review=str(FINAL),evidence=evidence,
        goal_turn_classification='progress',full_goal_complete=False)
    ledger['formatting_watchlist']['admiral_shot_contextual_v2664']=dict(status='current-native-and-representative-scope-complete',final_review=str(FINAL),no_runtime_or_geometry_change=True)
    ledger['next_named_target_reports_source_lead_v2664']=dict(IDs=list(range(2187,2192)),file_path='/COMMON/MESFILE.DK4',
        packet=str(SAMPLING),sha256=sha(SAMPLING.read_bytes()),context_read_only=True,source_prose_credit_added=0,completion_credit_added=0,
        next='Full individual contextual review and consumer/name/font proof remain required;these are outside the109previously source/prose-reviewed incomplete records.')
    old_inventory=read('work/analysis/lil_cliff_completion_v2654/unfinished_editorial_scope_inventory.json')
    inventory=deepcopy(old_inventory)
    inventory['incomplete_COMMON_source_prose_groups']=[g for g in inventory['incomplete_COMMON_source_prose_groups'] if g['family']!='Lookout-admiral-shot']
    inventory.update(incomplete_COMMON_count=109,new_context_only_uncredited_named_target_leads=list(range(2187,2192)),
        next_focus='Review the remaining battle-aftermath34 and other source/prose drafts;include five newly identified named-target outcome reports in broad unreviewed prose inventory. Every never-reviewed route/shared/town/shop/random/player-facing line remains in scope.')
    inventorypath=ROOT/'unfinished_editorial_scope_inventory.json';save(inventorypath,inventory)
    assert {n for g in inventory['incomplete_COMMON_source_prose_groups'] for n in g['IDs']}==set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    ledger['unfinished_editorial_scope_v2664']=dict(path=str(inventorypath),sha256=sha(inventorypath.read_bytes()),incomplete_COMMON=109,full_goal_complete=False)
    save(lp,ledger)
    section='## V2664: Lookout shot7 completed through native and representative scope\n\n'+SUMMARY+'\n\nFinal review: '+FINAL.as_posix()+'. Focused return: work/analysis/admiral_shot_return_v2662b/original_post_report_cleanup_and_dispatch.json. Sampling: '+SAMPLING.as_posix()+'. Unfinished inventory: '+inventorypath.as_posix()+'.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text().split('\n',1);p.write_text(('# Current editorial handoff - V2664' if i==0 else first)+'\n\n'+section+rest,newline='\n')
    GUIDE.mkdir(parents=True)
    images=[]
    for source,kind in [(Path(read(doc['current_native_font_proof'])['review_sheet']),'current-native-CPU'),(sheet,'historical-other-family-representative-only')]:
        target=GUIDE/(kind+'_'+source.name);copy2(source,target);images.append(dict(path=str(target),sha256=sha(target.read_bytes()),kind=kind))
    save(GUIDE/'scope.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],final_review=str(FINAL),
        images=images,actual_shot_IDs=[],new_emulator_runs=0,historical_and_native_scopes_distinct=True,full_goal_complete=False))
    evidence.update({str(FINAL):sha(FINAL.read_bytes()),str(inventorypath):sha(inventorypath.read_bytes())})
    save(ROOT/'completion_receipt.json',dict(checkpoint='V2664',summary=SUMMARY,fresh_reconciliations=7,new_completed_records=7,
        new_current_prose_revisions=0,fresh_justified_retentions=7,historical_revisions_newly_completed=6,historical_retentions_newly_completed=1,
        fresh_reread=2150,fresh_integrated=2150,fresh_pending=0,completed_records=2150,historical_revised=1504,historical_retained=646,
        source_prose_reviewed=2259,COMMON_incomplete=109,companion_leads_uncredited=5,
        candidate_sha256=doc['current_ROM_sha256'],patch_sha256=release['patch_sha256'],guide=str(GUIDE),
        evidence=evidence,updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs,DOC,FINAL]},
        goal_turn_classification='progress',new_emulator_runs=0,all_jobs_terminal=True,full_goal_complete=False))
    print('V2664:7new completions,2150fresh reconciled;1504historical revisions/646retentions;2259source/prose,109incompleteCOMMON. No ROM/patch change;full goal active.')
