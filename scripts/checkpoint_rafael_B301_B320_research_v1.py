"""Record the five-gate review and release qualification without assigning credit."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load
from scripts.checkpoint_rafael3894_registered_v1 import LEDGER, NEXT, PACKAGE, RELEASE
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.checkpoint_rafael_B301_B320_display_v1 import NEXT_PACKET
from scripts.finalize_rafael_B301_B320_research_v1 import FINAL, FINAL_NAMES, READY, RESEARCH, ROOT, STORED
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_rafael_B301_B320_registered_v1 import CONFIG, QUALIFICATION
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint


def main():
    paths = (FINAL, FINAL_NAMES, READY, CONFIG, QUALIFICATION, Path(__file__))
    ready, release, qualification, ledger, package = map(load, (READY, RELEASE, QUALIFICATION, LEDGER, PACKAGE))
    assert ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
    assert (ready['records'], ready['revisions'], ready['retentions']) == (453, 397, 56)
    assert (ready['actual_source_variants'], ready['actual_pages'], ready['actual_choice_labels'],
            ready['actual_menus'], ready['actual_name_headers'], ready['offline_only_source_variants']) == (45, 47, 11, 5, 10, 397)
    assert ready['manuscript_sha256'] == digest(FINAL)
    assert all(digest(path) == checksum for path, checksum in ready['evidence'].items())
    assert qualification['config_sha256'] == digest(CONFIG)
    assert qualification['predecessor_release_sha256'] == digest(RELEASE)
    assert qualification['registry_sha256'] == release['registry_sha256']
    assert qualification['only_SC0_changes'] and qualification['complete_parent_inverse_exact']
    assert qualification['dialogue_rebuilt_and_exact_453_stored_bindings_verified']
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    summary = (
        'Rafael B301–B320 passed all five review gates for 453 records. The focused emulator sequence displayed '
        '47 pages and all five menus. The dialogue transaction qualifies over Rafael3894. '
        'Cumulative registration and candidate startup remain pending. Integrated coverage is 15,739.'
    )
    doc = f"""# Rafael B301–B320 release qualification checkpoint

{summary}

The batch has 397 revisions and 56 justified retentions. All 444 stored pages and 630 relocated branch cases passed. The cold-boot initialized sequence displayed 45 utterances, both two-page turns, 11 captions, the default choice and following dialogue at each menu, and 10 public nameplates including Safia and Al Shin. The other 397 speech variants passed offline. Natural quest activation and event outcomes remain outside this emulator sample. {link('Final five-gate ledger', FINAL)}. {link('Final name decisions', FINAL_NAMES)}. {link('Stored evidence', STORED)}. {link('Focused emulator evidence', RESEARCH/'actual_review.json')}.

The reviewed SC0 transaction reverses byte for byte to Rafael3894. ARM9 and the other files and components match the registered predecessor. Carry forward the existing ASCII right-bound correction and all accepted stages, rerun the four-archive format guard, verify the exact clean-input patch, and test the successor’s own startup before assigning credit. The clean B321–B342 intake contains 556 records and is available for the next contextual batch. {link('Release qualification', QUALIFICATION)}. {link('Registered configuration input', CONFIG)}. {link('Next clean packet', NEXT_PACKET)}.
"""
    checkpoint(mutation=ROOT/'B301_B320_research_checkpoint_v1', batch_key=NEXT,
        batch_updates=dict(new_credit=0, formatting_pending=False, representative_gameplay_pending=False,
            registered_integration_pending=True, five_gate_research_records=453, representative_pages=47,
            representative_menus=5, research_completion=str(READY), research_completion_sha256=digest(READY),
            registration_qualification=str(QUALIFICATION), registration_qualification_sha256=digest(QUALIFICATION),
            evidence={**ledger[NEXT]['evidence'], **{str(path): digest(path) for path in paths}}),
        additional_updates={'editorial_execution_priority_20261104': dict(new_credit=0,
            current_batch='Rafael B301–B320 registered integration.',
            next_action='Create and verify the cumulative successor with exact clean-input patch and own startup.',
            native_job_live=False, registered_build_live=False, guide_photos=False)},
        summary=summary, document='docs/editorial_Rafael_B301_B320_research_20261106.md',
        document_text=doc, completed=15739, protected={
            'translations/release_stack.json': release['registry_sha256'],
            release['canonical_base']: release['canonical_sha256'],
            release['candidate']: release['candidate_sha256'],
            release['patch']: release['patch_sha256'],
            package['zip']: package['zip_sha256'],
        })
    print(summary)


if __name__ == '__main__':
    main()
