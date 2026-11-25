"""Preserve the registered candidate and hand off the remaining editorial scope."""
import inspect
import os
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.build_registered_rafael4903_v1 import CANDIDATE, INVERSE_PATCH, PARENT_REGISTRY, RELEASE
from scripts.checkpoint_rafael3649_registered_v1 import pin_release as previous_pins
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import LEDGER, PACKAGE
from scripts.source_locked_derivation_v5118 import checked_text


REGISTRY = Path('translations/release_stack.json')
PINS = Path('translations/rom_retention_pins.json')
INTEGRATED = Path('translations/rafael_B321_B342_integrated_final_review_v1.json')
pin_source = checked_text(inspect.getsource(previous_pins), {'Rafael3649': 'Rafael4903'})
exec(compile(pin_source, __file__ + '::registered-ROM-pins', 'exec'), globals())


def main():
    release, ledger, package = map(load, (RELEASE, LEDGER, PACKAGE))
    assert ledger['records_editorially_completed'] == 16748 and not ledger['full_goal_complete']
    assert ledger['Rafael_SC0_B321_B342_clean_20261106']['completion_credit_added'] == 556
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    assert digest(REGISTRY) == release['registry_sha256']
    registry, parent = map(load, (REGISTRY, PARENT_REGISTRY))
    assert registry['latest_promoted_build'] == parent['latest_promoted_build']
    assert registry['accepted_layers'] == parent['accepted_layers']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    summary = ('Rafael B321–B342 is registered in Rafael4903 and credited once: 556 reviews, '
               '364 revisions and 192 justified retentions. All 552 stored pages and seven menus passed; '
               'the emulator sample displayed 76 pages across 72 utterances. The exact clean-input patch, '
               'candidate startup and inherited names passed. Integrated coverage is 16,748. Main is unchanged.')
    doc = f'''# Rafael B321–B342 registered checkpoint

{summary}

The cumulative test candidate preserves all 697 predecessor manifest entries, 114 accepted layers and the registered ASCII right-bound correction. Its manifest has 698 entries and 33 passing release checks, including a fresh check across all four story archives. Only the 22 reviewed SC0 blocks differ from Rafael4347; the complete parent inverse is exact. Both candidate and clean-input reconstruction are retention-pinned.

- [Rafael4903 candidate](../{CANDIDATE.as_posix()})
- [Exact patch from clean Japanese input](../{Path(release['patch']).as_posix()})
- [Registered release verification](../{RELEASE.as_posix()})
- [556 integrated review decisions and exact references](../{INTEGRATED.as_posix()})
- [Final research and display evidence](editorial_Rafael_B321_B342_research_20261106.md)

The candidate's own 4,001-frame cold boot matched all ten verified opening captures. Its original progressive and full-name getters returned Fernan Silveira, Plett Perrault, Jacob Portunto, Zaganos Bey, Francisca and Sakura. These startup checks add no editorial credit. No main promotion or user hardware acceptance is claimed.

Offline coverage includes 540 body variants, 552 pages, 650 relocated branch cases, 343 archive loads and 686 loader modes. All final body, caption and scoped name sheets were inspected. Fifty-two layouts use refreshed wrapping and 488 retain checked layouts; three full-width I characters were corrected. The complete idiom “what I'm capable of.” has a narrow documented line-ending waiver rather than an unnecessary prose rewrite.

The initialized emulator sample observed 72 utterances, 76 pages, all 16 scoped headers and all 16 captions in seven menus, with each default selection returning to following fixture dialogue. The remaining 468 speech variants have offline checks. Original conditional activation, locations, earned chronology, other menu outcomes, full natural-route play and hardware remain unvisited for this batch.

SC0's final numbered intake is now integrated. Next reconcile the Rafael and tutorial source coverage for residual ordinary speech, style alternatives, typed captions and linked shared scenes, using existing source packets and exact integrated keys. Do not infer complete player-facing route coverage from reaching block 342. Give any residual early-game or tutorial exchange priority, then continue the other remaining routes and shared/town/random prose in substantial complete exchanges. The 202 HELP-topic records are already credited; reuse their proofs and do not restart them. Scoped names are not the complete 207-name localization review.

The existing weekend test package is preserved byte for byte. No guide photographs are requested. All prior ROMs, translations, retentions and evidence remain; artwork and the later older-record technical re-audit remain separate. The full editorial goal is still active.
'''
    pin_release()
    checkpoint(mutation=CANDIDATE.parent/'registered_documentation_v1',
        batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Rafael B321–B342 registered and credited once in Rafael4903.',
            next_action='Reconcile residual Rafael/tutorial source coverage, then continue untouched complete exchanges.',
            current_batch_not_yet_integrated=False, all_current_batch_fifth_gates_pending=False,
            registered_integration_pending=False, native_job_live=False, registered_build_live=False,
            registered_cumulative_build_live=False, guide_photos=False),
        summary=summary, document='docs/editorial_Rafael_B321_B342_registered_20261106.md',
        document_text=doc, completed=16748, protected={
            str(REGISTRY): release['registry_sha256'], release['canonical_base']: release['canonical_sha256'],
            release['candidate']: release['candidate_sha256'], release['patch']: release['patch_sha256'],
            package['zip']: package['zip_sha256']})
    print('Saved registered Rafael4903. Integrated coverage 16,748; main and weekend package unchanged.')


if __name__ == '__main__':
    main()
