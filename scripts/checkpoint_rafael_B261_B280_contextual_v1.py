"""Save the reviewed Rafael manuscript without assigning release credit."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import LEDGER, PACKAGE
from scripts.save_rafael3514_registered_checkpoint_v1 import NEXT
from scripts.verify_rafael3514_registered_release_v1 import RELEASE, digest
from scripts.write_rafael_B261_B280_contextual_v1 import INPUTS, LABELS, OUT, ROOT


def main():
    review, names, ledger, release, package = map(load, (OUT, LABELS, LEDGER, RELEASE, PACKAGE))
    assert all(digest(path) == checksum for path, checksum in review['evidence'].items())
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256'] == review['current_ROM_sha256']
    assert review['all_individual_four_prose_gates_pass'] and review['all_fifth_formatting_gates_pending']
    assert names['all_name_formatting_gates_pending'] and names['scoped_name_field_corrections_pending'] == [65, 68]
    assert (review['proposed_revisions'], review['justified_retentions'], len(names['records'])) == (118, 17, 18)
    assert names['new_credit'] == review['new_credit'] == 0
    summary = (
        'Rafael B261–B280 has 135 contextual decisions against Rafael3514, with 118 revisions and 17 justified retentions. '
        'The scoped name review covers 18 actors and proposes two surname corrections. Native formatting, focused scene tests and '
        'registration remain pending. Integrated coverage is 15,359.'
    )
    doc = f"""# Rafael B261–B280 contextual checkpoint

{summary}

The ledger binds 114 speeches and system panels, 16 physical crew voices across both cave-in branches, and five captions across two puzzle menus. Three Jacob capture records still contained Japanese in Rafael3514. The revised dialogue keeps the follower's familiar address and lets his use of Jacob's name set up the threat. The ice puzzle gives the player its full premise and states which stone corresponds to each answer. The town exchanges retain all three FI substitutions, and the four reward sequences preserve their gold amounts and share changes. {link('Contextual review ledger', OUT)}.

The scoped review keeps distinct dialogue and catalogue role labels where the source distinguishes them. It selects Jacob Portunto and Plett Perrault to match the established quest and bounty spellings. Both surname fields need an ownership and capacity check before any edit, followed by native getter and nameplate checks. {link('Scoped name review', LABELS)}.

Use the verified Rafael3514 runtime and carry forward its nine final stages, including the ASCII right-bound and Francisca corrections. Format all 130 speech and style records with their validated consumers, including the 17 FE panels. Check both menus, all new pages, stored controls, branch targets and bounds. Use focused emulator tests for the two menus and cave-in transitions and sample the reward and town substitutions. This checkpoint binds original getters but adds no gameplay or hardware coverage. The registered Rafael3514 candidate and Rafael3222 weekend package remain available. {link('Registered predecessor verification', RELEASE)}.
"""
    evidence = {**ledger[NEXT]['evidence'], **review['evidence'],
                str(OUT): digest(OUT), str(Path(__file__).resolve().relative_to(Path.cwd())): digest(__file__)}
    checkpoint(
        mutation=ROOT/'B261_B280_contextual_checkpoint_v1', batch_key=NEXT,
        batch_updates=dict(
            new_credit=0, independently_drafted_records=135, independent_draft_blocks=review['blocks'],
            remaining_clean_meanings_anddrafts=0, remaining_current_comparisons=0,
            clean_drafts=str(INPUTS[0]), clean_drafts_sha256=digest(INPUTS[0]),
            contextual_review=str(OUT), contextual_review_sha256=digest(OUT),
            proposed_revisions=118, justified_retentions=17, source_context_localization_and_naturalness_pass=True,
            formatting_pending=True, representative_gameplay_pending=True,
            registered_integration_pending=True, evidence=evidence,
        ),
        additional_updates={'editorial_execution_priority_20261104': dict(
            new_credit=0, current_batch='Rafael B261–B280 native display validation.',
            next_action='Format both menus, progressive and FE panels, and qualify the two surname fields.',
            native_job_live=False, registered_build_live=False, guide_photos=False,
        )},
        summary=summary, document='docs/editorial_Rafael_B261_B280_contextual_20261106.md',
        document_text=doc, completed=15359,
        protected={
            'translations/release_stack.json': release['registry_sha256'],
            release['canonical_base']: release['canonical_sha256'],
            release['candidate']: release['candidate_sha256'],
            release['patch']: release['patch_sha256'],
            package['zip']: package['zip_sha256'],
        },
    )
    print('Saved 135 contextual decisions. Integrated coverage remains 15,359.')


if __name__ == '__main__':
    main()
