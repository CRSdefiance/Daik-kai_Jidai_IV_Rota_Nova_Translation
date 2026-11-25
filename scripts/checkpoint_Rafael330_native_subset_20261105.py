"""Save330 prose decisions,332 reviewed native pages and16 names without premature completion credit."""
import ctypes as ct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint

ROOT=Path('work/analysis/Rafael_B81_B84_formatting_20261105')
FINAL=Path('translations/rafael_B81_B84_contextual_editorial_manuscript_v1.json')
NATIVE=ROOT/'combined_native_v5.json'
NAMES=Path('work/analysis/Rafael_B81_B84_progressive_name_planes_v2_20261105/direct_visual_approval.json')
RETRY=Path('work/analysis/Sea22_Fleet66_malloc_retry_20261105')

if __name__=='__main__':
    doc,native,names=map(load,[FINAL,NATIVE,NAMES])
    assert len(doc['records'])==330 and doc['complete_four_gate_comparisons']==330
    assert len(native['records'])==323 and native['pages']==332 and native['all332_complete_pages_directly_viewed']
    assert (native['fresh_final_layout_records'],native['exact_reused_records'])==(19,304)
    assert names['all16_complete_name_planes_approved'] and not (RETRY/'completion.json').exists()
    kernel=ct.WinDLL('kernel32',use_last_error=True);kernel.OpenProcess.argtypes=[ct.c_ulong,ct.c_int,ct.c_ulong];kernel.OpenProcess.restype=ct.c_void_p
    kernel.GetExitCodeProcess.argtypes=[ct.c_void_p,ct.POINTER(ct.c_ulong)];kernel.GetExitCodeProcess.restype=ct.c_int
    kernel.CloseHandle.argtypes=[ct.c_void_p];kernel.CloseHandle.restype=ct.c_int
    h=kernel.OpenProcess(0x1000,False,113672);assert h
    code=ct.c_ulong();assert kernel.GetExitCodeProcess(h,ct.byref(code));kernel.CloseHandle(h);assert code.value==259
    summary=('Rafael/tutorial priority continues.330 source-complete prose decisions nowpassfour gates(173 revisions/157 retentions). '
        '323 speeches have332 complete native/viewed pages;19 exact layout refinements fixseven page turns and12 phrase wraps,304 unchanged records reuseproofs. '
        'Four full-width Latin artifacts nowrender asnormal ASCII. All16 scoped names/roles haveindividual retention reasons,qualified getters andviewed style11 planes(6 fresh/10 reused). '
        'Two146-character FE tutorial paragraphs remainheld for source-preserving pagination;five typedlabels,stored checks andfocused actual scenes remain. '
        '675 original-source build71768/PID113672 remainsOS-confirmed live;two-layer/composite verifier andown-startup adapter areprepared,the three proof-group preflight passes. '
        'All202 Help research remainscomplete/156 integrationpending.11359 integrated/current9c5/main unchanged;zero newcredit,no guidephotos,full scope preserved.')
    document='''# Rafael330 native dialogue and scoped names — November 5, 2026

Rafael's early story andall tutorials remain first. Preserve the full all-route,earlier-translation,shared town-shop,random-scene,name/glyph/wrap objective,all ROMs,evidence andcredit. No guide photos,promotion,pruning orcommit/push. Reuse [the preceding source/build checkpoint](editorial_Rafael330_build_recovery_20261105.md) andthe completed202-Help research;do not repeat those checks.

`translations/rafael_B81_B84_contextual_editorial_manuscript_v1.json` assembles330 complete-exchange prose decisions(173 revisions/157 retentions),nowallfour prose gates. The B81R106 throw remains deliberately agent/object-implicit as in the Japanese: “Whoa! What a throw!” Neither incompatible old thrower interpretation is asserted. This is a fidelity-preserving wording decision,not visual action evidence;the full B81 action/transition sample remains required. All325 six-byte speech preambles,source/current refs,all physical duplicates andFI/FA/FO/FU counts arebound. Other255 speeches in the580 packet still need drafts/comparisons. No completion credit.

## Native body pages and actual wrap corrections

Root `work/analysis/Rafael_B81_B84_formatting_20261105/`. `native_subset_v2/compiled_native_pages.json` passes323 speeches/332 complete pages/1292 native macro alignments;all30 readable sheets were directly viewed. `native_subset_v2/direct_visual_review_with_findings.json` records20 exact layout findings. Full-width I/F defects inB82R133,B84R60 andB84R93 nowuseordinary ASCII in their complete fresh native planes;controls remain exact.

Final plan `automatic_subset_v5/automatic_plans.json` retains every prose character. `combined_native_v5.json` binds19 refined records/26 pages to `native_delta_v4/compiled_native_pages.json` and304 records/306 pages to their exact base proofs. Allfive delta sheets/27 newlygenerated pages wereviewed. One attempted question-tag refinement produced a sparse You really opening;the final retains its better-balanced earlier two rows witha specific reason. This is not a blanket QA waiver.

Seven page turns nowkeep complete closing sentences or tightly connected imperatives together: B82R18/R140 andB84R140/R458/R466/R527/R535. Four ofthem useformatter-owned completion ofunused native rows at a semantic sentence boundary;there isno blank page. All332 final pages retaincomplete first/internal/final glyph order,independent pixels,all bytesconsumed,bounds/canaries andnative pagination. Twelve other scoped phrase-wrap changes keepnames,phrasalverbs andidioms together. No prose wascut,no font/window widened,andpagecount stays332. Fresh stored dispatch/allocation/branch checks andrepresentative actual transitions stillremain;native checks areoffline,not gameplay.

Two identical146-character FE tutorial paragraphs,B84R470/R539,remain explicitly held in `native_ready_subset_v1/held_FE_risk.json`. Native228px/four-row guarded layout hasno faithful one-panel plan. Do not shrink fonts,widen geometry,drop words orshorten good prose merelytofit. Next qualify consumer/source-preserving pagination,including focused actual transitions. These two records andfive typedcaptions areexcluded fromthe323-body approval,not passed by omission.

## Sixteen scoped speaker names and roles

`translations/rafael_B81_B84_scoped_names_androles_v1.json` records16 individual source/current retentions. The exact source貴婦人 supportsLady;男の子 supportsBoy;Shopkeeper,Patron,Trader,Port Worker andGuildmaster arecontextual roles,not personal namesor inventedkinship. Body Cristina/Genz/Manaus/Ferog consistency repairs remainin330. Keepallapprovednames. No namefieldchanges orglobal207 approval.

`scoped_names_macro_andconsumer_dependency_qualification_v1.json` binds16 actors:seven fresh clean/current intrinsicgetter bindings andnine exact qualified reuses. AllARM9/COMMON/actor arrays andfont inputs matchthepreviouslyqualified current runtime;the existing four default macro cases are reused withoutnew execution. Native nameplates: `work/analysis/Rafael_B81_B84_progressive_name_planes_v2_20261105/native_name_planes.json`,six fresh planes/ten exact string/style/code/font reuses(includinga previouslyrendered Shopkeeper). Both16-name sheets wereviewed;`direct_visual_approval.json` approvescomplete style11 pixels and216px bounds. Originalfailed v1 six partialplanes remainpreserved;they are not a whole-run pass. Actual headers/fullcatalogueUI remainunvisited.

## Registered build and integration

Original-source675 build remainslive: session71768/PID113672,`work/analysis/Sea22_Fleet66_malloc_retry_20261105/`,output `out/all_routes_combined_sea22_fleet66_20261105_malloc_candidate.nds`,work `work/s22f66m`. Do not restartquietjobs orchange live core/registry/drivers. Original core27ce0796,registry82a17be4,114 layers/eightfinalstages/26 checks stayexact. No terminal675 candidate yet.

Prepared `scripts/verify_sea22_fleet66_registered_release_v1.py` checks675 manifests,allpreserved layers/stages,orderedSea22/Fleet66 plans,59 exact sourcearticles,60 native/viewed pages,39 observed pages/38 articles and21 offline-only pages,andclean-input reconstruction. `scripts/verify_registered_sea22_fleet66_startup_v1.py` retainsown4001-frame/captain0/route0/RAM/payload/RGB checks withhonest three-group page provenance. Both entrypoints import/parsecorrectly. `work/analysis/Sea22_Fleet66_composite_verifier_preflight_20261105.json` passesallthree saved proof-group page/dependency/capture/RAM hashes andordered independent plans onthe prepared target;this is not registered-build/patch/startup completion.

Onterminal0 executefinalverifier,ownstartup andbothFernan getters,then credit59 once(44 revisions/15 retentions;66 amendment addsnone). Final expected81511dde target remainsunchanged. Existing4001-frame preparedidentitycapture isterminaland reusableonlyafter exactregistered equality. Corrected31+67 Help research shouldbe one successorwithtwoorderedextensions,avoidingtwo full rebuilds. All202 sourceHelp topicsretaincompletedfive-gate research,156 sourcecreditsawaitintegration. Current integrated11359=6601 revisions+4758 retentions(source/prose11362),Town9c5ca87b andmain3cb827e4 unchanged. Graphics artwork andthe laterolder-record technical re-audit remainseparate. Fullgoalactive.
'''
    proofpaths=[FINAL,NATIVE,NAMES,ROOT/'automatic_subset_v5/automatic_plans.json',ROOT/'native_delta_v4/direct_visual_approval_v5.json',
        Path('translations/rafael_B81_B84_scoped_names_androles_v1.json'),Path('work/analysis/Sea22_Fleet66_composite_verifier_preflight_20261105.json'),
        Path('scripts/verify_sea22_fleet66_registered_release_v1.py'),Path('scripts/verify_registered_sea22_fleet66_startup_v1.py'),Path(__file__)]
    protected={str(p):sha(p.read_bytes()) for p in proofpaths}
    protected.update({'translations/release_stack.json':'82a17be4f7610abef225fa39c2059cd4180511af5683f519aec8171de3df5f4e',
        'dk4tool/rom/nds.py':'27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
        'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        'out/all_routes_combined_town_help23_20261104_candidate.nds':'9c5ca87bce5c4ace721ad4ce33c8409374eb412349acf4098098c927f08e7a9f'})
    live=dict(new_credit=0,build_live=True,registered_build_live=True,registered_cumulative_build_live=True,build_session=71768,build_PID=113672,
        registered_build_session=71768,registered_build_PID=113672,registered_integration_pending=True)
    progress=dict(new_credit=0,source_speeches=580,source_draft_speeches=325,source_draft_choices=5,contextual_comparisons=330,
        four_gate_passes=330,proposed_revisions=173,justified_retentions=157,manuscript=str(FINAL),manuscript_sha256=sha(FINAL.read_bytes()),
        pending_source_action_IDs=['DK4_MES_B81_R0106'],throw_prose_preserves_source_implicit_agent_andobject=True,
        native_body_records=323,native_body_pages=332,viewed_base_sheets=30,viewed_delta_sheets=5,final_layout_refinements=19,
        fixed_page_boundaries=7,phrase_wrap_fixes=12,fullwidth_Latin_letters_corrected_andnative_rendered=4,
        final_body_proof=str(NATIVE),final_body_proof_sha256=sha(NATIVE.read_bytes()),
        held_FE_source_IDs=['DK4_MES_B84_R0470','DK4_MES_B84_R0539'],typed_labels_pending=5,scoped_names_native_andviewed=16,
        actual_headers_stored_branches_andregistered_release_pending=True,all_fifth_gates_pending=True,
        all_registered_integration_pending=True,remaining_packet_speech_drafts=255,new_gameplay_runs=0,guide_photos=False)
    checkpoint(mutation='work/analysis/Editorial_checkpoint_Rafael330_native_subset_20261105',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(**live,current_batch='Rafael_SC0_B81_B100_clean_20261105',new_Rafael_four_gate_passes=330,
            new_Rafael_native_records=323,new_Rafael_native_pages=332,new_Rafael_page_turn_fixes=7,new_Rafael_scoped_names_reviewed=16,
            next_focus='Qualify two FE tutorial pagination cases/five captions;stored/representative scenes. Finish675 verification on terminal0;combine reviewed31+67 Help inone successor.',guide_photos=False),
        additional_updates={'Rafael_SC0_B81_B100_clean_20261105':progress,
            'sea22_fleet66_registered_cumulative_20261105':dict(**live,final_verifier_prepared=True,own_startup_adapter_prepared=True,three_group_composite_provenance_preflight_pass=True)},
        summary=summary,document='docs/editorial_Rafael330_native_subset_20261105.md',document_text=document,completed=11359,protected=protected)
    print('Saved330 prose/323 native bodies/332 viewed pages/16 scoped names andlive675;11359 integrated unchanged,fullgoalactive.')
