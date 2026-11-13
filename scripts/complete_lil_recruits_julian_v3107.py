"""Reconcile199 only after registered build,patch and actual current startup."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from collections import Counter
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Recruits_Julian_completion_v3107')
DOC=Path('translations/lil_recruits_julian_editorial_manuscript_v5.json')
FINAL=Path('translations/lil_recruits_julian_contextual_final_review_v1.json')
CHOICE=Path('translations/lil_recruits_julian_choice_manuscript_v4.json')
RELEASE=Path('work/analysis/lil_Recruits_Julian_release_v3104/registered_release_verification.json')
START=Path('work/analysis/lil_Recruits_Julian_startup_v3106/cold_boot_Lil_startup_town_verification.json')
FAMILY='Lil-Recruits-Julian-199-contextual-completed'
SUMMARY='V3107 completes199 fresh contextual reviews in registered cumulative experimental V3103:158revisions/41individually justified retentions across five complete LilSC2B75-B79 exchanges. All197speeches(196ordinary/one unlabeledFE) andtwo typed choices have exactclean/current/integrated references,fresh glosses,whole-exchange context,localization notes andallfive review gates. Janus Pasar retains practical inexperience,1000gold advance,one-day wait,repairs/debts andtest-of-character/excitement self-correction;the guide correctly uses Dock/Remodel. Lil is admiral. Shipwright109 metadata is reconciled without source-byte changes. Charles retains Academy letter,conditional experiment,bomb-to-science correction,slaps/countdown,three-years-on-display andmisread threat. Yukihisa retains source hostile extortion context,back-of-blade/no cuts,optional eating companions andpersonal moral/world resolve. Julian retains Silla Gold Crown,Hangzhou tavern,Mihwa,Luo Yuli,grandparents/delicate-air unknown girl/black-haired parents andscholar-or-official wishes,without inventedrelationships/ranks/illness/amnesia. All372commands/197preambles/68relative sites/340relocatedcases/16predicates/noqueries/one menu andinverse restoration pass;680clean-current branchcases/394historical dispatchcases remain bound. Bothimages pass336wholeloaders/cachehits and672parentmodes;threeentrycensuses pass. OnlySC2B75-B79 change;331otherblocks/everyotherfile/component/ARM9/COMMON/graphics/fonts/cache/BSS/123040stagedbytes exact. All197nativeplanes/1576logical-compiledmacro cases/788finalparitycases preserve everyglyph,blankpaper,origins,bounds,fourrows/singlepage. FE uses source-unlabeled nullactor24310 andcalibrated228x48logical/228x64physical paper;variadic5473Cr1isnotgeometry. Two speech refinements resolved pair-phase/five-row findings. A19cell114pxmenu exposed11missing leading-Ypixels;faithful20cell You must be kidding! passes120pxgeometry,eightcurrent-reviewedstyleplanes,three decoderobjects andsixoriginalVMselection/cancelcases. No manualpadding/runtimechange orolderaudit. Failed3090/3090bproducers,all drafts/proofs/ROMs preserved. All27sheets viewed;31source/consumer,28formatter and28compilerrejections pass;only74rowcount notes,no orphan/weak-ending/control/glyph/bounds/paginationwaivers. Sharedactual progressive/FE/menu rules inherit byexactruntime/COMMON/EV2/font/B74bytes. OfflineCPU/font work isdistinct fromactualgameplay. FullV3066successorV3103 has510manifestbatches/114acceptedlayers;clean-inputpatch reconstructs entireROMbyteforbyte. Two fresh targetedheadlesscoldboots complete4001LilNewGame/17401town-Refitframes;31wholeframebuffers matchV3066,fiveactor/captain controls/donorhashes pass,andthe currentsix-frame sheet wasviewed. Inheritedfive-shipCopenhagenbattery/threeaccessfixtures remainunearned. No selectedrecruitment/earnedpayment/shipdelivery/itemtransfer/newnameplate/fullroute/hardwareclaim. Freshcoverage3990reread/3990integrated/zeropending;completion3990=2800historicallyrevised+1190retained. Source/prose3993includes2163SC2;all2391reviewedrouteobjects integrated. COMMON750-752callers,allwideruntouchedstorylines/sharedshop-town/random/help/playerprose,SourceItems/LocalProduct,fivenamedtargetleads,rawrejectedclassificationincludingB141,SC3B109,separategraphics/all18plaques andlaterolder-recordtechnicalreaudit remainopen. Queued0Dvalidationgap staysforlater withoutassertinganolderruntimedefect. B66/B121 andallpreviouscompletedfamilies remaincompleted. PreserveeveryROM,translation,executedproducer/proof/failure,clean/canonicalinput. V1492remainspromoted. Fullgoalactive;alljobsterminal.'

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    prior=Path('work/analysis/editorial_handoff_verification_v3095/verified_handoff.json')
    assert sha(lp.read_bytes())==read(prior)['ledger_sha256']
    release,start=read(RELEASE),read(START)
    assert release['whole_ROM_reconstruction_byte_exact'] and release['all510_manifest_batches_and114_accepted_layers_present']
    assert start['all_current_requested_and_final_framebuffers_equal_V3066'] and start['all_five_postload_actor_model_and_captain_checks_equal']
    assert start['current_Lil_captain2_and_B22_payload_verified'] and start['source_and_disposable_town_donor_unchanged']
    assert start['actual_selected_Recruits_Julian_IDs']==[] and sha(Path(start['review_sheet']).read_bytes())==start['review_sheet_sha256']
    # The six current frames were viewed before executing this producer.
    doc=read(DOC);mapping=read(doc['reference_map']);rows=deepcopy(doc['records']+read(CHOICE)['records'])
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':158,'retain-wording':41}
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
            integrated_hex=value.hex(),completed_candidate_reference=release['candidate'],registered_prose_owner='lil_recruits_julian_editorial',
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
    assert len(selected)==199 and {(r['file_path'],r['id']) for r in fresh['pending_record_keys']}==selected
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(3990,3791,199)
    oldkeys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']};assert not oldkeys&selected
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V3094')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    review=ROOT/'current_six_frame_visual_review.json';save(review,dict(sheet=start['review_sheet'],sha256=start['review_sheet_sha256'],viewed=True,
        findings='Lil selection and opening dialogue and inherited town/Refit component screens are legible and match V3066. Current startup only; no selected recruitment/Julian activation.'))
    proofpaths=[DOC,CHOICE,Path(doc['reference_map']),Path(doc['native_font_proof']),Path(doc['representative_proof']),Path(doc['historical_representative_sheet_review']),Path(doc['prior_current_sheet_review']),RELEASE,START,prior,review,Path(__file__),
        Path('work/analysis/lil_Recruits_Julian_registration_v3102/registration_receipt.json'),Path('work/analysis/lil_Recruits_Julian_registration_v3102/negative_cases.json'),
        Path('work/analysis/lil_Recruits_Julian_research_v3097/research_image_receipt.json'),
        Path('work/analysis/lil_Recruits_Julian_reference_census_v3099/all372_commands68_relative_sites_and_shipped_entry_census.json'),
        Path('work/analysis/lil_Recruits_Julian_loader_v3098/whole_SC2_and_five_selected_blocks_initial_entry_proof.json')]
    evidence={str(p):sha(p.read_bytes()) for p in proofpaths}
    save(FINAL,dict(format='dk4-natural-dialogue-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        id=FAMILY,manuscript=str(DOC),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        revised=158,retained=41,records=rows,summary=SUMMARY,evidence=evidence,actual_selected_Recruits_Julian_IDs=[],
        new_current_candidate_emulator_runs=2,new_independent_control_runs=0,current_six_frame_sheet_viewed=True,full_goal_complete=False))
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[75,76,77,78,79],record_IDs=[r['id'] for r in rows],
        final_review=str(FINAL),revised_count=158,retained_count=41,fresh_revisions=158,fresh_retentions=41,
        actual_verification_scope='Historical progressive,FEandmenu sharedrules plus two current cold-start/story/town samples;197panels/one typedmenu and16relocatedpredicates separately native-tested. No selected recruitment/Julian activation.',records=rows))
    ledger.update(records_editorially_completed=3990,records_revised_and_integrated=2800,retained_wordings_editorially_completed=1190)
    ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4']=2163
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=[]
    active=ledger['active_source_prose_drafts']
    for p,ids in active['route_record_subsets_pending'].items():
        active['route_record_subsets_pending'][p]=[ident for ident in ids if ('/data/SC2.DK4',ident) not in selected]
    for p in [DOC,CHOICE]:
        if str(p) not in active['manuscripts']:active['manuscripts'].append(str(p))
        active['route_record_subsets_pending'][str(p)]=[]
    active.update(status='3-reviewed-COMMON-incomplete;no-pending-route-drafts;historical-manuscripts-preserved',
        note='3990 fresh rereads integrated/reconciled;source/prose3993. MarketCOMMON750-752caller context unresolved;all wider untouched prose remains in scope.')
    fresh['integrated_record_keys'].extend(fresh['pending_record_keys'])
    fresh.update(fresh_pass_records_integrated=3990,fresh_pass_records_pending_native_actual_release=0,pending_record_keys=[],pending_contextual_families=[],
        latest_pending_contextual_family=None,latest_contextual_manuscript=str(DOC),latest_contextual_choice_draft=str(CHOICE),
        latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=active['note'])
    fresh['reconciled_families'].append(dict(id=FAMILY,records=199,final_review=str(FINAL),new_revisions=158,justified_retentions=41,new_completed_records=199,
        historical_reconciliation_only=False,historical_decisions_newly_completed=dict(revised=158,retained=41),actual_selected_Recruits_Julian_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0))
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=2391,completed_route_records=2391,next='Continue untouched route/shared/town/random/player prose. All-route review remains open.')
        if unit['id']=='Lil-Recruits-Julian-199':unit.update(status='complete-contextual-current-native-references-representative-and-registered-release',pending=None,completion_credit_added=199,final_review=str(FINAL),full_goal_complete=False)
    watch=ledger['formatting_watchlist']['lil_Recruits_Julian_v3094']
    watch.update(status='complete-through-V3107',reference_map_pending=False,
        representative_reconciliation_pending=False,superseded_by='lil_Recruits_Julian_v3107',final_review=str(FINAL))
    ledger['formatting_watchlist']['lil_Recruits_Julian_v3107']=dict(status='all199-source-native-reference-representative-release-checks-pass',final_review=str(FINAL),evidence=evidence,
        actual_selected_Recruits_Julian_IDs=[],individual_conditional_visits_not_required_under_user_policy=True,no_orphan_predicate_or_missing_glyph_waivers=True)
    oldcandidate=deepcopy(ledger['current_integrated_candidate']);ledger['previous_current_integrated_candidate_before_V3103']=oldcandidate
    ledger['integrated_candidate_reference_history'].append(oldcandidate)
    candidate=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=SUMMARY,full_goal_complete=False,
        **{key+'_sha256':digest for key,digest in release['story_hashes'].items()})
    ledger['current_integrated_candidate']=candidate;ledger['latest_registered_editorial_candidate']=deepcopy(candidate)
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v3094']['path']))
    inventory['lil_B75_B79_fresh_context_review_checkpoint'].update(checkpoint='V3107',status='complete-contextual-current-native-references-representative-and-registered-release')
    inventory['next_clean_only_uncredited_recruits_Julian_scope_v3077']['reconciled_by']='V3107;all197speeches andtwo typedlabels reviewed andintegrated;historical source-only lead preserved'
    inventory['next_clean_only_uncredited_exchange_inventory_v2964']['reconciled_subsets'].append(dict(blocks=[75,76,77,78,79],speeches=197,typed_choice_labels=2,final_review=str(FINAL),checkpoint='V3107'))
    inventory['next_clean_only_uncredited_exchange_inventory_v2964']['all657_source_speeches_and2_typedlabels_reviewed_and_integrated']=True
    inventory['next_clean_only_uncredited_exchange_inventory_v2964']['nontext_B80_editorial_credit']=0
    inventory.update(incomplete_route_source_prose_groups=[],incomplete_route_source_prose_count=0,
        next_focus='Continue every untouched storyline/shared shop-town/random/player prose family. BothB66/B121 now reviewed;COMMON750-752callers,SourceItems/LocalProduct,five named-target leads,raw rejected-object classification includingB141,SC3B109,separategraphics andlaterolder-record technical re-audit remainopen.')
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=2391,completed_route_records=2391,source_prose_pending_records=0,source_prose_pending_family=None,next=inventory['next_focus'])
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v3107']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=0,full_goal_complete=False)
    ledger['lil_Recruits_Julian_completion_v3107']=dict(summary=SUMMARY,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    keys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert keys==oldkeys|selected=={(r['file_path'],r['id']) for r in fresh['integrated_record_keys']}=={(r['file_path'],r['id']) for r in fresh['record_keys']}
    assert len(keys)==len(fresh['integrated_record_keys'])==3990
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==3993
    for key in ['reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','source_prose_reviewed_counts_by_file']:
        assert ledger[key]==before[key],key
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    release_note=('Release details: experimental profile `'+release['profile']+'`. Candidate `'+release['candidate']+'`, SHA-256 `'+release['candidate_sha256']+'`. '
        'Canonical base `'+release['canonical_base']+'`, SHA-256 `'+release['canonical_base_sha256']+'`. '
        'Clean-input patch `'+release['patch']+'`, SHA-256 `'+release['patch_sha256']+'`. '
        'The manifest enumerates all510 batches and114 accepted layers, including the full V3066 stack and the new197-panel manuscript andtwo-label typed-choice manuscript. '
        'Internal delta from V3066: `/data/SC2.DK4` blocks75/76/77/78/79 only; every other file and component is exact. '
        'Verifiers: source/relocation/reference/native-font/padding checks,28 compiler rejections, `verify_lil_recruits_julian_release_v3104.py` and `verify_lil_recruits_julian_startup_v3106.py`. '
        'Current cold-boot areas are title/character selection,Lil opening,andtown/Refit. Human cold-boot acceptance is still required for promotion; V1492 remains promoted.\n\n')
    section='## V3107:199 recruitment/Julian entries completed in V3103\n\n'+SUMMARY+'\n\n'+release_note+'Final review: '+FINAL.as_posix()+'. Release/patch: '+RELEASE.as_posix()+'. Current startup: '+START.as_posix()+'. Unfinished scope: '+inv.as_posix()+'. Current COMMON parser remains dk4tool.patch.surrender_advice_contextual_v1.current_entries;bounded context remains scripts/current_common_native_context_v2677.py because ARM9/COMMON are byte-identical.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        p.write_text(('# Current editorial handoff - V3107' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    save(ROOT/'completion_receipt.json',dict(checkpoint='V3107',summary=SUMMARY,evidence={**evidence,str(FINAL):sha(FINAL.read_bytes()),str(inv):sha(inv.read_bytes())},
        updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},new_completed_records=199,new_source_prose_reviews=0,revisions=158,justified_retentions=41,
        fresh_reread=3990,fresh_integrated=3990,fresh_pending=0,source_prose=3993,completed=3990,historical_revised=2800,historical_retained=1190,incomplete_COMMON=3,incomplete_route=0,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        actual_selected_Recruits_Julian_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0,goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V3107:199completed in registeredV3103;158revisions/41retentions;3990reread/integrated,source-prose3993. COMMON3andall widerprose remainopen;full goalactive.')
