"""Record the verified weekend package and the unintegrated editorial checkpoint."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint
from scripts.write_rafael_B241_B260_contextual_v1 import LABELS, OUT, ROOT


PACKAGE = Path('work/Weekend_testing_package_Rafael3222_20261106/package_verification.json')
RELEASE = Path('work/Rafael3222_extended_release_verified_v1_20261106/registered_release_verification.json')
PRIOR = Path('work/analysis/Weekend_testing_package_Rafael2549_20261106/package_verification.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
PLAN = ROOT / 'ordinary_plans_v3/automatic_plans.json'
DIAGNOSTICS = PLAN.with_name('diagnostics.json')
MENUS = ROOT / 'native_menus_v1/complete_choice_objects.json'
SIGNATURES = ROOT / 'staged_native_v1/compiled_staged.json'
FIELD = ROOT / 'Francisca_name_field_v1/ownership_verification.json'
BATCH = 'Rafael_SC0_B241_B260_clean_20261106'


def digest(path):
    return sha(Path(path).read_bytes())


def main():
    package, release, previous, ledger, review, names, plan, diagnostics, menus, signatures, field = map(
        load, (PACKAGE, RELEASE, PRIOR, LEDGER, OUT, LABELS, PLAN, DIAGNOSTICS, MENUS, SIGNATURES, FIELD)
    )
    assert package['ROM_sha256'] == release['candidate_sha256'] == package['reconstructed_sha256']
    assert package['ZIP_CRCs_and_member_hashes_pass'] and package['experimental_not_promoted']
    assert release['candidate_sha256'] == review['current_ROM_sha256']
    assert release['candidate_sha256'] in str(ledger['current_integrated_candidate'])
    assert (review['source_objects'], review['proposed_revisions'], review['justified_retentions']) == (292, 244, 48)
    assert review['all_individual_four_prose_gates_pass'] and review['all_fifth_formatting_gates_pending']
    assert len(names['records']) == 20 and names['one_scoped_name_field_correction_pending']
    assert len(plan['records']) == 284 and not plan['failures']
    assert all(issue['severity'] == 'info' for issue in diagnostics['issues'])
    assert menus['all_checks_pass'] and menus['physical_caption_records'] == 6
    assert signatures['complete_native_glyphs_pages_bounds_and_canaries_pass'] and len(signatures['records']) == 2
    assert field['complete_parent_inverse_exact'] and field['fields'][0]['actor'] == 186
    assert all(digest(path) == expected for path, expected in review['evidence'].items())

    summary = (
        f"The {link('Rafael3222 weekend ZIP', package['zip'])} contains the registered four-route ROM, "
        "the shared tutorial updates, exact clean-input patch, manifest and Rafael-first testing notes. "
        "It adds 673 reviewed records since Rafael2549 and brings integrated coverage to 15,067. "
        "All 292 B241–B260 contextual decisions are saved, with 244 proposed revisions and 48 justified retentions. "
        "Those changes remain outside the package."
    )
    document = f"""# Rafael3222 weekend package and B241–B260 checkpoint

{summary}

Package verification confirmed the original 690-entry manifest, all 114 accepted layers, eight registered final stages including the ASCII right-bound fix, 26 passing release checks, exact hashes for all ZIP members, English menu anchors and byte-for-byte clean-input reconstruction. Compared with the canonical base, the manifest identifies 53 changed internal paths. The exact ROM previously cold-booted in an emulator through Rafael's opening. Initialized fixtures for B201–B240 displayed 268 pages across selected scenes. The remaining branches and physical hardware have no new gameplay coverage. {link('Registered release verification', RELEASE)}. {link('Package verification', PACKAGE)}.

B241–B260 now has all four prose gates across 272 ordinary or FE speeches, 14 voice alternatives and six captions. B244 is control-only and B246 supplies 18 previously credited records for context. The review preserves the uncertainty around the Frozen Rose, restores specific geographic references, corrects Jam Jack Ludwyan's signature and fixes the full-width I in Hatra's greeting while retaining the runtime name token. The 20-name ledger retains 19 names or roles and proposes normalizing the initial F in Francisca in both consumers. The fixed-slot ownership and complete inverse passed for the proposal. {link('Contextual manuscript', OUT)}. {link('Name and role ledger', LABELS)}. {link('Field ownership receipt', FIELD)}.

The latest ordinary plan has 284 bodies with zero warnings or errors. The six binary-choice captions and both staged signature panels passed offline native rendering and direct visual review. Ordinary body and style-object native checks, readable page reviews, the Francisca getter/render check, stored-script checks, focused gameplay and registered integration are next. {link('Ordinary plans', PLAN)}. {link('Native menus', MENUS)}. {link('Staged signatures', SIGNATURES)}.
"""
    evidence = {**ledger[BATCH]['evidence'], **review['evidence']}
    evidence.update({str(path): digest(path) for path in (
        OUT, LABELS, PLAN, DIAGNOSTICS, MENUS, SIGNATURES, FIELD, PACKAGE, Path(__file__),
    )})
    checkpoint(
        mutation=PACKAGE.parent / 'editorial_checkpoint',
        batch_key=BATCH,
        batch_updates=dict(
            new_credit=0, source_only=False, independently_drafted_records=292,
            remaining_clean_meanings_anddrafts=0, current_binding_records=292,
            current_comparisons=292, contextual_comparison_records=292, remaining_current_comparisons=0,
            four_prose_gates_pass=292, proposed_revisions=244, justified_retentions=48,
            scoped_name_and_role_retentions=19, scoped_name_glyph_corrections_pending=1,
            native_style_slots=16, ordinary_planned_bodies=284, binary_captions_native_andviewed=6,
            staged_signatures_native_andviewed=2, glyph_defect_records=review['current_glyph_defect_records'],
            punctuation_consistency_revisions=review['punctuation_consistency_revisions'],
            fifth_formatting_gate_pending=True, stored_checks_pending=True, focused_gameplay_pending=True,
            registered_integration_pending=True, full_intake_not_complete=True,
            contextual_manuscript=str(OUT), contextual_manuscript_sha256=digest(OUT),
            scoped_names_review=str(LABELS), scoped_names_review_sha256=digest(LABELS), evidence=evidence,
        ),
        additional_updates={'editorial_execution_priority_20261104': dict(
            new_credit=0, current_batch='Rafael B241–B260 native formatting and validation.',
            next_action='Verify v3 ordinary pages, style objects and Francisca name rendering. '
                        'Continue with stored-script checks and focused gameplay.',
            current_batch_not_yet_integrated=True, all_current_batch_fifth_gates_pending=True,
            native_job_live=False, registered_build_live=False, guide_photos=False,
        )},
        new_entries={'weekend_testing_package_Rafael3222_20261106': dict(
            new_credit=0, package=package['zip'], package_sha256=package['zip_sha256'],
            verification=str(PACKAGE), verification_sha256=digest(PACKAGE),
            candidate=release['candidate'], candidate_sha256=release['candidate_sha256'],
            previous_package=previous['zip'], additional_reviewed_records_since_previous_package=673,
            main_unchanged=True,
        )},
        summary=summary, document='docs/editorial_Rafael3222_weekend_checkpoint_20261106.md',
        document_text=document, completed=15067, protected={
            'translations/release_stack.json': release['registry_sha256'],
            release['canonical_base']: release['canonical_sha256'],
            release['candidate']: release['candidate_sha256'],
            release['patch']: release['patch_sha256'],
            package['zip']: package['zip_sha256'],
            previous['zip']: previous['zip_sha256'],
        },
    )
    print('Recorded Rafael3222 weekend ZIP and all 292 uncredited B241–B260 contextual decisions.')


if __name__ == '__main__':
    main()
