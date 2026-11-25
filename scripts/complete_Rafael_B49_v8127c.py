"""Credit sixtyone disjoint integrated B49 decisions after release/startup; recover prior ledger exactly."""
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
from scripts.Rafael_B49_release_paths_v8114 import *
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B49_completion_v8127')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8128')
LEDGER=Path('translations/editorial_review_current_v1.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8116/verified_handoff.json')
RELEASE=Path('work/analysis/Rafael_B49_release_v8123/registered_release_verification.json')
START=Path('work/analysis/Rafael_B49_context_binding_v8125/own_Rafael_startup_andstrict_captain0_context.json')
START_VIEW=Path('work/analysis/Rafael_B49_startup_view_v8126/own_Rafael_startup_sheet_viewed.json')
ATOMIC=Path('work/analysis/Rafael_B49_atomic_challenges_v8120/atomic_validation_receipt.json')
REGISTRATION=Path('work/analysis/Rafael_B49_registration_v8121/registration_receipt.json')
FINAL=Path('translations/rafael_B49_contextual_final_review_v1.json')
KEY='Rafael_SC0B49_completion_v8127'
FAMILY='Rafael_SC0B49_contextual_NorthSea_Argot_pact_exchange_v8127'
SCOPE='unfinished_editorial_scope_v8127'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed']
BEFORE=(7082,7085,7085,4411,2671)
AFTER=(7143,7146,7146,4442,2701)
UNVISITED=['DK4_MES_B49_R0032', 'DK4_MES_B49_R0067', 'DK4_MES_B49_R0112', 'DK4_MES_B49_R0225', 'DK4_MES_B49_R0244', 'DK4_MES_B49_R0296', 'DK4_MES_B49_R0311', 'DK4_MES_B49_R0356', 'DK4_MES_B49_R0381', 'DK4_MES_B49_R0405', 'DK4_MES_B49_R0409']
INTRO='Rafael B49 is complete in registered experimental cumulative V8122: 61 speeches,31 revisions and30 individually justified retentions credited once. Totals are7,143completed,7,146source/prose records anddrafts,4,442integrated revisions and2,701retentions. SC0has340completed records;the route subset has5,543. All638manifest batches,114accepted layers,18release checks,110regressions,whole-reference equality andexact clean-input patch reconstruction pass. MainV4701 is unchanged. The full editorial goal remains active.'
DETAILS="Complete clean Japanese,seven source identities,B39's22-speech prerequisite andB41's27-speech destination context preceded current English. Exact source/current/effective/stored/integrated references,31revisions and30individual retention reasons are in translations/rafael_B49_contextual_final_review_v1.json. Preserve Lil's blunt bravado,Camille's restraint,Rafael's mild perceptiveness,the unfinished Hodram Ber... something joke,surname-only Clifford,Martin Speyer/Hanseatic League,prospective territorial claims,temporary trade request,the proposed pact rather than completed alliance,conditional common-enemy exchange,grudging loyalty andqualified closing. No new kinship,rank,romance,identity reveal,already-signed alliance,permanent trading ban or guaranteed future behavior is invented. R388 retains working effective catalogue words,normalizes full-width I andpreserves FI;R311 retains its working words andFI. Approved Rafael,Hodram,Joakim andCamille remain. Full207name/role/alias andbroader consumer review stays open.\n\nAll61native paragraphs produce61complete single pages;no FE/menu or invented page-turn test. Final compiled evidence20fresh224reused cases;stored124fresh120reused with31parity tails. Source00has16objects/15unique bodies,allseven selectors00/02/04/05/06/08/09 retain complete six-byte preambles. English uses216px/four physical rows,unchanged fonts/global profile/body NULguard,exact private FI6/FA6/FO10,twoFI andnoFA/FO. Final8090c keeps coherent phrases without newwords orrows;all22original infos andthree precise warning exceptions remain at R213line1the/fight,R244line2to/the,R405line1the/North. Preserve all initial/experimental plans,failures andthe retrospective planner leads.\n\nAll154commands,56relative sites,13raw predicates,one completion query,sevenA000effects,C281 andfullfour-byte end survive.280relocated relative cases,25seeded value-carry ends,343load/cache paths,686parent modes andshipped callers pass.156250structural compositions produce256distinct complete text paths;they are not all proved attainable gameplay states. Event49requires39/excludes151;query41choosesAfrica/NewWorld versusNewWorld/farEast,not Africa-cleared/Proof-obtained. Research3976stored/3974logical/tail2 becomes3792stored/logical/tail0,end3788. Complete clean/predecessor block andwhole archive inverses are exact,342otherSC0blocks/allotherfiles/components unchanged.\n\nPaired readonly cold-boot emulator entry fixtures preserve all original ten B44initializers andthe complete154-command B49block. Both completed24001frames,48002total withidentical ordinary Ainputs andno RAM/party/role/roster/funds/seed/condition/resultforcing. Both actually selected50speeches/50pages,119exchangecommands/129including initialization. All318complete body/name holds pass,zero partials/unresolved masks. All22actual sheets directlyviewed. ActualnamesRafael0,Lil2,Claudio5,Camille9 complete;Janus4,Julio6,Arcadius8 remain native-only. Elevenconditional speechesR32/67/112/225/244/296/311/356/381/405/409 remain native-only. No further visit is required absent a distinct display orconcrete risk. This disclosed initialized fixture is inLisbon,not naturalAmsterdam/event49activation,earned progress,fullroute orhardware coverage. IncidentalTrader/tradeUI hasno extra editorialcredit.\n\nC281's original effect body executes4016-4017inboth languages,consumes2bytes,returns[3,0],has equal measuredUIrequests andno internalRNGadvance. Its transition,Lil/Camille fullnames/portraits,completeconfrontation andnormalreturn areverified. All50upper-scene/portrait/headerRGBpairs andall129selected results/UIrequests match. Normalreturns[0,0]occur16013Japanese/16016English. Preserve111comparisonrows/18durationdifferences;first phase difference atsourceoffset114,duration237/241,steps57/58. English exitLCGphase+3/final+2,seeds3456469704/204362374. Finalsampled state,models,persistentobjects,tasks,calendar andwholeactor match;19of134later unmaskedRGBsamples differ. Rawcalendarsticks0/[0,0,0]remain uninterpreted. No laterfixture-reentry/unreturneddialogue withinthishorizon. Noevery-callcausaltrace,fullRAMeveryframe,futurerandomoutcome orbroad simulationequivalenceclaim.\n\nFrozen source/prose/width/page/control/warning policy passes61positives/1014distinct expected-guard rejections. Independent production passesone finalfile-list commit,whole-ROMequality toapprovedfullreference,and413meaningful semantic proof-corruption rejects withdependencies deliberatelybypassed andcommits trapped;trustedfrozencontract revalidatedbefore/after. RegisteredV8122includesfullV8066stack plusoneB49manifest,exactclean-inputxdelta,all18releasechecks/110regressions andfresh4001-frame own-current Rafaelstartup. SixwholeRGBpairs,wholeactor/captain0 andstrict123264payload/2b6/COMMON/directoryguards pass;startup sheetdirectlyviewed. Otherroutecontextshistoricaluntilrebound/recaptured. AllpreviousROMs,translations,drafts,failures andproofspreserved. Broadereditorialscope,graphics/all18plaques andlaterolder-recordtechnicalre-auditremainopen."
NEXT="B50 source-only progress is already saved:28 complete clean Japanese speeches,three original identities and28first-source glosses. Current B50English bodies remain unread. Event50/category5/action51 has no explicit prerequisite/exclusion list;numeric adjacency toB49 doesnot establish chronology. Lil offers a key to decipher a treasure-location map andlater identifies it as a pigment;Camille says FAisnowtheNorthSealeader. Preparations,newwayoflife,thanks andan unnamed congratulatory gesture leave Rafaelprivatelypuzzled. Preserve that ambiguity;do not invent marriage,romance,pregnancy,retirement orbiography. Native EV0entry,all37commands/28preambles,zero relative/predicate/query sites and25seeded normalvaluecarry ends nowpass at work/analysis/Rafael_B50_source_controls_v8132/source_EV0_entry37_commands28_speeches_no_relative_predicate25_seeded_ends.json. Opaque4821/4720/4681/A000bytes andextents arebound;full effects/itemidentity,nativeFA2/FI1expansion/title/context/callers andcurrentEnglish comparison remainpending. Sourcepacket:work/analysis/Rafael_next_clean_v8129/complete_clean_SC0_B50_EV0_andcoverage_before_current_English.json;cleanidentities:work/analysis/Rafael_B50_clean_names_v8130/three_clean_static_identity_fields_before_current_English.json;glosses:work/analysis/Rafael_B50_clean_gloss_v8131/28_first_clean_glosses_three_source_identities_before_current_English.json. These artifacts bind verifiedV8116 whileB49atomic checks ran;cleaninputunchanged. B50hasno completion/source-prosecredit.\n\nContinue the full editorial goal from verifiedV8128/currentregisteredV8122. B49's61decisions are complete andcreditedonce. Reuse verified source/context/sevennames/branches/prose/native/stored/fullreference/actual/policy/atomic/release/patch/startup checks without needlessreplay. Use work/analysis/current_V8122_Rafael_native_v8125/current_native_input.json;otherroutecontextsremainhistorical.\n\nSelect the next untouched complete clean exchange using exactEV/caller/conditional/prerequisitecontext before currentEnglish. Blockorder alone doesnotprovechronology. B39/B41 prerequisite/variant contexts andB128/B37callbackcontexts were read earlier;incidental B127/Sailor/resource/Trader/tradeUI remain previouslyexposed leads,not newcredit. Preserve allfourstorylines,earliertranslations,sharedshops/towns,randomscenes,Help,remainingprose,all207names/roles/aliases andretrospectiveprematurewrapping. Keep everypriorunfinishedinventory,twelvecontraction/questiontagleads,unscannedrecords beyond558plans,the inheritedweak-before-row/page-boundary-before-readability andB49phrase-coherenceleads. Do notmechanically minimize rows orreverse justifiedphrasing.\n\nKeepPasardistinctfromPasha andhistoricalcounterpartqueues;retainCristina/Christina,HansRetzel/Letzel,Trader/PortWorker/Guildmaster,Sailor151-159 versusRetainerconsumers,COMMON750-752,preLF6435,ArmadilloHide/SteelHide,HerophilusMedicine,AksumGoldSeal,AlShin/AlFeridShin,イギリス andeveryrecorded item/counterpart/displaylead. Graphics/all18plaques andlaterolder-recordtechnicalre-auditstayseparate,includingnormal-endvaluecarry,source-onlyB35R65/B48R129nineteenthcells,B48stalerelocationlabel,B47correctedregistrationreceipt andallmeasuredtiming/highlight/RNG/component/calendar/RGB/fixture-reentrylimits. Preserveeveryartifact. MainV4701unchanged;no separateunifiedpackage,promotion,pruning,commit orpush. Fullobjectiveactive."

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
    assert manifest['profile']=='all-routes-unified-v8122' and len(manifest['batches'])==638 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert release['all110_release_dialogue_regressions_pass'] and release['whole_clean_input_ROM_reconstruction_byte_exact']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256'] and Path(release['exact_patch_reconstruction']).read_bytes()==rom.read_bytes()
    assert start['all_whole_RGB_actor_andcaptain_controls_equal'] and start['actual_original_captain_ID']==0 and start['whole_RGB_pair_count']==6
    assert start['all_strict2b6_COMMON_directory_and123264_payload_guards_pass']
    assert view['viewed'] and view['startup_proof_sha256']==sha(START.read_bytes())
    assert atomic['positive_records']==61 and atomic['negative_count']==reg['negative_count']==413
    assert reg['expected_manifest_batches']==638 and atomic['all_negatives_reject_before_any_files_list_commit'] and atomic['config_dependency_digests_deliberately_bypassed']
    assert seal['manuscript_sha256']==sha(APPROVED.read_bytes()) and seal['all61_five_gates_andexact_references_approved']
    assert len(doc['records'])==61 and not doc.get('typed_choice_records') and all(all(r['review'].values()) for r in doc['records'])
    assert sum(bool(r['qa_waivers']) for r in doc['records'])==3
    return release

def stage():
    assert not ROOT.exists() and not FINAL.exists();release=gates();prior=read(PRIOR)
    before=LEDGER.read_bytes();old=json.loads(before);assert sha(before)==prior['ledger_sha256']
    assert tuple(old[k] for k in COUNTERS)==BEFORE and old['goal_status']=='active' and not old['full_goal_complete']
    doc,mapping,actual=map(read,[APPROVED,MAP,proofs()['actual_proof']])
    image=NdsImage.open(release['candidate']);bank=IlnkContainer.parse(image.read_file('/data/SC0.DK4')).blocks
    oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']}
    rows=[];keys={historical_key(r) for r in doc['records']}
    assert len(oldkeys)==7082 and len(keys)==61 and not oldkeys&keys and KEY not in old
    for original in doc['records']:
        row=deepcopy(original);group=mapping['groups'][0];block=bank[49]
        ref=next(r for r in group['text_records'] if r['id']==row['id']);at=ref['new_offset'];raw=bytes.fromhex(ref['target_hex'])
        assert block[at:at+len(raw)+1]==raw+b'\0' and block[:at].count(b'\0')==ref['new_record_index'] and sha(block)==group['target_block_sha256']
        observations=[dict(block=49,version=g['version'],speech=s) for g in actual['groups'] for s in g['speech_observations'] if s['id']==row['id']]
        observed=row['id'] not in UNVISITED
        assert bool(observations)==observed and row['actual_record_observed'] is observed
        if observed:assert {o['version'] for o in observations}=={'clean_Japanese','English'} and len(observations)==2 and all(o['speech']['complete_body_holds'] for o in observations)
        row.update(actual_source_andEnglish_observations=observations,
            integrated_reference=dict(file_path=row['file_path'],block=49,offset=at,record_index=ref['new_record_index'],
                bytes=len(raw),stored_hex=raw.hex(),block_sha256=sha(block),ROM=release['candidate'],ROM_sha256=release['candidate_sha256']),
            exact_stored_reference=deepcopy(ref),source_prose_andcompletion_credit_added_once=True,source_prose_orcompletion_credit_added=True,registered_integration_pending=False,
            frozen_policy_atomic_production_andregistered_release_still_pending=False)
        rows.append(row)
    assert Counter(r['decision'] for r in rows)=={'revision':31,'retention':30}
    summary=INTRO+'\n\n'+DETAILS+'\n\n'+NEXT
    evidence={str(p):sha(Path(p).read_bytes()) for p in [
        PRIOR,APPROVED,MAP,SEAL,RELEASE,START,START_VIEW,ATOMIC,REGISTRATION,*map(Path,proofs().values()),
        Path('work/analysis/Rafael_B49_atomic_positive_v8119/positive_receipt.json'),Path('work/analysis/Rafael_next_clean_v8073/complete_clean_SC0_B49_EV0_andcoverage_before_current_English.json'),Path('work/analysis/Rafael_B49_clean_names_v8074/seven_clean_static_identity_fields_before_current_English.json'),Path('work/analysis/Rafael_B49_clean_gloss_v8075/61_first_clean_glosses_seven_source_identities_before_current_English.json'),Path('work/analysis/Rafael_B49_prerequisite_B39_v8076/complete_clean_SC0_B39_EV0_andcoverage_before_current_English.json'),Path('work/analysis/Rafael_B49_prerequisite_gloss_v8077/complete22_clean_B39_glosses_explicit_B49_prerequisite_context_only.json'),*[Path(p) for p in ['work/analysis/Rafael_next_clean_v8129/complete_clean_SC0_B50_EV0_andcoverage_before_current_English.json', 'work/analysis/Rafael_B50_clean_names_v8130/three_clean_static_identity_fields_before_current_English.json', 'work/analysis/Rafael_B50_clean_gloss_v8131/28_first_clean_glosses_three_source_identities_before_current_English.json']],Path('work/analysis/Rafael_B50_source_controls_v8132/source_EV0_entry37_commands28_speeches_no_relative_predicate25_seeded_ends.json'),Path(__file__)]}
    ROOT.mkdir(parents=True)
    save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        manuscript=str(APPROVED),manuscript_sha256=sha(APPROVED.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        profile=release['profile'],records=rows,revised=31,retained=30,source_prose_and_completion_credit_added_once=61,
        actual_unique_speeches_each_language=50,actual_speech_occurrences=100,actual_total_complete_page_occurrences=100,
        actual_unique_pages_both_languages=100,complete_body_andheader_holds=318,offline_only_object_IDs=UNVISITED,
        native_all61_paragraphs61_single_pages_no_FE=True,
        all_source_current_effective_compiled_stored_scoped_actual_andintegrated_refs_bound=True,
        all154_commands56_relatives61_preambles_13predicates_onequery_twoFI_sevenA000_C281_andcomplete_ends_preserved=True,
        clean_predecessor_block_andwhole_archive_inverse_exact=True,
        four_actual_names_three_native_only_full207_broader_consumers_open=True,
        all_late_differences_andnatural_activation_limits_preserved=True,
        policy61_positives1014_negatives_atomic61_positive413_negatives=True,
        original_QA_22_infos_three_exact_warning_exceptions_retained=True,
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
        assert new[key][file]==279;put([key,file],340)
    append(['completed_editorial_families'],[dict(id=FAMILY,file_path=file,blocks=[49],record_IDs=[r['id'] for r in rows],
        final_review=str(FINAL),records=rows,revised_count=31,retained_count=30,fresh_revisions=31,fresh_retentions=30,actual_verification_scope=DETAILS)])
    fp=['contextual_story_natural_dialogue_pass_v1871'];keyrows=[dict(file_path=file,id=r['id']) for r in rows]
    for key in ['record_keys','integrated_record_keys']:append(fp+[key],keyrows)
    append(fp+['record_IDs'],[r['id'] for r in rows])
    for key,value in dict(fresh_pass_records_explicitly_reread=7143,fresh_pass_records_integrated=7143,latest_contextual_manuscript=str(APPROVED),
        latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=INTRO).items():put(fp+[key],value)
    append(fp+['reconciled_families'],[dict(id=FAMILY,records=61,final_review=str(FINAL),new_revisions=31,justified_retentions=30,new_completed_records=61,
        historical_reconciliation_only=False,actual_optional_event_selected=False,actual_initialized_fixture_speeches=50,
        actual_pages=50,offline_only_objects=11,all_source_English_scene_proofs_reused_without_replay=True)])
    path=str(APPROVED)
    if path not in new['active_source_prose_drafts']['manuscripts']:append(['active_source_prose_drafts','manuscripts'],[path])
    put(['active_source_prose_drafts','route_record_subsets_pending',path],[]);put(['active_source_prose_drafts','note'],INTRO)
    ri=next(i for i,r in enumerate(new['coverage_units']) if r['id']=='all-route-scenes')
    assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5482
    for key,value in dict(reviewed_route_records=5543,completed_route_records=5543,next=NEXT).items():put(['coverage_units',ri,key],value)
    append(['coverage_units'],[dict(id=FAMILY,status='complete-contextual-current-native-reference-representative-and-registered-release',
        file_path=file,blocks=[49],completion_credit_added=61,final_review=str(FINAL),actual_original_optional_activation=False,
        actual_objects=50,actual_pages=50,offline_only_objects=11,full_goal_complete=False)])
    put(['formatting_watchlist','Rafael_SC0B49_v8127'],dict(status='61-source-prose-native-stored-reference-representative-actual-registered-release-pass',
        final_review=str(FINAL),native_pages61_single_pages_no_FE=True,row_infos22_three_exact_warning_exceptions=True,
        all_measured_limits_andearlier_proofs_preserved=True,full207_names_andfull_editorial_objective_open=True))
    current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],
        ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
        status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
    current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)})
    put(['current_integrated_candidate'],current);put(['latest_checkpoint'],summary)
    pending=prior['pending_source_batch']
    put([pending,'registered_integration_completed_by'],dict(checkpoint=KEY,final_review=str(FINAL),candidate=release['candidate'],
        all_historical_pending_flags_superseded_not_deleted=True,new_credit_added_here=0))
    put(['Rafael_SC0B50_source_gloss_pending_controls_current_andrelease_v8127'], {'source_packet': 'work/analysis/Rafael_next_clean_v8129/complete_clean_SC0_B50_EV0_andcoverage_before_current_English.json', 'clean_names': 'work/analysis/Rafael_B50_clean_names_v8130/three_clean_static_identity_fields_before_current_English.json', 'first_gloss': 'work/analysis/Rafael_B50_clean_gloss_v8131/28_first_clean_glosses_three_source_identities_before_current_English.json', 'physical_source_objects': 28, 'source_static_identities': 3, 'source_macro_counts': {'FI': 1, 'FA': 2, 'FO': 0}, 'event50_category5_action51_no_explicit_prerequisite_exclusion_not_natural_eligibility': True, 'current_B50_English_body_still_unread': True, 'B49_known_approved_names_not_new_B50_current_name_comparison': True, 'source_gloss_only_no_localized_manuscript': True, 'unnamed_celebration_occasion_not_invented': True, 'native_controls_getters_item_effects_title_context_current_comparison_andrelease_pending': True, 'completion_credit_added': 0, 'source_prose_credit_added': 0, 'full_goal_complete': False, 'source_controls': 'work/analysis/Rafael_B50_source_controls_v8132/source_EV0_entry37_commands28_speeches_no_relative_predicate25_seeded_ends.json', 'original_EV0_entry37commands28speeches_zero_branches_predicates25_seeded_ends_pass': True})
    prior_scope=old[prior['unfinished_scope']];assert sha(Path(prior_scope['path']).read_bytes())==prior_scope['sha256']
    inventory=deepcopy(read(prior_scope['path']));inventory['next_focus']=NEXT
    inventory['Rafael_SC0B50_source_gloss_pending_controls_current_andrelease_v8127']={'source_packet': 'work/analysis/Rafael_next_clean_v8129/complete_clean_SC0_B50_EV0_andcoverage_before_current_English.json', 'clean_names': 'work/analysis/Rafael_B50_clean_names_v8130/three_clean_static_identity_fields_before_current_English.json', 'first_gloss': 'work/analysis/Rafael_B50_clean_gloss_v8131/28_first_clean_glosses_three_source_identities_before_current_English.json', 'physical_source_objects': 28, 'source_static_identities': 3, 'source_macro_counts': {'FI': 1, 'FA': 2, 'FO': 0}, 'event50_category5_action51_no_explicit_prerequisite_exclusion_not_natural_eligibility': True, 'current_B50_English_body_still_unread': True, 'B49_known_approved_names_not_new_B50_current_name_comparison': True, 'source_gloss_only_no_localized_manuscript': True, 'unnamed_celebration_occasion_not_invented': True, 'native_controls_getters_item_effects_title_context_current_comparison_andrelease_pending': True, 'completion_credit_added': 0, 'source_prose_credit_added': 0, 'full_goal_complete': False, 'source_controls': 'work/analysis/Rafael_B50_source_controls_v8132/source_EV0_entry37_commands28_speeches_no_relative_predicate25_seeded_ends.json', 'original_EV0_entry37commands28speeches_zero_branches_predicates25_seeded_ends_pass': True}
    inventory[KEY]=dict(final_review=str(FINAL),completed_objects=61,revisions=31,retentions=30,registered_candidate=release['candidate'],
        full207_names_full_goal_andall_late_limits_preserved=True)
    if pending in inventory:inventory[pending]['registered_integration_completed_by']=dict(final_review=str(FINAL),all_historical_pending_flags_preserved_as_superseded=True,new_credit_here=0)
    for unit in inventory.get('broader_coverage_units',[]):
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=5543,completed_route_records=5543,next=NEXT)
    assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
    scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
    put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,
        incomplete_COMMON=3,incomplete_credited_route_drafts=0,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
    evidence[str(FINAL)]=sha(FINAL.read_bytes());evidence[str(scope)]=sha(scope.read_bytes())
    new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_operations=ops,
        record_keys=keyrows,new_source_prose_reviews=61,new_completed_records=61,revised=31,retained=30,
        new_current_candidate_emulator_runs=1,new_current_candidate_frames=read(START)['actual_frames'],
        all_source_English_scene_proofs_reused_without_replay=True,all_sessions_terminal_andreaped=True,goal_turn_classification='progress',full_goal_complete=False)
    assert restore(new)==old and new['goal_status']=='active' and not new['full_goal_complete']
    f=new[fp[0]];assert {historical_key(r) for r in f['record_keys']}=={historical_key(r) for r in f['integrated_record_keys']}==oldkeys|keys
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
    section='## V8127: Rafael B49 North Sea confrontation integrated in cumulative V8122; full review continues\n\n'+summary+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name;prefix=('# Current editorial handoff - V8127; V8122 current\n\n' if name=='editorial_handoff_current.md' else '')+section
        targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
    files=[]
    for i,(path,data) in enumerate(targets.items()):
        planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
        if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
        files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
    save(ROOT/'staged_completion.json',dict(files=files,evidence=evidence,all61_records_integrated_once=True,no_shared_mutation_yet=True,full_goal_complete=False))
    print('Six completion targets staged:61 disjoint Rafael decisions/31 revisions/30 retentions.Deep inverse audit next.')

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
                deep_inverse_recovers_every_prior_root_family_record_counter_andcandidate=True,exactly61_disjoint_new_records=True,
                all_six_before_andplanned_hashes_verified=True,full_goal_complete=False))
            print('Deep inverse audit passes;every prior root/family/record/count/history value recovers exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes())
            for entry in plan['files']:assert Path(entry['target']).is_relative_to(Path.cwd().resolve()) and Path(entry['planned']).is_relative_to(ROOT.resolve())
            for entry in plan['files']:
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,exactly61_decisions_credited_once=True,
                current=release['candidate'],mainV4701_preserved=True,full_goal_complete=False))
            print('Six audited completion targets applied;7143 completed/4442 revisions/2701 retentions,currentV8122.Full goal active.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();VERIFY.mkdir(parents=True)
            completed={historical_key(r) for f in new['completed_editorial_families'] for r in f['records']}
            assert len(completed)==7143 and new['current_integrated_candidate']['sha256']==release['candidate_sha256']
            verified=dict(candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],
                patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
                ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                records_editorially_completed=7143,records_with_source_and_prose_pass=7146,records_with_source_prose_drafts=7146,
                records_revised_and_integrated=4442,retained_wordings_editorially_completed=2701,
                completed=7143,source_prose=7146,revised=4442,retained=2701,SC0=340,SC1=91,SC2=4915,SC3=197,
                reviewed_routes=5543,completed_routes=5543,manifest_batches=638,accepted_layers=114,release_checks=18,regressions=110,
                Rafael_B49_completed_once=True,Rafael_B49_policy_atomic_registered_integration_pending=False,
                final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),actual_unique_pages_both_languages=100,
                actual_speech_occurrences=100,actual_complete_body_andheader_holds=318,native_only_object_IDs=UNVISITED,
                strict_own_Rafael_current_input=read(START)['current_native_input'],next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch='Rafael_SC0B50_source_gloss_pending_controls_current_andrelease_v8127',next_clean_exchange_not_selected=False,
                full_goal_active=True,full_goal_complete=False,all_current_andearlier_limits_preserved=True,
                producer_sha256=sha(Path(__file__).read_bytes()))
            save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV8128/currentV8122:7143completed/7146source-prose/4442revisions/2701retentions;61credited once.Full objective active.')
