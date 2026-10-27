"""Reconcile360 only after registered build,patch and actual current startup."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from collections import Counter
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Kuhn_Resolution_completion_v2962')
DOC=Path('translations/lil_kuhn_resolution_editorial_manuscript_v7.json')
FINAL=Path('translations/lil_kuhn_resolution_contextual_final_review_v1.json')
CHOICE=Path('translations/lil_kuhn_resolution_choice_manuscript_v3.json')
RELEASE=Path('work/analysis/lil_Kuhn_Resolution_release_v2959/registered_release_verification.json')
START=Path('work/analysis/lil_Kuhn_Resolution_startup_v2961/cold_boot_Lil_startup_town_verification.json')
FAMILY='Lil-Kuhn-Resolution-New-World-Clifford-Camille-360-contextual-completed'
SUMMARY='V2962 completes 360 fresh contextual reviews in registered cumulative experimental V2958: 214 revisions and 146 individually justified retentions across Lil SC2 B57/B58/B59/B60/B61/B62/B63/B64/B65/B66/B121. Every object has exact clean/current/integrated references, a fresh gloss, complete-exchange context, localization notes and all five review gates. The 358 speeches comprise 342 ordinary and 16 FE panels; two typed choices preserve fight versus the better course of retreat. Preserve Li and Spanish-officer aftermath qualifications, Clifford letter and faux-courteous hostage betrayal, Crown mission, companion alternatives, conditional map/Proof thefts, relic uncertainty and New World experiment. Registered item pointers reconcile names including Ullr, Aksum, Rigveda, Ceremonial Knife and Sun-Crest Sheath without UI/catalog/font changes. Keep the complete letter salutation/signature and unlabeled offscreen FI call before Camille reveal. Native actors28 James Clifford,43 Diogo Escante and11 Jam Jack Ludwyan are sourcebound; no newly visited nameplate is claimed. The three Kuhn/Camille outcomes remain distinct. B64 requires121 and temporarily entrusts two objects including the later identified locket. B65 excludes48, has one unnamed youthful object and explicitly mentions many years. B66 requires48/excludes121 and preserves four known/unknown bartender branches. B121 requires54 and preserves five ships, disguised fleets and a fabricated death/vengeance pretext, fear and rescue, Hodram/Maria arrival alternatives, birth-name/nickname explanations and the fuller family backstory. Overijssel is maternal surname, Marinus Kuhn birthname, Camille nickname. Translate his feminine-name recollection respectfully without invented bullying, identity explanations or fatherly gender-disapproval motive. Preserve personal apologies, Mother/Mom register, greed and Spice Islands history, private relief, reunion work banter and Hodram/Maria deadpan joke without invented romance or ranks. Camille thanks Maria for telling ME of the attack. Maria literal deciphering key remains distinct from her metaphorical hope for Asian independence; Lil promises effort rather than guaranteed salvation. All 936 commands,358 complete speech preambles,340 relative sites/1700 relocated branch cases,84 relocated predicates,nine event queries and inverse restoration pass. Source clean/current3400branch cases and716historical dispatcher contexts remain bound. Getter arguments0/1/2 and mapped incidental r3 source cursor are exact; original four-byte alignment scratch restores all4MiB. Each image passes336whole loads/cache hits and672parent modes; three shipped-entry censuses preserve original interpreter calls. Only11selected SC2blocks change;325otherblocks,everyotherfile/component,ARM9/COMMON,graphics/fonts,cache/BSS and123040stagedbytes remainexact. Complete358 native panels/2864logical-compiled macro cases plus1432final padded alignments preserve leading/interior/final glyphs,blank paper,bounds,four rows,return andsingle-page consumption. FEuses null-actor24310 and calibrated mode1typed228x48logical/228x64physical paper; variadic5473Centryr1is not layoutmode. TwoFIcases independently becomeLil. One two-choice menu preserves order,pointers,count and0/1/cancel in six original VMcases andeight current/reviewed styleplanes; its inputloop is bridged. All46final sheets were viewed orhashmatch viewed predecessors. Local formatter successors resolve concrete weak-word andphrase boundaries without changing reviewed wording. Only104individual row-count notes remain;no weak-ending,orphan,control,overflow,glyph orblank-page waiver. Twenty-eight formatter,11source/consumer and28compiler negatives pass. All drafts,failed producers andproofs remain preserved; global helpers unchanged. Historical progressive ink/gray/blank,B74return,FEandmenu actual rules inherit byexact runtime/COMMON/EV2/font/B74bytes. Offline CPU/font evidence stays distinct fromactual gameplay;individual conditional/speaker/nameplate visits are unnecessary absent a concrete unresolved distinct risk. One guarded optionalstage extends fullV2916. V2958 has505manifest batches/114acceptedlayers;the clean-input xdelta reconstructs the entire ROM byteforbyte. Two fresh targeted headless coldboots complete4001LilNewGame and17401town/Refitframes;all31whole framebuffers matchV2916,five actor/captain controls anddonor hashes pass,andthe current six-frame sheet was viewed. The inherited five-ship Copenhagen battery andthree access fixtures remain unearned/disclosed. No selected Kuhn-resolution activation,earnedtravel/funding/pact/battle,newfixture,newnameplate,full-route orhardware claim. Fresh coverage is3331 reread /3331 integrated-reconciled /zero pending. Completion3331 comprises2304historically revised and1027retained;source/prose3334 includes1504SC2. Completed filecounts1599COMMON/1504SC2/117SC0/73SC1/38SC3;all1732reviewed route objects are integrated. BothB66/B121 now have fresh contextual review. COMMON750-752callers,every wider untouched storyline/shared shop-town/random/player prose family,uncredited SourceItems/LocalProduct andfive named-target leads,raw rejected-object classification includingB141,SC3B109,separate graphics/all18plaques andlater older-record technical re-audit remain open. Preserve every ROM,earlier translation,source/profile/proof andclean/canonical input. V1492 remains promoted. Full goal active;all jobs terminal.'

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    prior=Path('work/analysis/editorial_handoff_verification_v2950/verified_handoff.json')
    assert sha(lp.read_bytes())==read(prior)['ledger_sha256']
    release,start=read(RELEASE),read(START)
    assert release['whole_ROM_reconstruction_byte_exact'] and release['all505_manifest_batches_and114_accepted_layers_present']
    assert start['all_current_requested_and_final_framebuffers_equal_V2916'] and start['all_five_postload_actor_model_and_captain_checks_equal']
    assert start['current_Lil_captain2_and_B22_payload_verified'] and start['source_and_disposable_town_donor_unchanged']
    assert start['actual_selected_Kuhn_Resolution_IDs']==[] and sha(Path(start['review_sheet']).read_bytes())==start['review_sheet_sha256']
    # The six current frames were viewed before executing this producer.
    doc=read(DOC);mapping=read(doc['reference_map']);rows=deepcopy(doc['records']+read(CHOICE)['records'])
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':214,'retain-wording':146}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['localization_note'] for r in rows)
    image=NdsImage.open(release['candidate']);blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==start['candidate_sha256']
    refs={r['id']:r for b in mapping['blocks'] for r in b['text_records']}
    for row in rows:
        block=blocks[row['block']]
        if row['kind']=='typed-choice-label':
            owned=next(c for c in release['stage']['changed_records'] if c['id']==row['id']);offset=owned['new_offset'];value=row['english'].encode('ascii')
            menu_ref=next(c for b in mapping['blocks'] if b['block']==row['block'] for c in b['choice_commands'] if c['old_offset']==row['command_offset'])
            assert block[offset:offset+len(value)]==value and block[offset+len(value)]==0
        else:
            spec=refs[row['id']];offset=spec['new_offset'];value=bytes.fromhex(spec['target_hex'])
            assert block[offset:offset+len(value)]==value and block[offset-5:offset]==bytes.fromhex('0040ffff00')
        row['historical_source_prose_predecessor_fields']={k:deepcopy(row[k]) for k in ['current_reference','current_hex','current_English','current_record_index','record_index'] if k in row}
        reference=dict(block=row['block'],offset=offset,bytes=len(value),record_index=block[:offset].count(b'\0'))
        if row['kind']=='typed-choice-label':reference.update(command_offset=menu_ref['new_offset'],option_index=row['option_index'])
        else:reference['header_offset']=offset-5
        row.update(current_reference=reference,current_hex=value.hex(),current_text_hex=value.hex(),integrated_reference=reference,
            integrated_hex=value.hex(),completed_candidate_reference=release['candidate'],registered_prose_owner='lil_kuhn_resolution_editorial',
            registered_manuscript=str(CHOICE if row['kind']=='typed-choice-label' else DOC),
            historical_editorial_decision='revise' if row['editorial_decision']=='revise' else 'retain',
            decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-and-editorially-reviewed',
            individual_actual_activation_not_claimed=True,all_source_native_representative_and_registered_gates_pass=True,
            status='complete-contextual-current-native-references-representative-and-registered-release')
        row['current_English']=(value if row['kind']=='typed-choice-label' else value[1:]).decode('ascii')
        if row['editorial_decision']=='retain-wording':row.setdefault('fresh_retained_wording_justification',row['localization_note'])
        if row['kind']!='typed-choice-label':
            row['current_record_index']=row['record_index']=reference['record_index']
    selected={(r['file_path'],r['id']) for r in rows};fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert len(selected)==360 and {(r['file_path'],r['id']) for r in fresh['pending_record_keys']}==selected
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(3331,2971,360)
    oldkeys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']};assert not oldkeys&selected
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V2949')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    review=ROOT/'current_six_frame_visual_review.json';save(review,dict(sheet=start['review_sheet'],sha256=start['review_sheet_sha256'],viewed=True,
        findings='Lil selection and opening dialogue and inherited town/Refit component screens are legible and match V2916. Current startup only; no selected Kuhn-resolution activation.'))
    proofpaths=[DOC,CHOICE,Path(doc['reference_map']),Path(doc['native_font_proof']),Path(doc['representative_proof']),Path(doc['historical_representative_sheet_review']),Path(doc['prior_current_sheet_review']),RELEASE,START,prior,review,Path(__file__),
        Path('work/analysis/lil_Kuhn_Resolution_registration_v2957/registration_receipt.json'),Path('work/analysis/lil_Kuhn_Resolution_registration_v2957/negative_cases.json'),
        Path('work/analysis/lil_Kuhn_Resolution_research_v2952/research_image_receipt.json'),
        Path('work/analysis/lil_Kuhn_Resolution_reference_census_v2954/all936_commands340_relative_sites_and_shipped_entry_census.json'),
        Path('work/analysis/lil_Kuhn_Resolution_loader_v2953/whole_SC2_and_eleven_selected_blocks_initial_entry_proof.json')]
    evidence={str(p):sha(p.read_bytes()) for p in proofpaths}
    save(FINAL,dict(format='dk4-natural-dialogue-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        id=FAMILY,manuscript=str(DOC),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        revised=214,retained=146,records=rows,summary=SUMMARY,evidence=evidence,actual_selected_Kuhn_Resolution_IDs=[],
        new_current_candidate_emulator_runs=2,new_independent_control_runs=0,current_six_frame_sheet_viewed=True,full_goal_complete=False))
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[57,58,59,60,61,62,63,64,65,66,121],record_IDs=[r['id'] for r in rows],
        final_review=str(FINAL),revised_count=214,retained_count=146,fresh_revisions=214,fresh_retentions=146,
        actual_verification_scope='Historical progressive,FEandmenu sharedrules plus two current cold-start/story/town samples;358panels/one typedmenu and84relocatedpredicates separately native-tested. No selected Kuhn-resolution activation.',records=rows))
    ledger.update(records_editorially_completed=3331,records_revised_and_integrated=2304,retained_wordings_editorially_completed=1027)
    ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4']=1504
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=[]
    active=ledger['active_source_prose_drafts']
    for p,ids in active['route_record_subsets_pending'].items():
        active['route_record_subsets_pending'][p]=[ident for ident in ids if ('/data/SC2.DK4',ident) not in selected]
    for p in [DOC,CHOICE]:
        if str(p) not in active['manuscripts']:active['manuscripts'].append(str(p))
        active['route_record_subsets_pending'][str(p)]=[]
    active.update(status='3-reviewed-COMMON-incomplete;no-pending-route-drafts;historical-manuscripts-preserved',
        note='3331 fresh rereads integrated/reconciled;source/prose3334. MarketCOMMON750-752caller context unresolved;all wider untouched prose remains in scope.')
    fresh['integrated_record_keys'].extend(fresh['pending_record_keys'])
    fresh.update(fresh_pass_records_integrated=3331,fresh_pass_records_pending_native_actual_release=0,pending_record_keys=[],pending_contextual_families=[],
        latest_pending_contextual_family=None,latest_contextual_manuscript=str(DOC),latest_contextual_choice_draft=str(CHOICE),
        latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=active['note'])
    fresh['reconciled_families'].append(dict(id=FAMILY,records=360,final_review=str(FINAL),new_revisions=214,justified_retentions=146,new_completed_records=360,
        historical_reconciliation_only=False,historical_decisions_newly_completed=dict(revised=214,retained=146),actual_selected_Kuhn_Resolution_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0))
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=1732,completed_route_records=1732,next='Continue untouched route/shared/town/random/player prose. All-route review remains open.')
        if unit['id']=='Lil-Kuhn-Resolution-New-World-Clifford-Camille-360':unit.update(status='complete-contextual-current-native-references-representative-and-registered-release',pending=None,completion_credit_added=360,final_review=str(FINAL),full_goal_complete=False)
    watch=ledger['formatting_watchlist']['lil_Kuhn_Resolution_v2949']
    watch.update(status='complete-through-V2962',reference_map_pending=False,
        representative_reconciliation_pending=False,superseded_by='lil_Kuhn_Resolution_v2962',final_review=str(FINAL))
    ledger['formatting_watchlist']['lil_Kuhn_Resolution_v2962']=dict(status='all360-source-native-reference-representative-release-checks-pass',final_review=str(FINAL),evidence=evidence,
        actual_selected_Kuhn_Resolution_IDs=[],individual_conditional_visits_not_required_under_user_policy=True,no_orphan_predicate_or_missing_glyph_waivers=True)
    oldcandidate=deepcopy(ledger['current_integrated_candidate']);ledger['previous_current_integrated_candidate_before_V2958']=oldcandidate
    ledger['integrated_candidate_reference_history'].append(oldcandidate)
    candidate=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=SUMMARY,full_goal_complete=False,
        **{key+'_sha256':digest for key,digest in release['story_hashes'].items()})
    ledger['current_integrated_candidate']=candidate;ledger['latest_registered_editorial_candidate']=deepcopy(candidate)
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v2949']['path']))
    inventory['lil_B66_B121_fresh_context_review_checkpoint'].update(checkpoint='V2962',status='complete-contextual-current-native-references-representative-and-registered-release')
    inventory['next_clean_only_uncredited_exchange_inventory']['reconciled_by']='V2962;the earlier clean-only358-speech lead now reviewed/integrated withtwo typed choices;historical inventory preserved'
    inventory.update(incomplete_route_source_prose_groups=[],incomplete_route_source_prose_count=0,
        next_focus='Continue every untouched storyline/shared shop-town/random/player prose family. BothB66/B121 now reviewed;COMMON750-752callers,SourceItems/LocalProduct,five named-target leads,raw rejected-object classification includingB141,SC3B109,separategraphics andlaterolder-record technical re-audit remainopen.')
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=1732,completed_route_records=1732,source_prose_pending_records=0,source_prose_pending_family=None,next=inventory['next_focus'])
    next_clean=Path('work/analysis/lil_after_Kuhn_Resolution_clean_scope_v2964/clean_next_exchange_inventory.json');scope=read(next_clean)
    assert scope['editorial_credit_added']==0 and not scope['unclassified']
    inventory['next_clean_only_uncredited_exchange_inventory_v2964']=dict(path=str(next_clean),sha256=sha(next_clean.read_bytes()),blocks=[b['block'] for b in scope['blocks']],speeches=sum(b['speeches'] for b in scope['blocks']),typed_menu_objects=sum(b['choice_commands'] for b in scope['blocks']),source_prose_or_completion_credit_added=0,status='clean-only scope leads;check exact coverage keys and complete-exchange context before choosing next batch')
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v2962']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=0,full_goal_complete=False)
    ledger['lil_Kuhn_Resolution_completion_v2962']=dict(summary=SUMMARY,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    keys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert keys==oldkeys|selected=={(r['file_path'],r['id']) for r in fresh['integrated_record_keys']}=={(r['file_path'],r['id']) for r in fresh['record_keys']}
    assert len(keys)==len(fresh['integrated_record_keys'])==3331
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==3334
    for key in ['reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','source_prose_reviewed_counts_by_file']:
        assert ledger[key]==before[key],key
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    release_note=('Release details: experimental profile `'+release['profile']+'`. Candidate `'+release['candidate']+'`, SHA-256 `'+release['candidate_sha256']+'`. '
        'Canonical base `'+release['canonical_base']+'`, SHA-256 `'+release['canonical_base_sha256']+'`. '
        'Clean-input patch `'+release['patch']+'`, SHA-256 `'+release['patch_sha256']+'`. '
        'The manifest enumerates all505 batches and114 accepted layers, including the full V2916 stack and the new358-panel manuscript andtwo-label typed-choice manuscript. '
        'Internal delta from V2916: `/data/SC2.DK4` blocks57/58/59/60/61/62/63/64/65/66/121 only; every other file and component is exact. '
        'Verifiers: source/relocation/reference/native-font/padding checks,28 compiler rejections, `verify_lil_kuhn_resolution_release_v2959.py` and `verify_lil_kuhn_resolution_startup_v2961.py`. '
        'Current cold-boot areas are title/character selection,Lil opening,andtown/Refit. Human cold-boot acceptance is still required for promotion; V1492 remains promoted.\n\n')
    section='## V2962:360 Kuhn-resolution entries completed in V2958\n\n'+SUMMARY+'\n\n'+release_note+'Final review: '+FINAL.as_posix()+'. Release/patch: '+RELEASE.as_posix()+'. Current startup: '+START.as_posix()+'. Unfinished scope: '+inv.as_posix()+'. Current COMMON parser remains dk4tool.patch.surrender_advice_contextual_v1.current_entries;bounded context remains scripts/current_common_native_context_v2677.py because ARM9/COMMON are byte-identical.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        p.write_text(('# Current editorial handoff - V2962' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    save(ROOT/'completion_receipt.json',dict(checkpoint='V2962',summary=SUMMARY,evidence={**evidence,str(FINAL):sha(FINAL.read_bytes()),str(inv):sha(inv.read_bytes())},
        updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},new_completed_records=360,new_source_prose_reviews=0,revisions=214,justified_retentions=146,
        fresh_reread=3331,fresh_integrated=3331,fresh_pending=0,source_prose=3334,completed=3331,historical_revised=2304,historical_retained=1027,incomplete_COMMON=3,incomplete_route=0,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        actual_selected_Kuhn_Resolution_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0,goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V2962:360completed in registeredV2958;214revisions/146retentions;3331reread/integrated,source-prose3334. COMMON3andall widerprose remainopen;full goalactive.')
