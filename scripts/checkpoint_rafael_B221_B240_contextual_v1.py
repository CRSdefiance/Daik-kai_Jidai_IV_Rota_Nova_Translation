"""Checkpoint the four completed prose gates for Rafael B221–B240."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint
from scripts.write_rafael_B221_B240_contextual_v1 import OUT, LABELS, digest

REGISTRY = Path('translations/release_stack.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
RELEASE = Path('work/analysis/Rafael2952_extended_release_verified_v1_20261106/registered_release_verification.json')
PACKAGE = Path('work/analysis/Weekend_testing_package_Rafael2549_20261106/package_verification.json')
KEY = 'Rafael_SC0_B221_B240_clean_20261106'
MUTATION = Path('work/analysis/Rafael_B221_B240_clean_20261106/contextual_checkpoint_v1')


def main():
    review, labels, release, package, ledger = map(load, (OUT, LABELS, RELEASE, PACKAGE, LEDGER))
    assert review['current_ROM_sha256'] == release['candidate_sha256']
    assert review['all_individual_four_prose_gates_pass'] and review['all_fifth_formatting_gates_pending']
    assert (review['proposed_revisions'], review['justified_retentions'], len(labels['records'])) == (221, 49, 26)
    assert all(digest(Path(path)) == expected for path, expected in review['evidence'].items())
    summary = (
        'Rafael B221–B240 now has 270 complete contextual comparisons, with 221 revisions and 49 justified retentions. '
        'The scoped name ledger retains 26 public names and roles. Fresh formatting, stored checks, focused gameplay '
        'and registration remain pending. Rafael2952 remains the registered cumulative candidate at 14,797 credited '
        'records. Rafael2549 remains the packaged weekend build.'
    )
    document = f"""# Rafael B221–B240 contextual checkpoint

{summary}

The changes restore the missing Guan Yu response, clarify the Three Kingdoms and book-familiarity choices, and preserve who reports, believes or doubts each legend. The catalogue titles Holy Spear of Ares, Armadillo Hide, Empress Gown and Medusa Shield match the dialogue. The comparison identifies two fullwidth I characters in the Solomon exchange and a separate fullwidth question mark in B225. The two deliberate source ellipses stay. See the {link('contextual manuscript and exact references', OUT)} and {link('scoped names and role ledger', LABELS)}.

The manuscript covers 234 ordinary or FE bodies, 29 voice alternatives in four native commands and seven captions across two binary choices and one three-option menu. B231 has only controls. Exact source and current record references, alias slots and command data are bound. The Rafael startup proof resolves selector 208 to actor 151 at voice class 4. Its result does not establish event reachability or every conditional speaker. No gameplay coverage was added in this pass.

Apply fresh native formatting to the revised and retained text. Keep the three signed progressive letters separate from the FE swan effects, exercise the voice alias slots and menu boundaries, and verify the six preserved runtime substitutions. Review every resulting page, then use focused gameplay for the distinct display consumers. Carry forward the registered ASCII right-bound correction and B146 percent-relocation proof. Guide photography is outside this work. {link('Current release verification', RELEASE)}. {link('Weekend testing package', package['zip'])}.
"""
    evidence = {**ledger[KEY]['evidence'], **review['evidence'],
                **{str(path): digest(path) for path in (OUT, LABELS, Path(__file__))}}
    checkpoint(
        mutation=MUTATION, batch_key=KEY,
        batch_updates=dict(new_credit=0, source_only=False, independently_drafted_records=270,
            independent_draft_blocks=list(range(221, 241)), remaining_clean_meanings_anddrafts=0,
            current_binding_records=270, current_comparisons=270, contextual_comparison_records=270,
            remaining_current_comparisons=0, four_prose_gates_pass=270, proposed_revisions=221,
            justified_retentions=49, scoped_name_and_role_retentions=26, native_style_slots=32,
            current_untranslated_records=review['untranslated_current_records'],
            glyph_defect_records=review['current_glyph_defect_records'],
            punctuation_consistency_revisions=review['punctuation_consistency_revisions'],
            fifth_formatting_gate_pending=True, stored_checks_pending=True, focused_gameplay_pending=True,
            registered_integration_pending=True, full_intake_not_complete=True, contextual_manuscript=str(OUT),
            contextual_manuscript_sha256=digest(OUT), scoped_names_review=str(LABELS),
            scoped_names_review_sha256=digest(LABELS), evidence=evidence),
        additional_updates={'editorial_execution_priority_20261104': dict(new_credit=0,
            current_batch='Rafael B221–B240 fresh native formatting and focused validation.',
            next_action='Format B221–B240 including three signed progressive letters, the staged swan call, '
                        'four native voice commands and three menus. Inspect all resulting pages and test distinct consumers.',
            current_batch_not_yet_integrated=True, current270_four_prose_gates_pass=True,
            all_current_batch_fifth_gates_pending=True, native_job_live=False, registered_build_live=False,
            guide_photos=False)},
        summary=summary, document='docs/editorial_Rafael_B221_B240_contextual_20261106.md',
        document_text=document, completed=14797, protected={str(REGISTRY): release['registry_sha256'],
            release['canonical_base']: release['canonical_sha256'], release['candidate']: release['candidate_sha256'],
            release['patch']: release['patch_sha256'], package['zip']: package['zip_sha256']},
    )
    print('Saved the exact 270-record Rafael contextual checkpoint with zero new registered credit.')


if __name__ == '__main__':
    main()

