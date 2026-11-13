"""Publish the registered batch, preserving every earlier credit and release."""
import os
from pathlib import Path
from scripts.meaning_maria330_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint

def main():
    releasepath=Path('work/maria330_release_v1/registered_release_verification.json'); release=load(releasepath)
    completepath=Path('work/maria330_release_v1/completion_checkpoint.json'); complete=load(completepath)
    censuspath=Path('work/story_source_coverage_20261109_SC3_v8/coverage.json'); census=load(censuspath)
    ledger=load('translations/editorial_review_current_v1.json'); actual=load(ROOT/'gameplay_review_v1.json')
    ready=load(ROOT/'research_completion_v1/research_completion.json')
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks'])==(716,114,51)
    assert complete['new_credit']==330 and complete['counts']==dict(completed=21019,revised=12637,retained=8382)
    assert ledger['records_editorially_completed']==21019 and not ledger['full_goal_complete']
    assert ledger['current_integrated_candidate']['sha256']==release['candidate_sha256']
    assert len(census['records'])==5129 and len(census['missing'])==3074 and census['new_exact_bindings']==330
    assert not census['inventory_failures'] and not census['legacy_source_bindings_not_exact']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert digest('translations/release_stack.json')==release['registry_sha256']
    assert digest(release['candidate'])==release['candidate_sha256'] and digest(release['patch'])==release['patch_sha256']
    assert digest(release['manifest'])==release['manifest_sha256']
    assert Path(release['candidate']).read_bytes()==Path(release['exact_clean_reconstruction']).read_bytes()
    bindings=load(release['exact_record_bindings'])['records']
    assert len(bindings)==330 and sum(len(r['registered_native_pages']) for r in bindings)==332
    assert ready['all_individual_five_gates_pass'] and actual['all58_selected_pages_two_captions_andboth_host_transitions_directly_viewed']
    packet=load(censuspath.with_name('residual_clean_source_packet.json'))
    nextgroups=[(g['block'],len(g['records'])) for g in packet['groups'][:16]]
    evidence={str(p):digest(p) for p in [releasepath,completepath,censuspath,Path('translations/maria330_integrated_final_review_v1.json'),
        ROOT/'research_completion_v1/research_completion.json',ROOT/'gameplay_review_v1.json',
        Path('work/maria330_release_v1/own_registered_startup_verification.json'),Path('work/maria330_release_v1/own_registered_name_getters_v1.json'),Path(__file__)]}
    summary=('Maria330 is registered and credited once: 249 revisions/81 justified retentions across26 exchanges and26 scoped name reviews. '
        'Three pages reclaimed,seven clause boundaries andone orphan repaired;three mixed-font Latin lines andone Japanese grant corrected. '
        'All338 body pages,two captions and29 name strings pass;two emulator runs observe53 source bodies/55 physical candidates/58 pages,both menu options '
        'andboth FE continuation returns. The cumulative716-entry/114-layer candidate passes51 checks,exact clean-input reconstruction,own startup '
        'and24 protected getters. Integrated21,019;4,879 native story objects remain (Lil1,805/Maria3,074). Main andthe full objective are unchanged.')
    text=f'''# Maria330 registered checkpoint — November 9, 2026

**330 original records are integrated once: 249 revisions and 81 justified retentions across 26 complete exchanges.** All five review gates pass. The 26 scoped name/role reviews retain 29 approved strings. Exact Japanese, prior English, final English, individual findings and retention reasons remain in `translations/maria330_integrated_final_review_v1.json` and `work/maria330_release_v1/exact_integrated_record_bindings.json`.

Cumulative [ROM](../work/maria330_release_v1/all_routes_maria330_candidate.nds), SHA-256 `{release['candidate_sha256']}`. [Clean-input patch](../work/maria330_release_v1/all_routes_maria330_candidate.xdelta), SHA-256 `{release['patch_sha256']}`. [Manifest](../work/maria330_release_v1/all_routes_maria330_candidate.manifest.json), SHA-256 `{release['manifest_sha256']}`. The patch reconstructs the exact ROM from clean `{release['clean_input_sha256']}`. All 715 predecessor entries and 114 accepted layers are retained; 51 checks pass. The candidate's own 31,000-frame startup reaches Hangzhou and passes 24 protected name-getter checks. All six startup checkpoints were viewed. Main remains unchanged; promotion requires user acceptance.

**Editorial and wrapping:** The pass corrects geography and personal/emotional distinctions while preserving the execution/reward account, humor, approved terms, controls and substitutions. Three premature pages are reclaimed without changing a word: B98R13, B106R16 and B115R4. Seven closing clauses and the orphaned figurehead See are repaired. Three mixed-font Latin I defects at B105R23, B110R11 and B121R19 now render consistently; B118R8's Japanese grant is translated. Documented shorter setup rows preserve complete closing thoughts. Reuse [the body-display checkpoint](editorial_Maria330_body_display_20261109.md) for individual layout reasons.

**Offline checks:** All 338 final body pages, two captions and 29 scoped name strings were visually reviewed. The 1,320 native alignment cases reuse exact completed receipts. Storage checks 295 ordinary commands and 35 style alternatives, with 156 fresh parity-dependent pages and 182 exact reused pages. All 330 effective lookups, 380 native relative cases, 303 whole-SC3 loads and 606 handoffs pass. Six complete style objects preserve all eight-slot aliases. The two-choice menu passes six provider alignments, 18 bridged returns and eight caption style planes. Name planes use 13 fresh and 16 dependency-exact prior proofs; catalogue UI remains unvisited.

**Observed emulator coverage:** Two disclosed cold boots total 34,402 frames and observe 53 source bodies, 55 physical candidates, 58 pages, both captions and both menu selections. All body sheets and host transitions were viewed. Complete comparisons cover 116 body holds, 100 header holds and six menu samples. Both added FE continuations advance by ordinary A input without blank panels; the three glyph repairs, translated grant, five complete style objects, pagination and named returns pass. Both hosts return through resupply and departure to sailing. The remaining 275 source bodies are offline-only. Original optional conditions, locations, chronology, rewards, branch/stat outcomes, catalogue UI and hardware remain unvisited. The isolated system unlock is disclosed, not earned. No guide photos are collected.

**Release transaction:** `reconstruction_v2/reconstruction.json` binds the unchanged v1 binary and completes the native-adapter metadata. All 26 owned blocks, 585 commands, 76 relative sites and full clean/current/block/archive/serialized-ROM inverses pass. B116R41 and R51 each preserve one complete paragraph in two FE children under the original six-byte control. There are 330 source records and 332 stored references; the extra commands receive no source credit. Fourteen invalid FE insertions and eight malformed production scopes are rejected. Partial producers and every earlier ROM, draft and proof remain preserved.

Use `dk4tool/patch/maria330_release_v1.py` and `scripts/build_registered_maria330_v1.py` (registration: `--register`). Preserve the entire predecessor, Market read-only allocation and Local/Cargo pointers, six-section ARM9, COMMON, fonts, graphics, ASCII right-bound correction and v2 source25 guard. Earlier B54/B62 amendments are already included. This retains the Market Goods Info correction missing from the user's older Rafael2952 build. `research_completion_v1/research_completion.json` and `gameplay_review_v1.json` bind detailed prerequisites and exact coverage.

Integrated totals: **21,019 = 12,637 revisions + 8,382 retentions**. Historical source/prose/draft counts remain three higher at 21,022. The SC3_v8 census rechecks all 5,129 source positions: 2,055 covered, 3,074 remaining, with no duplicate or unresolved bindings. Remaining native story objects: **4,879 (Lil 1,805 / Maria 3,074)**. Shared/player-facing prose remains separately in scope.

**Next:** Select complete exchanges from `work/story_source_coverage_20261109_SC3_v8/residual_clean_source_packet.json`; first block/object counts: {nextgroups}. Save clean meanings and independent logical drafts before comparing current English. Reuse matching technical proofs; changed text still needs fresh formatting and page review. Preserve early Rafael/tutorial priority and the full unfinished objective, including earlier contextual passes, shared town/shop/random dialogue and names/roles. Deferred graphics artwork and the later older-record technical re-audit remain separate. No promotion, cleanup, commit or push occurred. No worker is live.
'''
    mutation=ROOT/'registered_progress_checkpoint_v1'
    checkpoint(mutation=mutation,batch_key='editorial_execution_priority_20261104',batch_updates=dict(new_credit=0,
        current_batch='Maria330 registered andcredited once;next complete exchanges in SC3_v8.',current_batch_not_yet_integrated=False,
        all_current_batch_fifth_gates_pending=False,proposed_revisions=249,justified_retentions=81,current_batch_registered_andcredited_once=True,
        native_job_live=False,native_sessions=[],registered_build_live=False,registered_cumulative_build_live=False,registered_profile=release['profile'],
        remaining_native_story_objects=4879,remaining_native_Maria_objects=3074,guide_photos=False,
        next_action='Select complete SC3_v8 residual exchanges;clean meanings andindependent drafts before current-English comparison.',current_batch_evidence=evidence),
        summary=summary,document='docs/editorial_Maria330_registered_20261109.md',document_text=text,completed=21019,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    protocol=Path('docs/build_continuity_protocol.md'); before=protocol.read_bytes()
    prefix=('Maria330 is the registered successor to Maria328:716 entries,114 accepted layers and51 passing checks. '
        'Use `scripts/build_registered_maria330_v1.py` for staging andwith `--register` for registration;pure transaction is `dk4tool/patch/maria330_release_v1.py`. '
        'Own only the26 reviewed SC3 B96–B124 blocks;insert both B116R41/R51 FE continuations together andcompose every relocation. '
        '330 source objects bind332 stored references:330 physical bodies/338 pages plus two captions,without duplicated credit. '
        'Clean-input reconstruction,complete inverses,own startup and24 protected getters pass. Preserve the715-entry predecessor,market allocation/pointers, '
        'six-section ARM9,ASCII right-bound correction andv2 source25 guard. Main promotion requires acceptance. '
        'Continue from [the registered checkpoint](editorial_Maria330_registered_20261109.md);older entries below are history.\n\n')
    after=prefix.encode()+before; (mutation/'build_continuity_protocol.before').write_bytes(before)
    pending=protocol.with_name('build_continuity_protocol.Maria330.pending.md'); assert not pending.exists(); pending.write_bytes(after)
    assert protocol.read_bytes()==before; os.replace(pending,protocol)
    save(mutation/'build_protocol_update.json',dict(path=str(protocol),before_sha256=digest(mutation/'build_continuity_protocol.before'),
        after_sha256=digest(protocol),registered_release=str(releasepath),registered_release_sha256=digest(releasepath),no_release_orcredit_change=True))
    print('Published registered Maria330:21,019 integrated;4,879 native story objects remain;main/full scope preserved.')

if __name__=='__main__':main()
