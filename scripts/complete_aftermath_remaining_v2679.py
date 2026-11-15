"""Reconcile34 reviews and registered2674;preserve the full wider objective."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from collections import Counter
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.surrender_advice_contextual_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.battle_aftermath_native_plan_v1255 import compiled
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/aftermath_remaining_completion_v2679')
OLD=Path('translations/aftermath_remaining_contextual_editorial_manuscript_v2.json')
DOC=Path('translations/aftermath_remaining_contextual_editorial_manuscript_v3.json')
FINAL=Path('translations/aftermath_remaining_contextual_final_review_v1.json')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V2674 Aftermath34 contextual revision and retentions verified')
FAMILY='Battle-aftermath-remaining34-contextual-completed'
SUMMARY=(
    'V2679 completes34 previously incomplete aftermath records1994-2010,2022-2037,and2192 in registered cumulative experimentalV2674. '
    'The clean-Japanese full-event review retains33 paragraphs and revises2029 to restore the emphatic courteous recommendation: '
    'You cannot win! I suggest you surrender at once! '
    'Town names,physical First Mate demand/town-representative white flag/member report,empty-duty report-only fallback,flagship destruction versus explicit2004sinking,uncontrolled flooding and individual-ship surrender remain distinct. '
    'No rank,kinship,weapon,casualty count,treatment promise or new outcome is invented. '
    'Fresh source evidence covers1035 voice choices,114town names and228 original assigned/unassigned town exchange prefixes. '
    'The assigned path uses one disclosed original-setter duty byte in copied RAM. '
    'Native checks pass712 layouts,34 complete native/independent font planes,34 deployed pipelines and68 copies;old synthetic-name waivers are not transferred. '
    'All34 previews on four sheets were viewed;complete leading/trailing/interior letters,blank paper,x6 margin,35-cell/four-row limits and16px stride pass. '
    'The2029 revision grows COMMON22 by14bytes to5392;its whole original direct-actor loader/printf/macro/wrap pipeline and all123repacked records/246cold-warm copies pass. '
    'All3667other complete copies and40other blocks are exact;only directory/offset metadata changes in ARM9,with every other byte restored exactly and code,font,geometry,sections,BSS,cache and123040-byte staged payload unchanged. '
    'Four new copied-state constructor probes prove member,direct-actor and scalar-numeric entries all reach the original kind0 panel,including the revised2029and2192and a native town argument. '
    'Constructor,return,town exchange and ship-caller code are clean/current/two-historical-build exact. '
    'Six preserved direct-actor town challenge2043,role1defeat2138,and substituted portrait2229/normal-return states bind the shared presentation and transition rules;the representative sheet was viewed. '
    'The initial2672probe used the pre-success2551path;preserved2672b binds the completed2551bproof. '
    'Under the user representative-sampling policy,no individual conditional visit to these34 is required;no actual town/ship surrender or current2029activation is claimed. '
    'One optional source-locked stage and one experimental profile extend the entire V2284stack;8negative cases reject before mutation. '
    'V2674contains494batches and114accepted layers. Every earlier profile and V1492promotion remains unchanged. '
    'The exact clean-input xdelta reconstructs the entire registered ROM byte for byte. '
    'Two new targeted headless cold boots complete4001NewGame and17401town/Refit frames. All30captured whole framebuffers equal verifiedV2284;five postload actor/captain controls and source/disposable donor hashes match. '
    'The town run uses the inherited five-ship Copenhagen test battery;it ends on a Refit component screen,not a claimed return to Port. '
    'The six-frame current startup/town sheet was viewed. No new RAM/code/gameplay fixture,observer or savestate is used. '
    'These are actual current startup/story/town samples,distinct from historical battle samples and copied-state native tests;no full-route or hardware verification is claimed. '
    'A final released-ROM2029pipeline/full-font check passes through the successor current parser and bounded context;modified COMMON is rejected. '
    'Fresh coverage is2184 reread /2184 integrated-reconciled /zero pending. Completion is2184(1527historically revised,657retained),source/prose2259 and incompleteCOMMON75. '
    'The34new completions comprise23historically revised and11retained entries;the current fresh pass itself makes one new English revision and33retentions. '
    'Old manifests,ROMs,translations,canonical/clean inputs and every generated ROM are preserved. '
    'Remaining drafts include market3,ship-sinking16,ship-loss/surrender24 andbattle-reactions32;five named-target2187-2191leads remain context-only and uncredited. '
    'Every never-reviewed storyline,shared shop/town dialogue,random scene and remaining player-facing prose stays in scope. '
    'Separate graphics/all18 plaques,raw rejected-record coverage,SC3B109 classification and later older-record technical re-audit remain open. Full goal active;all jobs terminal.'
)

if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,DOC,FINAL,GUIDE])
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp)
    prior_audit_path=Path('work/analysis/editorial_handoff_verification_v2671/verified_handoff.json');prior=read(prior_audit_path)
    assert sha(lp.read_bytes())==prior['ledger_sha256']
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2184,2150,34)
    releasepath=Path('work/analysis/surrender_advice_release_v2675/registered_release_verification.json')
    startpath=Path('work/analysis/surrender_advice_startup_v2677/cold_boot_startup_town_verification.json')
    samplepath=Path('work/analysis/aftermath_sampling_v2672b/representative_control_reconciliation.json')
    nativepath=Path('work/analysis/current_surrender_advice_native_v2678/released_current_native_verification.json')
    release,start,sample,native=map(read,[releasepath,startpath,samplepath,nativepath]);doc=deepcopy(read(OLD))
    assert release['candidate_sha256']==start['candidate_sha256']==native['candidate_sha256']
    assert sample['no_open_translation_specific_display_or_control_finding'] and len(sample['four_original_constructor_boundaries'])==4
    assert start['all_current_requested_and_final_framebuffers_equal_V2284'] and start['all_five_postload_actor_model_and_captain_checks_equal']
    assert sum(len(r['paired_whole_frames']) for r in start['runs'])==30 and [r['frames'] for r in start['runs']]==[4001,17401]
    assert release['whole_ROM_reconstruction_byte_exact'] and native['complete_native_independent_plane_and_prior_reviewed_pixels_equal']
    sheets=read(doc['current_native_font_proof'])['review_sheets']+[
        dict(path=sample['review_sheet'],sha256=sample['review_sheet_sha256']),dict(path=start['review_sheet'],sha256=start['review_sheet_sha256'])]
    for s in sheets:assert sha(Path(s['path']).read_bytes())==s['sha256']
    rompath=Path(release['candidate']);rom=NdsImage.open(rompath);arm,common=rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm)
    assert sha(rompath.read_bytes())==release['candidate_sha256'] and sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    manifest=read(rompath.with_suffix('.manifest.json'));stage=manifest['relocations']['/COMMON/MESFILE.DK4']['surrender_advice_contextual'];cp=Path(stage['release_config']);conf=read(cp)
    assert sha(cp.read_bytes())==stage['release_config_sha256'] and conf['manuscript']==str(OLD)
    baseowner=doc['registered_prose_owner_bindings'][0];source_rows={r['message_id']:r for r in read(baseowner['manuscript'])['records']}
    def ref(r):return dict(block=r.block,offset=r.block_offset,copy_end=r.copy_end,bytes=len(r.text),record_index=r.record_index,table_offset=r.table_offset,start_in_record=r.start)
    for row in doc['records']:
        n=row['message_id'];target=entries[n];assert compiled(row)==target.text
        row.update(fresh_review_input_current_reference=row['current_reference'],fresh_review_input_current_hex=row['current_hex'],
            original_source_prose_editorial_decision=source_rows[n]['editorial_decision'],
            completed_editorial_decision='revise' if n==2029 else source_rows[n]['editorial_decision'],
            current_reference=ref(target),current_hex=target.text.hex(),current_text_hex=target.text.hex(),
            current_stored_English=target.text.decode('ascii'),current_English=target.text[1:].decode('ascii'),
            integrated_reference=ref(target),integrated_hex=target.text.hex(),
            status='contextual-current-native-representative-and-registered-release-complete',
            completed_candidate_reference=str(rompath),registered_review_stage='surrender_advice_contextual',
            representative_reconciliation=str(samplepath),actual_holds=[],individual_actual_activation_not_claimed=True,
            completion_credit_added=1,all_source_native_representative_and_registered_gates_pass=True)
        row['decision']='revised-and-integrated' if row['completed_editorial_decision']=='revise' else 'retained-and-editorially-reviewed'
    assert Counter(r['completed_editorial_decision'] for r in doc['records'])=={'revise':23,'retain':11}
    owner=dict(stage='surrender_advice_contextual',config=str(cp),config_sha256=sha(cp.read_bytes()),manuscript=conf['manuscript'],
        manuscript_sha256=sha(OLD.read_bytes()),selected_IDs=[r['message_id'] for r in doc['records']],compiler='scripts.battle_aftermath_native_plan_v1255.compiled')
    doc.update(current_ROM=str(rompath),current_ROM_sha256=release['candidate_sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),
        status='complete-contextual-current-native-and-registered-release',registered_review_binding=owner,
        representative_reconciliation=str(samplepath),representative_reconciliation_sha256=sha(samplepath.read_bytes()),
        current_released_native_proof=str(nativepath),current_released_native_proof_sha256=sha(nativepath.read_bytes()),
        registered_release_proof=str(releasepath),registered_release_proof_sha256=sha(releasepath.read_bytes()),
        current_startup_proof=str(startpath),current_startup_proof_sha256=sha(startpath.read_bytes()),
        all_six_native_historical_current_review_sheets_viewed=True,current_native_and_representative_reconciliation_pending=False,
        registered_revision_integration_pending=False,actual_selected34_IDs=[],new_emulator_runs=2,
        completion_credit_added=34,source_prose_credit_added=0)
    validate_natural_dialogue_batch(doc)
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text().startswith('# Current editorial handoff - V2670')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    save(DOC,doc)
    paths=[OLD,DOC,releasepath,startpath,samplepath,nativepath,cp,Path(doc['current_native_font_proof']),Path(doc['revision_payload_plan']),
        Path(doc['source_context_packet']),Path(doc['native_context_proof']),Path(doc['fresh_ordinary_supplement']),
        Path('work/analysis/surrender_advice_registration_v2673/registration_receipt.json'),
        Path('scripts/current_common_native_context_v2677.py'),Path('dk4tool/patch/surrender_advice_contextual_v1.py'),
        Path('scripts/verify_current_surrender_advice_native_v2678.py'),Path(__file__),prior_audit_path,*[Path(s['path']) for s in sheets]]
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    save(FINAL,dict(format='dk4-editorial-final-review-v1',family=FAMILY,file_path='/COMMON/MESFILE.DK4',
        native_message_IDs=[r['message_id'] for r in doc['records']],revised_count=1,retained_count=33,
        new_completed_records=34,historical_decisions_newly_completed=dict(revised=23,retained=11),records=doc['records'],
        summary=SUMMARY,evidence=evidence,registered_review_binding=owner,
        candidate=str(rompath),candidate_sha256=release['candidate_sha256'],profile='all-routes-unified-v2674',
        patch=release['patch'],patch_sha256=release['patch_sha256'],whole_clean_input_reconstruction_exact=True,
        actual_selected34_IDs=[],representative_historical_IDs=[2043,2138,2229],current_startup_emulator_runs=2,
        current_startup_captured_frames=30,current2029_native_pipeline_verified=True,current2029_actual_activation_claimed=False,
        all_review_sheets_viewed=True,full_goal_complete=False))
    selected={('/COMMON/MESFILE.DK4',r['id']) for r in doc['records']};existing={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert len(selected)==34 and not selected&existing
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/COMMON/MESFILE.DK4',native_message_IDs=owner['selected_IDs'],
        record_IDs=[r['id'] for r in doc['records']],final_review=str(FINAL),revised_count=23,retained_count=11,
        fresh_revisions=1,fresh_retentions=33,actual_verification_scope='Shared constructor/source/representative historical rules plus two current startup/town runs. No selected34individual surrender or2029activation claim.',records=doc['records']))
    ledger['records_editorially_completed']=2184;ledger['records_revised_and_integrated']=1527;ledger['retained_wordings_editorially_completed']=657
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']=1527
    ids=set(owner['selected_IDs']);ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in ids]
    active=ledger['active_source_prose_drafts'];active['native_message_IDs']=[n for n in active['native_message_IDs'] if n not in ids]
    for key,ns in active['manuscript_record_subsets_pending'].items():active['manuscript_record_subsets_pending'][key]=[n for n in ns if n not in ids]
    oldcandidate=deepcopy(ledger['current_integrated_candidate']);ledger['previous_current_integrated_candidate_before_V2674']=oldcandidate
    ledger['integrated_candidate_reference_history'].append(dict(path=oldcandidate['path'],sha256=oldcandidate['sha256'],profile=oldcandidate['profile'],superseded_by=str(rompath),reason='Source-bound2029courteous recommendation;fullV2284stack retained.'))
    candidate=deepcopy(oldcandidate);candidate.update(path=str(rompath),sha256=release['candidate_sha256'],profile='all-routes-unified-v2674',
        MESFILE_sha256=sha(common),ARM9_sha256=sha(arm),patch=release['patch'],patch_sha256=release['patch_sha256'],
        manifest=str(rompath.with_suffix('.manifest.json')),status='experimental-verified-editorial-checkpoint-not-promoted',details=SUMMARY)
    for i in range(4):candidate[f'SC{i}_sha256']=release['story_hashes'][f'SC{i}']
    ledger['current_integrated_candidate']=candidate;ledger['latest_registered_editorial_candidate']=deepcopy(candidate)
    ledger['native_relocation_reference_before_V2674']=deepcopy(ledger['current_native_relocation_reference'])
    ledger['current_native_relocation_reference']=dict(module='dk4tool.patch.surrender_advice_contextual_v1',function='current_entries',
        release_config=str(cp),ARM9_sha256=sha(arm),COMMON_sha256=sha(common),whole_target_and_directory_source_locks=True,
        bounded_context_helper='scripts/current_common_native_context_v2677.py')
    fresh.update(fresh_pass_records_integrated=2184,fresh_pass_records_pending_native_actual_release=0,
        integrated_record_keys=deepcopy(fresh['record_keys']),pending_record_keys=[],pending_contextual_families=[],
        latest_pending_contextual_family=None,latest_contextual_manuscript=str(DOC),latest_completed_family=FAMILY,
        latest_final_review=str(FINAL),latest_contextual_retention_review=str(FINAL),
        coverage_note='2184fresh rereads andregistered reconciliations;34new aftermath completions include one fresh tone revision and33retentions. Source/prose2259 and75incompleteCOMMON remain;all wider never-reviewed prose andfive named-target leads remain in scope.')
    fresh['reconciled_families'].append(dict(id=FAMILY,records=34,final_review=str(FINAL),new_revisions=1,justified_retentions=33,
        new_completed_records=34,historical_reconciliation_only=False,historical_decisions_newly_completed=dict(revised=23,retained=11),
        actual_selected34_IDs=[],current_startup_emulator_runs=2,profile='all-routes-unified-v2674'))
    active['note']=fresh['coverage_note'];ledger['latest_checkpoint']=SUMMARY
    ledger['aftermath_remaining_contextual_v2679']=dict(summary=SUMMARY,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['formatting_watchlist']['aftermath_remaining_v2679']=dict(status='complete-native-representative-and-registered2674',final_review=str(FINAL),new_runtime_or_geometry_change=False)
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v2664']['path']))
    inventory['incomplete_COMMON_source_prose_groups']=[g for g in inventory['incomplete_COMMON_source_prose_groups'] if g['family']!='battle-aftermath-unfinished']
    inventory.update(incomplete_COMMON_count=75,next_focus='Complete market3,ship-sinking16,ship-loss/surrender24 andbattle-reactions32;then all never-reviewed route/shared/town/shop/random/player-facing prose,including five separately uncredited named-target outcomes. This is not the entire source universe.')
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    assert {n for g in inventory['incomplete_COMMON_source_prose_groups'] for n in g['IDs']}==set(ledger['reviewed_but_incomplete_COMMON_IDs']) and sum(g['count'] for g in inventory['incomplete_COMMON_source_prose_groups'])==75
    ledger['unfinished_editorial_scope_v2679']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=75,full_goal_complete=False)
    save(lp,ledger)
    section='## V2679: Aftermath34 completed in registered cumulative V2674\n\n'+SUMMARY+'\n\nFinal review: '+FINAL.as_posix()+'. Release/patch proof: '+releasepath.as_posix()+'. Current startup: '+startpath.as_posix()+'. Current parser: dk4tool.patch.surrender_advice_contextual_v1.current_entries. Current bounded context: scripts/current_common_native_context_v2677.py. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text().split('\n',1);p.write_text(('# Current editorial handoff - V2679' if i==0 else first)+'\n\n'+section+rest,newline='\n')
    GUIDE.mkdir(parents=True);images=[]
    for i,s in enumerate(sheets):
        kind='current-native-CPU' if i<4 else 'historical-other-family-representative' if i==4 else 'current-headless-startup-town'
        target=GUIDE/(kind+'_'+Path(s['path']).name);copy2(s['path'],target);images.append(dict(path=str(target),sha256=s['sha256'],kind=kind))
    save(GUIDE/'scope.json',dict(candidate=str(rompath),candidate_sha256=release['candidate_sha256'],images=images,
        actual_selected34_IDs=[],current2029_native_not_gameplay=True,current_startup_runs=2,all_scopes_distinct=True,full_goal_complete=False))
    evidence.update({str(FINAL):sha(FINAL.read_bytes()),str(inv):sha(inv.read_bytes())})
    save(ROOT/'completion_receipt.json',dict(checkpoint='V2679',summary=SUMMARY,new_completed_records=34,new_current_prose_revisions=1,
        fresh_justified_retentions=33,historical_revisions_newly_completed=23,historical_retentions_newly_completed=11,
        fresh_reread=2184,fresh_integrated=2184,fresh_pending=0,completed_records=2184,historical_revised=1527,historical_retained=657,
        source_prose_reviewed=2259,COMMON_incomplete=75,candidate=str(rompath),candidate_sha256=release['candidate_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],guide=str(GUIDE),evidence=evidence,
        updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs,DOC,FINAL]},goal_turn_classification='progress',
        current_startup_runs=2,actual_selected34_IDs=[],all_jobs_terminal=True,full_goal_complete=False))
    print('V2679:34new completions;2184fresh reconciled,1527historical revisions/657retentions;2259source/prose,75incompleteCOMMON. Registered2674/494batches,exactcleanpatch and2coldboots pass. Full goal active.')
