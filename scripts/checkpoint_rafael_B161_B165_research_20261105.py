"""Record the 67 completed Rafael research reviews and 26 additional clean drafts."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint

A = Path('work/analysis')
ROOT = A / 'Rafael_B161_B165_research_final_v1_20261105'
READY = ROOT / 'research_completion.json'
ACTUAL = ROOT / 'actual_review.json'
REBUILT = A / 'Rafael_B161_B165_reconstruction_v1_20261105/reconstruction.json'
DRAFT = A / 'Rafael_B161_B180_clean_20261105/B166_opening_audience_clean_drafts_v1.json'
RELEASE = A / 'Rafael1607_extended_release_verified_v1_20261105/registered_release_verification.json'
PACKAGE = A / 'Weekend_testing_package_Rafael1607_20261105/package_verification.json'
REGISTRY = Path('translations/release_stack.json')
BATCH = 'Rafael_SC0_B161_B165_research_20261105'


def digest(path):
    return sha(Path(path).read_bytes())


def main():
    ready, actual, rebuilt, draft, release, package = map(load, (READY, ACTUAL, REBUILT, DRAFT, RELEASE, PACKAGE))
    assert ready['all_individual_five_gates_pass'] and (ready['records'], ready['revisions'], ready['retentions']) == (67, 51, 16)
    assert (actual['source_speech_variants_observed'], actual['native_body_pages_observed'], actual['offline_only_speech_variants']) == (55, 56, 12)
    assert len(draft['records']) == 26
    assert digest(rebuilt['research_ROM']) == rebuilt['research_ROM_sha256']
    assert rebuilt['parent_sha256'] == release['candidate_sha256'] == package['ROM_sha256']
    assert digest(REGISTRY) == release['registry_sha256']
    summary = ('Rafael B161–B165 has 67 complete five-gate research reviews, with 51 revisions and 16 justified retentions. '
        'All 68 stored and directly viewed pages, eight scoped nameplates, 100 native branch cases and 343 archive loads passed. '
        'An initialized emulator fixture displayed 55 speeches and 56 pages. The other 12 speeches were checked offline. '
        'Registered integration is pending. The B166 opening audience has 26 new clean-first drafts. '
        'Integrated total remains 13,452. Main and the Rafael1607 weekend ZIP are preserved.')
    doc = """# Rafael B161–B165 research checkpoint

The [individual review ledger](../translations/rafael_B161_B165_final_review_v1.json) seals 67 five-gate reviews with exact clean, current and stored references, 51 revisions and 16 justified retentions. The revisions restore the priest's Japanese relic award, remove the invented family relationship in the boy's exchange with Claudio and correct three mixed-width lines. The king's exchanges preserve his own promise to rebuild Portugal and the possibility of seeking the Pope's recognition. All eight public names or roles were retained with individual reasons.

The [research completion proof](../work/analysis/Rafael_B161_B165_research_final_v1_20261105/research_completion.json) binds the pinned research image and its inverse. The build changes only SC0 B161–B165. Direct visual review covered all 68 body pages and eight headers alongside full stored glyph, bounds, pagination and substitution checks. All 67 native catalogue lookups, 100 relative branch cases and 343 archive loads passed.

One disclosed 18,401-frame initialized emulator run displayed 55 speeches, 56 pages and all eight public headers. It covered the FE sound notice, ordinary advance, all seven substitutions and the king's two-page negotiation. All five actual dialogue sheets were reviewed. Twelve other speeches were checked offline. Natural branch activation, original locations, story chronology and hardware remain unvisited for this batch.

The current registered release and weekend ZIP remain Rafael1607. Proceed with the v6 registered cumulative transaction using the compatible B146 percent relocation proof, all 114 accepted layers and eight final stages including ASCII right bounds. Grant the 67 credits once the release, clean patch and own startup pass.

The [B166 opening audience](../work/analysis/Rafael_B161_B180_clean_20261105/B166_opening_audience_clean_drafts_v1.json) has 26 independent clean-first drafts. All 491 B166–B176 current-English comparisons and 465 remaining clean drafts are open. Keep the other routes, shared dialogue, speaker labels and player-facing prose in scope.
"""
    checkpoint(mutation=A/'Rafael_B161_B165_research_ledger_20261105',
        batch_key='Rafael_SC0_B161_B180_clean_20261105',
        batch_updates=dict(new_credit=0, independently_drafted_records=276,
            independent_draft_blocks=[161,162,163,164,165,177,178,179,180],
            remaining_clean_meanings_anddrafts=465, current_comparisons=250, remaining_current_comparisons=491,
            partially_drafted_block_166_records=26, new_clean_B166_opening_drafts=str(DRAFT),
            new_clean_B166_opening_drafts_sha256=digest(DRAFT), latest_complete_research_subset=BATCH, full_intake_not_complete=True),
        new_entries={BATCH: dict(new_credit=0, records=67, blocks=[161,162,163,164,165], revisions=51, justified_retentions=16,
            all_five_research_gates_pass=True, registered_integration_pending=True, research_completion=str(READY),
            research_completion_sha256=digest(READY), actual_source_variants=55, offline_only_source_variants=12,
            exact_manuscript=ready['manuscript'], exact_manuscript_sha256=ready['manuscript_sha256'])},
        additional_updates={'editorial_execution_priority_20261104': dict(new_credit=0, current_batch=summary,
            next_action='Register B161–B165 and continue clean drafting and contextual review of B166–B176.',
            current_batch_not_yet_integrated=True, native_job_live=False, guide_photos=False)},
        summary=summary, document='docs/editorial_Rafael_B161_B165_research_ready_20261105.md', document_text=doc,
        completed=13452, protected={str(REGISTRY):release['registry_sha256'],
            'dk4tool/rom/nds.py':'27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
            release['canonical_base']:release['canonical_sha256'], release['candidate']:release['candidate_sha256'],
            package['zip']:package['zip_sha256']})
    print('Saved 67 research reviews and 26 new clean drafts. Integrated credit stays at 13,452.')


if __name__ == '__main__':
    main()
