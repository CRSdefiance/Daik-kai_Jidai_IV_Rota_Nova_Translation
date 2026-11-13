"""Checkpoint offline and direct visual review of the B221–B240 choice menus."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.checkpoint_rafael_B221_B240_contextual_v1 import KEY, LEDGER, PACKAGE, REGISTRY, RELEASE
from scripts.review_rafael_B221_B240_menus_v1 import REVIEW
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint
from scripts.write_rafael_B221_B240_contextual_v1 import digest


def main():
    menu, release, package, ledger = map(load, (REVIEW, RELEASE, PACKAGE, LEDGER))
    assert menu['visually_reviewed_captions'] == 7 and not menu['actual_gameplay']
    assert all(digest(Path(path)) == expected for path, expected in menu['evidence'].items())
    batch = ledger[KEY]
    assert batch['four_prose_gates_pass'] == 270 and batch['new_credit'] == 0
    summary = (
        'Rafael B221–B240 has 270 contextual decisions, including 221 revisions and 49 retentions. '
        'All seven captions in three menus passed native offline formatting and direct visual checks. '
        'Speech formatting, stored checks, focused gameplay and registration remain pending. '
        'Integrated coverage remains 14,797.'
    )
    detail = f"""# Rafael B221–B240 caption verification

{summary}

The binary menus preserve the full answers, including the apostrophe and periods. The three-choice menu displays Zhao Yun, Guan Yu and Zhuge Liang in full. The offline check covered 28 caption style planes, 18 native provider alignments and 60 bridged returns. Controller behavior and final stored menus remain pending. {link('Direct caption review', REVIEW)}.

Resume the body formatting and native verification from the [contextual checkpoint](editorial_Rafael_B221_B240_contextual_20261106.md). Reuse this caption proof when the relevant dependencies match. Rafael2952 is the current registered cumulative ROM and Rafael2549 is the packaged weekend build.
"""
    checkpoint(
        mutation=REVIEW.parent/'caption_checkpoint_v1', batch_key=KEY,
        batch_updates=dict(new_credit=0, offline_native_captions=7, visually_reviewed_captions=7,
            caption_style_planes=28, caption_visual_review=str(REVIEW), caption_visual_review_sha256=digest(REVIEW),
            evidence={**batch['evidence'], str(REVIEW): digest(REVIEW), str(Path(__file__)): digest(Path(__file__))}),
        additional_updates={'editorial_execution_priority_20261104': dict(new_credit=0,
            current_batch='Rafael B221–B240 speech formatting and focused validation.',
            next_action='Format and verify the speech bodies, including three signed progressive letters, the swan effect '
                        'and the four voice commands. Reuse the offline caption and visual proof for the three menus.',
            guide_photos=False)},
        summary=summary, document='docs/editorial_Rafael_B221_B240_captions_20261106.md',
        document_text=detail, completed=14797, protected={str(REGISTRY): release['registry_sha256'],
            release['canonical_base']: release['canonical_sha256'], release['candidate']: release['candidate_sha256'],
            release['patch']: release['patch_sha256'], package['zip']: package['zip_sha256']},
    )
    print('Saved caption progress without adding registered coverage.')


if __name__ == '__main__':
    main()

