"""Save the exact five-gate research and the next clean-source intake before credit."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint


A = Path('work/analysis')
ROOT = A / 'Rafael_B170_B176_research_final_v1_20261105'
RESEARCH = ROOT / 'research_completion.json'
INTAKE = A / 'Rafael_B181_B200_clean_20261105'
CENSUS = INTAKE / 'clean_source_census_v1.json'
DRAFTS = [INTAKE / (name + '_clean_drafts_v1.json') for name in ('B181_B182', 'B183', 'B184_B185')]
PARENT = A / 'Rafael1975_extended_release_verified_v1_20261105/registered_release_verification.json'
PACKAGE = A / 'Weekend_testing_package_Rafael1860_20261105/package_verification.json'
REGISTRY = Path('translations/release_stack.json')
KEY = 'Rafael_SC0_B170_B176_research_20261105'
NEXT = 'Rafael_SC0_B181_B200_clean_20261105'


def digest(path):
    return sha(Path(path).read_bytes())


def main():
    review, census, release, package = map(load, (RESEARCH, CENSUS, PARENT, PACKAGE))
    assert review['all_individual_five_gates_pass']
    assert (review['records'], review['revisions'], review['retentions'], review['body_pages']) == (190, 152, 38, 190)
    assert (review['actual_source_variants'], review['actual_pages'], review['offline_only_source_variants']) == (72, 72, 118)
    assert review['scoped_public_names'] == 13
    assert census['clean_speeches'] == 384 and census['zero_already_credited_keys']
    assert census['complete_blocks'] == list(range(181, 201)) and census['source_only_no_current_English_extracted']
    for path, count in zip(DRAFTS, (58, 37, 43), strict=True):
        draft = load(path)
        assert draft['records_count'] == count and draft['all_five_gates_pending']
    assert digest(package['zip']) == package['zip_sha256']
    evidence = {str(p): digest(p) for p in (RESEARCH, CENSUS, *DRAFTS, PARENT, PACKAGE, Path(__file__))}
    summary = ('Rafael B170–B176 has 190 five-gate reviews, with 152 revisions and 38 justified retentions. '
               'An initialized emulator sequence showed 72 speeches and 13 nameplates. The remaining 118 speeches passed offline checks. '
               'Registered integration is pending. The B181–B200 intake has 384 source records and 138 clean drafts. Integrated credit remains 13,820.')
    doc = f"""# Rafael B170–B176 reviewed and ready for integration

{summary} The initialized sequence also covered the six modal pages and both FI substitutions. Natural conditional activation, the full route and physical hardware remain open. {link('Five-gate review and evidence', RESEARCH)}.

The B181–B200 intake has 138 independent drafts across B181–B185. Continue the other 246 clean drafts, then the 384 contextual comparisons. {link('Clean intake census', CENSUS)}.

The designated main and all earlier candidates and weekend packages are preserved.
"""
    checkpoint(
        mutation=ROOT / 'research_documentation_checkpoint',
        batch_key='Rafael_SC0_B161_B180_clean_20261105',
        batch_updates=dict(new_credit=0, independently_drafted_records=741,
            current_comparisons=741, contextual_comparison_records=741, remaining_current_comparisons=0,
            integrated_subbatch_credit=551, full_intake_not_complete=True, latest_research_subset=KEY,
            next_clean_intake=NEXT, B170_B176_research=str(RESEARCH)),
        additional_updates={'editorial_execution_priority_20261104': dict(new_credit=0,
            current_batch='Registered Rafael2165 release and weekend testing package.',
            next_action='Finish registered verification and package Rafael2165. Continue B181–B200 clean-source drafts.',
            current_batch_not_yet_integrated=True, native_job_live=False, guide_photos=False)},
        new_entries={
            KEY: dict(new_credit=0, records=190, blocks=list(range(170, 177)), proposed_revisions=152,
                justified_retentions=38, all_individual_five_research_gates_pass=True, observed_speeches=72,
                observed_pages=72, offline_only_speeches=118, observed_headers=13, registered_integration_pending=True,
                focused_gameplay_pending=False, current_review=review['manuscript'],
                current_review_sha256=review['manuscript_sha256'], evidence=evidence),
            NEXT: dict(new_credit=0, source_records=384, independently_drafted_records=138,
                independent_draft_blocks=list(range(181, 186)), remaining_clean_meanings_anddrafts=246,
                remaining_current_comparisons=384, current_comparisons=0, full_intake_not_complete=True,
                source_only=True, evidence={str(p): evidence[str(p)] for p in (CENSUS, *DRAFTS)}),
        },
        summary=summary, document='docs/editorial_Rafael_B170_B176_research_ready_20261105.md',
        document_text=doc, completed=13820,
        protected={str(REGISTRY): digest(REGISTRY), release['canonical_base']: release['canonical_sha256'],
            release['candidate']: release['candidate_sha256'], package['zip']: package['zip_sha256']},
    )


if __name__ == '__main__':
    main()
