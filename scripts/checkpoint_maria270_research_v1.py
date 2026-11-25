"""Persist the completed Maria270 research and exact new parent without release credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v8 import checkpoint

ROOT=Path('work/Maria_B37_B50_clean_20261109')
def main():
    ready_path=ROOT/'research_final_v1/research_completion.json';ready=load(ready_path)
    actual_path=ROOT/'gameplay270_review_v1.json';actual=load(actual_path)
    assert (ready['records'],ready['revisions'],ready['retentions'])==(270,161,109)
    assert ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
    assert (actual['distinct_source_utterances'],actual['distinct_body_pages'],actual['offline_only_source_utterances'])==(63,69,203)
    assert actual['complete_original_host_nonspeech_setup_reaches_resupply_andordinary_sailing']
    assert actual['ordinary_default_menu_returns_to_next_fixture_speech_observed']
    for p,h in ready['evidence'].items():assert digest(p)==h
    release=load('work/market_goods_info_terminator_release_v1/registered_release_verification.json')
    evidence={str(p):digest(p) for p in [ready_path,actual_path,ROOT/'stored270_reconstruction_v1/reconstruction.json',
        ROOT/'stored270_v1/stored_native_verification.json',ROOT/'stored270_catalogue_v1/all266_stored_effective_body_bindings.json',
        ROOT/'loaders270_v1/verification.json',ROOT/'market_parent_qualification_v1.json',Path(__file__)]}
    summary=('Maria270 now passes all five individual review gates: 161 revisions/109 retentions, 26 wrap improvements, '
        '272 checked body pages, four captions and 28 scoped names. Four emulator runs observe 63 utterances/69 distinct '
        'pages, both default menu returns, the FE transition and resupply/sailing; 203 bodies remain offline-only. '
        'Stored/native checks preserve the registered 243e21fc market correction. Registered integration remains; '
        'integrated 19,462/main unchanged. Complete B50/16 and full editorial scope remain active.')
    text='''# Maria270 research checkpoint — November 9, 2026

**All 270 individual reviews in 13 complete B37–B49 exchanges pass five gates:** 161 dialogue revisions and 109 justified retentions. All 272 final native body pages, four captions and 28 scoped names/42 strings are checked and directly viewed. The 26 wrap improvements, six justified layout retentions and four reclaimed pages preserve every word. Reuse [the offline review](editorial_Maria270_offline_20261109.md); no source meanings, independent drafts, contextual findings or accepted layouts were redone.

The final manuscripts are `translations/maria_B37_B49_final_review_v1.json` and `translations/maria_B37_B49_scoped_names_final_v1.json`. Exact source/current and stored references, individual findings, retention reasons, observations and all five gates are recorded per object. The full 286-record source-first manuscript remains intact; B50’s 16 records still await its separate long-FE display resolution.

All new evidence is under `work/Maria_B37_B50_clean_20261109`:

- `research_final_v1/research_completion.json` seals the final manuscripts and `release_plans.json`. The registered integration and completion-credit flags remain pending.
- `market_parent_qualification_v1.json` proves the exact registered market-only transformation from the old native Maria301 context to the current cumulative parent. All story archives, font, COMMON, names and relevant renderer/macro/getter instructions match. The old Maria3 snapshot retains its actual identity. Fresh stored and catalogue calls reject reads/execution of the changed market fields and new literal allocation; no unexpected dependency occurred. This is a narrow source-locked qualification, not a generic ARM9 waiver.
- `stored270_reconstruction_v1/reconstruction.json` reconstructs all 13 reviewed blocks, 490 commands and 96 relative sites. Complete clean/current block, archive and serialized parent inverses pass. Only SC3 changes; the six-section ARM9, new market literal and pointers, town capture opcode, ASCII right-bound correction and all unrelated components remain exact. Its pinned research ROM is `reviewed_RESEARCH_ONLY.nds`, SHA-256 `5a44078512a7d1dc144b4c9401ab58d22cc95b1d1a09148da57a8728a23ee1f6`; it is not a release handoff.
- `stored270_v1/stored_native_verification.json` passes all 266 bodies/272 pages, four labels and 480 native relocated branch cases. Only 138 parity-dependent pages were freshly rendered; 134 exact compiled pages were reused. All complete leading/internal/trailing glyphs, native FE rows, buffers, canaries, substitutions and bounds pass.
- `stored270_catalogue_v1/all266_stored_effective_body_bindings.json` passes every complete original pre-macro lookup, input canary, stack and four-MiB unowned-memory guard. `loaders270_v1/verification.json` passes 303 complete SC3 loads/cache hits, one null EV action and 606 native parent handoffs/first reads. Other unchanged route archives were not replayed.
- `gameplay270_review_v1.json` binds four coldboot runs totaling 41,924 frames: three broad display fixtures and one small exit test. All 63 distinct utterances/69 distinct pages match complete native body/header masks and blank guards in exact declared order. All six two-page cases, the FE unseen voice followed by Xien, both reclaimed B49 paragraphs, the complete question tag and eight source-bound headers are observed. Every page is directly viewed in 14 readable sheets; both menus have their own viewed sheets. The remaining 203 bodies are explicitly listed as offline-only.

Both two-choice menus show all four corrected labels, native centering/highlights and default selection0. Ordinary 16-frame A inputs at frames6160 and7840 return to the next declared speech at6177 and7858. Numeric VM returns, the other choices/cancel and original conditional story branches remain offline evidence. The fixtures deliberately sequence source-ordered alternatives; they do not claim one earned story chronology, original location or natural activation. The inherited isolated system unlock is disclosed as unearned; six route save slots and the original donor save remain unchanged. No savestate or gameplay RAM/RNG/money/roster/event override, hardware or full catalogue UI claim.

The three short runs end before the original host exit finishes; they are not proof of a production fault. The focused two-utterance/three-page test keeps all 47 source host initialization/setup/effect/cleanup commands and provides enough ordinary input time. Its complete text pages match again, then actual gameplay reaches the resupply prompt at6659, departure from Hangzhou at7628 and sailing at10001. All three transition captures are directly viewed. No production prose, body bytes or engine code changed during these gameplay tests.

Pre-output fixture-v1 derivation and menu-v1 bridge-schema rejections are preserved. Successful fixture preparation isv2; menu analyzer v2 resolves exact original complete provider/raster receipts through the stored bridge. The research-finalizer v1 stopped before writing because the empty style scope intentionally has no compiler-case list; v2 explicitly verifies zero objects/slots/stored alternatives. No checks were waived and no case counts were fabricated. All generated ROMs, prior drafts, plans, failures and evidence remain pinned/preserved. No process is live at this checkpoint.

Next extend the **registered 710-entry/114-layer/45-check market candidate** `243e21fce256c285b47556c0f0b3789911ead5a86a372edf6b420e36f5c19910` through the registered cumulative workflow. Reconcile its profile, retain the 16-byte read-only autoload section at01FFD000 and both Local/Cargo pointers, preserve the original town code at01FFC6AC, and add only the reviewed 13 SC3 blocks. Require the source-bound transaction, complete inverses, exact clean-input patch, candidate-owned startup and protected getters before registration/once-only credit. Do not promote main without user acceptance.

Integrated coverage remains **19,462 = 11,710 revisions + 7,752 retentions**; **6,436 native story objects remain**, including this unintegrated batch and B50. The promoted main and canonical baseline remain unchanged. Full story/town/shop/random/name/player-prose scope, unfinished prior contextual passes and the held B50 issue stay in the goal. No guide photos. Deferred graphics artwork and the later older-record technical re-audit remain separate.
'''
    checkpoint(mutation=ROOT/'research270_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria270 research complete; registered cumulative integration next.',
            all_current_batch_fifth_gates_pending=False,current_batch_not_yet_integrated=True,
            native_job_live=False,registered_build_live=False,guide_photos=False,
            next_action='Register270 reviewed B37-B49 records over the market-fixed cumulative parent; exact patch andown startup/getters beforeonce-only credit. Preserve held B50.'),
        additional_updates={
            'Maria_SC3_B37_B50_clean_20261109':dict(new_credit=0,subset_five_gate_approval=str(ready_path),
                subset_five_gate_approval_sha256=digest(ready_path),source_objects=286,active_complete_exchange_subset=270,
                withheld_complete_exchange=50,withheld_records=16,registered_integration_pending=True),
            'Maria_SC3_B37_B49_display_20261109':dict(new_credit=0,all270_individual_five_gates_pass=True,
                all_fifth_formatting_gates_pending=False,stored_andrepresentative_checks_pending=False,
                stored_checks_pass=True,stored_pages=272,stored_branch_cases=480,stored_catalogue_bodies=266,
                native_archive_loads=303,native_parent_handoffs=606,actual_current_batch_gameplay_observations=63,
                actual_distinct_pages=69,offline_only_body_records=203,observed_menu_instances=2,
                observed_choice_labels=4,qualified_scoped_names=28,registered_integration_pending=True,evidence=evidence)},
        summary=summary,document='docs/editorial_Maria270_research_20261109.md',document_text=text,completed=19462,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],
            release['canonical_base']:release['canonical_sha256']})
    print('Saved270-review research checkpoint;19,462 integrated,market candidate andmain unchanged;zero new credit.')

if __name__=='__main__':main()
