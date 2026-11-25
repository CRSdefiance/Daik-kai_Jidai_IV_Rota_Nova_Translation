"""Record the verified Rafael2549 package and preserve the next dialogue checkpoint."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint


ANALYSIS = Path('work/analysis')
RELEASE = ANALYSIS / 'Rafael2549_extended_release_verified_v1_20261106/registered_release_verification.json'
PACKAGE = ANALYSIS / 'Weekend_testing_package_Rafael2549_20261106/package_verification.json'
PRIOR = ANALYSIS / 'Weekend_testing_package_Rafael2165_20261105/package_verification.json'
CONTEXT = Path('translations/rafael_B201_B220_contextual_review_v1.json')
NAMES = Path('translations/rafael_B201_B220_scoped_names_review_v1.json')
DRAFTS = ANALYSIS / 'Rafael_B201_B220_clean_20261106/sealed_all_clean_first_v1/sealed_drafts.json'
CREDIT = RELEASE.with_name('completion_checkpoint.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
REGISTRY = Path('translations/release_stack.json')
BATCH = 'Rafael_SC0_B201_B220_clean_20261106'


def digest(path):
    return sha(Path(path).read_bytes())


def main():
    release, package, prior, review, names, credit, ledger = map(
        load, (RELEASE, PACKAGE, PRIOR, CONTEXT, NAMES, CREDIT, LEDGER)
    )
    assert credit['counts'] == dict(completed=14394, revised=8407, retained=5987)
    assert (release['new_contextual_records'], release['prose_revisions'], release['justified_retentions']) == (384, 317, 67)
    assert package['ROM_sha256'] == release['candidate_sha256'] == package['reconstructed_sha256']
    assert package['ZIP_CRCs_and_member_hashes_pass'] and package['experimental_not_promoted']
    assert prior['ROM_sha256'] == release['parent_sha256']
    assert (release['observed_actual_body_pages'], release['offline_only_source_speeches']) == (148, 236)
    assert review['current_ROM_sha256'] == release['candidate_sha256']
    assert (review['source_objects'], review['proposed_revisions'], review['justified_retentions']) == (403, 299, 104)
    assert (review['typed_choice_objects'], review['typed_choice_commands']) == (21, 10)
    assert review['all_individual_four_prose_gates_pass'] and review['all_fifth_formatting_gates_pending']
    assert len(review['current_glyph_defect_records']) == 3
    assert len(names['records']) == 41 and names['all_name_formatting_gates_pending']
    assert review['evidence'][str(DRAFTS)] == digest(DRAFTS)
    assert review['evidence'][str(NAMES)] == digest(NAMES)
    assert release['candidate_sha256'] in str(ledger['current_integrated_candidate'])

    summary = (
        f"The {link('Rafael2549 weekend ZIP', package['zip'])} contains the registered four-route ROM "
        f"and its exact clean-input patch, manifest and Rafael-first testing notes. It adds 384 reviewed records "
        "since Rafael2165. The ZIP, patch reconstruction and baseline checks passed. "
        "All 403 B201–B220 drafts and contextual decisions are now saved, with 299 proposed revisions and 104 justified retentions. "
        "Fresh display and integration checks remain for that batch. Integrated total is 14,394."
    )
    doc = f"""# Rafael2549 weekend test package and B201–B220 checkpoint

{summary}

The build includes the shared tutorials and all 114 accepted layers. The original manifest identifies 688 stack entries, 53 changed internal files against the canonical base and eight registered final stages including the ASCII right-bound repair. All 26 release checks passed. The exact candidate cold-booted in an emulator through Rafael's opening. Focused initialized B181–B200 fixtures displayed 148 pages, with 236 speeches checked offline. Physical hardware, complete routes and original conditional activation remain open. {link('Registered release verification', RELEASE)}. {link('Package verification', PACKAGE)}.

The next batch has 382 speeches and 21 captions in ten menus. The prose ledger records all four contextual gates and three mixed-width glyph defects, including the full-width I in Istanbul and the damaged stammer. The 41 scoped public names and role labels have contextual retentions. Continue with source-qualified formatting, the staged letter presentation, all caption consumers, stored checks and representative emulator tests before registering the batch. {link('Contextual decisions', CONTEXT)}. {link('Name and role review', NAMES)}.

The designated main and earlier ZIPs are preserved. Keep Rafael and tutorial priority, deferred artwork and the later older-record technical re-audit.
"""
    evidence = dict(ledger[BATCH]['evidence'])
    evidence.update({str(path): digest(path) for path in (RELEASE, CONTEXT, NAMES, DRAFTS, Path(__file__))})
    checkpoint(
        mutation=PACKAGE.parent / 'editorial_checkpoint',
        batch_key=BATCH,
        batch_updates=dict(
            new_credit=0, source_only=False, independently_drafted_records=403,
            independent_draft_blocks=list(range(201, 221)), remaining_clean_meanings_anddrafts=0,
            current_comparisons=403, contextual_comparison_records=403, current_binding_records=403,
            remaining_current_comparisons=0, proposed_revisions=299, justified_retentions=104,
            scoped_public_names=41, current_glyph_defect_records=review['current_glyph_defect_records'],
            all_four_prose_gates_pass=True, fifth_formatting_gate_pending=True, stored_checks_pending=True,
            focused_gameplay_pending=True, registered_integration_pending=True, full_intake_not_complete=True,
            current_review=str(CONTEXT), current_review_sha256=digest(CONTEXT),
            names_review=str(NAMES), names_review_sha256=digest(NAMES), evidence=evidence,
        ),
        additional_updates={'editorial_execution_priority_20261104': dict(
            new_credit=0, current_batch='Rafael B201–B220 contextual dialogue and choice captions.',
            next_action='Format speech and captions, qualify the staged FE letter signature, and verify native display.',
            current_batch_not_yet_integrated=True, native_job_live=False, registered_build_live=False, guide_photos=False,
        )},
        new_entries={'weekend_testing_package_Rafael2549_20261106': dict(
            new_credit=0, package=package['zip'], package_sha256=package['zip_sha256'],
            verification=str(PACKAGE), verification_sha256=digest(PACKAGE),
            candidate=release['candidate'], candidate_sha256=release['candidate_sha256'],
            previous_package=prior['zip'], additional_reviewed_records_since_previous_package=384,
            main_unchanged=True,
        )},
        summary=summary, document='docs/editorial_Rafael2549_weekend_checkpoint_20261106.md',
        document_text=doc, completed=14394, protected={
            str(REGISTRY): release['registry_sha256'], release['canonical_base']: release['canonical_sha256'],
            release['candidate']: release['candidate_sha256'], release['patch']: release['patch_sha256'],
            package['zip']: package['zip_sha256'], prior['zip']: prior['zip_sha256'],
        },
    )
    print('Recorded Rafael2549 weekend ZIP and all 403 uncredited B201–B220 contextual decisions.')


if __name__ == '__main__':
    main()

