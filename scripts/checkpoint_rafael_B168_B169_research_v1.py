"""Record the sealed Angelo and Ian reviews and all remaining clean-first drafts."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint


A = Path('work/analysis')
ROOT = A / 'Rafael_B168_B169_research_final_v1_20261105'
RESEARCH = ROOT / 'research_completion.json'
ACTUAL = ROOT / 'actual_review.json'
RECONSTRUCTION = A / 'Rafael_B168_B169_current1860_20261105/reconstruction_v1/reconstruction.json'
DRAFTS = A / 'Rafael_B161_B180_clean_20261105/B170_B176_clean_first_v1/sealed_drafts.json'
BINDING = DRAFTS.with_name('current_binding_meanings.json')
RELEASE = A / 'Rafael1860_extended_release_verified_v1_20261105/registered_release_verification.json'
PACKAGE = A / 'Weekend_testing_package_Rafael1860_20261105/package_verification.json'
REGISTRY = Path('translations/release_stack.json')
KEY = 'Rafael_SC0_B168_B169_research_20261105'


def digest(path):
    return sha(Path(path).read_bytes())


def link(label, path):
    return f'[{label}](../{Path(path).as_posix()})'


def main():
    ready, actual, rebuild, drafts, release, package = map(load, (RESEARCH, ACTUAL, RECONSTRUCTION, DRAFTS, RELEASE, PACKAGE))
    assert ready['all_individual_five_gates_pass'] and (ready['records'], ready['revisions'], ready['retentions']) == (115, 90, 25)
    assert rebuild['changed_blocks'] == [168, 169] and rebuild['parent_sha256'] == release['candidate_sha256']
    assert rebuild['full_clean_current_block_archive_andserialized_NDS_inverses_exact']
    assert (ready['body_pages'], ready['scoped_public_names'], actual['source_speech_variants_observed'],
            actual['native_body_pages_observed'], actual['offline_only_speech_variants']) == (117, 10, 58, 60, 57)
    assert drafts['records_count'] == 190 and drafts['complete_blocks'] == list(range(170, 177))
    assert drafts['all_five_gates_pending'] and load(BINDING)['all_drafts_sha256'] == digest(DRAFTS)
    assert package['ROM_sha256'] == release['candidate_sha256'] and digest(package['zip']) == package['zip_sha256']
    evidence = {str(p): digest(p) for p in (RESEARCH, ACTUAL, RECONSTRUCTION, DRAFTS, BINDING, RELEASE, PACKAGE, Path(__file__))}
    summary = ('Rafael B168–B169 has 115 five-gate reviews, 90 revisions and 25 justified retentions. '
        'All 117 stored and directly viewed pages, ten nameplates, 125 branch cases and 343 archive loads passed. '
        'An initialized emulator sequence showed 58 speeches and 60 pages. '
        'Registered integration is in progress. All 190 B170–B176 clean drafts are sealed. '
        'Integrated credit remains 13,705, and Rafael1860 remains the delivered weekend build.')
    doc = f"""# Rafael B168–B169 reviewed and ready for integration

The {link('individual five-gate ledger', ready['manuscript'])} contains 115 complete-exchange decisions, with 90 revisions and 25 justified retentions. The revised text restores Claudio Manaus, the source’s navigator and fleet-command distinctions, Ian’s objection to being touched and one untranslated line. The two trade turns now follow complete thoughts. The two mixed-width Latin glyphs and two inconsistent reaction marks in B168 are corrected. Source-authored silence and the lone alarm mark in B169 retain their native punctuation. The Sailor nameplate and separate Retainer catalogue label follow the distinct clean getters. {link('Research verification', RESEARCH)}.

All 117 final pages and ten nameplates passed the native and direct visual checks. The stored proof covers 55 fresh parity-dependent pages, 62 exact reusable compiled pages, 125 branch cases, 115 catalogue reads and all 343 archive loads. The isolated reference changes only B168–B169 over Rafael1860. A 19,361-frame initialized emulator sequence with ordinary A inputs showed 58 speeches and 60 pages, both trade page turns and all ten nameplates. The remaining 57 speeches are offline-only. Natural event activation, original locations and hardware remain unvisited. {link('Reconstruction', RECONSTRUCTION)}. {link('Observed emulator scope', ACTUAL)}.

All 190 clean-first drafts for B170–B176 are sealed. The six modal leads include Carlo’s family-loss account and the flamenco audience’s labelled reactions, joint cheer and applause. Compare the full exchanges against current English before display planning. All 741 inventoried B161–B180 records now have independent clean drafts. {link('Next source packet', BINDING)}.

Register this exact experimental successor with the preserved ASCII right-bound fix and all accepted layers, then verify clean-input patch reconstruction and an own startup before adding credit. Rafael1860 remains the delivered weekend ZIP. The designated main, earlier builds, deferred artwork and later technical re-audit are preserved.
"""
    checkpoint(
        mutation=ROOT / 'research_documentation_checkpoint',
        batch_key='Rafael_SC0_B161_B180_clean_20261105',
        batch_updates=dict(new_credit=0, independently_drafted_records=741, independent_draft_blocks=list(range(161, 181)),
            full_intake_not_complete=True, current_comparisons=551, contextual_comparison_records=551,
            remaining_current_comparisons=190, remaining_clean_meanings_anddrafts=0, current_binding_records=190,
            latest_research_subset=KEY, next_current_binding=str(BINDING), next_current_binding_sha256=digest(BINDING),
            evidence=evidence),
        additional_updates={'editorial_execution_priority_20261104': dict(new_credit=0,
            current_batch='Rafael B168–B169 complete five-gate research, registered integration in progress.',
            next_action='Finish registered Rafael1975 validation. Compare the 190 sealed B170–B176 drafts with current English.',
            current_batch_not_yet_integrated=True, native_job_live=False, guide_photos=False)},
        new_entries={KEY: dict(new_credit=0, records=115, blocks=[168,169], proposed_revisions=90, justified_retentions=25,
            all_individual_five_research_gates_pass=True, all_117_offline_and_stored_pages_pass=True,
            observed_speeches=58, observed_pages=60, observed_headers=10, offline_only_speeches=57,
            registered_integration_pending=True, focused_gameplay_pending=False,
            research_ROM_sha256=rebuild['research_ROM_sha256'], current_review=ready['manuscript'],
            current_review_sha256=ready['manuscript_sha256'], evidence=evidence)},
        summary=summary, document='docs/editorial_Rafael_B168_B169_research_ready_20261105.md', document_text=doc,
        completed=13705, protected={
            str(REGISTRY): digest(REGISTRY),
            'dk4tool/rom/nds.py': '27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
            release['canonical_base']: release['canonical_sha256'], release['candidate']: release['candidate_sha256'],
            package['zip']: package['zip_sha256'],
        },
    )
    print('Saved the 115 research reviews and all 190 remaining clean drafts. Integrated credit is 13,705.')


if __name__ == '__main__':
    main()
