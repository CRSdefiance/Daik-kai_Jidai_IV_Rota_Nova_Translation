"""Prepare a reversible new-family completion checkpoint from the proven workflow."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
INTRO="""Rafael's twelve-speech SC0 B45 trade tutorial is integrated in registered experimental cumulative V7911. Seven wording revisions and five individually justified retentions follow a fresh clean-Japanese whole-exchange review before current English. Exact source, effective current, compiled, stored, actual and integrated references are in translations/rafael_B45_contextual_final_review_v1.json. Conditional Lisbon cargo, local trading rights and ruler's fee at the Palace or Governor's Office, minimum-fee advice, Julio's Ceuta contract, Rafael's future responsibility and optional sale remain. Clean Help150 supports describing market share as the portion of local stock available to buy; it does not impose a proportional sales cap.

The ledger now has 6950 completed records, 6953 source/prose records and drafts, 4354 integrated wording revisions and 2596 retentions. Completed counts: SC0 147, SC1 91, SC2 4915, SC3 197, COMMON1600; COMMON has three source/prose drafts. Route5350/5350 is only a subset. V7911 contains all633 batches/114 accepted layers, passes18 release checks/110 regressions, equals the approved research reference ROM and reconstructs exactly from its clean-input xdelta patch. MainV4701 and every prior ROM/translation remain unchanged."""
DETAILS="""All twelve complete native single pages, first/internal/final characters, canaries, bounds, consumption and pagination pass. Original actor00 is kept in the six-byte preamble, separate from the unchanged body-NUL guard. The FE panel has its original228px bitmap and measured216px usable text, original null-actor path and20-percent/FO wording. All48 compiled alignments and28 fresh stored alignments plus20 exact reused alignments pass. Seven compiler parity spaces add zero ink; six row-count infos have individual reasons, with no warnings or waivers. No manual breaks or wider geometry.

All24 commands, twelve original six-byte preambles, source selectors00/06/FE, FO order andfive relative sites remain. Twenty-five relocated native cases,343 native load/cache paths and686 parent modes pass. Both full clean/predecessor blocks and the entire predecessor archive invert exactly. OnlyB45 changes, from764stored/762logical/tail2 to864stored/864logical/tail0;342 otherSC0 blocks andallotherfiles/components remain exact. Frozen policy passes12 positives/159 actual-changing rejections. Atomic production passes a whole-ROM positive and131 actual-changing rejections with dependency checks bypassed, each before any final commit. The preserved first production challenge has14 real gaps; the source-locked successor closes all14 without deleting or counting the failures as passes.

Paired source/English16001-frame headless emulator entry fixtures play all12 original speeches each:24 pages/90 complete holds, zero eligible partials, unidentified or unfinished calls. All seven actual/comparison sheets were viewed. Original unforced result1 selectsFE;0400 andouter0100 have native coverage only. Both normal ends are[0,1] at6653. All12 paired upper scenes, portraits and headers,32 command results/UI words, five final components, whole actors and157 sampled later RGB pairs agree. Preserve21 comparison rows andseven duration differences. Final seeds2420418440/1937175841 place English one original LCG step ahead, consistent with discarded cooperative-wait timing; no fresh every-call causal trace orfuture random-outcome equivalence is claimed. These are disclosed Lisbon entry fixtures, not natural B45/Ceuta activation, original location, full mechanics, full route orhardware coverage.

Fresh own-V7911 ordinary Rafael NewGame runs4001 frames andmatches six prior whole-RGB pairs, captain0 andwhole-actor controls. The strict current context is work/analysis/current_V7911_Rafael_native_v7914/current_native_input.json. The unchanged source/target scene proofs are reused byexact whole-reference/fixture hashes without replay. Rafael Castor andJulio Erneco remain supported byclean fields/original getters andobserved nameplates; エルネコ doesnot justify Ernesto. Full catalogue UI andthe complete207-name/role/alias review remain open.

All earlier translations, drafts, executed/failing producers, ROMs andproofs remain. Graphics/all18 plaques andthe later older-record technical re-audit remain separate, including normal-end value carry andB35 R65's source-only nineteenth cell. No canceled separate unified package, promotion, pruning, commit orpush."""
NEXT="""Continue the full editorial objective from verifiedV7917/current registeredV7911. RafaelB45 is complete; reuse its source/context/names/native/stored/actual/policy/atomic/registered-release/patch/startup checks unless a new change orconcrete unresolved risk warrants more testing. Use own-V7911 Rafael context forfuture route0 native work. Lil's ownV7857 andMaria's ownV7821 contexts remain historical; obtain each route's owncurrent context when needed.

Continue fresh complete-exchange review through every storyline andearlier translation, broad practical shared shop/town/random captures, Help/remaining prose andall207 names/roles/aliases. Next select an untouched clean Rafael source exchange with its exact EV/caller context; numeric block order doesnot establish chronology oractivation. Retain all earlier unfinished inventories, twelve remaining retrospective contraction/question-tag wrap leads andthe unscanned records beyond558 recorded plans. Sailor151-159 progressive labels remain separate fromRetainer full-name/indirect/typed/COMMON/UI consumers. Preserve every older item, counterpart anddisplay lead, including750-752,preLF6435,JanusPasha counterparts,Trader/PortWorker/Guildmaster,AlShin/AlFeridShin,ArmadilloHide,HerophilusMedicine,イギリス andAksumGoldSeal.

The full goal remains active. Preserve every generated ROM andearlier translation. Keep graphics/all18 plaques andthe later older-record technical re-audit separate. MainV4701 remains unchanged; no separate unified package, promotion, pruning, commit orpush."""
GATES="""def gates():
    release,start,view,atomic,doc,seal=map(read,[RELEASE,START,START_VIEW,ATOMIC,SEALED,SEAL])
    rom=Path(release['candidate']);manifest=read(release['manifest']);registry=read('translations/release_stack.json')
    assert sha(rom.read_bytes())==release['candidate_sha256']==manifest['candidate_sha256']==start['candidate_sha256']==view['candidate_sha256']
    assert manifest['profile']=='all-routes-unified-v7911' and len(manifest['batches'])==633 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert release['all110_release_dialogue_regressions_pass'] and release['whole_clean_input_ROM_reconstruction_byte_exact']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256'] and Path(release['exact_patch_reconstruction']).read_bytes()==rom.read_bytes()
    assert start['all_whole_RGB_actor_andcaptain_controls_equal'] and start['actual_original_captain_ID']==0 and start['whole_RGB_pair_count']==6
    assert start['all_strict2b6_COMMON_directory_and123264_payload_guards_pass']
    assert view['viewed'] and view['startup_proof_sha256']==sha(START.read_bytes())
    assert atomic['positive_records']==12 and atomic['negative_count']==131 and atomic['all_negatives_reject_before_any_files_list_commit'] and atomic['config_dependency_digests_deliberately_bypassed']
    assert seal['manuscript_sha256']==sha(SEALED.read_bytes()) and seal['all12_five_gates_andexact_references_approved']
    assert len(doc['records'])==12 and all(all(r['review'].values()) for r in doc['records'])
    return release

"""
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B45_completion_tools_v7916');assert not root.exists()
    src=Path('scripts/complete_Maria_B36_v7826b.py').read_text('utf8')
    assignments=src[src.index('INTRO='):src.index('\ndef digest')]
    gates=src[src.index('def gates():'):src.index('def stage():')]
    first=src.index('            verified=deepcopy(read(PRIOR))')
    last=src.index("            save(VERIFY/'verified_handoff.json',verified)",first)
    verify="""            verified=dict(candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],
                patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
                ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                records_editorially_completed=6950,records_with_source_and_prose_pass=6953,records_with_source_prose_drafts=6953,
                records_revised_and_integrated=4354,retained_wordings_editorially_completed=2596,
                completed=6950,source_prose=6953,revised=4354,retained=2596,SC0=147,SC1=91,SC2=4915,SC3=197,
                reviewed_routes=5350,completed_routes=5350,manifest_batches=633,accepted_layers=114,release_checks=18,regressions=110,
                Rafael_B45_completed_once=True,Rafael_B45_policy_atomic_registered_integration_pending=False,
                final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),actual_final_pages=24,actual_complete_body_andheader_holds=90,
                strict_own_Rafael_current_input=read(START)['current_native_input'],next_required=NEXT,unfinished_scope=SCOPE,latest_completion=KEY,
                all_prior_roots_families_records_andcounts_recover_exactly=True,full_goal_active=True,full_goal_complete=False,
                new_credit=12,new_emulator_runs=1,new_actual_frames=4001,main_V4701_preserved=True,all_sessions_terminal_andreaped=True,
                RNG_one_step_difference_andall_actual_scope_limits_retained=True,producer_sha256=sha(Path(__file__).read_bytes()))
"""
    changes={
        src.splitlines()[0]:'"""Credit twelve disjoint integrated Rafael decisions once; preserve every prior ledger value reversibly."""',
        'from scripts.Maria_B36_final_paths_v7816b import *':"from scripts.Rafael_B45_release_paths_v7903 import *\nSEALED=APPROVED\nACTUAL=Path(proofs()['actual_proof'])\nAPPROVAL=Path(proofs()['actual_approval'])",
        'maria_B36_completion_v7826':'Rafael_B45_completion_v7916',
        'editorial_handoff_verification_v7827':'editorial_handoff_verification_v7917',
        'editorial_handoff_verification_v7817d':'editorial_handoff_verification_v7900',
        'maria_B36_release_v7822':'Rafael_B45_release_v7912',
        'work/analysis/maria_B36_startup_verification_v7824/own_Maria_startup_exact_V7779_andstrict_current_input.json':'work/analysis/Rafael_B45_context_binding_v7914/own_Rafael_startup_andstrict_captain0_context.json',
        'work/analysis/maria_B36_startup_view_v7825/own_Maria_startup_sheet_viewed.json':'work/analysis/Rafael_B45_startup_view_v7915/own_Rafael_startup_sheet_viewed.json',
        'maria_B36_atomic_challenges_v7819':'Rafael_B45_atomic_challenges_v7909',
        'maria_B36_contextual_final_review_v1':'rafael_B45_contextual_final_review_v1',
        'Maria_SC3B36_completion_v7826':'Rafael_SC0B45_completion_v7916',
        'Maria_SC3B36_contextual_confrontation_v7826':'Rafael_SC0B45_contextual_trade_tutorial_v7916',
        'unfinished_editorial_scope_v7826':'unfinished_editorial_scope_v7916',
        'BEFORE=(6922,6925,6925,4338,2584)':'BEFORE=(6938,6941,6941,4347,2591)',
        'AFTER=(6938,6941,6941,4347,2591)':'AFTER=(6950,6953,6953,4354,2596)',
        assignments:'INTRO='+repr(INTRO)+'\nDETAILS='+repr(DETAILS)+'\nNEXT='+repr(NEXT)+'\n',
        gates:GATES,
        '/data/SC3.DK4':'/data/SC0.DK4',
        'len(oldkeys)==6922 and len(keys)==16':'len(oldkeys)==6938 and len(keys)==12',
        "dict(block=g['block'],version=g['version'],speech=s)":"dict(block=45,version=g['version'],speech=s)",
        "Counter(r['editorial_decision'] for r in rows)=={'revise':9,'retain-wording':7}":"Counter(r['decision'] for r in rows)=={'revision':7,'retention':5}",
        'maria_B36_atomic_v7818b':'Rafael_B45_atomic_positive_v7908',
        'maria_B36_registration_v7820':'Rafael_B45_registration_v7910',
        'maria_B36_production_tools_v7818b':'Rafael_B45_production_guard_tools_v7907',
        'revised=9,retained=7':'revised=7,retained=5',
        'source_prose_and_completion_credit_added_once=16':'source_prose_and_completion_credit_added_once=12',
        'actual_speeches_each_language=16,actual_total_complete_pages=32,complete_body_andheader_holds=132':'actual_speeches_each_language=12,actual_total_complete_pages=24,complete_body_andheader_holds=90',
        'all16_complete_native_single_pages':'all12_complete_native_single_pages',
        'all22_commands_no_relative_sites16_preambles3_substitutions_andcomplete_ends_preserved':'all24_commands_five_relative_sites12_preambles_FO_andcomplete_ends_preserved',
        'names_shared155_semantics_andfull207_broader_consumers_open':'names_Rafael_Julio_FE_andfull207_broader_consumers_open',
        'policy_positive16_negative81_andatomic_positive16_negative120':'policy_positive12_negative159_andatomic_positive12_negative131',
        "new[key][file]==181;put([key,file],197)":"new[key][file]==135;put([key,file],147)",
        'blocks=[36]':'blocks=[45]',
        'revised_count=9,retained_count=7,fresh_revisions=9,fresh_retentions=7':'revised_count=7,retained_count=5,fresh_revisions=7,fresh_retentions=5',
        'fresh_pass_records_explicitly_reread=6938,fresh_pass_records_integrated=6938':'fresh_pass_records_explicitly_reread=6950,fresh_pass_records_integrated=6950',
        'records=16,final_review=str(FINAL),new_revisions=9,justified_retentions=7,new_completed_records=16':'records=12,final_review=str(FINAL),new_revisions=7,justified_retentions=5,new_completed_records=12',
        'actual_initialized_fixture_speeches=16,actual_pages=16':'actual_initialized_fixture_speeches=12,actual_pages=12',
        '==5322':'==5338',
        'reviewed_route_records=5338,completed_route_records=5338':'reviewed_route_records=5350,completed_route_records=5350',
        'completion_credit_added=16':'completion_credit_added=12',
        'actual_objects=16,actual_pages=16':'actual_objects=12,actual_pages=12',
        "'Maria_SC3B36_v7826'":"'Rafael_SC0B45_v7916'",
        '16-source-prose-native-stored-reference-representative-actual-registered-release-pass':'12-source-prose-native-stored-reference-representative-actual-registered-release-pass',
        'final16_single_pages=True,row_infos9_no_waivers=True':'final12_single_pages=True,row_infos6_no_waivers=True',
        'shared155_names_andfull_editorial_objective_open':'full207_names_andfull_editorial_objective_open',
        'Maria_SC3B36_sealed_pending_v7817c':'Rafael_SC0B45_actual_native_approved_pending_production_v7899',
        'unfinished_editorial_scope_v7817c':'unfinished_editorial_scope_v7899',
        'completed_objects=16,revisions=9,retentions=7':'completed_objects=12,revisions=7,retentions=5',
        'shared155_names_full_goal_andall_late_limits_preserved':'full207_names_full_goal_andall_late_limits_preserved',
        'new_source_prose_reviews=16,new_completed_records=16':'new_source_prose_reviews=12,new_completed_records=12',
        '## V7826: Maria confrontation integrated in cumulative V7821; full editorial review continues':'## V7916: Rafael trade tutorial integrated in cumulative V7911; full editorial review continues',
        '# Current editorial handoff - V7826; V7821 current':'# Current editorial handoff - V7916; V7911 current',
        'all16_records_integrated_once':'all12_records_integrated_once',
        'Six completion targets staged:16disjoint Maria decisions/9revisions/7retentions.Deep inverse audit next.':'Six completion targets staged:12 disjoint Rafael decisions/7 revisions/5 retentions. Deep inverse audit next.',
        'exactly16_disjoint_new_records':'exactly12_disjoint_new_records',
        'exactly16_decisions_credited_once':'exactly12_decisions_credited_once',
        'Six audited completion targets applied;6938completed/4347revisions/2591retentions,currentV7821.Fullgoal active.':'Six audited completion targets applied;6950 completed/4354 revisions/2596 retentions,currentV7911. Full goal active.',
        'len(completed)==6938':'len(completed)==6950',
        src[first:last]:verify,
        'VerifiedV7826/V7821:6938completed/6941source-prose/4347revisions/2591retentions;16creditedonce.Fullgoal/names/graphicsseparation/lateraudit preserved.':'Verified V7917/current V7911:6950 completed/6953 source-prose/4354 revisions/2596 retentions;12 credited once. Full objective active.',
    }
    row=derive('scripts/complete_Maria_B36_v7826b.py','scripts/complete_Rafael_B45_v7916.py',changes)
    root.mkdir(parents=True);save(root/'source_locked_derivation.json',row)
    print('Prepared reversible twelve-record completion; no ledger or docs mutation.')
