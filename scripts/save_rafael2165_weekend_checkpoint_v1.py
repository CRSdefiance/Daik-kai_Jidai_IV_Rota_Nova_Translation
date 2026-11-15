"""Record the verified weekend package and preserve the next editorial checkpoint."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint


ANALYSIS = Path('work/analysis')
ROOT = ANALYSIS / 'Rafael2165_extended_release_verified_v1_20261105'
RELEASE = ROOT / 'registered_release_verification.json'
CREDIT = ROOT / 'completion_checkpoint.json'
PACKAGE = ANALYSIS / 'Weekend_testing_package_Rafael2165_20261105/package_verification.json'
PRIOR = ANALYSIS / 'Weekend_testing_package_Rafael1860_20261105/package_verification.json'
RESEARCH = ANALYSIS / 'Rafael_B170_B176_research_final_v1_20261105/research_completion.json'
REGISTRY = Path('translations/release_stack.json')


def digest(path):
    return sha(Path(path).read_bytes())


def main():
    release, credit, package, prior, research = map(load, (RELEASE, CREDIT, PACKAGE, PRIOR, RESEARCH))
    assert credit['new_credit'] == 190 and credit['counts'] == dict(completed=14010, revised=8090, retained=5920)
    assert (release['complete_stack_entries'], release['accepted_layers'], release['passing_release_checks']) == (687, 114, 26)
    assert release['only_owned_SC0_blocks_changed'] == list(range(170, 177))
    assert release['clean_input_patch_byte_exact'] and release['all_eight_registered_final_stages_preserved']
    assert not release['own_registered_startup_pending']
    assert package['ROM_sha256'] == release['candidate_sha256'] == package['reconstructed_sha256']
    assert package['ZIP_CRCs_and_member_hashes_pass'] and package['experimental_not_promoted']
    assert digest(package['zip']) == package['zip_sha256'] and digest(prior['zip']) == prior['zip_sha256']
    assert (research['actual_source_variants'], research['actual_pages'], research['offline_only_source_variants']) == (72, 72, 118)
    summary = (
        f"The {link('Rafael2165 weekend ZIP', package['zip'])} contains the registered four-route ROM "
        f"`{release['candidate_sha256'][:8]}`, its clean-input patch, manifest and Rafael-first test notes. "
        "It adds 305 reviewed Rafael records since Rafael1860. All 687 stack entries, 114 accepted layers, "
        "eight final stages and 26 release checks passed, along with exact clean-input reconstruction and a fresh Rafael startup. "
        "Integrated total is 14,010. Continue the B181–B200 intake from 138 clean drafts. "
        "The designated main and earlier packages are preserved."
    )
    doc = f"""# Rafael2165 registered checkpoint and weekend package

{summary}

The ZIP was re-read and every member hash verified. The packaged patch rebuilt the ROM byte for byte from the clean Japanese input. Exact-ROM emulator cold boot reached Rafael's opening. Physical hardware and a full playthrough remain open. {link('Package verification', PACKAGE)}. {link('Registered release verification', RELEASE)}.

The new B170–B176 batch credits 152 revisions and 38 justified retentions once. All 190 stored pages and 13 scoped nameplates passed offline and direct visual checks. The initialized emulator sequence showed 72 speeches and pages, six modal pages, all 13 nameplates and both FI substitutions. The other 118 speeches passed offline checks. Original conditional activation remains open. {link('Review and emulator scope', RESEARCH)}.

All 741 B161–B180 records are integrated. The next intake has 384 clean records. B181–B185 have 138 independent drafts, leaving 246 clean drafts and 384 current-English comparisons. Maintain Rafael and tutorial priority. Artwork and the later technical re-audit remain separate.
"""
    evidence = {str(p): digest(p) for p in (RELEASE, CREDIT, PACKAGE, PRIOR, RESEARCH, Path(__file__))}
    checkpoint(
        mutation=ROOT / 'weekend_documentation_checkpoint',
        batch_key='Rafael_SC0_B161_B180_clean_20261105',
        batch_updates=dict(new_credit=0, independently_drafted_records=741, current_comparisons=741,
            contextual_comparison_records=741, integrated_subbatch_credit=741,
            integrated_blocks=list(range(161, 181)), full_intake_not_complete=False,
            subset_registered_release=str(RELEASE), subset_registered_release_sha256=digest(RELEASE), evidence=evidence),
        additional_updates={'editorial_execution_priority_20261104': dict(new_credit=0,
            current_batch='Rafael B181–B200 clean-first dialogue intake.',
            next_action='Draft remaining complete clean-source exchanges, then compare with registered Rafael2165.',
            current_batch_not_yet_integrated=True, prior_B170_B176_integrated_and_credited_once=True,
            native_job_live=False, registered_build_live=False, guide_photos=False)},
        new_entries={'weekend_testing_package_Rafael2165_20261105': dict(new_credit=0,
            package=package['zip'], package_sha256=package['zip_sha256'], verification=str(PACKAGE),
            verification_sha256=digest(PACKAGE), candidate=release['candidate'],
            candidate_sha256=release['candidate_sha256'], previous_package=prior['zip'],
            additional_reviewed_records_since_previous_package=305, main_unchanged=True)},
        summary=summary, document='docs/editorial_Rafael2165_registered_checkpoint_v1_20261105.md',
        document_text=doc, completed=14010, protected={str(REGISTRY): release['registry_sha256'],
            release['canonical_base']: release['canonical_sha256'], release['candidate']: release['candidate_sha256'],
            release['parent']: release['parent_sha256'], package['zip']: package['zip_sha256'],
            prior['zip']: prior['zip_sha256']},
    )
    print('Saved Rafael2165 weekend package verification and editorial handoff.')


if __name__ == '__main__':
    main()
