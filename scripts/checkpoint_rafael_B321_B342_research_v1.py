"""Save the finished batch without prematurely crediting its pending release."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.build_registered_rafael4347_v1 import RELEASE, REGISTRY
from scripts.finalize_rafael_B321_B342_research_v1 import ROOT, READY, FINAL, FINAL_NAMES, RESEARCH
from scripts.prepare_rafael_B321_B342_registered_v1 import QUALIFICATION
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import PACKAGE


def main():
    ready, release, package = map(load, (READY, RELEASE, PACKAGE))
    assert ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
    assert load(QUALIFICATION)['dialogue_rebuilt_and_exact_556_stored_bindings_verified']
    summary = ('Rafael B321–B342 passed all five review gates for 556 records: 364 revisions and 192 justified retentions. '
               'All 552 stored pages, 650 branch cases and seven menus passed. The focused emulator sequence displayed '
               '76 pages across 72 utterances and all 16 captions. The cumulative successor is qualified; registration '
               'and its own startup remain pending. Integrated coverage is 16,192.')
    doc = f'''# Rafael B321–B342 research checkpoint

{summary}

Final reviews: [556 exact source/current/target bindings](../{FINAL.as_posix()}) and [16 scoped speaker-name decisions](../{FINAL_NAMES.as_posix()}). Every individual record passed the five natural-dialogue-v2 gates. The 16 names are scoped to these conversations, not a claim of completing the 207-name catalogue. [Sealed research completion](../{READY.as_posix()}).

All 540 ordinary and alternate bodies were checked offline. Final body sheets, refreshed layouts, name sheets and menu sheets were directly inspected. Fifty-two layouts use approved refreshed wrapping; 488 retain their checked layouts. The phrase “what I'm capable of.” retains its complete idiomatic ending with one documented narrow line-ending waiver. Three full-width I characters were corrected. [Final visual proof](../{(ROOT/'complete_visual_review_v1.json').as_posix()}).

The initialized emulator display sequence observed 72 utterances, 76 pages, all 16 scoped headers, all seven default menu choices and their following dialogue. All four selected page turns passed. The remaining 468 body variants have offline coverage. Natural quest activation, original locations, earned chronology, other choice outcomes, the full route and hardware were not observed. [Gameplay evidence](../{(RESEARCH/'actual_review.json').as_posix()}). [Stored evidence](../{(ROOT/'stored_v1/stored_native_verification.json').as_posix()}). Tiny ellipsis ink was individually checked against the native font and matched.

The release qualification reproduces the exact research ROM and its 556 bindings, changes only the reviewed SC0 blocks and restores the complete Rafael4347 parent byte for byte. Two three-choice menus share a receipt; release checks identify each by original block, command offset and caption IDs, and bind source and relocated stored offsets separately. Earlier failed preparation drafts are preserved. [Qualification](../{QUALIFICATION.as_posix()}).

Continue with registered Rafael4903 staging, its own startup and inherited name getters, then credit this batch once. Preserve the accepted ASCII right-bound correction, every prior layer, promoted main and weekend package. The full editorial objective, remaining shared/town/random prose and name catalogue remain open. Artwork and the later older-record audit remain separate. No guide photographs are being collected.
'''
    evidence = {str(p): digest(p) for p in (READY, FINAL, FINAL_NAMES, QUALIFICATION, Path(__file__))}
    checkpoint(mutation=ROOT/'research_checkpoint_v1', batch_key='Rafael_SC0_B321_B342_clean_20261106',
        batch_updates=dict(new_credit=0, five_gate_research_records=556, prose_revisions=364,
            justified_retentions=192, formatting_pending=False, representative_gameplay_pending=False,
            representative_utterances=72, representative_pages=76, representative_menus=7,
            offline_only_speech_variants=468, scoped_names_reviewed=16, registered_integration_pending=True,
            native_job_live=False, guide_photos=False, evidence=evidence),
        summary=summary, document='docs/editorial_Rafael_B321_B342_research_20261106.md',
        document_text=doc, completed=16192, protected={
            str(REGISTRY): release['registry_sha256'], release['canonical_base']: release['canonical_sha256'],
            release['candidate']: release['candidate_sha256'], release['patch']: release['patch_sha256'],
            package['zip']: package['zip_sha256']})
    print('Saved all 556 completed research reviews; registered credit remains 16,192.')


if __name__ == '__main__':
    main()
