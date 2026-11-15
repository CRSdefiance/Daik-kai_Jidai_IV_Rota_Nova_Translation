"""Save the qualified Rafael research handoff without assigning credit twice."""
from pathlib import Path

from scripts import finalize_rafael_B261_B280_research_v1 as batch
from scripts.audit_story_glyph_consistency import load
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.finish_rafael_B261_B280_native_pages_v1 import ROOT, digest
from scripts.prepare_rafael_B261_B280_registered_v1 import CONFIG, OUT as PREPARATION
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import LEDGER, PACKAGE
from scripts.save_rafael3514_registered_checkpoint_v1 import NEXT
from scripts.verify_rafael3514_registered_release_v1 import RELEASE


QUALIFICATION = PREPARATION/'qualification.json'


def main():
    ready, qualification, release, ledger, package = map(load, (batch.READY, QUALIFICATION, RELEASE, LEDGER, PACKAGE))
    assert ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
    assert (ready['records'], ready['revisions'], ready['retentions'], ready['new_credit']) == (135, 118, 17, 0)
    assert all(digest(path) == checksum for path, checksum in ready['evidence'].items())
    assert qualification['config_sha256'] == digest(CONFIG) and qualification['predecessor_release_sha256'] == digest(RELEASE)
    assert qualification['both_components_whole_parent_inverse_exact'] and qualification['all_nine_prior_stage_dependencies_preserved']
    assert qualification['registration_and_candidate_own_startup_pending']
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    summary = (
        'Rafael B261–B280 passed all five research gates for 135 records, with 118 revisions and 17 justified retentions. '
        'All 131 stored pages passed. A focused emulator sequence displayed 43 pages, both menus and Jacob’s nameplate. '
        'Both surname corrections and the cumulative transaction are qualified. Registration and candidate startup remain pending. '
        'Integrated coverage is 15,359.'
    )
    doc = f"""# Rafael B261–B280 research completion

{summary}

All 20 blocks rebuilt with 353 commands and 78 relative sites. All 390 native relative cases, all 343 native archive loads, 686 parent-mode cases and all 130 stored pre-macro body lookups passed. Forty-seven stored pages received fresh parity checks. The Hamburg notice keeps its one-line layout because the two extra native space events contribute zero ink and its full logical and physical planes remain byte-identical. {link('Final five-gate ledger', batch.FINAL)}. {link('Stored display and command evidence', batch.STORED)}.

The 15,761-frame initialized emulator sequence displayed 42 speech variants across 43 pages. Both menus showed all five captions and responded to the default selection. Both cave-in tables displayed their Sailor voice, all three town greetings expanded FI to Rafael, and both pages of Julian’s briefing displayed. The sequence showed 10 distinct speaker identities including Jacob Portunto. The other 88 speech variants, other cursor states and original branches received offline checks. This run used selected commands from multiple scenes and did not establish natural activation, original locations, original branch outcomes or hardware behavior. {link('Observed and offline scope', batch.RESEARCH/'actual_review.json')}.

Plett Perrault uses nine bytes in the existing 24-byte staged alignment reserve. The item prose, original Perot slot, adjacent Sakura, cache wrapper and heap boundaries remain byte-exact. The only coincidental raw address match in other ROM files was inside a decoded pixel plane. Both original name getters and the complete native glyph planes passed for Plett and Jacob. The emulator fixture’s read-only RAM dump contains the exact proposed Plett pointer and complete staged payload. Plett’s nameplate was unvisited. {link('Scoped names', batch.FINAL_NAMES)}.

The prepared successor freshly reconstructs the 135 exact records over Rafael3514 and applies the two independent surname corrections. Only SC0 and ARM9 change, and the inverse reproduces the entire nine-stage predecessor. Register the sealed successor, verify its own startup and name getters, reconstruct the exact ROM from the clean-input patch, and assign batch credit once. The registry and accepted main remain at their verified state. {link('Cumulative transaction qualification', QUALIFICATION)}.
"""
    evidence = {**ledger[NEXT]['evidence'], **ready['evidence'],
        **{str(path): digest(path) for path in (batch.READY, QUALIFICATION, CONFIG, Path(__file__))}}
    checkpoint(
        mutation=ROOT/'B261_B280_research_checkpoint_v1', batch_key=NEXT,
        batch_updates=dict(
            new_credit=0, contextual_review=str(batch.FINAL), contextual_review_sha256=digest(batch.FINAL),
            formatting_pending=False, stored_checks_pending=False, representative_gameplay_pending=False,
            plett_surname_relocation_pending=False, two_surname_fields_qualified=True,
            five_research_gates_complete=True, observed_speech_variants=42, observed_pages=43,
            offline_only_speech_variants=88, registered_integration_pending=True,
            release_qualification=str(QUALIFICATION), release_qualification_sha256=digest(QUALIFICATION),
            evidence=evidence,
        ),
        additional_updates={'editorial_execution_priority_20261104': dict(
            new_credit=0, current_batch='Rafael B261–B280 registered cumulative integration.',
            next_action='Register the exact qualified successor and verify its own startup, getters and clean-input reconstruction.',
            native_job_live=False, registered_build_live=False, guide_photos=False,
        )},
        summary=summary, document='docs/editorial_Rafael_B261_B280_research_20261106.md',
        document_text=doc, completed=15359, protected={
            'translations/release_stack.json': release['registry_sha256'],
            release['canonical_base']: release['canonical_sha256'],
            release['candidate']: release['candidate_sha256'],
            release['patch']: release['patch_sha256'],
            package['zip']: package['zip_sha256'],
        },
    )
    print('Saved qualified Rafael research and registered handoff. Integrated coverage remains 15,359.')


if __name__ == '__main__':
    main()
