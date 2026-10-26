"""Reconcile145 only after registered build,patch and actual current startup."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from collections import Counter
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Christina_Mivor_completion_v3070')
DOC=Path('translations/lil_christina_mivor_editorial_manuscript_v8.json')
FINAL=Path('translations/lil_christina_mivor_contextual_final_review_v1.json')
RELEASE=Path('work/analysis/lil_Christina_Mivor_release_v3067/registered_release_verification.json')
START=Path('work/analysis/lil_Christina_Mivor_startup_v3069/cold_boot_Lil_startup_town_verification.json')
FAMILY='Lil-Christina-Mivor-145-contextual-completed'
SUMMARY='V3070 completes145 speeches in complete LilSC2B72/B73 Christina recruitment andMivor harbor rescue,with130revisions/15individually justified retentions. All have exact clean/current references,fresh glosses,whole-exchange context,localization notes andallfive gates. Julio is explicitly Christina grandfather inthis source;her unwanted parental engagement andcontinued refusal remain firm. Mivor misplaced confidence andtheatrical formality do not establish mutual consent. The rescue doesnot buy romance. Restore the first fear-greater-than-love comparison beforethe later love-wins reversal;keep repeated fear/name cries,unexpected swimming andhis own disbelief without inventing permanent skill orfear cure. Preserve actual swordchallenge/pain andfather-bought rapier without inventedfatal injury orsnappedblade. Mother167 andBoy162 remain source classes;familiar elder-sister/brother addresses establish norescue kinship. Allthree FEpanels retain explicit source Boy labels. Registered current nativecatalog confirms Mivor Genz;provisional Gentz source-packet annotation is corrected inmanuscript metadata,whileexecuted source proof andJapanese bytes remain preserved. Original fullname getter uses32slots of128bytes;failed3039 readonly assumption and3039b write diagnostic remain. Successor3039c bounds only original counter/output writes andrestores them to recover all4MiB;no runtime defect orolder technical audit isclaimed. Event72dependency123/event73dependency158 are historicalsourceeligibility,not earnedcurrent progress. All236commands/145preambles/12relative sites/120clean-current cases/290historicaldispatch cases/threecurrentpredicates pass;noeventqueries orchoices. Complete142ordinary216x64planes plus3labeledFE228x48logical/228x64physicalplanes and1160logical-compiled macro cases preserve allglyphs,blankpaper,origins,bounds,fourrows andsinglepage. Ninechanged ordinaryplanes/72macro cases were reexecuted;133unchanged/1064cases reuse exactEnglish/source/current/runtime/encodedbytes/previewhashes. FEreuse binds exactEnglish/source/controls/encodedbytes across formatterrefinements. All18finalordinary sheets andoneFE sheet viewed. Twenty-eightformatter and13source-consumer negatives pass. Only51row-count notes;no orphan,weakending,control,glyph,bounds orpagination waiver. Allfailedplans,drafts,producers,proofs andROMs preserved. Fresh coverage is3791 reread /3791 integrated-reconciled /zero pending;source-prose3794 including1964SC2. Completion3791 comprises2642 historically revised and1149retained. All2192reviewedrouteobjects are integrated. Source236commands/12sites/60relocatedcases/3predicates/noqueries andallopaque bytes remain exact byinverse restoration. All145finalparityplanes/580macro cases and336wholeloaders/twoparents/threeentrycensuses pass. Oneguarded optionalstage extends fullV3029;28compilernegatives reject beforemutation. Registration drafts3065/3065b/3065c stopped onsyntax/stale manuscript/formatter bindings beforeanyROM orregistry mutation;3065d binds finalmanuscriptv8/formatterv3 andregisteredcompilerv2,withallfailedproducers preserved. V3066 contains508manifestbatches/114acceptedlayers. OnlySC2B72/B73 differ fromV3029;334otherblocks,everyotherfile/component,ARM9/COMMON,fonts/graphics,cache/BSS and123040stagedbytes stayexact. The clean-input patch reconstructs the fullROM byteforbyte. Two fresh targetedheadless coldboots complete4001LilNewGame and17401town/Refitframes;all31wholeframebuffers matchV3029,five actor/captain controls anddonor hashes pass,andthecurrent six-frame sheet wasviewed. OfflineCPU/font work isdistinct fromactualscene gameplay. Allwider untouchedstorylines/sharedshop-town/random/help/playerprose,COMMON750-752callers,SourceItems/LocalProduct,five namedtargetleads,raw rejected-object classification includingB141,SC3B109,separategraphics/all18plaques andlaterolder-record technicalreaudit remainopen. Queued0Dvalidation-gap lead staysforlaterwithoutassertinganolderruntimedefect. BothB66/B121 andB70/B71 staycompleted. V1492remainspromoted;canonical/cleaninputs preserved. Fullgoalactive;alljobsterminal.'

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    prior=Path('work/analysis/editorial_handoff_verification_v3058/verified_handoff.json')
    assert sha(lp.read_bytes())==read(prior)['ledger_sha256']
    release,start=read(RELEASE),read(START)
    assert release['whole_ROM_reconstruction_byte_exact'] and release['all508_manifest_batches_and114_accepted_layers_present']
    assert start['all_current_requested_and_final_framebuffers_equal_V3029'] and start['all_five_postload_actor_model_and_captain_checks_equal']
    assert start['current_Lil_captain2_and_B22_payload_verified'] and start['source_and_disposable_town_donor_unchanged']
    assert start['actual_selected_Christina_Mivor_IDs']==[] and sha(Path(start['review_sheet']).read_bytes())==start['review_sheet_sha256']
    # The six current frames were viewed before executing this producer.
    doc=read(DOC);mapping=read(doc['reference_map']);rows=deepcopy(doc['records'])
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':130,'retain-wording':15}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['localization_note'] for r in rows)
    image=NdsImage.open(release['candidate']);blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==start['candidate_sha256']
    refs={r['id']:r for b in mapping['blocks'] for r in b['text_records']}
    for row in rows:
        block=blocks[row['block']]
        spec=refs[row['id']];offset=spec['new_offset'];value=bytes.fromhex(spec['target_hex'])
        assert block[offset:offset+len(value)]==value and block[offset-5:offset]==bytes.fromhex('0040ffff00')
        row['historical_source_prose_predecessor_fields']={k:deepcopy(row[k]) for k in ['current_reference','current_hex','current_English','current_record_index','record_index'] if k in row}
        reference=dict(block=row['block'],offset=offset,header_offset=offset-5,bytes=len(value),record_index=block[:offset].count(b'\0'))
        row.update(current_reference=reference,current_hex=value.hex(),current_text_hex=value.hex(),integrated_reference=reference,
            integrated_hex=value.hex(),completed_candidate_reference=release['candidate'],registered_prose_owner='lil_christina_mivor_editorial',
            registered_manuscript=str(DOC),
            historical_editorial_decision='revise' if row['editorial_decision']=='revise' else 'retain',
            decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-and-editorially-reviewed',
            individual_actual_activation_not_claimed=True,all_source_native_representative_and_registered_gates_pass=True,
            status='complete-contextual-current-native-references-representative-and-registered-release')
        row['current_English']=value[1:].decode('ascii')
        if row['editorial_decision']=='retain-wording':row.setdefault('fresh_retained_wording_justification',row['localization_note'])
        if row['kind']!='typed-choice-label':
            row['current_record_index']=row['record_index']=reference['record_index']
    selected={(r['file_path'],r['id']) for r in rows};fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert len(selected)==145 and {(r['file_path'],r['id']) for r in fresh['pending_record_keys']}==selected
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(3791,3646,145)
    oldkeys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']};assert not oldkeys&selected
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V3057')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    review=ROOT/'current_six_frame_visual_review.json';save(review,dict(sheet=start['review_sheet'],sha256=start['review_sheet_sha256'],viewed=True,
        findings='Lil selection and opening dialogue and inherited town/Refit component screens are legible and match V3029. Current startup only; no selectedChristina/Mivor activation.'))
    proofpaths=[DOC,Path(doc['reference_map']),Path(doc['native_font_proof']),Path(doc['native_FE_font_proof']),Path(doc['representative_proof']),Path(doc['historical_representative_sheet_review']),Path(doc['prior_current_sheet_review']),RELEASE,START,prior,review,Path(__file__),
        Path('work/analysis/lil_Christina_Mivor_registration_v3065d/registration_receipt.json'),Path('work/analysis/lil_Christina_Mivor_registration_v3065d/negative_cases.json'),
        Path('work/analysis/lil_Christina_Mivor_research_v3060/research_image_receipt.json'),
        Path('work/analysis/lil_Christina_Mivor_reference_census_v3062/all236_commands12_relative_sites_and_shipped_entry_census.json'),
        Path('work/analysis/lil_Christina_Mivor_loader_v3061/whole_SC2_and_two_selected_blocks_initial_entry_proof.json')]
    evidence={str(p):sha(p.read_bytes()) for p in proofpaths}
    save(FINAL,dict(format='dk4-natural-dialogue-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        id=FAMILY,manuscript=str(DOC),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        revised=130,retained=15,records=rows,summary=SUMMARY,evidence=evidence,actual_selected_Christina_Mivor_IDs=[],
        new_current_candidate_emulator_runs=2,new_independent_control_runs=0,current_six_frame_sheet_viewed=True,full_goal_complete=False))
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[72,73],record_IDs=[r['id'] for r in rows],
        final_review=str(FINAL),revised_count=130,retained_count=15,fresh_revisions=130,fresh_retentions=15,
        actual_verification_scope='Historical progressive/FE rules plus two current cold-start/story/town samples.142ordinary/3source-labeledBoyFE panels bind current native font/paper/parity;strict4F/A2/A7 source controls. Original name-ring writes bounded/restored;no selectedChristina/Mivor activation ornewnameplate claim.',records=rows))
    ledger.update(records_editorially_completed=3791,records_revised_and_integrated=2642,retained_wordings_editorially_completed=1149)
    ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4']=1964
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=[]
    active=ledger['active_source_prose_drafts']
    for p,ids in active['route_record_subsets_pending'].items():
        active['route_record_subsets_pending'][p]=[ident for ident in ids if ('/data/SC2.DK4',ident) not in selected]
    for p in [DOC]:
        if str(p) not in active['manuscripts']:active['manuscripts'].append(str(p))
        active['route_record_subsets_pending'][str(p)]=[]
    active.update(status='3-reviewed-COMMON-incomplete;no-pending-route-drafts;historical-manuscripts-preserved',
        note='3791 fresh rereads integrated/reconciled;source/prose3794. MarketCOMMON750-752caller context unresolved;all wider untouched prose remains in scope.')
    fresh['integrated_record_keys'].extend(fresh['pending_record_keys'])
    fresh.update(fresh_pass_records_integrated=3791,fresh_pass_records_pending_native_actual_release=0,pending_record_keys=[],pending_contextual_families=[],
        latest_pending_contextual_family=None,latest_contextual_manuscript=str(DOC),latest_contextual_choice_draft=None,
        latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=active['note'])
    fresh['reconciled_families'].append(dict(id=FAMILY,records=145,final_review=str(FINAL),new_revisions=130,justified_retentions=15,new_completed_records=145,
        historical_reconciliation_only=False,historical_decisions_newly_completed=dict(revised=130,retained=15),actual_selected_Christina_Mivor_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0))
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=2192,completed_route_records=2192,next='Continue untouched route/shared/town/random/player prose. All-route review remains open.')
        if unit['id']=='Lil-Christina-Mivor-145':unit.update(status='complete-contextual-current-native-references-representative-and-registered-release',pending=None,completion_credit_added=145,final_review=str(FINAL),full_goal_complete=False)
    watch=ledger['formatting_watchlist']['lil_Christina_Mivor_v3057']
    watch.update(status='complete-through-V3070',reference_map_pending=False,
        representative_reconciliation_pending=False,superseded_by='lil_Christina_Mivor_v3070',final_review=str(FINAL))
    ledger['formatting_watchlist']['lil_Christina_Mivor_v3070']=dict(status='all145-source-native-reference-representative-release-checks-pass',final_review=str(FINAL),evidence=evidence,
        actual_selected_Christina_Mivor_IDs=[],individual_conditional_visits_not_required_under_user_policy=True,no_orphan_predicate_or_missing_glyph_waivers=True)
    oldcandidate=deepcopy(ledger['current_integrated_candidate']);ledger['previous_current_integrated_candidate_before_V3066']=oldcandidate
    ledger['integrated_candidate_reference_history'].append(oldcandidate)
    candidate=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=SUMMARY,full_goal_complete=False,
        **{key+'_sha256':digest for key,digest in release['story_hashes'].items()})
    ledger['current_integrated_candidate']=candidate;ledger['latest_registered_editorial_candidate']=deepcopy(candidate)
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v3057']['path']))
    inventory['next_clean_only_uncredited_exchange_inventory_v2964'].setdefault('reconciled_subsets',[]).append(dict(blocks=[72,73],speeches=145,final_review=str(FINAL),checkpoint='V3070'))
    inventory.update(incomplete_route_source_prose_groups=[],incomplete_route_source_prose_count=0,
        next_focus='Continue every untouched storyline/shared shop-town/random/player prose family,includingB75-B80andlaterrecruitment/randomscenes. BothB66/B121remaincompleted. COMMON750-752callers,SourceItems/LocalProduct,fivenamed-target leads,raw rejected-object classification includingB141,SC3B109,separategraphics andlaterolder-recordtechnicalreaudit remainopen.')
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=2192,completed_route_records=2192,source_prose_pending_records=0,source_prose_pending_family=None,next=inventory['next_focus'])
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v3070']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=0,full_goal_complete=False)
    ledger['lil_Christina_Mivor_completion_v3070']=dict(summary=SUMMARY,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    keys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert keys==oldkeys|selected=={(r['file_path'],r['id']) for r in fresh['integrated_record_keys']}=={(r['file_path'],r['id']) for r in fresh['record_keys']}
    assert len(keys)==len(fresh['integrated_record_keys'])==3791
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==3794
    for key in ['reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','source_prose_reviewed_counts_by_file']:
        assert ledger[key]==before[key],key
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    release_note=('Release details: experimental profile `'+release['profile']+'`. Candidate `'+release['candidate']+'`, SHA-256 `'+release['candidate_sha256']+'`. '
        'Canonical base `'+release['canonical_base']+'`, SHA-256 `'+release['canonical_base_sha256']+'`. '
        'Clean-input patch `'+release['patch']+'`, SHA-256 `'+release['patch_sha256']+'`. '
        'The manifest enumerates all508 batches and114 accepted layers, including the full V3029 stack and the new145-speech manuscript. '
        'Internal delta from V3029: `/data/SC2.DK4` blocks72/73 only; every other file and component is exact. '
        'Verifiers: source/relocation/reference/native-font/padding checks,28 compiler rejections, `verify_lil_christina_mivor_release_v3067.py` and `verify_lil_christina_mivor_startup_v3069.py`. '
        'Current cold-boot areas are title/character selection,Lil opening,andtown/Refit. Human cold-boot acceptance is still required for promotion; V1492 remains promoted.\n\n')
    section='## V3070:145 Christina/Mivor reviews completed in V3066\n\n'+SUMMARY+'\n\n'+release_note+'Final review: '+FINAL.as_posix()+'. Release/patch: '+RELEASE.as_posix()+'. Current startup: '+START.as_posix()+'. Unfinished scope: '+inv.as_posix()+'. Current COMMON parser remains dk4tool.patch.surrender_advice_contextual_v1.current_entries;bounded context remains scripts/current_common_native_context_v2677.py because ARM9/COMMON are byte-identical.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        p.write_text(('# Current editorial handoff - V3070' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    save(ROOT/'completion_receipt.json',dict(checkpoint='V3070',summary=SUMMARY,evidence={**evidence,str(FINAL):sha(FINAL.read_bytes()),str(inv):sha(inv.read_bytes())},
        updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},new_completed_records=145,new_source_prose_reviews=0,revisions=130,justified_retentions=15,
        fresh_reread=3791,fresh_integrated=3791,fresh_pending=0,source_prose=3794,completed=3791,historical_revised=2642,historical_retained=1149,incomplete_COMMON=3,incomplete_route=0,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        actual_selected_Christina_Mivor_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0,goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V3070:145completed inregisteredV3066;130revisions/15retentions;3791reread/integrated,source-prose3794. Fullgoalactive.')
