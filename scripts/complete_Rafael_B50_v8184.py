"""Credit twentyeight disjoint integrated B50 decisions after release/startup; recover prior ledger exactly."""
import argparse,gzip,json,os
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.Rafael_B50_release_paths_v8164 import *
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B50_completion_v8184')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8185')
LEDGER=Path('translations/editorial_review_current_v1.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8166/verified_handoff.json')
RELEASE=Path('work/analysis/Rafael_B50_release_v8173/registered_release_verification.json')
START=Path('work/analysis/Rafael_B50_context_binding_v8175/own_Rafael_startup_andstrict_captain0_context.json')
START_VIEW=Path('work/analysis/Rafael_B50_startup_view_v8176/own_Rafael_startup_sheet_viewed.json')
ATOMIC=Path('work/analysis/Rafael_B50_atomic_challenges_v8170/atomic_validation_receipt.json')
REGISTRATION=Path('work/analysis/Rafael_B50_registration_v8171/registration_receipt.json')
FINAL=Path('translations/rafael_B50_contextual_final_review_v1.json')
KEY='Rafael_SC0B50_completion_v8184'
FAMILY='Rafael_SC0B50_contextual_Lil_Camille_dye_farewell_v8184'
SCOPE='unfinished_editorial_scope_v8184'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed']
BEFORE=(7143,7146,7146,4442,2701)
AFTER=(7171,7174,7174,4455,2716)
UNVISITED=[]
INTRO='Rafael B50 is complete in registered experimental cumulative V8172:28speeches,13revisions and15individually justified retentions credited once. Totals7171completed,7174source/prose records anddrafts,4455integrated revisions,2716retentions. SC0has368completed;route subset5571. All639manifest batches/114accepted layers/18releasechecks/110regressions,full-reference equality,exactclean-inputpatch andown-currentstartup pass. MainV4701unchanged;no separate unifiedtestpackage,promotion,pruning,commit orpush. Full editorial objective remainsactive.'
DETAILS='Clean-first source/control/gloss/name/context work8131-8135 preceded currentEnglish:complete13-speech LilB131dye/map callback,all117prior opening source references/five title refs,original4821descriptor[0,181,1,5]/layout[2,0,1] andclean item181紅色の顔料/current Red Dye. No duplicate callback credit,owned parchment,route chronology orinventory award inferred. FA2 is surname Castor atR40/R61;FI1 is given Rafael atR108. No Commander rank,new relationship,marriage,pregnancy,retirement oroccupation is invented. Occasion/preparations remain unnamed andRafael remains privatelypuzzled. All prior individual prose/name reasons remain exact.\n\nFinal automaticplan8140b uses216px/fourphysical rows,all28singlepages,source00/02/09,ten source00objects,unchanged font/globalprofile/bodyNULguard andprivateFI6/FA6/FO10. Five phrase refinements preservewords/rowcounts. Native final20fresh/92reused alignments,stored60fresh/52reused,28complete sourcepages,three headerplanes andsynthetic fullCamille getter pass withscoped exact reuse. Six final native sheets and14actual sheets directlyviewed. All18infos/two exact warnings remain:R61line1the/North,R114line2to/live. No manualprosewraps,missingglyphs,blankpages orweakenedwidth/guard/rules. Preserve initialplans,supersededviews andbroader wrapleads.\n\nResearchreference out/Rafael_B50_reference_v8151_RESEARCH_ONLY.nds is preserved/pinned,not registered/newparent/handoff. OnlySC0B50changes;342otherblocks/allotherfiles/components exact. Source/current1520stored/1518logical/tail2 becomes1376stored/1374logical/tail2,end1370,15paritytails. All37commands/28six-bytepreambles/nine nontextcontrols survive,with genuinelyzero relative/predicate/querysites. Fullclean/predecessor block/wholearchive inverses pass;343fresh native load/cachepaths,686parentmodes,EV0entry8/action51/event50 andfresh shippedcallercensus bind. Outerconditions/naturalactivation andchronology unclaimed. Original opaqueA000/4821/4720/4681 andnormalvaluecarry arepreserved.\n\nPaired actual initial16001-frame coldboot fixtures each selectall28speeches/28complete singlepages/all37B50commands,plus10originalB44initializers. Total184completebody/nameholds,zero partial/unresolved masks,noFE/menu/inventedpageturn. All28upper-scene/portrait/headerRGBpairs and47selectedresults/UIrequests match. SourceJapanese is oncurrenttranslatedUI/names,not acompletecleanROM. InitializedLisbonentry isnot natural event50/originallocation/earnedprogress/fullroute/hardwarecoverage. Every originaleffectbody executes inthecore:noopaquebridge. Dyecard appears asRed Dye/Mystery Item andclears;4821duration60,A000240,4720zero,468188 both. Finalnormalreturns[0,0]at10822JP/10824EN. No RAM/party/roster/role/funds/seed/condition/resultforcing orinputretiming.\n\nMeasured35commandcomparisonrows/11durationdifferences remain. Firstphase difference sourceoffset350/R37:237/241frames,57/58LCGsteps. English exitphase+2/finalphase-10,seeds3888306843/2225786845. Seventeenof87laterfullRGBsamples differ;finalstate/tasks/calendar equal,models/persistentobjects/wholeactors differ. Rawcalendar185/[0,3,41]uninterpreted. Incidental subsequentB127tutorial/resource/town prose getsno newcredit. No laterfixture-reentry orunreturned dialoguewithin horizon.\n\nConcrete later-risk followup repeats exactfixtures/input/horizon with8read-onlyRAMsamples perlanguage,32002additionalframes/64004B50framestotal. Everyobserverrow exceptoutputpaths,all8framebuffers andfinalwholeRAM reproduceexactly perlanguage. First7samples3970/5170/5770/10930/11890/15310/15550 have equal sampledstate/models/persistentobjects/tasks/calendar/wholeactor,includingdye/hide/normalreturn andtutorial/departure. At16000 underway:twofleetbytes,oneshipbyte,105actorbytes,twotownbytes differ;company/items/goods remain equal. Fullbyte/snapshotmetadata retained at actualfocus8160. This boundsobserved laterdivergence without completecausal/everyframe/futureoutcome/broadsimulationequivalence claims. No concreteB50display/control/return defect remains. Keep allmeasuredlimits forlater older-recordtechnicalre-audit.\n\nFrozen natural-dialogue-v2 policy passes28exactpositives/511distinct expectedguard rejections. Independent production recomputes boundedrisk nativevalues fromcapturedRAM andmatches theapproved fullROM afteronefinalSC0file-listcommit. All479actual-changing proofcorruption tests reject beforeanycommit withdependencies deliberatelybypassed;trustedfrozencontract revalidatedbefore/after. RegisteredV8172 includes completeV8122stack plusone28-recordB50manifest,byteequalapprovedreference/cleaninputxdelta,18releasechecks/110regressions andfresh4001frameown-currentRafaelstartup. SixwholeRGBpairs/wholeactor/captain0/strict123264payload/2b6/COMMON/directoryguards pass;startup sheetdirectlyviewed. Otherroutecontexts historicaluntilrebound/recaptured. All28five-gate decisions andexactsource/current/effective/compiled/stored/scopedactual/integrated references arein translations/rafael_B50_contextual_final_review_v1.json. Namesv3 retainsRafaelCastor/LilArgot/CamilleOverijssel withindividualsource reasons;fullCamillegetterretainsMarinus. Full207names/roles/aliases/catalogue/customnames remainopen. Fourteendirectlyviewedactualsheets,sixfinalnativesheets,all18infos/twoexactwarningexceptions retained. Historical8149pendingmetadata block49label isincorrect;actualclean/current/native/research/actual/sealed/integrated B50references areallSC0block50. Preserve8149and8165correctioncompanion forlatertechnicalaudit. Fullfour-story editorialscope/sharedshop-town/random/Help/remainingprose/retrospectivewraps,graphics/all18plaques andlaterolder-recordtechnicalre-audit remainopen. PreserveeverypriorROM,translation,draft,failure,executedproducer,proof andunfinishedlead.'
NEXT='Continue full editorial goal from verifiedV8185/currentregisteredV8172. B50 completeandcreditedonce;reuseallverifiedsource/context/prose/names/macros/native/stored/reference/actual/policy/atomic/release/patch/startup work. OwncurrentRafaelinput work/analysis/current_V8172_Rafael_native_v8175/current_native_input.json;otherroutecontexts historicaluntilbound/recaptured. NextcleanHodram packet alreadyhas28firstsourceglosses:six-speaker B137apology/staffing21speeches,B45Amsterdam invitation1,B46treasuremapkeychallenge6. Exactsourcepackets underHodram_B137_clean_context_v8180/Hodram_next_clean_v8178/Hodram_B46_clean_context_v8179;combinednames8182 andcompletegloss/prior27B44sourcecallbacks8183. No currentEnglish bodies/names consulted,nolocalizedmanuscript/no newcredit. B137requires44;B45excludes46;B46requires137and45. Numericblockorder/graphaloneisnotnaturaleligibility ortotalchronology. SourceB13733commands/21speeches,B453commands/1speech,B4624commands/6speeches;allnewsourceactors01/02/09/10/12/71,zeroFA/FI/FO/FE. Preserveeveryfullpreamble,silence,8000predicate/queryconsumer,relatives/effects/fullend. Bind original4800b5a8and4800versusB50 4821displaybehavior beforeitemname/giftassumptions;B46identifiesdecipheringkey/proposesfirst-findcontest butdoesnotexplicitlysaymap/newgift/acceptance/winner. Portworker113source出港所の兄貴/ヨーロッパisnotliteralbrotherornewEuropeansurname;broaderPortWorkerconsumerleadremains. UseapprovedHodram/Joakim/Camille;cleansixidentitiesHodrammiddleヨアキム,Lil,Camillemiddleマリヌス,Gerhard,Charlesmiddleジャン,PortWorker. Reviewfullgetters/voices/aliases/customnames carefullywithoutnewrank/kinship/romance/hiddenidentity/biography. B137CamilleapologizesforLilbusinessterritoryinsults,Hodramacknowledgesability/reassuresratherthanformsalliance,Gerhardpromisingyoungperson/fleetstaffing/MediterraneanLisbon-Sevillepossiblecrewsearch/prospectiveroutes. Nativeevententries/branches/controls/getters/currentownHodramcontext beforecurrentEnglish comparison;thencompletewholesceneprose/native/display/representativeactual/policy/atomic/registered integration perworkflow. Preserve28sourceglossesand27priorB44callbackswithno duplicatecredit.\n\nKeepfullobjective:allfourstories/earliertranslateddialogue/sharedshop-town/random/Help/remainingprose/all207names-roles-aliases/retrospectiveearlybreaks. Cloneeverypriorunfinishedinventory,12contraction/questiontagleads,unscannedbeyond558plans,weak-before-row/page-before-readability/phrasecoherence. KeepPasardistinctfromPasha,Cristina/Christina,HansRetzel/Letzel,Trader/PortWorker/Guildmaster,Sailor151-159versusRetainerconsumers,COMMON750-752,preLF6435,ArmadilloHide/SteelHide,HerophilusMedicine,AksumGoldSeal,AlShin/AlFeridShin,イギリス andallitem/counterpart/displayleads. Graphics/all18plaques andlaterolder-recordtechnicalre-audit separate:normalendcarry,B35R65/B48R129source19thcells,B48stalerelocationlabel,B47correctedregistrationreceipt,B50checkpoint8149blocklabelcompanion,andalltiming/highlight/RNG/component/byte/calendar/RGB/fixture-reentrylimits. PreserveallROMs/translations/drafts/failures/producers/proofs. No separateunifiedpackage,promotion,pruning,commit orpush. Fullgoalactive.'
HODRAM_KEY='Hodram_SC1B137_B45_B46_clean_gloss_pending_native_context_current_andrelease_v8184'
HODRAM={'source_packets': {'137': 'work/analysis/Hodram_B137_clean_context_v8180/complete_clean_SC1_B137_EV1_andcoverage_before_current_English.json', '45': 'work/analysis/Hodram_next_clean_v8178/complete_clean_SC1_B45_EV1_andcoverage_before_current_English.json', '46': 'work/analysis/Hodram_B46_clean_context_v8179/complete_clean_SC1_B46_EV1_andcoverage_before_current_English.json'}, 'clean_names': 'work/analysis/Hodram_B137_B45_B46_clean_names_v8182/six_clean_static_identity_fields_before_current_English.json', 'first_gloss': 'work/analysis/Hodram_B137_B45_B46_clean_gloss_v8183/28_first_clean_glosses_six_identities_explicit_prerequisite_graph_before_current_English.json', 'prior_B44_source_refs': 'work/analysis/Hodram_B137_B45_B46_clean_gloss_v8183/27_prior_clean_B44_source_refs_exact_no_new_credit.json', 'file_path': '/data/SC1.DK4', 'blocks': [137, 45, 46], 'physical_source_objects': 28, 'source_static_identities': 6, 'source_macro_counts': {'FI': 0, 'FA': 0, 'FO': 0}, 'source_event_graph': '137requires44;45excludes46;46requires137and45;outereligibility/nativeactivation/totalchronologyunproved', 'current_English_bodies_andname_fields_not_consulted': True, 'source_only_no_localized_manuscript': True, 'no_new_kinship_rank_romance_map_gift_invented': True, 'native_controls_getters_items_branches_entry_context_current_andrelease_pending': True, 'source_prose_credit_added': 0, 'completion_credit_added': 0, 'full_goal_complete': False}

def digest(value):return sha(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def restore(value):
    result=deepcopy(value);entry=result.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(result,op['path'])
        if op['kind']=='append':
            assert len(parent[key])==op['before_length']+op['count'] and digest(parent[key][op['before_length']:])==op['appended_sha256']
            del parent[key][op['before_length']:]
        elif op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return result

def gates():
    release,start,view,atomic,doc,seal,reg=map(read,[RELEASE,START,START_VIEW,ATOMIC,APPROVED,SEAL,REGISTRATION])
    rom=Path(release['candidate']);manifest=read(release['manifest']);registry=read('translations/release_stack.json')
    assert sha(rom.read_bytes())==release['candidate_sha256']==manifest['candidate_sha256']==start['candidate_sha256']==view['candidate_sha256']
    assert manifest['profile']=='all-routes-unified-v8172' and len(manifest['batches'])==639 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert release['all110_release_dialogue_regressions_pass'] and release['whole_clean_input_ROM_reconstruction_byte_exact']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256'] and Path(release['exact_patch_reconstruction']).read_bytes()==rom.read_bytes()
    assert start['all_whole_RGB_actor_andcaptain_controls_equal'] and start['actual_original_captain_ID']==0 and start['whole_RGB_pair_count']==6
    assert start['all_strict2b6_COMMON_directory_and123264_payload_guards_pass']
    assert view['viewed'] and view['startup_proof_sha256']==sha(START.read_bytes())
    assert atomic['positive_records']==28 and atomic['negative_count']==reg['negative_count']==479
    assert reg['expected_manifest_batches']==639 and atomic['all_negatives_reject_before_any_files_list_commit'] and atomic['config_dependency_digests_deliberately_bypassed']
    assert seal['manuscript_sha256']==sha(APPROVED.read_bytes()) and seal['all28_five_gates_andexact_references_approved']
    assert len(doc['records'])==28 and not doc.get('typed_choice_records') and all(all(r['review'].values()) for r in doc['records'])
    assert sum(bool(r['qa_waivers']) for r in doc['records'])==2
    return release

def stage():
    assert not ROOT.exists() and not FINAL.exists();release=gates();prior=read(PRIOR)
    before=LEDGER.read_bytes();old=json.loads(before);assert sha(before)==prior['ledger_sha256']
    assert tuple(old[k] for k in COUNTERS)==BEFORE and old['goal_status']=='active' and not old['full_goal_complete']
    doc,mapping,actual=map(read,[APPROVED,MAP,proofs()['actual_proof']])
    image=NdsImage.open(release['candidate']);bank=IlnkContainer.parse(image.read_file('/data/SC0.DK4')).blocks
    oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']}
    rows=[];keys={historical_key(r) for r in doc['records']}
    assert len(oldkeys)==7143 and len(keys)==28 and not oldkeys&keys and KEY not in old
    for original in doc['records']:
        row=deepcopy(original);group=mapping['groups'][0];block=bank[50]
        ref=next(r for r in group['text_records'] if r['id']==row['id']);at=ref['new_offset'];raw=bytes.fromhex(ref['target_hex'])
        assert block[at:at+len(raw)+1]==raw+b'\0' and block[:at].count(b'\0')==ref['new_record_index'] and sha(block)==group['target_block_sha256']
        observations=[dict(block=50,version=g['version'],speech=s) for g in actual['groups'] for s in g['speech_observations'] if s['id']==row['id']]
        observed=row['id'] not in UNVISITED
        assert bool(observations)==observed and row['actual_record_observed'] is observed
        if observed:assert {o['version'] for o in observations}=={'clean_Japanese','English'} and len(observations)==2 and all(o['speech']['complete_body_holds'] for o in observations)
        row.update(actual_source_andEnglish_observations=observations,
            integrated_reference=dict(file_path=row['file_path'],block=50,offset=at,record_index=ref['new_record_index'],
                bytes=len(raw),stored_hex=raw.hex(),block_sha256=sha(block),ROM=release['candidate'],ROM_sha256=release['candidate_sha256']),
            exact_stored_reference=deepcopy(ref),source_prose_andcompletion_credit_added_once=True,source_prose_orcompletion_credit_added=True,registered_integration_pending=False,
            frozen_policy_atomic_production_andregistered_release_still_pending=False)
        rows.append(row)
    assert Counter(r['decision'] for r in rows)=={'revision':13,'retention':15}
    summary=INTRO+'\n\n'+DETAILS+'\n\n'+NEXT
    evidence={str(p):sha(Path(p).read_bytes()) for p in [PRIOR,APPROVED,MAP,SEAL,RELEASE,START,START_VIEW,ATOMIC,REGISTRATION,*map(Path,proofs().values()),Path('work/analysis/Rafael_B50_atomic_positive_v8169/positive_receipt.json'),Path(__file__),*[Path(p) for p in HODRAM['source_packets'].values()],*[Path(HODRAM[k]) for k in ['clean_names','first_gloss','prior_B44_source_refs']]]}
    ROOT.mkdir(parents=True)
    save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        manuscript=str(APPROVED),manuscript_sha256=sha(APPROVED.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        profile=release['profile'],records=rows,revised=13,retained=15,source_prose_and_completion_credit_added_once=28,
        actual_unique_speeches_each_language=28,actual_speech_occurrences=56,actual_total_complete_page_occurrences=56,
        actual_unique_pages_both_languages=56,complete_body_andheader_holds=184,offline_only_object_IDs=UNVISITED,
        native_all28_paragraphs28_single_pages_no_FE=True,
        all_source_current_effective_compiled_stored_scoped_actual_andintegrated_refs_bound=True,
        all37_commands_zero_relative_predicate_query_sites28_preambles_FA2_FI1_nine_nontext_controls_andcomplete_ends_preserved=True,
        clean_predecessor_block_andwhole_archive_inverse_exact=True,
        three_actual_names_no_native_only_full207_broader_consumers_open=True,
        all_late_differences_andnatural_activation_limits_preserved=True,
        policy28_positives511_negatives_atomic28_positive479_negatives=True,
        original_QA_18_infos_two_exact_warning_exceptions_retained=True,
        own_ROM_new_startup_runs=1,own_ROM_new_startup_frames=read(START)['actual_frames'],
        all_prior_artifacts_full_scope_graphics_separation_andlater_audit_preserved=True,
        evidence=evidence,summary=summary,full_goal_complete=False))
    new=deepcopy(old);ops=[]
    def put(path,value):
        parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent)
        ops.append(dict(kind='set',path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
    def append(path,values):
        parent,key=parent_at(new,path);ops.append(dict(kind='append',path=path,before_length=len(parent[key]),count=len(values),appended_sha256=digest(values)))
        parent[key].extend(deepcopy(values))
    for key,value in zip(COUNTERS,AFTER,strict=True):put([key],value)
    file='/data/SC0.DK4'
    for key in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:
        assert new[key][file]==340;put([key,file],368)
    append(['completed_editorial_families'],[dict(id=FAMILY,file_path=file,blocks=[50],record_IDs=[r['id'] for r in rows],
        final_review=str(FINAL),records=rows,revised_count=13,retained_count=15,fresh_revisions=13,fresh_retentions=15,actual_verification_scope=DETAILS)])
    fp=['contextual_story_natural_dialogue_pass_v1871'];keyrows=[dict(file_path=file,id=r['id']) for r in rows]
    for key in ['record_keys','integrated_record_keys']:append(fp+[key],keyrows)
    append(fp+['record_IDs'],[r['id'] for r in rows])
    for key,value in dict(fresh_pass_records_explicitly_reread=7171,fresh_pass_records_integrated=7171,latest_contextual_manuscript=str(APPROVED),
        latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=INTRO).items():put(fp+[key],value)
    append(fp+['reconciled_families'],[dict(id=FAMILY,records=28,final_review=str(FINAL),new_revisions=13,justified_retentions=15,new_completed_records=28,
        historical_reconciliation_only=False,actual_optional_event_selected=False,actual_initialized_fixture_speeches=28,
        actual_pages=28,offline_only_objects=0,all_source_English_scene_proofs_reused_without_replay=True)])
    path=str(APPROVED)
    if path not in new['active_source_prose_drafts']['manuscripts']:append(['active_source_prose_drafts','manuscripts'],[path])
    put(['active_source_prose_drafts','route_record_subsets_pending',path],[]);put(['active_source_prose_drafts','note'],INTRO)
    ri=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes')
    assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5543
    for key,value in dict(reviewed_route_records=5571,completed_route_records=5571,next=NEXT).items():put(['coverage_units',ri,key],value)
    append(['coverage_units'],[dict(id=FAMILY,status='complete-contextual-current-native-reference-representative-and-registered-release',
        file_path=file,blocks=[50],completion_credit_added=28,final_review=str(FINAL),actual_original_optional_activation=False,
        actual_objects=28,actual_pages=28,offline_only_objects=0,full_goal_complete=False)])
    put(['formatting_watchlist','Rafael_SC0B50_v8184'],dict(status='28-source-prose-native-stored-reference-allactual-registered-release-pass',
        final_review=str(FINAL),native_pages28_single_pages_no_FE=True,row_infos18_two_exact_warning_exceptions=True,
        all_measured_limits_andearlier_proofs_preserved=True,full207_names_andfull_editorial_objective_open=True))
    current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],
        ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
        status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
    current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)})
    put(['current_integrated_candidate'],current);put(['latest_checkpoint'],summary)
    pending=prior['pending_source_batch']
    put([pending,'registered_integration_completed_by'],dict(checkpoint=KEY,final_review=str(FINAL),candidate=release['candidate'],
        all_historical_pending_flags_superseded_not_deleted=True,new_credit_added_here=0))
    put([HODRAM_KEY],HODRAM)
    prior_scope=old[prior['unfinished_scope']];assert sha(Path(prior_scope['path']).read_bytes())==prior_scope['sha256']
    inventory=deepcopy(read(prior_scope['path']));inventory['next_focus']=NEXT
    inventory[HODRAM_KEY]=deepcopy(HODRAM)
    inventory[KEY]=dict(final_review=str(FINAL),completed_objects=28,revisions=13,retentions=15,registered_candidate=release['candidate'],
        full207_names_full_goal_andall_late_limits_preserved=True)
    if pending in inventory:inventory[pending]['registered_integration_completed_by']=dict(final_review=str(FINAL),all_historical_pending_flags_preserved_as_superseded=True,new_credit_here=0)
    for unit in inventory.get('broader_coverage_units',[]):
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=5571,completed_route_records=5571,next=NEXT)
    assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
    scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
    put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,
        incomplete_COMMON=3,incomplete_credited_route_drafts=0,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
    evidence[str(FINAL)]=sha(FINAL.read_bytes());evidence[str(scope)]=sha(scope.read_bytes())
    new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_operations=ops,
        record_keys=keyrows,new_source_prose_reviews=28,new_completed_records=28,revised=13,retained=15,
        new_current_candidate_emulator_runs=1,new_current_candidate_frames=read(START)['actual_frames'],
        all_source_English_scene_proofs_reused_without_replay=True,all_sessions_terminal_andreaped=True,goal_turn_classification='progress',full_goal_complete=False)
    assert restore(new)==old and new['goal_status']=='active' and not new['full_goal_complete']
    f=new[fp[0]];assert {historical_key(r) for r in f['record_keys']}=={historical_key(r) for r in f['integrated_record_keys']}==oldkeys|keys
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
    section='## V8184: Rafael B50 dye farewell integrated in cumulative V8172; full review continues\n\n'+summary+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name;prefix=('# Current editorial handoff - V8184; V8172 current\n\n' if name=='editorial_handoff_current.md' else '')+section
        targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
    files=[]
    for i,(path,data) in enumerate(targets.items()):
        planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
        if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
        files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
    save(ROOT/'staged_completion.json',dict(files=files,evidence=evidence,all28_records_integrated_once=True,no_shared_mutation_yet=True,full_goal_complete=False))
    print('Six completion targets staged:28 disjoint Rafael decisions/13 revisions/15 retentions.Deep inverse audit next.')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    if mode=='stage':stage()
    else:
        release=gates();plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
        for entry in plan['files']:
            assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256']
            assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,h in plan['evidence'].items():assert sha(Path(path).read_bytes())==h
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),
                deep_inverse_recovers_every_prior_root_family_record_counter_andcandidate=True,exactly28_disjoint_new_records=True,
                all_six_before_andplanned_hashes_verified=True,full_goal_complete=False))
            print('Deep inverse audit passes;every prior root/family/record/count/history value recovers exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes())
            for entry in plan['files']:assert Path(entry['target']).is_relative_to(Path.cwd().resolve()) and Path(entry['planned']).is_relative_to(ROOT.resolve())
            for entry in plan['files']:
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,exactly28_decisions_credited_once=True,
                current=release['candidate'],mainV4701_preserved=True,full_goal_complete=False))
            print('Six audited completion targets applied;7171 completed/4455 revisions/2716 retentions,currentV8172.Full goal active.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            completed={historical_key(r) for f in new['completed_editorial_families'] for r in f['records']}
            assert len(completed)==7171 and new['current_integrated_candidate']['sha256']==release['candidate_sha256']
            verified=dict(candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],
                patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
                ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                records_editorially_completed=7171,records_with_source_and_prose_pass=7174,records_with_source_prose_drafts=7174,
                records_revised_and_integrated=4455,retained_wordings_editorially_completed=2716,
                completed=7171,source_prose=7174,revised=4455,retained=2716,SC0=368,SC1=91,SC2=4915,SC3=197,
                reviewed_routes=5571,completed_routes=5571,manifest_batches=639,accepted_layers=114,release_checks=18,regressions=110,
                Rafael_B50_completed_once=True,Rafael_B50_policy_atomic_registered_integration_pending=False,
                final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),actual_unique_pages_both_languages=56,
                actual_speech_occurrences=56,actual_complete_body_andheader_holds=184,native_only_object_IDs=UNVISITED,
                strict_own_Rafael_current_input=read(START)['current_native_input'],next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch=HODRAM_KEY,next_clean_exchange_not_selected=False,
                full_goal_active=True,full_goal_complete=False,all_current_andearlier_limits_preserved=True,
                producer_sha256=sha(Path(__file__).read_bytes()))
            save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV8185/currentV8172:7171completed/7174source-prose/4455revisions/2716retentions;28credited once.Full objective active.')
