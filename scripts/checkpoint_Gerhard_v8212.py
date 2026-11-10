"""Checkpoint clean Hodram/source/current-native/name concern proofs without newcredit;full goalactive."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.complete_Rafael_B50_v8184 import COUNTERS,AFTER
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Gerhard_checkpoint_v8212')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8213')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8195/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/gerhard_surname_consistency_manuscript_v1.json')
NAMES=Path('translations/hodram_B137_B45_B46_speaker_name_review_v2.json')
KEY='Gerhard_Adernkatz_native_sparse_pending_actual_registered_andHodram28_v8212'
OLD_KEY='Hodram_SC1B137_B45_B46_source_native_pending_surname_current_prose_release_v8194'
SCOPE='unfinished_editorial_scope_v8212'
PROOFS={'source137': 'work/analysis/Hodram_B137_clean_context_v8180/complete_clean_SC1_B137_EV1_andcoverage_before_current_English.json', 'source45': 'work/analysis/Hodram_next_clean_v8178/complete_clean_SC1_B45_EV1_andcoverage_before_current_English.json', 'source46': 'work/analysis/Hodram_B46_clean_context_v8179/complete_clean_SC1_B46_EV1_andcoverage_before_current_English.json', 'clean_names': 'work/analysis/Hodram_B137_B45_B46_clean_names_v8182/six_clean_static_identity_fields_before_current_English.json', 'gloss': 'work/analysis/Hodram_B137_B45_B46_clean_gloss_v8183/28_first_clean_glosses_six_identities_explicit_prerequisite_graph_before_current_English.json', 'prior_B44': 'work/analysis/Hodram_B137_B45_B46_clean_gloss_v8183/27_prior_clean_B44_source_refs_exact_no_new_credit.json', 'current_input': 'work/analysis/current_V8172_Hodram_native_v8187/current_native_input.json', 'startup': 'work/analysis/Hodram_current_binding_v8187/own_Hodram_startup_andstrict_captain1_context.json', 'startup_view': 'work/analysis/Hodram_current_startup_view_v8189/own_Hodram_startup_sheet_viewed.json', 'controls': 'work/analysis/Hodram_B137_B45_B46_source_controls_v8188/three_EV1_entries60_commands28_speeches_native_relative_predicate_and75_seeded_ends.json', 'picture': 'work/analysis/Hodram_B46_pigment_v8190b/original4800_descriptor181_clean_current_Red_Dye_andbounded_consumer_path.json', 'paths': 'work/analysis/Hodram_B137_B45_B46_source_paths_v8191/11_structural_compositions_all60_commands28_source_memberships.json', 'native_names': 'work/analysis/Hodram_B137_B45_B46_names_v8192/six_static_speakers12_getters_clean_fields24_synthetic_macro_alignments.json', 'names': 'translations/hodram_B137_B45_B46_speaker_name_review_v2.json', 'surname_source': 'work/analysis/Hodram_B137_B45_B46_name_review_v8193/five_clean_surname_mentions_selfintro_andprior_name_decision.json', 'consumers': 'work/analysis/Gerhard_surname_consumers_v8196/all20_current_Latin_occurrences_five_whole_clean_exchanges.json', 'Lil_input': 'work/analysis/current_V8172_Lil_native_v8198/current_native_input.json', 'Lil_startup': 'work/analysis/Lil_Gerhard_current_binding_v8198/own_Lil_startup_andstrict_captain2_context.json', 'five_refs': 'work/analysis/Gerhard_surname_five_v8199/five_prior_completed_source_current_refs_andwhole295_source_context_receipt.json', 'before_names': 'work/analysis/Gerhard_before_names_v8200/four_identities8_getters3_source_voices16_synthetic_Lil_alignments.json', 'effective': 'work/analysis/Gerhard_surname_effective_v8201/all5_effective_English_templates10_original_dispatches_no_FE.json', 'manuscript': 'translations/gerhard_surname_consistency_manuscript_v1.json', 'ownership': 'work/analysis/Gerhard_name_ownership_v8203/current12_byte_surname_owned_original20_contains_protected_Blades.json', 'logical': 'work/analysis/Gerhard_logical_v8204/5_logical_paragraphs20_original_native_alignments.json', 'plan': 'work/analysis/Gerhard_layout_v8205/5_automatic_Lil_plans_full_native_width.json', 'pages': 'work/analysis/Gerhard_pages_v8206/5_complete_native_paragraphs5_pages20_compiled_alignments.json', 'page_view': 'work/analysis/Gerhard_native_review_v8207/five_native_pages_directly_viewed_one_info_zero_warnings.json', 'relocation': 'work/analysis/Gerhard_sparse_relocation_v8208b/two_blocks_five_sparse_revisions_all_commands_native_relative_cases_full_predecessor_inverse.json', 'stored': 'work/analysis/Gerhard_stored_v8209/5_stored_bodies4_fresh16_reused_alignments5_exact_viewed_pages.json', 'target_name': 'work/analysis/Gerhard_target_name_v8210c/owned12byte_input8_getters4_complete_name_planes_Blades_protected.json', 'target_name_view': 'work/analysis/Gerhard_name_view_v8211/four_name_planes_directly_viewed_research_input_only.json'}
SUMMARY="Current registered cumulative remains V8172; main V4701 unchanged. Counts remain 7171 completed, 7174 source/prose and drafts, 4455 integrated revisions and 2716 retentions; SC0 368, SC1 91, SC2 4915, SC3 197, COMMON 1600 complete/1603 source-prose, route subset 5571. V8172 still has 639 manifest batches,114 accepted layers,18 release checks,110 regressions,exact clean-input patch and verified full-reference/startup evidence. No separate unified test package,promotion,pruning,commit orpush. Full editorial goal active.\n\nGerhard surname localization is now decided as Adernkatz after all295 clean speeches across SC0B84/B85,SC2B27/B74 andSC3B59 were read in complete exchanges. Current census has14 Adernkatz occurrences and6 inconsistent Ardelknatts consumers:one ARM9 family field andfive previously completed SC2 speeches. The established Adernkatz follows the cleanアーデルンカッツ sequence;no official Latin canon,historical identity ornew biography is claimed. Preserve allother prose with individual reasons. New Hodram namesv2 records five justified retentions andGerhard revision;allfour prose gates true,formatting false. Earlier namesv1 andallprior approvals remain historical evidence. Initial discovery exposed existing surname snippets before full295-source reread;this is not claimed as a blind new translation. The28 pending Hodram dialogue English bodies remain unconsulted anduncredited.\n\nImportant ownership correction:the original20-byte Japanese name allocation now contains Ardelknatts-NUL followed by separately referenced Blades-NUL-NUL. Only the current12-byte terminated name span is owned for this correction. Exact literal-pointer census finds actor16 surname reference,no interior aliases,andthe separate Blades pointer. Target is Adernkatz-NUL plus two zeros;allother ARM9 bytes,pointer fields andBlades stay exact,with full ARM9 inverse. Do not write the original20-byte slot orclaim arbitrary dynamic-pointer proof. Initial20-byte assumption failed before output mutation;preserve producer8202 andsuccessor8202b. No ROM name asset has changed.\n\nFresh own-current Lil ordinary NewGame ran4001frames withactualcaptain2,strict123264 payload/2b6 ARM9/COMMON/directory guards anddirectstartup view;no optional Stockholm/Hamburg activation. Own Lil input8198 complements current Rafael8175/Hodram8187;other routes historical until rebound. Eight current name getters,three source voices,16 synthetic default alignments prove Lil3/Argot5/ArgotCo.9. Five current/source bodies have10 original dispatches andzero catalogue matches. Logical five paragraphs pass20 original native alignments,sourceFI1/noFAFO. Private Lil automatic layout uses216px/four physical rows,exact source01/09/10,full NUL/phase/guard rules andno global changes. Five complete one-page native bodies/20 compiled alignments pass independent first/internal/final glyph masks,bounds andconsumption. One native body sheet directly viewed;zero warnings andone unchanged line-break-count info. Gerhard Adernkatz andIt's been remain coherent;no manualwraps/padding/shortening.\n\nSparse research reconstruction changes onlyfive speeches inSC2B27/B74 andpreserves125 other speeches,all130 six-byte preambles,225 commands,nested scopes,opaque effects,complete four-byte terminals andseparate tails. All44 relative sites pass220 clean+220 current+220 target native structural cases;these are not gameplay branches orproof ofall attainable states. Exact prior Hamburg typed choice Yes,please./No need. isbound through approved relocation map,retained unchanged. Initial8208 treated it as untranslated opaque bytes andcorrectly stopped after partial block27;preserve failure and8208b successor. B27 2972stored/2970logical/tail2 becomes2968stored/2966logical/tail2;B74 4824stored/4824logical/tail0 becomes4820stored/4818logical/tail2. All predecessor block/archive bytes invert exactly;334 otherSC2 blocks exact. Full clean TEXT inverse isnot claimed for sparse changes:allother prior translations stay. One compiler parity tail atB74R185 gets4fresh native alignments;four exact bodies reuse16. Allfive stored ink planes equal directly viewed pages,with no extra/blank page.\n\nDisclosed CPU-only target-name input changes exactly12 RAM bytes under original current instruction guards,not a new-ROM snapshot oractualgameplay. Eight progressive/full getters pass:onlyGerhard two strings becomeGerhardAdernkatz;Hodram/Joakim/Lil/Camille/Marinus remain exact. Four complete style11 planes (currentheader,proposedheader,surname,given) pass independent exact-current font masks andbounds;sheet directly viewed. Blades andallunowned RAM remain exact andentire research input inverses. Preserve8210 helper-binding failure and8210b older-font-oracle hash rejection;8210c uses existing exact2b6 oracle withallguards preserved. This does not claim actual catalogue geometry,customname coverage,currentnameasset,newROM startup oroptionalscene gameplay.\n\nNo new ROM orregistry change inthischeckpoint;five speeches remain priorrevisions withzero duplicate source/prose/completed/revised/retained credit. Allfive final formatting gates remainfalse. Fullreference,finalcontrol/endcarry/loaders/callers,representative actual name/body/transition coverage,frozenpolicy,atomicproduction,registered cumulative/exactcleanpatch/startup remainpending. All28 Hodram source/context/native controls/item/path proofs remain verified anduncredited. Broaderfour-story/sharedtown-shop/random/Help/remainingprose/207names/retrospectivewrap scope,graphics andlaterolder-record technicalre-audit remainintact."
NEXT='Continue from verifiedV8213/currentregisteredV8172. Reuse Gerhard sourceconsumer/name decision8196-8203,own Lil8198,logical8204,plan8205,pages8206/view8207,sparse relocation8208b,stored8209,targetname8210c/view8211. Build an isolated pinned research fullreference changingonlyARM9 owned12-byte surname andSC2five bodies;allother files/components/334otherblocks/125otherparagraphs/Blades exact. Finish current/target dispatch,all225 original commands/44 relative sites/preserved typedchoice/rawqueries/fullfour-byte ends andvaluecarry,fullreference caller/load/cache tests. Use representative actual surname/nameheader/body andscene/transition checks withdisclosed initialization scope,not exhaustiveconditionalvisits. Freeze natural-dialogue-v2/referencepolicy,independentatomicguards andmeaningful precommit corruption tests;then registered cumulative after full639-stack,exactapprovedfullreference/clean-inputpatch/appropriate regressions/ownstartup. No duplicate credit forfive alreadycompleted revisions. MainV4701 unchanged;no promotion,separateunifiedpackage,pruning,commit orpush.\n\nThe28 HodramSC1B137/B45/B46 bodies remain pending clean-first contextual English comparison,manuscript,route-aware layout/nativeglyphs/storedcontrols/actualdistinct4800layout0 andhide4700/silences/normalreturns/policy/registeredrelease. Sourcegloss8183/ownHodram8187/controls8188/picture8190b/paths8191/names8192 are verified;Hodram namev2 nowdepends on explicit registered Adernkatz correction,not unresolvedLatinlexicon orsilentglobalrename. Current English body mapping/prose review may proceed independently,while no H1 integration may omit the name dependency. Preserve formalrestrainedHodram,hesitantCamille,bluntCharles,practicalGerhard andcompetitiveLil;no invented ranks,kinship,romance,recruitment guarantees,mapgift/ownership/accepted orwoncontest.\n\nKeepfullobjectiveallfourstories/earliertranslateddialogue/sharedshops-towns/random/Help/remainingprose/all207names-roles-aliases/retrospectiveearlybreaks. Preserveeverypriorunfinishedinventory,12contraction/questiontagleads,unscannedbeyond558plans,weak-before-row/page-before-readability/phrasecoherence. KeepPasardistinctfromPasha,Cristina/Christina,HansRetzel/Letzel,Trader/PortWorker/Guildmaster,Sailor151-159versusRetainerconsumers,COMMON750-752,preLF6435,ArmadilloHide/SteelHide,HerophilusMedicine,AksumGoldSeal,AlShin/AlFeridShin,イギリス andallrecordeditem/counterpart/displayleads. Graphics/all18plaques andlaterolder-recordtechnicalre-audit separate:normalendcarry,B35R65/B48R129source19thcells,B48stalerelocationlabel,B47correctedregistrationreceipt,B50checkpoint8149blocklabelcompanion,andalltiming/highlight/RNG/component/byte/calendar/RGB/fixture-reentrylimits. PreserveallROMs/translations/drafts/failures/executedproducers/proofs. MainV4701unchanged;no separateunifiedpackage,promotion,pruning,commit orpush. Fullgoalactive.'

def restore(value):
    result=deepcopy(value);entry=result.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(result,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return result
def gates():
    prior,doc,names=map(read,[PRIOR,DOC,NAMES]);data={k:read(p) for k,p in PROOFS.items()}
    assert prior['completed']==7171 and prior['manifest_batches']==639
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']==data['Lil_input']['current_ROM_sha256']
    assert sha(Path(prior['patch']).read_bytes())==prior['patch_sha256']
    assert len(doc['records'])==5 and all(r['already_editorially_completed'] and r['previous_credit_classification']=='revised-and-integrated' for r in doc['records'])
    assert all(all(r['review'][k] for k in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in doc['records'])
    assert len(names['records'])==6 and sum(r['decision']=='retention' for r in names['records'])==5 and sum(r['decision']=='revision' for r in names['records'])==1
    assert all(all(r['review'][k] for k in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in names['records'])
    assert data['five_refs']['all295_clean_records_reviewed_for_name_identity_context_not_full_new_prose_credit']
    assert data['five_refs']['current_Hodram_B137_B45_B46_body_English_still_unconsulted']
    assert data['Lil_startup']['actual_original_captain_ID']==2 and data['Lil_startup']['actual_frames']==4001
    assert data['Lil_startup']['all_strict2b6_COMMON_directory_and123264_payload_guards_pass']
    assert data['before_names']['measured_default_macro_lengths']==dict(FI=3,FA=5,FO=9)
    assert len(data['effective']['effective_current_records'])==5 and len(data['effective']['source_current_dispatches'])==10
    assert data['ownership']['current_owned_name_span']['bytes']==12 and data['ownership']['protected_neighbor']['text']=='Blades'
    assert not data['ownership']['interior_name_literal_pointer_references'] and data['ownership']['whole_ARM9_inverse_recovers_exact_current']
    assert data['logical']['total_bound_alignment_cases']==20 and data['logical']['source_macro_totals']==dict(FI=1,FA=0,FO=0)
    assert len(data['plan']['records'])==5 and not data['plan']['failures']
    assert sum(i['severity']=='info' for r in data['plan']['records'] for i in r['base_QA']['issues'])==1
    assert not any(i['severity'] in ['warning','error'] for r in data['plan']['records'] for i in r['base_QA']['issues'])
    assert data['pages']['complete_progressive_pages']==5 and data['pages']['fresh_compiled_alignment_cases']==20
    assert data['page_view']['all_five_complete_bodies_visually_read'] and data['page_view']['pages_sha256']==sha(Path(PROOFS['pages']).read_bytes())
    rel=data['relocation'];assert len(rel['groups'])==2 and rel['source_relative_sites']==44
    assert rel['clean_native_skip_cases']==rel['current_native_skip_cases']==rel['target_native_skip_cases']==220
    assert sum(len(g['all_target_commands']) for g in rel['groups'])==225 and rel['all125_other_speeches_unchanged'] and rel['other_archive_blocks_exact']==334
    assert rel['all_full_predecessor_archive_bytes_reconstructed_exactly']
    assert sha(Path(rel['target_archive']).read_bytes())==rel['target_archive_sha256']
    stored=data['stored'];assert len(stored['records'])==5 and stored['fresh_native_alignment_cases']==4 and stored['exact_reused_native_alignment_cases']==16
    target=data['target_name'];assert len(target['native_eight_getters']['rows'])==8 and len(target['planes'])==4
    assert target['CPU_only_owned_data_input_not_current_ROM_change_actual_scene_ornew_ROM_startup'] and target['protected_Blades_bytes_andall_other_RAM_exact']
    assert data['target_name_view']['viewed'] and data['target_name_view']['name_proof_sha256']==sha(Path(PROOFS['target_name']).read_bytes())
    assert len(data['gloss']['records'])==28 and all(r['current_English_body_not_yet_consulted'] for r in data['gloss']['records'])
    registry=read('translations/release_stack.json');assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    return prior,data

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    prior,data=gates()
    if mode=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==prior['ledger_sha256'] and tuple(old[k] for k in COUNTERS)==AFTER
        assert old['goal_status']=='active' and not old['full_goal_complete'] and KEY not in old and SCOPE not in old and OLD_KEY in old
        new=deepcopy(old);ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);exists=key in parent
            ops.append(dict(path=path,existed=exists,before=deepcopy(parent[key]) if exists else None));parent[key]=deepcopy(value)
        previous_scope=old[prior['unfinished_scope']]
        assert sha(Path(previous_scope['path']).read_bytes())==previous_scope['sha256']
        inventory=deepcopy(read(previous_scope['path']));inventory['next_focus']=NEXT
        evidence={str(p):sha(Path(p).read_bytes()) for p in [PRIOR,DOC,NAMES,Path(__file__),*map(Path,PROOFS.values())]}
        pending=dict(status='Adernkatz-source-localization-five-native-pages-sparse-relocation-andstored-pass-pending-final-controls-actual-registered-release',
            manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),
            corrected_name_target='Gerhard Adernkatz',registered_name_asset_not_yet_changed=True,
            corrected_five_existing_body_records=5,file_path='/data/SC2.DK4',blocks=[27,74],
            prior_completed_revisions_revisited_no_duplicate_credit=True,complete_clean_name_context_speeches=295,
            logical_alignments=20,compiled_alignments=20,native_complete_pages=5,source_relative_sites=44,
            clean_current_target_native_structural_cases=660,all125_other_speeches_andtyped_choice_preserved=True,
            stored_fresh_alignments=4,stored_exact_reused_alignments=16,
            owned_ARM9_name_span_bytes=12,protected_neighbor='Blades',CPU_only_target_getters=8,complete_name_input_planes=4,
            owned_CPU_input_not_current_ROM_oractual_scene=True,
            source_Hodram_pending_reference=OLD_KEY,Hodram_blocks=[137,45,46],Hodram_objects=28,Hodram_current_body_English_unconsulted=True,
            own_Lil_native_input=PROOFS['Lil_input'],all_proofs=PROOFS,current_ROM=prior['candidate'],current_ROM_sha256=prior['candidate_sha256'],
            new_credit=0,new_emulator_runs=1,new_actual_frames=4001,new_optional_scene_runs=0,full_goal_complete=False)
        inventory[KEY]=deepcopy(pending)
        if OLD_KEY in inventory:inventory[OLD_KEY]['superseded_by']=dict(checkpoint=KEY,Gerhard_source_localization_native_pages_sparse_andstored_checks_now_pass=True,surname_asset_actual_registered_andHodram_bodyEnglish_pending=True,new_credit=0)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,
            incomplete_COMMON=3,incomplete_credited_route_drafts=0,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
        put([OLD_KEY,'superseded_by'],dict(checkpoint=KEY,Gerhard_source_localization_native_pages_sparse_andstored_checks_now_pass=True,surname_asset_actual_registered_andHodram_bodyEnglish_pending=True,new_credit=0))
        put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        new[KEY]=dict(**pending,summary=SUMMARY,next=NEXT,evidence=evidence,inverse_operations=ops,goal_turn_classification='progress',all_sessions_terminal_andreaped=True)
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['current_integrated_candidate']==old['current_integrated_candidate']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        section='## V8212: Gerhard Adernkatz decision andfive native surname pages verified; actual andregistered correction pending\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name
            prefix=('# Current editorial handoff - V8212; V8172 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,value) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(value)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(value)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,unchanged_counters=list(AFTER),new_credit=0,full_goal_complete=False))
        print('Gerhard name/native/sparse checkpoint staged;six targets,zero credit.Deep inverse audit next.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
        for entry in plan['files']:
            assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256']
            assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),
                deep_inverse_recovers_every_prior_root_family_record_counter_andcandidate=True,
                full_goal_all_prior_leads_andnew_native_stored_limits_preserved=True,new_credit=0,full_goal_complete=False))
            print('Deep inverse passes;every prior ledger value,candidate,count andunfinished lead recovers exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes())
            for entry in plan['files']:
                assert Path(entry['target']).is_relative_to(Path.cwd().resolve()) and Path(entry['planned']).is_relative_to(ROOT.resolve())
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_prior_values_reversible=True,new_credit=0,full_goal_complete=False))
            print('Gerhard name/native/sparse checkpoint applied;currentV8172 andallcompletion counts unchanged.Full goal active.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists()
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),
                previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch=KEY,
                strict_own_Lil_current_input=PROOFS['Lil_input'],
                Gerhard_surname_correction_checkpoint=dict(target='Gerhard Adernkatz',prior_completed_speeches=5,source_context_speeches=295,
                    logical_alignments=20,compiled_alignments=20,complete_pages=5,relative_sites=44,clean_current_target_native_cases=660,
                    stored_fresh=4,stored_reused=16,owned_name_bytes=12,protected_neighbor='Blades',CPU_input_getters=8,complete_name_planes=4,
                    new_optional_scene_runs=0,new_ROMs=0,asset_actual_andregistered_release_pending=True),
                new_credit=0,new_emulator_runs=1,new_actual_frames=4001,all_sessions_terminal_andreaped=True,
                all_prior_roots_families_records_andcounts_recover_exactly=True,full_goal_active=True,full_goal_complete=False,
                producer_sha256=sha(Path(__file__).read_bytes()))
            verified['Hodram_source_native_checkpoint'].update(name_surname_concern_pending=False,surname_registered_asset_pending=True,current_dialogue_English_unconsulted=True)
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV8213/currentV8172:7171completed;Gerhard Adernkatz decision/5 native pages/660 branch cases/stored/name planes pass.Asset/actual/registered andHodram28 prose pending.Full goal active.')
