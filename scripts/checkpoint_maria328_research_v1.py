"""Publish the completed328-review research gates with registration and credit still pending."""
from pathlib import Path
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint

def main():
    ready_path=ROOT/'research_completion_v1/research_completion.json';ready=load(ready_path)
    release_path=Path('work/maria303_release_v1/registered_release_verification.json');release=load(release_path)
    rebuilt_path=ROOT/'reconstruction_v1/reconstruction.json';rebuilt=load(rebuilt_path)
    assert (ready['records'],ready['revisions'],ready['retentions'])==(328,143,185) and ready['all_individual_five_gates_pass']
    assert ready['registered_integration_pending'] and ready['new_credit']==0
    for p,h in ready['evidence'].items():assert digest(p)==h
    assert digest('translations/release_stack.json')==release['registry_sha256'] and rebuilt['parent_sha256']==release['candidate_sha256']
    evidence={str(p):digest(p) for p in [ready_path,rebuilt_path,ROOT/'gameplay_review_v1.json',
        ROOT/'stored_v1/stored_native_verification.json',ROOT/'stored_catalogue_all_v1/all314_stored_effective_body_bindings.json',
        ROOT/'loaders_v1/verification.json',Path(ready['manuscript']),Path(ready['names']),release_path,Path(__file__)]}
    summary=('Maria328 now passes all five individual review gates: 143 revisions, 185 justified retentions and 24 scoped names. '
        'All 321 body pages and 15 captions pass native/visual/storage checks; 314 effective lookups, 315 branch cases, '
        '303 loads and 606 handoffs pass. Representative emulator QA observes 43 source bodies/48 pages, six captions, '
        'the new FE continuation/menu return, three style objects and ordinary sailing. Twelve layout changes reclaim one page; '
        'two FE defects and two corrupt rescue replies are corrected. Registered integration and once-only credit are next. '
        'Integrated 20,361, registered d42dcd8e, main and the full editorial scope remain unchanged.')
    text=f'''# Maria328 research ready — November 9, 2026

**All 328 individual reviews now pass all five gates: 143 revisions and 185 justified retentions across 21 complete exchanges.** The 24 scoped name/role reviews also pass. Registration and completion credit remain pending; this is a completed research batch, not a new registered candidate or main promotion.

Continue under `work/Maria_B73_B95_clean_20261109`. The final source manuscript is `translations/maria_B73_B95_final_review_v1.json`; names are `translations/maria_B73_B95_scoped_names_final_v1.json`. `research_completion_v1/research_completion.json` binds every prerequisite and both final hashes. The unchanged logical paragraphs, exact source/current references, individual findings and retention reasons are preserved. B87 R139 remains one source object with two physical FE children. `research_completion_v1/source313_release_plans.json` contains its first-panel plan and both child plans; the physical plan still has 314 bodies and 321 pages. All prior meanings, independent drafts, comparisons and superseded trials remain intact.

Reuse the [offline checkpoint](editorial_Maria328_offline_20261109.md) for the prose, names, 12 layout changes, one reclaimed page, two FE defects, 20 non-ASCII targets and two corrupted rescue replies. No wording, font, physical viewport or runtime instructions were changed to fit. Full native/visual approval covers all 321 pages, 15 captions and 28 name strings.

**Storage is complete.** `reconstruction_v1/reconstruction.json` binds 21 complete SC3 blocks, 554 final commands, 63 relative sites and exact clean/current/block/archive/serialized-ROM inverses. Research ROM SHA-256 is `{rebuilt['research_ROM_sha256']}`. Only SC3 changes. The qualified FE helper adds one exact original six-byte FE control under the original conditional ancestors; seven invalid insertions are rejected. Final offsets compose both relocation stages for ordinary bodies, menus and styles. Do not reapply the unrelated B54 storage or B62 alignment amendments.

Passing proofs are `stored_v1/stored_native_verification.json` (290 ordinary physical commands plus 24 style bodies, all 321 pages, 148 freshly checked parity-dependent pages/173 exact reused pages and 315 native branch cases), `stored_catalogue_all_v1/all314_stored_effective_body_bindings.json`, `loaders_v1/verification.json` (303 complete loads/cache hits and 606 parent handoffs), and `compiled_styles_v1/compiled_style_objects.json` (four full objects, 32 target slots and 36 rejected compiler cases). Each invocation exited 0. All stored pixels remain identical to the directly reviewed pages.

**Representative actual emulator QA is complete.** `gameplay_review_v1.json` binds one 22,001-frame cold boot, 43 original source bodies/44 physical candidates/48 pages, six captions in two three-choice menus, 96 complete body planes and 72 header planes. All eight body contact sheets, the menu sheet and host-transition sheet were directly viewed. The two-panel FE riddle advances with ordinary A input through the menu to the next named speech without an extra blank panel. The bean tutorial's repaired rows, four progressive continuations, FI substitution, FE/named transitions and three complete dynamic style objects pass. The formerly corrupted `SC3_B95_STYLE_400_42` reply is observed cleanly; `_18` remains offline-only. Both menus show option 0 and return normally. Resupply, departure and ordinary sailing follow with the original host setup/effects/cleanup preserved. The coverage audit's first version confused original and relocated menu offsets; v2 checks both separately (for example, B87 source 816 / stored 796). No ROM correction was required for that audit issue.

The disclosed Hangzhou QA sequence copies selected native commands, uses the existing isolated system-only unlock and leaves original conditional activation, locations, chronology, rewards, story effects and hardware unvisited. The remaining 270 source body objects and nine captions have offline native/storage coverage. Other choices and cancellation have native offline proofs, without a claim of actual controller activation. Full catalogue name strings have font proofs; catalogue UI layout and future role assignments remain unvisited. No guide photos are required. Fixtures and all ROMs are pinned and preserved. No worker is live.

**Next freeze the pure registered Maria328 transaction over Maria303 and integrate immediately through the cumulative workflow.** Preserve all 714 predecessor entries, 114 accepted layers, market read-only allocation and both pointers, six-section ARM9, ASCII right-bound correction and v2 source25 guard. Reconstruct the exact research output, including the FE insertion and composed references. Require a byte-exact clean-input patch, the candidate's own Maria/Hangzhou startup and 24 protected name getters before registration and once-only credit. Main promotion requires user acceptance.

Registered candidate remains `work/maria303_release_v1/all_routes_maria303_candidate.nds`, SHA-256 `{release['candidate_sha256']}`, with 714 entries and 49 passing release checks. Integrated totals stay **20,361 = 12,245 revisions + 8,116 retentions**. Native story objects remaining stay **5,537 (Lil 1,805 / Maria 3,732)**; these 328 receive zero credit until registered integration. The user's tested older Rafael2952 build predates the registered Market correction, which remains preserved here.

The full objective remains active: every unfinished storyline and prior contextual pass, shared shop/town/random exchange, name/role label and remaining player-facing prose. Earlier completed coverage and early Rafael/tutorial priority are preserved. Deferred graphics artwork and the later older-record technical re-audit remain separate.
'''
    checkpoint(mutation=ROOT/'research_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria328 all five review gates passed; registered cumulative integration next.',
            current_batch_not_yet_integrated=True,all_current_batch_fifth_gates_pending=False,current_batch_five_gates_pass=328,
            proposed_revisions=143,justified_retentions=185,current_body_pages_native_andvisually_reviewed=321,
            current_batch_actual_source_body_objects=43,current_batch_actual_body_pages=48,current_batch_actual_caption_strings=6,
            native_job_live=False,registered_build_live=False,guide_photos=False,
            next_action='Freeze and execute pure Maria328 registered transaction, including the B87R139 FE continuation; exact clean-input patch and own startup/getters before registration/credit.',
            current_batch_evidence=evidence),
        additional_updates={'Maria_SC3_B73_B95_clean_20261109':dict(new_credit=0,all_fifth_formatting_gates_pending=False,
            all_individual_five_gates_pass=True,five_gate_reviews=328,scoped_five_gate_names=24,
            final_review=ready['manuscript'],final_review_sha256=ready['manuscript_sha256'],
            stored_native_pass=True,stored_catalogue_pass=True,complete_archive_loaders_pass=True,
            source_owned_FE_continuation_storage_andactual_transition_pending=False,
            stored_script_allocation_branches_andrepresentative_gameplay_pending=False,representative_gameplay_pass=True,
            actual_gameplay_observations=43,current_batch_actual_gameplay_observations=43,
            actual_physical_body_candidates=44,actual_body_pages=48,actual_caption_strings=6,
            offline_only_source_body_objects=270,offline_only_caption_strings=9,
            registered_integration_pending=True,research_completion=str(ready_path),research_completion_sha256=digest(ready_path),progress_evidence=evidence)},
        summary=summary,document='docs/editorial_Maria328_research_ready_20261109.md',document_text=text,completed=20361,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    print('Saved328 five-gate research checkpoint; registration and credit pending; main and full scope preserved.')

if __name__=='__main__':main()
