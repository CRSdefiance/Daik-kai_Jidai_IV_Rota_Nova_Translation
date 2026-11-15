"""Preserve town Help23 five-gate research andprepared final checks whileprior build remains live."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v4 import checkpoint
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Shared_HELP_T21_T43_formatting_20261104')
FINAL=Path('translations/help_town23_contextual_final_review_v1.json')
PREP=Path('work/analysis/Early_HELP23_release_20261104/registered_preparation.json')
OBS=PREP.with_name('build_process_observation_02.json')
KEY='shared_HELP_T21_T43_contextual_20261104'
FIRST='shared_HELP_T00_T20_contextual_20261104'
DOC=Path('docs/editorial_town_help23_research_ready_20261104.md')
if __name__=='__main__':
    doc,prep,obs=map(load,[FINAL,PREP,OBS]);assert len(doc['records'])==23 and doc['all23_individual_five_gates_pass']
    assert (doc['proposed_revisions'],doc['justified_retentions'],doc['native_andvisually_approved_pages'])==(19,4,28)
    assert (doc['actual_pages'],doc['actual_articles'],doc['offline_only_pages'],doc['offline_only_articles'])==(15,10,13,13)
    assert obs['PID']==102816 and not obs['HasExited']
    summary='Rafael/tutorial priority:next23 town Help articles nowpass all five research gates—19 revisions/4 word-exact body retentions,28 native/viewed pages,15 observed/13 offline-only. Six display refinements removeone needless page;source controls/labels arebound. Earlier Help23 registered build61834/PID102816 remainsOS-confirmed live;final verifier/completion scripts areprepared,not executed.11313 integrated completions/current9ace/main unchanged. Both Help groups remain uncredited pendingregistered integration;full scope/all ROMs preserved;no guide photos.'
    text=f'''# Town Help23 research ready — 2026-11-04

Rafael early story andall tutorial/help work remain first. Full all-story/earlier-translation/shared town-shop/random/name-role/player-prose scope stays active. Preserve all ROMs,translations,retentions,credit,evidence andearlier failed runs. No main promotion,pruning,commit/push orguide photos. Graphics artwork andlater older-record technical re-audit remain separate. Previous goal turn wasprogress (credited Rafael539 andregistered Help23);this turn isprogress (resolved next23 prose bindings,completed native/visual/focused actual checks andprepared final release checks).

## Current registered build andcredits

Continue the samebuild61834/PID102816,not a replacement. OS snapshot `{OBS}` at{obs['observation_UTC']} showsCPU{obs['CPU_seconds']}seconds,HasExited false,start{obs['start_UTC']}. It isreconstructing profile `all-routes-early-help23-20261104` into `out/all_routes_combined_early_help23_20261104_candidate.nds`,using `work/h23`. Registry remains `{prep['registry_sha256']}`. All114 accepted layers,all old profiles andeight final runtime/name/data contracts remain registered,includingASCII right bounds/Fernan F. Do not change registry orfrozen producers whilethis build isrunning. Quiet output isnot failure;poll its same handle/PID andstart time. The canonical log is `work/h23/prior/prior/grouped_fields/next_fields/prior_fields/owned_names/runtime_bounds/canonical_builder.log`.

Current verified cumulative image remains9ace6dcdf45097ad2f779d15597ab06ab85a0e5442486e6ad98c112a422c446e and11313 integrated completions/6566 revisions/4747 retentions. Source/draft historical count11316 retains the3-record offset. Reuse all670-entry/eight-stage/Rafael539 source/native/visual/storage/actual/patch/startup proofs in `work/analysis/Rafael_B61_B80_release_verified_20261104`. Main3cb827e4 remains unchanged. Neither Help group's source credit hasbeen added.

Earlier Help0–20/181/184 has23 five-gate research reviews/25 complete native andactual pages/16 revisions/7 retentions;planned final d61af9136de66e3915d64e4f4e48195d3fc9938b0131509365e3c2c5aad350c9. Reuse its completed checks from `docs/editorial_rafael539_integrated_help23_build_next23_20261104.md`. Its own planned4001-frame startup matches10 reviewed Rafael frames. A source-only spot check of9 confirms 提督 and予算に乏しい support the retained admiral/underfunded wording;no new revision orcredit.

After build terminal0,execute the nowprepared dedicated verifier (imports pass;actual run remains untested):

`python scripts/verify_early_HELP23_registered_release.py --candidate out/all_routes_combined_early_help23_20261104_candidate.nds --preparation work/analysis/Early_HELP23_release_20261104/registered_preparation.json --out work/analysis/Early_HELP23_release_verified_20261104`

It mustprove671 entries/114 accepted layers/26 checks/eight final stages,23 exact source/current/final article references,onlyHELP different from9ace,complete inverse,andbyte-exact clean-input xdelta. Then run `scripts/verify_registered_early_HELP23_startup.py` withthe new release proof,`work/analysis/Early_HELP23_identity_coldboot_20261104/capture_report.json`,parent `work/analysis/Rafael_B61_B80_release_verified_20261104/own_registered_startup_verification.json`,andnew own startup output underEarly_HELP23_release_verified. This adapter explicitly binds changed HELP toits separate25-page actual proof;do not use an unchanged-HELP claim. Reuse `scripts/verify_rafael_B51_B60_own_Fernan_getters.py` onthe newrelease/startup toproduce its own `own_Fernan_name_getter_verification.json`. Only afterthose pass,execute the prepared `scripts/complete_early_HELP23_review.py`. It mustcredit23 once,raising totals to11336/6582/4754 andsource/draft11339. Those arefuture totals,not current counts. All newverification/completion scripts import successfully butareNOT executed yet. Do not pre-credit.

## Next23 complete town-help reviews

Authoritative final manuscript `{FINAL}` covers21–43,23 articles/19 proposed revisions/four justified complete-body retentions23/37/40/43. Source21's good prose iskept,butthe native command-label binding changes its24 link fromMarket Prices toMarket Info;therefore its disposition changes fromretention torevision. Prior18/5 andintermediate19/4 drafts remain historical. Current comparison `work/analysis/Shared_HELP_T21_T43_clean_20261104/whole_article_comparisons_v5.json` preserves exact clean/current references andindividual findings. Earlier English exposure for21/23 isdisclosed;no unconsulted-English claim forthose. Source comesfromclean Japanese,not the planned parent.

Inn34:the original hashed V804 RAM/capture proves B interrupts a30-night stay aftertwo nights,withA confirming departure. Exact source-owned Inn flow/dialogue-parent/input/voice code spans match the current ARM9. The historical V803 ROM file ismissing,butthe original hashed captured RAM exists andsupplies the matched code;no whole-old-ROM ornew current-town-playthrough claim. Localize the source cross/cancel intent aspress B;physicalX wasnot tested andisnot claimed broken. Square42:clean流行情報/currentTrends occupyARM9 field143E98 withsame pointer143F78;the historical Square sign UI wasdirectly viewed. Market Info isbound tothree exact current native labels. These areword/control bindings,not new current-command glyph executions. Receipts `Inn34_Square42_control_bindings_v1.json` and`Market24_label_binding_v1.json` areinthe clean next23 folder.

Other findings restore guild selling,profit margin,red purchase prices,Friendship versusrelation state,First Mate,atleast200 Persuasion andthree actual contracts. Retained source37 alreadyincluded allbenefits across37/204/205;do not report omitted text orcount continuations asnew source reviews. Full costs,conditions,letters,home-base restrictions andoriginal binary links arepreserved. Four body retentions areword-exact afterremoving old wrapping/restoring links;heading capitalization/context remains separately reviewed.

## Formatting,coverage andreuse

`work/analysis/Shared_HELP_T21_T43_formatting_20261104/production_plan_v1.json` compiles28 final pages onthe exact planned212-topic d61 parent into216 topics. It preserves firstHelp23/all unowned data/sentinel203. Continuations:22↔212,25↔213,37↔204,38↔214,39↔215. Old205 isretained byte-exact asunreferenced historical data afterthe investment article nowfits two pages;no foreign incoming205 links areallowed. Wholeparent inverse passes. Pending parent bytes areexact toselected9ace comparison records;source/current archive offsets areexplicitly rebound in `refined_v2/formatting_input_v1.json`. Final registered d61 identity stillneeds verification beforethis group canbe registered.

Original29 pages allpassed native checks andall eight sheets wereviewed;visual findings required six article-specific refinements plusA Purser grammar repair. Source tips remain withtheir markers;letter-use instructions and100-percent exceptions stay whole atpage boundaries;press B remains together;continuation headings repeat the command without redundant caller context. Allbody prose remains complete. Final28 pages pass10 fresh native calls/18 exact encoded-byte andruntime/font proof reuses;all seven refined sheets were directly viewed. One unnecessary third investment page isremoved. Four new ownership/paragraph rejection cases pass. Frozen first-help compiler/producers areunchanged;new successors are `reviewed_help_pages_v2.py` and`reviewed_help_pages_v3.py`.

Focused ordinary coldboot `focused_navigation_v1` isterminal0/31641frames. Generic verifier proves15 complete actual pages/10 articles,all five two-page continuation/return cases,two-row initial heading andL/R history. All four actual sheets were directly viewed. Thirteen pages/thirteen articles remain offline-only,explicit perrecord. No story playthrough,hardware ornew physical Inn/Square command activation isclaimed. Proofs: `refined_native_v2/native_help_pages.json`, `preview_qualification_v2/direct_visual_approval.json`, `focused_navigation_checked_v1/ordinary_gameplay_verification.json` and`direct_actual_visual_approval.json`. The Help-only research ROM isqualified andpinned in `preview_qualification_v2`;never hand itoff asregistered. All23 fifth gates nowpass withrepresentative actual scope;registered parent/integration/patch/credit remain pending.

Reusable parameterized `scripts/plan_reviewed_help_navigation_v1.py` and`verify_reviewed_help_navigation_v1.py` nowreplace per-batch navigation/verifier copies. Reuse them andthe compatible Help consumer proofs forlater work;changed text stillneeds fresh formatting andevery newpage directview. Once earlier Help23 isverified/credited,register this complete town group through the same cumulative/eight-stage workflow,rebinding onlymetadata ifd61 bytes match. Do not repeat completed native/visual/actual tests without changed dependencies orconcrete failures. Continue remaining tutorial/help/Rafael source work whilethe long canonical build runs. Full editorial objective remains active.
'''
    protected={str(p):sha(p.read_bytes()) for p in [Path('translations/release_stack.json'),Path('translations/rom_retention_pins.json'),
        Path('out/all_routes_combined_rafael_b61_b80_20261104_candidate.nds'),Path(prep['final_ROM']),Path('out/raphael_natural_v2_accepted_base.nds')]}
    checkpoint(mutation='work/analysis/Editorial_town_HELP23_research_ready_checkpoint_20261104',batch_key=KEY,
        batch_updates=dict(new_credit=0,proposed_revisions=19,justified_retentions=4,first_four_gates_passed=23,localization_binding_pending_topic_IDs=[],
            comparison='work/analysis/Shared_HELP_T21_T43_clean_20261104/whole_article_comparisons_v5.json',
            all_fifth_gates_pending=False,all23_individual_five_gates_pass=True,manuscript=str(FINAL),manuscript_sha256=sha(FINAL.read_bytes()),
            formatting_plan=str(ROOT/'production_plan_v1.json'),native_pages=28,fresh_native_pages=10,exact_reused_native_pages=18,
            actual_gameplay_records=10,actual_gameplay_pages=15,offline_only_articles=13,offline_only_pages=13,
            all28_pages_andfour_actual_sheets_directly_viewed=True,six_display_refinements_one_grammar_fix_one_page_removed=True,
            no_new_ROM_bytes_orcredit=False,only_Help_research_ROM_changed=True,registered_parent_andintegration_pending=True,
            research_checks_complete=True,main_unchanged=True,full_editorial_scope_preserved=True),
        summary=summary,document=DOC,document_text=text,completed=11313,protected=protected,
        additional_updates={FIRST:dict(new_credit=0,registered_build=dict(session=61834,PID=102816,terminal=False,OS_observation=str(OBS)),
                final_verifier='scripts/verify_early_HELP23_registered_release.py',completion_script='scripts/complete_early_HELP23_review.py',
                final_verifier_andcompletion_imports_pass_butnot_executed=True),
            'editorial_execution_priority_20261104':dict(new_credit=0,current_batch=FIRST,next_batch=KEY,next_help_batch=KEY,
                registered_cumulative_build_live=True,next23_all_five_gates_research_ready=True,next_source_meanings=23,next_source_drafts=23,
                next_contextual_comparisons=23,next_body_pages=28,next_actual_pages=15,next_offline_only_pages=13,
                Rafael_early_story_andall_tutorials_first=True,full_editorial_scope_preserved=True)},
        coverage_unit_updates={'help-and-other-player-facing-prose':dict(status='in-progress',active_batch=KEY,
            progress_evidence=str(FINAL),progress_evidence_sha256=sha(FINAL.read_bytes()))})
    print('Checkpoint saved:23 town Help reviews research-ready/zero credit;earlier Help build61834 live;11313 integrated/full scope/main preserved.')
