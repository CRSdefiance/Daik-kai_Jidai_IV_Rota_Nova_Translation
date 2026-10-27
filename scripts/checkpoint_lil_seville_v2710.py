"""Record20 newly reviewed source/prose objects;full native/release pending."""
from pathlib import Path
from copy import deepcopy
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Seville_checkpoint_v2710')
DOC=Path('translations/lil_seville_encounter_editorial_manuscript_v2.json')
CHOICES=Path('translations/lil_seville_choices_editorial_draft_v1.json')
SOURCE=Path('work/analysis/lil_Seville_source_v2704b/complete20_clean_current_native_context.json')
CONTROL=Path('work/analysis/lil_Seville_controls_v2706b/source_bound_B28_B29_presenter_and_control_contract.json')
BRANCH=Path('work/analysis/lil_Seville_branches_v2705/original_relative_skip_operand_proof.json')
BODY=Path('work/analysis/lil_Seville_body_probe_v2708b/body_only_layout_and_native_fonts.json')
NOTES=Path('work/analysis/lil_Seville_layout_notes_v2709/line_count_waivers.json')
FAMILY='Lil-Seville-Valdes-B28-B29-20-source-prose'
SUMMARY=(
    'V2710 reviews the complete clean-Japanese Lil/Valdes Seville exchange in SC2B28andB29:20editorial objects,with17proposed revisions and3individually justified retentions. '
    'Native command walking identifies17progressive speeches,one FEshare-loss panel andtwo typed reply labels. This includes the previously omitted punctuation-only Lil reaction B28R0065,which Japanese-only CSV filtering missed. '
    'Valdes contempt andmilitary intimidation,Lil offended dignity anddefiance,Gerhard hesitant recognition andqualified counsel,Fernando avoidance,andJanus alarm remain distinct. '
    'Restore complete self-introduction andthe explicit Spanish admiral/navy claim,the source Invincible Armada designation,full-strength threat,stammers,appearance qualification andcomplete acknowledgment/refusal choices. Remove the unsupported piracy implication andthe invented withdraw-and-live survival promise. No relationship,extra rank,weapon,death orguaranteed outcome is added. '
    'Retain Could that be...?,So it is Valdes...,andOur share in Seville has fallen,withindividual reasons. All20have fresh glosses,localization notes andexact clean/current references;prose is unwrapped withcompiler-owned layout. '
    'The original69command shapes match current data. Native tests verify28relative-skip sites at280clean/current cases andboth original typed-choice labels/count/pointers. Thirty-six historical copied-state dispatcher/macro/caller-return contexts bind actor2/4/16/20/31andthe separate FE5473Cpath,withwhole4MiB,input guards andsaved-register ABI exact. UIpreparation940B0andpanel bodies are explicit unexecuted boundaries. '
    'Three existing reviewed-name catalog calls andthe existing FE54798wrap call are separated from clean-exact spans. Preserved2704/2706predecessors stopped before producing approval onoverly broad clean-code assertions;2704band2706bbind those owned calls correctly. No new runtime change is made. '
    'The conservative body probe passes18layouts and17complete native/independent216x64progressive font planes withhost default macro substitution. Allthree sheets were viewed. This is not native macro execution orfull consumer approval. '
    'Eight source/English line-count differences are individually documented because ordinary Japanese wrapping is not an English layout constraint. The first2708probe rejected those warnings;preserved2708bpasses withthe narrow notes. No overflow,orphan,predicate,control orblank-page waiver is granted. Full native QA still must assess phrase breaks,including Gerhard115. '
    'Current whole macro contexts,scoped progressive/FEprofiles,228x48FEpaper/pagination,typed-choice geometry/full fonts,complete relocation/reference proofs,representative reconciliation andregistered cumulative integration remain pending. No individual Seville activation,Janus/Valdes portrait/nameplate sighting,new emulator run orcurrent startup is claimed. '
    'Fresh coverage is2276 reread /2256 integrated-reconciled /20pending. Source/prose is2279,including449SC2;completion remains2256(1575historically revised,681retained). The20are new source/prose reviews withzero completion credit. Three marketCOMMON entries andall wider untouched prose remain open. '
    'The frozen raw native-source census remains valid source/navigation evidence,not a full-ROM dialogue denominator. Five named-target2187-2191leads remain separately uncredited. Every storyline,shared shop/town dialogue,random scene andremaining player-facing prose stays in scope. '
    'Registered cumulative experimentalV2674 remains494batches/114accepted layers withits exactly reconstructable clean-input patch. No ROM,registry,builder,profile,manifest orpatch changes occur;V1492 remains promoted. All ROMs,earlier translations,canonical/clean inputs andexecuted proofs are preserved. '
    'Separate graphics/all18plaques,raw rejected-object classification,SC3B109classification andlater older-record technical re-audit remain open. Full goal active;all jobs terminal.'
)
if __name__=='__main__':
    assert not ROOT.exists();lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    priorpath=Path('work/analysis/editorial_handoff_verification_v2703/verified_handoff.json');assert sha(lp.read_bytes())==read(priorpath)['ledger_sha256']
    doc,choice,source,control,branch,body,notes=map(read,[DOC,CHOICES,SOURCE,CONTROL,BRANCH,BODY,NOTES]);rows=doc['records']+choice['records'];ids=[r['id'] for r in rows]
    assert len(rows)==len(set(ids))==20 and sum(r['editorial_decision']=='revise' for r in rows)==17 and sum(r['editorial_decision']=='retain-wording' for r in rows)==3
    assert all(all(r['review'][g] for g in ['source','context','localization','naturalness']) and not r['review']['formatting'] and r['source_meaning'] and r['localization_note'] for r in rows)
    assert source['total_editorial_objects']==20 and len(branch['cases'])==280 and len(control['all36_source_current_text_contexts_dispatch_to_correct_actor_or_FE'])==36
    assert body['manuscript_sha256']==sha(DOC.read_bytes()) and len(body['records'])==18 and body['actual_progressive_planes']==17 and body['failures']==[] and len(body['review_sheets'])==3
    assert len(notes['waivers'])==8 and notes['English_and_controls_unchanged']
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2256,2256,0)
    keys={(r['file_path'],r['id']) for r in fresh['record_keys']};selected=[dict(file_path='/data/SC2.DK4',id=n) for n in ids];assert not {(r['file_path'],r['id']) for r in selected}&keys
    completed={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']};assert completed==keys
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==2259
    assert not any(ledger['reviewed_but_incomplete_route_record_IDs'].values())
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']];assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V2702')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=2279
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']=449
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=ids
    active=ledger['active_source_prose_drafts']
    for path,records in [(DOC,doc['records']),(CHOICES,choice['records'])]:
        active['manuscripts'].append(str(path));active['route_record_subsets_pending'][str(path)]=[r['id'] for r in records]
    active.update(status='3-reviewed-COMMON-incomplete;20fresh-Seville-route-drafts;historical-manuscripts-preserved',note='2276fresh rereads:2256reconciled and20Seville source/prose drafts pending full native/FE/menu/reference/registered-release gates. Source/prose2279;3marketCOMMON entries unresolved;all wider prose remains in scope.')
    fresh['record_keys'].extend(selected);fresh['record_IDs'].extend(ids)
    pending=dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[28,29],records=20,record_keys=selected,manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),choices=str(CHOICES),choices_sha256=sha(CHOICES.read_bytes()),proposed_revisions=17,retentions=3,
        source_prose_reviews_added=20,completion_credit_added=0,body_probe=str(BODY),pending='Current whole macro contexts;scoped progressive/FEprofiles;FEpaper/menu geometry andfull fonts;complete reference/relocation map;representative reconciliation;optional registered cumulative layer/full clean patch/required startup checks.',new_emulator_runs=0)
    fresh.update(fresh_pass_records_explicitly_reread=2276,fresh_pass_records_integrated=2256,fresh_pass_records_pending_native_actual_release=20,pending_record_keys=selected,pending_contextual_families=[pending],latest_pending_contextual_family=FAMILY,
        latest_contextual_manuscript=str(DOC),latest_contextual_choice_draft=str(CHOICES),coverage_note=active['note'])
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=677,completed_route_records=657,next='Complete the20Seville source/prose drafts through full native/reference/registered-release gates,then continue untouched route/shared/town/random/player prose. Other-route openings remain included in the677/657file-qualified totals.')
    ledger['coverage_units'].append(dict(**pending,status='source-context-prose-reviewed;full-native-reference-representative-release-pending',full_goal_complete=False))
    ledger['formatting_watchlist']['lil_Seville_v2710']=dict(status='body-only18layouts/17progressive-planes-pass;full-consumer-and-release-pending',source_context=str(SOURCE),control_contract=str(CONTROL),body_probe=str(BODY),manuscript=str(DOC),choices=str(CHOICES),
        FE_panel_and_typed_choice_native_approval_pending=True,current_macro_alignment_execution_pending=True,reference_map_pending=True,all_three_body_sheets_viewed=True,phrase_breaks_require_full_QA=['DK4_MES_B28_R0115'],no_orphan_predicate_or_missing_glyph_waivers=True,actual_Seville_IDs=[],new_emulator_runs=0)
    requirements=ROOT/'next_registered_integration_requirements.json';save(requirements,dict(parent_profile='all-routes-unified-v2674',parent_ROM=doc['current_ROM'],parent_ROM_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),choices=str(CHOICES),choices_sha256=sha(CHOICES.read_bytes()),
        source_context=str(SOURCE),control_contract=str(CONTROL),branch_proof=str(BRANCH),body_only_probe=str(BODY),blocks=[28,29],progressive=17,FE_panels=1,choice_labels=2,
        next='Create an exact B28/B29/current-ARM scoped profile;execute all logical/wrapped original macro contexts at four input alignments under bounded current-code overlays;check complete native progressive fonts andfull QA/phrase breaks,FE228x48paper/pagination andtyped menu geometry/selected-result mapping. Prove all69native commands,28relative operands,two label offsets andexternal entry references under relocation;preserve334other SC2blocks andallother ROM files/ARM/runtime. Bind established progressive/FE/menu representative evidence andresolve only distinct concrete risks. Add one optional registered layer after the full2674stack,build through build_integrated_release.py,verify ancestry/manifest/whole-source guards,exact clean-input patch andrequired cold-start/story/town samples,then reconcile20onlywhen all gates pass.',
        do_not_require_all_conditional_or_individual_speaker_gameplay_visits=True,no_actual_Seville_or_Janus_Valdes_nameplate_claim=True,preserve_every_prior_ROM_translation_profile_accepted114_and_V1492_promotion=True,no_new_ROM_or_registration_created_here=True,full_goal_complete=False))
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v2702']['path']));inventory.update(incomplete_route_source_prose_groups=[dict(family=FAMILY,file_path='/data/SC2.DK4',blocks=[28,29],count=20,record_IDs=ids)],incomplete_route_source_prose_count=20,next_focus='Finish Seville20full native/reference/release gates;continue all wider untouched source,withmarket750-752callers andraw rejected-object classification remaining open.')
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=677,completed_route_records=657,source_prose_pending_records=20,source_prose_pending_family=FAMILY,next=inventory['next_focus'])
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory);ledger['unfinished_editorial_scope_v2710']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=20,full_goal_complete=False)
    proofpaths=[DOC,CHOICES,SOURCE,CONTROL,BRANCH,BODY,NOTES,requirements,inv,priorpath,Path(__file__),*[Path(s['path']) for s in body['review_sheets']]];evidence={str(p):sha(p.read_bytes()) for p in proofpaths}
    ledger['lil_Seville_source_prose_v2710']=dict(summary=SUMMARY,**pending,evidence=evidence,goal_turn_classification='progress',full_goal_complete=False);ledger['latest_checkpoint']=SUMMARY
    for key in ['completed_editorial_families','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal']:
        assert ledger[key]==before[key],key
    assert len(fresh['record_keys'])==len({(r['file_path'],r['id']) for r in fresh['record_keys']})==2276 and len(fresh['integrated_record_keys'])==2256
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    section='## V2710: Lil Seville20 source/context/prose review; integration pending\n\n'+SUMMARY+'\n\nManuscript: '+DOC.as_posix()+'. Choices: '+CHOICES.as_posix()+'. Source: '+SOURCE.as_posix()+'. Body-only probe: '+BODY.as_posix()+'. Next integration: '+requirements.as_posix()+'. Unfinished scope: '+inv.as_posix()+'. Current parser: dk4tool.patch.surrender_advice_contextual_v1.current_entries. Current bounded CPU context: scripts/current_common_native_context_v2677.py.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1);p.write_text(('# Current editorial handoff - V2710' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    candidate=ledger['current_integrated_candidate'];save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V2710',summary=SUMMARY,evidence=evidence,updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},new_completed_records=0,new_source_prose_reviews=20,proposed_revisions=17,justified_retentions=3,fresh_reread=2276,fresh_integrated=2256,fresh_pending=20,source_prose=2279,completed=2256,historical_revised=1575,historical_retained=681,incomplete_COMMON=3,incomplete_route=20,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],next_requirements=str(requirements),actual_Seville_IDs=[],new_emulator_runs=0,goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V2710:20new source/prose reviews,17proposed revisions/3retentions;2276reread/2256reconciled/20pending. Source/prose2279;2674ROM/patch unchanged,full goal active.')
