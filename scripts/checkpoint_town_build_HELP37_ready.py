"""Save current tutorial priority,live registered job and37 ready research reviews without credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v4 import checkpoint
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    prep_path=Path('work/analysis/Town_HELP23_release_20261104/registered_preparation.json');prep=load(prep_path)
    qual_path=Path('work/analysis/Town_HELP23_release_qualification_20261104/qualification.json');qual=load(qual_path)
    live_path=prep_path.parent/'build_live_checkpoint_v1.json';live=load(live_path)
    assert live['process_id']==73672 and live['session_id']==86273 and not live['terminal_or_release_pass']
    assert qual['registry_sha256']==prep['registry_sha256']=='013b1aa0698652ea044c609de66d661f2d3460d1478c6e2a91519bd354b588aa'
    assert len(qual['changed_partial_coverage_rejections'])==4 and qual['unchanged_eight_final_stage_contracts_compared_exactly']
    final_path=Path('translations/help_shipyard37_contextual_final_review_v1.json');final=load(final_path)
    assert len(final['records'])==37 and all(all(r['review'].values()) for r in final['records'])
    assert (final['proposed_revisions'],final['justified_retentions'],final['actual_pages'],final['actual_articles'],final['offline_only_pages'])==(27,10,17,16,21)
    next_path=Path('work/analysis/Shared_HELP_T81_T102_clean_20261104/clean_meanings_andfull_drafts_v1.json');nxt=load(next_path)
    assert len(nxt['records'])==22 and nxt['new_credit']==0
    registered=Path('work/analysis/Early_HELP23_release_verified_20261104/registered_release_verification.json');verified=load(registered)
    current='out/all_routes_combined_early_help23_20261104_candidate.nds'
    current_sha='d61af9136de66e3915d64e4f4e48195d3fc9938b0131509365e3c2c5aad350c9'
    assert verified['candidate_sha256']==current_sha and verified['clean_input_patch_byte_exact']
    summary=('Rafael/tutorial priority:town Help23 isregistered andqualified;build86273/PID73672 isOS-confirmed live,withall eight stages preserved. '
      'Own4001-frame planned-identity capture isterminal;final manifest/patch/registered RAM binding remain. Next37 Help reviews pass all five research gates:27 revisions/10 exact-body retentions,38 fresh native/viewed pages,17 observed/21 offline-only,seven returns. '
      'Corrected the real Y-versus-X Refit instruction using bound native footer/code evidence andfixed a commander-return page split without changing prose. '
      'Next22 sailing/battle meanings/drafts sealed.11336 integrated completions/currentverified d61/main unchanged;no new credit. Full scope/all ROMs preserved;no guide photos.')
    doc=Path('docs/editorial_town_build_shipyard37_ready_20261104.md')
    text=f'''# Rafael and tutorials: town build live, next 37 Help reviews ready

{summary}

The current verified experimental release remains `{current}`, SHA256 `{current_sha}`. Its registered profile is `all-routes-early-help23-20261104`; all671 manifest entries,114 accepted layers,26 checks,eight final stages,own Rafael startup andexact clean-input patch already pass. Keep11336 integrated completions =6582 revisions +4754 retentions. Source/prose/draft counters11339 retain the historical three-record offset. Do not repeat orre-credit these checks.

The new registered profile `all-routes-town-help23-20261104` is additive; registrySHA256 `{prep['registry_sha256']}`. Preparation: `{prep_path}`. Qualification: `{qual_path}`; four partial-coverage rejection cases pass,unchanged prior ten source/gate cases arehash-bound,andall eight stage contracts match. Expected672 manifest entries/114 accepted layers/26 checks/eight stages. Preserve every original final driver andthe ASCII right-bound correction.

Build session86273/PID73672 began at21:42 Indianapolis andwasOS-confirmed live in `{live_path}`. It runs `scripts/build_integrated_release_with_Fernan_field.py --profile all-routes-town-help23-20261104 --out out/all_routes_combined_town_help23_20261104_candidate.nds --work work/t23`. Quiet reconstruction isnormal. Resume this handle/check the process;do not restart a live orsuccessful producer. Planned targetSHA256 `{prep['target_ROM_sha256']}` isresearch identity,notyet a verified registered result.

Town23 research stays19 revisions/4 justified body retentions,28 native/viewed pages,15 observed pages/10 articles and13 offline-only pages/articles. Its verified parent isd61. The immutable manuscript/plan are`translations/help_town23_contextual_final_review_v2.json` and`work/analysis/Shared_HELP_T21_T43_formatting_20261104/production_plan_v2.json`. All5 continuation cases/six returns already pass;do not rerun unchanged native/visual/gameplay proofs. Current source-owned Inn B/Square Trends bindings remain scoped,not fresh town-command activation.

Own planned-identity4001-frame Rafael capture completed in`work/analysis/Town_HELP23_identity_coldboot_20261104`;session33074 terminal0. Final registered equality/captain0/route0/payload/name/RGB binding ispending. Prepared verifiers compile butwereNOT executed: `scripts/verify_town_HELP23_registered_release.py` and`scripts/verify_registered_town_HELP23_startup.py`. After buildterminal0,run the release verifier with`--candidate out/all_routes_combined_town_help23_20261104_candidate.nds --preparation {prep_path} --out work/analysis/Town_HELP23_release_verified_20261104`. Then bind own startup usingthe established CLI andboth Fernan getters. Produce/reconstruct the clean-input xdelta andcredit23 once onlyafter allrequired checks pass. No main promotion.

Next37 complete source/current comparisons are`work/analysis/Shared_HELP_T44_T80_clean_20261104/whole_article_comparisons_v2.json`. They yield27 revisions/10 word-exact body retentions. Exact source/current offsets,hex,original links,individual findings andretention reasons arein every record. All current labels andthe separate per-type four-room limits arebound in`native_UI_terms_andfour_limits_v1.json`. Body retentions areseparate from scoped title/link formatting. No global207-name review credit isclaimed.

The concrete Refit defect isclosed inresearch: current Help51 saysY beginswork,butthe observed nativefooter isA Edit/X Finish/Y Undo/B Back. `HELP51_native_controls_v1.json` binds the original hashed14300-frame RAM/screenshot,14001 A cycling andcurrent corresponding code/vtable/descriptor windows. The old wholeROM file isnot required andno whole-old-ROM equality ornew physical X-press claim ismade. New Help saysA tocycle andX tofinish. This istext instruction localization,no runtime modification.

Research final: `{final_path}`. Compiler`dk4tool/dialogue/reviewed_help_pages_v5.py`; productionplan`work/analysis/Shared_HELP_T44_T80_formatting_20261104/production_plan_v1.json`. All38 pages havefresh original parser/full-font/instruction/canary checks andallten readable sheets weredirectly viewed. Source66's definition/operating-funds paragraphs prevent a sentence crossing pages;the at least150 phrase andA/X phrases staywhole. No body shortening ormanual ordinary breaks. All other36 article plans areunchanged bythat refinement.

Pinned Help-only217-topic research image andsix rejection proofs:`work/analysis/Shared_HELP_T44_T80_formatting_20261104/preview_qualification_v1/qualification.json`. All unownedtopics—including earlier46 reviews andtheir appendedpages—otherfiles/components andcomplete parent inverse areexact. This stillhas the planned Town216 parent;rebind metadata onlyafter that registered parent isverified.

Ordinary title-menu Help run20348 completed30681 frames,without battery/savestate/RAM fixture. Generic navigation/verifier tools were reused. Proof:`work/analysis/Shared_HELP_T44_T80_formatting_20261104/focused_navigation_checked_v1/ordinary_gameplay_verification.json`. All17 observed pages/16 articles andseven returnpairs pass;allfive actual sheets weredirectly viewed.21 pages/21 articles remainoffline-only,listed explicitly. The corrected A/X text isseen inHelp;this isnot a newphysical Refit execution,story playthrough,town-command visit orhardware test. All37 individual five-gate research reviews pass,withzero integrated credit untilregistered release.

The next22 clean meanings/full drafts81–102 aresealed in`{next_path}` beforefresh current-body extraction. All original link IDs match. Physical sailing/mode buttons83–87,item/crew/ability labels andthe historical PCgame/password reference102 needbinding;current comparison,formatting andintegration remain. Provisional button phrases mustnot ship. Earlier general sailing/COMMON evidence isknown;no blanket never-seen-English claim.

After the live Townbuild isverified,integrate ready37 through the registered cumulative workflow,preserving all eight final stages. Keep doing early/tutorial prose while necessary builds run. All Rafael earlier batches andHodram B211–B230 drafts remainpreserved. Every storyline,shared town/shop exchange,random scene,remaining player prose,speaker/name review andunfinished earlier contextual pass staysin scope. Graphics artwork andlater older-record technical re-audit remainseparate. Preserve allROMs/earlier translations/evidence,no guide-photo collection,no promotion orpruning. Full objective active.
'''
    newkey='shared_HELP_T44_T80_contextual_20261104';nextkey='shared_HELP_T81_T102_contextual_20261104'
    protected={current:current_sha,'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
      'translations/release_stack.json':prep['registry_sha256'],str(final_path):sha(final_path.read_bytes()),str(next_path):sha(next_path.read_bytes())}
    checkpoint(mutation='work/analysis/editorial_checkpoint_town_build_HELP37_ready_20261104',batch_key='shared_HELP_T21_T43_contextual_20261104',
      batch_updates=dict(new_credit=0,registered_profile=prep['profile'],registered_preparation=str(prep_path),registered_preparation_sha256=sha(prep_path.read_bytes()),
       release_qualification=str(qual_path),release_qualification_sha256=sha(qual_path.read_bytes()),registered_build_live=True,registered_build_session=86273,registered_build_PID=73672,
       build_live_observation=str(live_path),build_live_observation_sha256=sha(live_path.read_bytes()),own_planned_identity_capture_terminal=True,final_registered_release_patch_own_startup_andcredit_pending=True),
      summary=summary,document=doc,document_text=text,completed=11336,protected=protected,
      new_entries={newkey:dict(new_credit=0,source_topics=37,source_topic_IDs=list(range(44,81)),source_meanings=37,sealed_source_drafts=37,contextual_comparisons=37,
       proposed_revisions=27,justified_retentions=10,first_four_gates_passed=37,all37_individual_five_gates_pass=True,all_fifth_gates_pending=False,
       manuscript=str(final_path),manuscript_sha256=sha(final_path.read_bytes()),formatting_plan='work/analysis/Shared_HELP_T44_T80_formatting_20261104/production_plan_v1.json',
       fresh_native_pages=38,native_andvisually_approved_pages=38,actual_gameplay_pages=17,actual_gameplay_records=16,offline_only_pages=21,offline_only_articles=21,
       all_ten_native_andfive_actual_sheets_directly_viewed=True,source51_Y_to_X_control_correction=True,source66_paragraph_boundary_refinement=True,
       research_checks_complete=True,registered_parent_still_pending=True,registered_integration_pending=True,full_editorial_scope_preserved=True,guide_photos=False),
       nextkey:dict(new_credit=0,source_topics=22,source_topic_IDs=list(range(81,103)),source_meanings=22,sealed_source_drafts=22,contextual_comparisons=0,
        draft=str(next_path),draft_sha256=sha(next_path.read_bytes()),all_localization_controls_terms_display_andintegration_pending=True,full_editorial_scope_preserved=True)},
      additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,current_batch='shared_HELP_T21_T43_contextual_20261104',next_batch=newkey,
       registered_cumulative_build_live=True,registered_build_session=86273,registered_build_PID=73672,next37_all_five_gates_research_ready=True,
       next_source_drafts=22,next_source_meanings=22,next_help_batch=nextkey,Rafael_early_story_andall_tutorials_first=True,full_editorial_scope_preserved=True,guide_photos=False)},
      coverage_unit_updates={'help-and-other-player-facing-prose':dict(status='in-progress',active_batch=newkey,progress_evidence=str(final_path),progress_evidence_sha256=sha(final_path.read_bytes()))})
    print('Ledger/handoff saved:11336 integrated;Town23 live,37 research-ready,22 clean drafts;no new credit/main change/all scope preserved.')
