"""Save completed research gates without prematurely crediting unregistered releases."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint


def main():
    root = Path('work/analysis/Rafael351_final_metadata_v2_20261105')
    complete = load(root / 'research_completion.json')
    metadata = load(root / 'qualification.json')
    combined = load(root / 'cumulative_reconstruction.json')
    canonical = Path('work/analysis/Rafael516_canonical_contract_v2_20261105/qualification.json')
    assert canonical.exists()
    assert complete['all_individual_five_gates_pass'] and complete['records'] == 351
    assert metadata['all_ROMs_andoriginal_proofs_unchanged']
    doc = load(complete['manuscript'])
    assert len(doc['records']) == 351 and all(all(r['review'].values()) for r in doc['records'])
    assert (complete['revisions'], complete['retentions'], complete['actual_pages']) == (201, 150, 134)
    prior_plan = load('work/analysis/Rafael351_prose_body_checkpoint_20261105/mutation_plan.json')
    protected = prior_plan['protected']
    summary = (
        "Rafael early story and all tutorials remain first. B121–B140 now has 351 complete-exchange reviews "
        "with all five research gates passing: 201 revisions and 150 justified retentions. All 344 native body pages, "
        "10 captions and 22 scoped public names are checked and visually reviewed; stored allocation, catalogue, "
        "style dispatch and loaders pass. Two disclosed cold-boot emulator fixtures observed 132 speech variants/134 pages "
        "and five menus at default cursor 0; 209 speech variants remain offline-only. No natural conditional activation "
        "or hardware playthrough is claimed. The 867-record combined research target is 3bf32397, with 47 disjoint "
        "changed blocks and three exact serialized inverses. It remains unregistered and unpromoted. The separator-only "
        "canonical contract successor is qualified against the completed 672-entry stage; registered continuation, "
        "clean-input patch, final startup checks and two catalogue de corrections remain pending. Integrated totals "
        "stay 11845; verified cc71/main 3cb8, all ROMs and full scope are preserved. No guide photos."
    )
    text = '''# Rafael351 research-ready checkpoint — November 5, 2026

Rafael's early story and all tutorials remain the first priority. Keep every other storyline, unfinished earlier contextual pass, shared town/shop exchange, random scene, speaker label, wrap/glyph defect and remaining player-facing prose in scope. Preserve all translations, ROMs, evidence and completed coverage. No guide-photo collection or main promotion.

## Editorial and display results

`translations/rafael_B121_B140_contextual_final_review_v2.json` contains 351 complete-exchange reviews from clean Japanese, exact source/current and proposed stored references, individual findings and all five passing research gates: **201 revisions and 150 justified retentions**. `translations/rafael_B121_B140_scoped_names_final_v2.json` preserves the 22 scoped public-name decisions and five gates. This is research readiness, not registered integration credit.

The earlier source and prose work is reused. Current item/menu labels, relationships, uncertainty and distinct character voices stay bound to the reviewed evidence. Five full-width I occurrences are corrected to ASCII I. Paragraphs use the validated consumer width; scoped phrase/page refinements and the B128R89 FE planning guard preserve the prose and native geometry. One short realization beat has a documented source/emotional reason. See the preceding prose/body checkpoint for those individual decisions rather than repeating the review.

The final automatic/native plans cover 341 speech variants and 344 pages. All 344 pages were directly viewed. Style dispatch checks cover six complete eight-slot objects/34 physical alternatives, 48 slot cases and 54 semantic negative cases. Five two-choice objects/10 captions pass complete provider, modal-return, centering and plane checks. All 22 public name planes pass, using exact compatible getter/font proofs where available.

Stored verification checks every byte, leading/internal/trailing glyphs, bounds, canaries, controls, substitution behavior, complete pages and allocations. It checks 147 fresh page parities and reuses 197 exact compatible page results. All 341 stored bodies pass full-catalogue pre-macro lookup. Loader checks cover 343 archive loads/cache hits and 686 handoffs: 36 fresh changed-block cases and 650 exact compatible cases. These numbers describe checks, not additional editorial coverage.

Evidence:

- `work/analysis/Rafael351_native_final_v3_20261105/compiled_native_pages.json`
- `work/analysis/Rafael351_body_visual_review_v1_20261105/body_visual_review.json`
- `work/analysis/Rafael351_style_objects_v1_20261105/compiled_style_objects.json`
- `work/analysis/Rafael351_choice_objects_v2_20261105/complete_choice_objects.json`
- `work/analysis/Rafael351_name_planes_v1_20261105/native_name_planes.json`
- `work/analysis/Rafael351_stored_native_v1_20261105/stored_native_verification.json`
- `work/analysis/Rafael351_stored_catalogue_v1_20261105/all_stored_effective_body_bindings.json`
- `work/analysis/Rafael351_loaders_v1_20261105/verification.json`

## Observed gameplay and limits

Two fresh cold-boot, initialized QA fixtures ran for **43,282 frames**. They copied complete reviewed commands into disclosed flat test sequences with ordinary New Game initialization. They observed **132 source speech variants and 134 pages**, including all six complete style commands under unchanged default roles, the repaired FE case and two multipage transitions. Four corrected I occurrences were observed; B128R189 remains offline-only. All complete native body/header pixel comparisons pass. Twelve readable dialogue sheets, two full-scene sheets and two menu sheets were directly viewed.

All five menus appeared with both captions visible and **default selected option 0**. Other cursor states, numeric return values, source branches and cancellation remain offline checks. Public headers match nine labels: Arcadius Eudoxios, Boy, Claudio Manaus, Janus Pasar, Julian Lopes, Julio Erneco, Mysterious Old Man, Rafael Castor and Sailor. Actor IDs come from offline bindings, not inference from pixels. Fallback role 151/Sailor in these fixtures does not establish original conditional participation.

**209 speech variants**, including 28 other physical style alternatives, were not activated in gameplay. Original locations, earned chronology, conditional event participation, recruitment/sailing/quest states, full routes and hardware operation were not tested by these fixtures. The initialized harbor background remains visible. No guide photos were collected.

See `work/analysis/Rafael351_checked_v1_20261105/actual_review.json`, both `Rafael351_*_actual_pixels_v1_20261105/focused_actual_pixels.json`, both menu pixel reports and both compact-sheet receipts. `work/analysis/Rafael351_final_metadata_v2_20261105/research_completion.json` retains their exact hashes. Its `qualification.json` clears 159 superseded intake flags and the obsolete name-formatting hold using existing sealed proofs; prose, findings, source/current references, controls, five gates and every ROM byte remain unchanged. The original metadata and failures are preserved.

## Combined research and registered continuation

`work/analysis/Rafael867_combined_research_v1_20261105/combined_RESEARCH_ONLY.nds` combines the prior 516 reviews and these 351: **867 = 447 revisions + 420 retentions**. SHA-256: **3bf3239736982e6398eda1f837f4c249b93e541128985013fbde02466bcbaa9c**. SC0 archive SHA-256: **66a86822e35c2a7a34132ee0c8ccf20198909bfed9c3d747e2f8d3f63d0938e7**. The 29 prior and 18 new changed blocks are disjoint. All 20 new local source/target blocks match their checked inputs. Three complete serialized inverses restore each parent and verified678. ARM9, COMMON, font, all accepted runtime/name layers, every unowned file and other components are exact.

This is an **unregistered research target**, not a candidate or new main. Metadata-only v2 references are `translations/rafael_B121_B140_cumulative867_refs_v2.json` and `work/analysis/Rafael351_final_metadata_v2_20261105/cumulative_reconstruction.json`. They point to the same existing ROM and do not rerender or claim fresh gameplay. The combined set has 839 speech variants/848 pages and 28 captions. Prior and new fixtures together observed 250 source variants/255 pages; 589 variants remain offline-only.

The old 516 build is terminal exit 1; do not poll or restart it. Its canonical ROM and 672-entry manifest pass every original canonical check. Failure was only entry670's path separator in the frozen expected list. `scripts/prepare_rafael516_registered_successor_v2.py` uses the original preparer's `Path` spelling. `work/analysis/Rafael516_canonical_contract_v2_20261105/qualification.json` qualifies a versioned successor contract against the actual completed canonical manifest, retaining the original contract, drivers, registry and canonical ROM. This is not final-stage execution or registration.

Next, implement a narrowly guarded registered continuation that reuses the completed canonical checkpoint, appends the new 351 owned-block transaction and runs all required original runtime/name/data stages and inverse checks. Preserve the registered ASCII right-bound correction and all 114 accepted layers. Require a final verified manifest, exactly reconstructable clean-input patch, own captain0/route0 startup and both Fernan getters before once-only integration credit. Do not blindly repeat the 102-minute reconstruction or weaken the manifest checks.

Two full-catalogue particles remain: **Dinis デ Albuquerque → Dinis de Albuquerque** and **Garcia デ Oviedo → Garcia de Oviedo**. Qualify their exclusive pointer fields through an appropriate registered data owner. Do not put them in the actor35-only Fernan stage. Public progressive headers are already correct; global 207-name/full-catalogue UI review remains open. Deferred graphics artwork and the later older-record technical re-audit remain separate.

Integrated totals remain **11845 = 6836 revisions + 5009 retentions**; historical source/prose11848 is unchanged. No research-only coverage is credited. Verified experimental678/cc71ec06 and main3cb827e4 remain unchanged. Full goal active.
'''
    references = [root / 'research_completion.json', root / 'qualification.json', root / 'cumulative_reconstruction.json', canonical]
    checkpoint(
        mutation='work/analysis/Rafael351_research_ready_checkpoint_20261105',
        batch_key='Rafael_SC0_B121_B140_clean_20261105',
        batch_updates=dict(new_credit=0, manuscript=complete['manuscript'], manuscript_sha256=complete['manuscript_sha256'],
            all_current_comparisons_name_term_controls_andfive_gates_pending=False,
            remaining_comparisons_UI_holds_andall_fifth_gates_pending=False, all_fifth_formatting_gates_pending=False,
            remaining_name_item_UI_holds_particle_fixes_andall_fifth_gates_pending=False,
            remaining_caption_name_particle_stored_gameplay_andintegration_work_pending=False,
            all351_individual_five_research_gates_pass=True, registered_integration_pending=True,
            scoped_names=doc['scoped_name_review'], scoped_names_sha256=doc['scoped_name_review_sha256'],
            two_full_catalogue_particle_fixes_still_pending=True, native_body_pages=344,
            actual_source_variants=132, actual_pages=134, offline_only_source_variants=209,
            actual_menu_cursor_states=[0], other_menu_states_returns_andbranches_offline_only=True,
            research_completion=str(root / 'research_completion.json'),
            research_completion_sha256=sha((root / 'research_completion.json').read_bytes()),
            evidence={str(p): sha(p.read_bytes()) for p in references}),
        additional_updates={
            'Rafael516_registered_cumulative_20261105': dict(new_credit=0, current_build_live=False,
                versioned_canonical_contract_qualification=str(canonical),
                versioned_canonical_contract_qualification_sha256=sha(canonical.read_bytes()),
                registered_continuation_needed=True, final_candidate_not_emitted=True),
            'editorial_execution_priority_20261104': dict(new_credit=0, current_batch='Rafael867 qualified cumulative research; registered continuation next',
                current351_all_five_research_gates_pass=True, current351_actual_source_variants=132,
                registered_build_live=False, current_batch_not_yet_integrated=True,
                next_action='Guarded versioned registered continuation from completed canonical stage, preserving original runtime/name/data checks; catalogue particles remain separate pending owner.',
                source_prose_anddisplay_checks_reused=True, guide_photos=False)},
        new_entries={'Rafael867_qualified_cumulative_research_20261105': dict(new_credit=0,
            records=867, proposed_revisions=447, justified_retentions=420, research_ROM=combined['research_ROM'],
            research_ROM_sha256=combined['research_ROM_sha256'], reconstruction=str(root / 'cumulative_reconstruction.json'),
            reconstruction_sha256=sha((root / 'cumulative_reconstruction.json').read_bytes()),
            changed_blocks=47, exact_serialized_inverses=3, not_registered_or_promoted=True,
            registered_integration_andclean_input_patch_pending=True, full_goal_complete=False)},
        summary=summary, document='docs/editorial_Rafael351_research_ready_20261105.md',
        document_text=text, completed=11845, protected=protected)
    print('Saved five-gate research checkpoint and867 combined target; integrated11845/main/registry preserved. Goal active.')


if __name__ == '__main__':
    main()
