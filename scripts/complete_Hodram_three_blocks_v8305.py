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
from scripts.Hodram_three_blocks_release_paths_v8290 import DOC,NAMES,MAP,SEAL,proofs
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_three_blocks_completion_v8305')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8306')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8292/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
RELEASE=Path('work/analysis/Hodram_three_blocks_release_v8301/registered_release_verification.json')
START=Path('work/analysis/Hodram_registered_binding_v8303/own_Hodram_startup_andstrict_captain1_context.json')
VIEW=Path('work/analysis/Hodram_registered_startup_view_v8304/own_registered_startup6_RGBpairs_actor_equal_unchanged_names_direct_view.json')
POSITIVE=Path('work/analysis/Hodram_atomic_positive_v8297b/one_whole_NDS_commit_exact_reference_andunchanged_precommit_input.json')
NEGATIVE=Path('work/analysis/Hodram_atomic_challenges_v8298/actual_changing_semantic_precommit_rejections.json')
REG=Path('work/analysis/Hodram_three_blocks_registration_v8299/registration_receipt.json')
FINAL=Path('translations/hodram_three_blocks_contextual_final_review_v1.json')
KEY='Hodram_SC1B137_B45_B46_completion_v8305'
FAMILY='Hodram_SC1B137_B45_B46_apology_staffing_treasure_challenge_v8305'
SCOPE='unfinished_editorial_scope_v8305'
NEXT_KEY='Hodram_SC1B47_B48_six_clean_glosses_artifact148_pending_source_controls_current_andrelease_v8305'
BEFORE=(7171,7174,7174,4455,2716)
AFTER=(7199,7202,7202,4471,2728)
NEXT_SOURCE={
    '47':'work/analysis/Hodram_B47_clean_v8310/complete_clean_SC1_B47_EV1_andcoverage_before_current_English.json',
    '48':'work/analysis/Hodram_B48_clean_v8311/complete_clean_SC1_B48_EV1_andcoverage_before_current_English.json'}
NEXT_GLOSS='work/analysis/Hodram_B47_B48_clean_gloss_v8312/six_first_clean_glosses_both_race_outcomes_FE_FI_andAmsterdam_wait_direction.json'
NEXT_ARTIFACT='work/analysis/Hodram_B48_artifact_identity_v8313/clean_notice_anditem148_established_Ullr_Bow_identity_not_current_dialogue_review.json'
INTRO="""Hodram SC1B137/B45/B46 are complete in registered experimental cumulative V8300:28speeches,16revisions and12individually justified retentions credited once. Totals7199completed/7202source-prose-and-drafts/4471integrated revisions/2728retentions. Perfile:SC0368,SC1119,SC24915,SC3197,COMMON1600complete1603source-prose;route subset5599 isnot a full-goal denominator. All641manifest batches/114accepted layers/18release checks/110regressions,full tested-reference equality,exactclean-input patch andown registered Hodramstartup pass. MainV4701/canonical baseline unchanged;no separate requested testpackage,promotion,pruning,commit orpush. Every ROM,translation,draft,executed producer,proof andfailure remains. Full objective stays active."""
DETAILS="""All28 clean-source whole-exchange decisions and27prior B44 callbacks preserve meaning,facts,voices andemotional progression. Camille's hesitant apology/modesty,Charles's bluntness,Hodram's courteous restraint,Gerhard's maritime-trade/capable-people/possible recruitment advice andLil's reported regional wealth/serious treasure race remain. Correct Duel tocontest,richestcaptain toreported richestperson inthese waters,revealsamap tokeyfordeciphering atreasuremap;treasure istherace object. Preserve Lisbon/Seville andmight,no guaranteed recruitment,newkinship/rank/romance,mapgift,accepted orwoncontest. Three silences remain literal. All individual reasons andearlier translations preserved. Six scoped name retentions include approved Hodram/Joakim/Camille andregistered Gerhard Adernkatz;wider207/catalogue/customnames andPortWorker7 stayopen.

Full216px/four-row automaticHodram layout usesdefault FI6/FA9/FO15 andsourcezeroFI/FA/FO. Source01/02/09/10/12/71,complete sixbyte preambles,bodyNUL/phase/guards andfonts remain. Eleven stored parity tails have44fresh alignments;17exact bodies reuse68. All28 complete single-page planes match viewed nativepages;two narrow weak-boundary exceptions/five infos remain,no manualwrap/shortening/globalrule change. Source B1371240to1384,B4596to84,B46444to480(logical478/tail2). All60commands/eightrelatives/two raw8000 operands/opaque effects/fourbyte terminals preserved;threeclean/predecessorblocks/fullarchive/fullROM inverses pass. Native325load-cachepaths/650parentmodes,three originalEV1blockindex entries andshippedcaller census bind;not allattainable paths ornaturalactivation.

Six paired clean-Japanese/revised-English initialized opening fixtures ran100006frames withsameordinary inputs/readonly observers. OriginaleightHodram initializers34bytes andwhole selectedscripts remain;no runtimeflags/party/roster/role/funds/RNG/conditions/results forcing orinputretiming. All28Japanese+28English pages/all six headers/three silences have262complete body-name holds. All12 actual sheets wereviewed. Original4800descriptor[0,181,1,5]/layout[0,0,0] showsRed Dye/Mystery Item icon/label and4700clears it;different fromRafael4821/4720. NormalreturnsB1378815[0,0],B454016[0,0],B465455[0,1] bothversions. All28upper-scene/portrait/header pairs match;command differences17/1/5 andduration4/0/0 remain. Finalfive component sets/wholeactors/PRNG matchperpair andall532laterfullRGBpairs match. B137fixture laterentersSC0B44/captain0 inbothversions,not normalHodramcontinuity. B45/B46finalcaptain1. These aredisclosed fixtures,not naturaloptional eventactivation/original locations/earnedprogress/fullroute/hardware/everyframe causal/future-outcome/broadsimulation proof. Retain limits forlater older-record audit.

Frozen source/prose/layout/name/actual policy8287b passes28positives/579actual-changing expectedrejections. Independent reconstruction8290 matchesfull8276reference;independent8293-8295 validation recomputes56bodyplanes/six names/all actualtraces/holds/controls/all532RGB/finalnativestates/loader-caller associations. Productionv1 positive ispreserved;v2 additionally rejects contradictory loader/census summaries andwrong proofROMownership. Positivev2 commitsonewholeNDS object onlyafterallgates,leavingthe originalobject byte-exact. All71independent actual-changing semanticcorruptions rejectbeforeanycommit withdependencydigests deliberately bypassed andtrusted frozen/nativeguards preserved. Registry/solebuilder registration followsfullV8259andregisteredAdernkatz dependency. OnlySC1B45/B46/B137 change;322otherblocks/allotherfiles/components/ARM9/Blades8/COMMON/fonts/123264payload remain exact. Freshown registeredcaptain1 coldboot4001frames/sixwholePNGpairs/wholeactors/actualAdernkatz12+Blades8 pass;unchanged12getters/sixnameplanes reuse exactcode/font/actor binding. No oldRAMoverlay orborrowedcaptain2 snapshot.

While releasechecks ran,the next two complete cleanJapanese outcomesB47/B48 were read andsix firstglosses saved beforecurrentEnglish. B47 hasthreeLil utterances;B48 hasoneFE systemnotice/twoLil utterances,oneFI andone♪. Sourceartifact狩猟神ウルの弓矢 bindsitem148/existingcomplete Ullr's Bow throughclean/current pointers andunchanged20nonname metadata bytes. Lil instructsthe addressee towaitinAmsterdam,not thatsheisalreadywaitingthere. Do not invent unfairness,conquest,rank/romance,playeritemacquisition orhandover. B47 excludes48;B48hasno such exclusion;outereligibility/chronologyunproved. These six remainuncredited sourceglosses,not currentEnglish/prose/formatting orname approvals. All earlier sources/drafts/proofs preserved,including metadata/syntax/waiver-schema failures andsuccessors. Graphics/all18plaques andlater technical re-audit stayseparate."""
NEXT="""Continue from verifiedV8306/currentregisteredV8300. Hodram28 are integrated andcredited once;do not repeat their source/native/actual/policy/atomic/release/startup checks withoutnewinput orconcrete risk. Begin nextHodramB47/B48 from sixclean glosses8312,sourcepackets8310/8311 andartifact148identity8313. CurrentEnglish bodies remainunconsulted. Preserve thetwo whole outcomes andB46treasure-race context. Map original61FF versusB48FE/nullactor/nativegeometry,sourceFI/samecaptain1 default lengths and♪,all15sourcecommands/fullends andopaqueeffects/originalEV1entries/outercondition limits;confirm source speaker labels withapproved identities. Thenexactcurrent/effective comparisons,natural-dialogue-v2 contextualprose withindividual revisions/retentions,automatic full-native-width wrapping/nativeglyphs/storedcontrols/representative distinctFE/transition tests andregistered integration. UseowncurrentV8300captain1 input8303;other route snapshots remainhistorical untilcorrectly rebound orrecaptured,no captain2 borrowing. No exhaustive naturalplaythrough orindividualconditional visits required.

Fullgoal remainsallfour stories,earlier translateddialogue,sharedshops/towns/randomscenes,Help/remainingprose,all207names/roles/aliases andretrospectivepremature wraps. Keepallprior unfinishedscope leads:COMMON750-752,12contraction/question-tag leads,unscanned beyond558plans,weak-before-row/page-before-readability concerns,all item/counterpart/name leads,graphics andlater older-record audit. Preserve normalendcarry,B35R65/B48R129source19thcells,corrected B47receipt andB48/B50stale labels,allprevious Gerhard/Rafael/Hodram timing/RNG/components/bytes/calendar/RGB/fixturelimits. Roughly20000lexicalcandidates isnot an exact player-facing remainingcount orpercentage. Preserveall artifacts;main4701unchanged,no separate requestedpackage,promotion,pruning,commit orpush."""

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
    assert manifest['profile']=='all-routes-unified-v8300' and len(manifest['batches'])==641 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert release['all110_release_dialogue_regressions_pass'] and release['whole_clean_input_ROM_reconstruction_byte_exact'] and sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert Path(release['exact_patch_reconstruction']).read_bytes()==Path(release['candidate']).read_bytes() and view['viewed'] and len(view['six_whole_RGB_pairs'])==6 and view['whole_actors_equal']
    assert start['all_strict_targetARM9_inverse_Blades_COMMON_directory_and123264_payload_guards_pass'] and start['actual_original_captain_ID']==1 and start['actual_frames']==4001
    assert positive['single_complete_NDS_commit'] and negative['negative_count']==reg['negative_count']==71 and negative['all_rejected_inputs_zero_whole_NDS_commits']
    assert all(c['rejected'] and c['commit_calls']==0 for c in negative['cases']) and seal['manuscript_sha256']==sha(DOC.read_bytes()) and seal['reference_map_sha256']==sha(MAP.read_bytes())
    assert len(doc['records'])==28 and all(all(r['review'].values()) for r in doc['records']) and Counter(r['decision'] for r in doc['records'])=={'revision':16,'retention':12}
    return release

def stage():
    assert not ROOT.exists() and not FINAL.exists();release=gates();prior=read(PRIOR);before=LEDGER.read_bytes();old=json.loads(before)
    assert sha(before)==prior['ledger_sha256'] and tuple(old[k] for k in COUNTERS)==BEFORE and old['goal_status']=='active' and not old['full_goal_complete']
    doc,mapping=map(read,[DOC,MAP]);image=NdsImage.open(release['candidate']);bank=IlnkContainer.parse(image.read_file('/data/SC1.DK4')).blocks
    oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};keys={historical_key(r) for r in doc['records']}
    assert len(oldkeys)==7171 and len(keys)==28 and not oldkeys&keys and KEY not in old
    rows=[]
    for original in doc['records']:
        row=deepcopy(original);ref=next(r for r in mapping['records'] if r['id']==row['id']);target=ref['target_reference'];block=bank[row['block']];raw=bytes.fromhex(ref['stored_hex']);at=target['offset']
        assert sha(block)==target['target_block_sha256'] and block[at:at+len(raw)+1]==raw+b'\0' and block[:at].count(b'\0')==target['record_index']
        group=next(g for g in mapping['groups'] if g['block']==row['block']);command=next(c for c in group['all_target_commands'] if c['offset']==at-5)
        body=raw[1:].decode('cp932');row['pre_integration_review_record_preserved']=deepcopy(original)
        row.update(predecessor_reference=deepcopy(original['current_reference']),predecessor_hex=original['current_hex'],reviewed_against_predecessor_ROM=doc['current_ROM'],reviewed_against_predecessor_ROM_sha256=doc['current_ROM_sha256'],
            localization_note_reference_scope='Individual editorial decision comparedwith V8259;pre-integration review preserved above.',current_reference=deepcopy(target),current_hex=raw.hex(),current_text_hex=raw.hex(),
            current_record_index=target['record_index'],current_native_extent=command['native_extent'],current_0100_ancestors=command['ancestor_0100_offsets'],current_raw_storage_English=body,
            current_English=' '.join(body.split()),current_stored_English=body,current_native_macro_English=body,current_native_macro_output_hex=raw[1:].hex(),raw_storage_comparison_paragraph=' '.join(body.split()),
            registered_catalogue_match=None,current_reference_ROM=release['candidate'],current_reference_ROM_sha256=release['candidate_sha256'],
            completed_candidate_reference=deepcopy(target),completed_candidate_sha256=release['candidate_sha256'],
            integrated_reference=dict(**target,stored_hex=raw.hex(),ROM=release['candidate'],ROM_sha256=release['candidate_sha256']),exact_stored_reference=deepcopy(ref),
            source_prose_andcompletion_credit_added_once=True,source_prose_orcompletion_credit_added=True,registered_integration_pending=False,
            frozen_policy_atomic_production_registered_integration_andcompletion_credit_pending=False,individually_activated_in_current_build=False,
            current_observation_scope='Complete body/name holds in disclosed initialized whole-script fixtures;byte-identical tested reference,not natural optional activation in V8300.',
            actual_proof=proofs()[f'actual_B{row["block"]}'],actual_holds=[dict(version=o['version'],**h) for o in row['actual_display_observations'] if o['version']=='revised_English' for h in o['speech']['complete_holds']])
        assert row['actual_holds'] and all(row[k]==original[k] for k in ['english','source_hex','source_reference','source_meaning','context','localization_note','retention_reason','review','decision','qa_waivers','qa_waiver_scope'])
        rows.append(row)
    summary=INTRO+'\n\n'+DETAILS+'\n\n'+NEXT
    pending=dict(status='six-clean-source-glosses-item148-identity-bound-current-dialogue-unconsulted-native-context-prose-formatting-release-pending',source_packets=NEXT_SOURCE,first_gloss=NEXT_GLOSS,artifact_identity=NEXT_ARTIFACT,
        file_path='/data/SC1.DK4',blocks=[47,48],physical_source_positions=6,source_selectors={'47':[2,2,2],'48':[254,2,2]},source_macro_counts=dict(FI=1,FA=0,FO=0),source_musical_notes=1,
        current_English_dialogue_bodies_unconsulted=True,established_artifact_name="Ullr's Bow",no_new_name_asset_orplayer_acquisition_claim=True,
        source_native_controls_original_entries_FE_geometry_FI_music_note_current_editorial_andrelease_pending=True,source_prose_credit_added=0,completion_credit_added=0,full_goal_complete=False)
    evidence={str(p):sha(Path(p).read_bytes()) for p in [PRIOR,DOC,NAMES,MAP,SEAL,RELEASE,START,VIEW,POSITIVE,NEGATIVE,REG,*map(Path,proofs().values()),
        *map(Path,NEXT_SOURCE.values()),Path(NEXT_GLOSS),Path(NEXT_ARTIFACT),Path(__file__)]}
    ROOT.mkdir(parents=True);save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=rows,revised=16,retained=12,source_prose_and_completion_credit_added_once=28,
        actual_speech_observations_both_versions=56,actual_complete_body_andname_holds=262,actual_original_optional_activation=False,all_actual_scope_limits_preserved=True,
        source_current_effective_compiled_stored_actual_andintegrated_refs_bound=True,all60commands28preambles8relatives2queries_4800layout0_4700_andcomplete_ends_preserved=True,
        all_three_clean_source_andfull_predecessor_inverses_exact=True,policy_expected_rejections=579,atomic_semantic_rejections=71,original_five_infos_two_exact_warning_waivers_preserved=True,
        new_registered_startup_frames=4001,full_goal_andall_prior_scope_graphics_separation_later_audit_preserved=True,summary=summary,evidence=evidence,full_goal_complete=False))
    new=deepcopy(old);ops=[]
    def put(path,value):
        parent,key=parent_at(new,path);exists=key in parent if isinstance(parent,dict) else key<len(parent);ops.append(dict(kind='set',path=path,existed=exists,before=deepcopy(parent[key]) if exists else None));parent[key]=deepcopy(value)
    def append(path,values):
        parent,key=parent_at(new,path);ops.append(dict(kind='append',path=path,before_length=len(parent[key]),count=len(values),appended_sha256=digest(values)));parent[key].extend(deepcopy(values))
    for k,v in zip(COUNTERS,AFTER,strict=True):put([k],v)
    for k in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:assert new[k]['/data/SC1.DK4']==91;put([k,'/data/SC1.DK4'],119)
    append(['completed_editorial_families'],[dict(id=FAMILY,file_path='/data/SC1.DK4',blocks=[137,45,46],record_IDs=[r['id'] for r in rows],records=rows,final_review=str(FINAL),revised_count=16,retained_count=12,fresh_revisions=16,fresh_retentions=12,actual_verification_scope=DETAILS)])
    fp=['contextual_story_natural_dialogue_pass_v1871'];keyrows=[dict(file_path='/data/SC1.DK4',id=r['id']) for r in rows]
    for k in ['record_keys','integrated_record_keys']:append(fp+[k],keyrows)
    append(fp+['record_IDs'],[r['id'] for r in rows])
    for k,v in dict(fresh_pass_records_explicitly_reread=7199,fresh_pass_records_integrated=7199,latest_contextual_manuscript=str(DOC),latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=INTRO).items():put(fp+[k],v)
    append(fp+['reconciled_families'],[dict(id=FAMILY,records=28,final_review=str(FINAL),new_revisions=16,justified_retentions=12,new_completed_records=28,historical_reconciliation_only=False,actual_optional_event_selected=False,actual_initialized_fixture_speeches=28,actual_pages=28,offline_only_objects=0,all_source_English_scene_proofs_reused_without_replay=True)])
    path=str(DOC)
    if path not in new['active_source_prose_drafts']['manuscripts']:append(['active_source_prose_drafts','manuscripts'],[path])
    put(['active_source_prose_drafts','route_record_subsets_pending',path],[]);put(['active_source_prose_drafts','note'],INTRO)
    ri=next(i for i,u in enumerate(new['coverage_units']) if u['id']=='all-route-scenes');assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5571
    for k,v in dict(reviewed_route_records=5599,completed_route_records=5599,next=NEXT).items():put(['coverage_units',ri,k],v)
    append(['coverage_units'],[dict(id=FAMILY,status='complete-contextual-native-stored-actual-registered-release',file_path='/data/SC1.DK4',blocks=[137,45,46],completion_credit_added=28,final_review=str(FINAL),actual_original_optional_activation=False,actual_objects=28,actual_pages=28,full_goal_complete=False)])
    put(['formatting_watchlist',FAMILY],dict(status='28complete-singlepages-six-scopednames-registered-release-pass',final_review=str(FINAL),row_infos5_two_exact_warning_waivers=True,all_scope_andprior_leads_preserved=True,full_goal_complete=False))
    current=deepcopy(old['current_integrated_candidate']);current.update(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False,**{f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)})
    put(['current_integrated_candidate'],current);put(['latest_checkpoint'],summary)
    previous_pending=prior['pending_source_batch'];marker=dict(checkpoint=KEY,final_review=str(FINAL),candidate=release['candidate'],all_historical_pending_flags_superseded_not_deleted=True,new_credit_added_here=0)
    put([previous_pending,'registered_integration_completed_by'],marker);put([NEXT_KEY],pending)
    prior_scope=old[prior['unfinished_scope']];assert sha(Path(prior_scope['path']).read_bytes())==prior_scope['sha256'];inventory=deepcopy(read(prior_scope['path']))
    inventory['next_focus']=NEXT;inventory[NEXT_KEY]=deepcopy(pending);inventory[KEY]=dict(final_review=str(FINAL),completed_objects=28,revisions=16,retentions=12,registered_candidate=release['candidate'],all_previous_limits_andfull_objective_preserved=True)
    if previous_pending in inventory:inventory[previous_pending]['registered_integration_completed_by']=marker
    for u in inventory.get('broader_coverage_units',[]):
        if u['id']=='all-route-scenes':u.update(reviewed_route_records=5599,completed_route_records=5599,next=NEXT)
    assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
    scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
    put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,incomplete_COMMON=3,incomplete_credited_route_drafts=0,new_uncredited_Hodram_source_positions=6,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
    evidence[str(FINAL)]=sha(FINAL.read_bytes());evidence[str(scope)]=sha(scope.read_bytes())
    new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_operations=ops,record_keys=keyrows,new_source_prose_reviews=28,new_completed_records=28,revised=16,retained=12,
        new_current_candidate_emulator_runs=1,new_current_candidate_frames=4001,all_prior_actual_proofs_reused_without_replay=True,all_sessions_terminal_andreaped=True,goal_turn_classification='progress',full_goal_complete=False)
    assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
    assert {historical_key(r) for r in new[fp[0]]['record_keys']}=={historical_key(r) for r in new[fp[0]]['integrated_record_keys']}==oldkeys|keys
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
    section='## V8305: Hodram28 integrated in cumulative V8300;next six clean source glosses prepared\n\n'+summary+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        p=Path('docs')/name;prefix=('# Current editorial handoff - V8305; V8300 current\n\n' if name=='editorial_handoff_current.md' else '')+section;targets[p]=prefix.replace('\n','\r\n').encode()+p.read_bytes()
    files=[]
    for i,(p,value) in enumerate(targets.items()):
        planned=ROOT/f'{i:02d}.after';planned.write_bytes(value)
        if p!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(p.read_bytes(),mtime=0))
        files.append(dict(target=str(p.resolve()),before_sha256=sha(p.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(value)))
    save(ROOT/'staged_completion.json',dict(files=files,evidence=evidence,all28_records_integrated_once=True,no_shared_mutation_yet=True,full_goal_complete=False))
    print('Staged six completion targets:28disjoint decisions/16revisions/12retentions;7199completed;deep inverse audit next.')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    if mode=='stage':stage()
    else:
        release=gates();plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
        for e in plan['files']:assert sha(Path(e['planned']).read_bytes())==e['planned_sha256'] and sha(Path(e['target']).read_bytes())==e['planned_sha256' if mode=='verify' else 'before_sha256']
        for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists();save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),deep_inverse_recovers_every_prior_root_family_record_counter_candidate=True,exactly28_disjoint_new_records=True,full_goal_complete=False))
            print('Deep inverse audit passed:every previous record/root/counter/candidate/scope recovers exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes())
            for e in plan['files']:
                assert Path(e['target']).is_relative_to(Path.cwd().resolve()) and Path(e['planned']).is_relative_to(ROOT.resolve())
                with Path(e['target']).open('r+b') as stream:stream.write(Path(e['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(e['target']).read_bytes())==e['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,exactly28_decisions_credited_once=True,current=release['candidate'],mainV4701_preserved=True,full_goal_complete=False))
            print('Applied currentV8300:7199completed/4471revised/2728retained;full objective active.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();prior=read(PRIOR);verified=deepcopy(prior)
            assert len({historical_key(r) for f in new['completed_editorial_families'] for r in f['records']})==7199
            verified.update(candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
                ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                **dict(zip(COUNTERS,AFTER,strict=True)),completed=7199,source_prose=7202,revised=4471,retained=2728,SC0=368,SC1=119,SC2=4915,SC3=197,reviewed_routes=5599,completed_routes=5599,
                manifest_batches=641,accepted_layers=114,release_checks=18,regressions=110,Hodram28_completed_once=True,Hodram28_atomic_registered_integration_pending=False,
                final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),actual_speech_observations_both_versions=56,actual_complete_body_andname_holds=262,
                strict_own_Hodram_current_input=read(START)['current_native_input'],previous_Rafael_Lil_andother_contexts_historical_until_correctly_rebound=True,
                next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch=NEXT_KEY,next_clean_exchange_not_selected=False,new_uncredited_source_positions=6,
                full_goal_active=True,full_goal_complete=False,all_current_andearlier_limits_preserved=True,all_sessions_terminal_andreaped=True,producer_sha256=sha(Path(__file__).read_bytes()))
            verified['Hodram_source_native_checkpoint'].update(completed_once=True,completion_final_review=str(FINAL),registered_candidate=release['candidate'],registered_candidate_sha256=release['candidate_sha256'],
                independent_actual_atomic_andregistered_integration_pending=False,independent_actual_atomic_andregistered_release_complete=True,completion_credit=28)
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV8306/currentV8300:7199completed/7202sourceprose/4471revisions/2728retentions;nextHodram6sourceglosses/fullgoal active.')
