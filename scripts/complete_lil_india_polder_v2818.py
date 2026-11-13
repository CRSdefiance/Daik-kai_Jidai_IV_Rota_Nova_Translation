"""Reconcile34 only after registered build,patch and actual current startup."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from collections import Counter
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_India_Polder_completion_v2818')
DOC=Path('translations/lil_india_polder_editorial_manuscript_v6.json')
FINAL=Path('translations/lil_india_polder_contextual_final_review_v1.json')
RELEASE=Path('work/analysis/lil_India_Polder_release_v2815/registered_release_verification.json')
START=Path('work/analysis/lil_India_Polder_startup_v2817/cold_boot_Lil_startup_town_verification.json')
FAMILY='Lil-India-Camille-Polder-Gift-B37-B38-B39-B40-B129-B130-119-contextual-completed'
SUMMARY=' '.join([
'V2818 completes119 fresh contextual reviews across LilSC2B37/B38/B39/B40/B129/B130 inregistered cumulativeexperimentalV2814:84revisions and35individually justifiedretentions. The complete India poverty/caste,moral-doubt/Camille,polder introduction/follow-up,Lelystad arrival/delivery andCliffordgift exchanges preserve every storedalternative andpunctuation-only speech. All119have freshglosses,context/localizationnotes,exactclean/current/integratedreferences andallfive reviewgates.',
'Preserve thecharacters birth-assignedsocialstanding explanation without inventing castegroups,ranks ormodernhistorical details. Restore Lil personalresponsibility andwish tohelp,the MaritimeSilkRoad reference,profit/competition reasoning,twopeaceproposals,recognition-versus-militaryconquest distinction,andProof ofConquest terminology. TheProofs do notgain inventedagency tojudge worthiness. Camille fatherreferences stayconditional,his aside staysprivate,andLil source scary-dad/sibling analogy doesnotinventactualkinship. ApprovedCamille replacesKamil. ResearchStudent171andBarkeep92remain sourceclasses withoutinventedunique names.',
'The polderstudent describes enclosingcoastalwater withdikes,pumpingitout,a hopeofhelpingthepoor,personalnaming,about1000000currencygold asaninitialestimate,andpreviously soughtbutinsufficientgovernmentaid. Thelaterthreeholds ofcommoditygold andLelystad nearAmsterdam aredistinct. Preserve thelocation/quantity/confirmationsequence,firstperson,modesty,mutualencouragement andfutureoffice/investment/tradingtown expectations;do notinventfundingpayments,who namedLelystad orcompleteddevelopment. Giftletter-reading andalready-heard alternatives do notgrantduplicateobjects;thekey isfordeciphering amap,not anewmapscreen unlock.',
'Complete193nativecommands,119originalpreambles,40relativespans/200relocatedbranchcases,tenrelocatedpredicates andeveryunownedlogicalbyte pass. Sourceclean/current400branchcases and238historicaldispatchercontexts remainbound. Originaleventgetter queries129,48/48,130and26 remainexact;event40requires39 and129mustnotfollowcompleted37. Do notinfer48is thefulltrue-name reveal. Thepreserved2791/2791bdiagnostics identifytheomitted130query;2794bindsallfive queries. Relocatedpredicateoperands/results/eventarguments0/1/2 andmappedcaller-sourcecursor areexact. Onlytheoriginalfour-byteoperandcopy maywrite02279600scratch,andrestoringit recoversall4MiB. Actor/event/roster/RNG/unownedstate remainexact.',
'All336wholeblockloaders/cachehits and672parententrymodes pass foreachparent/researchimage;three shippedentrycensuses preserve theoriginalinterpretercall withoutliteralaliases. All330otherSC2blocks andallotherfiles/components remainexact. Currentnativeproofs bind119completefontplanes,952logical/compiledmacroalignmentcases and476additionalfinalparitycases. Completefirst/interior/finalglyphs,blankpaper,origin0,16pxrows,bounds andfour-row/singlepagecompletion pass. Fourteenformatterrejections and119completeEnglish/control/macroinvariants pass. Only39individualordinaryJapanese/Englishrowcountnotes remain;no weak-ending,orphan,predicate,control,overflow,missingglyph orblankpage waiver isgranted.',
'The2796weakarticlefinding isresolved byonefaithfulparagraph refinement preservingallfacts/qualification. Subsequentlocalformatter refinements preserve everyreviewedword whileavoiding isolatedeverything/struggled,negation andfixedphrasebreaks. All15originalfont sheets,ninechanged2801sheets andthreefinal2803sheets wereviewed;unchangedfinals arehash-identical toviewedpredecessors. Native171is executablepresentationstate,notageneralShiftJisstrippingrule. Everyglobalhelper andnativecodebyte remainsunchanged.',
'Historicalactual progressiveink/gray/blank/B74return andsharedconsumer rules areinherited throughexactARM9/COMMON/EV2/font/B74identity. CurrentCPU/font tests areseparate fromactualgameplay. Theuserrepresentativepolicy doesnotrequireindividualconditional/speaker/nameplatevisits absentaconcreteunresolvedrisk. No selectedIndia/polderactivation,newnameplate,earnedfunding/delivery,full-route orhardwareclaim ismade. Inheritedthreeaccessfixtures andfive-shipCopenhagen townbattery remainunearned anddisclosed.',
'Oneguardedoptionalstage extendsfullV2783;17negativecases rejectbeforemutation. RegisteredV2814contains500batches/114acceptedlayers. OnlySC2B37/B38/B39/B40/B129/B130changesfromV2783;ARM9,COMMON,allotherfiles/components,fonts/graphics,section/BSS/cacheextents and123040stagedbytes remainexact. Theclean-inputxdelta reconstructsthewholeROMbyteforbyte. Everypreviousprofile andV1492promotion ispreserved. Twonewtargetedheadlesscoldboots complete4001LilNewGame and17401town/Refitframes. All31wholeframebuffers matchV2783;fivepostloadactor/captainchecks,Lil2/residentB22payload andsource/disposabletown-donorhashes pass. Thesix-framecurrentsheet wasviewed. NonewRAM/code/gameplayfixture,observer orsavestate isused.',
'Freshcoverage is2581 reread /2581 integrated-reconciled /zero pending. Completion is2581(1808historicallyrevised,773retained);source/prose remains2584. Completedfilecounts are1599COMMON,754SC2,117SC0,73SC1and38SC3. All982reviewedrouteobjects arenowintegrated. ThreeCOMMONmarketrecords750-752remainincomplete;everyuntouchedstoryline,sharedshop/town dialogue,randomscene andremainingplayer-facingprose remainsinscope. Fivenamed-target2187-2191leads remainuncredited. Rawrejected-objectclassification,SC3B109,separategraphics/all18plaques andlaterolder-recordtechnicalre-audit remainopen. AllROMs,earliertranslations,clean/canonicalinputs andexecutedproofs arepreserved. Fullgoalactive;alljobsterminal.'
])

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    prior=Path('work/analysis/editorial_handoff_verification_v2806/verified_handoff.json')
    assert sha(lp.read_bytes())==read(prior)['ledger_sha256']
    release,start=read(RELEASE),read(START)
    assert release['whole_ROM_reconstruction_byte_exact'] and release['all500_manifest_batches_and114_accepted_layers_present']
    assert start['all_current_requested_and_final_framebuffers_equal_V2783'] and start['all_five_postload_actor_model_and_captain_checks_equal']
    assert start['current_Lil_captain2_and_B22_payload_verified'] and start['source_and_disposable_town_donor_unchanged']
    assert start['actual_selected_India_Polder_IDs']==[] and sha(Path(start['review_sheet']).read_bytes())==start['review_sheet_sha256']
    # The six current frames were viewed before executing this producer.
    doc=read(DOC);mapping=read(doc['reference_map']);rows=deepcopy(doc['records'])
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':84,'retain-wording':35}
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
            integrated_hex=value.hex(),completed_candidate_reference=release['candidate'],registered_prose_owner='lil_india_polder_editorial',
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
    assert len(selected)==119 and {(r['file_path'],r['id']) for r in fresh['pending_record_keys']}==selected
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2581,2462,119)
    oldkeys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']};assert not oldkeys&selected
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V2805')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    review=ROOT/'current_six_frame_visual_review.json';save(review,dict(sheet=start['review_sheet'],sha256=start['review_sheet_sha256'],viewed=True,
        findings='Lil selection and opening dialogue and inherited town/Refit component screens are legible and match V2783. Current startup only; no selectedIndia/polder activation.'))
    proofpaths=[DOC,Path(doc['reference_map']),Path(doc['native_font_proof']),Path(doc['representative_proof']),Path(doc['historical_representative_sheet_review']),Path(doc['prior_current_sheet_review']),RELEASE,START,prior,review,Path(__file__),
        Path('work/analysis/lil_India_Polder_registration_v2813/registration_receipt.json'),Path('work/analysis/lil_India_Polder_registration_v2813/negative_cases.json'),
        Path('work/analysis/lil_India_Polder_research_v2808/research_image_receipt.json'),
        Path('work/analysis/lil_India_Polder_reference_census_v2810/all193_commands40_relative_sites_and_shipped_entry_census.json'),
        Path('work/analysis/lil_India_Polder_loader_v2809/whole_SC2_and_six_selected_blocks_initial_entry_proof.json')]
    evidence={str(p):sha(p.read_bytes()) for p in proofpaths}
    save(FINAL,dict(format='dk4-natural-dialogue-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        id=FAMILY,manuscript=str(DOC),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        revised=84,retained=35,records=rows,summary=SUMMARY,evidence=evidence,actual_selected_India_Polder_IDs=[],
        new_current_candidate_emulator_runs=2,new_independent_control_runs=0,current_six_frame_sheet_viewed=True,full_goal_complete=False))
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[37,38,39,40,129,130],record_IDs=[r['id'] for r in rows],
        final_review=str(FINAL),revised_count=84,retained_count=35,fresh_revisions=84,fresh_retentions=35,
        actual_verification_scope='Historical shared progressive rules plus two current cold-start/story/town samples. All119are originalprogressive;noFEorchoices inthisbatch. No selectedIndia/polder activation.',records=rows))
    ledger.update(records_editorially_completed=2581,records_revised_and_integrated=1808,retained_wordings_editorially_completed=773)
    ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4']=754
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=[]
    active=ledger['active_source_prose_drafts']
    for p,ids in active['route_record_subsets_pending'].items():
        active['route_record_subsets_pending'][p]=[ident for ident in ids if ('/data/SC2.DK4',ident) not in selected]
    for p in [DOC]:
        if str(p) not in active['manuscripts']:active['manuscripts'].append(str(p))
        active['route_record_subsets_pending'][str(p)]=[]
    active.update(status='3-reviewed-COMMON-incomplete;no-pending-route-drafts;historical-manuscripts-preserved',
        note='2581fresh rereads integrated/reconciled;source/prose2584. MarketCOMMON750-752caller context unresolved;all wider untouched prose remains in scope.')
    fresh['integrated_record_keys'].extend(fresh['pending_record_keys'])
    fresh.update(fresh_pass_records_integrated=2581,fresh_pass_records_pending_native_actual_release=0,pending_record_keys=[],pending_contextual_families=[],
        latest_pending_contextual_family=None,latest_contextual_manuscript=str(DOC),latest_contextual_choice_draft=None,
        latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=active['note'])
    fresh['reconciled_families'].append(dict(id=FAMILY,records=119,final_review=str(FINAL),new_revisions=84,justified_retentions=35,new_completed_records=119,
        historical_reconciliation_only=False,historical_decisions_newly_completed=dict(revised=84,retained=35),actual_selected_India_Polder_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0))
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=982,completed_route_records=982,next='Continue untouched route/shared/town/random/player prose. All-route review remains open.')
        if unit['id']=='Lil-India-Camille-Polder-Gift-B37-B38-B39-B40-B129-B130-119':unit.update(status='complete-contextual-current-native-references-representative-and-registered-release',pending=None,completion_credit_added=119,final_review=str(FINAL),full_goal_complete=False)
    watch=ledger['formatting_watchlist']['lil_India_Polder_v2805']
    watch.update(status='complete-through-V2818',reference_map_pending=False,
        representative_reconciliation_pending=False,superseded_by='lil_India_Polder_v2818',final_review=str(FINAL))
    ledger['formatting_watchlist']['lil_India_Polder_v2818']=dict(status='all119-source-native-reference-representative-release-checks-pass',final_review=str(FINAL),evidence=evidence,
        actual_selected_India_Polder_IDs=[],individual_conditional_visits_not_required_under_user_policy=True,no_orphan_predicate_or_missing_glyph_waivers=True)
    oldcandidate=deepcopy(ledger['current_integrated_candidate']);ledger['previous_current_integrated_candidate_before_V2814']=oldcandidate
    ledger['integrated_candidate_reference_history'].append(oldcandidate)
    candidate=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=SUMMARY,full_goal_complete=False,
        **{key+'_sha256':digest for key,digest in release['story_hashes'].items()})
    ledger['current_integrated_candidate']=candidate;ledger['latest_registered_editorial_candidate']=deepcopy(candidate)
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v2805']['path']))
    inventory.update(incomplete_route_source_prose_groups=[],incomplete_route_source_prose_count=0,
        next_focus='Continue untouched source/story exchanges,includingthe IndianOcean/B41onward,CamilleKuhnbackstory,andallotherstorylines/sharedshop-town/random/player prose;marketCOMMON750-752callers,rawrejected-objectclassification,separategraphics andlaterolder-recordtechnicalreaudit remainopen.')
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=982,completed_route_records=982,source_prose_pending_records=0,source_prose_pending_family=None,next=inventory['next_focus'])
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v2818']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=0,full_goal_complete=False)
    ledger['lil_India_Polder_completion_v2818']=dict(summary=SUMMARY,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    keys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert keys==oldkeys|selected=={(r['file_path'],r['id']) for r in fresh['integrated_record_keys']}=={(r['file_path'],r['id']) for r in fresh['record_keys']}
    assert len(keys)==len(fresh['integrated_record_keys'])==2581
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==2584
    for key in ['reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','source_prose_reviewed_counts_by_file']:
        assert ledger[key]==before[key],key
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    release_note=('Release details: experimental profile `'+release['profile']+'`. Candidate `'+release['candidate']+'`, SHA-256 `'+release['candidate_sha256']+'`. '
        'Canonical base `'+release['canonical_base']+'`, SHA-256 `'+release['canonical_base_sha256']+'`. '
        'Clean-input patch `'+release['patch']+'`, SHA-256 `'+release['patch_sha256']+'`. '
        'The manifest enumerates all500 batches and114 accepted layers, including the full V2783 stack and the new119-speech manuscript. '
        'Internal delta from V2783: `/data/SC2.DK4` blocks37/38/39/40/129/130 only; every other file and component is exact. '
        'Verifiers: source/relocation/reference/native-font/padding checks,17 compiler rejections, `verify_lil_india_polder_release_v2815.py` and `verify_lil_india_polder_startup_v2817.py`. '
        'Current cold-boot areas are title/character selection,Lil opening,andtown/Refit. Human cold-boot acceptance is still required for promotion; V1492 remains promoted.\n\n')
    section='## V2818:119 India, Camille, polder and gift reviews completed in V2814\n\n'+SUMMARY+'\n\n'+release_note+'Final review: '+FINAL.as_posix()+'. Release/patch: '+RELEASE.as_posix()+'. Current startup: '+START.as_posix()+'. Unfinished scope: '+inv.as_posix()+'. Current COMMON parser remains dk4tool.patch.surrender_advice_contextual_v1.current_entries;bounded context remains scripts/current_common_native_context_v2677.py because ARM9/COMMON are byte-identical.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        p.write_text(('# Current editorial handoff - V2818' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    save(ROOT/'completion_receipt.json',dict(checkpoint='V2818',summary=SUMMARY,evidence={**evidence,str(FINAL):sha(FINAL.read_bytes()),str(inv):sha(inv.read_bytes())},
        updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},new_completed_records=119,new_source_prose_reviews=0,revisions=84,justified_retentions=35,
        fresh_reread=2581,fresh_integrated=2581,fresh_pending=0,source_prose=2584,completed=2581,historical_revised=1808,historical_retained=773,incomplete_COMMON=3,incomplete_route=0,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        actual_selected_India_Polder_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0,goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V2818:119completed in registeredV2814;84revisions/35retentions;2581reread/integrated,source-prose2584. COMMON3andall widerprose remainopen;fullgoalactive.')
