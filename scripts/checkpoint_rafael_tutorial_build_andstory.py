"""Record registered build progress and next contextual work without completion credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v2 import checkpoint

ROOT=Path('work/analysis/Rafael_early_story_B36_B41_B51_B60_clean_20261104')
RELEASE=Path('work/analysis/Rafael_early_tutorial_B42_B43_release_20261104')
CHECKED=Path('work/analysis/Rafael_early_tutorial_B42_B43_checked_20261104')

if __name__=='__main__':
    prep=load(RELEASE/'registered_preparation.json')
    qualification_path=Path('work/analysis/Rafael_early_tutorial_B42_B43_release_qualification_20261104/qualification.json')
    qualification=load(qualification_path)
    assert len(qualification['semantic_rejections'])==7 and qualification['direct_andshared_scene_targets_equal']
    assert qualification['unchanged_six_final_stage_contracts_compared_exactly']
    source_path=ROOT/'B36_B41_175_complete_clean_meanings_v1.json'
    names_path=ROOT/'B36_B41_source_identity_andFU_checkpoint_v1.json'
    drafts_path=ROOT/'B36_B41_all175_sealed_drafts_v1.json'
    current_path=Path('work/analysis/Rafael_B36_B41_current_20261104/current_effective.json')
    comparison_path=ROOT/'B36_B37_92_whole_exchange_comparison_v1.json'
    source,names,drafts,current,compared=map(load,[source_path,names_path,drafts_path,current_path,comparison_path])
    assert len(source['records'])==len(drafts['records'])==current['records']==175
    assert (compared['compared'],compared['proposed_revisions'],compared['justified_retentions'])==(92,40,52)
    assert all(not r['review']['formatting'] for r in compared['records'])
    assert sum(bool(r.get('wording_retention_with_scoped_glyph_fix')) for r in compared['records'])==1
    assert names['FU_fresh_alignment_cases']==8 and names['default_macro_lengths']['FU']==13
    assert not Path('out/all_routes_combined_rafael_early_tutorial_static_text_20261104_candidate.nds').exists()
    new_key='Rafael_SC0_B36_B41_contextual_20261104'
    pending=dict(file_path='/data/SC0.DK4',blocks=list(range(36,42)),total_editorial_objects=175,
        source_meanings_saved=175,logical_drafts_saved=175,current_records_bound=175,contextual_comparisons_saved=92,
        proposed_prose_revisions=40,justified_wording_retentions=52,remaining_contextual_comparisons=83,
        source=str(source_path),source_sha256=sha(source_path.read_bytes()),drafts=str(drafts_path),drafts_sha256=sha(drafts_path.read_bytes()),
        current=str(current_path),current_sha256=sha(current_path.read_bytes()),individual_source_current_findings=str(comparison_path),
        individual_source_current_findings_sha256=sha(comparison_path.read_bytes()),identity_andmacro_binding=str(names_path),identity_andmacro_binding_sha256=sha(names_path.read_bytes()),
        ordinary_actors=11,name_consumers=22,fresh_clean_getters=14,fresh_current_getters=14,exact_reused_current_getters=8,
        FU_default='Rafael Castor',FU_bytes=13,FU_fresh_alignments=8,
        proposed_display_only_dialogue_fix=dict(id='DK4_MES_B37_R0099',current='Ｉ',proposed='I',wording_retained=True,native_formatting_pending=True),
        additional_pending_full_name_artifacts=names['full_name_only_artifact_findings'],
        current_dialogue_comparison_now_exposed=True,all_fifth_gates_pending=True,
        source_intake_includes_245_additional_B51_B60_speeches_preserved_for_later=True,
        B40_explicitly_later_rematch_not_early_activation=True,
        no_natural_playthrough_ornew_target_gameplay_credit=True,new_credit=0,guide_photos=False,full_goal_complete=False)
    summary=('Rafael B42/B43: 40 five-gate research reviews, 19 revisions/21 retentions, 42 pages/two page fixes; '
        'registered profile and seven rejection checks pass. First build15896 predecessor4941 failed only saving a 270-character staging path; '
        'retry15896 is live on a tested 230-character maximum path; final candidate/manifest/patch/startup remain pending. '
        'Next Rafael B36–B41:175 source-first drafts/current bindings,92 comparisons (40 revisions/52 retentions),83 comparisons pending; '
        'FU full-name13 measured,one dialogue I andtwo catalogue-name artifact fixes proposed. '
        '10306 integrated completions; experimental88e9984f/main unchanged. Full scope/all prior work andROMs retained;no guide photos.')
    # Do not call this checkpoint a release pass: the retry handle was polled live
    # immediately before this producer, and the final candidate is still absent.
    summary=summary.replace('First build15896 predecessor4941','First build4941')
    document=Path('docs/editorial_rafael_tutorial_build_andstory_comparisons_20261104.md')
    text='''# Rafael tutorial integration and next complete exchanges

The previous goal turn made concrete progress: all 40 B42/B43 tutorial research reviews, 42 pages, names, stored scripts and focused gameplay checks were completed. Reuse [that checked batch](editorial_rafael_early_tutorial_checked_20261104.md).

The cumulative successor is now registered as `all-routes-rafael-early-tutorial-static-text-20261104`. Its production adapter passed direct/shared positive plans and seven rejection cases: failed prose/name formatting review, encoded glyph tampering, changed selector00, lost FI, stale parent and missing actual page. All 114 accepted layers, all prior profiles and all six final runtime/name/static stage contracts remain exact. Expected final SHA256 is `c555f555a0e6a15b35e10a27b87ac98ed17601ba814cfeb9ba3d98dcc87344a8`; this is still a research/reference identity, not a verified release candidate.

The first registered build (session4941) completed reconstruction but failed at saveToFile because its absolute canonical-stage path was 270 characters. Parent directories existed; no final candidate was produced. The complete log and failed tree remain. Retry session15896 uses `work/rf_tut_1104_v2/`; a longest-path probe passed at230 characters. The same registered driver and all guards run unchanged. The retry was polled live before this checkpoint. Do not restart it based only on a quiet log or an observation timeout.

Live build log: `work/analysis/Rafael_early_tutorial_B42_B43_release_20261104/registered_build_v2.log`. Original failure: `registered_build.log`; preflight: `short_path_retry_preflight.json`. Preparation: `registered_preparation.json`; seven-case qualification: `work/analysis/Rafael_early_tutorial_B42_B43_release_qualification_20261104/qualification.json`.

When the retry is terminal, verify the complete665-entry manifest, all114 accepted layers/six final stages, exact candidate identity and clean-input patch, then capture and verify its own ordinary startup. Reuse existing unchanged runtime/framebuffer evidence where dependencies match, but obtain the new candidate’s own RAM. Rafael captain0 requires the explicit route-aware runtime; do not accidentally pass a Hodram captain1 snapshot. Credit the40 reviews once only after integration passes. Current completed coverage remains10306 and the current verified experimental candidate remains88e9984f. Main is unchanged and still requires user acceptance for promotion.

## Next source-first Rafael batch

Six complete exchanges in SC0 B36–B41 have175 clean meanings,175 logical English drafts and175 exact current stored/effective bindings. Zero overlap with the10306 explicit completed record keys. The larger420-speech clean intake also preserves B51–B60 (245 speeches); those later source records have no new meaning/draft/comparison credit. Numeric adjacency is not chronology: B40 is explicitly a later Hayreddin rematch lead, while B36–B39 cover pirate/Spanish/Dutch encounters and B41 gives ruins/locals’ trust guidance.

All92 B36/B37 comparisons are saved:40 proposed prose revisions/52 justified word retentions, with exact source/current references and individual findings. Good questions, reactions, warnings, declarations and banter stay. Corrections restore source uncertainty, regional wording and training/trading details; use Salid rather than Salih; remove invented Lord and pirate king titles; avoid implying biological family for Hayreddin’s organization; preserve transit/trading limits and non-guaranteed assistance in his waters. Full conversational context and emotional progression were reviewed. The83 B38–B41 comparisons remain pending. All formatting gates remain false and there is no new completion credit.

B37 R99 contains full-width Ｉ in otherwise English dialogue. Its words are retained as `And I'm Admiral {MACRO:FU}!`; the scoped ASCII-I correction requires fresh native/layout/visual verification. FU is a distinct complete-name macro, not FI: eight fresh native alignment cases expand it to `Rafael Castor`,13 bytes/78px. Preserve source FI/FA/FO/FU independently when planning. The older generic macro lists cover only three names; do not drop FU. Native instructions/scratch rings/ABI/unowned snapshot guards remain exact.

Eleven ordinary identities/22 consumers are bound. Seven additional actors have14 fresh clean and14 fresh current getters plus their voice selections; four existing actors/eight current getters reuse the exact same own Rafael context. The first voice helper correctly rejected its stale captain1 assumption; the successor now requires captain0 without changing native instructions. Two full catalogue-name artifacts are pending: actor31 `Pedro デ Valdes` proposes `Pedro de Valdes`; actor34 `Barbarossa Ｆazul Hayreddin` proposes `Barbarossa Fazul Hayreddin`. Their progressive names are already ASCII. Qualify exclusive source fields, complete native full-name consumers, glyphs/allocation and representative display before integration. No catalogue UI was observed and no name correction has shipped.

All175 drafts preceded current-English extraction in this intake. Approved B48 recordsR71/R92/R370 supply Proof of Conquest/Proof/Proofs terminology; retain that consistency while leaving the broader terminology question separate. B41 keeps Hans’s ruins hypothesis, religious/cultural context, need to earn local trust and concrete examples of help. Arcadius’s internal-thought line adds no gender inference. Legacy COMMON parsing did not match the modern relocated directory; no parser was changed and no global technical re-audit was opened. Use registered/source-qualified term evidence rather than broadening that investigation.

Primary next-batch root: `work/analysis/Rafael_early_story_B36_B41_B51_B60_clean_20261104/`. Key files: `B36_B41_175_complete_clean_meanings_v1.json`, `B36_B41_source_identity_andFU_checkpoint_v1.json`, `B36_B41_all175_sealed_drafts_v1.json`, and `B36_B37_92_whole_exchange_comparison_v1.json`. Current bindings: `work/analysis/Rafael_B36_B41_current_20261104/current_effective.json`. Resume the remaining83 current comparisons, then consolidate and perform fresh formatting/storage/representative gameplay. The First Mate/adjutant shared deck-tooltip mismatch remains queued.

Preserve all earlier opening/trade/sea reviews, all later Hodram drafts, every ROM/evidence artifact and the full every-story/shared/town/random/player-text objective. No guide photos, pruning, commit/push or main promotion. Graphics artwork and the later older-record technical re-audit remain separate.
'''
    protected={'translations/release_stack.json':prep['registry_sha256'],
        'out/all_routes_combined_hodram_b191_b210_static_text_20261104_candidate.nds':'88e9984f767a0fa14bde5e9ce07392d1fbcf44fb41a6815e4ca466740fb82a15',
        'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'}
    checkpoint(mutation=ROOT/'tutorial_build_andstory_checkpoint_mutation_v1',batch_key='Rafael_SC0_B42_B43_early_tutorial_20261104',
        batch_updates=dict(new_credit=0,registered_profile=prep['profile'],registered_preparation=str(RELEASE/'registered_preparation.json'),
            production_qualification=str(qualification_path),production_qualification_sha256=sha(qualification_path.read_bytes()),
            semantic_rejections=7,first_build_session=4941,first_build_terminal_exit_code=1,first_build_path_failure=True,
            current_build_session=15896,current_build_work='work/rf_tut_1104_v2',build_observed_live_at_this_checkpoint=True,
            final_candidate_verification_andpatch_andown_startup_pending=True,
            remaining=['Poll existing retry15896','Complete manifest/patch/own-startup verification','Once-only integrated credit']),
        new_entries={new_key:pending},summary=summary,document=document,document_text=text,completed=10306,protected=protected)
    print('Registered tutorial retry15896 andnext175-record Rafael batch saved;10306 integrated completions andall earlier keys preserved.')
