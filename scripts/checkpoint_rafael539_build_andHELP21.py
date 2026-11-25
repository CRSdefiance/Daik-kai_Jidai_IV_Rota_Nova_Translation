"""Preserve the live registered build and21 complete early-Help contextual comparisons."""
from pathlib import Path
from datetime import datetime,timezone
from scripts.audit_story_glyph_consistency import load
from dk4tool.patch.grand_race_menu_release import sha
from scripts.save_editorial_progress_checkpoint_v4 import checkpoint

ROOT=Path('work/analysis/Rafael_B61_B80_release_20261104')
HELP=Path('work/analysis/Shared_HELP_early_topics_clean_20261104')
HELP_KEY='shared_HELP_T00_T20_contextual_20261104'
if __name__=='__main__':
    prep_path=ROOT/'registered_preparation.json';prep=load(prep_path)
    qualified=Path('work/analysis/Rafael_B61_B80_release_qualification_20261104/qualification.json');qualification=load(qualified)
    startup=Path('work/analysis/Rafael_B61_B80_identity_coldboot_20261104/identity_RGB_qualification.json')
    assert len(qualification['semantic_rejections'])==9 and qualification['direct_andshared_scene_targets_equal']
    assert load(startup)['existing_direct_startup_visual_review_reused_by_exact_ten_RGB_pairs']
    observed_path=ROOT/'build_process_observation_01.json';observed=load(observed_path)
    assert observed['PID']==6100 and observed['session_id']==96622 and not observed['HasExited']
    assert (datetime.now(timezone.utc)-datetime.fromisoformat(observed['observed_UTC'].replace('Z','+00:00'))).total_seconds()<600
    manuscript=Path('translations/help_T00_T20_contextual_manuscript_v1.json');help_doc=load(manuscript)
    assert len(help_doc['records'])==21 and (help_doc['proposed_revisions'],help_doc['justified_retentions'])==(13,8)
    assert help_doc['first_four_gates_passed']==18 and all(not r['review']['formatting'] for r in help_doc['records'])
    parent=load('work/analysis/Rafael_B51_B60_release_verified_20261104/registered_release_verification.json')
    summary=('Rafael539 isregistered andqualified:direct/shared plans,nine rejection cases andall eight stage contracts pass. '
        'Build96622/PID6100 wasOS-confirmed live;final manifest/patch/own RAM binding andonce-only credit remain. '
        'Planned9ace6dcd startup matches10 reviewed RGB frames. Early Help nowhas21 contextual comparisons:13 proposed revisions/8 retentions;18 four-gate passes/three metric-label bindings pending. '
        '202 clean/211 current topics andRafael continuation202 arebound;all Help formatting remains pending. '
        '10774 integrated completions/verified eb62870b/main unchanged. Full scope/all ROMs preserved;no guide photos.')
    document=Path('docs/editorial_rafael539_build_andHELP21_20261104.md')
    text=f'''# Rafael539 registered build andearly Help21 — 2026-11-04

Rafael early story andall tutorial/help work remain first. Preserve the full all-story/earlier-translation/shared town-shop/random/name-role/player-prose scope andall translations,retentions,credit,ROMs andevidence. No main promotion,pruning,commit/push orguide photos. Graphics artwork andlater older-record technical re-audit stay separate.

## Registered build in progress

New experimental profile `{prep['profile']}`, registry SHA256 `{prep['registry_sha256']}`. Previous profiles/all114 accepted layers areunchanged. `{prep_path}` and`{qualified}` qualify539 records/all eight final stages,nine semantic rejection cases,direct/shared equality andcomplete source/control/inverse preservation. The lowercase module `dk4tool.patch.rafael_story_b61_b80_release_v1` isregistered. Reuse all completed prose/native/visual/storage/gameplay checks from `docs/editorial_rafael_539_research_ready_20261104.md`;do not repeat them.

Build session96622/PID6100 isnot terminal atthis checkpoint. OS observation `{observed_path}`:UTC `{observed['observed_UTC']}`,CPU `{observed['CPU_seconds']}` seconds,HasExited false. Poll the same session orcheckthat PID/start time;do not restart because output isquiet. Command: `scripts/build_integrated_release_with_Fernan_field.py --profile {prep['profile']} --out out/all_routes_combined_rafael_b61_b80_20261104_candidate.nds --work work/r61`. Its log is `work/r61/prior/prior/grouped_fields/next_fields/prior_fields/owned_names/runtime_bounds/canonical_builder.log`. The canonical builder hasstarted;the final candidate/manifest isnot yet verified. All generated reference ROMs arepinned.

Planned final identity `{prep['target_ROM_sha256']}`. Own4001-frame ordinary Rafael coldboot isterminal0;all10 RGB frames exactlymatch the prior reviewed chain: `{startup}`. This qualifies the planned image only;final registered identity/patch andown snapshot context remain tobind. It doesnot grant release orcompletion credit.

After build terminal0,run `scripts/verify_rafael_B61_B80_registered_release.py --candidate out/all_routes_combined_rafael_b61_b80_20261104_candidate.nds --preparation {prep_path} --out work/analysis/Rafael_B61_B80_release_verified_20261104`. Then use `scripts/verify_registered_rafael_startup_v2.py` withnew release proof,the new identity coldboot `capture_report.json`,parent `work/analysis/Rafael_B51_B60_release_verified_20261104/own_registered_startup_verification.json`,andnew `own_registered_startup_verification.json` output. New ARM9/COMMON/HELP/font areidentical tothe parent;the generic unchanged-runtime Rafael verifier isappropriate. Use the frozen `scripts/verify_rafael_B51_B60_own_Fernan_getters.py` onthe newrelease/startup toproduce new `own_Fernan_name_getter_verification.json`.

Only after those pass,run `scripts/complete_rafael_B61_B80_review.py`;it isprepared butNOT executed. It mustcredit539 once,raising totals to11313 complete/6566 revisions/4747 retentions,withthe historical3-record source/draft offset preserved at11316. Do not use future counts beforeverification. Current totals remain10774/6356/4418 andverified parent eb62870b;main `{parent['canonical_base']}` remainsunchanged. The remaining full objective isnot complete.

## Early Help contextual work

`{manuscript}` holds21 complete source/current article comparisons,13 proposed revisions/eight specifically justified retentions. Source,context andnaturalness passforall21;localization passes18,with7/8/9 waiting forInfluence versusPower metric-label consistency. All formatting/native/visual/gameplay/release gates remain pending;zero new credit. No Help bytes have changed inany ROM.

Source packet `{HELP/'clean_HELP_source_packet_v2.json'}` contains202 original clean topics andexact binary-link/offset refs. The first21 complete meanings/independent drafts were sealed beforetheir current-English extraction in `{HELP/'T00_T20_clean_meanings_andindependent_drafts_v1.json'}`. The earlier source-packet metadata wascorrected:old producer prose fornonselected21,23,103,105,127,134,144 hadbeen visible during compiler reading,so no independent-before-English claim ismade forthose later topics. Selected0–20 have no such exposure. Original drafts andfailed206-topic assumptions arepreserved;the authoritative current HELP actuallyhas211 topics,SHA256 `015ee6aaab9544555a2bcd90f74dbd10450ca20e441954cf5b99f8196e275cc0`.

Current refs `{HELP/'current_T00_T20_verified_parent_v1.json'}` bindverified eb62870b andprove HELP/ARM9/COMMON/font identity inthe planned9ace successor. `{HELP/'native_UI_terms_andRafael_continuation_v1.json'}` binds existing COMMON terminology andcurrent Help headings;it isnot new menu-label renderer execution. It also bindscurrent202,Rafael's continuation:the doubled ruins/item bonus wasalready present there. Review7+202 asone article andpreserve the existing forward202/back7 navigation;do not count202 asa second source review orreport the bonus asmissing. Preserve allnine addedcurrent topics202–210 andall unselected bytes.

Findings:correctRaphael toRafael;restore North Sea bases andJoakim;replace ambiguous poor navy withunderfunded navy andrestore victory/other-faction rewardconditions. Remove unsupported worthy fromthe proof explanation. Restore religious context withthe source many-town qualifier,without adding stereotypes. Replace invented host occupation withthe source knowledgeable women. Preserve costs5–10/1000,5 percent sale benefit,20 percent investment discount,double-gain conditions,three fleet-specific game-over alternatives,forgery exception anddefinite low-ability restrictions. Restore missing original help links. Retain the clear index,introduction,overview,mysterious-token explanation,initial three-captain choice,complete existing Rafael description andfleet-lure instruction. Article11 English words areunchanged;punctuation/spacing inlinks andthe tip marker needformatting repair.

Next resolve the three metric-label bindings,then format/allocate all21 complete articles withthe validated Help consumer,retaining good prose. Native ten-row/41-planning-cell geometry andcurrent continuation allocations areexisting evidence,not a license toshorten. Use automatic continuation pagination where needed;preserve original binary links andaccepted navigation. Review every generated page andrepresentative Help interactions. Reuse relevant consumer proofs only afterexact dependency qualification. Integrate the complete checked Help batch througha successor registered cumulative workflow,while all broader scope continues.
'''
    checkpoint(mutation=ROOT/'build_andHELP21_checkpoint_mutation_v1',batch_key='Rafael_SC0_B61_B80_clean_20261104',
        batch_updates=dict(new_credit=0,registered_profile=prep['profile'],registered_preparation=str(prep_path),registered_preparation_sha256=sha(prep_path.read_bytes()),
            registered_qualification=str(qualified),registered_qualification_sha256=sha(qualified.read_bytes()),
            registered_build=dict(session=96622,PID=6100,live_at_observation=True,observation=str(observed_path),observation_sha256=sha(observed_path.read_bytes())),
            planned_target_sha256=prep['target_ROM_sha256'],planned_identity_startup=str(startup),planned_identity_startup_sha256=sha(startup.read_bytes()),
            no_live_jobs=False,registered_build_andmanifest_patch_own_RAM_binding_andcredit_pending=True,
            next_action='Poll96622/PID6100;verify670-entry eight-stage candidate/exact clean patch;own Rafael RAM andFernan getters;credit539 once.'),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,registered_cumulative_build_live=True,
            current_batch='Rafael_SC0_B61_B80_clean_20261104',registered_cumulative_integration_next=False,
            next_help_batch=HELP_KEY,Rafael_early_story_andall_tutorials_first=True,full_editorial_scope_preserved=True,guide_photos=False)},
        new_entries={HELP_KEY:dict(new_credit=0,source_topics=21,contextual_comparisons=21,proposed_revisions=13,justified_retentions=8,
            first_four_gates_passed=18,source_context_naturalness_passed=21,metric_label_binding_pending_topic_ids=[7,8,9],
            manuscript=str(manuscript),manuscript_sha256=sha(manuscript.read_bytes()),
            source_packet=str(HELP/'clean_HELP_source_packet_v2.json'),source_packet_sha256=sha((HELP/'clean_HELP_source_packet_v2.json').read_bytes()),
            independent_drafts=str(HELP/'T00_T20_clean_meanings_andindependent_drafts_v1.json'),
            current_reference=str(HELP/'current_T00_T20_verified_parent_v1.json'),
            source_topic_count=202,current_topic_count=211,nine_added_current_topics_preserved_required=True,
            existing_Rafael202_bonus_present_not_an_omission=True,all_fifth_gates_pending=True,actual_gameplay_records=0,
            native_rows_glyphs_links_bounds_pagination_visual_gameplay_andregistered_integration_pending=True,
            no_Help_ROM_bytes_changed=True,full_editorial_scope_preserved=True)},
        coverage_unit_updates={'help-and-other-player-facing-prose':dict(status='in-progress',active_batch=HELP_KEY,
            progress_evidence=str(manuscript),progress_evidence_sha256=sha(manuscript.read_bytes()))},
        summary=summary,document=document,document_text=text,completed=10774,
        protected={'translations/release_stack.json':prep['registry_sha256'],parent['candidate']:parent['candidate_sha256'],
            parent['patch']:parent['patch_sha256'],parent['canonical_base']:parent['canonical_sha256']})
    print('Checkpointed live registered build andHelp21 contextual comparisons;10774 completions/main unchanged,full goal active.')
