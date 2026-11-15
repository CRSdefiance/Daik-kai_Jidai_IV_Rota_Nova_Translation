"""Save the cumulative handoff after the verified 292-record credit."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import LEDGER, PACKAGE
from scripts.verify_rafael3514_registered_release_v1 import RELEASE, ROOT, digest


NEXT = 'Rafael_SC0_B261_B280_clean_20261106'
FINAL = Path('translations/rafael_B241_B260_integrated_final_review_v1.json')
PROGRESS = ROOT/'completion_checkpoint.json'
FIELD = Path('work/Rafael3514_Francisca_field_preparation_v1_20261106/qualification.json')


def main():
    release, credit, ledger, package, field = map(load, (RELEASE, PROGRESS, LEDGER, PACKAGE, FIELD))
    assert credit['new_credit'] == release['new_contextual_records'] == 292
    assert credit['counts'] == dict(completed=15359, revised=9171, retained=6188)
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    assert field['target_reference_sha256'] == release['candidate_sha256'] and not release['own_registered_startup_pending']
    assert ledger[NEXT]['independently_drafted_records'] == 57
    summary = (
        'Rafael B241–B260 is registered and credited once, with 244 revisions and 48 justified retentions. '
        'Experimental Rafael3514 passed 692 manifest entries, 114 accepted layers, 27 release checks, exact clean-input reconstruction '
        'and its own Rafael startup. The independently owned Francisca name correction is included. Integrated coverage is 15,359.'
    )
    doc = f"""# Rafael B241–B260 registered checkpoint

{summary}

The combined candidate retains the eight earlier final stages, including the ASCII right-bound correction, and appends the exclusive actor 186 name field. Only 18 reviewed SC0 blocks and the tested ARM9 span differ from Rafael3222. All 292 stored references match the research proofs. The clean-input patch reproduces the final ROM byte for byte. Both name getters return Francisca and Fernan Silveira from the final candidate's own startup data. {link('Registered ROM', release['candidate'])}. {link('Clean-input patch', release['patch'])}. {link('Release verification', RELEASE)}. {link('Integrated review ledger', FINAL)}.

The B241–B260 research fixtures displayed 132 speech variants across 135 pages, all six captions and 13 speaker headers. The other 154 speech variants passed offline checks. Natural activation of unvisited branches and physical hardware remain outside this evidence. The Rafael3222 weekend package remains available. {link('Weekend package', package['zip'])}.

Continue B265–B280 from the 57 completed B261–B264 clean drafts. The intake still needs 78 clean-source drafts and 135 comparisons. The next release must retain the new field and the earlier eight stages. Preserve Rafael/tutorial priority, deferred artwork and the later older-record audit. {link('Clean drafts', ledger[NEXT]['clean_drafts'])}.
"""
    evidence = {**ledger[NEXT]['evidence'], **{str(path):digest(path) for path in (RELEASE, PROGRESS, FINAL, FIELD)}}
    checkpoint(mutation=ROOT/'registered_documentation_v1', batch_key=NEXT,
        batch_updates=dict(new_credit=0, evidence=evidence, independent_draft_parent_candidate=release['candidate'],
            independent_draft_parent_candidate_sha256=release['candidate_sha256']),
        additional_updates={'editorial_execution_priority_20261104': dict(new_credit=0,
            current_batch='Rafael B265–B280 remaining clean drafts.',
            next_action='Seal all remaining source meanings and independent English before comparing with Rafael3514.',
            native_job_live=False, registered_build_live=False, guide_photos=False)},
        summary=summary, document='docs/editorial_Rafael_B241_B260_registered_20261106.md',
        document_text=doc, completed=15359, protected={'translations/release_stack.json':release['registry_sha256'],
            release['canonical_base']:release['canonical_sha256'], release['candidate']:release['candidate_sha256'],
            release['patch']:release['patch_sha256'], package['zip']:package['zip_sha256']})
    print('Saved the Rafael3514 registered handoff and next clean checkpoint.')


if __name__ == '__main__':
    main()
