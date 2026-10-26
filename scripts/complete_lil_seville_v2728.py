"""Reconcile20 only after registered build,patch and actual current startup."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from collections import Counter
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Seville_completion_v2728')
DOC=Path('translations/lil_seville_encounter_editorial_manuscript_v4.json')
CHOICES=Path('translations/lil_seville_choices_editorial_draft_v3.json')
FINAL=Path('translations/lil_seville_contextual_final_review_v1.json')
RELEASE=Path('work/analysis/lil_Seville_release_v2725/registered_release_verification.json')
START=Path('work/analysis/lil_Seville_startup_v2727/cold_boot_Lil_startup_town_verification.json')
FAMILY='Lil-Seville-Valdes-B28-B29-20-contextual-completed'
SUMMARY=(
    'V2728 completes the20 reviewed Lil/Valdes Seville objects in SC2B28/B29:17progressive speeches,one FEshare-loss panel andtwo typed replies. '
    'The clean-Japanese complete confrontation,withdrawal/refusal branches andseparate later change-of-mind exchange yield17revisions and3individually justified retentions. '
    'Valdes contempt andmilitary intimidation,Lil offended dignity,Gerhard hesitant recognition andqualified advice,Fernando avoidance,andJanus alarm remain distinct. '
    'Restore the complete self-introduction,explicit Spanish admiral/navy claim,Invincible Armada designation,full-strength threat,stammers,appearance qualification andcomplete reply meanings. '
    'Remove the unsupported piracy implication andthe invented withdrawal-and-live survival promise. No relationship,extra rank,weapon,death orguaranteed outcome is added. '
    'Retain Could that be...?,So it is Valdes...,andOur share in Seville has fallen,withindividual reasons. The punctuation-only Lil reaction B28R0065 is included. '
    'All20 have fresh source glosses,context/localization notes,exact clean/current/integrated references andallfive review gates. '
    'Scoped source/runtime-bound profiles preserve complete speaker preambles,ordinary actor IDs2/4/16/20/31,separate FEdispatch,original macros andcompiler-owned pair-safe layout. '
    'Current native tests pass18complete font planes,144logical/compiled macro alignment cases and72additional final-padding alignment cases. '
    'Whole first/final/interior glyphs,blank paper,bounds,16px row advance,FE228x48mode1paper/pagination andtyped-menu centering pass. '
    'Eight individually justified line-count-only notes accept ordinary source wrapping differences;no overflow,orphan,predicate,control orblank-page waiver is granted. Gerhard115 phrase flow is reviewed. '
    'All five font/menu sheets were viewed orhash-identical to previously viewed sheets. The FEcold typed-object reconstruction matches a preserved actual tutorial hold without installing captured initializedRAM. '
    'All69original native commands,28relative sites/140relocated cases,source headers,choiceorder/results0/1/cancel andevery unowned logical byte are preserved. '
    'All336whole SC2loaders/cachehits andtwo parent-entry modes pass;the shipped entry census finds only the original interpreter call. '
    'B28grows1156to1404bytes;B29grows224to240;334other SC2blocks remain exact. '
    'Four preserved historical Lil/Gerhard holds freshly match current complete ink,gray andblank RGB masks. '
    'The exact registered96-byte town-service ITCMwrapper change is separately bound to its owner;all other compared ITCMbytes andthe deployed123040-byte payload are exact. '
    'Historical two-choice menu,normal Hamburgreturn andFEtutorial paper supply representative shared rules;three inherited travel/funds access fixtures remain disclosed andunearned. '
    'Under the user representative policy,no new translation-specific display/control finding requires an individual conditional Seville orJanus/Valdes portrait visit. '
    'No Seville activation,choice1gameplay,new earned route progress,full-route orhardware verification is claimed. '
    'One guarded optional stage after the complete V2674stack registers cumulative experimentalV2724 with496batches/114accepted layers. '
    'Fifteen negative cases reject before mutation. OnlySC2B28/B29change fromV2674;ARM9,COMMON,allother files,graphics,components,section/BSS/cache extents and123040staged bytes remain exact. '
    'The clean-input xdelta reconstructs the whole registered ROM byte for byte. '
    'Two current targeted headless cold boots complete4001LilNewGame and17401town/Refitframes,plus anindependent4001frame V2674Lil control. '
    'Every captured current whole framebuffer matches V2674;five postload actor/captain controls,actual Lil2/B22resident payload andsource/disposable town-donor hashes pass. '
    'The town sample uses the inherited five-ship Copenhagen test battery andends onthe Refit component screen. No new RAM/code/gameplay fixture,observer orsavestate is used. The six-frame current sheet was viewed. '
    'Fresh coverage is2276 reread /2276 integrated-reconciled /zero pending. Completion is2276(1592historically revised,684retained);source/prose remains2279. '
    'Completed file counts are1599COMMON,449SC2,117SC0,73SC1and38SC3. Three COMMONmarket records750-752 remain incomplete;all wider untouched story/shared shop/town/random/player prose remains in scope. '
    'The raw native-source census remains navigation evidence,not a dialogue denominator;five named-target2187-2191leads remain separately uncredited. '
    'All prior ROMs,translations,profiles,114accepted layers,canonical/clean inputs andexecuted proofs are preserved;V1492 remains promoted. '
    'Separate graphics/all18plaques,raw rejected-object classification,SC3B109classification andlater older-record technical re-audit remain open. Full goal active;all jobs terminal.'
)

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    prior=Path('work/analysis/editorial_handoff_verification_v2711/verified_handoff.json')
    assert sha(lp.read_bytes())==read(prior)['ledger_sha256']
    release,start=read(RELEASE),read(START)
    assert release['whole_ROM_reconstruction_byte_exact'] and release['all496_manifest_batches_and114_accepted_layers_present']
    assert start['all_current_requested_and_final_framebuffers_equal_V2674'] and start['all_five_postload_actor_model_and_captain_checks_equal']
    assert start['current_Lil_captain2_and_B22_payload_verified'] and start['source_and_disposable_town_donor_unchanged']
    assert start['actual_Seville_IDs']==[] and sha(Path(start['review_sheet']).read_bytes())==start['review_sheet_sha256']
    # The six current frames were viewed before executing this producer.
    doc,choices=read(DOC),read(CHOICES);mapping=read(doc['reference_map']);rows=deepcopy(doc['records']+choices['records'])
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':17,'retain-wording':3}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['localization_note'] for r in rows)
    image=NdsImage.open(release['candidate']);blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==start['candidate_sha256']
    refs={r['id']:r for b in mapping['blocks'] for r in b['text_records']}
    for row in rows:
        block=blocks[row['block']]
        if row['kind']=='typed-choice-label':
            spec=next(c for b in mapping['blocks'] if b['block']==row['block'] for c in b['choice_commands'])
            at=spec['new_offset'];offset=at+6+int.from_bytes(block[at+2+row['option_index']*2:at+4+row['option_index']*2],'little')
            value=block[offset:block.index(b'\0',offset)];assert value==row['english'].encode('ascii')
        else:
            spec=refs[row['id']];offset=spec['new_offset'];value=bytes.fromhex(spec['target_hex'])
            assert block[offset:offset+len(value)]==value and block[offset-5:offset]==bytes.fromhex('0040ffff00')
        row['historical_source_prose_predecessor_fields']={k:deepcopy(row[k]) for k in ['current_reference','current_hex','current_English','current_record_index','record_index'] if k in row}
        reference=dict(block=row['block'],offset=offset,bytes=len(value),record_index=block[:offset].count(b'\0'))
        row.update(current_reference=reference,current_hex=value.hex(),current_text_hex=value.hex(),integrated_reference=reference,
            integrated_hex=value.hex(),completed_candidate_reference=release['candidate'],registered_prose_owner='lil_seville_editorial',
            registered_manuscript=str(CHOICES if row['kind']=='typed-choice-label' else DOC),
            historical_editorial_decision='revise' if row['editorial_decision']=='revise' else 'retain',
            decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-and-editorially-reviewed',
            individual_actual_activation_not_claimed=True,all_source_native_representative_and_registered_gates_pass=True,
            status='complete-contextual-current-native-references-representative-and-registered-release')
        row['current_English']=(value if row['kind']=='typed-choice-label' else value[1:]).decode('ascii')
        if row['kind']!='typed-choice-label':
            row['current_record_index']=row['record_index']=reference['record_index']
    selected={(r['file_path'],r['id']) for r in rows};fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert len(selected)==20 and {(r['file_path'],r['id']) for r in fresh['pending_record_keys']}==selected
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2276,2256,20)
    oldkeys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']};assert not oldkeys&selected
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V2710')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    review=ROOT/'current_six_frame_visual_review.json';save(review,dict(sheet=start['review_sheet'],sha256=start['review_sheet_sha256'],viewed=True,
        findings='Lil selection and opening dialogue and inherited town/Refit component screens are legible and match V2674. Current startup only; no Seville activation.'))
    proofpaths=[DOC,CHOICES,Path(doc['reference_map']),Path(doc['native_font_proof']),Path(doc['representative_proof']),Path(doc['representative_sheet_review']),RELEASE,START,prior,review,Path(__file__),
        Path('work/analysis/lil_Seville_registration_v2723/registration_receipt.json'),Path('work/analysis/lil_Seville_registration_v2723/negative_cases.json'),
        Path('work/analysis/lil_Seville_research_v2718/research_image_receipt.json'),
        Path('work/analysis/lil_Seville_reference_census_v2720/all69_commands28_relative_sites_and_shipped_entry_census.json'),
        Path('work/analysis/lil_Seville_loader_v2719/whole_SC2_and_B28_B29_initial_entry_proof.json')]
    evidence={str(p):sha(p.read_bytes()) for p in proofpaths}
    save(FINAL,dict(format='dk4-natural-dialogue-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        id=FAMILY,manuscript=str(DOC),choices=str(CHOICES),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        revised=17,retained=3,records=rows,summary=SUMMARY,evidence=evidence,actual_Seville_IDs=[],
        new_current_candidate_emulator_runs=2,new_independent_control_runs=1,current_six_frame_sheet_viewed=True,full_goal_complete=False))
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[28,29],record_IDs=[r['id'] for r in rows],
        final_review=str(FINAL),revised_count=17,retained_count=3,fresh_revisions=17,fresh_retentions=3,
        actual_verification_scope='Historical shared progressive/menu/FE rules plus two current cold-start/story/town samples; no Seville activation.',records=rows))
    ledger.update(records_editorially_completed=2276,records_revised_and_integrated=1592,retained_wordings_editorially_completed=684)
    ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4']=449
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=[]
    active=ledger['active_source_prose_drafts']
    for p,ids in active['route_record_subsets_pending'].items():
        active['route_record_subsets_pending'][p]=[ident for ident in ids if ('/data/SC2.DK4',ident) not in selected]
    for p in [DOC,CHOICES]:
        if str(p) not in active['manuscripts']:active['manuscripts'].append(str(p))
        active['route_record_subsets_pending'][str(p)]=[]
    active.update(status='3-reviewed-COMMON-incomplete;no-pending-route-drafts;historical-manuscripts-preserved',
        note='2276fresh rereads integrated/reconciled;source/prose2279. MarketCOMMON750-752caller context unresolved;all wider untouched prose remains in scope.')
    fresh['integrated_record_keys'].extend(fresh['pending_record_keys'])
    fresh.update(fresh_pass_records_integrated=2276,fresh_pass_records_pending_native_actual_release=0,pending_record_keys=[],pending_contextual_families=[],
        latest_pending_contextual_family=None,latest_contextual_manuscript=str(DOC),latest_contextual_choice_draft=str(CHOICES),
        latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=active['note'])
    fresh['reconciled_families'].append(dict(id=FAMILY,records=20,final_review=str(FINAL),new_revisions=17,justified_retentions=3,new_completed_records=20,
        historical_reconciliation_only=False,historical_decisions_newly_completed=dict(revised=17,retained=3),actual_Seville_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=1))
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=677,completed_route_records=677,next='Continue untouched route/shared/town/random/player prose. All-route review remains open.')
        if unit['id']=='Lil-Seville-Valdes-B28-B29-20-source-prose':unit.update(status='complete-contextual-current-native-references-representative-and-registered-release',pending=None,completion_credit_added=20,final_review=str(FINAL),full_goal_complete=False)
    watch=ledger['formatting_watchlist']['lil_Seville_v2710']
    watch.update(status='complete-through-V2728',FE_panel_and_typed_choice_native_approval_pending=False,current_macro_alignment_execution_pending=False,reference_map_pending=False,
        phrase_breaks_require_full_QA=[],superseded_by='lil_Seville_v2728',final_review=str(FINAL))
    ledger['formatting_watchlist']['lil_Seville_v2728']=dict(status='all20-source-native-reference-representative-release-checks-pass',final_review=str(FINAL),evidence=evidence,
        actual_Seville_IDs=[],individual_conditional_visits_not_required_under_user_policy=True,no_orphan_predicate_or_missing_glyph_waivers=True)
    oldcandidate=deepcopy(ledger['current_integrated_candidate']);ledger['previous_current_integrated_candidate_before_V2724']=oldcandidate
    ledger['integrated_candidate_reference_history'].append(oldcandidate)
    candidate=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=SUMMARY,full_goal_complete=False,
        **{key+'_sha256':digest for key,digest in release['story_hashes'].items()})
    ledger['current_integrated_candidate']=candidate;ledger['latest_registered_editorial_candidate']=deepcopy(candidate)
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v2710']['path']))
    inventory.update(incomplete_route_source_prose_groups=[],incomplete_route_source_prose_count=0,
        next_focus='Continue untouched source/story exchanges beyond Seville and shared shop/town/random/player prose;marketCOMMON750-752callers andraw rejected-object classification remain open.')
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=677,completed_route_records=677,source_prose_pending_records=0,source_prose_pending_family=None,next=inventory['next_focus'])
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v2728']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=0,full_goal_complete=False)
    ledger['lil_Seville_completion_v2728']=dict(summary=SUMMARY,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    keys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert keys==oldkeys|selected=={(r['file_path'],r['id']) for r in fresh['integrated_record_keys']}=={(r['file_path'],r['id']) for r in fresh['record_keys']}
    assert len(keys)==len(fresh['integrated_record_keys'])==2276
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==2279
    for key in ['reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','source_prose_reviewed_counts_by_file']:
        assert ledger[key]==before[key],key
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    section='## V2728: Lil Seville20 completed in registered cumulative V2724\n\n'+SUMMARY+'\n\nFinal review: '+FINAL.as_posix()+'. Release/patch: '+RELEASE.as_posix()+'. Current startup: '+START.as_posix()+'. Unfinished scope: '+inv.as_posix()+'. Current COMMON parser remains dk4tool.patch.surrender_advice_contextual_v1.current_entries;bounded context remains scripts/current_common_native_context_v2677.py because ARM9/COMMON are byte-identical.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        p.write_text(('# Current editorial handoff - V2728' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    save(ROOT/'completion_receipt.json',dict(checkpoint='V2728',summary=SUMMARY,evidence={**evidence,str(FINAL):sha(FINAL.read_bytes()),str(inv):sha(inv.read_bytes())},
        updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},new_completed_records=20,new_source_prose_reviews=0,revisions=17,justified_retentions=3,
        fresh_reread=2276,fresh_integrated=2276,fresh_pending=0,source_prose=2279,completed=2276,historical_revised=1592,historical_retained=684,incomplete_COMMON=3,incomplete_route=0,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        actual_Seville_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=1,goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V2728:20completed in registeredV2724;17revisions/3retentions;2276reread/integrated,source/prose2279. COMMON3andall wider prose still open;full goal active.')
