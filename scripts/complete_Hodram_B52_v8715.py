"""Credit five disjoint B52 decisions after registered release/startup; preserve the entire prior ledger."""
import argparse,gzip,json,os
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_B52_editorial_v2 import check_dependencies
from dk4tool.dialogue.hodram_B52_profile_v1 import validate_approved_batch,validate_runtime
from dk4tool.dialogue.hodram_B52_names_v1 import validate_scoped_names
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.complete_Rafael_B50_v8184 import COUNTERS,digest
from scripts.Hodram_B52_release_paths_v8693 import DOC,NAMES,SEAL,proofs,observed_scope
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B52_completion_v8715')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8716')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8710/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
CONFIG=Path('translations/hodram_B52_editorial_release_v3.json')
RELEASE=Path('work/analysis/Hodram_B52_release_v8705/registered_release_verification.json')
START=Path('work/analysis/Hodram_B52_registered_binding_v8707/own_Hodram_startup_andstrict_captain1_context.json')
VIEW=Path('work/analysis/Hodram_B52_registered_startup_view_v8708/own_registered_startup6_RGBpairs_actor_equal_unchanged_names_direct_view.json')
POSITIVE=Path('work/analysis/Hodram_B52_atomic_positive_v8690b/atomic_positive.json')
NEGATIVE=Path('work/analysis/Hodram_B52_atomic_challenges_v8692/semantic_rejections.json')
BINDING=Path('work/analysis/Hodram_B52_integration_binding_v8699/integration_binding.json')
MEMORY=Path('work/analysis/Hodram_B52_wrong_memory_v8691b/wrong_memory_rejections.json')
REG=Path('work/analysis/Hodram_B52_registration_v8703/registration_receipt.json')
FINAL=Path('translations/hodram_B52_contextual_final_review_v1.json')
KEY='Hodram_SC1B52_completion_v8715'
FAMILY='Hodram_SC1B52_opposition_warning_v8715'
SCOPE='unfinished_editorial_scope_v8715'
NEXT_KEY='Hodram_SC1B31_B53_three_clean_glosses_pending_native_current_andrelease_v8715'
NEXT_SOURCE=Path('work/analysis/Hodram_B53_clean_v8711/complete_clean_SC1_B53_EV1_andcoverage_before_current_English.json')
NEXT_CONTEXT_SOURCE=Path('work/analysis/Hodram_B53_dependency_context_v8713/complete_clean_SC1_B31_dependency_context_before_B53_English.json')
NEXT_GLOSS=Path('work/analysis/Hodram_B31_B53_clean_context_v8714/three_clean_glosses_explicit52_31_53_dependency_andunnamed_man_before_current_English.json')
BEFORE=(7229,7232,7232,4487,2742)
AFTER=(7234,7237,7237,4489,2745)
PENDING_FLAGS=[
    'source_presentation_consumer_not_yet_approved','current_English_body_unread','current_English_dialogue_still_unconsulted',
    'source_meaning_only_not_localized_orformatting_approval','native_speakers_menu_queries_branches_opaque_controls_terminal_current_actual_release_pending',
    'current_effective_dispatch_andcatalogue_pending','current_contextual_prose_formatting_actual_andrelease_pending',
    'formatting_native_stored_actual_policy_atomic_andregistered_integration_pending','all_stored_controls_actual_branch_context_headers_policy_andregistered_release_pending',
    'current_body_not_contextually_approved','all_stored_choice_references_branch_extents_actual_backing_controller_policy_andregistered_release_pending',
    'formal_policy_atomic_registered_release_andcompletion_credit_pending','formatting_registered_release_pending']

INTRO='Hodram SC1B52 is complete in registered experimental cumulative V8704:five decisions,two revisions andthree individually justified retentions,credited exactly once. Totals7,234 completed/7,237 credited source-prose anddrafts/4,489 integrated revisions/2,745 retentions. SC0 368/SC1 154/SC2 4,915/SC3 197/COMMON1,600 completed and1,603 source-prose;route subtotal5,634 isnot the full-goal denominator. All646manifestbatches/114acceptedlayers/18releasechecks/110regressions,exactreviewed-referenceROM,clean-inputpatch andown4001frame registeredstartup pass. MainV4701/canonicalbaseline remainunchanged. Preserve every ROM,translation,draft,executed producer,proof andfailure. No separatepackage,promotion,pruning,commitorpush. Full editorial objective remainsactive.'
DETAILS='''Clean Japanese question,both typed choices andboth responses were read/glossed as a complete exchange before existing English. Revise the question to Are you planning to make an enemy of Hayreddin's outfit? to preserve intention andan informal named-group sense without inventing blood kinship. Revise the final idiom to You've got a death wish, huh? as a casual comment on dangerous boldness,not a literal death guarantee,threat orsuicidal intent. Individually retain Not at all., Bring it on. and Then get out before they notice you. because they naturally carry denial,confident acceptance andbrisk advice in their complete response paths. Port Worker is a scoped actor113 role retention;兄貴 supplies no family relationship/rank. Hayreddin is the verified mentioned actor34 surname component,not an actual actor34 header/full-name/catalogue approval. Wider PortWorker contexts/all207 names remainopen.

Every individual natural-dialogue-v2 gate and exact clean/predecessor/compiled/stored/integrated reference passes. Three English singlepages use full216px automatic wrapping,original font/guard/pair-phase/macro rules andcomplete leading/internal/finalglyphs,bounds,consumption andpagination. One original line-count info remains;zero warnings/waivers. No authored ordinary breaks,padding,shortening orviewport/font changes. Source228/target236 bytes preserve14commands/3fullsix-bytepreludes/4relatives/zeroqueries/one two-choice menu/4opaquecontrols/both fullfour-byteends/zero tail. Normal166moves158/carriesvalue;flagged224moves232/returnskind1clearsvalue. Preserve83c2andthreeA000s structurally withoutinvented effectsemantics. Two compiler-owned parity tails pass8freshstoredalignments;the exact first body explicitly reuses4. Complete clean/currentblock,archive andwhole-ROM inverses/all324unownedblocks/everyotherfile/component/name/font/full123264payload pass. All325load/cache paths/650parentmodes/326actions bind;the complete caller census is reused only through every decoded section/overlay name/base/length/payload hash.

Representative actual evidence is reused through exact reference/registered ROM equality and independently reconstructed full initialized fixtures. Six source/English coldboots50,406frames include main40,004frames/92complete body-name holds/8page occurrences andfocused10,402frames/46holds/4pages. All3unique speeches andboth ordinary A/Down choices/both normal[0,0] andflagged[1,0] ends are observed across cases,with explicit case-specific unvisited opposite responses. The Japanese-body fixture uses current registered English names/UI/code/font;it isnot an all-Japanese UI or natural event activation. Twelve existing actualmenus/24captions passcomplete Japanese/English glyphs,constructor-based centering/bounds,selected/unselected backgrounds/highlights andthe shared4210blink-off. Native backing bounds are separate offline proof;no live owner/RAM/VRAM/palette/unowned backing-byte identity oractualB/cancelavailability is claimed. The inherited combined backing/controller pending flag is resolved only within this qualified offline-plus-visible scope.

Keep all differences:menu durations229Japanese/231English;normalreturns4495/4497 andflagged4494/4496;boundaryRNG andfollowingcommand differences. Longwithdrawal has46of93laterRGBdifferences,unequal state/models/persistentobjects/calendar/wholeactors,matching tasks,finalseeds2571928604/1941737819 anddifferent rawcalendars. At10001Japanese sails whileEnglish is atRigaresupply. Longopposition has13of93laterRGBdifferences,matching five sampledcomponents/actors butfinalseeds1611048932/1190801271. Focusedwithdrawal uses exact unretimed defaultinputprefix,lastA4480duration5,noinputsafter4484;all5sampledcomponents/actors/captain1/seed613908813/rawcalendar and13laterRGBpairs match,withno followingcommands. This supports immediate postexchange behavior only;no harmlessness,causal explanation,everyframe orfuture simulation equivalence is established. Event52requires30/excludes74;outereligibility/scheduling/originallocation/earnedprogress/fullroute/customnames/hardware remainunobserved.

Original source-controls8620 used ownV8543,notV8609. Exact separate input/report/snapshot hashes andcomplete ARM9/COMMON/font/EV1/wholeactors qualify source reuse;wholeRAMsnapshots differ andno historical RAM is transplanted. ControlsV2 rebinds all needed source consumers in ownV8609. All frozen/native/production tests pass340 actualchanged-input rejections. AtomicV2/configV3 retains1026dependencies,all471frozen/all855prior entries:bothlifecycle reportsvalue-equal,onewholeNDScommit each,3wrong-memory/16semantic/6shared failures leave originalobjects exact. Builder5positive/29negative forms preserveentire oldbuilder/newline inverse;compatible prefix reproduceswholeV8609. Shared late hook runs aftercompleteB51 beforefinalguards. Keep stoppedV1alias/seal/config/positive,the originalnewline-preparer failure andallqualified successors.

RegisteredV8704 equals pinned reference cc6da60d7ba1e3306bf27ba62991c2058fcc35c8139e2ec00fa65ff352091dae. Exact clean-input patch SHA7edf63599a844f2a8fee970879f1dd859b6f38277baa64e803b4af52c77ff29c reconstructs it fromoriginalclean. Its own ordinary4001framecoldboot,strict captain1 currentcontext,sixwholePNGpairs/wholeactors/currentname12+Blades8/code/COMMON/font/full123264payload anddirectstartupview pass. Oldname/getter proofs are reused only through complete code/font/actors equality. No optionalB52 original-location visit is added. Build11577 andcapture56308 areterminal/reaped. All earlier B51/B50/B49/Gerhard/Rafael/Hodram/B48 timing/RNG/RGB/calendar/following-command/fixture limitations remain.'''
NEXT='''Continue from verifiedV8716/current verified experimentalV8704. B52five decisions arecredited once;do not replay its completed source/native/actual/atomic/builder/release/cleanpatch/startup work. Latest finalreview translations/hodram_B52_contextual_final_review_v1.json;manuscriptv6/namesv4/contractv1/atomicV2/configV3 remainimmutable. New owncaptain1 helper scripts/Hodram_B52_registered_route_context_v8707.py uses work/analysis/current_V8704_Hodram_native_v8707/current_native_input.json. No historicalRAMoverlay/captain2. Main4701/canonicalbaseline unchanged;preserveeveryROM/translation/draft/failure. No separatepackage,promotion,pruning,commitorpush.

Next clean source group is SC1B31/B53,three uncredited utterances:two B31 source variants actor34 andone B53 warning actor113. Qualified clean-firstgloss8714 precedes all earlier English forboth. Exact EV1 dependencychain52->31->53 exists:31requires52;53requires31andexcludes74. It doesnot prove continuousscene,chronologicalproximity,original location orcompletioneffectofeitherB52choice. B31'sshort andlong variantsexpress irritation atpersistence andtakingtheopponenton;thelongvariant adds before incurringtheangerofatrulyfrightening man. Do not identify the unnamedman witha sultan/commander/father/speaker/other namedcharacter without sourceevidence. B53 reports apparent wantedstatus byOttomanEmpire andgruff caution;preserve ようだ/とうとう/されちまった anddo not inventbounty,crime,warrant,rank,pursuer,location oroutcome. OriginalB53gloss8712 isretained;8714 explicitlycorrects its incomplete dependency note. These arethree sourceglosses only,not approved English,gates orcredit.

Next map original B31 query/branches/opaque6311/fullend/two22preambles andB53's6000/633F/623F/A000 controls/fullend/71preamble against clean/current native consumers in own verifiedV8704context. Bind source names/roles andactor34 full-header consumers before localization;the earlier Hayreddin surname-component approval isnot a fullheader/catalogue decision. Read complete source branch/context andnative source pages before consulting earlier English. Do not force original predicates/roster/RNG/flags,assume numeric blockadjacency ischronology,or reinterpret structural opaque bridges asgameplay semantics. Continue natural American whole-exchange review,individually justified retentions/fullwidth wrapping,practical town/random/representative focusedrisk evidence,andshared registered cumulative workflow.

Keep all inverse-preserved unfinished scope:allfourstories/earliertranslateddialogue/sharedtown-shop/random/Help/restprose/all207names-roles-aliases-customnames/retrospectiveearlybreaks. Preserve contraction/questiontag/unscanned558plans/weak-before-row/COMMON750-752/preLF6435/wideractors104/105/113/147/JanusPasar-Pasha/ceramics17wrap/Cristina-Christina/HansRetzel-Letzel/Samwellmiddle/SourceItem-LocalProduct/Alexandria/AksumGoldSeal/Armadillo-SteelHide/HerophilusMedicine/イギリス/AlShin-AlFeridShin/Sailor151-159-versus-Retainer andoldernormal-end/nineteenth-cell/B47/B48/B50metadata leads. Graphics/all18plaques andlaterolder-recordtechnicalre-audit remainseparate. Roughly20,000remainingcandidates isonlyaplanningestimate,not an audited prose denominator. Fullgoalactive.'''


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
    assert manifest['profile']==reg['profile']=='all-routes-unified-v8704' and len(manifest['batches'])==646 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())==reg['registry_after_sha256'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert release['all110_release_dialogue_regressions_pass'] and release['whole_clean_input_ROM_reconstruction_byte_exact'] and sha(Path(release['patch']).read_bytes())==release['patch_sha256'] and Path(release['exact_patch_reconstruction']).read_bytes()==candidate.read_bytes()
    assert view['viewed'] and len(view['six_whole_RGB_pairs'])==6 and view['whole_actors_equal'] and view['target_family12_andprotected_Blades8_measured_inactual_coldboot_RAM']
    assert start['all_strict_targetARM9_inverse_Blades_COMMON_directory_and123264_payload_guards_pass'] and start['actual_original_captain_ID']==1 and start['actual_frames']==4001
    assert positive['positive_lifecycles']==2 and positive['one_complete_NDS_commit_percase'] and positive['cases'][0]['report']==positive['cases'][1]['report']
    assert negative['negative_count']==16 and all(c['rejected'] and c['commit_calls']==0 and c['actual_changed_input'] and c['original_object_identity_files_components_andserialized_bytes_unchanged'] for c in negative['cases'])
    assert binding['lifecycle_reports_value_equal'] and binding['genuine_wrong_memory_cases']==3 and binding['semantic_zero_commit_cases']==16
    assert memory['negative_count']==3 and memory['every_wrong_image_rejected_before_commit_withall_guards_active'] and memory['no_digest_orsemantic_bypass']
    assert seal['manuscript_sha256']==sha(DOC.read_bytes()) and seal['name_review_sha256']==sha(NAMES.read_bytes()) and reg['release_config']==str(CONFIG) and reg['release_config_sha256']==sha(CONFIG.read_bytes())
    originals=doc['records']+doc['typed_choice_records']
    assert len(doc['records'])==3 and len(doc['typed_choice_records'])==2 and Counter(r['decision'] for r in originals)==dict(revision=2,retention=3)
    validate_approved_batch(doc);validate_scoped_names(read(NAMES));validate_runtime(NdsImage.open(candidate));check_dependencies(read(CONFIG))
    data={k:read(p) for k,p in proofs().items()}
    assert observed_scope(data)==seal['observed_scope']==positive['cases'][1]['report']['actual_scope']==release['actual_scope_limits']
    assert release['only_SC1_B52_change_324_otherblocks_andall_other_files_components_exact'] and candidate.read_bytes()==Path(doc['reference_ROM']).read_bytes()
    source,context,gloss=map(read,[NEXT_SOURCE,NEXT_CONTEXT_SOURCE,NEXT_GLOSS])
    assert source['source_only_no_current_English_exposed_orused'] and context['source_only_no_current_English_exposed_orused']
    assert gloss['all_three_complete_clean_utterances_glossed_before_earlier_English'] and gloss['current_English_for_B31_andB53_still_unconsulted']
    assert [g['block'] for g in gloss['groups']]==[31,53] and sum(len(g['records']) for g in gloss['groups'])==3 and gloss['explicit_source_event_chain']==[52,31,53]
    assert read('work/analysis/Hodram_B52_build_v8704/build_terminal.json')['returncode']==0 and read('work/analysis/Hodram_B52_registered_context_runs_v8706/route1/terminal.json')['terminal']
    return release


def stage():
    assert not ROOT.exists() and not FINAL.exists();release=gates();prior=read(PRIOR);before=LEDGER.read_bytes();old=json.loads(before);doc=read(DOC)
    assert sha(before)==prior['ledger_sha256'] and tuple(old[k] for k in COUNTERS)==BEFORE and old['goal_status']=='active' and KEY not in old
    originals=doc['records']+doc['typed_choice_records'];oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};keys={historical_key(r) for r in originals}
    assert len(oldkeys)==7229 and len(keys)==5 and not oldkeys&keys
    bank=IlnkContainer.parse(NdsImage.open(release['candidate']).read_file('/data/SC1.DK4')).blocks;mapping=read(proofs()['relocation'])['groups'][0];rows=[]
    for original in originals:
        row=deepcopy(original);target=row['final_reference'];raw=bytes.fromhex(row['final_hex']);block=bank[52];at=target['offset'];typed='option_index' in row
        assert target['block']==52 and sha(block)==target['target_block_sha256'] and block[at:at+len(raw)+1]==raw+b'\0' and block[:at].count(b'\0')==target['record_index']
        command=next(c for c in mapping['all_target_commands'] if c['offset']==target['header_offset']);assert command['word']==(0x2100 if typed else 0x4000)
        body=(raw if typed else raw[1:]).decode('cp932');row['pre_integration_review_record_preserved']=deepcopy(original)
        row.update(predecessor_reference=deepcopy(original['current_reference']),predecessor_hex=original['current_hex'],
            reviewed_against_predecessor_ROM=doc['current_ROM'],reviewed_against_predecessor_ROM_sha256=doc['current_ROM_sha256'],
            current_reference=deepcopy(target),current_hex=raw.hex(),current_text_hex=raw.hex(),current_record_index=target['record_index'],
            current_native_extent=command['native_extent'],current_0100_ancestors=command['ancestor_0100_offsets'],current_raw_storage_English=body,
            current_English=' '.join(body.split()),current_stored_English=body,current_reference_ROM=release['candidate'],current_reference_ROM_sha256=release['candidate_sha256'],
            completed_candidate_reference=deepcopy(target),completed_candidate_sha256=release['candidate_sha256'],
            integrated_reference=dict(**target,stored_hex=raw.hex(),ROM=release['candidate'],ROM_sha256=release['candidate_sha256']),
            source_prose_andcompletion_credit_added_once=True,source_prose_orcompletion_credit_added=True,
            registered_integration_pending=False,current_review_status='integrated-contextual-native-actual-registered-release',already_contextually_completed=True,
            individually_activated_in_current_build=False,actual_initialized_source_andEnglish_selected_paths_observed=True,
            current_observation_scope='RegisteredV8704 equals reviewed reference;6initialized source/English coldboots/50406frames/138holds/12pages cover all3speeches/bothchoices/distinctends. No natural optional activation,original location,live backing/cancel availability,fullroute orhardware claim.',
            actual_proofs={k:proofs()[k] for k in ['actual','opposition_actual','focus_actual','menu_actual','comparison','focus_comparison']},
            editorial_unit_kind='typed-choice' if typed else 'speech',
            actual_live_owner_RAM_VRAM_palette_andunowned_backing_byte_identity_unobserved=True,
            combined_backing_pending_flag_resolved_only_by_separate_offline_native_bounds_andactual_visible_RGB=True)
        if typed:row['predecessor_choice_command_offset']=original['current_choice_command_offset'];row['current_choice_command_offset']=command['offset']
        for key in PENDING_FLAGS:
            if key in row:assert isinstance(row[key],bool);row[key]=False
        row['all_current_editorial_formatting_policy_atomic_registered_requirements_completed']=True
        row['opaque_effect_gameplay_semantics_outer_eligibility_andfuture_causality_remain_unproven']=True
        assert all(row[k]==original[k] for k in ['english','source_hex','source_reference','source_meaning','context','localization_note','retention_reason','review','decision']);rows.append(row)
    summary=INTRO+'\n\n'+DETAILS+'\n\n'+NEXT
    evidence={str(p):sha(Path(p).read_bytes()) for p in [PRIOR,CONFIG,DOC,NAMES,SEAL,RELEASE,START,VIEW,POSITIVE,NEGATIVE,BINDING,MEMORY,REG,NEXT_SOURCE,NEXT_CONTEXT_SOURCE,NEXT_GLOSS,__file__,*proofs().values()]}
    ROOT.mkdir(parents=True)
    save(FINAL,dict(format='dk4-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=rows,revised=2,retained=3,
        source_dialogue_order=[r['id'] for r in sorted(rows,key=lambda r:r['source_reference']['offset'])],
        source_prose_and_completion_credit_added_once=5,physical_speeches=3,typed_choice_labels=2,
        actual_speech_page_occurrences_both_versions=12,actual_complete_body_andname_holds=138,actual_original_optional_activation=False,
        source_fixture_clean_Japanese_body_withcurrent_registered_English_names_UI_code_font=True,
        all_actual_scope_limits_preserved=True,all_source_current_compiled_stored_actual_andintegrated_refs_bound=True,
        all14_commands3_preambles4_relatives_zeroqueries_twochoices4_opaque_bothfullends_andtails_preserved=True,
        both_clean_source_andfull_predecessor_inverses_exact=True,policy_expected_rejections=243,all_independent_technical_rejections=340,
        atomic_semantic_rejections=16,new_all_guard_wrong_memory_rejections=3,shared_precommit_rejections=6,builder_rejections=29,
        one_original_info_zero_warnings_orwaivers_preserved=True,new_registered_startup_frames=4001,
        all_prior_scope_graphics_separation_later_audit_preserved=True,summary=summary,evidence=evidence,full_goal_complete=False))
    new=deepcopy(old);ops=[]
    def put(path,value):
        parent,key=parent_at(new,path);exists=key in parent if isinstance(parent,dict) else key<len(parent)
        ops.append(dict(kind='set',path=path,existed=exists,before=deepcopy(parent[key]) if exists else None));parent[key]=deepcopy(value)
    def append(path,values):
        parent,key=parent_at(new,path);ops.append(dict(kind='append',path=path,before_length=len(parent[key]),count=len(values),appended_sha256=digest(values)));parent[key].extend(deepcopy(values))
    for key,value in zip(COUNTERS,AFTER,strict=True):put([key],value)
    for key in ['completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:
        assert new[key]['/data/SC1.DK4']==149;put([key,'/data/SC1.DK4'],154)
    append(['completed_editorial_families'],[dict(id=FAMILY,file_path='/data/SC1.DK4',blocks=[52],record_IDs=[r['id'] for r in rows],records=rows,
        final_review=str(FINAL),revised_count=2,retained_count=3,fresh_revisions=2,fresh_retentions=3,actual_verification_scope=DETAILS)])
    fp=['contextual_story_natural_dialogue_pass_v1871'];keyrows=[dict(file_path='/data/SC1.DK4',id=r['id']) for r in rows]
    for key in ['record_keys','integrated_record_keys']:append(fp+[key],keyrows)
    append(fp+['record_IDs'],[r['id'] for r in rows])
    for key,value in dict(fresh_pass_records_explicitly_reread=7234,fresh_pass_records_integrated=7234,latest_contextual_manuscript=str(DOC),latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=INTRO).items():put(fp+[key],value)
    append(fp+['reconciled_families'],[dict(id=FAMILY,records=5,physical_speeches=3,typed_choices=2,final_review=str(FINAL),new_revisions=2,justified_retentions=3,
        new_completed_records=5,historical_reconciliation_only=False,actual_optional_event_selected=False,actual_unique_speech_displays=3,actual_typed_options=2,offline_only_objects=0,all_prior_scene_proofs_reused_without_replay=True)])
    if str(DOC) not in new['active_source_prose_drafts']['manuscripts']:append(['active_source_prose_drafts','manuscripts'],[str(DOC)])
    put(['active_source_prose_drafts','route_record_subsets_pending',str(DOC)],[]);put(['active_source_prose_drafts','note'],INTRO)
    ri=next(i for i,u in enumerate(new['coverage_units']) if u['id']=='all-route-scenes')
    assert new['coverage_units'][ri]['reviewed_route_records']==new['coverage_units'][ri]['completed_route_records']==5629
    for key,value in dict(reviewed_route_records=5634,completed_route_records=5634,next=NEXT).items():put(['coverage_units',ri,key],value)
    append(['coverage_units'],[dict(id=FAMILY,status='complete-contextual-native-stored-actual-registered-release',file_path='/data/SC1.DK4',blocks=[52],completion_credit_added=5,
        final_review=str(FINAL),actual_original_optional_activation=False,actual_speeches=3,actual_typed_options=2,full_goal_complete=False)])
    put(['formatting_watchlist',FAMILY],dict(status='three-complete-native-pages-two-typed-choices-both-paths-registered-pass',final_review=str(FINAL),one_original_info_zero_warnings_orwaivers=True,
        native_backing_offline_actual_visible_RGB_scope_preserved=True,all_prior_leads_preserved=True,full_goal_complete=False))
    current=deepcopy(old['current_integrated_candidate']);current.update(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],MESFILE_sha256=release['COMMON_sha256'],
        ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
        status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False,**{f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)})
    put(['current_integrated_candidate'],current);put(['latest_checkpoint'],summary)
    gloss=read(NEXT_GLOSS);pending=dict(status='three-clean-glosses-explicit-dependency-source-controls-names-current-English-format-actual-release-pending',
        source_packets=[dict(path=str(p),sha256=sha(p.read_bytes())) for p in [NEXT_CONTEXT_SOURCE,NEXT_SOURCE]],source_gloss=str(NEXT_GLOSS),source_gloss_sha256=sha(NEXT_GLOSS.read_bytes()),
        source_groups=deepcopy(gloss['groups']),file_path='/data/SC1.DK4',blocks=[31,53],physical_speeches=3,typed_choice_labels=0,
        source_commands_byblock={str(g['block']):len(g['commands']) for g in gloss['groups']},source_selectors=[34,34,113],explicit_EV1_dependency_chain=[52,31,53],
        all_three_glossed_before_earlier_English=True,current_English_forboth_blocks_still_unconsulted=True,source_positions_credited=0,completion_credit_added=0,
        unnamed_frightening_man_andapparent_wanted_status_not_identified_orinflated=True,whole_full_editorial_objective_active=True,full_goal_complete=False)
    oldpending=prior['pending_source_batch'];marker=dict(completion=KEY,final_review=str(FINAL),records=5,all_prior_pending_notes_historical_not_deleted=True,new_credit_added_here=0)
    put([oldpending,'registered_integration_completed_by'],marker);put([NEXT_KEY],pending)
    descriptor=old[prior['unfinished_scope']];assert sha(Path(descriptor['path']).read_bytes())==descriptor['sha256']
    inventory=deepcopy(read(descriptor['path']));inventory['next_focus']=NEXT;inventory[NEXT_KEY]=deepcopy(pending)
    inventory[KEY]=dict(final_review=str(FINAL),completed_objects=5,revisions=2,retentions=3,registered_candidate=release['candidate'],all_previous_limits_andfull_objective_preserved=True)
    if oldpending in inventory:inventory[oldpending]['registered_integration_completed_by']=marker
    for unit in inventory.get('broader_coverage_units',[]):
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=5634,completed_route_records=5634,next=NEXT)
    assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
    scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
    put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,
        incomplete_COMMON=3,incomplete_credited_route_drafts=0,next_clean_exchange_not_yet_selected=False,new_uncredited_clean_source_positions=3,
        graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
    evidence[str(FINAL)]=sha(FINAL.read_bytes());evidence[str(scope)]=sha(scope.read_bytes())
    new[KEY]=dict(summary=summary,next=NEXT,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),evidence=evidence,inverse_operations=ops,record_keys=keyrows,
        new_source_prose_reviews=5,new_completed_records=5,revised=2,retained=3,new_current_candidate_emulator_runs=1,new_current_candidate_frames=4001,
        all_prior_scene_proofs_reused_without_replay=True,all_sessions_terminal_andreaped=True,goal_turn_classification='progress',full_goal_complete=False)
    assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
    assert {historical_key(r) for r in new[fp[0]]['record_keys']}=={historical_key(r) for r in new[fp[0]]['integrated_record_keys']}==oldkeys|keys
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name;prefix=('# Current editorial handoff - V8715; V8704 current\n\n' if name=='editorial_handoff_current.md' else '')+'## V8715: B52 five decisions integrated once in V8704; B31/B53 clean-first context ready\n\n'+summary+'\n\n'
        targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
    files=[]
    for index,(path,value) in enumerate(targets.items()):
        planned=ROOT/f'{index:02d}.after';planned.write_bytes(value)
        if path!=LEDGER:(ROOT/f'{index:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
        files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(value)))
    save(ROOT/'staged_completion.json',dict(files=files,evidence=evidence,all5_records_integrated_once=True,no_shared_mutation_yet=True,full_goal_complete=False))
    print('Staged B52 completion:5disjoint decisions/2revisions/3retentions;all old values recover;independent audit next.')


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
                every_prior_document_preserved_byte_exact=True,exactly5_disjoint_new_records=True,full_goal_complete=False))
            print('B52 deep inverse audit passes;all earlier values/counters/families/candidate/documents recover exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes())
            independent=read('work/analysis/Hodram_B52_completion_audit_v8717/independent_staged_completion_audit.json')
            assert independent['five_disjoint_new_keys_only'] and independent['exact_full_prior_ledger_inverse']
            for entry in plan['files']:
                assert Path(entry['target']).is_relative_to(Path.cwd().resolve()) and Path(entry['planned']).is_relative_to(ROOT.resolve())
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,exactly5_decisions_credited_once=True,current=release['candidate'],mainV4701_preserved=True,full_goal_complete=False))
            print('Applied V8704:7234completed/7237source-prose/4489revised/2745retained;full goal active.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists();prior=read(PRIOR);verified=deepcopy(prior)
            assert len({historical_key(r) for f in new['completed_editorial_families'] for r in f['records']})==7234
            verified.update(candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],ledger_sha256=sha(LEDGER.read_bytes()),
                previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),**dict(zip(COUNTERS,AFTER,strict=True)),
                completed=7234,source_prose=7237,revised=4489,retained=2745,SC0=368,SC1=154,SC2=4915,SC3=197,reviewed_routes=5634,completed_routes=5634,manifest_batches=646,accepted_layers=114,release_checks=18,regressions=110,
                Hodram_B52_completed_once=True,Hodram_B52_atomic_registered_integration_pending=False,registered_builder_11577_pending_as_observed=False,
                final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch=NEXT_KEY,next_clean_exchange_not_selected=False,
                new_uncredited_source_positions=3,physical_speeches_pending=3,typed_choice_labels_pending=0,new_credit=5,new_emulator_runs=1,new_actual_frames=4001,
                all_sessions_terminal_andreaped=True,all_new_native_jobs_terminal_andreaped=True,all_prior_roots_families_records_andcounts_recover_exactly=True,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV8716/currentV8704:7234completed,5B52decisions credited once;B31/B53three clean glosses/olderEnglishunread;full goal active.')
