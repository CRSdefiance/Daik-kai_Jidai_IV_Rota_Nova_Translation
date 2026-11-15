"""Credit five disjoint B52 decisions after registered release/startup; preserve the entire prior ledger."""
import argparse,gzip,json,os
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_B31_B53_editorial_v2 import check_dependencies
from dk4tool.dialogue.hodram_B31_B53_profile_v1 import validate_approved_batch,validate_runtime
from dk4tool.dialogue.hodram_B31_B53_names_v1 import validate_scoped_names
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.complete_Rafael_B50_v8184 import COUNTERS,digest
from scripts.Hodram_B31_B53_release_paths_v8767 import DOC,NAMES,SEAL,proofs,observed_scope
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B31_B53_completion_v8783')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8790')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8775/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
CONFIG=Path('translations/hodram_B31_B53_editorial_release_v2.json')
RELEASE=Path('work/analysis/Hodram_B31_B53_release_v8779/registered_release_verification.json')
START=Path('work/analysis/Hodram_B31_B53_registered_binding_v8781/own_Hodram_startup_andstrict_captain1_context.json')
VIEW=Path('work/analysis/Hodram_B31_B53_registered_startup_view_v8782/own_registered_startup6_RGBpairs_actor_equal_unchanged_names_direct_view.json')
POSITIVE=Path('work/analysis/Hodram_B31_B53_atomic_positive_v8770/atomic_positive.json')
NEGATIVE=Path('work/analysis/Hodram_B31_B53_atomic_challenges_v8772/semantic_rejections.json')
BINDING=Path('work/analysis/Hodram_B31_B53_integration_binding_v8776/integration_binding.json')
MEMORY=Path('work/analysis/Hodram_B31_B53_wrong_memory_v8771/wrong_memory_rejections.json')
REG=Path('work/analysis/Hodram_B31_B53_registration_v8777/registration_receipt.json')
FINAL=Path('translations/hodram_B31_B53_contextual_final_review_v1.json')
KEY='Hodram_SC1B31_B53_completion_v8783'
FAMILY='Hodram_SC1B31_B53_agency_andwanted_status_v8783'
SCOPE='unfinished_editorial_scope_v8783'
NEXT_KEY='Hodram_SC1B54_B60_82_clean_glosses_pending_native_andcurrent_English_v8783'
NEXT_SOURCE=Path('work/analysis/Hodram_next_clean_v8785/complete_clean_SC1_B54_B60_EV1_andcoverage_before_current_English.json')
NEXT_CONTEXT_SOURCE=NEXT_SOURCE
NEXT_GLOSS=Path('work/analysis/Hodram_next_clean_gloss_v8787/82_qualified_clean_glosses_no_unbound_gender_orFA_type.json')
BEFORE=(7234,7237,7237,4489,2745)
AFTER=(7237,7240,7240,4492,2745)
PENDING_FLAGS=['source_presentation_consumer_not_yet_approved','current_English_body_unread','current_English_dialogue_still_unconsulted','current_English_dialogue_still_unread',
    'source_meaning_only_not_editorial_orformatting_approval','native_branch_membership_androle_name_full_preamble_consumer_pending',
    'current_contextual_prose_formatting_actual_andrelease_pending','formatting_native_stored_actual_policy_atomic_andregistered_integration_pending',
    'all_stored_controls_actual_branch_context_headers_policy_andregistered_release_pending','formatting_registered_release_pending',
    'no_source_prose_counter_orcompletion_credit','no_completion_or_source_prose_counter_credit_added']
INTRO='Hodram SC1 B31/B53 is complete in registered experimental cumulative V8778:three revisions,credited exactly once. Totals7,237 completed/7,240 credited source-prose anddrafts/4,492 integrated revisions/2,745 retentions. SC0 368/SC1 157/SC2 4,915/SC3 197/COMMON1,600 completed and1,603 source-prose;route subtotal5,637 isnot the full-goal denominator. All647manifestbatches/114acceptedlayers/18releasechecks/110regressions,exactreviewed-referenceROM,clean-inputpatch andown4001frame registeredstartup pass. MainV4701/canonicalbaseline remainunchanged. Preserve every ROM,translation,draft,executed producer,proof andfailure. No separatepackage,promotion,pruning,commitorpush. Full editorial objective remainsactive.'
DETAILS="""Clean Japanese and complete alternate-branch/dependency context preceded prior English. B31's two revisions restore the speaker taking the opponent on himself, rather than ordering the addressee to face him. The longer variant retains the warning about crossing a truly frightening man without assigning that unnamed man an identity, rank or relationship. B53 restores apparent wanted status, undesirable culmination and gruff practical caution;it removes the unsupported bounty without inventing a crime,warrant,pursuer,location oroutcome. All three are individual revisions;no new dialogue-retention credit is added. Scoped actor34 retention preserves the actual source progressive/full getter components including Fazul and existing order/mixed-width storage. Actor113 remains Port Worker,with no brother relationship orrank. Wider catalogue UI/all207/customnames andwider role contexts remainopen.

All five individual natural-dialogue-v2 gates,exact clean/predecessor/compiled/stored/final references,full216px automatic pages2/4/3rows,complete leading/internal/final characters,bounds,consumption andpagination pass. Zero original QAissues,warnings orwaivers;no authored ordinary breaks,padding,shortening orfont/viewport changes. B31 source196/target228stored bytes has4relatives/1unforcedquery andnormalend192->224;B53 source136/target156stored bytes hasno relatives/queries andnormalend132->150 withseparate2byte tail. All18commands/3fullsix-bytepreambles/8opaquecontrols/2normalends preserve original semantics;opaque effect semantics remainuninferred. Both clean/currentblock,archive andwhole-ROM inverses/all323unownedblocks/everyotherfile/component/full123264payload pass. Source52->31->53 dependencies do not prove continuous conversation,chronological proximity,original location,earned progress,B52choice effects orunnamed-man identity.

Four initialized whole-block source/English cold boots24,004frames provide76complete body/name holds/fourpage occurrences:long B31R0018 andB53R0007 inbothlanguages. Short B31R0013 remains offline-only,with complete native page/control/branch/same-consumer representative evidence;its predicate isneverforced. Japanese bodies use current English names/UI/code/font andeight original initializers34bytes,not all-Japanese UI or natural event activation. B31 returns[0,1]at4016;B53 returns[0,0]at4013 whileinterpreter mode is1. Normalend preserves prior parser-result value independently ofr3. Retain allthree decodedlength differences;duration/UIrequests/boundaryRNG/followingcommands match. Allfive sampled finalcomponents/wholeactors/captain1/rawcalendar/finalseed3325064553 and68laterRGBpairs matchthrough6001frames. No natural eligibility/location,fullcatalogue,customnames,everyframecausality,broad future simulation,fullroute orhardware claim. Preserve every earlier B52/B51/B50/B49/Gerhard/Rafael/Hodram/Lil measured limitation.

All364 meaningful changed-input production rejections pass. Both whole-NDS atomiclifecycles yield value-equal reports/exactreviewedROM withonefinalcommit;3wrong-memory,4representative semantic andone late shared target failure leaveoriginalobjects exact. Only the outer digest layer isbypassed in the4inmemory semantic injections;native/frozen/editorial/semantic guards remainactive. Unchanged shared-framework6generic cases andbuilder5positive/29negative cases arereused byexactsource binding. ConfigurationV2 preservesall1424original entries andextends to1435dependencies. The unchanged sharedbuilder appends this batch after unchanged B52,without editing oldprefix configurations orbuilderbytes.

RegisteredV8778 SHA251e947d17d4b24af987546834fb07192ebc2b93f6e59b89766fdb73affaf8af equals the independently reviewed research reference. Patch SHA55d187fc5d935fa67996728c6662578cd8240c2c360e6f5bd6d16e8995a0cfec reconstructs it exactly fromclean Japanese. Its own4001frame ordinarycoldboot/strict captain1 context/six wholePNGpairs/wholeactors/name12+Blades8/ARM9/COMMON/font/full123264payload anddirectstartupview pass. This is ownstartup,not new optional-event coverage. Build90938,releasecheck9365 andcapture39260 areterminal/reaped. The live-observer8788 correctly refused to recordrunning status because the build had become terminal before observation;no live receipt waswritten andno restartoccurred.

Preserve stopped8776integrationpreparer andits three complete derived producers;8776b qualifies the generic pytest runner's actual no-ROM/profile schema without overwriting them. Preserve all previous qualified failures:shared8773path-key/8773bseparator/8773ccompletion,seal8769context-key/8769b,prepared atomicV1/V2four-sheet schema,actual8742wrongresultchannel/8742b,sourcefullname8733one-row/8733b19-glyph qualification,formatting8745receipt/8745b,andallolder artifacts. No original producer isrewritten."""
NEXT="""Continue from verifiedV8790/current experimentalV8778. Three B31/B53 revisions arecredited once;reuse all completed source/prose/native/stored/production/actual/atomic/shared/registeredbuild/cleanpatch/ownstartup checks. New owncaptain1 helper scripts/Hodram_B31_B53_registered_route_context_v8781.py uses work/analysis/current_V8778_Hodram_native_v8781/current_native_input.json. Main4701/canonicalbaseline remainunchanged;preserve every ROM,translation,draft,producer,proof andfailure.

Next clean source candidate set is SC1 B54-B60:82 uncredited utterances in seven complete blocks,one FE panel,no typedmenu,zero completed overlap. Full native commands,source references/preambles/EV1 metadata areinventoried in8785;82 individual first meanings andwhole-block contextual/cultural notes arein8786,qualified by8787 toavoid unbound actor genders andunproved FA personal-name type. Earlier gloss/producer remain. Existing English for allsevenblocks isstillunconsulted. These areclean meaning glosses only,no localization,names,nativeformatting,actual orcompletion approval. Numeric blockadjacency isnot chronology orone attainable exchange. B58's49utterances include conditional companion paths:bind actual source queries/branches andmembership before English. Bind surrounding original event context,source names/roles,FI/FA referents,FEcaption consumer,opaque controls andnormalends inownV8778 before consulting older English. Treat the girl's language learning respectfully;preserve ethnic identity,actual kinship versusfamily simile,missing versusdead relatives,slavery/colonial context,Christian neighbor-love reference,hearsay aboutSolomon anduncertainIceland suggestion. Do not invent ages,ranks,biography,weapon/itemidentity,punishment,macrotype orquery effects.

Allfourstorylines/earlier translateddialogue/sharedtown-shop/random/Help/restprose/all207names-roles-aliases-customnames/retrospectiveprematurebreaks remainactive. Preserve every copiedunfinishedscope lead,including contractions/questiontags/unscanned558plans/weak-before-row/COMMON750-752/preLF6435/wider104-105-113-147/JanusPasar-versusPasha/ceramics17wrap/Cristina-Christina/HansRetzel-Letzel/Samwellmiddle/SourceItem-LocalProduct/Alexandria/AksumGoldSeal/Armadillo-SteelHide/HerophilusMedicine/イギリス/AlShin-AlFeridShin/Sailor151-159versusRetainer/oldernormalends/nineteenthcells/B47-B48-B50metadata. Graphics/all18plaques andlaterolder-recordtechnicalre-audit stayseparate. Roughly20,000remainingcandidates isonly a planning estimate,not an audited denominator. Fullgoalactive."""

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
    release,start,view,positive,negative,binding,reg,doc,seal,memory=map(read,[RELEASE,START,VIEW,POSITIVE,NEGATIVE,BINDING,REG,DOC,SEAL,MEMORY])
    candidate=Path(release['candidate']);manifest=read(release['manifest']);registry=read('translations/release_stack.json')
    assert sha(candidate.read_bytes())==release['candidate_sha256']==start['candidate_sha256']==view['candidate_sha256']==manifest['candidate_sha256']
    assert manifest['profile']==reg['profile']=='all-routes-unified-v8778' and len(manifest['batches'])==647 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())==reg['registry_after_sha256'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert release['all110_release_dialogue_regressions_pass'] and release['whole_clean_input_ROM_reconstruction_byte_exact'] and sha(Path(release['patch']).read_bytes())==release['patch_sha256'] and Path(release['exact_patch_reconstruction']).read_bytes()==candidate.read_bytes()
    assert view['viewed'] and len(view['six_whole_RGB_pairs'])==6 and view['whole_actors_equal'] and view['target_family12_andprotected_Blades8_measured_inactual_coldboot_RAM']
    assert start['all_strict_targetARM9_inverse_Blades_COMMON_directory_and123264_payload_guards_pass'] and start['actual_original_captain_ID']==1 and start['actual_frames']==4001
    assert positive['positive_lifecycles']==2 and positive['one_complete_NDS_commit_percase'] and positive['cases'][0]['report']==positive['cases'][1]['report']
    assert negative['negative_count']==4 and all(c['rejected'] and c['commit_calls']==0 and c['actual_changed_input'] and c['original_object_identity_files_components_andserialized_bytes_unchanged'] for c in negative['cases'])
    assert binding['lifecycle_reports_value_equal'] and binding['genuine_wrong_memory_cases']==3 and binding['semantic_zero_commit_cases']==4 and binding['shared_zero_commit_cases']==1 and binding['final_dependencies']==1435
    assert memory['negative_count']==3 and memory['every_wrong_image_rejected_before_commit_withall_guards_active'] and memory['no_digest_orsemantic_bypass']
    assert seal['manuscript_sha256']==sha(DOC.read_bytes()) and seal['name_review_sha256']==sha(NAMES.read_bytes()) and reg['release_config']==str(CONFIG) and reg['release_config_sha256']==sha(CONFIG.read_bytes())
    assert len(doc['records'])==3 and not doc['typed_choice_records'] and Counter(r['decision'] for r in doc['records'])==dict(revision=3)
    validate_approved_batch(doc);validate_scoped_names(read(NAMES));validate_runtime(NdsImage.open(candidate));check_dependencies(read(CONFIG))
    data={k:read(p) for k,p in proofs().items()};scope=observed_scope(data)
    assert scope==seal['observed_scope']==positive['cases'][1]['report']['actual_scope']==release['actual_scope_limits']
    assert (scope['complete_page_occurrences'],scope['complete_body_name_holds'],scope['total_actual_frames'])==(4,76,24004)
    assert scope['actual_unique_speech_IDs']==['DK4_MES_B31_R0018','DK4_MES_B53_R0007'] and scope['unvisited_conditional_text_IDs']==['DK4_MES_B31_R0013']
    assert release['only_SC1_B31_B53_change_323_otherblocks_andall_other_files_components_exact'] and candidate.read_bytes()==Path(doc['reference_ROM']).read_bytes()
    source,gloss=map(read,[NEXT_SOURCE,NEXT_GLOSS]);assert not source['inventory_failures'] and source['source_only_no_current_English_exposed_orused']
    assert gloss['all82_clean_utterances_andseven_complete_blocks_read_before_earlier_English'] and gloss['unbound_actor_genders_andmacro_referent_types_not_invented']
    assert [g['block'] for g in gloss['groups']]==[54,55,56,57,58,59,60] and sum(len(g['records']) for g in gloss['groups'])==82
    assert all(r['current_English_dialogue_still_unconsulted'] and not r['already_contextually_completed'] for g in gloss['groups'] for r in g['records'])
    assert read('work/analysis/Hodram_B31_B53_build_v8778/build_terminal.json')['returncode']==0 and read('work/analysis/Hodram_B31_B53_registered_context_runs_v8780/route1/terminal.json')['terminal']
    return release


def stage():
    assert not ROOT.exists() and not FINAL.exists();release=gates();prior=read(PRIOR);before=LEDGER.read_bytes();old=json.loads(before);doc=read(DOC)
    assert sha(before)==prior['ledger_sha256'] and tuple(old[k] for k in COUNTERS)==BEFORE and old['goal_status']=='active' and KEY not in old
    originals=doc['records'];oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};keys={historical_key(r) for r in originals}
    assert len(oldkeys)==7234 and len(keys)==3 and not oldkeys&keys
    bank=IlnkContainer.parse(NdsImage.open(release['candidate']).read_file('/data/SC1.DK4')).blocks
    mappings={g['block']:g for g in read(proofs()['relocation'])['groups']};rows=[]
    observed=set(release['actual_scope_limits']['actual_unique_speech_IDs'])
    for original in originals:
        row=deepcopy(original);target=row['final_reference'];raw=bytes.fromhex(row['final_hex']);number=row['block'];block=bank[number];at=target['offset'];mapping=mappings[number]
        assert target['block']==number and sha(block)==target['target_block_sha256'] and block[at:at+len(raw)+1]==raw+b'\0' and block[:at].count(b'\0')==target['record_index']
        command=next(c for c in mapping['all_target_commands'] if c['offset']==target['header_offset']);assert command['word']==0x4000
        body=raw[1:].decode('cp932');row['pre_integration_review_record_preserved']=deepcopy(original)
        row.update(predecessor_reference=deepcopy(original['current_reference']),predecessor_hex=original['current_hex'],
            reviewed_against_predecessor_ROM=doc['current_ROM'],reviewed_against_predecessor_ROM_sha256=doc['current_ROM_sha256'],
            current_reference=deepcopy(target),current_hex=raw.hex(),current_text_hex=raw.hex(),current_record_index=target['record_index'],
            current_native_extent=command['native_extent'],current_0100_ancestors=command['ancestor_0100_offsets'],current_raw_storage_English=body,
            current_English=' '.join(body.split()),current_stored_English=body,current_reference_ROM=release['candidate'],current_reference_ROM_sha256=release['candidate_sha256'],
            completed_candidate_reference=deepcopy(target),completed_candidate_sha256=release['candidate_sha256'],
            integrated_reference=dict(**target,stored_hex=raw.hex(),ROM=release['candidate'],ROM_sha256=release['candidate_sha256']),
            source_prose_andcompletion_credit_added_once=True,source_prose_orcompletion_credit_added=True,registered_integration_pending=False,
            current_review_status='integrated-contextual-native-qualified-actual-registered-release',already_contextually_completed=True,
            individually_activated_in_current_build=False,actual_initialized_source_andEnglish_selected_paths_observed=row['id'] in observed,
            offline_only_variant_with_complete_native_andrepresentative_sameconsumer_evidence=row['id'] not in observed,
            current_observation_scope='Exact reviewed reference equals registeredV8778. Four initialized source/English wholeblock runs/24004frames/76holds/4pages show long B31 andB53warning;short B31R13 remains offline-only. No natural eventactivation/location/fullcatalogue/customnames/fullroute/hardware/future simulation claim.',
            actual_proofs={k:proofs()[k] for k in ['B31_actual','B53_actual','comparison']},editorial_unit_kind='speech')
        for key in PENDING_FLAGS:
            if key in row:assert isinstance(row[key],bool);row[key]=False
        row['all_current_editorial_formatting_policy_atomic_registered_requirements_completed']=True
        row['opaque_effect_gameplay_semantics_outer_eligibility_andfuture_causality_remain_unproven']=True
        assert all(row[k]==original[k] for k in ['english','source_hex','source_reference','source_meaning','context','localization_note','retention_reason','review','decision']);rows.append(row)
    summary=INTRO+'\n\n'+DETAILS+'\n\n'+NEXT
    evidence={str(p):sha(Path(p).read_bytes()) for p in [PRIOR,CONFIG,DOC,NAMES,SEAL,RELEASE,START,VIEW,POSITIVE,NEGATIVE,BINDING,MEMORY,REG,NEXT_SOURCE,NEXT_CONTEXT_SOURCE,NEXT_GLOSS,__file__,*proofs().values()]}
    ROOT.mkdir(parents=True)
    save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=rows,revised=3,retained=0,
        source_dialogue_order=[r['id'] for r in rows],source_prose_and_completion_credit_added_once=3,physical_speeches=3,typed_choice_labels=0,
        actual_unique_speech_IDs=sorted(observed),offline_only_text_IDs=['DK4_MES_B31_R0013'],actual_speech_page_occurrences_both_versions=4,
        actual_complete_body_andname_holds=76,actual_original_optional_activation=False,source_fixture_clean_Japanese_body_withcurrent_registered_English_names_UI_code_font=True,
        all_actual_scope_limits_preserved=True,all_source_current_compiled_stored_actual_andintegrated_refs_bound=True,
        all18_commands3_preambles4_relatives1_query8_opaque2_normalends_andtails_preserved=True,both_clean_source_andfull_predecessor_inverses_exact=True,
        policy_expected_rejections=236,all_independent_technical_rejections=364,atomic_semantic_rejections=4,new_all_guard_wrong_memory_rejections=3,shared_precommit_rejections=1,
        unchanged_shared_generic_six_andbuilder29_cases_reused_byexact_source_hash=True,zero_original_QAissues_warnings_andwaivers_preserved=True,new_registered_startup_frames=4001,
        all_prior_scope_graphics_separation_later_audit_preserved=True,summary=summary,evidence=evidence,full_goal_complete=False))
    new=deepcopy(old);ops=[]
    def put(path,value):
        parent,key=parent_at(new,path);exists=key in parent if isinstance(parent,dict) else key<len(parent)
        ops.append(dict(kind='set',path=path,existed=exists,before=deepcopy(parent[key]) if exists else None));parent[key]=deepcopy(value)
    def append(path,values):
        parent,key=parent_at(new,path);ops.append(dict(kind='append',path=path,before_length=len(parent[key]),count=len(values),appended_sha256=digest(values)));parent[key].extend(deepcopy(values))
    for key,value in zip(COUNTERS,AFTER,strict=True):put([key],value)
    for key in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:
        assert new[key]['/data/SC1.DK4']==154;put([key,'/data/SC1.DK4'],157)
    append(['completed_editorial_families'],[dict(id=FAMILY,file_path='/data/SC1.DK4',blocks=[31,53],record_IDs=[r['id'] for r in rows],records=rows,
        final_review=str(FINAL),revised_count=3,retained_count=0,fresh_revisions=3,fresh_retentions=0,actual_verification_scope=DETAILS)])
    fp=['contextual_story_natural_dialogue_pass_v1871'];keyrows=[dict(file_path='/data/SC1.DK4',id=r['id']) for r in rows]
    for key in ['record_keys','integrated_record_keys']:append(fp+[key],keyrows)
    append(fp+['record_IDs'],[r['id'] for r in rows])
    for key,value in dict(fresh_pass_records_explicitly_reread=7237,fresh_pass_records_integrated=7237,latest_contextual_manuscript=str(DOC),latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=INTRO).items():put(fp+[key],value)
    append(fp+['reconciled_families'],[dict(id=FAMILY,records=3,physical_speeches=3,typed_choices=0,final_review=str(FINAL),new_revisions=3,justified_retentions=0,
        new_completed_records=3,historical_reconciliation_only=False,actual_optional_event_selected=False,actual_unique_speech_displays=2,actual_typed_options=0,offline_only_objects=1,all_prior_scene_proofs_reused_without_replay=True)])
    if str(DOC) not in new['active_source_prose_drafts']['manuscripts']:append(['active_source_prose_drafts','manuscripts'],[str(DOC)])
    put(['active_source_prose_drafts','route_record_subsets_pending',str(DOC)],[]);put(['active_source_prose_drafts','note'],INTRO)
    ri=next(i for i,u in enumerate(new['coverage_units']) if u['id']=='all-route-scenes')
    assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5634
    for key,value in dict(reviewed_route_records=5637,completed_route_records=5637,next=NEXT).items():put(['coverage_units',ri,key],value)
    append(['coverage_units'],[dict(id=FAMILY,status='complete-contextual-native-qualified-actual-registered-release',file_path='/data/SC1.DK4',blocks=[31,53],completion_credit_added=3,
        final_review=str(FINAL),actual_original_optional_activation=False,actual_speeches=2,offline_only_speeches=1,actual_typed_options=0,full_goal_complete=False)])
    put(['formatting_watchlist',FAMILY],dict(status='three-complete-native-pages-two-observed-utterances-one-offline-alternate-registered-pass',final_review=str(FINAL),zero_QAissues_warnings_orwaivers=True,
        complete_glyphs_full216px_bounds_pagination_andall_prior_leads_preserved=True,full_goal_complete=False))
    current=deepcopy(old['current_integrated_candidate']);current.update(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],
        ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
        status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False,**{f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)})
    put(['current_integrated_candidate'],current);put(['latest_checkpoint'],summary)
    gloss=read(NEXT_GLOSS);pending=dict(status='82-clean-meaning-glosses-names-native-controls-branches-current-English-localization-format-actual-release-pending',
        source_packets=[dict(path=str(NEXT_SOURCE),sha256=sha(NEXT_SOURCE.read_bytes()))],source_gloss=str(NEXT_GLOSS),source_gloss_sha256=sha(NEXT_GLOSS.read_bytes()),
        source_groups=deepcopy(gloss['groups']),file_path='/data/SC1.DK4',blocks=[54,55,56,57,58,59,60],physical_speeches=82,typed_choice_labels=0,source_FE_objects=1,
        source_commands_byblock={str(g['block']):len(g['commands']) for g in gloss['groups']},all82_glossed_before_earlier_English=True,
        current_English_forall_seven_blocks_still_unconsulted=True,source_positions_credited=0,completion_credit_added=0,
        native_branch_membership_names_macros_FE_consumer_opaque_controls_eligibility_andfinal_English_unapproved=True,whole_full_editorial_objective_active=True,full_goal_complete=False)
    oldpending=prior['pending_source_batch'];marker=dict(completion=KEY,final_review=str(FINAL),records=3,all_prior_pending_notes_historical_not_deleted=True,new_credit_added_here=0)
    put([oldpending,'registered_integration_completed_by'],marker);put([NEXT_KEY],pending)
    descriptor=old[prior['unfinished_scope']];assert sha(Path(descriptor['path']).read_bytes())==descriptor['sha256']
    original_inventory=read(descriptor['path']);inventory=deepcopy(original_inventory)
    inventory['latest_next_focus_v8783']=NEXT;inventory[NEXT_KEY]=deepcopy(pending)
    inventory[KEY]=dict(final_review=str(FINAL),completed_objects=3,revisions=3,retentions=0,registered_candidate=release['candidate'],completed_prior_pending_key=oldpending,all_previous_limits_andfull_objective_preserved=True)
    assert all(inventory[k]==v for k,v in original_inventory.items())
    assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
    scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
    put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,
        incomplete_COMMON=3,incomplete_credited_route_drafts=0,next_clean_exchange_not_yet_selected=False,new_uncredited_clean_source_positions=82,
        graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
    evidence[str(FINAL)]=sha(FINAL.read_bytes());evidence[str(scope)]=sha(scope.read_bytes())
    new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_operations=ops,record_keys=keyrows,
        new_source_prose_reviews=3,new_completed_records=3,revised=3,retained=0,new_current_candidate_emulator_runs=1,new_current_candidate_frames=4001,
        all_prior_scene_proofs_reused_without_replay=True,all_sessions_terminal_andreaped=True,goal_turn_classification='progress',full_goal_complete=False)
    assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
    assert {historical_key(r) for r in new[fp[0]]['record_keys']}=={historical_key(r) for r in new[fp[0]]['integrated_record_keys']}==oldkeys|keys
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name;prefix=('# Current editorial handoff - V8783; V8778 current\n\n' if name=='editorial_handoff_current.md' else '')+'## V8783: B31/B53 three revisions integrated once in V8778; next82 clean meanings pending native andEnglish review\n\n'+summary+'\n\n'
        targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
    files=[]
    for index,(path,value) in enumerate(targets.items()):
        planned=ROOT/f'{index:02d}.after';planned.write_bytes(value)
        if path!=LEDGER:(ROOT/f'{index:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
        files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(value)))
    save(ROOT/'staged_completion.json',dict(files=files,evidence=evidence,all3_records_integrated_once=True,no_shared_mutation_yet=True,full_goal_complete=False))
    print('Staged B31/B53 completion:3disjoint revisions/zero newretentions;all old values recover;independent audit next.')


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    if mode=='stage':stage()
    else:
        release=gates();plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
        for entry in plan['files']:
            assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256'] and sha(Path(entry['target']).read_bytes())==entry['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest_ in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest_
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            for index,entry in enumerate(plan['files'][1:],start=1):
                raw=gzip.decompress((ROOT/f'{index:02d}.before.gz').read_bytes());assert sha(raw)==entry['before_sha256'] and Path(entry['planned']).read_bytes().endswith(raw)
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),deep_inverse_recovers_every_prior_root_family_record_counter_candidate=True,
                every_prior_document_preserved_byte_exact=True,exactly3_disjoint_new_records=True,full_goal_complete=False))
            print('B31/B53 deep inverse audit passes;all earlier values/counters/families/candidate/documents recover exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes())
            independent=read('work/analysis/Hodram_B31_B53_completion_audit_v8784/independent_staged_completion_audit.json')
            assert independent['three_disjoint_new_keys_only'] and independent['exact_full_prior_ledger_inverse']
            for entry in plan['files']:
                assert Path(entry['target']).is_relative_to(Path.cwd().resolve()) and Path(entry['planned']).is_relative_to(ROOT.resolve())
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,exactly3_decisions_credited_once=True,current=release['candidate'],mainV4701_preserved=True,full_goal_complete=False))
            print('Applied V8778:7237completed/7240source-prose/4492revised/2745retained;full goal active.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();prior=read(PRIOR);verified=deepcopy(prior)
            assert len({historical_key(r) for f in new['completed_editorial_families'] for r in f['records']})==7237
            verified.update(candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],ledger_sha256=sha(LEDGER.read_bytes()),
                previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),**dict(zip(COUNTERS,AFTER,strict=True)),
                completed=7237,source_prose=7240,revised=4492,retained=2745,SC0=368,SC1=157,SC2=4915,SC3=197,reviewed_routes=5637,completed_routes=5637,manifest_batches=647,accepted_layers=114,release_checks=18,regressions=110,
                Hodram_B31_B53_completed_once=True,Hodram_B31_B53_atomic_registered_integration_pending=False,registered_builder_90938_terminal_andreaped=True,
                final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch=NEXT_KEY,next_clean_exchange_not_selected=False,
                new_uncredited_source_positions=82,physical_speeches_pending=82,typed_choice_labels_pending=0,new_credit=3,new_emulator_runs=1,new_actual_frames=4001,
                all_sessions_terminal_andreaped=True,all_new_native_jobs_terminal_andreaped=True,all_prior_roots_families_records_andcounts_recover_exactly=True,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV8790/currentV8778:7237completed,3B31/B53revisions credited once;next82clean meanings/olderEnglishunread;full goal active.')
