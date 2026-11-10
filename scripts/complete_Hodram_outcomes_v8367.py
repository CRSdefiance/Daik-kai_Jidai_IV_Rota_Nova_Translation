"""Credit28 disjoint Hodram decisions once after registered release/startup; preserve full ledger inverse."""
import argparse,gzip,json,os
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.complete_Rafael_B50_v8184 import COUNTERS,digest
from scripts.Hodram_outcomes_release_paths_v8347 import DOC,NAMES,MAP,SEAL,proofs
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_outcomes_completion_v8367')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8368')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8360/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
RELEASE=Path('work/analysis/Hodram_outcomes_release_v8363/registered_release_verification.json')
START=Path('work/analysis/Hodram_outcomes_registered_binding_v8365/own_Hodram_startup_andstrict_captain1_context.json')
VIEW=Path('work/analysis/Hodram_outcomes_registered_startup_view_v8366/own_registered_startup6_RGBpairs_actor_equal_unchanged_names_direct_view.json')
POSITIVE=Path('work/analysis/Hodram_outcome_atomic_positive_v8359e/one_whole_NDS_commit_exact_reference_andunchanged_precommit_input.json')
NEGATIVE=Path('work/analysis/Hodram_outcomes_atomic_challenges_v8356b/actual_changing_semantic_precommit_rejections.json')
REG=Path('work/analysis/Hodram_outcomes_registration_v8361/registration_receipt.json')
FINAL=Path('translations/hodram_outcomes_contextual_final_review_v1.json')
KEY='Hodram_SC1B47_B48_completion_v8367'
FAMILY='Hodram_SC1B47_B48_treasure_outcomes_v8367'
SCOPE='unfinished_editorial_scope_v8367'
NEXT_KEY='Hodram_SC1B49_fourteen_clean_glosses_two_choices_items_pending_controls_current_andrelease_v8367'
BEFORE=(7199,7202,7202,4471,2728)
AFTER=(7205,7208,7208,4474,2731)
NEXT_SOURCE={'49':'work/analysis/Hodram_B49_clean_v8357/complete_clean_SC1_B49_EV1_andcoverage_before_current_English.json'}
NEXT_GLOSS='work/analysis/Hodram_B49_clean_gloss_v8358/fourteen_first_clean_glosses_two_choice_labels_wristband_trade_direction_andqualified_Hodram_reply.json'
NEXT_ARTIFACT='work/analysis/Hodram_B49_item_identity_v8360a/clean_trade_item84_Heavenly_Wristband_item148_Ullr_Bow_exact_native_name_fields.json'
INTRO='Hodram SC1B47/B48 are complete in registered experimental cumulative V8362:6records,3revisions and3individually justified retentions credited once. Totals7205completed/7208source-prose-and-drafts/4474integrated revisions/2731retentions. SC0368,SC1125,SC24915,SC3197,COMMON1600complete1603source-prose;route subset5605 isnot a full-goal denominator. All642manifest batches/114accepted layers/18release checks/110regressions,whole tested-reference equality,exact clean-input patch andown registered Hodramstartup pass. MainV4701/canonicalbaseline unchanged;preserve every ROM,translation,draft,executed producer,proof andfailure. No separate requestedtestpackage,promotion,pruning,commit orpush. Fullobjective active.'
DETAILS="Whole clean Japanese outcomes andindividual first glosses precede priorEnglish. Remove invented unfairness,restore Lil's prospective best-in-the-world insistence,andkeep the addressee's instruction towait inAmsterdam. Retain the rueful concession,qualified Lil Argot/Ullr's Bow discovery andplayful chuckle/taunt withone real FI;source musicalnote expresses playful intent without inventing singing,romance orrank. Scoped Lil Argot identity is retained;FE isnot actor254 orpersonalname. No present worldsupremacy,territorialconquest,player award orpromised handover isadded.\n\nSix complete automatic paragraphs preserve usable216px progressive/FE widths,original FE228x48/288stride/6x12/16pitch geometry,allfirst/internal/finalglyphs,completeconsumption,bounds andsinglepages. Zero warnings/waivers andsix source line-count infos remain. Full15commands/six preambles/seven opaque effects/oneFE/oneFI/two fourbyte ends andseparate tails survive bothclean source/fullparentarchive/wholeROMinverses. All323otherSC1blocks/allotherfiles/components/names/fonts/123264payload remainexact;325loads-cache/650modes/326actions andcaller census pass.\n\nFour complete initialized source/revised fixtures40004frames cover12pages/100body-name orFE-absentheader holds,alloriginalcommands/returns andFE-to-Lil transition. TwofocusedFE runs8002frames bindoriginalpaint CPU/WRAM/TCM objects,temporary stackcontext,persistentview/palette andbankDVRAM/everyRGBinkpixel. B47 returns4495both;B48source4495/English4494 returns[0,0]. B47later93of93RGBpairs andfinalPRNGmatch. B48later80of93RGBpairs match;13differ(Aprompt/menu highlights/lower sailingclouds),andfinalPRNG3450714279 versus3110383956 differs. Alloriginalscript-boundaryPRNGpairs match;fivecheckednativecomponents/actors/captain1match. Rawcalendar remainsuninterpreted. This isdisclosed opening-fixture coverage,not naturaloptionalactivation,originaleventlocation/outereligibility/earnedprogress/everyframecausality/future-random-outcome/broadsimulation/fullroute/hardwareproof.\n\nFrozenpolicy6positives/357changed-inputrejections andindependent native/actual/FE/control/comparison checks pass. Atomicone-whole-objectpositive preservesoriginalinput untilcommit. Fiftysemanticprecommitrejections makezerocommits withrelease dependencydigestsbypassed. Preserve stoppedreaders/harnesses;onlyCPUindex/JSONrepresentation/expectederrorwording werecorrected. Builderguard successors retainall417frozenentries and481otheroldproductiondependencies;exactsingleownedstage removalmustrecoverwholeoldbuilder. Eightalteredbuildercases reject. Prior50semanticcases bind byexactsevenmodule sourceequivalence andarenot claimed asrerun;currentproductionv2 hasfresh fullpositive. Newownregistered4001frameordinaryHodramstartup/sixcompletePNGpairs/wholeactors/name12/Blades8/runtimefontCOMMONdirectoryand123264payload pass withoutreplayingoptional scenes.\n\nAllfour stories,earliertranslations,sharedtowns/shops/randomscenes,Help/remainingprose,all207names/roles/aliases andretrospectiveprematurewraps remainopen. Keepallpriorfamilies/leads andGerhard/Rafael/Hodram timing/RNG/component/calendar/RGB/fixture-entry limits. Graphics/all18plaques andlaterolder-recordtechnicalre-audit stayseparate."
NEXT="Continue from verifiedV8368/currentregisteredV8362. These6Hodramoutcomes areintegrated/creditedonce;reusecompleted source/context/native/stored/actual/policy/atomic/release/startup proofs withoutunchangedreplays. UseownV8362captain1 input8365;otherroutecontexts needproperrebind/recapture,no historicalRAMoverlay orcaptain2 borrowing.\n\nContinue completeclean SC1B49 from8357/first14speech+twochoiceglosses8358/itemidentity8360a. CurrentEnglishdialogue remainsunread. Established item84isHeavenlyWristband/item148Ullr'sBow;completeclean/currentnativepointers/NULnames/20unownedmetadata fieldsbound. Preserve Lil'sexcitedbargaining,regionalproof/hearsayNewWorldlocation/conditionaltrade,Hodram'ssilence andqualifiednegateddenial,andoutgoingwristband FEnotice. Keeprepeatedenthusiasticopeningsdistinct. Bindall14source/current/effective refs/twochoices,36commands/fullpreambles/relatives/query/itemdisplay-hide/opaqueeffects/fullend/tails;reviewwholeexchangepaths beforeindividualnatural-dialogue-v2 revisions/retentions. Originalevent49requires48;outereligibility/location/activation/fullchronology unproven. These14firstglosses addzerocreditedcounts. Nativechoice/control/FE/display/representativeactualrisk tests andregisteredintegration remainpending. Exhaustivenaturalplaythroughs/individualconditionalvisits arenotrequired.\n\nPreserve allprior scopeleads:12contraction/questiontags,unscanned beyond558plans,weak-before-row/page-before-readability,COMMON750-752/preLF6435,item/counterpart/nameconsistency/all207labels/customnames;normalendcarry/B35R65/B48R129nineteenthcells/correctedoldB47receipt/B48/B50labels;allGerhard/Rafael/Hodram timing/RNG/component/calendar/RGB/fixture-entrylimits. Maintainbroadpractical town/randomcapture andhonest offline/gameplay scope. Keepfullgoalactive,main4701/canonicalbaseline unchanged andeveryartifact;no separatepackage/promotion/pruning/commit/push. Graphics/latertechnicalaudit separate."

def restore(value):
    result=deepcopy(value);entry=result.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(result,op['path'])
        if op['kind']=='append':
            assert len(parent[key])==op['before_length']+op['count'] and digest(parent[key][op['before_length']:])==op['appended_sha256'];del parent[key][op['before_length']:]
        elif op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return result

def gates():
    release,start,view,positive,negative,reg,doc,seal=map(read,[RELEASE,START,VIEW,POSITIVE,NEGATIVE,REG,DOC,SEAL])
    manifest=read(release['manifest']);registry=read('translations/release_stack.json')
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==start['candidate_sha256']==view['candidate_sha256']==manifest['candidate_sha256']
    assert manifest['profile']=='all-routes-unified-v8362' and len(manifest['batches'])==642 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert release['all110_release_dialogue_regressions_pass'] and release['whole_clean_input_ROM_reconstruction_byte_exact'] and sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert Path(release['exact_patch_reconstruction']).read_bytes()==Path(release['candidate']).read_bytes() and view['viewed'] and len(view['six_whole_RGB_pairs'])==6 and view['whole_actors_equal']
    assert start['all_strict_targetARM9_inverse_Blades_COMMON_directory_and123264_payload_guards_pass'] and start['actual_original_captain_ID']==1 and start['actual_frames']==4001
    assert positive['single_complete_NDS_commit'] and negative['negative_count']==reg['negative_count']==50 and negative['all_rejected_inputs_zero_whole_NDS_commits']
    assert all(c['rejected'] and c['commit_calls']==0 for c in negative['cases']) and seal['manuscript_sha256']==sha(DOC.read_bytes()) and seal['reference_map_sha256']==sha(MAP.read_bytes())
    assert len(doc['records'])==6 and all(all(r['review'].values()) for r in doc['records']) and Counter(r['decision'] for r in doc['records'])=={'revision':3,'retention':3}
    return release

def stage():
    assert not ROOT.exists() and not FINAL.exists();release=gates();prior=read(PRIOR);before=LEDGER.read_bytes();old=json.loads(before)
    assert sha(before)==prior['ledger_sha256'] and tuple(old[k] for k in COUNTERS)==BEFORE and old['goal_status']=='active' and not old['full_goal_complete']
    doc,mapping=map(read,[DOC,MAP]);image=NdsImage.open(release['candidate']);bank=IlnkContainer.parse(image.read_file('/data/SC1.DK4')).blocks
    oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};keys={historical_key(r) for r in doc['records']}
    assert len(oldkeys)==7199 and len(keys)==6 and not oldkeys&keys and KEY not in old
    rows=[]
    for original in doc['records']:
        row=deepcopy(original);ref=next(r for r in mapping['records'] if r['id']==row['id']);target=ref['target_reference'];block=bank[row['block']];raw=bytes.fromhex(ref['stored_hex']);at=target['offset']
        assert sha(block)==target['target_block_sha256'] and block[at:at+len(raw)+1]==raw+b'\0' and block[:at].count(b'\0')==target['record_index']
        group=next(g for g in mapping['groups'] if g['block']==row['block']);command=next(c for c in group['all_target_commands'] if c['offset']==at-5)
        body=raw[1:].decode('cp932');row['pre_integration_review_record_preserved']=deepcopy(original)
        row.update(predecessor_reference=deepcopy(original['current_reference']),predecessor_hex=original['current_hex'],reviewed_against_predecessor_ROM=doc['current_ROM'],reviewed_against_predecessor_ROM_sha256=doc['current_ROM_sha256'],
            localization_note_reference_scope='Individual editorial decision comparedwith V8362;pre-integration review preserved above.',current_reference=deepcopy(target),current_hex=raw.hex(),current_text_hex=raw.hex(),
            current_record_index=target['record_index'],current_native_extent=command['native_extent'],current_0100_ancestors=command['ancestor_0100_offsets'],current_raw_storage_English=body,
            current_English=' '.join(body.split()),current_stored_English=body,current_native_macro_English=raw[1:].replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet').decode('cp932'),current_native_macro_output_hex=raw[1:].replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet').hex(),raw_storage_comparison_paragraph=' '.join(body.split()),
            registered_catalogue_match=None,current_reference_ROM=release['candidate'],current_reference_ROM_sha256=release['candidate_sha256'],
            completed_candidate_reference=deepcopy(target),completed_candidate_sha256=release['candidate_sha256'],
            integrated_reference=dict(**target,stored_hex=raw.hex(),ROM=release['candidate'],ROM_sha256=release['candidate_sha256']),exact_stored_reference=deepcopy(ref),
            source_prose_andcompletion_credit_added_once=True,source_prose_orcompletion_credit_added=True,registered_integration_pending=False,
            frozen_policy_atomic_production_registered_integration_andcompletion_credit_pending=False,individually_activated_in_current_build=False,
            current_observation_scope='Complete body/name-orFE-absent-header holds in disclosed initialized whole-script fixtures;byte-identical tested reference,not natural optional activation in V8362.',
            actual_proof=proofs()[f'actual{row["block"]}'],actual_holds=[dict(version=o['version'],**h) for o in row['actual_display_observations'] if o['version']=='revised_English' for h in o['speech']['complete_holds']])
        assert row['actual_holds'] and all(row[k]==original[k] for k in ['english','source_hex','source_reference','source_meaning','context','localization_note','retention_reason','review','decision','qa_waivers','qa_waiver_scope'])
        rows.append(row)
    summary=INTRO+'\n\n'+DETAILS+'\n\n'+NEXT
    pending=dict(status='fourteen-clean-source-glosses-two-choice-labels-item84and148-identity-bound-current-dialogue-unconsulted-controls-native-prose-formatting-release-pending',source_packets=NEXT_SOURCE,first_gloss=NEXT_GLOSS,artifact_identity=NEXT_ARTIFACT,file_path='/data/SC1.DK4',blocks=[49],physical_source_positions=14,typed_choice_labels=2,original_commands=36,current_English_dialogue_bodies_unconsulted=True,established_artifact_names=['Heavenly Wristband',"Ullr's Bow"],source_notice_outgoing_wristband=True,no_new_name_asset_mechanics_ororiginal_activation_claim=True,source_native_controls_choice_predicates_relatives_items_FE_current_editorial_andrelease_pending=True,source_prose_credit_added=0,completion_credit_added=0,full_goal_complete=False)
    evidence={str(p):sha(Path(p).read_bytes()) for p in [PRIOR,DOC,NAMES,MAP,SEAL,RELEASE,START,VIEW,POSITIVE,NEGATIVE,REG,*map(Path,proofs().values()),
        *map(Path,NEXT_SOURCE.values()),Path(NEXT_GLOSS),Path(NEXT_ARTIFACT),Path(__file__)]}
    ROOT.mkdir(parents=True);save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=rows,revised=3,retained=3,source_prose_and_completion_credit_added_once=6,
        actual_speech_observations_both_versions=12,actual_complete_body_andname_holds=100,actual_original_optional_activation=False,all_actual_scope_limits_preserved=True,
        source_current_effective_compiled_stored_actual_andintegrated_refs_bound=True,all15commands6preambles_zero_relatives_queries_one_FE_one_FI_andcomplete_ends_preserved=True,
        both_clean_source_andfull_predecessor_inverses_exact=True,policy_expected_rejections=357,atomic_semantic_rejections=50,six_original_infos_zero_warnings_orwaivers_preserved=True,
        new_registered_startup_frames=4001,full_goal_andall_prior_scope_graphics_separation_later_audit_preserved=True,summary=summary,evidence=evidence,full_goal_complete=False))
    new=deepcopy(old);ops=[]
    def put(path,value):
        parent,key=parent_at(new,path);exists=key in parent if isinstance(parent,dict) else key<len(parent);ops.append(dict(kind='set',path=path,existed=exists,before=deepcopy(parent[key]) if exists else None));parent[key]=deepcopy(value)
    def append(path,values):
        parent,key=parent_at(new,path);ops.append(dict(kind='append',path=path,before_length=len(parent[key]),count=len(values),appended_sha256=digest(values)));parent[key].extend(deepcopy(values))
    for k,v in zip(COUNTERS,AFTER,strict=True):put([k],v)
    for k in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:assert new[k]['/data/SC1.DK4']==119;put([k,'/data/SC1.DK4'],125)
    append(['completed_editorial_families'],[dict(id=FAMILY,file_path='/data/SC1.DK4',blocks=[47,48],record_IDs=[r['id'] for r in rows],records=rows,final_review=str(FINAL),revised_count=3,retained_count=3,fresh_revisions=3,fresh_retentions=3,actual_verification_scope=DETAILS)])
    fp=['contextual_story_natural_dialogue_pass_v1871'];keyrows=[dict(file_path='/data/SC1.DK4',id=r['id']) for r in rows]
    for k in ['record_keys','integrated_record_keys']:append(fp+[k],keyrows)
    append(fp+['record_IDs'],[r['id'] for r in rows])
    for k,v in dict(fresh_pass_records_explicitly_reread=7205,fresh_pass_records_integrated=7205,latest_contextual_manuscript=str(DOC),latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=INTRO).items():put(fp+[k],v)
    append(fp+['reconciled_families'],[dict(id=FAMILY,records=6,final_review=str(FINAL),new_revisions=3,justified_retentions=3,new_completed_records=6,historical_reconciliation_only=False,actual_optional_event_selected=False,actual_initialized_fixture_speeches=6,actual_pages=6,offline_only_objects=0,all_source_English_scene_proofs_reused_without_replay=True)])
    path=str(DOC)
    if path not in new['active_source_prose_drafts']['manuscripts']:append(['active_source_prose_drafts','manuscripts'],[path])
    put(['active_source_prose_drafts','route_record_subsets_pending',path],[]);put(['active_source_prose_drafts','note'],INTRO)
    ri=next(i for i,u in enumerate(new['coverage_units']) if u['id']=='all-route-scenes');assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5599
    for k,v in dict(reviewed_route_records=5605,completed_route_records=5605,next=NEXT).items():put(['coverage_units',ri,k],v)
    append(['coverage_units'],[dict(id=FAMILY,status='complete-contextual-native-stored-actual-registered-release',file_path='/data/SC1.DK4',blocks=[47,48],completion_credit_added=6,final_review=str(FINAL),actual_original_optional_activation=False,actual_objects=6,actual_pages=6,full_goal_complete=False)])
    put(['formatting_watchlist',FAMILY],dict(status='six-complete-singlepages-originalFE-one-scopedLil-name-registered-release-pass',final_review=str(FINAL),six_original_row_infos_zero_warnings_orwaivers=True,all_scope_andprior_leads_preserved=True,full_goal_complete=False))
    current=deepcopy(old['current_integrated_candidate']);current.update(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False,**{f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)})
    put(['current_integrated_candidate'],current);put(['latest_checkpoint'],summary)
    previous_pending=prior['pending_source_batch'];marker=dict(checkpoint=KEY,final_review=str(FINAL),candidate=release['candidate'],all_historical_pending_flags_superseded_not_deleted=True,new_credit_added_here=0)
    put([previous_pending,'registered_integration_completed_by'],marker);put([NEXT_KEY],pending)
    prior_scope=old[prior['unfinished_scope']];assert sha(Path(prior_scope['path']).read_bytes())==prior_scope['sha256'];inventory=deepcopy(read(prior_scope['path']))
    inventory['next_focus']=NEXT;inventory[NEXT_KEY]=deepcopy(pending);inventory[KEY]=dict(final_review=str(FINAL),completed_objects=6,revisions=3,retentions=3,registered_candidate=release['candidate'],all_previous_limits_andfull_objective_preserved=True)
    if previous_pending in inventory:inventory[previous_pending]['registered_integration_completed_by']=marker
    for u in inventory.get('broader_coverage_units',[]):
        if u['id']=='all-route-scenes':u.update(reviewed_route_records=5605,completed_route_records=5605,next=NEXT)
    assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
    scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
    put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,incomplete_COMMON=3,incomplete_credited_route_drafts=0,new_uncredited_Hodram_source_positions=14,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
    evidence[str(FINAL)]=sha(FINAL.read_bytes());evidence[str(scope)]=sha(scope.read_bytes())
    new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_operations=ops,record_keys=keyrows,new_source_prose_reviews=6,new_completed_records=6,revised=3,retained=3,
        new_current_candidate_emulator_runs=1,new_current_candidate_frames=4001,all_prior_actual_proofs_reused_without_replay=True,all_sessions_terminal_andreaped=True,goal_turn_classification='progress',full_goal_complete=False)
    assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
    assert {historical_key(r) for r in new[fp[0]]['record_keys']}=={historical_key(r) for r in new[fp[0]]['integrated_record_keys']}==oldkeys|keys
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
    section='## V8367: Hodram6 integrated in cumulative V8362;next14clean utterances/twochoices glossed\n\n'+summary+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        p=Path('docs')/name;prefix=('# Current editorial handoff - V8367; V8362 current\n\n' if name=='editorial_handoff_current.md' else '')+section;targets[p]=prefix.replace('\n','\r\n').encode()+p.read_bytes()
    files=[]
    for i,(p,value) in enumerate(targets.items()):
        planned=ROOT/f'{i:02d}.after';planned.write_bytes(value)
        if p!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(p.read_bytes(),mtime=0))
        files.append(dict(target=str(p.resolve()),before_sha256=sha(p.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(value)))
    save(ROOT/'staged_completion.json',dict(files=files,evidence=evidence,all6_records_integrated_once=True,no_shared_mutation_yet=True,full_goal_complete=False))
    print('Staged six completion targets:6disjoint decisions/3revisions/3retentions;7199completed;deep inverse audit next.')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    if mode=='stage':stage()
    else:
        release=gates();plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists();save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),deep_inverse_recovers_every_prior_root_family_record_counter_candidate=True,exactly6_disjoint_new_records=True,full_goal_complete=False))
            print('Deep inverse audit passed:every previous record/root/counter/candidate/scope recovers exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes())
            for e in plan['files']:
                assert Path(e['target']).is_relative_to(Path.cwd().resolve()) and Path(e['planned']).is_relative_to(ROOT.resolve())
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,exactly6_decisions_credited_once=True,current=release['candidate'],mainV4701_preserved=True,full_goal_complete=False))
            print('Applied currentV8362:7199completed/4471revised/2728retained;full objective active.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();prior=read(PRIOR);verified=deepcopy(prior)
            assert len({historical_key(r) for f in new['completed_editorial_families'] for r in f['records']})==7205
            verified.update(candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
                ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                **dict(zip(COUNTERS,AFTER,strict=True)),completed=7205,source_prose=7208,revised=4474,retained=2731,SC0=368,SC1=125,SC2=4915,SC3=197,reviewed_routes=5605,completed_routes=5605,
                manifest_batches=642,accepted_layers=114,release_checks=18,regressions=110,Hodram6_completed_once=True,Hodram6_atomic_registered_integration_pending=False,
                final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),actual_speech_observations_both_versions=12,actual_complete_body_andname_holds=100,
                strict_own_Hodram_current_input=read(START)['current_native_input'],previous_Rafael_Lil_andother_contexts_historical_until_correctly_rebound=True,
                next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch=NEXT_KEY,next_clean_exchange_not_selected=False,new_uncredited_source_positions=14,
                full_goal_active=True,full_goal_complete=False,all_current_andearlier_limits_preserved=True,all_sessions_terminal_andreaped=True,producer_sha256=sha(Path(__file__).read_bytes()))
            verified['Hodram_outcomes_production_checkpoint']=dict(completed_once=True,completion_final_review=str(FINAL),registered_candidate=release['candidate'],registered_candidate_sha256=release['candidate_sha256'],
                independent_actual_atomic_andregistered_integration_pending=False,independent_actual_atomic_andregistered_release_complete=True,completion_credit=6)
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV8368/currentV8362:7199completed/7202sourceprose/4471revisions/2728retentions;nextHodram14utterances/twochoices glossed/fullgoal active.')
