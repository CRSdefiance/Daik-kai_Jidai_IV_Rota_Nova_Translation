"""Checkpoint the verified B221–B240 batch at the registered integration boundary."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.checkpoint_rafael_B221_B240_contextual_v1 import KEY, LEDGER, PACKAGE, REGISTRY, RELEASE
from scripts.finalize_rafael_B221_B240_research_v1 import FINAL, REBUILT, RESEARCH, digest
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint

READY = RESEARCH/'research_completion.json'
ACTUAL = RESEARCH/'actual_review.json'


def main():
    ready, actual, rebuilt, registered, package, ledger = map(load, (READY, ACTUAL, REBUILT, RELEASE, PACKAGE, LEDGER))
    assert ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
    assert (ready['records'], ready['revisions'], ready['retentions'], ready['new_credit']) == (270, 221, 49, 0)
    assert (ready['body_pages'], ready['typed_labels'], ready['scoped_public_names']) == (279, 7, 26)
    assert (ready['actual_source_variants'], ready['actual_pages'], ready['actual_menus'], ready['actual_name_headers']) == (86,94,3,16)
    assert actual['offline_only_speech_variants'] == 177
    assert rebuilt['parent_sha256'] == registered['candidate_sha256']
    assert all(digest(Path(p)) == h for p, h in ready['evidence'].items())
    summary = (
        'Rafael B221–B240 passed all five review gates for 270 records, with 221 revisions and 49 retentions. '
        'All 279 pages, seven captions, and 26 name or role bindings passed offline review. '
        'Two initialized emulator fixtures showed 94 pages, 16 distinct speaker headers, and all three menus. '
        'Registered integration is pending. Integrated coverage remains 14,797.'
    )
    doc = f"""# Rafael B221–B240 research verification

{summary}

The Solomon exchange now uses normal-width I glyphs while retaining the Rafael and Castor substitutions. The missing Guan Yu response is in English. Three indented letter signatures and the three-row swan call retain their source staging. The pass also kept question tags and titles together where the native width allowed. Exact references and per-record decisions are in the {link('five-gate manuscript', FINAL)}.

The research ROM changes only 19 reviewed blocks of SC0. B231 remains byte-identical. The four voice commands preserve all 32 getter slots and aliases across 29 physical alternatives. Native checks covered 263 pre-macro catalogue reads, 34 relocated branch sites with 170 cases, and 343 archive loads. Every stored body page matches its inspected preview, including 127 pages rerendered with storage padding. {link('Research completion evidence', READY)}.

The initialized fixtures showed 86 speech variants, the four default voice choices, and all seven captions at the default menu cursor. A returned to the next fixture line in each menu. The other 177 speech variants passed offline checks. Original conditional activation, alternate controller paths, and hardware remain unobserved. {link('Focused emulator evidence', ACTUAL)}.

Next register the mixed speech, voice, and menu append over Rafael2952 and verify the exact clean-input patch and candidate startup. Preserve the registered ASCII right-bound repair and the B146 percent-relocation proof. Rafael2549 remains the packaged weekend build. {link('Rafael2952 release evidence', RELEASE)}.
"""
    evidence = {**ledger[KEY]['evidence'], **{str(path): digest(path) for path in (READY, ACTUAL, REBUILT, FINAL, Path(__file__))}}
    checkpoint(mutation=RESEARCH/'verified_checkpoint_v1', batch_key=KEY,
        batch_updates=dict(new_credit=0, all_individual_five_research_gates_pass=True, fifth_formatting_gate_pending=False,
            stored_checks_pending=False, focused_gameplay_pending=False, registered_integration_pending=True,
            full_intake_not_complete=True, source_speech_variants=263, typed_captions=7, complete_body_pages=279,
            scoped_public_names=26, observed_speeches=86, observed_pages=94, observed_menus=3, observed_headers=16,
            offline_only_speeches=177, offline_only_captions=0, final_review=str(FINAL), final_review_sha256=digest(FINAL),
            research_completion=str(READY), research_completion_sha256=digest(READY), evidence=evidence),
        additional_updates={'editorial_execution_priority_20261104': dict(new_credit=0,
            current_batch='Rafael B221–B240 registered cumulative integration.',
            next_action='Register the exact mixed speech, voice and menu transaction, then verify its clean-input patch and startup.',
            current_batch_not_yet_integrated=True, native_job_live=False, registered_build_live=False, guide_photos=False)},
        summary=summary, document='docs/editorial_Rafael_B221_B240_research_ready_20261106.md', document_text=doc,
        completed=14797, protected={str(REGISTRY):registered['registry_sha256'],
            registered['canonical_base']:registered['canonical_sha256'], registered['candidate']:registered['candidate_sha256'],
            registered['patch']:registered['patch_sha256'], package['zip']:package['zip_sha256'],
            rebuilt['research_ROM']:rebuilt['research_ROM_sha256']})
    print('Recorded the complete 270-record research checkpoint with zero new registered credit.')


if __name__ == '__main__':
    main()

