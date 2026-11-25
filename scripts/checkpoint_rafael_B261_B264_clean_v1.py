"""Record four clean-first exchanges while B241–B260 awaits integration."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.checkpoint_rafael_B241_B260_research_v1 import READY
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import LEDGER, PACKAGE, RELEASE
from scripts.seal_rafael_B261_B264_clean_v1 import BLOCKS, OUTPUT, ROOT, digest


KEY = 'Rafael_SC0_B261_B280_clean_20261106'


def main():
    drafts, ready, ledger, release, package = map(load, (OUTPUT, READY, LEDGER, RELEASE, PACKAGE))
    assert drafts['complete_blocks'] == BLOCKS and drafts['records_count'] == 57
    assert drafts['all_five_gates_pending'] and drafts['no_current_English_extracted_for_this_intake_before_drafts']
    assert all(digest(path) == checksum for path, checksum in drafts['evidence'].items())
    assert ready['records'] == 292 and ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
    assert ledger[KEY]['source_records'] == 135
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256'] == package['ROM_sha256']
    summary = (
        'Rafael B261–B264 has 57 clean-source drafts across four complete exchanges. '
        'The remaining B261–B280 intake has 78 drafts and 135 comparisons pending. '
        'B241–B260 has 292 verified reviews awaiting registered integration. '
        'Rafael3222 remains the weekend candidate with 15,067 integrated records.'
    )
    doc = f"""# Rafael B261–B264 clean drafts

{summary}

The drafts preserve both cave-in voice tables, all five choice captions, the distinction between the stone puzzle and the figure's challenge, and the separate outcomes of the second choice. The three town exchanges preserve each greeting's FI substitution and the difference between nearby ruins and the lack of famous ruins. All source IDs, controls, and exact references remain attached. {link('Clean drafts', OUTPUT)}.

Finish the clean drafts for B265–B280 before opening the current English for comparison. Carry the verified B241–B260 dialogue and Francisca's exclusive name field through registered integration and exact clean-input reconstruction. {link('B241–B260 research completion', READY)}.
"""
    evidence = {**ledger[KEY]['evidence'], str(OUTPUT): digest(OUTPUT), str(Path(__file__)): digest(__file__)}
    checkpoint(mutation=ROOT/'B261_B264_checkpoint_v1', batch_key=KEY,
        batch_updates=dict(new_credit=0, independently_drafted_records=57,
            independent_draft_blocks=BLOCKS, remaining_clean_meanings_anddrafts=78,
            remaining_current_comparisons=135, clean_drafts=str(OUTPUT),
            clean_drafts_sha256=digest(OUTPUT), evidence=evidence),
        summary=summary, document='docs/editorial_Rafael_B261_B264_clean_20261106.md', document_text=doc,
        completed=15067, protected={'translations/release_stack.json': release['registry_sha256'],
            release['canonical_base']: release['canonical_sha256'], release['candidate']: release['candidate_sha256'],
            release['patch']: release['patch_sha256'], package['zip']: package['zip_sha256']})
    print('Recorded 57 source-first drafts with all integrated coverage preserved.')


if __name__ == '__main__':
    main()
