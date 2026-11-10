"""Record the resolved FE risk without changing registered builds or adding source credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint

ROOT=Path('work/Maria_B50_FE_resolution_20261109_v3')
def main():
    ready_path=ROOT/'research_completion_v1.json';ready=load(ready_path)
    assert ready['all_individual_five_gates_pass'] and (ready['records'],ready['revisions'],ready['retentions'],ready['native_pages'])==(16,9,7,17)
    for p,h in ready['evidence'].items():assert digest(p)==h
    release=load('work/maria270_release_v1/registered_release_verification.json')
    assert digest('translations/release_stack.json')==release['registry_sha256']
    evidence={str(p):digest(p) for p in [ready_path,Path(ready['manuscript']),ROOT/'gameplay_review_v1.json',ROOT/'offline_approval_v1.json',
        ROOT/'reconstruction_v1/reconstruction.json',ROOT/'stored_v1/stored_native_verification.json',ROOT/'source16_release_plans.json',Path(__file__)]}
    summary=('The held B50 exchange is research-complete: 16 reviews/9 revisions/7 retentions, all five gates and17 viewed '
        'native panels pass. The full139-character paragraph uses the already-qualified exact-control FE continuation; '
        'the blank-row defect andtwo awkward wraps are fixed. Stored checks,303 loads/606 handoffs andactual A/page/next-line '
        'plusresupply/sailing pass. Registered integration remains; registered5a440785,integrated19,732/main andfull scope '
        'are unchanged. No prose,font,viewport orengine changes;zero new credit.')
    text='''# Maria B50 FE research checkpoint — November 9, 2026

**The separate B50 display risk is resolved in research.** All16 source reviews (nine revisions/seven justified retentions) now pass five gates, preserving their original Japanese meanings, independent drafts, contextual comparisons and every word of reviewed English. There are17 native panels for16 source utterances; the additional panel is formatting, not another translation or completion credit. Registered integration and candidate-owned release checks remain.

Use the exact artifacts under `work/Maria_B50_FE_resolution_20261109_v3`:

- `research_completion_v1.json` seals `translations/maria_B50_final_review_v1.json`, `source16_release_plans.json` and all research evidence. The16 final records bind exact clean/current references, individual findings, retentions, five gates and planned stored references. R43 has both references in `planned_integrated_native_pages`; its primary encoded field is explicitly only its first panel.
- `source16_manuscript.json`, `physical17_manuscript.json`, `pagination_owners.json` and `source_and_runtime_binding.json` preserve the complete source exchange. B50 is byte-exact between the old native context and registered Maria270. The exact intervening market transformation and SC3-only append preserve COMMON/font/name and macro code/data. Old proof identities remain disclosed; fresh current Maria3 progressive and null-actor FI calls pass four alignments each. Three source FI occurrences remain unchanged.
- `plan_v5/automatic_plans.json` uses the existing guarded FE36 budget where needed, with zero errors/warnings and no QA waivers. `final_native_v1.json` contains all17 passing final panels and their directly viewed sheet bindings. Initial native checks cover68 alignments; only the two later wrap improvements are rerendered/eight alignments. Fifteen matching panels/60 selected alignment proofs are reused. All17 final pages, their superseded trials and the successful diagnostic matrix pages are directly viewed.
- `offline_approval_v1.json` records the R36 blank-row fix, complete R43 paragraph, improved R57 noun phrase and R76 three-row report. The rejected grammar-warning annotation was unnecessary: the final ordinary boundaries pass the original QA without a waiver. No authored breaks, font, viewport or engine edits.
- `reconstruction_v1/reconstruction.json` independently executes unchanged `rebuild_block` and `insert_FE_continuations`, preserving every original command and complete preamble. One exact `0040ffff00fe` continuation is added in the same source scope. All seven wrong-control/offset/child/prose/omission/index cases reject. Final B50 has38 commands, no relative operands, and1068 bytes within the9216-byte allocation. Complete clean/current block, archive and serialized NDS inverses pass. Only SC3 B50 changes; the six-section ARM9, registered market literal/pointers, town code, ASCII right-bound correction, other routes, names, UI and artwork remain exact.
- The pinned research ROM is `reconstruction_v1/reviewed_FE_paginated_RESEARCH_ONLY.nds`, SHA-256 `de2ffce183ec277bcdd853b0b2e13437468dc1e102673c064e1767e2ac9fbfcd`. This is not a registered release or user testing handoff.
- `stored_v1/stored_native_verification.json` checks17 complete bodies/pages, rerendering only eight parity-dependent pages and reusing nine exact planes. All native glyphs, first/internal/final characters, guarded row membership, bounds, consumption and canaries pass. There are zero branch cases because the complete source block has no relative operands; no predicate coverage is fabricated. `catalogue_v1/all17_stored_effective_body_bindings.json` checks every original pre-macro lookup with full input/stack/four-MiB guards. `loaders_v1/verification.json` passes303 complete SC3 loads/cache hits, one null EV action and606 original parent handoffs/first reads. Other unchanged routes are not replayed.
- `gameplay_review_v1.json` binds one13,001-frame current native-command fixture. All16 source utterances/17 physical panels match the complete native body/header masks and blank guards in exact order. All pages are directly viewed in three readable sheets. Both Maria Li and Xien Yan headers match; FE remains the native null-actor consumer, with no assigned actor254/fallback208. The full conditional premise appears at6185, ordinary A at6400 shows its unchanged consequence at6425, and A at6640 returns to the next source line at6665. Both panels have complete captured text before their A presses. The original47-command QA host returns to resupply at10019, departure at10988 and sailing at13001; those three captures are directly viewed.

The139-character R43 counterfactual is not shortened. Its first panel ends with the complete conditional premise `...in the Far East,`; the second gives `England might have taken you on as a useful subordinate one day...`. The single paragraph space becomes the native panel boundary; all punctuation, nuance and cultural `wokou pirates` context remain. This reuses the already registered source-owned FE pagination method from the earlier Rafael B84 tutorial, rather than changing native geometry. R36 keeps its full boast without the unintended blank row. R57 now keeps `admiral like you` together instead of isolating `admiral`; R76 uses three substantial rows with an ordinary trading/rights boundary in uninterrupted prose. Every changed layout receives fresh native checks and direct review.

The initial break-encoding matrix preserves all original painter assertions. Some bare-LF R36 cases pass, but the full R43 still fails native bounds/consumption; no global bare-LF permission is inferred. The first diagnostic event copy occurred after an early-return assertion and stopped the producer; v2 moves only that read-only diagnostic copy earlier, preserving every assertion. All failed producers, raw planes, rejected preferences and old proofs remain. The successful page preparation isv2, planner is `plan_maria_B50_FE_pages_v2.py` with `preferences_v4_no_waiver.json`, and fixture preparation isv2. Missing adapter/menu namespace attempts stopped before output and are retained; the speech-only helpers explicitly inventory zero menu/style objects rather than pretending to have their proofs.

The initialized fixture uses the existing disclosed system-only unlock and ordinary input, not an earned late-game path. The original donor and all six route slots remain unchanged. Original B50 cutscene art/effects, natural activation, story outcomes, full catalogue UI and hardware remain unvisited. All original B50 scene/effect commands remain in the research ROM and byte maps; the display fixture runs copied speech commands behind the independently source-complete Maria QA host. No guide photos. Name/role localization is retained from the exact previously reviewed four relevant identities (Maria, Xien, Richard and Clifford); no name field, rank or relationship is invented or changed.

**Next integrate all16 source records/17 physical panels through a registered cumulative successor over Maria270** (`5a44078512a7d1dc144b4c9401ab58d22cc95b1d1a09148da57a8728a23ee1f6`,711 entries/114 accepted layers/46 checks). Reuse the pure FE continuation integration in `dk4tool/patch/rafael_story_b81_b84_release_v1.py`, with this complete SC3 source/current/reconstruction/native/stored/actual evidence. The ordinary one-record/one-command integration path is insufficient for R43. Retain both native references under its single source record. Carry the registered multi-archive source25 guard from `format_safety_relocated_v2.py`; its five SC0 and two SC3 B38 bindings remain exact because B50 has no source25 speakers. Require the final four-archive format check, whole parent inverse, exact clean-input patch, candidate-own startup and both protected getters before registration and once-only credit. Do not promote main without user acceptance.

Integrated totals remain **19,732 =11,871 revisions +7,861 retentions**; **6,166 native story objects remain** (Lil1,805/Maria4,361), including these16 unintegrated reviews. The current registered testing candidate remains [Maria270](editorial_Maria270_registered_20261109.md); its registry, ROM, manifest, patch, canonical baseline, main and every earlier artifact are unchanged. After B50 integration, continue with substantial complete-exchange batches from B51 onward; reuse completed source/prose and display proofs, and do not replay B37–B49. Every storyline, unfinished prior contextual pass, town/shop/random exchange, name, wrap/glyph and remaining player prose stays in scope. Deferred graphics artwork and the later older-record technical re-audit remain separate. No current-batch process is live.
'''
    checkpoint(mutation=ROOT/'research_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='B50 complete research:16 source reviews/17 panels;registered cumulative integration next.',
            current_batch_not_yet_integrated=True,all_current_batch_fifth_gates_pending=False,native_job_live=False,
            registered_build_live=False,guide_photos=False,
            next_action='Register B50 source-owned FE continuation over Maria270;exact patch,own startup/getters andonce-only16 credit. Thencontinue substantial B51+ source-first exchanges.'),
        additional_updates={'Maria_SC3_B37_B50_clean_20261109':dict(new_credit=0,
            remaining_unintegrated_source_objects=16,held_FE_native_risk_resolved_in_research=True,
            held16_all_individual_five_gates_pass=True,all_fifth_formatting_gates_pending=False,
            held_research_approval=str(ready_path),held_research_approval_sha256=digest(ready_path),
            withheld_reason='Native FE risk closed in research;registered cumulative integration,exact clean-input patch andcandidate startup/getters remain.',
            registered_integration_pending=True)},
        new_entries={'Maria_SC3_B50_FE_research_20261109':dict(new_credit=0,source_objects=16,complete_exchanges=1,
            proposed_revisions=9,justified_retentions=7,physical_native_commands=17,native_pages=17,
            source_FE_records=12,native_FE_panels=13,additional_exact_FE_controls=1,
            all16_individual_five_gates_pass=True,all_final_native_pages_directly_viewed=True,
            actual_source_utterances=16,actual_native_panels=17,actual_frames=13001,offline_only_source_utterances=0,
            FE_continuation_andfollowing_A_return_observed=True,source_complete_QA_host_exit_observed=True,
            whole_scene_natural_activation_andcutscene_effects_unvisited=True,registered_integration_pending=True,evidence=evidence)},
        summary=summary,document='docs/editorial_Maria_B50_FE_research_20261109.md',document_text=text,completed=19732,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    print('Savedresolved B50 research checkpoint;registered Maria270/main and19,732 integrated unchanged;zero new credit.')
if __name__=='__main__':main()
