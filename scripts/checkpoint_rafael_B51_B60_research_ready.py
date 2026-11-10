"""Preserve completed research checks and the user's early-game priority without awarding release credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v3 import checkpoint

ROOT = Path('work/analysis/Rafael_B51_B60_checked_20261104')
RUNTIME = Path('work/analysis/Rafael_B51_B60_current_runtime_20261104')
RELEASE = Path('work/analysis/Shared_tutorial_name_data_release_verified_20261104/registered_release_verification.json')

if __name__ == '__main__':
    release = load(RELEASE)
    ready_path = ROOT/'formatting_checkpoint.json'
    ready = load(ready_path)
    final_path = Path(ready['final_review'])
    names_path = Path(ready['scoped_names'])
    actual_path = ROOT/'actual_review.json'
    final, names, actual = map(load, [final_path, names_path, actual_path])
    assert ready['all_individual_five_gates_pass_in_research'] and ready['new_credit'] == 0
    assert len(final['records']) == 249 and all(all(r['review'].values()) for r in final['records'])
    assert len(names['records']) == 18 and actual['actual_utterances'] == 32 and actual['offline_only_utterances'] == 213
    summary = ('Rafael early story and all tutorials remain first. B51–B60 now has249 five-gate research reviews:102 revisions/147 retentions,38 wrap fixes/three ASCII-I corrections,253 offline body pages/four captions. '
        'Latest4b10fd67 dependencies,18 scoped names/roles,Fernan’s F field,full storage/catalogue/loaders and representative gameplay pass. '
        'Two initialized coldboots observed32 speeches/35 pages/four captions andall18 headers;213 speeches remain offline-only. '
        'Registered cumulative integration/clean-input patch remain;zero new completion credit. Verified release4b10fd67 and10525 completions/main remain unchanged. '
        'No live jobs;all prior work/ROMs/full scope retained;no guide photos.')
    document = Path('docs/editorial_rafael_B51_B60_research_ready_20261104.md')
    text = f'''# Rafael B51–B60 ready for registered integration — 2026-11-04

Rafael’s early storyline and all tutorials are the execution priority. The full all-story, earlier-translation, shared shop/town, random-scene and remaining player-facing scope remains active. Completed editorial work, justified retentions, coverage credit, evidence and all ROMs are preserved. Later Hodram drafts are retained. Graphics artwork and the later older-record technical re-audit remain separate. No guide-photo collection, pruning, main promotion or commit/push.

## Verified release remains unchanged

`{release['candidate']}` — SHA256 `{release['candidate_sha256']}` — profile `{release['profile']}`.

Registered seven-stage release:667 entries/114 accepted layers/25 passing checks, exact clean-input patch, own4001-frame Rafael startup and complete own RAM/getters. Proof:`{RELEASE}`. Patch:`{release['patch']}`, SHA256 `{release['patch_sha256']}`. Main remains `out/raphael_natural_v2_accepted_base.nds`, SHA256 `{release['canonical_sha256']}`. Registry SHA256 `{release['registry_sha256']}`.

Totals remain10525 integrated completions,6254 revisions/4271 retentions. Source/prose/draft counters retain10528 and their historical difference of three. The249 below have zero completion credit until registered release verification succeeds. All seven earlier stages, including ASCII right bounds and the four tutorial/two catalogue-field data spans, must survive the successor.

## Finished249-record research batch

Final individual reviews:`{final_path}`, SHA256 `{sha(final_path.read_bytes())}`. Scoped18-name review:`{names_path}`, SHA256 `{sha(names_path.read_bytes())}`. All five individual gates pass in research; no release or main-acceptance claim follows from that. Each row retains exact clean/current references, whole-exchange context, source-first draft provenance, a specific finding/retention reason, and a planned stored target reference.245 speeches plus four captions in two complete2100 objects:102 revisions/147 retentions.

The clean-source-first prose pass was already finished and was not restarted. B51–B60 contains alternative crew/strategy/event branches; numerical block order is not chronology. Important corrections include the Portuguese military summons, Silveira’s deducted reward joke, untranslated Huh?, future Africa conquest, Emilio’s indoor confinement, Uddin’s first-person leadership alternatives, Evergreen Lotus Leaf/Rigveda/Antony Kuhn references, Spain’s royal succession hypotheticals and the Mediterranean Proof. Already-natural wording such as Uddin’s “May it prove worthy of you” remains justified. No invented ranks, relationships or route chronology.

Body formatting/visual approval remains `work/analysis/Rafael_B51_B60_formatting_20261104/body_display_approval_v4.json`.253 final native body pages and all four captions were directly viewed offline.38 wrap fixes and three ASCII-I replacements in two retained speeches. Native216px progressive/228px FE geometry, four rows, substitutions, controls, complete first/internal/final glyphs, bounds and pagination pass. Existing exact native pages/planes were reused after explicit dependency qualification, without claiming fresh rendering. Keep the documented grammatical retention “The whole town chipped in,” and the reviewed B60R486 conditional page boundary; its complete insult noun phrase stays together.

## Current-parent/name qualification

`{RUNTIME/'dependency_qualification.json'}` explains the complete ee04bf6f→4b10fd67 ARM9 inverse with six typed data spans. SC0, COMMON, fonts, code outside those spans and all scoped actor/name inputs are exact. Four fresh own-Rafael default macro alignments pass. Compatible current manuscript/plans/native/menu receipts and current-effective bindings are all under `{RUNTIME}`. Original producers/proofs remain immutable.

All18 scoped progressive names/roles pass source/context/localization/naturalness/native formatting and live-header comparison.17 strings include two distinct Port Worker actors; Shopkeeper and Sailor remain appropriate source-bound roles. Retain approved character identities, progressive ordering and existing earlier F/E fixes. Catalogue middle components, unused Retainer metadata and global207-name approval are not silently approved by this scoped pass. Actor40’s full-middleＦong/Fong/von question remains separate.

Fernan Silveira’s new correction is actor35,column0 only: full-widthＦ→ASCII F, spelling unchanged. Seven owned bytes/six differing bytes, exclusive owner/interior-reference scan, complete parent inverse, original getters, four native name planes and eight negatives pass. Rebased proposal/plan/proposed ARM9 are in `{RUNTIME}`; target ARM9 SHA256 `d45932617dfffeac2932a5a8d398d236758a8c1a835081ab9601aea5ed67dac2`. It commutes exactly with all six current deployed data spans. Full catalogue UI remains unvisited; the corrected progressive header was observed in the research fixture.

## Stored blocks/catalogue/loaders finished

Reconstruction:`work/analysis/Rafael_B51_B60_rebuilt_20261104/reconstruction.json`. All ten complete mixed blocks rebuilt;333 blocks unchanged,438 commands/76 relative sites.245 speeches/four captions/two complete2100 objects/zero4100 style objects/three FE notices. Complete clean/current block, archive and serialized NDS inverses pass; all unowned commands and components remain exact.

Stored proof:`work/analysis/Rafael_B51_B60_stored_native_20261104/stored_native_verification.json`.253 pages,130 fresh parity-dependent pages/123 exact compiled-page reuses;380 relocated original native relative cases. Every stored plane equals its directly viewed compiled plane; complete consumption, boundaries and canaries pass.

Catalogue proof:`work/analysis/Rafael_B51_B60_stored_catalogue_20261104/all245_stored_effective_body_bindings.json`. Every245 body remains byte-exact through the original pre-macro lookup; complete unowned memory/stack/canaries are preserved. Former aliases cannot restore old wording, glyphs or wraps.

Loaders:`work/analysis/Rafael_B51_B60_loaders_20261104/verification.json`.343 full loads/cache hits and344 original EV0 actions;686 parent modes,20 fresh changed-block cases/666 exact qualified reuses. Code/payload instruction dependencies and unchanged block hashes match. These are controlled native tests, not natural event activation.

Research composition:`work/analysis/Rafael_B51_B60_focused_20261104/composition.json`. `scenes_Fernan_RESEARCH_ONLY.nds` combines only the ten SC0 blocks and the exclusive Fernan field over verified4b10fd67. Serialized inverses recover both the SC0-only research image and complete verified parent. Stored/catalogue/loader proofs carry forward by exact archive/code/font/pointer/unowned identity; they were not falsely reexecuted on this composition. All generated research/fixture ROMs are pinned. This is not a registered candidate or handoff build.

## Representative actual coverage finished

`{actual_path}` and `{ROOT/'actual_visual_approval.json'}`. Two ordinary-initialized coldboots,18662 frames total.32 distinct speeches/35 complete body pages and all four choice captions observed;213 speeches offline-only. All18 progressive actors observed.64 full body/58 full header planes from the first run match native rendering; five more speeches and the four captions are verified in the menu run. Six readable QA sheets were directly viewed. No guide photos were collected.

First run: `work/analysis/Rafael_B51_B60_focused_run_20261104/terminal.json`, captures `work/rf51cap`,12161 frames.27 selected utterances/30 ordered pages, all18 actors/three FE notices, source00 and macro behavior, three ASCII-I fixes, Fernan’s normal F and three two-page transitions. Exact ordered modal calls plus complete sequential copied command bytes establish source occurrence; identical pixels alone are insufficient. Body/header first/internal/final glyphs and blank guards match. The FE “...” pause was opened individually at4320: all three native period pixels exist at relative(0,9),(6,9),(12,9); its small appearance is not missing text.

Second run: `work/analysis/Rafael_B60_menu_actual_run_20261104/terminal.json`, captures `work/rf60mcap`,6501 frames. Original question speeches and both complete2100 objects copied byte-exact. Eight full menu samples verify all four captions, centering, guards and background/highlight pixels. DOWN/UP in the first and DOWN in the second visibly move the cursor. A accepts each menu and subsequent source speech calls occur at4728/5687. At5400 the callback still shows second-menu option0 at the scheduled DOWN boundary;5520 shows option1. The failed strict-before5400 sampling assertion was corrected before any analyzer output existed; no ROM/input/renderer change was made. Initial5280 is a normal highlight-off phase, not missing text.

These are disclosed initialized display fixtures: original new-game initialization plus copied complete reviewed commands. They are synthetic QA sequences, not a newly authored story exchange or natural event activation. Original locations, earned chronology, full routes, hardware, economic/condition effects and original menu response branches remain unvisited. The second menu’s final R41 is an exact source-command continuation sentinel, not its original narrative branch result. Live numeric return registers/cancellation were not observed; native bridged0/1/-1 returns and original relative branch sites already pass offline. No need to replay all249 conditional lines individually.

## Next action: registered cumulative successor

No live jobs. Finalizer:`scripts/finalize_rafael_B51_B60_review.py`; formatting checkpoint:`{ready_path}`; current-parent inputs:`{RUNTIME}`. Do not repeat completed prose/native/storage/loaders/actual checks without a changed dependency or concrete failed risk.

Register the249-record mixed SC0 extension through the generic complete-scene framework, preserving all other files/components. Use `dk4tool.script.reviewed_scene_rebuild_v3` (already used for reconstruction) and two typed choices; zero4100 objects need no style extension. Current profile’s recent generic mixed-scene reference is `dk4tool.patch.reviewed_scene_batch_v8` for Hodram B171–B190; existing SC0-qualified source-control/profile behavior must be preserved. Inspect actual registry/module names before opening, and print only selected keys from large JSONs.

Rebase the seven final-stage configurations to the new SC0 whole-ROM identities, retaining each frozen driver/data qualification. Fernan’s ARM9 change must be a separately registered source-owned data stage, never hidden in the component-preserving scene extension. A straightforward successor is an eighth exclusive-field stage after unchanged `scripts/build_integrated_release_with_reviewed_text_data_v3.py`. Qualify/pure-plan before registry mutation; add final manifest/config/inverse checks and update AGENTS/build continuity for the new profile key/driver. Keep Windows build paths short (e.g.work/rf8).

After the registered cumulative build, require its complete manifest, all114 accepted layers/seven preserved stages plus Fernan, exact clean-input patch and whole-ROM reconstruction, and own4001-frame Rafael startup/current RAM/getters before awarding249 completions exactly once. Expected then10774 completed/6356 revisions/4418 retentions, not yet credited. Main promotion still requires user acceptance. Continue useful next Rafael/tutorial source/prose work while the long build runs; avoid idle repeated native investigations. All remaining storylines/shared/town/random/player prose obligations remain intact.
'''
    checkpoint(mutation=ROOT/'research_ready_checkpoint_mutation_v1',
        batch_key='Rafael_SC0_B51_B60_contextual_20261104',
        batch_updates=dict(new_credit=0, final_research_review=str(final_path), final_research_review_sha256=sha(final_path.read_bytes()),
            all_five_individual_gates_pass_in_research=True, scoped_names=str(names_path), scoped_names_sha256=sha(names_path.read_bytes()),
            latest_registered_parent_reconciliation_pending=False, latest_verified_parent=release['candidate'], latest_verified_parent_sha256=release['candidate_sha256'],
            stored_headers_actual_andregistered_integration_pending=False, fresh_formatting_stored_visual_representative_gameplay_andintegration_pending=False,
            stored_headers_representative_gameplay_complete=True, registered_integration_pending=True,
            actual_review=str(actual_path), actual_review_sha256=sha(actual_path.read_bytes()),
            actual_gameplay_records=36, actual_gameplay_speeches=32, actual_gameplay_choice_captions=4,
            actual_body_pages=35, actual_frames=18662, offline_only_speeches=213, scoped_headers_observed=18,
            actual_natural_event_activation=False, full_catalogue_UI_unvisited=True,
            Fernan_exclusive_field_rebased_andactual_progressive_header_verified=True,
            remaining=['Registered mixed SC0 extension andseven-stage config rebase',
                'Separate registered Fernan exclusive-name-field stage', 'Cumulative build/manifest/clean-input patch/own startup',
                'Once-only249-record credit after release verification']),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Rafael_SC0_B51_B60_contextual_20261104', Rafael_early_story_andall_tutorials_first=True,
            current249_five_gate_research_ready=True, registered_cumulative_integration_next=True,
            full_editorial_scope_preserved=True, guide_photos=False)},
        summary=summary, document=document, document_text=text, completed=10525,
        protected={'translations/release_stack.json':release['registry_sha256'], release['candidate']:release['candidate_sha256'],
            release['patch']:release['patch_sha256'], 'out/raphael_natural_v2_accepted_base.nds':release['canonical_sha256']})
    print('Saved249 research-ready reviews andearly-game priority;32 speeches/four captions observed,213 offline-only;10525 integrated completions unchanged. No live jobs.')
