"""Prepare reversible zero-credit progress checkpoint; preserve full goal and every prior value."""
import ast
from pathlib import Path
from scripts import checkpoint_Hodram_source_v8194 as previous
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Gerhard_checkpoint_tools_v8212')
PROOFS={**previous.PROOFS,
 'names':'translations/hodram_B137_B45_B46_speaker_name_review_v2.json',
 'consumers':'work/analysis/Gerhard_surname_consumers_v8196/all20_current_Latin_occurrences_five_whole_clean_exchanges.json',
 'Lil_input':'work/analysis/current_V8172_Lil_native_v8198/current_native_input.json',
 'Lil_startup':'work/analysis/Lil_Gerhard_current_binding_v8198/own_Lil_startup_andstrict_captain2_context.json',
 'five_refs':'work/analysis/Gerhard_surname_five_v8199/five_prior_completed_source_current_refs_andwhole295_source_context_receipt.json',
 'before_names':'work/analysis/Gerhard_before_names_v8200/four_identities8_getters3_source_voices16_synthetic_Lil_alignments.json',
 'effective':'work/analysis/Gerhard_surname_effective_v8201/all5_effective_English_templates10_original_dispatches_no_FE.json',
 'manuscript':'translations/gerhard_surname_consistency_manuscript_v1.json',
 'ownership':'work/analysis/Gerhard_name_ownership_v8203/current12_byte_surname_owned_original20_contains_protected_Blades.json',
 'logical':'work/analysis/Gerhard_logical_v8204/5_logical_paragraphs20_original_native_alignments.json',
 'plan':'work/analysis/Gerhard_layout_v8205/5_automatic_Lil_plans_full_native_width.json',
 'pages':'work/analysis/Gerhard_pages_v8206/5_complete_native_paragraphs5_pages20_compiled_alignments.json',
 'page_view':'work/analysis/Gerhard_native_review_v8207/five_native_pages_directly_viewed_one_info_zero_warnings.json',
 'relocation':'work/analysis/Gerhard_sparse_relocation_v8208b/two_blocks_five_sparse_revisions_all_commands_native_relative_cases_full_predecessor_inverse.json',
 'stored':'work/analysis/Gerhard_stored_v8209/5_stored_bodies4_fresh16_reused_alignments5_exact_viewed_pages.json',
 'target_name':'work/analysis/Gerhard_target_name_v8210c/owned12byte_input8_getters4_complete_name_planes_Blades_protected.json',
 'target_name_view':'work/analysis/Gerhard_name_view_v8211/four_name_planes_directly_viewed_research_input_only.json',
}
SUMMARY=(
 'Current registered cumulative remains V8172; main V4701 unchanged. Counts remain 7171 completed, 7174 source/prose and drafts, 4455 integrated revisions and 2716 retentions; SC0 368, SC1 91, SC2 4915, SC3 197, COMMON 1600 complete/1603 source-prose, route subset 5571. '
 'V8172 still has 639 manifest batches,114 accepted layers,18 release checks,110 regressions,exact clean-input patch and verified full-reference/startup evidence. No separate unified test package,promotion,pruning,commit orpush. Full editorial goal active.\n\n'
 'Gerhard surname localization is now decided as Adernkatz after all295 clean speeches across SC0B84/B85,SC2B27/B74 andSC3B59 were read in complete exchanges. '
 'Current census has14 Adernkatz occurrences and6 inconsistent Ardelknatts consumers:one ARM9 family field andfive previously completed SC2 speeches. '
 'The established Adernkatz follows the cleanアーデルンカッツ sequence;no official Latin canon,historical identity ornew biography is claimed. Preserve allother prose with individual reasons. '
 'New Hodram namesv2 records five justified retentions andGerhard revision;allfour prose gates true,formatting false. Earlier namesv1 andallprior approvals remain historical evidence. '
 'Initial discovery exposed existing surname snippets before full295-source reread;this is not claimed as a blind new translation. The28 pending Hodram dialogue English bodies remain unconsulted anduncredited.\n\n'
 'Important ownership correction:the original20-byte Japanese name allocation now contains Ardelknatts-NUL followed by separately referenced Blades-NUL-NUL. '
 'Only the current12-byte terminated name span is owned for this correction. Exact literal-pointer census finds actor16 surname reference,no interior aliases,andthe separate Blades pointer. '
 'Target is Adernkatz-NUL plus two zeros;allother ARM9 bytes,pointer fields andBlades stay exact,with full ARM9 inverse. Do not write the original20-byte slot orclaim arbitrary dynamic-pointer proof. '
 'Initial20-byte assumption failed before output mutation;preserve producer8202 andsuccessor8202b. No ROM name asset has changed.\n\n'
 'Fresh own-current Lil ordinary NewGame ran4001frames withactualcaptain2,strict123264 payload/2b6 ARM9/COMMON/directory guards anddirectstartup view;no optional Stockholm/Hamburg activation. '
 'Own Lil input8198 complements current Rafael8175/Hodram8187;other routes historical until rebound. Eight current name getters,three source voices,16 synthetic default alignments prove Lil3/Argot5/ArgotCo.9. '
 'Five current/source bodies have10 original dispatches andzero catalogue matches. Logical five paragraphs pass20 original native alignments,sourceFI1/noFAFO. '
 'Private Lil automatic layout uses216px/four physical rows,exact source01/09/10,full NUL/phase/guard rules andno global changes. Five complete one-page native bodies/20 compiled alignments pass independent first/internal/final glyph masks,bounds andconsumption. '
 'One native body sheet directly viewed;zero warnings andone unchanged line-break-count info. Gerhard Adernkatz andIt\'s been remain coherent;no manualwraps/padding/shortening.\n\n'
 'Sparse research reconstruction changes onlyfive speeches inSC2B27/B74 andpreserves125 other speeches,all130 six-byte preambles,225 commands,nested scopes,opaque effects,complete four-byte terminals andseparate tails. '
 'All44 relative sites pass220 clean+220 current+220 target native structural cases;these are not gameplay branches orproof ofall attainable states. '
 'Exact prior Hamburg typed choice Yes,please./No need. isbound through approved relocation map,retained unchanged. Initial8208 treated it as untranslated opaque bytes andcorrectly stopped after partial block27;preserve failure and8208b successor. '
 'B27 2972stored/2970logical/tail2 becomes2968stored/2966logical/tail2;B74 4824stored/4824logical/tail0 becomes4820stored/4818logical/tail2. '
 'All predecessor block/archive bytes invert exactly;334 otherSC2 blocks exact. Full clean TEXT inverse isnot claimed for sparse changes:allother prior translations stay. '
 'One compiler parity tail atB74R185 gets4fresh native alignments;four exact bodies reuse16. Allfive stored ink planes equal directly viewed pages,with no extra/blank page.\n\n'
 'Disclosed CPU-only target-name input changes exactly12 RAM bytes under original current instruction guards,not a new-ROM snapshot oractualgameplay. '
 'Eight progressive/full getters pass:onlyGerhard two strings becomeGerhardAdernkatz;Hodram/Joakim/Lil/Camille/Marinus remain exact. '
 'Four complete style11 planes (currentheader,proposedheader,surname,given) pass independent exact-current font masks andbounds;sheet directly viewed. Blades andallunowned RAM remain exact andentire research input inverses. '
 'Preserve8210 helper-binding failure and8210b older-font-oracle hash rejection;8210c uses existing exact2b6 oracle withallguards preserved. '
 'This does not claim actual catalogue geometry,customname coverage,currentnameasset,newROM startup oroptionalscene gameplay.\n\n'
 'No new ROM orregistry change inthischeckpoint;five speeches remain priorrevisions withzero duplicate source/prose/completed/revised/retained credit. '
 'Allfive final formatting gates remainfalse. Fullreference,finalcontrol/endcarry/loaders/callers,representative actual name/body/transition coverage,frozenpolicy,atomicproduction,registered cumulative/exactcleanpatch/startup remainpending. '
 'All28 Hodram source/context/native controls/item/path proofs remain verified anduncredited. Broaderfour-story/sharedtown-shop/random/Help/remainingprose/207names/retrospectivewrap scope,graphics andlaterolder-record technicalre-audit remainintact.'
)
NEXT=(
 'Continue from verifiedV8213/currentregisteredV8172. Reuse Gerhard sourceconsumer/name decision8196-8203,own Lil8198,logical8204,plan8205,pages8206/view8207,sparse relocation8208b,stored8209,targetname8210c/view8211. '
 'Build an isolated pinned research fullreference changingonlyARM9 owned12-byte surname andSC2five bodies;allother files/components/334otherblocks/125otherparagraphs/Blades exact. '
 'Finish current/target dispatch,all225 original commands/44 relative sites/preserved typedchoice/rawqueries/fullfour-byte ends andvaluecarry,fullreference caller/load/cache tests. '
 'Use representative actual surname/nameheader/body andscene/transition checks withdisclosed initialization scope,not exhaustiveconditionalvisits. '
 'Freeze natural-dialogue-v2/referencepolicy,independentatomicguards andmeaningful precommit corruption tests;then registered cumulative after full639-stack,exactapprovedfullreference/clean-inputpatch/appropriate regressions/ownstartup. '
 'No duplicate credit forfive alreadycompleted revisions. MainV4701 unchanged;no promotion,separateunifiedpackage,pruning,commit orpush.\n\n'
 'The28 HodramSC1B137/B45/B46 bodies remain pending clean-first contextual English comparison,manuscript,route-aware layout/nativeglyphs/storedcontrols/actualdistinct4800layout0 andhide4700/silences/normalreturns/policy/registeredrelease. '
 'Sourcegloss8183/ownHodram8187/controls8188/picture8190b/paths8191/names8192 are verified;Hodram namev2 nowdepends on explicit registered Adernkatz correction,not unresolvedLatinlexicon orsilentglobalrename. '
 'Current English body mapping/prose review may proceed independently,while no H1 integration may omit the name dependency. Preserve formalrestrainedHodram,hesitantCamille,bluntCharles,practicalGerhard andcompetitiveLil;no invented ranks,kinship,romance,recruitment guarantees,mapgift/ownership/accepted orwoncontest.\n\n'
 +previous.NEXT[previous.NEXT.index('Keepfullobjective'):]
)

if __name__=='__main__':
    assert not ROOT.exists();source=Path(previous.__file__).read_text('utf8');tree=ast.parse(source)
    assignments={n.targets[0].id:ast.get_source_segment(source,n) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)}
    gates_old=next(ast.get_source_segment(source,n) for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='gates')
    pending_old=source[source.index('        pending=dict('):source.index('        inventory[KEY]=')]
    verify_old=source[source.index('            verified=deepcopy(prior);'):source.index('            VERIFY.mkdir')]
    gates='''def gates():
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
    return prior,data'''
    pending='''        pending=dict(status='Adernkatz-source-localization-five-native-pages-sparse-relocation-andstored-pass-pending-final-controls-actual-registered-release',
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
'''
    verify='''            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),
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
'''
    newvalues={
        'ROOT':"Path('work/analysis/Gerhard_checkpoint_v8212')",'VERIFY':"Path('work/analysis/editorial_handoff_verification_v8213')",
        'PRIOR':"Path('work/analysis/editorial_handoff_verification_v8195/verified_handoff.json')",'DOC':"Path('translations/gerhard_surname_consistency_manuscript_v1.json')",
        'NAMES':"Path('translations/hodram_B137_B45_B46_speaker_name_review_v2.json')",'KEY':repr('Gerhard_Adernkatz_native_sparse_pending_actual_registered_andHodram28_v8212'),
        'OLD_KEY':repr(previous.KEY),'SCOPE':repr('unfinished_editorial_scope_v8212'),'PROOFS':repr(PROOFS),'SUMMARY':repr(SUMMARY),'NEXT':repr(NEXT),
    }
    changes={assignments[k]:k+'='+v for k,v in newvalues.items()}
    changes.update({gates_old:gates,pending_old:pending,verify_old:verify,
        'own_Hodram_context_source_controls_paths_item_andnative_name_getters_now_pass=True,surname_editorial_concern_andbodyEnglish_native_actual_release_pending=True':
        'Gerhard_source_localization_native_pages_sparse_andstored_checks_now_pass=True,surname_asset_actual_registered_andHodram_bodyEnglish_pending=True',
        '## V8194: Hodram clean-source/current-native controls, item andnames bound; surname/body/prose/release pending':
        '## V8212: Gerhard Adernkatz decision andfive native surname pages verified; actual andregistered correction pending',
        '# Current editorial handoff - V8194; V8172 current':'# Current editorial handoff - V8212; V8172 current',
        'Hodram source/native checkpoint staged;six targets,zero credit.Deep inverse audit next.':'Gerhard name/native/sparse checkpoint staged;six targets,zero credit.Deep inverse audit next.',
        'Hodram source/native checkpoint applied;currentV8172 andallcompletion counts unchanged.Full goal active.':'Gerhard name/native/sparse checkpoint applied;currentV8172 andallcompletion counts unchanged.Full goal active.',
        'VerifiedV8195/currentV8172:7171completed;Hodram60commands/28cleanglosses/8relatives/2rawpredicates/currentcaptain1/names-item bound.Surname/bodyEnglish/layout/actual/release pending.Full goal active.':
        'VerifiedV8213/currentV8172:7171completed;Gerhard Adernkatz decision/5 native pages/660 branch cases/stored/name planes pass.Asset/actual/registered andHodram28 prose pending.Full goal active.',
    })
    result=derive(str(Path(previous.__file__)),'scripts/checkpoint_Gerhard_v8212.py',changes)
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared reversible six-target checkpoint;allprior values/counters/candidate/fullscope preserved.')
