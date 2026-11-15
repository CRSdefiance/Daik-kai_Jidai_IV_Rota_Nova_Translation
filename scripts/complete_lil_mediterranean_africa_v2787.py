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

ROOT=Path('work/analysis/lil_Mediterranean_Africa_completion_v2787')
DOC=Path('translations/lil_mediterranean_africa_editorial_manuscript_v5.json')
FINAL=Path('translations/lil_mediterranean_africa_contextual_final_review_v1.json')
CHOICE=Path('translations/lil_mediterranean_africa_choices_editorial_draft_v4.json')
RELEASE=Path('work/analysis/lil_Mediterranean_Africa_release_v2784/registered_release_verification.json')
START=Path('work/analysis/lil_Mediterranean_Africa_startup_v2786/cold_boot_Lil_startup_town_verification.json')
FAMILY='Lil-Mediterranean-Africa-Hayreddin-Silveira-Sofala-152-contextual-completed'
SUMMARY=' '.join([
'V2787 completes152 fresh contextual reviews across Lil SC2B20/B32/B33/B34/B35/B36/B134 in registered cumulative experimentalV2783:110revisions and42individually justified retentions. All145progressive speeches,one FEshare-loss panel andsix typed reply labels preserve the complete clean-Japanese exchanges andevery stored alternative,including punctuation-only reactions. Event32requires20;event33requires134. Silveira bankruptcy aftermath is distinct fromHayreddin,andEspinosa defeat differs fromsurrender.',
'Preserve Hayreddin multiplefleets andseparate injury/lethal threats,Lil defiance,Gerhard recognition/reluctance,Camille caution,Fernando commercialreasoning andJanus alarm. Restore Fernan Silveira andGeronimo deEspinosa source introductions/company claims,littlemarketshare inSaoJorge,second-purchasepricing rather than inventeddosage,andreported recoverywithtime rather than aguaranteedcure. Goddess\' Temptation remains theapprovedtitle. No inventedrelationships,ranks,uniquenames,casualties,drugformulation orselectedoutcomes are added. All152have freshglosses,context/localizationnotes,exactclean/current/integratedreferences andallfivegates.',
'Complete353nativecommands,146preambles,124relativespans/620relocatedbranchcases,28relocatedoriginalpredicates,three typedmenus andeveryunownedlogicalbyte pass. Originalsource/current1240branchcases and292historicaldispatchercontexts remainbound. Predicateresults,eventqueryarguments0/1/2 andmappedcaller-sourcecursor are exact;onlytheoriginalfour-byteoperandcopy maywrite02279600scratch,andrestoringit recoversall4MiB. Actor/event/roster/RNG/unownedstate remainexact. All336wholeblockloaders/cachehits and672parententrymodes pass foreachparent/researchimage;three shippedentrycensuses preserve theoriginalinterpretercall withoutliteralaliases. The329otherSC2blocks andallotherfiles/components remainexact.',
'Currentnativechecks bind146complete fontplanes,1168logical/compiledmacroalignmentcases,584additionalfinalparitycases,24menustyleplanes and18bridgedVMselection/cancelreturns. Completefirst/interior/finalglyphs,blankpaper,bounds,zeroorigins,16pxphysicalrows,FE228x48mode1paper andsingle-pagecompletion pass. Sourceboundlocalv3formatter improvesphraseboundaries withoutchangingreviewedspeechwords orglobalhelper/runtimebytes;13formatterrejections and146completeEnglish/control/macroinvariants pass. All23finalsheets wereviewed orhash-identical toviewedoriginals. Only54individual ordinaryJapanese/Englishrowcountnotes remain;no weak-ending,orphan,predicate,overflow,control,missingglyph orblankpagewaiver isgranted.',
'Failed2764/2766/2768layout/font predecessors and2772/2772b/2772cmenu diagnostics arepreserved. The114pxfull-length19cellmenu losesitsleadingglyph inthenativeprobe andisnotvalidated orshipped. Finalbattleactions useunpunctuated Prepare for battle andFlee,matchingtheJapanese actionlabelstyle;spokenreplypunctuation staysintact. Allfinalmenucompleteglyphs,visiblecentering,blankstorage,order,pointers,count andresults0/1/cancel pass. No manualEnglishpadding orglobalruntimechange isintroduced.',
'Historicalactual progressive ink/gray/blank,typedmenu,FEpaper andnormalreturn rules areinherited throughexactcurrentARM9/COMMON/EV2/font/B74/sharedconsumerbytes. Currentfont/CPUtests areseparate fromactualgameplay. Userrepresentativepolicy doesnotrequireindividual conditional/speaker/nameplatevisits absentaconcreteunresolvedrisk. No selectedMediterranean/Africaactivation,newnameplate,earnedtravel,full-route orhardwareclaim ismade;inheritedthreeaccessfixtures andfive-shipCopenhagen townbattery remainunearned anddisclosed.',
'Oneguardedoptionalstage extendsthecompleteV2750stack;21negativecases rejectbeforemutation. RegisteredV2783contains499batches/114acceptedlayers. OnlySC2B20/B32/B33/B34/B35/B36/B134changesfromV2750;ARM9,COMMON,allotherfiles/components,fonts/graphics,section/BSS/cacheextents and123040stagedbytes remainexact. Theclean-inputxdelta reconstructsthewholeROMbyteforbyte. Allpreviousprofiles andV1492promotion arepreserved. Twonewtargetedheadlesscoldboots complete4001LilNewGame and17401town/Refitframes. All31wholeframebuffers matchV2750;fivepostloadactor/captainchecks,Lil2/residentB22payload andsource/disposabletown-donorhashes pass. Thesix-framecurrentsheet wasviewed. NonewRAM/code/gameplayfixture,observer orsavestate isused.',
'Freshcoverage is2462 reread /2462 integrated-reconciled /zero pending. Completion is2462(1724historicallyrevised,738retained);source/prose remains2465. Completedfilecounts are1599COMMON,635SC2,117SC0,73SC1and38SC3. All863reviewedrouteobjects arenowintegrated. ThreeCOMMONmarketrecords750-752remainincomplete;everyuntouchedstoryline,sharedshop/town dialogue,randomscene andremainingplayer-facingprose remainsinscope. Fivenamed-target2187-2191leads remainuncredited. Rawrejected-objectclassification,SC3B109,separategraphics/all18plaques andlaterolder-recordtechnicalre-audit remainopen. AllROMs,earliertranslations,clean/canonicalinputs andexecutedproofs arepreserved. Fullgoalactive;alljobsterminal.'
])

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    prior=Path('work/analysis/editorial_handoff_verification_v2775/verified_handoff.json')
    assert sha(lp.read_bytes())==read(prior)['ledger_sha256']
    release,start=read(RELEASE),read(START)
    assert release['whole_ROM_reconstruction_byte_exact'] and release['all499_manifest_batches_and114_accepted_layers_present']
    assert start['all_current_requested_and_final_framebuffers_equal_V2750'] and start['all_five_postload_actor_model_and_captain_checks_equal']
    assert start['current_Lil_captain2_and_B22_payload_verified'] and start['source_and_disposable_town_donor_unchanged']
    assert start['actual_selected_Mediterranean_Africa_IDs']==[] and sha(Path(start['review_sheet']).read_bytes())==start['review_sheet_sha256']
    # The six current frames were viewed before executing this producer.
    doc=read(DOC);mapping=read(doc['reference_map']);rows=deepcopy(doc['records']+read(CHOICE)['records'])
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':110,'retain-wording':42}
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
            integrated_hex=value.hex(),completed_candidate_reference=release['candidate'],registered_prose_owner='lil_mediterranean_africa_editorial',
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
    assert len(selected)==152 and {(r['file_path'],r['id']) for r in fresh['pending_record_keys']}==selected
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2462,2310,152)
    oldkeys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']};assert not oldkeys&selected
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V2774')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    review=ROOT/'current_six_frame_visual_review.json';save(review,dict(sheet=start['review_sheet'],sha256=start['review_sheet_sha256'],viewed=True,
        findings='Lil selection and opening dialogue and inherited town/Refit component screens are legible and match V2750. Current startup only; no selected Mediterranean/Africa activation.'))
    proofpaths=[DOC,CHOICE,Path(doc['reference_map']),Path(doc['native_font_proof']),Path(doc['representative_proof']),Path(doc['historical_representative_sheet_review']),Path(doc['prior_current_sheet_review']),RELEASE,START,prior,review,Path(__file__),
        Path('work/analysis/lil_Mediterranean_Africa_registration_v2782/registration_receipt.json'),Path('work/analysis/lil_Mediterranean_Africa_registration_v2782/negative_cases.json'),
        Path('work/analysis/lil_Mediterranean_Africa_research_v2777/research_image_receipt.json'),
        Path('work/analysis/lil_Mediterranean_Africa_reference_census_v2779/all353_commands124_relative_sites_and_shipped_entry_census.json'),
        Path('work/analysis/lil_Mediterranean_Africa_loader_v2778/whole_SC2_and_seven_selected_blocks_initial_entry_proof.json')]
    evidence={str(p):sha(p.read_bytes()) for p in proofpaths}
    save(FINAL,dict(format='dk4-natural-dialogue-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        id=FAMILY,manuscript=str(DOC),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        revised=110,retained=42,records=rows,summary=SUMMARY,evidence=evidence,actual_selected_Mediterranean_Africa_IDs=[],
        new_current_candidate_emulator_runs=2,new_independent_control_runs=0,current_six_frame_sheet_viewed=True,full_goal_complete=False))
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[20,32,33,152,35,36,134],record_IDs=[r['id'] for r in rows],
        final_review=str(FINAL),revised_count=110,retained_count=42,fresh_revisions=110,fresh_retentions=42,
        actual_verification_scope='Historical progressive,FEandmenu sharedrules plus two current cold-start/story/town samples;all146panels/three typedmenus and28relocatedpredicates are separately native-tested. No selected Mediterranean/Africa activation.',records=rows))
    ledger.update(records_editorially_completed=2462,records_revised_and_integrated=1724,retained_wordings_editorially_completed=738)
    ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4']=635
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=[]
    active=ledger['active_source_prose_drafts']
    for p,ids in active['route_record_subsets_pending'].items():
        active['route_record_subsets_pending'][p]=[ident for ident in ids if ('/data/SC2.DK4',ident) not in selected]
    for p in [DOC,CHOICE]:
        if str(p) not in active['manuscripts']:active['manuscripts'].append(str(p))
        active['route_record_subsets_pending'][str(p)]=[]
    active.update(status='3-reviewed-COMMON-incomplete;no-pending-route-drafts;historical-manuscripts-preserved',
        note='2462fresh rereads integrated/reconciled;source/prose2465. MarketCOMMON750-752caller context unresolved;all wider untouched prose remains in scope.')
    fresh['integrated_record_keys'].extend(fresh['pending_record_keys'])
    fresh.update(fresh_pass_records_integrated=2462,fresh_pass_records_pending_native_actual_release=0,pending_record_keys=[],pending_contextual_families=[],
        latest_pending_contextual_family=None,latest_contextual_manuscript=str(DOC),latest_contextual_choice_draft=str(CHOICE),
        latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=active['note'])
    fresh['reconciled_families'].append(dict(id=FAMILY,records=152,final_review=str(FINAL),new_revisions=110,justified_retentions=42,new_completed_records=152,
        historical_reconciliation_only=False,historical_decisions_newly_completed=dict(revised=110,retained=42),actual_selected_Mediterranean_Africa_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0))
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=863,completed_route_records=863,next='Continue untouched route/shared/town/random/player prose. All-route review remains open.')
        if unit['id']=='Lil-Mediterranean-Africa-Hayreddin-Silveira-Sofala-152':unit.update(status='complete-contextual-current-native-references-representative-and-registered-release',pending=None,completion_credit_added=152,final_review=str(FINAL),full_goal_complete=False)
    watch=ledger['formatting_watchlist']['lil_Mediterranean_Africa_v2774']
    watch.update(status='complete-through-V2787',reference_map_pending=False,
        representative_reconciliation_pending=False,superseded_by='lil_Mediterranean_Africa_v2787',final_review=str(FINAL))
    ledger['formatting_watchlist']['lil_Mediterranean_Africa_v2787']=dict(status='all152-source-native-reference-representative-release-checks-pass',final_review=str(FINAL),evidence=evidence,
        actual_selected_Mediterranean_Africa_IDs=[],individual_conditional_visits_not_required_under_user_policy=True,no_orphan_predicate_or_missing_glyph_waivers=True)
    oldcandidate=deepcopy(ledger['current_integrated_candidate']);ledger['previous_current_integrated_candidate_before_V2783']=oldcandidate
    ledger['integrated_candidate_reference_history'].append(oldcandidate)
    candidate=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=SUMMARY,full_goal_complete=False,
        **{key+'_sha256':digest for key,digest in release['story_hashes'].items()})
    ledger['current_integrated_candidate']=candidate;ledger['latest_registered_editorial_candidate']=deepcopy(candidate)
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v2774']['path']))
    inventory.update(incomplete_route_source_prose_groups=[],incomplete_route_source_prose_count=0,
        next_focus='Continue untouched source/story exchanges,includingB37India/B38Camille/B39-B40polders,andallotherstorylines/sharedshop-town/random/player prose;marketCOMMON750-752callers,rawrejected-objectclassification,separategraphics andlaterolder-recordreaudit remainopen.')
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=863,completed_route_records=863,source_prose_pending_records=0,source_prose_pending_family=None,next=inventory['next_focus'])
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v2787']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=0,full_goal_complete=False)
    ledger['lil_Mediterranean_Africa_completion_v2787']=dict(summary=SUMMARY,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    keys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert keys==oldkeys|selected=={(r['file_path'],r['id']) for r in fresh['integrated_record_keys']}=={(r['file_path'],r['id']) for r in fresh['record_keys']}
    assert len(keys)==len(fresh['integrated_record_keys'])==2462
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==2465
    for key in ['reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','source_prose_reviewed_counts_by_file']:
        assert ledger[key]==before[key],key
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    release_note=('Release details: experimental profile `'+release['profile']+'`. Candidate `'+release['candidate']+'`, SHA-256 `'+release['candidate_sha256']+'`. '
        'Canonical base `'+release['canonical_base']+'`, SHA-256 `'+release['canonical_base_sha256']+'`. '
        'Clean-input patch `'+release['patch']+'`, SHA-256 `'+release['patch_sha256']+'`. '
        'The manifest enumerates all499 batches and114 accepted layers, including the full V2750 stack and the new146-panel manuscript andsix-label typed-choice manuscript. '
        'Internal delta from V2750: `/data/SC2.DK4` blocks20/32/33/34/35/36/134 only; every other file and component is exact. '
        'Verifiers: source/relocation/reference/native-font/padding checks,21 compiler rejections, `verify_lil_mediterranean_africa_release_v2784.py` and `verify_lil_mediterranean_africa_startup_v2786.py`. '
        'Current cold-boot areas are title/character selection,Lil opening,andtown/Refit. Human cold-boot acceptance is still required for promotion; V1492 remains promoted.\n\n')
    section='## V2787:152 post-Seville and Egypt-warning entries completed in V2783\n\n'+SUMMARY+'\n\n'+release_note+'Final review: '+FINAL.as_posix()+'. Release/patch: '+RELEASE.as_posix()+'. Current startup: '+START.as_posix()+'. Unfinished scope: '+inv.as_posix()+'. Current COMMON parser remains dk4tool.patch.surrender_advice_contextual_v1.current_entries;bounded context remains scripts/current_common_native_context_v2677.py because ARM9/COMMON are byte-identical.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        p.write_text(('# Current editorial handoff - V2787' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    save(ROOT/'completion_receipt.json',dict(checkpoint='V2787',summary=SUMMARY,evidence={**evidence,str(FINAL):sha(FINAL.read_bytes()),str(inv):sha(inv.read_bytes())},
        updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},new_completed_records=152,new_source_prose_reviews=0,revisions=110,justified_retentions=42,
        fresh_reread=2462,fresh_integrated=2462,fresh_pending=0,source_prose=2465,completed=2462,historical_revised=1724,historical_retained=738,incomplete_COMMON=3,incomplete_route=0,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        actual_selected_Mediterranean_Africa_IDs=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0,goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V2787:152completed in registeredV2783;110revisions/42retentions;2462reread/integrated,source/prose2465. COMMON3andall wider prose remain open;full goal active.')
