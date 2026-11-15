"""Preserve credited Rafael539,live registered Help23 build andthe next23 contextual comparisons."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v4 import checkpoint
from dk4tool.patch.grand_race_menu_release import sha

HELP=Path('work/analysis/Shared_HELP_early23_formatting_20261104')
PREP=Path('work/analysis/Early_HELP23_release_20261104/registered_preparation.json')
QUAL=Path('work/analysis/Early_HELP23_release_qualification_20261104/qualification.json')
OBS=PREP.with_name('build_process_observation_01.json')
FINAL=Path('translations/help_early23_contextual_final_review_v1.json')
NEXT=Path('work/analysis/Shared_HELP_T21_T43_clean_20261104/whole_article_comparisons_v2.json')
KEY='shared_HELP_T00_T20_contextual_20261104'
NEXT_KEY='shared_HELP_T21_T43_contextual_20261104'
RELEASE=Path('work/analysis/Rafael_B61_B80_release_verified_20261104/registered_release_verification.json')
DOC=Path('docs/editorial_rafael539_integrated_help23_build_next23_20261104.md')

if __name__=='__main__':
    prep,qual,obs,doc,next_doc,release=map(load,[PREP,QUAL,OBS,FINAL,NEXT,RELEASE])
    completion=load(RELEASE.with_name('completion_checkpoint.json'))
    assert completion['new_credit']==539 and completion['counts']==dict(completed=11313,revised=6566,retained=4747)
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact']
    assert len(doc['records'])==23 and doc['all23_individual_five_gates_pass']
    assert len(qual['semantic_rejections'])==10 and qual['direct_andshared_Help_targets_equal']
    assert obs['session']==61834 and obs['PID']==102816 and not obs['HasExited']
    assert next_doc['records_count']==23 and next_doc['first_four_gates_passed']==21
    startup=Path('work/analysis/Early_HELP23_identity_coldboot_20261104/identity_RGB_qualification.json')
    assert len(load(startup)['exact_RGB_pairs'])==10
    summary='Rafael539 isregistered,verified andcredited once:11313 completions/6566 revisions/4747 retentions;experimental9ace6dcd passes670 entries,all eight stages,exact clean patch andown startup. Early Help23 has16 revisions/7 retentions,25 fully checked native andordinary UI pages,all five gates;registered cumulative build61834/PID102816 isOS-confirmed live. Final Help manifest/patch/own RAM binding remain;zero new Help credit. Next23 town-help comparisons yield18 proposed revisions/5 word-exact retentions;21 four-gate passes,two control/label bindings andall display gates pending. Full scope/all ROMs/main preserved;no guide photos.'
    text=f'''# Rafael539 integrated; Help23 building; next23 tutorials compared — 2026-11-04

Rafael early story andall tutorial/help work remain first. Preserve the full all-story/earlier-translation/shared town-shop/random/name-role/player-prose objective andall translations,retentions,coverage,ROMs andevidence. No main promotion,pruning,commit/push orguide photos. QA captures remain evidence. Graphics artwork andlater older-record technical re-audit stay separate.

## Verified andcredited Rafael539

`out/all_routes_combined_rafael_b61_b80_20261104_candidate.nds`, SHA256 `{release['candidate_sha256']}`, isregistered andverified;build96622/PID6100 wasobserved terminal0. Reuse all539 editorial/native/storage/gameplay proofs;do not repeat them. Its670 manifest entries/114 accepted layers/eight final stages/26 checks,all539 final references,complete inverse andexact clean-input xdelta pass. Patch `{release['patch']}`, SHA256 `{release['patch_sha256']}`, reconstructs the image exactly from `work/clean.nds` SHA256f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d. Own4001-frame Rafael captain0/route0 startup andboth original Fernan getters pass. Proofs andonce-only credit arein `work/analysis/Rafael_B61_B80_release_verified_20261104/`.

Totals are11313 integrated completions:6566 revisions/4747 retentions. The historical3-record source/draft offset ispreserved at11316. This includes539 newreviews/210 revisions/329 retentions,14 wrap refinements/16 I fixes/14 ellipsis fixes. Story actual scope remains95 utterances/101 pages ininitialized fixtures;444 utterances offline-only. This isnot a full natural route orhardware playthrough. Main3cb827e4 isunchanged.

## Help23 ready research andregistered build

`translations/help_early23_contextual_final_review_v1.json` has23 individual five-gate reviews:0–20,181,184;16 revisions/seven justified retentions. The complete Power family isconsistent withregional faction Power andCOMMON288. It doesnot rewrite unrelated skill prose saying influenced by. Original Japanese links,logical prose,costs,qualifiers andbiographical facts arepreserved. First21 source meanings/drafts were sealed beforetheir selected current extraction;181/184 bodydrafts likewiseprecede their bodies. Earlier nonselected producer exposure isdisclosed inthe source notes;do not claim allfuture topics wereunseen.

`work/analysis/Shared_HELP_early23_formatting_20261104/production_plan_v1.json` compiles23 articles into25 pages,211→212 topics,using41 planning cells/252px/ten native rows. It retains existing Rafael7↔202 andadds Hodram9↔211. Biography andnumbered-benefit semantic paragraphs justify those page boundaries;no manual ordinary wrapping orprose shortening. All other original/appended topics,203 sentinel and204–210 remain exact.

All25 complete native/parser/font planes andall25 actual UI pages pass;seven offline sheets andseven actual sheets were directly viewed. Whole first/internal/final glyphs,blank gaps,original link children,archive loading andboth continuation returns plusL/R history pass. Actual qualifying ordinary coldboot is32761 frames,not a story playthrough. The independent font oracle wasupdated fromhistorical y+0 toaccepted current y+1;native code/addresses/geometry stayed unchanged. The first34841-frame navigation attempt double-activated selected links;the validated default-first-A/otherwise-select-and-A successor fixes onlythe schedule. Both failed/probe runs andall outputs arepreserved. Authoritative actual proof: `work/analysis/Shared_HELP_early23_formatting_20261104/ordinary_navigation_checked_v2/ordinary_gameplay_verification.json`.

New profile `{prep['profile']}`, registry SHA256 `{prep['registry_sha256']}`. Puremodule `dk4tool.patch.early_help23_release_v1`,config `translations/early_help23_editorial_release_v1.json`;preparation `{PREP}` andqualification `{QUAL}` pass direct/shared equality andten semantic rejection cases. All114 accepted layers,prior profiles andeight final runtime/name/data contracts—includingASCII right bounds andFernan F—arepreserved. Allnine stage/reference ROMs arepinned. New planned final image SHA256 `{prep['target_ROM_sha256']}` isexactly the reviewed Help-only research image.

Build session61834/PID102816 islive,not terminal. OS evidence `{OBS}` observed at{obs['observation_UTC']},CPU{obs['CPU_seconds']} seconds/HasExited false. Poll the same session/PID+start;do not restart because output isquiet. Command: `scripts/build_integrated_release_with_Fernan_field.py --profile all-routes-early-help23-20261104 --out out/all_routes_combined_early_help23_20261104_candidate.nds --work work/h23`. Log: `work/h23/prior/prior/grouped_fields/next_fields/prior_fields/owned_names/runtime_bounds/canonical_builder.log`.

Own4001-frame planned-identity Rafael startup isterminal0 andall10 RGB frames match9ace parent: `{startup}`. Final registered identity/manifest,clean-input patch andown native RAM binding remain. Use `scripts/verify_registered_early_HELP23_startup.py` afterthe final release proof;it preserves the original snapshot/code/name checks while binding changed HELP toits separate all25-page actual proof. It imports successfully buthasNOT yetexecuted onthe final release. Do not use the old unchanged-HELP startup claim. A dedicated Help final-release verifier/completion step muststill beimplemented afterbuild terminal0:expect671 entries,the same114 accepted layers/26 checks/eight stages,onlyHELP different from9ace,andexact23 source/current/target page refs. Follow the existing registered verifier patterns,compile the same production resource,invert itto9ace,reconstruct fromclean withxdelta,andbind the candidate toall25 actual pages/own startup beforeonce-only23 credit. Current Help credit remainszero. Expected future totals11336/6582/4754 areNOT current counts.

## Next23 town-help contextual pass

`work/analysis/Shared_HELP_T21_T43_clean_20261104/clean_meanings_andfull_drafts_v2.json` and`current_full_articles_verified_parent_v1.json` bind23 clean/current complete articles21–43. Prior English exposure for21/23 isdisclosed;no wholly unconsulted claim forthose. V2 source-draft refinements keep the definite specialty increase aftera conditional item request/gift,remove unsupported instead fromthe trend rewards,andclarify ceasefire acceptance versus the discarded-during-battle exception. Draftv1 andall earlier text remain.

`{NEXT}` has23 whole-article comparisons:18 proposed revisions/five justified retentions,21 four-gate passes. Retentions21/23/37/40/43 preserve the entire current word chain while restoring original links/reflowing. Military37 alreadycontains allbenefits across37+204+205;complete refs arein `Military37_complete_current_continuations_v1.json`. Do not report missing bonuses orcount continuations asadditional source reviews. The v2 comparison corrects onlytopic25's original-link count tofour;English/gates unchanged.

Findings include guild selling omitted,absolute profit versus margin,red purchase-price clarity,Friendship numeric metric versusrelationship status,First Mate instead ofadjutant,atleast200 Persuasion ratherthan exact200,three actual contracts versus merely three factions present,andretail-shop sign/trend-information meaning. All fresh display gates andintegration remain. Resolve34 source cross/cancel control and42 exact trend-command label usingexisting compatible UI evidence/focused current checks. Role evidence119 Purser office/121 First Mate office isheaded glossary/source context;do not call those heading reads new runtime execution. Preserve accepted Source Items/Specialties/command terms orbind any change explicitly.

Next formatter mustbe a successor ofthe frozen `reviewed_help_pages_v1.py`,which isnow registered. Do not edit itorits frozen producers. Generalize onlyneeded ownership for37's204/205 continuations andcurrent212-topic parent afterHelp23 isverified. Reuse the completed Help consumer/font/widget proofs afterdependency qualification;changed text stillneeds fresh automatic/native/visual checks. Continue useful complete-article work whilethe long cumulative build runs. Full objective remains active.
'''
    protected={str(p):sha(p.read_bytes()) for p in [Path('translations/release_stack.json'),Path('translations/rom_retention_pins.json'),
        Path(release['candidate']),Path(release['patch']),Path(prep['final_ROM']),Path('out/raphael_natural_v2_accepted_base.nds')]}
    updates=dict(new_credit=0,source_topics=23,source_topic_IDs=list(range(21))+[181,184],contextual_comparisons=23,
        proposed_revisions=16,justified_retentions=7,first_four_gates_passed=23,source_context_naturalness_passed=23,
        metric_label_binding_pending_topic_ids=[],manuscript=str(FINAL),manuscript_sha256=sha(FINAL.read_bytes()),
        all_fifth_gates_pending=False,all_individual_five_gates_passed=True,actual_gameplay_records=23,actual_gameplay_pages=25,
        native_rows_glyphs_links_bounds_pagination_visual_gameplay_andregistered_integration_pending=False,
        no_Help_ROM_bytes_changed=False,only_research_HELP_changed_registered_output_pending=True,
        formatting_plan=str(HELP/'production_plan_v1.json'),native_pages=str(HELP/'native_pages_v2/native_help_pages.json'),
        actual_proof=str(HELP/'ordinary_navigation_checked_v2/ordinary_gameplay_verification.json'),actual_qualifying_coldboot_frames=32761,
        offline_andactual_all25_pages_separately_verified=True,registered_integration_pending=True,registered_preparation=str(PREP),
        registered_qualification=str(QUAL),registered_profile=prep['profile'],registered_registry_sha256=prep['registry_sha256'],
        registered_build=dict(session=61834,PID=102816,terminal=False,OS_observation=str(OBS)),
        planned_identity_startup=str(startup),final_manifest_patch_andown_RAM_binding_pending=True,
        existing_Rafael202_bonus_present_not_an_omission=True,target_topic_count=212,full_editorial_scope_preserved=True)
    next_entry=dict(new_credit=0,source_topics=23,source_topic_IDs=list(range(21,44)),source_meanings=23,sealed_source_drafts=23,
        contextual_comparisons=23,proposed_revisions=18,justified_retentions=5,first_four_gates_passed=21,
        localization_binding_pending_topic_IDs=[34,42],all_fifth_gates_pending=True,comparison=str(NEXT),comparison_sha256=sha(NEXT.read_bytes()),
        current_ROM=next_doc['current_ROM'],current_ROM_sha256=next_doc['current_ROM_sha256'],
        existing37_204_205_complete_article_bound_not_missing_text=True,prior21_23_producer_exposure_disclosed=True,
        actual_gameplay_records=0,no_new_ROM_bytes_orcredit=True,full_editorial_scope_preserved=True)
    checkpoint(mutation='work/analysis/Editorial_Rafael539_Help23_andnext23_checkpoint_20261104',batch_key=KEY,batch_updates=updates,
        summary=summary,document=DOC,document_text=text,completed=11313,protected=protected,new_entries={NEXT_KEY:next_entry},
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,current_batch=KEY,next_batch=NEXT_KEY,next_help_batch=NEXT_KEY,
            previous539_registered_verified_andcredited_once=True,current539_batch_integrated=True,current539_five_gate_research_ready=True,
            registered_cumulative_integration_next=False,registered_cumulative_build_live=True,current_batch_not_yet_integrated=True,
            next_source_meanings=23,next_independent_drafts=21,next_source_drafts=23,next_contextual_comparisons=23,
            current_body_pages_native_andvisually_reviewed=25,Rafael_early_story_andall_tutorials_first=True,full_editorial_scope_preserved=True)},
        coverage_unit_updates={'help-and-other-player-facing-prose':dict(status='in-progress',active_batch=KEY,progress_evidence=str(FINAL),progress_evidence_sha256=sha(FINAL.read_bytes()))})
    print('Checkpoint saved:11313 credited;Help23 registered build61834 live;next23 compared;full scope/main/ROMs preserved.')
